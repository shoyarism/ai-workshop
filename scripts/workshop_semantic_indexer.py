#!/usr/bin/env python3
"""
Workshop Hybrid Semantic & Vector Indexer (Horizon 1: Neural Cognitive Engine)
=============================================================================
Indexes 884+ Domain Skills and all Obsidian Second Brain Vault notes using:
  1. Dense Semantic Vector Embeddings (ONNX FastEmbed: BAAI/bge-small-en-v1.5)
  2. Sparse Lexical Search (SQLite FTS5 + BM25 ranking)
  3. Reciprocal Rank Fusion (RRF) for superior hybrid retrieval.

Usage:
    python scripts/workshop_semantic_indexer.py index [--dense]
    python scripts/workshop_semantic_indexer.py search "<query>" [--limit 10] [--mode hybrid|dense|sparse]
"""

import sys
import re
import json
import sqlite3
import hashlib
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError, OSError):  # @court-exempt: console encoding fallback
        pass

SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSHOP_DIR = SCRIPTS_DIR.parent
VAULT_DIR = WORKSHOP_DIR / "vault"
DB_PATH = SCRIPTS_DIR / ".workshop_skills.db"

SKILL_PATHS = [
    WORKSHOP_DIR / "skills",
    WORKSHOP_DIR / "hyperframes" / "skills",
    WORKSHOP_DIR / "browser-use" / "skills",
    WORKSHOP_DIR / "ai-agents-handbook" / "packs" / "ponytail" / "skills",
    WORKSHOP_DIR / "ai-agents-handbook" / "packs" / "styleseed" / "skills",
    WORKSHOP_DIR / "ai-agents-handbook" / "packs" / "garden-skills" / "skills",
    WORKSHOP_DIR / "ai-agents-handbook" / "packs" / "baoyu-design" / "skills",
    WORKSHOP_DIR / "ai-agents-handbook" / "packs" / "karpathy" / "skills",
    WORKSHOP_DIR / "ai-agents-handbook" / "packs" / "universal" / "skills",
]

# FastEmbed lazy loader
_embedding_model = None


def get_embedding_model():
    """Lazily load FastEmbed TextEmbedding model."""
    global _embedding_model
    if _embedding_model is None:
        try:
            from fastembed import TextEmbedding

            _embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
        except Exception:
            return None
    return _embedding_model


def extract_skill_metadata(skill_md_path: Path) -> Optional[Dict[str, Any]]:
    """Parse YAML frontmatter, title, and description from a SKILL.md."""
    try:
        content = skill_md_path.read_text(encoding="utf-8", errors="replace")
        name = skill_md_path.parent.name
        desc = ""
        body = ""

        # Check YAML frontmatter (--- ... ---)
        frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if frontmatter_match:
            fm_text = frontmatter_match.group(1)
            try:
                fm_data = yaml.safe_load(fm_text) or {}
                name = str(fm_data.get("name") or name).strip()
                desc = " ".join(str(fm_data.get("description") or "").split())
            except yaml.YAMLError:
                # Fallback to regex if YAML parsing fails
                name_m = re.search(
                    r"^name:\s*['\"]?(.*?)['\"]?\s*$", fm_text, re.MULTILINE
                )
                desc_m = re.search(
                    r"^description:\s*['\"]?(.*?)['\"]?\s*$", fm_text, re.MULTILINE
                )
                if name_m:
                    name = name_m.group(1).strip()
                if desc_m:
                    desc = desc_m.group(1).strip()
            body = content[frontmatter_match.end() :][:2000]
        else:
            lines = [
                l.strip()
                for l in content.splitlines()
                if l.strip() and not l.startswith("#")
            ]
            desc = lines[0] if lines else "Domain skill specification."
            body = content[:2000]

        return {
            "type": "skill",
            "name": name,
            "description": desc,
            "body": body,
            "path": str(skill_md_path.relative_to(WORKSHOP_DIR)).replace("\\", "/"),
            "full_path": str(skill_md_path).replace("\\", "/"),
        }
    except Exception:
        return None


