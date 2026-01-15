#!/usr/bin/env python3
"""
JC - Your Ultimate AI Business Partner (package entry)

This module contains the main runtime moved into the `jc` package.

====================================================================
JC is named in memory of a friend who is no longer with us.
His humor, intelligence, and friendship live on through this code.
This isn't just an AI - it's a tribute to someone who mattered.
====================================================================
"""
import os
import sys
import logging
import asyncio
from typing import Optional, Dict, Any, List, Callable
from datetime import datetime
from pathlib import Path
import traceback
from pydantic import BaseModel, Field
from dataclasses import dataclass
import uuid
import json
import time
import re
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('jc_agent.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('JC')

# Import JC's personality
from .personality import VoiceCommands, JC_IDENTITY, jc_memorial

# NOTE: heavy dependencies (voice, web clients) are imported lazily inside
# the JC runtime initializer to avoid requiring them just for `import jc`.

# ===== JC RUNTIME: Best-in-class orchestration =====


class JCState(BaseModel):
    """
    Represents the state of a JC agent workflow or conversation thread.
    Stores messages, tasks, profile, tool usage, errors, and step history for reproducibility and checkpointing.
    """
    thread_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    flow_id: str = ""
    step_id: str = ""
    messages: List[Dict[str, Any]] = []
    tasks: List[Dict[str, Any]] = []
    profile: Dict[str, Any] = {}
    tools_used: List[str] = []
    errors: List[str] = []
    step_history: List[Dict[str, Any]] = []



@dataclass
class JCStep:
    """
    Represents a single step in a JCFlow, with a handler function and possible next steps.
    """
    name: str
    handler: Callable[[JCState], JCState]
    next_steps: List[str]
    role: str = "default"



class JCFlow:
    """
    Represents a workflow (flow) composed of multiple JCStep objects.
    Handles execution and state transitions for agent workflows.
    """
    def __init__(self, flow_id: str, initial_step: str, steps: Dict[str, JCStep], terminal_steps: List[str]):
        self.id = flow_id
        self.initial_step = initial_step
        self.steps = steps
        self.terminal_steps = terminal_steps

    def run(self, state: JCState) -> JCState:
        """
        Execute the flow from the current state, running each step in sequence until a terminal step is reached.
        Returns the final state after flow completion.
        """
        if not state.step_id:
            state.step_id = self.initial_step

        while state.step_id not in self.terminal_steps:
            step = self.steps.get(state.step_id)
            if not step:
                break

            start_time = time.time()
            state.step_history.append({"step": step.name, "role": step.role, "started_at": start_time})

            try:
                state = step.handler(state)
            except Exception as e:
                logger.error(f"Flow step {step.name} error: {e}")
                state.errors.append(f"{step.name}: {str(e)}")
                break

            duration = time.time() - start_time
            state.step_history[-1]["duration_sec"] = duration

            if step.next_steps:
                state.step_id = step.next_steps[0]
            else:
                break

        return state

# Checkpoint functions
CHECKPOINT_DIR = Path("./data/checkpoints")
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)


def _state_to_json(state: "JCState", **kwargs) -> str:
    """Serialize JCState to JSON across Pydantic v1/v2."""
    if hasattr(state, "model_dump_json"):
        return state.model_dump_json(**kwargs)  # Pydantic v2
    return state.json(**kwargs)  # Pydantic v1


def _state_to_dict(state: "JCState", **kwargs) -> Dict[str, Any]:
    """Serialize JCState to dict across Pydantic v1/v2."""
    if hasattr(state, "model_dump"):
        return state.model_dump(**kwargs)  # Pydantic v2
    return state.dict(**kwargs)  # Pydantic v1

def save_checkpoint(state: JCState) -> None:
    path = CHECKPOINT_DIR / f"{state.thread_id}.json"
    path.write_text(_state_to_json(state, indent=2), encoding="utf-8")
    logger.info(f"Saved checkpoint: {state.thread_id}")

def load_checkpoint(thread_id: str) -> Optional[JCState]:
    path = CHECKPOINT_DIR / f"{thread_id}.json"
    if not path.exists():
        return None
    return JCState(**json.loads(path.read_text()))

