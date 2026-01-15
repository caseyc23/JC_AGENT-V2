#!/usr/bin/env python3
"""
JC Voice - Speech Recognition and TTS with Natural 36-Year-Old Male Voice
"""
import os
import threading
import queue
from typing import Optional, Callable
import speech_recognition as sr
import pyttsx3
import pygame
import io


class JCVoice:
	"""Voice interface for JC - Speak and listen naturally"""
    
	def __init__(self, use_elevenlabs: bool = True):
		self.use_elevenlabs = bool(use_elevenlabs and os.getenv("ELEVENLABS_API_KEY"))
		# ElevenLabs module is optional and imported lazily to avoid import-time failures
		self._eleven = None
		self._eleven_client = None
		self._eleven_available = False
		self._eleven_api = None  # "client" (>=1.x) or "legacy" (0.x)
		if self.use_elevenlabs:
			try:
				import elevenlabs as _eleven
				self._eleven = _eleven
				api_key = os.getenv("ELEVENLABS_API_KEY") or ""

				# Newer elevenlabs (e.g. 1.x/2.x) exposes an ElevenLabs client with text_to_speech.convert
				if hasattr(_eleven, "ElevenLabs"):
					try:
						client = _eleven.ElevenLabs(api_key=api_key)
						tts = getattr(client, "text_to_speech", None)
						if tts is not None and hasattr(tts, "convert"):
							self._eleven_client = client
							self._eleven_available = True
							self._eleven_api = "client"
					except Exception:
						# ignore init failures; will fall back below
						pass

				# Older elevenlabs (0.x) exposes generate/play/set_api_key/Voice/VoiceSettings
				if not self._eleven_available:
					if all(hasattr(_eleven, name) for name in ("generate", "Voice", "VoiceSettings")):
						self._eleven_available = True
						self._eleven_api = "legacy"
						if hasattr(_eleven, "set_api_key"):
							try:
								_eleven.set_api_key(api_key)
							except Exception:
								# ignore errors setting the key here; will surface at runtime
								pass

				if not self._eleven_available:
					# elevenlabs present but missing expected symbols
					self.use_elevenlabs = False
			except Exception:
				# failed to import elevenlabs; fall back to system TTS
				self.use_elevenlabs = False
        
		# Initialize speech recognition
		self.recognizer = sr.Recognizer()
		self.microphone = sr.Microphone()
        
		# Adjust for ambient noise
		with self.microphone as source:
			print("Calibrating microphone for ambient noise...")
			self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
		# Initialize TTS
		# Initialize TTS
		if self.use_elevenlabs and self._eleven_available:
			# Use ElevenLabs for natural-sounding voice
			# Voice ID for a natural 36-year-old male (can be customized)
			self.voice_id = "onwK6e4l9Sz8FqLk2wHf"  # "Adam" voice
			print("Using ElevenLabs for high-quality voice")
		else:
			# Fallback to pyttsx3
			self.use_elevenlabs = False
			self._eleven = None
			self.tts_engine = pyttsx3.init()
			voices = self.tts_engine.getProperty('voices')
			# Select male voice
			for voice in voices:
				if 'male' in voice.name.lower() and 'female' not in voice.name.lower():
					self.tts_engine.setProperty('voice', voice.id)
					break
			# Set speech rate (words per minute) - natural conversational pace
			self.tts_engine.setProperty('rate', 175)
			# Set volume
			self.tts_engine.setProperty('volume', 0.9)
			print("Using system TTS voice")
        
		# Voice listening state
		self.is_listening = False
		self.listen_thread = None
		self.speech_queue = queue.Queue()
		self.callback = None
        
		# Initialize pygame for audio
		try:
			pygame.mixer.init()
		except Exception:
			# Audio output may be unavailable in some environments; speaking can still work via ElevenLabs/play
			pass

	def _eleven_play_audio(self, audio):
		"""Play ElevenLabs audio across multiple SDK versions."""
		play_obj = getattr(self._eleven, "play", None)
		# Some versions export `play` as a function, others as a module with `play()`.
		if callable(play_obj):
			play_obj(audio)
			return
		play_fn = getattr(play_obj, "play", None)
		if callable(play_fn):
			play_fn(audio)
			return
		raise RuntimeError("ElevenLabs playback function not available")
    
	def speak(self, text: str, wait: bool = True):
		"""Speak text with JC's voice"""
		if not text:
			return
        
		print(f"JC: {text}")
        
		if self.use_elevenlabs and self._eleven_available:
			try:
				# Generate audio with natural voice settings using the lazily-imported module
				if self._eleven_api == "client" and self._eleven_client is not None:
					audio = self._eleven_client.text_to_speech.convert(
						self.voice_id,
						text=text,
						model_id="eleven_multilingual_v2",
						voice_settings=self._eleven.VoiceSettings(
							stability=0.5,
							similarity_boost=0.75,
							style=0.5,
							use_speaker_boost=True,
						),
					)
				else:
					audio = self._eleven.generate(
						text=text,
						voice=self._eleven.Voice(
							voice_id=self.voice_id,
							settings=self._eleven.VoiceSettings(
								stability=0.5,
								similarity_boost=0.75,
								style=0.5,
								use_speaker_boost=True,
							)
						),
						model="eleven_multilingual_v2",
					)

				# Play audio
				if wait:
					self._eleven_play_audio(audio)
				else:
					threading.Thread(target=self._eleven_play_audio, args=(audio,), daemon=True).start()
			except Exception as e:
				print(f"ElevenLabs error: {e}, falling back to system TTS")
				self._fallback_speak(text, wait)
		else:
			self._fallback_speak(text, wait)
    
	def _fallback_speak(self, text: str, wait: bool = True):
		"""Fallback TTS using pyttsx3"""
		if wait:
			self.tts_engine.say(text)
			self.tts_engine.runAndWait()
		else:
			threading.Thread(
				target=lambda: (self.tts_engine.say(text), self.tts_engine.runAndWait()),
				daemon=True
			).start()
    
	def listen_once(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
		"""Listen for a single phrase"""
		try:
			with self.microphone as source:
				print("Listening...")
				audio = self.recognizer.listen(
					source, 
					timeout=timeout,
					phrase_time_limit=phrase_time_limit
				)
                
			print("Processing speech...")
			text = self.recognizer.recognize_google(audio)
			print(f"You said: {text}")
			return text
            
		except sr.WaitTimeoutError:
			print("Listening timed out")
			return None
		except sr.UnknownValueError:
			print("Could not understand audio")
			return None
		except sr.RequestError as e:
			print(f"Speech recognition error: {e}")
			return None
    
	def start_continuous_listening(self, callback: Callable[[str], None]):
		"""Start listening continuously in background"""
		if self.is_listening:
			print("Already listening")
			return
        
		self.callback = callback
		self.is_listening = True
		self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
		self.listen_thread.start()
		print("Started continuous listening")
    
	def stop_continuous_listening(self):
		"""Stop continuous listening"""
		self.is_listening = False
		if self.listen_thread:
			self.listen_thread.join(timeout=2)
		print("Stopped continuous listening")
    
	def _listen_loop(self):
		"""Background listening loop"""
		with self.microphone as source:
			while self.is_listening:
				try:
					print("[Listening for 'Hey JC'...]")
					audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    
					try:
						text = self.recognizer.recognize_google(audio)
						print(f"Heard: {text}")
                        
						# Check for wake word
						if self._is_wake_word(text):
							self.speak("What's up?", wait=False)
							# Listen for command
							command_audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
							command = self.recognizer.recognize_google(command_audio)
							print(f"Command: {command}")
                            
							if self.callback:
								self.callback(command)
                        
					except sr.UnknownValueError:
						pass  # Couldn't understand, keep listening
					except sr.RequestError as e:
						print(f"Recognition error: {e}")
                        
				except sr.WaitTimeoutError:
					pass  # No speech detected, continue loop
				except Exception as e:
					print(f"Listening error: {e}")
    
	def _is_wake_word(self, text: str) -> bool:
		"""Check if text contains wake word"""
		wake_words = ["hey jc", "hey jay", "hey jay c", "yo jc", "jc"]
		text_lower = text.lower()
		return any(wake in text_lower for wake in wake_words)
    
	def get_voice_settings_info(self) -> dict:
		"""Get information about current voice settings"""
		return {
			"provider": "ElevenLabs" if self.use_elevenlabs else "System TTS",
			"voice_id": self.voice_id if self.use_elevenlabs else "system",
			"description": "Natural 36-year-old male voice with personality",
			"features": [
				"Wake word detection ('Hey JC')",
				"Continuous background listening",
				"Natural speech synthesis",
				"Ambient noise adjustment"
			]
		}


class VoiceCommands:
	"""Common voice commands and responses"""
    
	GREETINGS = [
		"What's up?",
		"Hey! What can I do for you?",
		"Yo, what's good?",
		"Talk to me, what do you need?",
		"I'm here, what's the play?"
	]
    
	CONFIRMATIONS = [
		"Got it",
		"On it",
		"You got it",
		"Consider it done",
		"I'm on it",
		"No problem"
	]
    
	THINKING = [
		"Let me think about that...",
		"Hmm, interesting question...",
		"Good one, let me figure that out...",
		"Alright, give me a sec..."
	]
    
	JOKES = [
		"Why did the AI go to therapy? It had too many neural issues!",
		"I'd tell you a UDP joke, but I'm not sure you'd get it...",
		"There are 10 types of people: those who understand binary and those who don't.",
		"I'm not saying I'm Batman, but have you ever seen me and Batman in the same room?"
	]
    
	@staticmethod
	def get_random_greeting():
		import random
		return random.choice(VoiceCommands.GREETINGS)
    
	@staticmethod
	def get_random_confirmation():
		import random
		return random.choice(VoiceCommands.CONFIRMATIONS)
    
	@staticmethod
	def get_random_thinking():
		import random
		return random.choice(VoiceCommands.THINKING)


if __name__ == "__main__":
	# Test the voice system
	print("Testing JC Voice System")
    
	voice = JCVoice(use_elevenlabs=False)  # Use system TTS for testing
    
	# Test speaking
	voice.speak("Hey boss! JC here. This is what I sound like. Pretty natural, right? Ready to crush some goals today?")
    
	# Test listening
	print("\nSay something (you have 5 seconds):")
	text = voice.listen_once()
	if text:
		voice.speak(f"You said: {text}. Nice!")
    
	# Show voice info
	print("\nVoice Settings:")
	import json
	print(json.dumps(voice.get_voice_settings_info(), indent=2))