def extract_vault_metadata(vault_md_path: Path) -> Optional[Dict[str, Any]]:
    """Parse YAML frontmatter, title, and content from an Obsidian vault note."""
    try:
        content = vault_md_path.read_text(encoding="utf-8", errors="replace")
        name = vault_md_path.stem
        desc = ""
        body = ""

        frontmatter_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if frontmatter_match:
            fm_text = frontmatter_match.group(1)
            title_m = re.search(
                r"^title:\s*['\"]?(.*?)['\"]?\s*$", fm_text, re.MULTILINE
            )
            type_m = re.search(r"^type:\s*['\"]?(.*?)['\"]?\s*$", fm_text, re.MULTILINE)
            tags_m = re.search(r"^tags:\s*\[(.*?)\]", fm_text, re.MULTILINE)

            if title_m:
                name = title_m.group(1).strip()
            note_type = type_m.group(1).strip() if type_m else "note"
            tags = tags_m.group(1).strip() if tags_m else ""
            desc = f"Obsidian Second Brain [{note_type}] tags: {tags}"
            body = content[frontmatter_match.end() :][:2000]
        else:
            desc = "Obsidian Second Brain Note"
            body = content[:2000]

        return {
            "type": "vault",
            "name": name,
            "description": desc,
            "body": body,
            "path": str(vault_md_path.relative_to(WORKSHOP_DIR)).replace("\\", "/"),
            "full_path": str(vault_md_path).replace("\\", "/"),
        }
    except Exception:
        return None


