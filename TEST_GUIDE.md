# JC Agent - Complete Testing Guide

🔷 **Diamond Polish Edition** - E2E Testing for Production Readiness

## Quick Test (30 seconds)

```bash
# Test 1: Import check
python -c "from jc import JCState, JCFlow, run_flow, FLOWS; print('✓ JC Runtime OK')"

# Test 2: Create state
python -c "from jc import JCState; s = JCState(messages=[]); print(f'✓ State: {s.thread_id[:8]}')"

# Test 3: List flows
python -c "from jc import FLOWS; print(f'✓ Flows: {list(FLOWS.keys())}')"
```

## Full Test Suite

### Test 1: Module Imports

```python
from jc import (
    JCState, JCStep, JCFlow,
    run_flow, save_checkpoint, load_checkpoint,
    FLOWS
)
from agent_api import app, run_flow as api_run_flow
print("✓ All imports successful")
```

### Test 2: JCState Operations

```python
state = JCState(
    messages=[{"role": "user", "content": "Test"}],
    tasks=[{"id": 1, "task": "Test task"}],
    profile={"name": "tester"}
)

assert state.thread_id, "Thread ID not generated"
assert len(state.messages) == 1
assert len(state.tasks) == 1
print(f"✓ JCState working: {state.thread_id[:8]}...")
```

### Test 3: Checkpoint System

```python
from jc import JCState, save_checkpoint, load_checkpoint

# Create and save
test_state = JCState(messages=[{"role": "user", "content": "Checkpoint test"}])
thread_id = test_state.thread_id
save_checkpoint(test_state)

# Load and verify
loaded = load_checkpoint(thread_id)
assert loaded.thread_id == thread_id
assert len(loaded.messages) == 1
print(f"✓ Checkpoints: saved & loaded {thread_id[:8]}...")
```

### Test 4: Flow Execution

```python
from jc import run_flow

result = run_flow("research_then_summarize", {
    "messages": [{"role": "user", "content": "Research AI agents"}]
})

assert result['flow_id'] == 'research_then_summarize'
assert len(result['step_history']) == 3  # plan, research, summarize
assert len(result['messages']) >= 2
print(f"✓ Flow executed: {len(result['step_history'])} steps")
```

### Test 5: API Integration

```python
from fastapi.testclient import TestClient
from agent_api import app

client = TestClient(app)

# Health check
response = client.get("/health")
assert response.status_code == 200
assert response.json()["status"] == "ok"

# Flow endpoint
response = client.post("/api/flows/run", json={
    "flow_name": "research_then_summarize",
    "input": {"messages": [{"role": "user", "content": "Test"}]}
})
assert response.status_code == 200
print("✓ API endpoints functional")
```

## Production Deployment Tests

### Windows One-Click Test

```cmd
REM Test installer
EASY_INSTALL.bat

REM Test launcher
start_jc.bat

REM Verify API is running
curl http://localhost:8000/health
```

### API Endpoint Tests

```bash
# Start server
python agent_api.py &

# Test health
curl http://localhost:8000/health

# Test chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello JC"}]}'

# Test flow
curl -X POST http://localhost:8000/api/flows/run \
  -H "Content-Type: application/json" \
  -d '{"flow_name":"research_then_summarize","input":{"messages":[{"role":"user","content":"Research Python"}]}}'
```

## Automated E2E Test Script

Save as `test_jc_full.py`:

```python
#!/usr/bin/env python3
import sys
import time
from pathlib import Path

print("🔷 JC Agent - Full E2E Test Suite\n" + "="*60)

tests_passed = 0
tests_total = 6

try:
    # Test 1: Imports
    print("[1/6] Testing imports...")
    from jc import JCState, JCFlow, run_flow, save_checkpoint, load_checkpoint, FLOWS
    import agent_api
    tests_passed += 1
    print("✓ PASS\n")
    
    # Test 2: State creation
    print("[2/6] Testing JCState...")
    state = JCState(messages=[{"role":"user","content":"test"}])
    assert state.thread_id
    tests_passed += 1
    print(f"✓ PASS - thread_id: {state.thread_id[:8]}...\n")
    
    # Test 3: Checkpoints
    print("[3/6] Testing checkpoints...")
    save_checkpoint(state)
    loaded = load_checkpoint(state.thread_id)
    assert loaded.thread_id == state.thread_id
    tests_passed += 1
    print("✓ PASS - saved & loaded\n")
    
    # Test 4: Flow list
    print("[4/6] Testing flows...")
    assert "research_then_summarize" in FLOWS
    tests_passed += 1
    print(f"✓ PASS - flows: {list(FLOWS.keys())}\n")
    
    # Test 5: Flow execution
    print("[5/6] Testing flow execution...")
    result = run_flow("research_then_summarize", {
        "messages": [{"role":"user","content":"Test query"}]
    })
    assert result['flow_id'] == 'research_then_summarize'
    tests_passed += 1
    print(f"✓ PASS - {len(result['step_history'])} steps executed\n")
    
    # Test 6: Data persistence
    print("[6/6] Testing data directory...")
    assert Path("./data/checkpoints").exists()
    tests_passed += 1
    print("✓ PASS - checkpoint dir exists\n")
    
except Exception as e:
    print(f"✗ FAIL: {e}\n")
    import traceback
    traceback.print_exc()

print("="*60)
print(f"Results: {tests_passed}/{tests_total} tests passed")
if tests_passed == tests_total:
    print("\n🏆 ALL TESTS PASSED - JC IS DIAMOND POLISHED! 💎")
    sys.exit(0)
else:
    print("\n⚠️  Some tests failed")
    sys.exit(1)
```

## Performance Benchmarks

```python
import time
from jc import run_flow

# Benchmark flow execution
start = time.time()
result = run_flow("research_then_summarize", {
    "messages": [{"role":"user","content":"Benchmark test"}]
})
duration = time.time() - start

print(f"Flow execution: {duration:.2f}s")
print(f"Steps: {len(result['step_history'])}")
for step in result['step_history']:
    print(f"  - {step['step']}: {step.get('duration_sec', 0):.3f}s")
```

## Troubleshooting

### Import Errors

```bash
# Missing dependencies
pip install -r requirements.txt

# Module not found
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Flow Errors

```python
# Check available flows
from jc import FLOWS
print(list(FLOWS.keys()))

# Validate input format
flow_input = {
    "messages": [{"role": "user", "content": "Your query"}],
    "thread_id": "optional-resume-thread"
}
```

### API Errors

```bash
# Check server is running
curl http://localhost:8000/health

# Check logs
tail -f jc_agent.log

# Restart server
pkill -f agent_api.py
python agent_api.py
```

## CI/CD Integration

### GitHub Actions

```yaml
name: JC Agent Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python test_jc_full.py
```

---

✨ **All tests passing = JC is production-ready!**

💎 **Diamond Standard**: JC beats LangGraph, AutoGen, CrewAI with desktop UX + complete runtime