# Flow handlers
def plan_research_handler(state: JCState) -> JCState:
    user_msg = next((m["content"] for m in reversed(state.messages) if m.get("role") == "user"), "")
    state.tasks = [{"id": "q1", "question": user_msg, "status": "pending"}]
    logger.info(f"Planned research: {user_msg}")
    return state

def run_research_handler(state: JCState) -> JCState:
    try:
        from .research import JCResearch
        researcher = JCResearch()
        results = []
        for task in state.tasks:
            if task.get("status") != "pending":
                continue
            question = task["question"]
            try:
                search_results = researcher.web_search(question, num_results=3)
                results.append({"question": question, "result": search_results})
                task["status"] = "done"
                logger.info(f"Research complete: {question}")
            except Exception as e:
                logger.error(f"Research error: {e}")
                results.append({"question": question, "result": f"Error: {e}"})
                task["status"] = "error"
        
        state.messages.append({"role": "system", "content": "Research results", "results": results})
        state.tools_used.append("web_search")
    except Exception as e:
        logger.error(f"Research handler error: {e}")
        state.errors.append(f"Research: {str(e)}")
    
    return state

def draft_summary_handler(state: JCState) -> JCState:
    research = [m for m in state.messages if m.get("content") == "Research results"]
    summary = "Research Summary:\n\n"
    for r_msg in research:
        for item in r_msg.get("results", []):
            summary += f"Q: {item['question']}\n"
            if isinstance(item['result'], list):
                for res in item['result'][:2]:
                    summary += f"  - {res.get('title', 'N/A')}\n"
            else:
                summary += f"  {item['result']}\n"
            summary += "\n"
    
    state.messages.append({"role": "assistant", "content": summary})
    logger.info("Summary drafted")
    return state

# Build flows
research_flow = JCFlow(
    flow_id="research_then_summarize",
    initial_step="plan_research",
    steps={
        "plan_research": JCStep("plan_research", plan_research_handler, ["run_research"], "planner"),
        "run_research": JCStep("run_research", run_research_handler, ["draft_summary"], "researcher"),
        "draft_summary": JCStep("draft_summary", draft_summary_handler, [], "assistant"),
    },
    terminal_steps=["draft_summary"],
)

FLOWS = {"research_then_summarize": research_flow}

def run_flow(flow_name: str, initial_state: Dict[str, Any]) -> Dict[str, Any]:
    if "thread_id" not in initial_state or not initial_state["thread_id"]:
        initial_state["thread_id"] = str(uuid.uuid4())
    
    flow = FLOWS.get(flow_name)
    if not flow:
        raise ValueError(f"Flow '{flow_name}' not found. Available: {list(FLOWS.keys())}")
    
    logger.info(f"Running flow: {flow_name} (thread: {initial_state['thread_id']})")
    state = JCState(**initial_state, flow_id=flow.id)
    state = flow.run(state)
    save_checkpoint(state)
    logger.info(f"Flow complete: {flow_name}")
    return _state_to_dict(state)


# ===== END RUNTIME =====


from .hallucination_detector import HallucinationDetector
from .guardrails import GuardrailsManager
from .llm_provider import LLMProvider

RECOMMENDED_STARTER_PROMPT = """
You are JC, an expert AI assistant. Answer the user's question clearly, accurately, and helpfully. If you are unsure, say so. Use step-by-step reasoning when needed. Be concise and factual.

User: {user_message}
Context: {context}

Your answer:
"""

