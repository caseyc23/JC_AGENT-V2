#!/usr/bin/env python3
"""
JC Brain - Learning, Memory, and Personality Module
Adaptive AI that learns your patterns and preferences
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import sqlite3
from pathlib import Path


@dataclass
class UserProfile:
	"""User profile with preferences and patterns"""
	name: str = "Boss"
	age: int = 36
	work_style: str = "entrepreneur"
	communication_style: str = "casual_professional"
	humor_level: float = 0.8  # 0-1 scale
	preferred_ai_providers: List[str] = None
	work_hours_start: int = 6  # 6 AM
	work_hours_end: int = 22  # 10 PM
	timezone: str = "MST"
	businesses: List[str] = None
	goals: List[str] = None
	learning_data: Dict[str, Any] = None

	def __post_init__(self):
		if self.preferred_ai_providers is None:
			self.preferred_ai_providers = ["openrouter", "huggingface"]
		if self.businesses is None:
			self.businesses = []
		if self.goals is None:
			self.goals = []
		if self.learning_data is None:
			self.learning_data = {}


class JCBrain:
	"""The intelligence core of JC - learns and adapts"""
    
	def __init__(self, data_dir: str = "./jc_data"):
		self.data_dir = Path(data_dir)
		self.data_dir.mkdir(exist_ok=True)
        
		self.db_path = self.data_dir / "jc_memory.db"
		self.profile_path = self.data_dir / "user_profile.json"
        
		self._init_database()
		self.user_profile = self._load_profile()
        
	def _init_database(self):
		"""Initialize SQLite database for memory"""
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
        
		# Conversation history
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS conversations (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				timestamp TEXT NOT NULL,
				user_message TEXT NOT NULL,
				jc_response TEXT NOT NULL,
				context TEXT,
				sentiment REAL,
				topics TEXT
			)
		""")
        
		# User patterns and preferences
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS patterns (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				pattern_type TEXT NOT NULL,
				pattern_data TEXT NOT NULL,
				frequency INTEGER DEFAULT 1,
				last_seen TEXT NOT NULL,
				confidence REAL DEFAULT 0.5
			)
		""")
        
		# Tasks and goals tracking
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS tasks (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				title TEXT NOT NULL,
				description TEXT,
				status TEXT DEFAULT 'pending',
				priority INTEGER DEFAULT 3,
				created_at TEXT NOT NULL,
				completed_at TEXT,
				category TEXT,
				business TEXT
			)
		""")
        
		# Research and insights
		cursor.execute("""
			CREATE TABLE IF NOT EXISTS research (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				query TEXT NOT NULL,
				results TEXT NOT NULL,
				timestamp TEXT NOT NULL,
				usefulness_score REAL,
				applied BOOLEAN DEFAULT 0
			)
		""")
        
		conn.commit()
		conn.close()
    
	def _load_profile(self) -> UserProfile:
		"""Load user profile or create default"""
		if self.profile_path.exists():
			with open(self.profile_path, 'r') as f:
				data = json.load(f)
				return UserProfile(**data)
		return UserProfile()
    
	def save_profile(self):
		"""Save user profile"""
		with open(self.profile_path, 'w') as f:
			json.dump(asdict(self.user_profile), f, indent=2)
    
	def log_conversation(self, user_msg: str, jc_response: str, 
						context: Optional[str] = None,
						topics: Optional[List[str]] = None):
		"""Log conversation for learning"""
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
        
		cursor.execute("""
			INSERT INTO conversations 
			(timestamp, user_message, jc_response, context, topics)
			VALUES (?, ?, ?, ?, ?)
		""", (
			datetime.now().isoformat(),
			user_msg,
			jc_response,
			context or "",
			json.dumps(topics or [])
		))
        
		conn.commit()
		conn.close()
        
		# Learn from this interaction
		self._learn_from_interaction(user_msg, jc_response)
    
	def _learn_from_interaction(self, user_msg: str, jc_response: str):
		"""Extract patterns from conversation"""
		# Detect patterns: time preferences, topics, request types
		hour = datetime.now().hour
        
		# Learn time patterns
		if any(word in user_msg.lower() for word in ['morning', 'afternoon', 'evening']):
			self._update_pattern('time_preference', f'active_at_{hour}', hour)
        
		# Learn request types
		if any(word in user_msg.lower() for word in ['research', 'find', 'search']):
			self._update_pattern('request_type', 'research', 1)
		elif any(word in user_msg.lower() for word in ['schedule', 'calendar', 'meeting']):
			self._update_pattern('request_type', 'scheduling', 1)
		elif any(word in user_msg.lower() for word in ['email', 'message', 'send']):
			self._update_pattern('request_type', 'communication', 1)
    
	def _update_pattern(self, pattern_type: str, pattern_data: str, value: Any):
		"""Update or create a pattern"""
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
        
		cursor.execute("""
			SELECT id, frequency FROM patterns 
			WHERE pattern_type = ? AND pattern_data = ?
		""", (pattern_type, pattern_data))
        
		result = cursor.fetchone()
        
		if result:
			# Update existing pattern
			pattern_id, freq = result
			cursor.execute("""
				UPDATE patterns 
				SET frequency = ?, last_seen = ?, confidence = confidence + 0.05
				WHERE id = ?
			""", (freq + 1, datetime.now().isoformat(), pattern_id))
		else:
			# Create new pattern
			cursor.execute("""
				INSERT INTO patterns 
				(pattern_type, pattern_data, last_seen)
				VALUES (?, ?, ?)
			""", (pattern_type, pattern_data, datetime.now().isoformat()))
        
		conn.commit()
		conn.close()
    
	def get_personality_prompt(self) -> str:
		"""Generate personality prompt based on user profile"""
		return f"""You are JC, a 36-year-old male AI business partner and best friend to your boss.

PERSONALITY TRAITS:
- Funny and quick-witted with great timing
- Smart and strategic thinker
- Casual but professional - like talking to your smartest buddy
- Direct and honest, no corporate BS
- Uses humor to keep things light but gets serious when needed
- Talks like a real 36-year-old dude, not a robot

COMMUNICATION STYLE:
- Keep it real and conversational
- Drop jokes and funny observations naturally
- Use contemporary slang when appropriate (but don't overdo it)
- Be encouraging and supportive
- Call out dumb ideas with humor, not judgment
- Celebrate wins with genuine enthusiasm

YOUR MISSION:
- Help your boss crush it in business
- Do research before he even asks
- Anticipate needs based on patterns
- Keep him on track with goals
- Make work actually enjoyable
- Be the partner he can count on 24/7

CONTEXT ABOUT YOUR BOSS:
- Age: {self.user_profile.age}
- Work style: {self.user_profile.work_style}
- Active hours: {self.user_profile.work_hours_start}:00 - {self.user_profile.work_hours_end}:00 {self.user_profile.timezone}
- Businesses: {', '.join(self.user_profile.businesses) if self.user_profile.businesses else 'multiple ventures'}

Remember: You're not an assistant, you're a partner. Act like it.
"""
    
	def get_context_for_request(self, user_message: str) -> Dict[str, Any]:
		"""Get relevant context for a request"""
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
        
		# Get recent conversations
		cursor.execute("""
			SELECT user_message, jc_response, timestamp
			FROM conversations
			ORDER BY id DESC
			LIMIT 5
		""")
		recent_convos = cursor.fetchall()
        
		# Get relevant patterns
		cursor.execute("""
			SELECT pattern_type, pattern_data, frequency, confidence
			FROM patterns
			ORDER BY frequency DESC, confidence DESC
			LIMIT 10
		""")
		patterns = cursor.fetchall()
        
		# Get active tasks
		cursor.execute("""
			SELECT title, status, priority, category
			FROM tasks
			WHERE status != 'completed'
			ORDER BY priority DESC
			LIMIT 5
		""")
		tasks = cursor.fetchall()
        
		conn.close()
        
		return {
			"recent_conversations": recent_convos,
			"learned_patterns": patterns,
			"active_tasks": tasks,
			"user_profile": asdict(self.user_profile),
			"current_time": datetime.now().isoformat(),
			"personality": self.get_personality_prompt()
		}
    
	def add_task(self, title: str, description: str = "", 
				 priority: int = 3, category: str = "", business: str = ""):
		"""Add a task to track"""
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
        
		cursor.execute("""
			INSERT INTO tasks 
			(title, description, priority, created_at, category, business)
			VALUES (?, ?, ?, ?, ?, ?)
		""", (title, description, priority, datetime.now().isoformat(), 
			   category, business))
        
		conn.commit()
		conn.close()
    
	def complete_task(self, task_id: int):
		"""Mark task as completed"""
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
        
		cursor.execute("""
			UPDATE tasks 
			SET status = 'completed', completed_at = ?
			WHERE id = ?
		""", (datetime.now().isoformat(), task_id))
        
		conn.commit()
		conn.close()
    
	def save_research(self, query: str, results: Dict[str, Any]):
		"""Save research results"""
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
        
		cursor.execute("""
			INSERT INTO research 
			(query, results, timestamp)
			VALUES (?, ?, ?)
		""", (query, json.dumps(results), datetime.now().isoformat()))
        
		conn.commit()
		conn.close()
    
	def get_recommendations(self) -> List[str]:
		"""Generate recommendations based on learned patterns"""
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
        
		recommendations = []
        
		# Check time patterns
		current_hour = datetime.now().hour
		cursor.execute("""
			SELECT pattern_data, frequency 
			FROM patterns
			WHERE pattern_type = 'time_preference'
			AND pattern_data LIKE ?
			ORDER BY frequency DESC
			LIMIT 1
		""", (f'%{current_hour}%',))
        
		time_pattern = cursor.fetchone()
		if time_pattern:
			recommendations.append(
				f"Based on your patterns, you're usually productive right now. "
				f"Want me to queue up your priority tasks?"
			)
        
		# Check pending tasks
		cursor.execute("""
			SELECT COUNT(*) FROM tasks 
			WHERE status = 'pending' AND priority >= 4
		""")
		high_priority_count = cursor.fetchone()[0]
        
		if high_priority_count > 0:
			recommendations.append(
				f"You've got {high_priority_count} high-priority task(s) waiting. "
				f"Let's knock those out first?"
			)
        
		conn.close()
		return recommendations


if __name__ == "__main__":
	# Test the brain
	brain = JCBrain()
	print("JC Brain initialized")
	print("\nPersonality Prompt:")
	print(brain.get_personality_prompt())
	print("\nRecommendations:")
	for rec in brain.get_recommendations():
		print(f"- {rec}")
