#!/usr/bin/env python3
"""
JC Research - Intelligent Web Research and Information Gathering
"""
import os
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from bs4 import BeautifulSoup
from googlesearch import search
import asyncio
import aiohttp

from .secrets import load_env, get_llm_api_key


class JCResearch:
	"""Research assistant for gathering and analyzing information"""
    
	def __init__(self):
		# Load local .env if present so keys are available during tests/runtime
		try:
			load_env()
		except Exception:
			pass

		self.serper_api_key = os.getenv("SERPER_API_KEY")
		# Prefer OPENAI API key, fallback to OPENROUTER
		self.openrouter_key = get_llm_api_key()
		self.session = requests.Session()
		self.session.headers.update({
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
		})
    
	def web_search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
		"""Search the web and return relevant results"""
		print(f"Searching for: {query}")
        
		if self.serper_api_key:
			return self._serper_search(query, num_results)
		else:
			return self._google_search(query, num_results)
    
	def _serper_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
		"""Use Serper API for search"""
		try:
			url = "https://google.serper.dev/search"
			payload = json.dumps({"q": query, "num": num_results})
			headers = {
				'X-API-KEY': self.serper_api_key,
				'Content-Type': 'application/json'
			}
            
			response = requests.post(url, headers=headers, data=payload)
			data = response.json()
            
			results = []
			for result in data.get('organic', []):
				results.append({
					'title': result.get('title', ''),
					'link': result.get('link', ''),
					'snippet': result.get('snippet', '')
				})
            
			return results
		except Exception as e:
			print(f"Serper search error: {e}")
			return self._google_search(query, num_results)
    
	def _google_search(self, query: str, num_results: int) -> List[Dict[str, str]]:
		"""Fallback Google search"""
		results = []
		try:
			for url in search(query, num_results=num_results, lang='en'):
				results.append({
					'title': url,
					'link': url,
					'snippet': ''
				})
		except Exception as e:
			print(f"Google search error: {e}")
        
		return results
    
	def fetch_page_content(self, url: str) -> Optional[str]:
		"""Fetch and extract main content from a webpage"""
		try:
			response = self.session.get(url, timeout=10)
			response.raise_for_status()
            
			soup = BeautifulSoup(response.content, 'html.parser')
            
			# Remove scripts and styles
			for script in soup(["script", "style"]):
				script.decompose()
            
			# Get text
			text = soup.get_text()
            
			# Clean up
			lines = (line.strip() for line in text.splitlines())
			chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
			text = '\n'.join(chunk for chunk in chunks if chunk)
            
			return text[:5000]  # Limit to 5000 chars
            
		except Exception as e:
			print(f"Error fetching {url}: {e}")
			return None
    
	def deep_research(self, topic: str, num_sources: int = 3) -> Dict[str, Any]:
		"""Conduct comprehensive research on a topic"""
		print(f"\nDeep research on: {topic}")
        
		# Search for information
		search_results = self.web_search(topic, num_sources)
        
		# Fetch content from top results
		detailed_info = []
		for result in search_results[:num_sources]:
			content = self.fetch_page_content(result['link'])
			if content:
				detailed_info.append({
					'source': result['title'],
					'url': result['link'],
					'content': content
				})
        
		return {
			'topic': topic,
			'timestamp': datetime.now().isoformat(),
			'search_results': search_results,
			'detailed_info': detailed_info,
			'sources_count': len(detailed_info)
		}
    
	def research_competitor(self, company_name: str) -> Dict[str, Any]:
		"""Research a competitor"""
		queries = [
			f"{company_name} business model",
			f"{company_name} revenue pricing",
			f"{company_name} recent news",
			f"{company_name} customer reviews"
		]
        
		research = {}
		for query in queries:
			results = self.web_search(query, 3)
			research[query] = results
        
		return research
    
	def research_market(self, market_niche: str) -> Dict[str, Any]:
		"""Research a market or niche"""
		queries = [
			f"{market_niche} market size 2025",
			f"{market_niche} trends",
			f"{market_niche} leading companies",
			f"{market_niche} challenges opportunities"
		]
        
		research = {}
		for query in queries:
			results = self.web_search(query, 3)
			research[query] = results
        
		return research
    
	def find_business_opportunities(self, industry: str) -> List[Dict[str, Any]]:
		"""Identify business opportunities in an industry"""
		queries = [
			f"{industry} emerging trends 2025",
			f"{industry} underserved markets",
			f"{industry} pain points",
			f"{industry} innovation opportunities"
		]
        
		opportunities = []
		for query in queries:
			results = self.web_search(query, 5)
			opportunities.extend(results)
        
		return opportunities
    
	def summarize_research(self, research_data: Dict[str, Any], max_length: int = 500) -> str:
		"""Summarize research findings using AI"""
		# This would integrate with your LLM provider
		# For now, returns a structured summary
        
		summary = f"Research Summary: {research_data.get('topic', 'Unknown')}\n\n"
		summary += f"Sources analyzed: {research_data.get('sources_count', 0)}\n\n"
        
		if 'search_results' in research_data:
			summary += "Key findings:\n"
			for i, result in enumerate(research_data['search_results'][:3], 1):
				summary += f"{i}. {result.get('title', 'N/A')}\n"
				summary += f"   {result.get('snippet', '')}\n"
        
		return summary[:max_length]