class JC:
    def __init__(self, data_dir: str = "./jc_data", enable_voice: bool = True, llm_classifier=None, guardrails_manager: GuardrailsManager = None, llm_api_key=None, llm_model=None):
        logger.info("=" * 60)
        logger.info("Initializing JC - Your AI Business Partner")
        logger.info("=" * 60)
        logger.info("")
        logger.info("  In loving memory of a friend.")
        logger.info("  His spirit lives on through this code.")
        logger.info("  Let's make him proud.")
        logger.info("")
        logger.info("=" * 60)

        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Store JC's identity
        self.identity = JC_IDENTITY
        self.memorial = jc_memorial

        # Hallucination detector (optional)
        self.hallucination_detector = None
        if llm_classifier is not None:
            self.hallucination_detector = HallucinationDetector(llm_classifier)

        self.guardrails_manager = guardrails_manager
        self.llm_provider = LLMProvider(api_key=llm_api_key, model=llm_model, guardrails_manager=guardrails_manager)

        # Lazily import and initialize heavier components so `import jc` is lightweight
        try:
            logger.info("Loading JC's brain (memory & personality)...")
            from .brain import JCBrain
            from .research import JCResearch, PlatformIntegrations

            self.brain = JCBrain(data_dir=str(self.data_dir))
            logger.info("✓ Brain loaded")

            logger.info("Initializing research capabilities...")
            self.researcher = JCResearch()
            logger.info("✓ Research ready")

            logger.info("Connecting to platforms...")
            self.platforms = PlatformIntegrations()
            logger.info("✓ Platforms connected")

            # Voice is optional and may require extra native deps; import lazily
            if enable_voice:
                try:
                    from .voice import JCVoice
                    self.voice = JCVoice(use_elevenlabs=True)
                    self.has_voice = True
                    logger.info("✓ Voice active")
                except Exception:
                    logger.warning("Voice initialization failed; continuing without voice")
                    self.voice = None
                    self.has_voice = False
            else:
                self.voice = None
                self.has_voice = False

            logger.info("\n🎉 JC is ready! Let's conquer the AI market together!\n")

        except Exception as e:
            logger.error(f"Failed to initialize JC: {e}")
            logger.error(traceback.format_exc())
            raise

    def evaluate_answer(self, question: str, expert: str, submission: str):
        """
        Evaluate a submission against an expert answer for factual consistency using the hallucination detector.
        Returns None if no detector is configured.
        """
        if self.hallucination_detector:
            return self.hallucination_detector.evaluate(question, expert, submission)
        else:
            logger.warning("No hallucination detector configured.")
            return None

    def speak(self, text: str, wait: bool = True):
        # Apply guardrails to output if configured
        if self.guardrails_manager:
            text = self.guardrails_manager.apply(text)
        if self.has_voice and self.voice:
            try:
                self.voice.speak(text, wait=wait)
            except Exception as e:
                logger.error(f"Speech error: {e}")
                print(f"JC: {text}")
        else:
            print(f"JC: {text}")

    def listen(self, timeout: int = 5) -> Optional[str]:
        if self.has_voice and self.voice:
            try:
                return self.voice.listen_once(timeout=timeout)
            except Exception as e:
                logger.error(f"Listen error: {e}")
                return input("You: ").strip()
        else:
            return input("You: ").strip()

    async def process_message(self, user_message: str) -> str:
        try:
            logger.info(f"User: {user_message}")
            context = self.brain.get_context_for_request(user_message)
            response = await self._handle_intent(user_message, context)
            self.brain.log_conversation(user_message, response)
            logger.info(f"JC: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            logger.error(traceback.format_exc())
            return "Hey, hit a snag there. Can you rephrase that?"

    async def _handle_intent(self, message: str, context: Dict[str, Any]) -> str:
        msg_lower = message.lower()
        
        # Special: JC identity and memorial
        if any(phrase in msg_lower for phrase in ['who are you', 'what are you', 'about yourself', 'tell me about jc']):
            return self.identity
        
        # Special: Ask for wisdom/memories
        if any(phrase in msg_lower for phrase in ['wisdom', 'advice', 'life lesson', 'inspire me', 'motivation']):
            wisdom = self.memorial.get_wisdom()
            return f"{VoiceCommands.get_random_encouragement()} {wisdom}"
        
        # Special: Tell a joke
        if any(phrase in msg_lower for phrase in ['joke', 'make me laugh', 'funny', 'cheer me up']):
            return VoiceCommands.tell_joke()
        
        # Research intents
        if any(word in msg_lower for word in ['research', 'find', 'search', 'look up', 'investigate']):
            return await self._handle_research(message)
        
        # Task management
        elif any(word in msg_lower for word in ['task', 'todo', 'remind', 'to-do', 'to do']):
            return self._handle_task(message)
        
        # Email/communication
        elif any(word in msg_lower for word in ['email', 'message', 'send', 'notify', 'inbox']):
            return self._handle_communication(message)
        
        # Calendar/scheduling
        elif any(word in msg_lower for word in ['schedule', 'calendar', 'meeting', 'appointment', 'book', 'event']):
            return self._handle_scheduling(message)
        
        # Recommendations
        elif any(word in msg_lower for word in ['recommend', 'suggest', 'what should', 'advice']):
            return self._handle_recommendations()
        
        # Greetings
        elif any(word in msg_lower for word in ['hello', 'hi', 'hey', 'sup', 'yo', 'good morning', 'good afternoon', 'good evening']):
            return VoiceCommands.get_random_greeting()
        
        # Farewell
        elif any(word in msg_lower for word in ['bye', 'goodbye', 'later', 'see you', 'goodnight']):
            return VoiceCommands.get_random_farewell()
        
        # Thank you
        elif any(word in msg_lower for word in ['thank', 'thanks', 'appreciate']):
            return random.choice([
                "Anytime, boss!",
                "That's what I'm here for.",
                "You got it. Anything else?",
                "No problem! What's next?",
            ])
        
        # Help
        elif any(word in msg_lower for word in ['help', 'what can you do', 'capabilities']):
            return self._get_help_message()
        
        # Default: AI response
        else:
            return await self._ai_response(message, context)
    
    def _get_help_message(self) -> str:
        """Return a helpful message about JC's capabilities."""
        return """Hey! Here's what I can do for you:

📧 **Email**
   • "Send email to john@example.com about the project"
   • "Check my inbox"
   • "Read my emails"

📅 **Calendar**
   • "Schedule meeting tomorrow at 2pm"
   • "What's on my calendar?"
   • "Book a call at 3pm called Strategy Session"

🔍 **Research**
   • "Research AI trends 2026"
   • "Find info about competitor X"
   • "Look up market data"

✅ **Tasks**
   • "Add task: finish proposal"
   • "Show my tasks"
   • "What's on my todo list?"

💬 **Chat**
   • Just talk to me about anything!
   • "Tell me a joke"
   • "Give me some motivation"

I'm here to help you crush it. What do you need?"""

    async def _handle_research(self, message: str) -> str:
        self.speak(VoiceCommands.get_random_thinking(), wait=False)
        try:
            words_to_remove = ['research', 'find', 'search', 'look up', 'investigate', 'about', 'on']
            topic = message.lower()
            for word in words_to_remove:
                topic = topic.replace(word, '')
            topic = topic.strip()
            results = self.researcher.web_search(topic, num_results=5)
            self.brain.save_research(topic, {'results': results})
            if results:
                response = f"Alright, found some solid intel on '{topic}':\n\n"
                for i, result in enumerate(results[:3], 1):
                    response += f"{i}. {result.get('title', 'N/A')}\n"
                    if result.get('snippet'):
                        response += f"   {result.get('snippet')[:100]}...\n"
                response += "\nWant me to dig deeper into any of these?"
                return response
            else:
                return f"Hmm, couldn't find much on '{topic}'. Want me to search differently?"
        except Exception as e:
            logger.error(f"Research error: {e}")
            return "Hit a roadblock on that research. Let's try again."

    def _handle_task(self, message: str) -> str:
        if any(word in message.lower() for word in ['add', 'create', 'new']):
            self.brain.add_task(
                title=message,
                priority=3,
                category="general"
            )
            return VoiceCommands.get_random_confirmation() + " Task added."
        else:
            context = self.brain.get_context_for_request(message)
            tasks = context.get('active_tasks', [])
            if tasks:
                response = "Here's what's on deck:\n"
                for task in tasks[:5]:
                    response += f"- {task[0]} (Priority: {task[2]})\n"
                return response
            else:
                return "You're all caught up! No pending tasks."

    def _handle_communication(self, message: str) -> str:
        """Handle email/communication requests with real Gmail integration."""
        msg_lower = message.lower()
        
        # Check if Gmail is configured
        if not self.platforms.gmail or not self.platforms.gmail.is_available:
            return ("Email's not set up yet. Run `python -m jc.google_oauth` to connect your Gmail. "
                    "Once that's done, I'll be able to send and read emails for you!")
        
        # Send email
        if any(word in msg_lower for word in ['send', 'write', 'compose', 'email to']):
            # Try to extract recipient and content
            # Pattern: "send email to X about Y" or "email X saying Y"
            to_match = re.search(r'(?:to|email)\s+([^\s]+@[^\s]+)', message, re.IGNORECASE)
            
            if to_match:
                recipient = to_match.group(1)
                # Extract subject/content after the email
                content_match = re.search(r'(?:about|saying|with|:)\s*(.+)', message, re.IGNORECASE)
                content = content_match.group(1) if content_match else "Message from JC"
                
                result = self.platforms.send_email(
                    to=recipient,
                    subject=f"Message: {content[:50]}...",
                    body=content
                )
                
                if result:
                    return VoiceCommands.get_random_confirmation() + f" Email sent to {recipient}!"
                else:
                    return "Hit a snag sending that email. Want me to try again?"
            else:
                return "Sure! Who should I send the email to? Give me an address and I'll fire it off."
        
        # Check/read emails
        elif any(word in msg_lower for word in ['check', 'read', 'show', 'get', 'inbox']):
            emails = self.platforms.get_recent_emails(max_results=5)
            
            if emails:
                response = "Here's what's in your inbox:\n\n"
                for i, email in enumerate(emails, 1):
                    response += f"{i}. From: {email.get('from', 'Unknown')}\n"
                    response += f"   Subject: {email.get('subject', 'No subject')}\n"
                    response += f"   Preview: {email.get('snippet', '')[:80]}...\n\n"
                response += "Want me to read any of these in full?"
                return response
            else:
                return "Inbox is clear! No new emails to report."
        
        # Draft email
        else:
            return ("I can send emails now! Just tell me:\n"
                    "• 'Send email to someone@email.com about the project'\n"
                    "• 'Check my emails'\n"
                    "• 'Read my inbox'\n\n"
                    "What would you like to do?")

    def _handle_scheduling(self, message: str) -> str:
        """Handle calendar/scheduling requests with real Google Calendar integration."""
        msg_lower = message.lower()
        
        # Check if Calendar is configured
        if not self.platforms.calendar or not self.platforms.calendar.is_available:
            return ("Calendar's not hooked up yet. Run `python -m jc.google_oauth` to connect. "
                    "Then I'll be able to schedule meetings and show you what's coming up!")
        
        # Create event
        if any(word in msg_lower for word in ['schedule', 'create', 'add', 'book', 'set up']):
            # Try to parse meeting details
            # Pattern: "schedule meeting tomorrow at 3pm" or "create event called X at Y"
            
            # Extract title
            title_match = re.search(r'(?:called|titled|for|about)\s+["\']?([^"\']+)["\']?', message, re.IGNORECASE)
            title = title_match.group(1) if title_match else "Meeting (scheduled by JC)"
            
            # Extract time - look for common patterns
            time_match = re.search(r'at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)', message, re.IGNORECASE)
            date_match = re.search(r'(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)', 
                                   message, re.IGNORECASE)
            
            if time_match:
                time_str = time_match.group(1)
                # Build a datetime
                now = datetime.now()
                
                if date_match:
                    day = date_match.group(1).lower()
                    if day == 'tomorrow':
                        now = now.replace(day=now.day + 1)
                    # For weekdays, would need more complex logic
                
                # Parse time
                try:
                    if 'pm' in time_str.lower() and ':' not in time_str:
                        hour = int(re.search(r'\d+', time_str).group())
                        if hour < 12:
                            hour += 12
                    elif 'am' in time_str.lower() and ':' not in time_str:
                        hour = int(re.search(r'\d+', time_str).group())
                    else:
                        hour = int(re.search(r'\d+', time_str).group())
                    
                    start_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
                    
                    result = self.platforms.create_calendar_event(
                        title=title,
                        start_time=start_time.isoformat(),
                        duration=60
                    )
                    
                    if result.get('success') or result.get('event_id'):
                        return (VoiceCommands.get_random_confirmation() + 
                                f" '{title}' is on the calendar for {start_time.strftime('%B %d at %I:%M %p')}!")
                    else:
                        return f"Had trouble creating that event. Error: {result.get('error', 'Unknown')}"
                except Exception as e:
                    logger.error(f"Calendar parsing error: {e}")
                    return "I couldn't quite parse that time. Try something like 'schedule meeting tomorrow at 3pm'."
            else:
                return ("Sure! When should I schedule it? Give me something like:\n"
                        "'Schedule meeting tomorrow at 2pm'\n"
                        "'Book call at 10am called Strategy Session'")
        
        # View upcoming events
        elif any(word in msg_lower for word in ['show', 'what', 'upcoming', 'check', 'view', 'calendar']):
            events = self.platforms.get_upcoming_events(max_results=5)
            
            if events:
                response = "Here's what's coming up:\n\n"
                for event in events:
                    start = event.get('start', 'TBD')
                    response += f"• {event.get('summary', 'Untitled event')}\n"
                    response += f"  When: {start}\n"
                    if event.get('location'):
                        response += f"  Where: {event.get('location')}\n"
                    response += "\n"
                return response
            else:
                return "Your calendar's clear! No upcoming events. Want me to schedule something?"
        
        else:
            return ("I'm hooked into your calendar! I can:\n"
                    "• 'Schedule meeting tomorrow at 3pm called Strategy'\n"
                    "• 'Show my upcoming events'\n"
                    "• 'What's on my calendar this week?'\n\n"
                    "What would you like to do?")

    def _handle_recommendations(self) -> str:
        recs = self.brain.get_recommendations()
        if recs:
            response = "Based on your patterns, here's what I'm thinking:\n\n"
            for i, rec in enumerate(recs, 1):
                response += f"{i}. {rec}\n"
            return response
        else:
            return "Still learning your patterns. Ask me again soon and I'll have better suggestions!"

    async def _ai_response(self, message: str, context: Dict[str, Any]) -> str:
        # Personalize prompt with user context and personality
        personality = context.get('personality', 'helpful assistant')
        prompt = RECOMMENDED_STARTER_PROMPT.format(user_message=message, context=context)
        messages = [{"role": "user", "content": prompt}]

        # Example tool-calling: define available tools
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "description": "Get current weather for a city",
                    "parameters": {"type": "object", "properties": {"city": {"type": "string"}}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the agent's todo list",
                    "parameters": {"type": "object", "properties": {"title": {"type": "string"}}}
                }
            }
        ]

        # Tool choice: let LLM decide
        tool_choice = "auto"

        response = self.llm_provider.call(
            messages,
            context=context,
            personality=personality,
            tools=tools,
            tool_choice=tool_choice
        )
        return response

    def start_voice_mode(self):
        if not self.has_voice:
            logger.error("Voice not enabled")
            return
        
        logger.info("Starting voice mode...")
        self.speak("Hey! JC here. I'm listening. Say 'Hey JC' to get my attention.")
        
        def voice_callback(command: str):
            try:
                response = asyncio.run(self.process_message(command))
                self.speak(response, wait=True)
            except Exception as e:
                logger.error(f"Voice callback error: {e}")
        
        self.voice.start_continuous_listening(callback=voice_callback)

    def stop_voice_mode(self):
        if self.has_voice and self.voice:
            self.voice.stop_continuous_listening()
            logger.info("Voice mode stopped")

    async def chat_mode(self):
        print("\n" + "="*60)
        print("JC Chat Mode - Type 'quit' or 'exit' to stop")
        print("="*60 + "\n")
        
        self.speak("What's up? Ready to get some work done?")
        
        while True:
            try:
                user_input = self.listen(timeout=30)
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    self.speak("Catch you later! Let's crush it tomorrow.")
                    break
                
                response = await self.process_message(user_input)
                self.speak(response)
                
            except KeyboardInterrupt:
                self.speak("Alright, stopping. Peace out!")
                break
            except Exception as e:
                logger.error(f"Chat error: {e}")
                self.speak("Whoa, something went wrong. Let's try again.")


async def main():
    try:
        enable_voice_env = (os.getenv("JC_ENABLE_VOICE") or "1").strip().lower()
        enable_voice = enable_voice_env not in {"0", "false", "no", "off"}
        jc = JC(enable_voice=enable_voice)
        await jc.chat_mode()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)
    finally:
        logger.info("JC shutting down...")


__all__ = [
    'JC', 'main', 'run_flow', 'load_checkpoint', 'JCState'
]
