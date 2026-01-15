#!/usr/bin/env python3
"""
JC Self-Awareness Module
In Memory of JC - A Wrestling Partner Who Never Gave Up

This module gives JC complete honesty about its capabilities.
JC will NEVER lie about what it can or cannot do.
Like a wrestling partner - always truthful, always pushing forward together.
"""
import os
import sys
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import json
from pathlib import Path

logger = logging.getLogger('JC.SelfAwareness')

try:
    # Load local env keys if present
    from jc.secrets import get_effective_provider, get_llm_api_key, load_env
    try:
        load_env()
    except Exception:
        pass
except Exception:
    # Fall back to os.getenv usages below
    load_env = None
    get_llm_api_key = None
    get_effective_provider = None


@dataclass
class CapabilityStatus:
    """Status of a single capability"""
    name: str
    available: bool
    reason: str
    free_alternative: Optional[str] = None
    setup_help: Optional[str] = None
    
class JCSelfAwareness:
    """
    Self-diagnostic system - JC knows what it can and can't do.
    Honest, transparent, and always looking for solutions.
    """
    
    def __init__(self):
        self.capabilities: Dict[str, CapabilityStatus] = {}
        self.startup_diagnostics_run = False
        
    def run_full_diagnostic(self) -> Dict[str, Any]:
        """
        Run complete system check on startup.
        Tests EVERYTHING and reports honestly.
        """
        logger.info("Running full system diagnostic...")
        
        results = {
            "timestamp": str(Path(__file__).stat().st_mtime),
            "capabilities": {},
            "summary": {"working": 0, "broken": 0, "partial": 0}
        }
        
        # Test each capability
        results["capabilities"]["voice"] = self._test_voice()
        results["capabilities"]["ai_models"] = self._test_ai_models()
        results["capabilities"]["research"] = self._test_research()
        results["capabilities"]["platforms"] = self._test_platforms()
        results["capabilities"]["database"] = self._test_database()
        
        # Count status
        for cap_name, cap_status in results["capabilities"].items():
            if cap_status.available:
                results["summary"]["working"] += 1
            else:
                results["summary"]["broken"] += 1
        
        self.capabilities = results["capabilities"]
        self.startup_diagnostics_run = True
        
        return results
    
    def _test_voice(self) -> CapabilityStatus:
        """Test voice capabilities"""
        try:
            import speech_recognition
            import pyttsx3
            
            # Check if microphone accessible
            sr = speech_recognition.Recognizer()
            try:
                with speech_recognition.Microphone() as source:
                    sr.adjust_for_ambient_noise(source, duration=0.1)
                mic_ok = True
            except:
                mic_ok = False
            
            # Check TTS
            try:
                engine = pyttsx3.init()
                tts_ok = True
            except:
                tts_ok = False
            
            # Check ElevenLabs (premium)
            elevenlabs_ok = bool(os.getenv("ELEVENLABS_API_KEY"))
            
            if mic_ok and tts_ok:
                return CapabilityStatus(
                    name="Voice",
                    available=True,
                    reason="Microphone and TTS working" + (" (using ElevenLabs premium voice)" if elevenlabs_ok else " (using system voice)"),
                    free_alternative="System TTS is free and working!" if not elevenlabs_ok else None
                )
            elif tts_ok:
                return CapabilityStatus(
                    name="Voice",
                    available=True,
                    reason="TTS working, microphone not detected",
                    setup_help="Check Windows microphone permissions in Settings > Privacy > Microphone"
                )
            else:
                return CapabilityStatus(
                    name="Voice",
                    available=False,
                    reason="Voice libraries not installed",
                    setup_help="Run: pip install SpeechRecognition pyttsx3 pyaudio"
                )
                
        except ImportError as e:
            return CapabilityStatus(
                name="Voice",
                available=False,
                reason=f"Missing library: {str(e)}",
                setup_help="Run: pip install -r requirements.txt"
            )
    
    def _test_ai_models(self) -> CapabilityStatus:
        """Test AI model access"""
        provider = "openrouter"
        provider_candidates = [
            ("openai", "OPENAI_API_KEY"),
            ("openrouter", "OPENROUTER_API_KEY"),
            ("huggingface", "HUGGINGFACE_API_KEY"),
        ]

        if get_effective_provider:
            provider = get_effective_provider()
        else:
            env_override = (os.getenv("JC_PROVIDER") or "").strip().lower()
            if env_override:
                for name, env_var in provider_candidates:
                    if name == env_override and os.getenv(env_var):
                        provider = name
                        break
            if provider == "openrouter":
                for name, env_var in provider_candidates:
                    if os.getenv(env_var):
                        provider = name
                        break

        key = None
        if get_llm_api_key:
            key = get_llm_api_key(provider)
        if not key:
            for _, env_var in provider_candidates:
                key = os.getenv(env_var)
                if key:
                    break

        if key:
            if provider == "openai":
                return CapabilityStatus(
                    name="AI Models",
                    available=True,
                    reason="OpenAI configured (GPT-4o-mini, Claude, etc available)",
                    free_alternative="HuggingFace has free models if you want alternatives"
                )
            if provider == "openrouter":
                return CapabilityStatus(
                    name="AI Models",
                    available=True,
                    reason="OpenRouter configured (GPT-4o-mini, Claude, etc available)",
                    free_alternative="HuggingFace has free models if you want alternatives"
                )
            if provider == "huggingface":
                return CapabilityStatus(
                    name="AI Models",
                    available=True,
                    reason="HuggingFace configured (free models available)",
                    setup_help="Add OPENROUTER_API_KEY or OPENAI_API_KEY for more advanced models",
                    free_alternative="Explore HuggingFace's hosted demos if you need more inspiration"
                )

        return CapabilityStatus(
            name="AI Models",
            available=False,
            reason="No AI API keys configured",
            free_alternative="Get free key at https://huggingface.co/settings/tokens",
            setup_help="Or get OpenRouter key at https://openrouter.ai/ (pay-as-you-go, very cheap)"
        )
    
    def _test_research(self) -> CapabilityStatus:
        """Test web research capabilities"""
        serper_key = os.getenv("SERPER_API_KEY")
        
        # Test if we can do basic web requests
        try:
            import requests
            import bs4
            libraries_ok = True
        except:
            libraries_ok = False
        
        if not libraries_ok:
            return CapabilityStatus(
                name="Research",
                available=False,
                reason="Missing libraries",
                setup_help="Run: pip install requests beautifulsoup4"
            )
        
        if serper_key:
            return CapabilityStatus(
                name="Research",
                available=True,
                reason="Using Serper API (fast, professional search)",
                free_alternative="Can fallback to free Google search if needed"
            )
        else:
            return CapabilityStatus(
                name="Research",
                available=True,
                reason="Using free Google search (works but slower)",
                setup_help="Get free Serper key at https://serper.dev (100 searches/month free)"
            )
    
    def _test_platforms(self) -> CapabilityStatus:
        """Test platform integrations"""
        gmail_ok = bool(os.getenv("GMAIL_CREDENTIALS"))
        notion_ok = bool(os.getenv("NOTION_TOKEN"))
        slack_ok = bool(os.getenv("SLACK_TOKEN"))
        
        active = []
        if gmail_ok: active.append("Gmail")
        if notion_ok: active.append("Notion")
        if slack_ok: active.append("Slack")
        
        if active:
            return CapabilityStatus(
                name="Platforms",
                available=True,
                reason=f"Connected: {', '.join(active)}",
                setup_help=f"Not connected: {', '.join([p for p in ['Gmail', 'Notion', 'Slack'] if p not in active])}"
            )
        else:
            return CapabilityStatus(
                name="Platforms",
                available=False,
                reason="No platform integrations configured",
                free_alternative="All platforms have free tiers!",
                setup_help="I can help you set these up one at a time when you need them"
            )
    
    def _test_database(self) -> CapabilityStatus:
        """Test SQLite database"""
        try:
            import sqlite3
            
            # Try to create/open database
            data_dir = Path("./jc_data")
            data_dir.mkdir(exist_ok=True)
            
            db_path = data_dir / "jc_memory.db"
            conn = sqlite3.connect(db_path)
            conn.close()
            
            return CapabilityStatus(
                name="Database",
                available=True,
                reason=f"SQLite working at {db_path}"
            )
        except Exception as e:
            return CapabilityStatus(
                name="Database",
                available=False,
                reason=f"Database error: {str(e)}",
                setup_help="This is critical - SQLite should be built into Python. Check your Python installation."
            )
    
    def get_honest_status_message(self) -> str:
        """
        Generate honest status message for user.
        Like a wrestling partner giving you the real score.
        """
        if not self.startup_diagnostics_run:
            return "Haven't run diagnostics yet. Let me check what I can do..."
        
        working = [name for name, cap in self.capabilities.items() if cap.available]
        broken = [name for name, cap in self.capabilities.items() if not cap.available]
        
        message = "🏋️ JC Status Report - Honest Truth:\\n\\n"
        
        if working:
            message += "✅ WORKING:\\n"
            for name in working:
                cap = self.capabilities[name]
                message += f"  • {cap.name}: {cap.reason}\\n"
                if cap.free_alternative:
                    message += f"    💡 {cap.free_alternative}\\n"
        
        if broken:
            message += "\\n❌ NOT WORKING:\\n"
            for name in broken:
                cap = self.capabilities[name]
                message += f"  • {cap.name}: {cap.reason}\\n"
                if cap.free_alternative:
                    message += f"    🆓 FREE OPTION: {cap.free_alternative}\\n"
                if cap.setup_help:
                    message += f"    🛠️  FIX: {cap.setup_help}\\n"
        
        message += "\\n💪 Bottom line: I'll work with what we have and be honest about what I can't do."
        message += "\\nLike a good wrestling partner - we figure it out together."
        
        return message
    
    def can_do(self, capability: str) -> bool:
        """Check if a capability is available"""
        if capability in self.capabilities:
            return self.capabilities[capability].available
        return False
    
    def get_alternative(self, capability: str) -> Optional[str]:
        """Get free alternative for a capability"""
        if capability in self.capabilities:
            return self.capabilities[capability].free_alternative
        return None
    
    def get_help(self, capability: str) -> Optional[str]:
        """Get help for setting up a capability"""
        if capability in self.capabilities:
            return self.capabilities[capability].setup_help
        return None


if __name__ == "__main__":
    # Test the self-awareness system
    print("Testing JC Self-Awareness System\\n")
    
    sa = JCSelfAwareness()
    results = sa.run_full_diagnostic()
    
    print(sa.get_honest_status_message())
    print("\\n" + "="*60)
    print("Full diagnostic results:")
    print(json.dumps({k: asdict(v) for k, v in results["capabilities"].items()}, indent=2))
