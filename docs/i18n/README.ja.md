# WORKSHOP // OS

<div align="center">
  <img src="../../assets/logo.svg" alt="Workshop OS Logo" width="440">
  <p><strong>AIコーディングエージェントのための決定論的実行基盤＆コード品質法廷</strong></p>

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](../../LICENSE)
[![Python 3.11 | 3.12](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](../../pyproject.toml)
[![Quality Gate](https://img.shields.io/badge/Slop_Court-v3.5_Armed-eb5e28.svg)](../../scripts/workshop_court.py)

[English](../../README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [Español](README.es.md)

</div>

<br>

<div align="center">
  <img src="../../assets/hero-banner.svg?v=3.5.0" alt="Workshop OS アーキテクチャ図" width="100%">
</div>

<br>

<p align="center">
  <code>仕様: WORKSHOP-OS-3.5</code> &nbsp;•&nbsp;
  <code>ライセンス: APACHE-2.0</code> &nbsp;•&nbsp;
  <code>7つの主権領土</code> &nbsp;•&nbsp;
  <code>2,147の検証済みスキル</code> &nbsp;•&nbsp;
  <code>品質法廷: v3.5 稼働</code>
</p>

---

## 01 // クイックスタート (60秒でセットアップ)

### オプション A: ローカル環境セットアップ (推奨)

`uv` (推奨) または通常の `pip` を選択してください:

```bash
# 1. リポジトリをクローン
git clone https://github.com/shoyarism/ai-workshop.git
cd ai-workshop

# 2. 依存関係のインストール (どちらか1つ)
uv sync                 # uvを使用する場合
pip install -e .        # pipを使用する場合

# 3. Gitプリコミット監視員 (Git Bailiff) の有効化
workshop court bailiff install

# 4. ヘルスチェックとテストの実行
workshop doctor --strict
pytest tests
```

### オプション B: ゼロクローン クラウドプロトコル (Zero-Clone)

一時的なコンテナ環境やリモートサーバーでは、`curl` を用いてスキルを直接エージェントコンテキストに読み込みます:

```bash
curl -fsSL https://raw.githubusercontent.com/shoyarism/ai-workshop/main/skills/dev-house/using-superpowers/SKILL.md
```

---

## 02 // 7つの主権領土 (Sovereign Houses)

コンテキストウィンドウの過負荷を防ぐため、Workshop OSは **2,147の検証済みスキル** を7つの専門領域にモジュール化しています:

| 主権領土 | 管轄領域と焦点 | 代表的なツール | 検証済み容量 |
| :--- | :--- | :--- | :---: |
| **🛡️ 01 セキュリティ領土** | 防御的監視、インシデント対応、AST拘束、ペネトレーションテスト | `slop-court` v3.5, `git-bailiff`, `digital-forensics` | **835 スキル** |
| **⚡ 02 開発領土** | TDD、厳格な型付け、ASTリファクタリング、不要コード削除 | `superpowers`, `matt-pocock`, `karpathy-skills`, `ast-grep` | **357 スキル** |
| **🎬 03 メディア領土** | プログラマブル動画生成、FLUX光学、Remotion/HyperFrames | `hyperframes`, `OpenMontage`, `photoreal-studio`, `remotion` | **178 スキル** |
| **🏎️ 04 運用・トークン領土** | 仕様駆動開発 (SDD)、トークン圧縮、スタートアップチーム模倣 | `caveman` (トークン70%削減), `headroom`, `gsd`, `gstack` | **166 スキル** |
| **🎨 05 デザイン領土** | タイポグラフィ規律、AIスロップ排除、デザイントークン | `ui-ux-pro-max`, `design-taste`, `impeccable`, `archify` | **132 スキル** |
| **🔬 06 インテリジェンス領土** | コード知識グラフ、ゼロコストスクレイピング、直近30日インテル | `graphify`, `agent-reach`, `last-30-days`, `rea` | **90 スキル** |
| **📢 07 グロース領土** | 人間的なトーン、価値提案、技術的SEO、プロダクトローンチ | `humanizer`, `marketing-skills`, `brand-voice` | **79 スキル** |

---

## 03 // マスターコマンド

```bash
workshop doctor --strict               # 41系統の自動診断プローブ
workshop search "<キーワード>"         # 2,147スキルからの全文検索
workshop court trial --staged          # ステージ済み差分の品質法廷裁判
workshop court council "<論題>"        # 4人格による敵対的アーキテクチャ審議
```
