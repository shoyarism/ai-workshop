import sys
import os

def test_verification_matrix_snippets():
    matrix_path = r'C:\Users\Ideapad\.gemini\antigravity\scratch\website_recon_prompt\VERIFICATION_MATRIX.md'
    with open(matrix_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"File length: {len(content)} chars")
    assert "S_{total}" in content or "S_{\\text{total}}" in content, "Mathematical model missing"
    assert "Benchmark Scenario 1" in content, "Scenario 1 missing"
    assert "Benchmark Scenario 2" in content, "Scenario 2 missing"
    assert "Benchmark Scenario 3" in content, "Scenario 3 missing"
    assert "Benchmark Scenario 4" in content, "Scenario 4 missing"
    assert "Automated JSON Schema & Structural Validation Suite" in content, "Validation suite missing"

    print("SUCCESS: All key structural elements verified in VERIFICATION_MATRIX.md")

if __name__ == "__main__":
    test_verification_matrix_snippets()