class PlatformIntegrations:
	"""Integrations with various platforms"""
    
	def __init__(self):
		self._gmail_client = None
		self._calendar_client = None
		self.notion_token = os.getenv("NOTION_TOKEN")
		self.slack_token = os.getenv("SLACK_TOKEN")
	
	@property
	def gmail(self):
		"""Lazy-load Gmail client."""
		if self._gmail_client is None:
			try:
				from .google_oauth import GmailClient
				self._gmail_client = GmailClient()
			except ImportError:
				self._gmail_client = None
		return self._gmail_client
	
	@property
	def calendar(self):
		"""Lazy-load Calendar client."""
		if self._calendar_client is None:
			try:
				from .google_oauth import CalendarClient
				self._calendar_client = CalendarClient()
			except ImportError:
				self._calendar_client = None
		return self._calendar_client
    
	def send_email(self, to: str, subject: str, body: str) -> bool:
		"""Send email via Gmail API (real OAuth integration)."""
		if self.gmail and self.gmail.is_available:
			result = self.gmail.send_email(to, subject, body)
			return result.get("success", False)
		else:
			print(f"Gmail not configured. Would send to {to}: {subject}")
			print("Run: python -m jc.google_oauth to authorize Gmail")
			return False
    
	def create_calendar_event(self, title: str, start_time: str, duration: int = 60) -> Dict[str, Any]:
		"""Create calendar event via Google Calendar API (real OAuth integration)."""
		if self.calendar and self.calendar.is_available:
			from datetime import datetime
			# Parse start_time string to datetime
			try:
				if "T" in start_time:
					dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
				else:
					dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
			except ValueError:
				dt = datetime.now()
			
			result = self.calendar.create_event(title, dt, duration)
			return result
		else:
			print(f"Calendar not configured. Would create: {title} at {start_time}")
			print("Run: python -m jc.google_oauth to authorize Calendar")
			return {"event_id": "not_configured", "title": title}
	
	def get_upcoming_events(self, max_results: int = 10) -> list:
		"""Get upcoming calendar events."""
		if self.calendar and self.calendar.is_available:
			return self.calendar.get_upcoming_events(max_results)
		return []
	
	def get_recent_emails(self, max_results: int = 10, query: str = "") -> list:
		"""Get recent emails from Gmail."""
		if self.gmail and self.gmail.is_available:
			return self.gmail.get_recent_emails(max_results, query)
		return []
    
	def add_notion_task(self, title: str, description: str = "") -> Dict[str, Any]:
		"""Add task to Notion"""
		if not self.notion_token:
			print("Notion not configured")
			return {}
        
		# Notion API integration would go here
		print(f"Notion task: {title}")
		return {"task_id": "placeholder"}
    
	def send_slack_message(self, channel: str, message: str) -> bool:
		"""Send Slack message"""
		if not self.slack_token:
			print("Slack not configured")
			return False
        
		try:
			url = "https://slack.com/api/chat.postMessage"
			headers = {"Authorization": f"Bearer {self.slack_token}"}
			data = {"channel": channel, "text": message}
            
			response = requests.post(url, headers=headers, json=data)
			return response.json().get('ok', False)
		except Exception as e:
			print(f"Slack error: {e}")
			return False


if __name__ == "__main__":
	# Test research capabilities
	researcher = JCResearch()
    
	# Test basic search
	results = researcher.web_search("AI business automation 2025", 3)
	print("\nSearch Results:")
	for i, result in enumerate(results, 1):
		print(f"{i}. {result.get('title', 'N/A')}")
		print(f"   {result.get('link', 'N/A')}")
		print(f"   {result.get('snippet', '')}\n")
