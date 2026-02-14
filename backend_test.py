#!/usr/bin/env python3
"""
Backend API Test Suite for Connect the Notes
Tests all API endpoints defined in server.py
"""

import requests
import json
import sys
from typing import Dict, Any, Optional, List

# Backend URL from frontend environment
BACKEND_URL = "https://music-six-degrees.preview.emergentagent.com/api"

class ConnectNotesAPITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})
        
    def test_endpoint(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Test a single endpoint and return results"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, timeout=10)
            else:
                return {"success": False, "error": f"Unsupported method: {method}"}
            
            result = {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "url": url,
                "method": method.upper()
            }
            
            if response.status_code == 200:
                try:
                    result["data"] = response.json()
                except:
                    result["data"] = response.text
            else:
                result["error"] = response.text
                
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "url": url,
                "method": method.upper()
            }
    
    def run_all_tests(self):
        """Run comprehensive test suite"""
        print(f"🧪 Testing Connect the Notes API at: {self.base_url}")
        print("=" * 60)
        
        test_results = {}
        
        # 1. Test stats endpoint first
        print("📊 Testing stats endpoint...")
        stats_result = self.test_endpoint("GET", "/stats")
        test_results["stats"] = stats_result
        
        if stats_result["success"]:
            data = stats_result["data"]
            print(f"✅ Stats: {data['totalArtists']} artists, {data['totalCollaborations']} collaborations")
        else:
            print(f"❌ Stats failed: {stats_result.get('error', 'Unknown error')}")
        
        # 2. Test artist search
        print("\n🔍 Testing artist search...")
        
        # Test Drake search
        drake_result = self.test_endpoint("GET", "/artists?search=Drake&limit=5")
        test_results["search_drake"] = drake_result
        
        if drake_result["success"]:
            drake_artists = drake_result["data"]["artists"]
            print(f"✅ Drake search: Found {len(drake_artists)} artists")
            drake_id = drake_artists[0]["id"] if drake_artists else None
        else:
            print(f"❌ Drake search failed: {drake_result.get('error', 'Unknown error')}")
            drake_id = None
        
        # Test Beyonce search (case insensitive)
        beyonce_result = self.test_endpoint("GET", "/artists?search=beyonce")
        test_results["search_beyonce"] = beyonce_result
        
        if beyonce_result["success"]:
            beyonce_artists = beyonce_result["data"]["artists"]
            print(f"✅ Beyonce search: Found {len(beyonce_artists)} artists")
            beyonce_id = beyonce_artists[0]["id"] if beyonce_artists else None
        else:
            print(f"❌ Beyonce search failed: {beyonce_result.get('error', 'Unknown error')}")
            beyonce_id = None
        
        # Test Ed Sheeran search
        ed_result = self.test_endpoint("GET", "/artists?search=Ed%20Sheeran&limit=5")
        test_results["search_ed"] = ed_result
        
        if ed_result["success"]:
            ed_artists = ed_result["data"]["artists"]
            print(f"✅ Ed Sheeran search: Found {len(ed_artists)} artists")
            ed_id = ed_artists[0]["id"] if ed_artists else None
        else:
            print(f"❌ Ed Sheeran search failed: {ed_result.get('error', 'Unknown error')}")
            ed_id = None
        
        # 3. Test random artist
        print("\n🎲 Testing random artist...")
        random_result = self.test_endpoint("GET", "/artists/random")
        test_results["random_artist"] = random_result
        
        if random_result["success"]:
            artist = random_result["data"]["artist"]
            print(f"✅ Random artist: {artist['name']} ({artist['genre']})")
            random_id = artist["id"]
        else:
            print(f"❌ Random artist failed: {random_result.get('error', 'Unknown error')}")
            random_id = None
        
        # Test random with exclude IDs
        if drake_id:
            exclude_result = self.test_endpoint("GET", f"/artists/random?excludeIds={drake_id}")
            test_results["random_exclude"] = exclude_result
            
            if exclude_result["success"]:
                excluded_artist = exclude_result["data"]["artist"]
                if excluded_artist["id"] != drake_id:
                    print(f"✅ Random exclude: Successfully excluded Drake, got {excluded_artist['name']}")
                else:
                    print("❌ Random exclude: Failed to exclude Drake")
            else:
                print(f"❌ Random exclude failed: {exclude_result.get('error', 'Unknown error')}")
        
        # 4. Test get artist by ID
        if drake_id:
            print(f"\n👤 Testing get artist by ID (Drake: {drake_id[:8]}...)...")
            artist_by_id_result = self.test_endpoint("GET", f"/artists/{drake_id}")
            test_results["artist_by_id"] = artist_by_id_result
            
            if artist_by_id_result["success"]:
                artist = artist_by_id_result["data"]
                print(f"✅ Get artist by ID: {artist['name']} ({artist['genre']})")
            else:
                print(f"❌ Get artist by ID failed: {artist_by_id_result.get('error', 'Unknown error')}")
        
        # 5. Test get collaborations for artist
        if drake_id:
            print(f"\n🎵 Testing collaborations for Drake...")
            collabs_result = self.test_endpoint("GET", f"/artists/{drake_id}/collaborations")
            test_results["artist_collaborations"] = collabs_result
            
            if collabs_result["success"]:
                collabs = collabs_result["data"]["collaborations"]
                print(f"✅ Drake collaborations: Found {len(collabs)} collaborations")
            else:
                print(f"❌ Drake collaborations failed: {collabs_result.get('error', 'Unknown error')}")
        
        # 6. Test get connected artists
        if drake_id:
            print(f"\n🔗 Testing connected artists for Drake...")
            connected_result = self.test_endpoint("GET", f"/artists/{drake_id}/connected")
            test_results["connected_artists"] = connected_result
            
            if connected_result["success"]:
                connected = connected_result["data"]["artists"]
                print(f"✅ Drake connected artists: Found {len(connected)} connected artists")
                if connected:
                    print(f"   Sample: {connected[0]['name']}")
            else:
                print(f"❌ Drake connected artists failed: {connected_result.get('error', 'Unknown error')}")
        
        # 7. Test collaborations between two artists
        if drake_id and ed_id:
            print(f"\n🤝 Testing collaborations between Drake and Ed Sheeran...")
            between_result = self.test_endpoint("GET", f"/collaborations/between/{drake_id}/{ed_id}")
            test_results["collaborations_between"] = between_result
            
            if between_result["success"]:
                between_collabs = between_result["data"]["collaborations"]
                print(f"✅ Drake-Ed collaborations: Found {len(between_collabs)} collaborations")
                if between_collabs:
                    print(f"   Sample: {between_collabs[0]['title']} ({between_collabs[0]['type']})")
            else:
                print(f"❌ Drake-Ed collaborations failed: {between_result.get('error', 'Unknown error')}")
        
        # 8. Test BFS pathfinding
        if drake_id and ed_id:
            print(f"\n🗺️ Testing BFS path finding between Drake and Ed Sheeran...")
            path_data = {"startId": drake_id, "endId": ed_id}
            path_result = self.test_endpoint("POST", "/game/find-path", path_data)
            test_results["bfs_pathfinding"] = path_result
            
            if path_result["success"]:
                path = path_result["data"]["path"]
                if path:
                    print(f"✅ BFS pathfinding: Found path with {len(path)} steps")
                    for i, step in enumerate(path):
                        print(f"   Step {i+1}: {step['collab']['title']} ({step['collab']['type']})")
                elif path == []:
                    print("✅ BFS pathfinding: Direct connection (same artist)")
                else:
                    print("✅ BFS pathfinding: No path found (expected behavior)")
            else:
                print(f"❌ BFS pathfinding failed: {path_result.get('error', 'Unknown error')}")
        
        # Test with different artists if available
        if beyonce_id and random_id and beyonce_id != random_id:
            print(f"\n🗺️ Testing BFS path finding between Beyonce and random artist...")
            path_data = {"startId": beyonce_id, "endId": random_id}
            path_result2 = self.test_endpoint("POST", "/game/find-path", path_data)
            test_results["bfs_pathfinding_2"] = path_result2
            
            if path_result2["success"]:
                path = path_result2["data"]["path"]
                if path:
                    print(f"✅ BFS pathfinding 2: Found path with {len(path)} steps")
                elif path == []:
                    print("✅ BFS pathfinding 2: Direct connection (same artist)")
                else:
                    print("✅ BFS pathfinding 2: No path found (expected behavior)")
            else:
                print(f"❌ BFS pathfinding 2 failed: {path_result2.get('error', 'Unknown error')}")
        
        print("\n" + "=" * 60)
        print("📋 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(test_results)
        passed_tests = sum(1 for r in test_results.values() if r.get("success", False))
        
        for test_name, result in test_results.items():
            status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
            print(f"{status} - {test_name}")
            if not result.get("success", False):
                print(f"      Error: {result.get('error', 'Unknown error')}")
        
        print(f"\n🎯 Results: {passed_tests}/{total_tests} tests passed")
        
        return test_results

def main():
    """Main test runner"""
    tester = ConnectNotesAPITester(BACKEND_URL)
    results = tester.run_all_tests()
    
    # Exit with error code if any tests failed
    failed_tests = [name for name, result in results.items() if not result.get("success", False)]
    if failed_tests:
        print(f"\n❌ {len(failed_tests)} test(s) failed")
        return 1
    else:
        print(f"\n✅ All tests passed!")
        return 0

if __name__ == "__main__":
    sys.exit(main())