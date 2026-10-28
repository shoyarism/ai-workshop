import re
import json

def test_json_schemas():
    with open(r'C:\Users\Ideapad\.gemini\antigravity\scratch\website_recon_prompt\OUTPUT_SCHEMAS.md', 'r', encoding='utf-8') as f:
        text = f.read()

    json_blocks = re.findall(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    print(f"Found {len(json_blocks)} JSON blocks in OUTPUT_SCHEMAS.md")

    for i, block in enumerate(json_blocks, 1):
        try:
            data = json.loads(block)
            title = data.get("title", f"Block_{i}")
            print(f"  Block {i} ({title}): VALID JSON")
        except Exception as e:
            print(f"  Block {i}: INVALID JSON - {e}")

if __name__ == "__main__":
    test_json_schemas()
