"""
Multi-Agent Architecture Example for JC-Agent

This module demonstrates a pattern where specialized agents collaborate to handle complex tasks.
Each agent is a class with a clear responsibility. A central Orchestrator coordinates their work.
"""

from typing import Any, Dict

class BrainAgent:
    def get_context(self, user_message: str) -> Dict[str, Any]:
        # Simulate retrieving context from memory
        return {"personality": "friendly", "history": [user_message]}

    def log_conversation(self, user_message: str, response: str):
        print(f"[Brain] Logged: {user_message} -> {response}")

class VoiceAgent:
    def speak(self, text: str):
        print(f"[Voice] {text}")

    def listen(self) -> str:
        return input("[Voice] You: ")

class ResearchAgent:
    def search(self, query: str) -> str:
        # Simulate a web search
        return f"[Research] Results for '{query}'"

class TaskAgent:
    def process(self, user_message: str, context: Dict[str, Any]) -> str:
        # Simulate task processing
        if "research" in user_message.lower():
            return "research"
        return f"[Task] Processed: {user_message} with context {context}"

class Orchestrator:
    def __init__(self):
        self.brain = BrainAgent()
        self.voice = VoiceAgent()
        self.research = ResearchAgent()
        self.task = TaskAgent()

    def run(self):
        self.voice.speak("Hello! How can I help you today?")
        user_message = self.voice.listen()
        context = self.brain.get_context(user_message)
        task_type = self.task.process(user_message, context)
        if task_type == "research":
            result = self.research.search(user_message)
            self.voice.speak(result)
            self.brain.log_conversation(user_message, result)
        else:
            self.voice.speak(task_type)
            self.brain.log_conversation(user_message, task_type)

if __name__ == "__main__":
    Orchestrator().run()
