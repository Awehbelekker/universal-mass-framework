#!/usr/bin/env python3

import requests
import json
import time

def test_demo_endpoints():
    """Test the demo cloud deployment endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing Cloud Deployment Demo Endpoints...")
    print("=" * 50)
    
    # Test 1: Cloud Providers
    try:
        response = requests.get(f"{base_url}/api/demo/cloud/providers", timeout=5)
        print(f"✅ Cloud Providers: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data['providers'])} providers")
            for provider in data['providers'][:2]:  # Show first 2
                print(f"   - {provider['name']}: {provider['status']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Cloud Providers failed: {e}")
    
    print()
    
    # Test 2: Deployment Templates
    try:
        response = requests.get(f"{base_url}/api/demo/cloud/templates", timeout=5)
        print(f"✅ Deployment Templates: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Found {len(data['templates'])} templates")
            for template in data['templates'][:2]:  # Show first 2
                print(f"   - {template['name']}: {template['description']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Deployment Templates failed: {e}")
    
    print()
    
    # Test 3: Deploy Application
    try:
        deploy_data = {
            "app_name": "test-mass-framework",
            "cloud_provider": "docker",
            "environment": "development"
        }
        response = requests.post(f"{base_url}/api/demo/cloud/deploy", 
                               json=deploy_data, timeout=5)
        print(f"✅ Deploy Application: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            deployment_id = data.get('deployment_id')
            print(f"   Deployment ID: {deployment_id}")
            print(f"   Status: {data.get('status')}")
            print(f"   API URL: {data.get('endpoints', {}).get('api_url')}")
            
            # Test 4: Check Deployment Status
            if deployment_id:
                time.sleep(1)  # Brief pause
                status_response = requests.get(f"{base_url}/api/demo/cloud/status/{deployment_id}", timeout=5)
                print(f"✅ Deployment Status: {status_response.status_code}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"   Status: {status_data.get('status')}")
                    print(f"   Progress: {status_data.get('progress')}%")
                    print(f"   CPU Usage: {status_data.get('resources', {}).get('cpu_usage'):.1f}%")
                    
                # Test 5: Get Metrics
                metrics_response = requests.get(f"{base_url}/api/demo/cloud/metrics/{deployment_id}", timeout=5)
                print(f"✅ Deployment Metrics: {metrics_response.status_code}")
                if metrics_response.status_code == 200:
                    metrics_data = metrics_response.json()
                    summary = metrics_data.get('summary', {})
                    print(f"   Total Requests: {summary.get('total_requests')}")
                    print(f"   Avg Response Time: {summary.get('avg_response_time'):.1f}ms")
                    
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Deploy Application failed: {e}")
    
    print()
    print("Demo endpoint testing completed!")

if __name__ == "__main__":
    test_demo_endpoints()
