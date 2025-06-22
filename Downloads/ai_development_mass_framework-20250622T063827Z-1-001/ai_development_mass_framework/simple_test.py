import requests
import time
import json

print("Testing Cloud Deployment Demo Endpoints...")
time.sleep(12)  # Wait for server

try:
    response = requests.get('http://localhost:8000/api/demo/cloud/providers', timeout=30)
    print(f'Cloud Providers Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'Found {len(data["providers"])} cloud providers:')
        for provider in data['providers']:
            print(f'  - {provider["name"]}: {provider["status"]}')
        print("\n✅ Cloud providers endpoint working!")
    else:
        print(f'Error: {response.text}')
        
    # Test deployment
    deploy_data = {
        "app_name": "test-mass-framework",
        "cloud_provider": "docker",
        "environment": "development"
    }
    response2 = requests.post('http://localhost:8000/api/demo/cloud/deploy', 
                            json=deploy_data, timeout=30)
    print(f'\nDeploy Status: {response2.status_code}')
    if response2.status_code == 200:
        data2 = response2.json()
        print(f'Deployment ID: {data2["deployment_id"]}')
        print(f'Status: {data2["status"]}')
        print("\n✅ Deployment endpoint working!")
    else:
        print(f'Deploy Error: {response2.text}')
        
except Exception as e:
    print(f'Error: {e}')
