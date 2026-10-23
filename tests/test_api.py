from fastapi.testclient import TestClient
from server.main import app

def test_api():
    client = TestClient(app)
    
    print("\n1. Testing /api/health...")
    res = client.get("/api/health")
    print("Health response:", res.json())
    assert res.status_code == 200

    print("\n2. Testing /api/check...")
    check_payload = {"text": "She do not knows how to writes clean codes."}
    res = client.post("/api/check", json=check_payload)
    data = res.json()
    print("Corrected:", data["corrected_text"])
    print("Total issues:", data["total_issues"])
    assert res.status_code == 200
    assert data["total_issues"] > 0

    print("\n3. Testing /api/paraphrase...")
    para_payload = {
        "text": "Although the team faced obstacles, they completed the project in a timely manner.",
        "mode": "formal",
        "synonym_level": 2
    }
    res = client.post("/api/paraphrase", json=para_payload)
    data = res.json()
    print("Paraphrased:", data["paraphrased_text"])
    print("Alternatives count:", len(data["alternatives"]))
    print("Diff tokens count:", len(data["alternatives"][0]["diff_tokens"]))
    assert res.status_code == 200

    print("\nAll API tests PASSED successfully!")

if __name__ == "__main__":
    test_api()
