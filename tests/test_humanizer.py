import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from engine.humanizer import HumanizerEngine

def test_humanizer():
    h = HumanizerEngine()
    ai_sample = (
        "In today's digital age, this groundbreaking tool serves as a testament to human innovation. "
        "We must delve into the intricate tapestry of modern technologies to foster robust synergies. "
        "The future looks bright. I hope this helps!"
    )

    print("=== Original AI Text ===")
    print(ai_sample)

    scan_res = h.scan(ai_sample)
    print(f"\nAI Tells Detected: {scan_res['total_detections']} | AI Tell Score: {scan_res['ai_score']}/100")
    for f in scan_res["findings"]:
        print(f"  [{f['tier']}] '{f['match']}' -> {f['description']}")

    humanized = h.humanize(ai_sample)
    print("\n=== Surgical Humanized Output ===")
    print(humanized)

if __name__ == "__main__":
    test_humanizer()
