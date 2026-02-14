"""
Test suite for Connect the Notes API - Brazilian Artists Focus
Tests search, collaboration, and path finding for Brazilian artists including
Anitta, Ludmilla, Caetano Veloso, and cross-regional connections to international artists.
"""
import pytest
import requests
import os

# Get the backend URL from environment variable
BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

class TestBrazilianArtistSearch:
    """Search functionality tests for Brazilian artists"""
    
    def test_search_anitta(self):
        """Test searching for Anitta (Brazilian pop/reggaeton)"""
        response = requests.get(f"{BASE_URL}/api/artists", params={"search": "Anitta"})
        assert response.status_code == 200
        data = response.json()
        assert "artists" in data
        assert len(data["artists"]) >= 1
        anitta = data["artists"][0]
        assert anitta["name"] == "Anitta"
        assert "Latin" in anitta["genre"] or "Reggaeton" in anitta["genre"]
        print(f"✅ Found Anitta with genre: {anitta['genre']}")
    
    def test_search_ludmilla(self):
        """Test searching for Ludmilla (Brazilian funk/R&B)"""
        response = requests.get(f"{BASE_URL}/api/artists", params={"search": "Ludmilla"})
        assert response.status_code == 200
        data = response.json()
        assert len(data["artists"]) >= 1
        ludmilla = data["artists"][0]
        assert ludmilla["name"] == "Ludmilla"
        assert "Funk" in ludmilla["genre"] or "Brasileiro" in ludmilla["genre"]
        print(f"✅ Found Ludmilla with genre: {ludmilla['genre']}")
    
    def test_search_caetano_veloso(self):
        """Test searching for Caetano Veloso (MPB legend)"""
        response = requests.get(f"{BASE_URL}/api/artists", params={"search": "Caetano"})
        assert response.status_code == 200
        data = response.json()
        assert len(data["artists"]) >= 1
        caetano = data["artists"][0]
        assert "Caetano" in caetano["name"]
        assert "MPB" in caetano["genre"]
        print(f"✅ Found Caetano Veloso with genre: {caetano['genre']}")
    
    def test_search_alok(self):
        """Test searching for Alok (Brazilian EDM producer)"""
        response = requests.get(f"{BASE_URL}/api/artists", params={"search": "Alok"})
        assert response.status_code == 200
        data = response.json()
        assert len(data["artists"]) >= 1
        alok = data["artists"][0]
        assert alok["name"] == "Alok"
        assert "EDM" in alok["genre"] or "Brazilian" in alok["genre"]
        print(f"✅ Found Alok with genre: {alok['genre']}")


class TestBrazilianArtistCollaborations:
    """Collaboration tests for Brazilian artists"""
    
    @pytest.fixture
    def anitta_id(self):
        """Get Anitta's ID"""
        response = requests.get(f"{BASE_URL}/api/artists", params={"search": "Anitta"})
        return response.json()["artists"][0]["id"]
    
    @pytest.fixture
    def ludmilla_id(self):
        """Get Ludmilla's ID"""
        response = requests.get(f"{BASE_URL}/api/artists", params={"search": "Ludmilla"})
        return response.json()["artists"][0]["id"]
    
    def test_anitta_has_collaborations(self, anitta_id):
        """Verify Anitta has multiple collaborations"""
        response = requests.get(f"{BASE_URL}/api/artists/{anitta_id}/collaborations")
        assert response.status_code == 200
        data = response.json()
        assert "collaborations" in data
        collabs = data["collaborations"]
        assert len(collabs) >= 30  # Anitta has 50+ collaborations
        print(f"✅ Anitta has {len(collabs)} collaborations")
        
        # Check for variety of collaboration types
        types = set(c["type"] for c in collabs)
        assert "song" in types
        print(f"✅ Collaboration types found: {types}")
    
    def test_ludmilla_has_collaborations(self, ludmilla_id):
        """Verify Ludmilla has multiple collaborations"""
        response = requests.get(f"{BASE_URL}/api/artists/{ludmilla_id}/collaborations")
        assert response.status_code == 200
        data = response.json()
        collabs = data["collaborations"]
        assert len(collabs) >= 15
        print(f"✅ Ludmilla has {len(collabs)} collaborations")
    
    def test_anitta_connected_artists(self, anitta_id):
        """Verify Anitta has many connected artists"""
        response = requests.get(f"{BASE_URL}/api/artists/{anitta_id}/connected")
        assert response.status_code == 200
        data = response.json()
        assert "artists" in data
        connected = data["artists"]
        assert len(connected) >= 30  # Anitta is very connected
        print(f"✅ Anitta has {len(connected)} connected artists")
        
        # Check if some Brazilian artists are among connections
        connected_names = [a["name"] for a in connected]
        print(f"Some connected artists: {connected_names[:10]}")


