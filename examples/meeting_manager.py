#!/usr/bin/env python3
"""
Meeting Manager Example - Advanced usage of GoTo Connect Authentication Library.
"""

from datetime import datetime, timedelta
from gotoconnect_auth import GoToConnectAuth


class MeetingManager:
    """A class to manage GoTo Connect meetings using the auth library."""
    
    def __init__(self, auth: GoToConnectAuth):
        self.auth = auth
        self.base_url = "https://api.goto.com/rest/meetings/v1"
    
    def get_meetings(self, limit: int = 50) -> list:
        """Get all meetings for the authenticated user."""
        try:
            response = self.auth.get(f"{self.base_url}/meetings?limit={limit}")
            return response.json().get('meetings', [])
        except Exception as e:
            print(f"Error getting meetings: {e}")
            return []
    
    def get_meeting(self, meeting_id: str) -> dict:
        """Get a specific meeting by ID."""
        try:
            response = self.auth.get(f"{self.base_url}/meetings/{meeting_id}")
            return response.json()
        except Exception as e:
            print(f"Error getting meeting {meeting_id}: {e}")
            return {}
    
    def create_meeting(self, subject: str, start_time: datetime, duration_minutes: int = 60, description: str = "") -> dict:
        """Create a new meeting."""
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        meeting_data = {
            "subject": subject,
            "startTime": start_time.isoformat() + "Z",
            "endTime": end_time.isoformat() + "Z",
            "description": description
        }
        
        try:
            response = self.auth.post(f"{self.base_url}/meetings", json=meeting_data)
            return response.json()
        except Exception as e:
            print(f"Error creating meeting: {e}")
            return {}
    
    def update_meeting(self, meeting_id: str, **kwargs) -> dict:
        """Update an existing meeting."""
        try:
            response = self.auth.put(f"{self.base_url}/meetings/{meeting_id}", json=kwargs)
            return response.json()
        except Exception as e:
            print(f"Error updating meeting {meeting_id}: {e}")
            return {}
    
    def delete_meeting(self, meeting_id: str) -> bool:
        """Delete a meeting."""
        try:
            self.auth.delete(f"{self.base_url}/meetings/{meeting_id}")
            return True
        except Exception as e:
            print(f"Error deleting meeting {meeting_id}: {e}")
            return False
    
    def get_upcoming_meetings(self, days: int = 7) -> list:
        """Get upcoming meetings within the specified number of days."""
        meetings = self.get_meetings()
        now = datetime.utcnow()
        cutoff = now + timedelta(days=days)
        
        upcoming = []
        for meeting in meetings:
            start_time_str = meeting.get('startTime')
            if start_time_str:
                start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
                if now <= start_time <= cutoff:
                    upcoming.append(meeting)
        
        return sorted(upcoming, key=lambda m: m.get('startTime', ''))
    
    def print_meeting_summary(self, meeting: dict) -> None:
        """Print a formatted meeting summary."""
        print(f"📅 {meeting.get('subject', 'No Subject')}")
        print(f"   ID: {meeting.get('meetingId', 'Unknown')}")
        print(f"   Start: {meeting.get('startTime', 'Unknown')}")
        print(f"   End: {meeting.get('endTime', 'Unknown')}")
        if meeting.get('description'):
            print(f"   Description: {meeting.get('description')}")
        print()


def main():
    """Demonstrate the MeetingManager class."""
    
    # Initialize authentication
    # Make sure you have set up your .env file with your credentials
    auth = GoToConnectAuth.from_env()
    
    try:
        # Authenticate
        print("🔐 Authenticating with GoTo Connect...")
        auth.authenticate()
        
        if not auth.is_authenticated():
            print("❌ Authentication failed!")
            return
        
        print("✅ Successfully authenticated!")
        
        # Create meeting manager
        manager = MeetingManager(auth)
        
        # Get upcoming meetings
        print("\n📅 Getting upcoming meetings...")
        upcoming = manager.get_upcoming_meetings(days=30)
        print(f"Found {len(upcoming)} upcoming meetings:")
        
        for meeting in upcoming:
            manager.print_meeting_summary(meeting)
        
        # Create a new meeting
        print("➕ Creating a new meeting...")
        start_time = datetime.utcnow() + timedelta(hours=1)
        new_meeting = manager.create_meeting(
            subject="Python Library Test Meeting",
            start_time=start_time,
            duration_minutes=30,
            description="This meeting was created using the GoTo Connect Auth Library"
        )
        
        if new_meeting:
            print("✅ Meeting created successfully!")
            manager.print_meeting_summary(new_meeting)
            
            # Update the meeting
            print("✏️ Updating meeting description...")
            updated = manager.update_meeting(
                new_meeting['meetingId'],
                description="Updated description from Python library"
            )
            
            if updated:
                print("✅ Meeting updated successfully!")
                manager.print_meeting_summary(updated)
            
            # Clean up - delete the test meeting
            print("🗑️ Cleaning up test meeting...")
            if manager.delete_meeting(new_meeting['meetingId']):
                print("✅ Test meeting deleted successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 