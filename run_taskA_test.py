from jc.ask_questions import generate_clarifying_questions

sample_meta = {
    "workspaceId": "test-ws",
    "README": "# Example project\nThis is a tiny README for testing.",
    "top_files": ["src/main.py", "README.md"],
    "top_languages": [{"lang": "Python", "count": 5}],
    "recent_commits": ["Initial commit"],
}

questions = generate_clarifying_questions(sample_meta)

assert isinstance(questions, list), 'questions should be a list'
assert len(questions) >= 1, 'expected at least one question'
assert all(isinstance(q, str) and len(q) < 400 for q in questions), 'each question must be a short string'
print('TASK A TEST: PASS')
