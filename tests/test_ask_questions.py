from jc.ask_questions import generate_clarifying_questions


def test_generate_clarifying_questions_mock():
    sample_meta = {
        "workspaceId": "test-ws",
        "README": "# Example project\nThis is a tiny README for testing.",
        "top_files": ["src/main.py", "README.md"],
        "top_languages": [{"lang": "Python", "count": 5}],
        "recent_commits": ["Initial commit"],
    }
    questions = generate_clarifying_questions(sample_meta)
    assert isinstance(questions, list)
    assert len(questions) >= 1
    # Ensure items are short strings
    assert all(isinstance(q, str) and len(q) < 400 for q in questions)
