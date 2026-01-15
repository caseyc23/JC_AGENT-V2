#!/usr/bin/env python3
"""
JC Google OAuth - Gmail and Calendar integration via OAuth2.

Uses Google's official libraries with secure token storage.
Requires google-auth, google-auth-oauthlib, google-api-python-client.

Setup:
1. Create a project in Google Cloud Console
2. Enable Gmail API and Calendar API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download client_secret.json to the project root or set GOOGLE_CLIENT_SECRET_PATH
5. Run this module to authorize: python -m jc.google_oauth
"""

from __future__ import annotations

import os
import json
import base64
from pathlib import Path
from typing import Optional, Dict, Any, List
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import logging

logger = logging.getLogger("JC.GoogleOAuth")

# Lazy imports for optional Google dependencies
_google_auth_available: Optional[bool] = None


def _check_google_deps() -> bool:
    """Check if Google API dependencies are available."""
    global _google_auth_available
    if _google_auth_available is not None:
        return _google_auth_available
    
    try:
        import google.auth  # noqa: F401
        from google_auth_oauthlib.flow import InstalledAppFlow  # noqa: F401
        from googleapiclient.discovery import build  # noqa: F401
        _google_auth_available = True
    except ImportError:
        _google_auth_available = False
        logger.warning(
            "Google API libraries not installed. "
            "Install with: pip install google-auth google-auth-oauthlib google-api-python-client"
        )
    return _google_auth_available


# OAuth scopes
SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
]

# Token storage
_BASE_DIR = Path(__file__).resolve().parent.parent
_TOKEN_PATH = _BASE_DIR / "data" / "google_token.json"
_CLIENT_SECRET_PATHS = [
    Path(os.getenv("GOOGLE_CLIENT_SECRET_PATH", "")) if os.getenv("GOOGLE_CLIENT_SECRET_PATH") else None,
    _BASE_DIR / "client_secret.json",
    _BASE_DIR / "credentials.json",
    Path.home() / ".jc" / "client_secret.json",
]


def _find_client_secret() -> Optional[Path]:
    """Find the Google OAuth client secret file."""
    for path in _CLIENT_SECRET_PATHS:
        if path and path.exists():
            return path
    return None


def _load_credentials():
    """Load stored OAuth credentials if they exist and are valid."""
    if not _check_google_deps():
        return None
    
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    
    if not _TOKEN_PATH.exists():
        return None
    
    try:
        creds = Credentials.from_authorized_user_file(str(_TOKEN_PATH), SCOPES)
        
        # Refresh if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            _save_credentials(creds)
        
        return creds if creds and creds.valid else None
    except Exception as e:
        logger.error(f"Error loading credentials: {e}")
        return None


def _save_credentials(creds) -> None:
    """Save OAuth credentials to disk."""
    _TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
    _TOKEN_PATH.write_text(creds.to_json())
    logger.info(f"Credentials saved to {_TOKEN_PATH}")


def authorize(force: bool = False):
    """
    Authorize with Google OAuth. Opens browser for consent if needed.
    
    Args:
        force: Force re-authorization even if valid credentials exist.
    
    Returns:
        Credentials object or None if authorization failed.
    """
    if not _check_google_deps():
        return None
    
    from google_auth_oauthlib.flow import InstalledAppFlow
    
    # Check existing credentials
    if not force:
        creds = _load_credentials()
        if creds:
            logger.info("Using existing Google credentials")
            return creds
    
    # Find client secret file
    client_secret_path = _find_client_secret()
    if not client_secret_path:
        logger.error(
            "Google OAuth client secret not found. "
            "Download from Google Cloud Console and save as client_secret.json"
        )
        return None
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(str(client_secret_path), SCOPES)
        creds = flow.run_local_server(port=0)
        _save_credentials(creds)
        logger.info("Google authorization successful")
        return creds
    except Exception as e:
        logger.error(f"Google authorization failed: {e}")
        return None


