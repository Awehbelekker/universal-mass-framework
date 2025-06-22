#!/usr/bin/env python3

import requests
import json

# Test the actual endpoint
def test_recommend_agents_endpoint():
    """Test the actual endpoint to see what error we get"""
    try:
        # Start the server first
        import subprocess
        import time
        import sys
        import os
        
        # Change to the project directory
        os.chdir(r"c:\Users\richard.downing\New folder\ai_development_mass_framework")
        
        # Start the server in the background
        server_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", "--port", "8000"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a bit for the server to start
        time.sleep(3)
        
        try:
            # Make the request
            url = "http://localhost:8000/api/ai/recommend-agents"
            payload = {
                "task_description": "Build a web scraper with error handling and tests",
                "context": {"domain": "web_scraping", "complexity": "intermediate"},
                "preferences": {"focus": "reliability"}
            }
            
            print(f"Making request to {url}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(url, json=payload, timeout=10)
            
            print(f"Status code: {response.status_code}")
            print(f"Response headers: {dict(response.headers)}")
            print(f"Response content: {response.text}")
            
            if response.status_code != 200:
                print("ERROR: Non-200 status code!")
            else:
                data = response.json()
                print(f"Response data: {json.dumps(data, indent=2)}")
                
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"Other error: {e}")
        finally:
            # Kill the server
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
                
    except Exception as e:
        print(f"Setup error: {e}")

if __name__ == "__main__":
    test_recommend_agents_endpoint()