def init_db() -> sqlite3.Connection:
    """Initialize the SQLite database with FTS5 and vector embedding tables."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY,
            item_type TEXT,
            name TEXT,
            description TEXT,
            body TEXT,
            path TEXT UNIQUE,
            full_path TEXT,
            hash TEXT,
            embedding BLOB
        )
    """)
    conn.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS items_fts USING fts5(
            name,
            description,
            body,
            path,
            content='items',
            content_rowid='id'
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_items_path ON items(path)")
    conn.commit()
    return conn


def index_all(dense: bool = True) -> Dict[str, Any]:
    """Scan and index all skills and vault notes with optional dense embeddings."""
    import numpy as np

    conn = init_db()

    # Collect all items
    items = []
    seen = set()

    # 1. Collect all skills recursively via workshop_skills.discover()
    import workshop_skills
    for s in workshop_skills.discover():
        meta = extract_skill_metadata(s.path)
        if meta:
            items.append(meta)

    # 2. Collect vault notes
    if VAULT_DIR.exists():
        for note in VAULT_DIR.rglob("*.md"):
            if (
                not any(part.startswith(".") for part in note.parts)
                and note not in seen
            ):
                seen.add(note)
                meta = extract_vault_metadata(note)
                if meta:
                    items.append(meta)

    # Check embedding model
    embed_model = get_embedding_model() if dense else None
    dense_enabled = embed_model is not None

    print(
        f"[*] Total items to index: {len(items)} (Dense Vector Embeddings: {'ENABLED' if dense_enabled else 'DISABLED'})"
    )

    # Generate embeddings in batch if enabled
    embeddings = None
    if dense_enabled:
        texts_to_embed = [
            f"{it['name']}: {it['description']}\n{it['body'][:500]}" for it in items
        ]
        print("[*] Computing FastEmbed BAAI/bge-small-en-v1.5 dense vectors...")
        try:
            embeddings_gen = embed_model.embed(texts_to_embed)
            embeddings = list(embeddings_gen)
            print(
                f"[+] Computed {len(embeddings)} dense embeddings (dim: {len(embeddings[0])})."
            )
        except Exception as e:
            print(
                f"[!] Embedding computation error: {e}. Falling back to sparse indexing."
            )
            dense_enabled = False

    # Clear old tables
    conn.execute("DELETE FROM items")
    conn.execute("DELETE FROM items_fts")

    # Insert items
    for idx, it in enumerate(items):
        content_hash = hashlib.md5(
            (it["name"] + it["description"] + it["body"]).encode("utf-8")
        ).hexdigest()
        emb_blob = None
        if dense_enabled and embeddings and idx < len(embeddings):
            emb_blob = np.array(embeddings[idx], dtype=np.float32).tobytes()

        cur = conn.execute(
            """INSERT INTO items (item_type, name, description, body, path, full_path, hash, embedding)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                it["type"],
                it["name"],
                it["description"],
                it["body"],
                it["path"],
                it["full_path"],
                content_hash,
                emb_blob,
            ),
        )
        rowid = cur.lastrowid
        conn.execute(
            """INSERT INTO items_fts (rowid, name, description, body, path)
               VALUES (?, ?, ?, ?, ?)""",
            (rowid, it["name"], it["description"], it["body"], it["path"]),
        )

    conn.commit()
    conn.close()

    return {
        "status": "success",
        "total_indexed": len(items),
        "dense_embeddings": dense_enabled,
        "database": str(DB_PATH),
    }


def search(query: str, limit: int = 10, mode: str = "hybrid") -> List[Dict[str, Any]]:
    """Execute hybrid, dense, or sparse search."""
    import numpy as np

    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row

    # Clean query for FTS5 (remove special syntax characters that break FTS5)
    clean_fts_query = re.sub(r"[^\w\s]", " ", query).strip()
    clean_fts_query = " ".join(clean_fts_query.split())

    # 1. Sparse FTS5 BM25 search
    sparse_ranks: Dict[int, float] = {}
    if clean_fts_query and mode in ("hybrid", "sparse"):
        # Match words with wildcard suffix for prefix matching
        terms = [f'"{term}"*' for term in clean_fts_query.split() if term]
        fts_match_expr = " AND ".join(terms) if terms else clean_fts_query
        try:
            sql = """
                SELECT id, bm25(items_fts) as rank
                FROM items_fts
                JOIN items ON items_fts.rowid = items.id
                WHERE items_fts MATCH ?
                ORDER BY rank
                LIMIT 50
            """
            cur = conn.execute(sql, (fts_match_expr,))
            for row in cur.fetchall():
                sparse_ranks[row["id"]] = float(row["rank"])
        except Exception:  # @court-exempt: handled fallback
            pass

    # 2. Dense Semantic Vector search
    dense_scores: Dict[int, float] = {}
    embed_model = get_embedding_model() if mode in ("hybrid", "dense") else None
    if embed_model is not None:
        try:
            query_emb = list(embed_model.embed([query]))[0]
            query_vec = np.array(query_emb, dtype=np.float32)
            query_norm = np.linalg.norm(query_vec)
            if query_norm > 0:
                query_vec = query_vec / query_norm

            # Fetch stored embeddings
            cur = conn.execute(
                "SELECT id, embedding FROM items WHERE embedding IS NOT NULL"
            )
            rows = cur.fetchall()
            if rows:
                ids = [r["id"] for r in rows]
                mat = np.array(
                    [np.frombuffer(r["embedding"], dtype=np.float32) for r in rows]
                )
                # Compute cosine similarities
                norms = np.linalg.norm(mat, axis=1, keepdims=True)
                norms[norms == 0] = 1.0
                normalized_mat = mat / norms
                similarities = np.dot(normalized_mat, query_vec)

                for item_id, sim in zip(ids, similarities):
                    dense_scores[item_id] = float(sim)
        except Exception:  # @court-exempt: handled fallback
            pass

    # 3. Reciprocal Rank Fusion (RRF) / Hybrid scoring
    all_candidate_ids = set(sparse_ranks.keys()) | set(dense_scores.keys())

    # If no results from FTS or Dense, fallback to LIKE query
    if not all_candidate_ids:
        cur = conn.execute(
            "SELECT id FROM items WHERE name LIKE ? OR description LIKE ? LIMIT ?",
            (f"%{query}%", f"%{query}%", limit),
        )
        for r in cur.fetchall():
            all_candidate_ids.add(r["id"])
            dense_scores[r["id"]] = 0.5

    scored_items = []
    # Sort sparse ranks ascending (BM25 lower is better)
    sorted_sparse = sorted(sparse_ranks.items(), key=lambda x: x[1])
    sparse_rrf_rank = {
        item_id: idx + 1 for idx, (item_id, _) in enumerate(sorted_sparse)
    }

    # Sort dense scores descending (Cosine similarity higher is better)
    sorted_dense = sorted(dense_scores.items(), key=lambda x: x[1], reverse=True)
    dense_rrf_rank = {item_id: idx + 1 for idx, (item_id, _) in enumerate(sorted_dense)}

    # Fetch paths to apply archive ranking attenuation
    cand_placeholders = ",".join("?" for _ in all_candidate_ids)
    cur = conn.execute(
        f"SELECT id, path FROM items WHERE id IN ({cand_placeholders})",  # @court-exempt: parameterized query placeholders
        list(all_candidate_ids),
    )
    cand_paths = {r["id"]: r["path"] for r in cur.fetchall()}

    k = 60  # Standard RRF constant
    for item_id in all_candidate_ids:
        score = 0.0
        if item_id in sparse_rrf_rank:
            score += 1.0 / (k + sparse_rrf_rank[item_id])
        if item_id in dense_rrf_rank:
            score += (
                1.0 / (k + dense_rrf_rank[item_id])
            ) * 1.5  # Weight semantic slightly higher

        # Archive ranking attenuation: preserve search recall while ranking below active records
        p = cand_paths.get(item_id, "")
        if "99 - Archive" in p or "Archive/" in p:
            score *= 0.5

        cosine_sim = dense_scores.get(item_id, 0.0)
        scored_items.append((item_id, score, cosine_sim))

    scored_items.sort(key=lambda x: x[1], reverse=True)
    top_candidates = scored_items[:limit]

    # Fetch full item details
    results = []
    if top_candidates:
        placeholders = ",".join("?" for _ in top_candidates)
        cand_ids = [c[0] for c in top_candidates]
        cur = conn.execute(
            f"SELECT id, item_type, name, description, path, full_path, body FROM items WHERE id IN ({placeholders})",  # @court-exempt: parameterized query placeholders
            cand_ids,
        )
        items_by_id = {r["id"]: dict(r) for r in cur.fetchall()}
        for item_id, rrf_score, cos_sim in top_candidates:
            if item_id in items_by_id:
                record = items_by_id[item_id]
                record["rrf_score"] = round(rrf_score, 4)
                record["semantic_similarity"] = round(cos_sim, 4)
                results.append(record)

    conn.close()
    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Workshop Hybrid Semantic & Vector Indexer"
    )
    subparsers = parser.add_subparsers(dest="action")

    # index
    p_index = subparsers.add_parser("index", help="Index all skills and vault notes")
    p_index.add_argument(
        "--no-dense", action="store_true", help="Skip dense vector embeddings"
    )

    # search
    p_search = subparsers.add_parser("search", help="Execute hybrid semantic search")
    p_search.add_argument("query", help="Query string")
    p_search.add_argument("--limit", type=int, default=10, help="Max results")
    p_search.add_argument(
        "--mode", choices=["hybrid", "dense", "sparse"], default="hybrid"
    )
    p_search.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.action == "index":
        res = index_all(dense=not getattr(args, "no_dense", False))
        print(json.dumps(res, indent=2))
    elif args.action == "search":
        results = search(args.query, limit=args.limit, mode=args.mode)
        if getattr(args, "json", False):
            print(json.dumps(results, indent=2))
        else:
            print("\n=======================================================")
            print(
                f" 🔍 WORKSHOP HYBRID SEARCH: '{args.query}' (Mode: {args.mode.upper()})"
            )
            print(f" Returned {len(results)} top results")
            print("=======================================================\n")
            for r in results:
                kind = f"[{r['item_type'].upper()}]"
                sim_str = (
                    f"Similarity: {r['semantic_similarity'] * 100:.1f}%"
                    if r.get("semantic_similarity")
                    else ""
                )
                print(f" • {kind:<8} {r['name']} ({sim_str})")
                print(f"   Path: {r['path']}")
                print(f"   Desc: {r['description'][:110]}...\n")
            print("=======================================================\n")
    else:
        results = search(sys.argv[1] if len(sys.argv) > 1 else "search", limit=10)
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