def get_gmail_service():
    """Get authorized Gmail API service."""
    if not _check_google_deps():
        return None
    
    from googleapiclient.discovery import build
    
    creds = _load_credentials()
    if not creds:
        logger.warning("Not authorized with Google. Run: python -m jc.google_oauth")
        return None
    
    return build("gmail", "v1", credentials=creds)


def get_calendar_service():
    """Get authorized Calendar API service."""
    if not _check_google_deps():
        return None
    
    from googleapiclient.discovery import build
    
    creds = _load_credentials()
    if not creds:
        logger.warning("Not authorized with Google. Run: python -m jc.google_oauth")
        return None
    
    return build("calendar", "v3", credentials=creds)


class GmailClient:
    """Gmail API client for sending and reading emails."""
    
    def __init__(self):
        self.service = get_gmail_service()
    
    @property
    def is_available(self) -> bool:
        """Check if Gmail service is available."""
        return self.service is not None
    
    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False,
        cc: Optional[str] = None,
        bcc: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send an email via Gmail API.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body (plain text or HTML)
            html: If True, body is treated as HTML
            cc: CC recipient(s)
            bcc: BCC recipient(s)
        
        Returns:
            Dict with message_id and thread_id on success, error info on failure.
        """
        if not self.is_available:
            return {"success": False, "error": "Gmail not authorized"}
        
        try:
            # Create message
            if html:
                message = MIMEMultipart("alternative")
                message.attach(MIMEText(body, "html"))
            else:
                message = MIMEText(body)
            
            message["to"] = to
            message["subject"] = subject
            if cc:
                message["cc"] = cc
            if bcc:
                message["bcc"] = bcc
            
            # Encode and send
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
            result = self.service.users().messages().send(
                userId="me", body={"raw": raw}
            ).execute()
            
            logger.info(f"Email sent to {to}: {result.get('id')}")
            return {
                "success": True,
                "message_id": result.get("id"),
                "thread_id": result.get("threadId"),
            }
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return {"success": False, "error": str(e)}
    
    def get_recent_emails(self, max_results: int = 10, query: str = "") -> List[Dict[str, Any]]:
        """
        Get recent emails from inbox.
        
        Args:
            max_results: Maximum number of emails to return
            query: Gmail search query (e.g., "is:unread", "from:example@gmail.com")
        
        Returns:
            List of email summaries.
        """
        if not self.is_available:
            return []
        
        try:
            results = self.service.users().messages().list(
                userId="me", maxResults=max_results, q=query
            ).execute()
            
            messages = results.get("messages", [])
            emails = []
            
            for msg in messages:
                detail = self.service.users().messages().get(
                    userId="me", id=msg["id"], format="metadata",
                    metadataHeaders=["From", "Subject", "Date"]
                ).execute()
                
                headers = {h["name"]: h["value"] for h in detail.get("payload", {}).get("headers", [])}
                emails.append({
                    "id": msg["id"],
                    "from": headers.get("From", ""),
                    "subject": headers.get("Subject", ""),
                    "date": headers.get("Date", ""),
                    "snippet": detail.get("snippet", ""),
                })
            
            return emails
        except Exception as e:
            logger.error(f"Failed to get emails: {e}")
            return []


class CalendarClient:
    """Google Calendar API client."""
    
    def __init__(self):
        self.service = get_calendar_service()
    
    @property
    def is_available(self) -> bool:
        """Check if Calendar service is available."""
        return self.service is not None
    
    def create_event(
        self,
        title: str,
        start_time: datetime,
        duration_minutes: int = 60,
        description: str = "",
        location: str = "",
        attendees: Optional[List[str]] = None,
        calendar_id: str = "primary",
    ) -> Dict[str, Any]:
        """
        Create a calendar event.
        
        Args:
            title: Event title
            start_time: Event start time (datetime object)
            duration_minutes: Event duration in minutes
            description: Event description
            location: Event location
            attendees: List of attendee email addresses
            calendar_id: Calendar ID (default: "primary")
        
        Returns:
            Dict with event details on success, error info on failure.
        """
        if not self.is_available:
            return {"success": False, "error": "Calendar not authorized"}
        
        try:
            end_time = start_time + timedelta(minutes=duration_minutes)
            
            event = {
                "summary": title,
                "description": description,
                "location": location,
                "start": {
                    "dateTime": start_time.isoformat(),
                    "timeZone": "UTC",
                },
                "end": {
                    "dateTime": end_time.isoformat(),
                    "timeZone": "UTC",
                },
            }
            
            if attendees:
                event["attendees"] = [{"email": email} for email in attendees]
            
            result = self.service.events().insert(
                calendarId=calendar_id, body=event
            ).execute()
            
            logger.info(f"Calendar event created: {result.get('id')}")
            return {
                "success": True,
                "event_id": result.get("id"),
                "html_link": result.get("htmlLink"),
                "start": result.get("start"),
                "end": result.get("end"),
            }
        except Exception as e:
            logger.error(f"Failed to create event: {e}")
            return {"success": False, "error": str(e)}
    
    def get_upcoming_events(
        self,
        max_results: int = 10,
        calendar_id: str = "primary",
    ) -> List[Dict[str, Any]]:
        """
        Get upcoming calendar events.
        
        Args:
            max_results: Maximum number of events to return
            calendar_id: Calendar ID (default: "primary")
        
        Returns:
            List of event summaries.
        """
        if not self.is_available:
            return []
        
        try:
            now = datetime.utcnow().isoformat() + "Z"
            
            results = self.service.events().list(
                calendarId=calendar_id,
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            ).execute()
            
            events = results.get("items", [])
            return [
                {
                    "id": event.get("id"),
                    "summary": event.get("summary", "No title"),
                    "start": event.get("start", {}).get("dateTime", event.get("start", {}).get("date")),
                    "end": event.get("end", {}).get("dateTime", event.get("end", {}).get("date")),
                    "location": event.get("location", ""),
                    "html_link": event.get("htmlLink"),
                }
                for event in events
            ]
        except Exception as e:
            logger.error(f"Failed to get events: {e}")
            return []
    
    def delete_event(self, event_id: str, calendar_id: str = "primary") -> bool:
        """Delete a calendar event."""
        if not self.is_available:
            return False
        
        try:
            self.service.events().delete(
                calendarId=calendar_id, eventId=event_id
            ).execute()
            logger.info(f"Event deleted: {event_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete event: {e}")
            return False


# CLI entry point for authorization
if __name__ == "__main__":
    import sys
    
    print("JC Google OAuth Authorization")
    print("=" * 40)
    
    # Check dependencies
    if not _check_google_deps():
        print("\nRequired packages not installed. Install with:")
        print("  pip install google-auth google-auth-oauthlib google-api-python-client")
        sys.exit(1)
    
    # Check for client secret
    client_secret = _find_client_secret()
    if not client_secret:
        print("\nClient secret file not found!")
        print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
        print("2. Create a project and enable Gmail API + Calendar API")
        print("3. Create OAuth 2.0 credentials (Desktop app)")
        print("4. Download and save as 'client_secret.json' in the project root")
        sys.exit(1)
    
    print(f"\nUsing client secret: {client_secret}")
    print("\nStarting authorization flow...")
    
    creds = authorize(force="--force" in sys.argv)
    
    if creds:
        print("\n✅ Authorization successful!")
        print(f"Token saved to: {_TOKEN_PATH}")
        
        # Test services
        gmail = GmailClient()
        calendar = CalendarClient()
        
        if gmail.is_available:
            print("✅ Gmail API ready")
        if calendar.is_available:
            print("✅ Calendar API ready")
    else:
        print("\n❌ Authorization failed")
        sys.exit(1)
