"""
Test cases for Auth and Leaderboard features
- Authentication endpoints
- Leaderboard endpoints with period/sort filters
- Game result submission auth requirement
"""
import pytest
import requests
import os

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestAuthEndpoints:
    """Test authentication endpoints"""
    
    def test_auth_me_returns_401_when_not_authenticated(self):
        """GET /api/auth/me should return 401 when not logged in"""
        response = requests.get(f"{BASE_URL}/api/auth/me")
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Not authenticated"
    
    def test_auth_session_requires_session_id(self):
        """POST /api/auth/session should require session_id"""
        response = requests.post(
            f"{BASE_URL}/api/auth/session", 
            json={},
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
    
    def test_auth_logout_works_without_session(self):
        """POST /api/auth/logout should work even without session"""
        response = requests.post(f"{BASE_URL}/api/auth/logout")
        assert response.status_code == 200
        data = response.json()
        assert data.get("message") == "Logged out successfully"


class TestLeaderboardEndpoints:
    """Test leaderboard endpoints"""
    
    def test_leaderboard_default_returns_200(self):
        """GET /api/leaderboard should return 200 with default params"""
        response = requests.get(f"{BASE_URL}/api/leaderboard")
        assert response.status_code == 200
        data = response.json()
        assert "leaderboard" in data
        assert isinstance(data["leaderboard"], list)
    
    def test_leaderboard_period_daily(self):
        """GET /api/leaderboard with period=daily"""
        response = requests.get(f"{BASE_URL}/api/leaderboard?period=daily")
        assert response.status_code == 200
        data = response.json()
        assert data.get("period") == "daily"
        assert "leaderboard" in data
    
    def test_leaderboard_period_weekly(self):
        """GET /api/leaderboard with period=weekly"""
        response = requests.get(f"{BASE_URL}/api/leaderboard?period=weekly")
        assert response.status_code == 200
        data = response.json()
        assert data.get("period") == "weekly"
        assert "leaderboard" in data
    
    def test_leaderboard_period_all(self):
        """GET /api/leaderboard with period=all"""
        response = requests.get(f"{BASE_URL}/api/leaderboard?period=all")
        assert response.status_code == 200
        data = response.json()
        assert data.get("period") == "all"
        assert "leaderboard" in data
    
    def test_leaderboard_sort_by_wins(self):
        """GET /api/leaderboard with sort_by=wins"""
        response = requests.get(f"{BASE_URL}/api/leaderboard?sort_by=wins")
        assert response.status_code == 200
        data = response.json()
        assert data.get("sort_by") == "wins"
        assert "leaderboard" in data
    
    def test_leaderboard_sort_by_steps(self):
        """GET /api/leaderboard with sort_by=steps"""
        response = requests.get(f"{BASE_URL}/api/leaderboard?sort_by=steps")
        assert response.status_code == 200
        data = response.json()
        assert data.get("sort_by") == "steps"
        assert "leaderboard" in data
    
    def test_leaderboard_sort_by_time(self):
        """GET /api/leaderboard with sort_by=time"""
        response = requests.get(f"{BASE_URL}/api/leaderboard?sort_by=time")
        assert response.status_code == 200
        data = response.json()
        assert data.get("sort_by") == "time"
        assert "leaderboard" in data
    
    def test_leaderboard_with_limit(self):
        """GET /api/leaderboard with custom limit"""
        response = requests.get(f"{BASE_URL}/api/leaderboard?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "leaderboard" in data
        # Leaderboard may be empty but should work
    
    def test_leaderboard_combined_filters(self):
        """GET /api/leaderboard with multiple filters"""
        response = requests.get(f"{BASE_URL}/api/leaderboard?period=weekly&sort_by=wins&limit=5")
        assert response.status_code == 200
        data = response.json()
        assert data.get("period") == "weekly"
        assert data.get("sort_by") == "wins"
        assert "leaderboard" in data


class TestGameResultSubmission:
    """Test game result submission"""
    
    def test_submit_result_requires_auth(self):
        """POST /api/game/submit-result should require authentication"""
        response = requests.post(
            f"{BASE_URL}/api/game/submit-result",
            json={
                "artist1_name": "Test Artist 1",
                "artist2_name": "Test Artist 2",
                "steps": 3,
                "time_seconds": 45,
                "difficulty": "medium",
                "timed_mode": True,
                "won": True
            },
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Not authenticated"


class TestUserHistoryAndRank:
    """Test user history and rank endpoints"""
    
    def test_user_rank_endpoint_exists(self):
        """GET /api/leaderboard/user/{user_id} should return user rank data"""
        # Test with a fake user_id - should return empty/null rank data
        response = requests.get(f"{BASE_URL}/api/leaderboard/user/fake_user_123")
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert data["user_id"] == "fake_user_123"
        assert "rank" in data
        assert data["rank"] is None  # No rank for non-existent user
    
    def test_user_rank_with_period(self):
        """GET /api/leaderboard/user/{user_id} with period filter"""
        response = requests.get(f"{BASE_URL}/api/leaderboard/user/fake_user_123?period=daily")
        assert response.status_code == 200
        data = response.json()
        assert data.get("period") == "daily"
    
    def test_user_history_endpoint_exists(self):
        """GET /api/user/{user_id}/history should return user's game history"""
        response = requests.get(f"{BASE_URL}/api/user/fake_user_123/history")
        assert response.status_code == 200
        data = response.json()
        assert "history" in data
        assert isinstance(data["history"], list)
    
    def test_user_history_with_limit(self):
        """GET /api/user/{user_id}/history with limit"""
        response = requests.get(f"{BASE_URL}/api/user/fake_user_123/history?limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "history" in data


class TestExistingEndpoints:
    """Verify existing endpoints still work"""
    
    def test_api_root(self):
        """GET /api/ should return API message"""
        response = requests.get(f"{BASE_URL}/api/")
        assert response.status_code == 200
        data = response.json()
        assert data.get("message") == "Connect the Notes API"
    
    def test_stats_endpoint(self):
        """GET /api/stats should return artist/collaboration counts"""
        response = requests.get(f"{BASE_URL}/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert "totalArtists" in data
        assert "totalCollaborations" in data
        assert data["totalArtists"] > 0
        assert data["totalCollaborations"] > 0
    
    def test_artists_search(self):
        """GET /api/artists with search should work"""
        response = requests.get(f"{BASE_URL}/api/artists?search=Drake")
        assert response.status_code == 200
        data = response.json()
        assert "artists" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
