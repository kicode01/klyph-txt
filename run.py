import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("  klyph-txt Engine (v6.0)")
    print("  Autonomous Neurosymbolic Writing & Adversarial Humanizer")
    print("  Server running at: http://127.0.0.1:8000")
    print("=" * 60)
    uvicorn.run("server.main:app", host="127.0.0.1", port=8000, reload=False)
