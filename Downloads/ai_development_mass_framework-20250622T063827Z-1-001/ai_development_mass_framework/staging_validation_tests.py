#!/usr/bin/env python3
"""
Staging Deployment Validation Tests
"""

import requests
import json
import time
from datetime import datetime

def test_health_endpoint():
    """Test health check endpoint"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_api_status():
    """Test API status endpoint"""
    try:
        response = requests.get("http://localhost:8000/api/v1/status", timeout=10)
        if response.status_code == 200:
            print("✅ API status check passed")
            return True
        else:
            print(f"❌ API status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API status error: {e}")
        return False

def test_analysis_endpoint():
    """Test data analysis endpoint"""
    try:
        test_data = {
            "data": [1, 2, 3, 4, 5],
            "type": "time_series",
            "analysis_types": ["patterns", "predictions"]
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/analyze",
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Analysis endpoint passed")
            print(f"   Analysis ID: {result.get('analysis_id')}")
            return True
        else:
            print(f"❌ Analysis endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analysis endpoint error: {e}")
        return False

def run_all_tests():
    """Run all validation tests"""
    print("🧪 Running Staging Deployment Validation Tests")
    print("=" * 50)
    print(f"Test Time: {datetime.now()}")
    print()
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("API Status", test_api_status),
        ("Analysis Endpoint", test_analysis_endpoint)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Staging deployment successful.")
        return True
    else:
        print("❌ Some tests failed. Please check the deployment.")
        return False

if __name__ == "__main__":
    run_all_tests()
