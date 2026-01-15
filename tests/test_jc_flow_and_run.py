import uuid
from jc import JCFlow, JCStep, JCState, save_checkpoint, load_checkpoint
from pathlib import Path


def test_jcflow_runs_steps(tmp_path):
    # Simple handlers
    def handler_a(state):
        state.messages.append({"role": "assistant", "content": "A done"})
        return state

    def handler_b(state):
        state.messages.append({"role": "assistant", "content": "B done"})
        return state

    steps = {
        "a": JCStep("a", handler_a, ["b"]),
        "b": JCStep("b", handler_b, []),
    }

    # Use empty terminal_steps so flow runs until a step has no next_steps
    flow = JCFlow(flow_id="f1", initial_step="a", steps=steps, terminal_steps=[])
    state = JCState(thread_id=str(uuid.uuid4()))
    state = flow.run(state)

    assert any(m.get("content") == "A done" for m in state.messages)
    assert any(m.get("content") == "B done" for m in state.messages)


def test_checkpoint_save_and_load(tmp_path, monkeypatch):
    # Use a temporary checkpoint dir to avoid polluting repo
    monkeypatch.setattr("jc.CHECKPOINT_DIR", tmp_path)

    state = JCState(thread_id="check-1")
    state.messages = [{"role": "user", "content": "hello"}]

    save_checkpoint(state)
    loaded = load_checkpoint("check-1")
    assert loaded is not None
    assert loaded.thread_id == state.thread_id
    assert loaded.messages == state.messages