class TestBrazilianArtistPathFinding:
    """Path finding tests between Brazilian and international artists"""
    
    @pytest.fixture
    def artist_ids(self):
        """Get IDs for test artists"""
        ids = {}
        artists_to_find = ["Anitta", "Ludmilla", "Rihanna", "Caetano"]
        for name in artists_to_find:
            response = requests.get(f"{BASE_URL}/api/artists", params={"search": name})
            if response.status_code == 200 and response.json()["artists"]:
                ids[name] = response.json()["artists"][0]["id"]
        return ids
    
    def test_anitta_to_ludmilla_direct_path(self, artist_ids):
        """Test direct path from Anitta to Ludmilla (should be 1 step)"""
        response = requests.post(
            f"{BASE_URL}/api/game/find-path",
            json={"startId": artist_ids["Anitta"], "endId": artist_ids["Ludmilla"]}
        )
        assert response.status_code == 200
        data = response.json()
        assert "path" in data
        path = data["path"]
        assert path is not None
        assert len(path) == 1  # Direct collaboration exists
        assert path[0]["collab"]["title"] == "Anitta x Ludmilla Medley"
        print(f"✅ Found direct path: {path[0]['collab']['title']}")
    
    def test_anitta_to_rihanna_direct_path(self, artist_ids):
        """Test direct path from Anitta to Rihanna (Lemon Remix)"""
        response = requests.post(
            f"{BASE_URL}/api/game/find-path",
            json={"startId": artist_ids["Anitta"], "endId": artist_ids["Rihanna"]}
        )
        assert response.status_code == 200
        data = response.json()
        path = data["path"]
        assert path is not None
        assert len(path) == 1  # Direct via Lemon Remix
        assert "Lemon" in path[0]["collab"]["title"]
        print(f"✅ Anitta -> Rihanna direct: {path[0]['collab']['title']}")
    
    def test_caetano_to_anitta_path(self, artist_ids):
        """Test path from Caetano Veloso to Anitta"""
        if "Caetano" not in artist_ids:
            pytest.skip("Caetano Veloso not found")
        
        response = requests.post(
            f"{BASE_URL}/api/game/find-path",
            json={"startId": artist_ids["Caetano"], "endId": artist_ids["Anitta"]}
        )
        assert response.status_code == 200
        data = response.json()
        path = data["path"]
        assert path is not None
        print(f"✅ Caetano -> Anitta path found ({len(path)} steps)")
        for step in path:
            print(f"   Via: {step['collab']['title']}")


class TestStatsEndpoint:
    """Test stats endpoint reflects updated database"""
    
    def test_stats_count(self):
        """Verify database has 590 artists and 1087 collaborations"""
        response = requests.get(f"{BASE_URL}/api/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["totalArtists"] == 590
        assert data["totalCollaborations"] == 1087
        print(f"✅ Stats: {data['totalArtists']} artists, {data['totalCollaborations']} connections")


class TestRandomArtist:
    """Test random artist endpoint"""
    
    def test_random_artist_returns_data(self):
        """Verify random artist endpoint returns valid artist"""
        response = requests.get(f"{BASE_URL}/api/artists/random")
        assert response.status_code == 200
        data = response.json()
        assert "artist" in data
        artist = data["artist"]
        assert "id" in artist
        assert "name" in artist
        assert "genre" in artist
        print(f"✅ Random artist: {artist['name']} ({artist['genre']})")
    
    def test_random_artist_excludes_ids(self):
        """Verify exclude IDs parameter works"""
        # First get Anitta's ID
        search_response = requests.get(f"{BASE_URL}/api/artists", params={"search": "Anitta"})
        anitta_id = search_response.json()["artists"][0]["id"]
        
        # Get random artist excluding Anitta
        response = requests.get(f"{BASE_URL}/api/artists/random", params={"excludeIds": anitta_id})
        assert response.status_code == 200
        random_artist = response.json()["artist"]
        assert random_artist["id"] != anitta_id
        print(f"✅ Random artist (excluding Anitta): {random_artist['name']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
