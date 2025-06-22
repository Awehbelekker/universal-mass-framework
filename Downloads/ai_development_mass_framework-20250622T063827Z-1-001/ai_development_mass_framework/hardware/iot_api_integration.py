"""
IoT/API Hardware Integration System for MASS Framework
Enables simple integration with hardware devices and APIs via document upload or supplier login
"""

import asyncio
import json
import os
import tempfile
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass, asdict
import re
import xml.etree.ElementTree as ET
from pathlib import Path
import zipfile
import yaml

class IntegrationType(Enum):
    """Types of integrations supported"""
    IOT_DEVICE = "iot_device"
    REST_API = "rest_api"
    WEBHOOK = "webhook"
    MQTT = "mqtt"
    WEBSOCKET = "websocket"
    GRAPHQL = "graphql"
    SOAP = "soap"
    DATABASE = "database"
    FILE_SYSTEM = "file_system"

class DocumentType(Enum):
    """Types of documentation supported"""
    API_SPEC = "api_spec"  # OpenAPI/Swagger
    POSTMAN_COLLECTION = "postman_collection"
    HARDWARE_MANUAL = "hardware_manual"
    SDK_DOCUMENTATION = "sdk_documentation"
    PROTOCOL_SPEC = "protocol_spec"
    DATABASE_SCHEMA = "database_schema"
    CUSTOM_DOC = "custom_doc"

class HardwareCategory(Enum):
    """Categories of hardware devices"""
    SENSORS = "sensors"
    ACTUATORS = "actuators"
    DISPLAYS = "displays"
    CAMERAS = "cameras"
    MICROCONTROLLERS = "microcontrollers"
    GATEWAYS = "gateways"
    SMART_DEVICES = "smart_devices"
    INDUSTRIAL = "industrial"
    AUTOMOTIVE = "automotive"
    MEDICAL = "medical"

@dataclass
class HardwareDevice:
    """Represents a hardware device"""
    id: str
    name: str
    category: HardwareCategory
    manufacturer: str
    model: str
    description: str
    communication_protocols: List[str]
    data_formats: List[str]
    capabilities: List[str]
    connection_info: Dict[str, Any]
    documentation_url: Optional[str] = None
    sdk_available: bool = False
    sample_code: Optional[str] = None

@dataclass
class APIEndpoint:
    """Represents an API endpoint"""
    id: str
    name: str
    url: str
    method: str
    description: str
    parameters: List[Dict[str, Any]]
    headers: Dict[str, str]
    request_body: Optional[Dict[str, Any]]
    response_schema: Dict[str, Any]
    authentication: Dict[str, Any]
    rate_limits: Optional[Dict[str, Any]] = None

@dataclass
class Integration:
    """Represents a complete integration"""
    id: str
    name: str
    type: IntegrationType
    description: str
    devices: List[HardwareDevice]
    endpoints: List[APIEndpoint]
    configuration: Dict[str, Any]
    generated_code: Dict[str, str]  # language -> code
    test_results: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

class DocumentParser:
    """Parses various types of technical documentation"""
    
    def __init__(self):
        self.supported_formats = ['.json', '.yaml', '.yml', '.xml', '.pdf', '.txt', '.md']
    
    async def parse_document(self, file_path: str, doc_type: DocumentType) -> Dict[str, Any]:
        """Parse a technical document and extract integration information"""
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if doc_type == DocumentType.API_SPEC:
            return await self._parse_api_spec(file_path, file_ext)
        elif doc_type == DocumentType.POSTMAN_COLLECTION:
            return await self._parse_postman_collection(file_path)
        elif doc_type == DocumentType.HARDWARE_MANUAL:
            return await self._parse_hardware_manual(file_path, file_ext)
        elif doc_type == DocumentType.SDK_DOCUMENTATION:
            return await self._parse_sdk_documentation(file_path, file_ext)
        elif doc_type == DocumentType.PROTOCOL_SPEC:
            return await self._parse_protocol_spec(file_path, file_ext)
        elif doc_type == DocumentType.DATABASE_SCHEMA:
            return await self._parse_database_schema(file_path, file_ext)
        else:
            return await self._parse_custom_doc(file_path, file_ext)
    
    async def _parse_api_spec(self, file_path: str, file_ext: str) -> Dict[str, Any]:
        """Parse OpenAPI/Swagger specification"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_ext in ['.yaml', '.yml']:
                    spec = yaml.safe_load(f)
                else:
                    spec = json.load(f)
            
            # Extract API information
            api_info = {
                "type": "rest_api",
                "name": spec.get("info", {}).get("title", "Unnamed API"),
                "version": spec.get("info", {}).get("version", "1.0.0"),
                "description": spec.get("info", {}).get("description", ""),
                "base_url": spec.get("servers", [{}])[0].get("url", ""),
                "endpoints": []
            }
            
            # Parse endpoints
            paths = spec.get("paths", {})
            for path, methods in paths.items():
                for method, details in methods.items():
                    if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                        endpoint = {
                            "path": path,
                            "method": method.upper(),
                            "summary": details.get("summary", ""),
                            "description": details.get("description", ""),
                            "parameters": details.get("parameters", []),
                            "request_body": details.get("requestBody", {}),
                            "responses": details.get("responses", {}),
                            "security": details.get("security", [])
                        }
                        api_info["endpoints"].append(endpoint)
            
            # Parse authentication
            security_schemes = spec.get("components", {}).get("securitySchemes", {})
            api_info["authentication"] = security_schemes
            
            return api_info
            
        except Exception as e:
            return {"error": f"Failed to parse API spec: {str(e)}"}
    
    async def _parse_postman_collection(self, file_path: str) -> Dict[str, Any]:
        """Parse Postman collection"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                collection = json.load(f)
            
            api_info = {
                "type": "rest_api",
                "name": collection.get("info", {}).get("name", "Postman Collection"),
                "description": collection.get("info", {}).get("description", ""),
                "endpoints": []
            }
            
            # Parse items (requests)
            items = collection.get("item", [])
            for item in items:
                if "request" in item:
                    request = item["request"]
                    endpoint = {
                        "name": item.get("name", ""),
                        "method": request.get("method", "GET"),
                        "url": request.get("url", ""),
                        "headers": request.get("header", []),
                        "body": request.get("body", {}),
                        "description": item.get("description", "")
                    }
                    api_info["endpoints"].append(endpoint)
            
            return api_info
            
        except Exception as e:
            return {"error": f"Failed to parse Postman collection: {str(e)}"}
    
    async def _parse_hardware_manual(self, file_path: str, file_ext: str) -> Dict[str, Any]:
        """Parse hardware manual/documentation"""
        try:
            # For demo purposes, simulate parsing
            device_info = {
                "type": "iot_device",
                "name": "Smart Sensor Device",
                "category": "sensors",
                "manufacturer": "TechCorp",
                "model": "TC-100",
                "description": "Multi-purpose IoT sensor with temperature, humidity, and motion detection",
                "protocols": ["HTTP", "MQTT", "WebSocket"],
                "data_formats": ["JSON", "XML"],
                "capabilities": [
                    "Temperature monitoring (-40°C to 85°C)",
                    "Humidity detection (0-100% RH)",
                    "Motion detection (PIR sensor)",
                    "Wi-Fi connectivity",
                    "Battery powered (up to 2 years)",
                    "Real-time alerts"
                ],
                "connection": {
                    "wifi": {
                        "supported_bands": ["2.4GHz", "5GHz"],
                        "security": ["WPA2", "WPA3"]
                    },
                    "endpoints": {
                        "data": "/api/v1/sensor/data",
                        "config": "/api/v1/sensor/config",
                        "status": "/api/v1/sensor/status"
                    }
                },
                "sample_data": {
                    "temperature": 23.5,
                    "humidity": 45.2,
                    "motion": False,
                    "battery": 87,
                    "timestamp": "2024-01-15T10:30:00Z"
                }
            }
            
            return device_info
            
        except Exception as e:
            return {"error": f"Failed to parse hardware manual: {str(e)}"}
    
    async def _parse_sdk_documentation(self, file_path: str, file_ext: str) -> Dict[str, Any]:
        """Parse SDK documentation"""
        try:
            # Simulate SDK parsing
            sdk_info = {
                "type": "sdk",
                "name": "IoT Device SDK",
                "language": "Python",
                "version": "2.1.0",
                "description": "Python SDK for IoT device integration",
                "installation": "pip install iot-device-sdk",
                "classes": [
                    {
                        "name": "DeviceManager",
                        "methods": [
                            "connect()",
                            "disconnect()",
                            "send_data(data)",
                            "get_status()",
                            "configure(config)"
                        ]
                    },
                    {
                        "name": "SensorData",
                        "properties": [
                            "temperature",
                            "humidity",
                            "motion",
                            "timestamp"
                        ]
                    }
                ],
                "examples": [
                    {
                        "title": "Basic Connection",
                        "code": """
from iot_device_sdk import DeviceManager

# Initialize device manager
device = DeviceManager(device_id="TC-100", api_key="your_api_key")

# Connect to device
await device.connect()

# Get sensor data
data = await device.get_sensor_data()
print(f"Temperature: {data.temperature}°C")
print(f"Humidity: {data.humidity}%")

# Disconnect
await device.disconnect()
"""
                    }
                ]
            }
            
            return sdk_info
            
        except Exception as e:
            return {"error": f"Failed to parse SDK documentation: {str(e)}"}
    
    async def _parse_protocol_spec(self, file_path: str, file_ext: str) -> Dict[str, Any]:
        """Parse protocol specification"""
        try:
            protocol_info = {
                "type": "protocol",
                "name": "Custom IoT Protocol",
                "version": "1.0",
                "transport": "TCP/UDP",
                "port": 8883,
                "security": "TLS 1.3",
                "message_format": "Binary",
                "commands": [
                    {
                        "name": "GET_STATUS",
                        "code": "0x01",
                        "description": "Get device status",
                        "parameters": [],
                        "response": "Status object"
                    },
                    {
                        "name": "SET_CONFIG",
                        "code": "0x02",
                        "description": "Update device configuration",
                        "parameters": ["config_json"],
                        "response": "Success/Error"
                    }
                ]
            }
            
            return protocol_info
            
        except Exception as e:
            return {"error": f"Failed to parse protocol spec: {str(e)}"}
    
    async def _parse_database_schema(self, file_path: str, file_ext: str) -> Dict[str, Any]:
        """Parse database schema"""
        try:
            schema_info = {
                "type": "database",
                "name": "IoT Data Schema",
                "database_type": "PostgreSQL",
                "tables": [
                    {
                        "name": "devices",
                        "columns": [
                            {"name": "id", "type": "UUID", "primary_key": True},
                            {"name": "name", "type": "VARCHAR(255)", "nullable": False},
                            {"name": "type", "type": "VARCHAR(100)", "nullable": False},
                            {"name": "created_at", "type": "TIMESTAMP", "default": "NOW()"}
                        ]
                    },
                    {
                        "name": "sensor_data",
                        "columns": [
                            {"name": "id", "type": "BIGSERIAL", "primary_key": True},
                            {"name": "device_id", "type": "UUID", "foreign_key": "devices.id"},
                            {"name": "temperature", "type": "DECIMAL(5,2)"},
                            {"name": "humidity", "type": "DECIMAL(5,2)"},
                            {"name": "timestamp", "type": "TIMESTAMP", "default": "NOW()"}
                        ]
                    }
                ]
            }
            
            return schema_info
            
        except Exception as e:
            return {"error": f"Failed to parse database schema: {str(e)}"}
    
    async def _parse_custom_doc(self, file_path: str, file_ext: str) -> Dict[str, Any]:
        """Parse custom documentation"""
        try:
            # Basic text extraction for custom docs
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract key information using regex patterns
            urls = re.findall(r'https?://[^\s<>"]+', content)
            api_keys = re.findall(r'api[_-]?key|token|secret', content, re.IGNORECASE)
            endpoints = re.findall(r'/api/[^\s<>"]+', content)
            
            custom_info = {
                "type": "custom",
                "content_length": len(content),
                "urls_found": urls[:10],  # First 10 URLs
                "potential_endpoints": endpoints[:10],
                "has_authentication": len(api_keys) > 0,
                "file_type": file_ext,
                "extraction_hints": [
                    "Review URLs for API endpoints",
                    "Check for authentication requirements",
                    "Look for data format specifications",
                    "Identify connection parameters"
                ]
            }
            
            return custom_info
            
        except Exception as e:
            return {"error": f"Failed to parse custom document: {str(e)}"}

class SupplierIntegration:
    """Integration with hardware/API suppliers"""
    
    def __init__(self):
        self.supported_suppliers = self._initialize_suppliers()
    
    def _initialize_suppliers(self) -> Dict[str, Dict[str, Any]]:
        """Initialize supported supplier integrations"""
        return {
            "arduino": {
                "name": "Arduino",
                "type": "hardware",
                "api_base": "https://api.arduino.cc/v1",
                "auth_type": "oauth2",
                "devices": ["Arduino Uno", "Arduino Nano", "Arduino MKR1000"],
                "protocols": ["HTTP", "MQTT", "Serial"],
                "categories": ["microcontrollers", "sensors", "actuators"]
            },
            "raspberry_pi": {
                "name": "Raspberry Pi",
                "type": "hardware",
                "api_base": "https://api.raspberrypi.org/v1",
                "auth_type": "api_key",
                "devices": ["Pi 4", "Pi Zero", "Pi Pico"],
                "protocols": ["HTTP", "SSH", "GPIO"],
                "categories": ["microcontrollers", "cameras", "displays"]
            },
            "aws_iot": {
                "name": "AWS IoT Core",
                "type": "platform",
                "api_base": "https://iot.amazonaws.com",
                "auth_type": "aws_signature",
                "services": ["Device Management", "Message Broker", "Rules Engine"],
                "protocols": ["MQTT", "HTTP", "WebSocket"],
                "categories": ["gateways", "cloud_services"]
            },
            "google_iot": {
                "name": "Google Cloud IoT",
                "type": "platform",
                "api_base": "https://cloudiot.googleapis.com/v1",
                "auth_type": "oauth2",
                "services": ["Device Registry", "Telemetry", "Configuration"],
                "protocols": ["MQTT", "HTTP"],
                "categories": ["gateways", "cloud_services"]
            },
            "particle": {
                "name": "Particle",
                "type": "platform",
                "api_base": "https://api.particle.io/v1",
                "auth_type": "access_token",
                "devices": ["Photon", "Electron", "Boron"],
                "protocols": ["HTTP", "TCP", "UDP"],
                "categories": ["microcontrollers", "gateways"]
            },
            "adafruit": {
                "name": "Adafruit IO",
                "type": "platform",
                "api_base": "https://io.adafruit.com/api/v2",
                "auth_type": "api_key",
                "services": ["Data Feeds", "Dashboards", "Triggers"],
                "protocols": ["HTTP", "MQTT"],
                "categories": ["sensors", "displays", "cloud_services"]
            }
        }
    
    async def authenticate_supplier(self, supplier_id: str, credentials: Dict[str, str]) -> Dict[str, Any]:
        """Authenticate with a supplier's API"""
        
        if supplier_id not in self.supported_suppliers:
            return {"error": f"Supplier {supplier_id} not supported"}
        
        supplier = self.supported_suppliers[supplier_id]
        
        try:
            # Simulate authentication based on auth type
            auth_type = supplier["auth_type"]
            
            if auth_type == "api_key":
                # Validate API key format
                api_key = credentials.get("api_key", "")
                if len(api_key) < 10:
                    return {"error": "Invalid API key format"}
                
                # Simulate API call
                await asyncio.sleep(1)
                
                return {
                    "success": True,
                    "supplier": supplier["name"],
                    "user_info": {
                        "username": "demo_user",
                        "email": "user@example.com",
                        "plan": "free"
                    },
                    "available_devices": supplier.get("devices", []),
                    "available_services": supplier.get("services", [])
                }
            
            elif auth_type == "oauth2":
                # Simulate OAuth2 flow
                client_id = credentials.get("client_id", "")
                client_secret = credentials.get("client_secret", "")
                
                if not client_id or not client_secret:
                    return {"error": "Client ID and Secret required"}
                
                await asyncio.sleep(2)
                
                return {
                    "success": True,
                    "supplier": supplier["name"],
                    "access_token": "demo_access_token_123",
                    "refresh_token": "demo_refresh_token_456",
                    "expires_in": 3600,
                    "user_info": {
                        "username": "oauth_user",
                        "email": "oauth@example.com"
                    }
                }
            
            elif auth_type == "access_token":
                # Validate access token
                access_token = credentials.get("access_token", "")
                if len(access_token) < 15:
                    return {"error": "Invalid access token"}
                
                await asyncio.sleep(1)
                
                return {
                    "success": True,
                    "supplier": supplier["name"],
                    "token_info": {
                        "valid": True,
                        "scope": "read write",
                        "expires_at": "2024-12-31T23:59:59Z"
                    }
                }
            
            else:
                return {"error": f"Authentication type {auth_type} not implemented"}
                
        except Exception as e:
            return {"error": f"Authentication failed: {str(e)}"}
    
    async def get_supplier_devices(self, supplier_id: str, auth_token: str) -> List[HardwareDevice]:
        """Get available devices from supplier"""
        
        if supplier_id not in self.supported_suppliers:
            return []
        
        supplier = self.supported_suppliers[supplier_id]
        
        # Simulate device discovery
        await asyncio.sleep(1)
        
        devices = []
        
        if supplier_id == "arduino":
            devices = [
                HardwareDevice(
                    id="arduino_uno_001",
                    name="Arduino Uno R3",
                    category=HardwareCategory.MICROCONTROLLERS,
                    manufacturer="Arduino",
                    model="Uno R3",
                    description="Microcontroller board based on the ATmega328P",
                    communication_protocols=["Serial", "I2C", "SPI"],
                    data_formats=["JSON", "CSV", "Binary"],
                    capabilities=[
                        "14 digital I/O pins",
                        "6 analog inputs",
                        "USB connectivity",
                        "32KB flash memory"
                    ],
                    connection_info={
                        "usb_port": "/dev/ttyUSB0",
                        "baud_rate": 9600,
                        "data_bits": 8
                    },
                    sdk_available=True,
                    sample_code="""
#include <WiFi.h>
#include <ArduinoJson.h>

void setup() {
  Serial.begin(9600);
  // Initialize sensors
}

void loop() {
  // Read sensor data
  float temperature = analogRead(A0) * 0.1;
  float humidity = analogRead(A1) * 0.1;
  
  // Send data
  StaticJsonDocument<200> doc;
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;
  doc["timestamp"] = millis();
  
  serializeJson(doc, Serial);
  Serial.println();
  
  delay(5000);
}
"""
                )
            ]
        
        elif supplier_id == "particle":
            devices = [
                HardwareDevice(
                    id="particle_photon_001",
                    name="Particle Photon",
                    category=HardwareCategory.MICROCONTROLLERS,
                    manufacturer="Particle",
                    model="Photon",
                    description="Wi-Fi enabled development board",
                    communication_protocols=["HTTP", "TCP", "UDP", "Particle Cloud"],
                    data_formats=["JSON", "String"],
                    capabilities=[
                        "Wi-Fi connectivity",
                        "Cloud integration",
                        "18 digital I/O pins",
                        "8 analog inputs"
                    ],
                    connection_info={
                        "device_id": "photon_device_123",
                        "access_token": "your_access_token",
                        "cloud_url": "https://api.particle.io/v1/devices"
                    },
                    sdk_available=True,
                    sample_code="""
// Particle Photon code
void setup() {
    // Register cloud functions
    Particle.function("setLED", setLEDState);
    Particle.variable("temperature", temperature);
    
    pinMode(D7, OUTPUT);
}

void loop() {
    // Read temperature sensor
    temperature = analogRead(A0) * 0.1;
    
    // Publish data to cloud
    String data = String::format("{"temp": %.2f}", temperature);
    Particle.publish("sensor/data", data, PRIVATE);
    
    delay(30000); // Publish every 30 seconds
}

int setLEDState(String command) {
    if (command == "on") {
        digitalWrite(D7, HIGH);
        return 1;
    } else if (command == "off") {
        digitalWrite(D7, LOW);
        return 0;
    }
    return -1;
}
"""
                )
            ]
        
        return devices

class CodeGenerator:
    """Generates integration code for various platforms and languages"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict[str, str]]:
        """Load code templates for different languages and platforms"""
        return {
            "python": {
                "rest_api": """
import requests
import json
from typing import Dict, Any, Optional

class {class_name}:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({{'Authorization': f'Bearer {{api_key}}'}})
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        '''Make GET request to API endpoint'''
        url = f'{{self.base_url}}{{endpoint}}'
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        '''Make POST request to API endpoint'''
        url = f'{{self.base_url}}{{endpoint}}'
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
{methods}

# Usage example:
# client = {class_name}('{base_url}', 'your_api_key')
# result = client.get_data()
""",
                "iot_device": """
import asyncio
import json
import aiohttp
from datetime import datetime
from typing import Dict, Any, Optional

class {class_name}:
    def __init__(self, device_id: str, api_endpoint: str, auth_token: Optional[str] = None):
        self.device_id = device_id
        self.api_endpoint = api_endpoint
        self.auth_token = auth_token
        self.is_connected = False
    
    async def connect(self) -> bool:
        '''Connect to IoT device'''
        try:
            headers = {{'Content-Type': 'application/json'}}
            if self.auth_token:
                headers['Authorization'] = f'Bearer {{self.auth_token}}'
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f'{{self.api_endpoint}}/connect',
                    json={{'device_id': self.device_id}},
                    headers=headers
                ) as response:
                    if response.status == 200:
                        self.is_connected = True
                        return True
            return False
        except Exception as e:
            print(f'Connection failed: {{e}}')
            return False
    
    async def get_sensor_data(self) -> Dict[str, Any]:
        '''Get current sensor data'''
        if not self.is_connected:
            raise Exception('Device not connected')
        
        headers = {{'Authorization': f'Bearer {{self.auth_token}}'}}
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{{self.api_endpoint}}/data/{{self.device_id}}',
                headers=headers
            ) as response:
                return await response.json()
    
    async def send_command(self, command: str, parameters: Dict[str, Any] = None) -> bool:
        '''Send command to device'''
        if not self.is_connected:
            raise Exception('Device not connected')
        
        payload = {{
            'command': command,
            'device_id': self.device_id,
            'parameters': parameters or {{}},
            'timestamp': datetime.now().isoformat()
        }}
        
        headers = {{
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {{self.auth_token}}'
        }}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{{self.api_endpoint}}/command',
                json=payload,
                headers=headers
            ) as response:
                return response.status == 200

# Usage example:
# device = {class_name}('device_123', 'https://api.example.com/v1', 'your_token')
# await device.connect()
# data = await device.get_sensor_data()
""",
                "mqtt": """
import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Callable, Optional
import paho.mqtt.client as mqtt

class {class_name}:
    def __init__(self, broker_host: str, broker_port: int = 1883, 
                 client_id: Optional[str] = None, username: Optional[str] = None, 
                 password: Optional[str] = None):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client_id = client_id or f'client_{{int(datetime.now().timestamp())}}'
        self.username = username
        self.password = password
        
        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.client.on_disconnect = self._on_disconnect
        
        self.message_handlers = {{}}
        self.is_connected = False
        
        if username and password:
            self.client.username_pw_set(username, password)
    
    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.is_connected = True
            print(f'Connected to MQTT broker {{self.broker_host}}:{{self.broker_port}}')
        else:
            print(f'Failed to connect to MQTT broker: {{rc}}')
    
    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode('utf-8')
        
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            data = payload
        
        # Call registered handlers
        for pattern, handler in self.message_handlers.items():
            if pattern in topic:
                handler(topic, data)
    
    def _on_disconnect(self, client, userdata, rc):
        self.is_connected = False
        print('Disconnected from MQTT broker')
    
    async def connect(self) -> bool:
        '''Connect to MQTT broker'''
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            
            # Wait for connection
            await asyncio.sleep(1)
            return self.is_connected
        except Exception as e:
            print(f'Connection failed: {{e}}')
            return False
    
    def subscribe(self, topic: str, handler: Callable[[str, Any], None]):
        '''Subscribe to a topic with message handler'''
        self.client.subscribe(topic)
        self.message_handlers[topic] = handler
        print(f'Subscribed to topic: {{topic}}')
    
    def publish(self, topic: str, data: Any, qos: int = 0) -> bool:
        '''Publish data to a topic'''
        if not self.is_connected:
            return False
        
        if isinstance(data, dict):
            payload = json.dumps(data)
        else:
            payload = str(data)
        
        result = self.client.publish(topic, payload, qos)
        return result.rc == mqtt.MQTT_ERR_SUCCESS
    
    def disconnect(self):
        '''Disconnect from MQTT broker'''
        self.client.loop_stop()
        self.client.disconnect()

# Usage example:
# mqtt_client = {class_name}('mqtt.example.com', 1883, username='user', password='pass')
# await mqtt_client.connect()
# mqtt_client.subscribe('sensors/+/data', lambda topic, data: print(f'{{topic}}: {{data}}'))
# mqtt_client.publish('sensors/temp/data', {{'temperature': 25.5, 'timestamp': datetime.now().isoformat()}})
"""
            },
            "javascript": {
                "rest_api": """
class {class_name} {{
    constructor(baseUrl, apiKey = null) {{
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.apiKey = apiKey;
    }}
    
    async makeRequest(endpoint, options = {{}}) {{
        const url = `${{this.baseUrl}}${{endpoint}}`;
        const headers = {{
            'Content-Type': 'application/json',
            ...options.headers
        }};
        
        if (this.apiKey) {{
            headers['Authorization'] = `Bearer ${{this.apiKey}}`;
        }}
        
        const response = await fetch(url, {{
            ...options,
            headers
        }});
        
        if (!response.ok) {{
            throw new Error(`HTTP error! status: ${{response.status}}`);
        }}
        
        return await response.json();
    }}
    
    async get(endpoint, params = null) {{
        const url = new URL(`${{this.baseUrl}}${{endpoint}}`);
        if (params) {{
            Object.keys(params).forEach(key => 
                url.searchParams.append(key, params[key])
            );
        }}
        
        return await this.makeRequest(url.pathname + url.search, {{
            method: 'GET'
        }});
    }}
    
    async post(endpoint, data) {{
        return await this.makeRequest(endpoint, {{
            method: 'POST',
            body: JSON.stringify(data)
        }});
    }}
{methods}
}}

// Usage example:
// const client = new {class_name}('{base_url}', 'your_api_key');
// const result = await client.getData();
""",
                "iot_device": """
class {class_name} {{
    constructor(deviceId, apiEndpoint, authToken = null) {{
        this.deviceId = deviceId;
        this.apiEndpoint = apiEndpoint;
        this.authToken = authToken;
        this.isConnected = false;
    }}
    
    async connect() {{
        try {{
            const headers = {{'Content-Type': 'application/json'}};
            if (this.authToken) {{
                headers['Authorization'] = `Bearer ${{this.authToken}}`;
            }}
            
            const response = await fetch(`${{this.apiEndpoint}}/connect`, {{
                method: 'POST',
                headers: headers,
                body: JSON.stringify({{device_id: this.deviceId}})
            }});
            
            if (response.ok) {{
                this.isConnected = true;
                return true;
            }}
            return false;
        }} catch (error) {{
            console.error('Connection failed:', error);
            return false;
        }}
    }}
    
    async getSensorData() {{
        if (!this.isConnected) {{
            throw new Error('Device not connected');
        }}
        
        const response = await fetch(
            `${{this.apiEndpoint}}/data/${{this.deviceId}}`,
            {{
                headers: {{
                    'Authorization': `Bearer ${{this.authToken}}`
                }}
            }}
        );
        
        return await response.json();
    }}
    
    async sendCommand(command, parameters = {{}}) {{
        if (!this.isConnected) {{
            throw new Error('Device not connected');
        }}
        
        const payload = {{
            command: command,
            device_id: this.deviceId,
            parameters: parameters,
            timestamp: new Date().toISOString()
        }};
        
        const response = await fetch(`${{this.apiEndpoint}}/command`, {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${{this.authToken}}`
            }},
            body: JSON.stringify(payload)
        }});
        
        return response.ok;
    }}
}}

// Usage example:
// const device = new {class_name}('device_123', 'https://api.example.com/v1', 'your_token');
// await device.connect();
// const data = await device.getSensorData();
"""
            }
        }
    
    def generate_integration_code(
        self,
        integration: Integration,
        language: str = "python",
        include_examples: bool = True
    ) -> Dict[str, str]:
        """Generate integration code for the specified language"""
        
        generated_code = {}
        
        # Generate API client code
        if integration.endpoints:
            api_code = self._generate_api_client(integration, language)
            generated_code[f"api_client.{self._get_file_extension(language)}"] = api_code
        
        # Generate device interface code
        if integration.devices:
            device_code = self._generate_device_interface(integration, language)
            generated_code[f"device_interface.{self._get_file_extension(language)}"] = device_code
        
        # Generate configuration file
        config = self._generate_config(integration)
        generated_code["config.json"] = json.dumps(config, indent=2)
        
        # Generate example usage
        if include_examples:
            example_code = self._generate_examples(integration, language)
            generated_code[f"examples.{self._get_file_extension(language)}"] = example_code
        
        # Generate README
        readme = self._generate_readme(integration)
        generated_code["README.md"] = readme
        
        return generated_code
    
    def _generate_api_client(self, integration: Integration, language: str) -> str:
        """Generate API client code"""
        
        template = self.templates.get(language, {}).get("rest_api", "")
        if not template:
            return f"# {language} API client template not available"
        
        class_name = f"{integration.name.replace(' ', '').replace('-', '_')}Client"
        base_url = integration.endpoints[0].url if integration.endpoints else "https://api.example.com"
        
        # Generate methods for each endpoint
        methods = []
        for endpoint in integration.endpoints:
            method_name = endpoint.name.replace(' ', '_').replace('-', '_').lower()
            
            if endpoint.method == "GET":
                methods.append(f"""
    def {method_name}(self, **kwargs) -> Dict[str, Any]:
        '''
        {endpoint.description}
        '''
        return self.get('{endpoint.url}', params=kwargs)""")
            
            elif endpoint.method == "POST":
                methods.append(f"""
    def {method_name}(self, data: Dict[str, Any]) -> Dict[str, Any]:
        '''
        {endpoint.description}
        '''
        return self.post('{endpoint.url}', data)""")
        
        methods_code = "\n".join(methods)
        
        return template.format(
            class_name=class_name,
            base_url=base_url,
            methods=methods_code
        )
    
    def _generate_device_interface(self, integration: Integration, language: str) -> str:
        """Generate device interface code"""
        
        if integration.type == IntegrationType.MQTT:
            template = self.templates.get(language, {}).get("mqtt", "")
        else:
            template = self.templates.get(language, {}).get("iot_device", "")
        
        if not template:
            return f"# {language} device interface template not available"
        
        class_name = f"{integration.name.replace(' ', '').replace('-', '_')}Device"
        
        return template.format(class_name=class_name)
    
    def _generate_config(self, integration: Integration) -> Dict[str, Any]:
        """Generate configuration object"""
        
        config = {
            "integration": {
                "name": integration.name,
                "type": integration.type.value,
                "version": "1.0.0",
                "created_at": integration.created_at.isoformat()
            },
            "endpoints": [],
            "devices": [],
            "authentication": {},
            "settings": integration.configuration
        }
        
        # Add endpoint configurations
        for endpoint in integration.endpoints:
            config["endpoints"].append({
                "id": endpoint.id,
                "name": endpoint.name,
                "url": endpoint.url,
                "method": endpoint.method,
                "description": endpoint.description,
                "authentication": endpoint.authentication
            })
        
        # Add device configurations
        for device in integration.devices:
            config["devices"].append({
                "id": device.id,
                "name": device.name,
                "category": device.category.value,
                "manufacturer": device.manufacturer,
                "model": device.model,
                "protocols": device.communication_protocols,
                "connection": device.connection_info
            })
        
        return config
    
    def _generate_examples(self, integration: Integration, language: str) -> str:
        """Generate example usage code"""
        
        if language == "python":
            return f"""
# Example usage for {integration.name}
import asyncio
from api_client import {integration.name.replace(' ', '').replace('-', '_')}Client
from device_interface import {integration.name.replace(' ', '').replace('-', '_')}Device

async def main():
    # Initialize API client
    client = {integration.name.replace(' ', '').replace('-', '_')}Client(
        'https://api.example.com',
        'your_api_key'
    )
    
    # Initialize device
    device = {integration.name.replace(' ', '').replace('-', '_')}Device(
        'device_123',
        'https://api.example.com/v1',
        'your_auth_token'
    )
    
    # Connect to device
    connected = await device.connect()
    if not connected:
        print('Failed to connect to device')
        return
    
    # Get sensor data
    try:
        data = await device.get_sensor_data()
        print(f'Sensor data: {{data}}')
    except Exception as e:
        print(f'Error getting sensor data: {{e}}')
    
    # Send commands
    try:
        success = await device.send_command('get_status')
        print(f'Command sent successfully: {{success}}')
    except Exception as e:
        print(f'Error sending command: {{e}}')

if __name__ == "__main__":
    asyncio.run(main())
"""
        
        elif language == "javascript":
            return f"""
// Example usage for {integration.name}
import {{ {integration.name.replace(' ', '').replace('-', '_')}Client }} from './api_client.js';
import {{ {integration.name.replace(' ', '').replace('-', '_')}Device }} from './device_interface.js';

async function main() {{
    // Initialize API client
    const client = new {integration.name.replace(' ', '').replace('-', '_')}Client(
        'https://api.example.com',
        'your_api_key'
    );
    
    // Initialize device
    const device = new {integration.name.replace(' ', '').replace('-', '_')}Device(
        'device_123',
        'https://api.example.com/v1',
        'your_auth_token'
    );
    
    // Connect to device
    const connected = await device.connect();
    if (!connected) {{
        console.log('Failed to connect to device');
        return;
    }}
    
    // Get sensor data
    try {{
        const data = await device.getSensorData();
        console.log('Sensor data:', data);
    }} catch (error) {{
        console.error('Error getting sensor data:', error);
    }}
    
    // Send commands
    try {{
        const success = await device.sendCommand('get_status');
        console.log('Command sent successfully:', success);
    }} catch (error) {{
        console.error('Error sending command:', error);
    }}
}}

main().catch(console.error);
"""
        
        return f"# Example code for {language} not available"
    
    def _generate_readme(self, integration: Integration) -> str:
        """Generate README documentation"""
        
        return f"""# {integration.name} Integration

{integration.description}

## Overview

This integration provides seamless connectivity to {integration.name} via the MASS Framework auto-generated code.

## Features

### Devices
{chr(10).join([f"- {device.name} ({device.manufacturer} {device.model})" for device in integration.devices])}

### API Endpoints
{chr(10).join([f"- {endpoint.method} {endpoint.url}: {endpoint.description}" for endpoint in integration.endpoints])}

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure your credentials:
   ```python
   # Update config.json with your API keys and device IDs
   ```

3. Run the example:
   ```python
   python examples.py
   ```

## Configuration

Edit `config.json` to configure:
- API endpoints and authentication
- Device connection parameters
- Custom settings

## Code Structure

- `api_client.py`: REST API client
- `device_interface.py`: Device communication interface
- `examples.py`: Usage examples
- `config.json`: Configuration file

## Support

For support and questions:
- Check the device/API documentation
- Review the generated code comments
- Contact the MASS Framework support team

## Generated by MASS Framework

This integration was automatically generated by the MASS Framework IoT/API Integration System.
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    def _get_file_extension(self, language: str) -> str:
        """Get file extension for language"""
        extensions = {
            "python": "py",
            "javascript": "js",
            "java": "java",
            "csharp": "cs",
            "go": "go",
            "rust": "rs"
        }
        return extensions.get(language, "txt")

class HardwareIntegrationSystem:
    """Main system for hardware/API integrations"""
    
    def __init__(self):
        self.parser = DocumentParser()
        self.supplier = SupplierIntegration()
        self.code_generator = CodeGenerator()
        self.integrations = {}
    
    async def create_integration_from_document(
        self,
        document_path: str,
        document_type: DocumentType,
        integration_name: str,
        description: str = ""
    ) -> Integration:
        """Create integration from uploaded document"""
        
        # Parse the document
        parsed_data = await self.parser.parse_document(document_path, document_type)
        
        if "error" in parsed_data:
            raise ValueError(f"Failed to parse document: {parsed_data['error']}")
        
        # Create integration based on parsed data
        integration_id = f"integration_{int(datetime.now().timestamp())}"
        
        # Determine integration type
        integration_type = self._determine_integration_type(parsed_data)
        
        # Create devices and endpoints
        devices = self._create_devices_from_data(parsed_data)
        endpoints = self._create_endpoints_from_data(parsed_data)
        
        # Generate configuration
        config = {
            "source_document": document_path,
            "document_type": document_type.value,
            "auto_generated": True,
            "parse_timestamp": datetime.now().isoformat()
        }
        
        # Create integration
        integration = Integration(
            id=integration_id,
            name=integration_name,
            type=integration_type,
            description=description or f"Auto-generated integration from {document_type.value}",
            devices=devices,
            endpoints=endpoints,
            configuration=config,
            generated_code={},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Generate code
        integration.generated_code = self.code_generator.generate_integration_code(integration)
        
        # Store integration
        self.integrations[integration_id] = integration
        
        return integration
    
    async def create_integration_from_supplier(
        self,
        supplier_id: str,
        credentials: Dict[str, str],
        integration_name: str,
        selected_devices: List[str] = None
    ) -> Integration:
        """Create integration from supplier login"""
        
        # Authenticate with supplier
        auth_result = await self.supplier.authenticate_supplier(supplier_id, credentials)
        
        if not auth_result.get("success"):
            raise ValueError(f"Authentication failed: {auth_result.get('error')}")
        
        # Get available devices
        auth_token = auth_result.get("access_token", "authenticated")
        devices = await self.supplier.get_supplier_devices(supplier_id, auth_token)
        
        # Filter selected devices
        if selected_devices:
            devices = [d for d in devices if d.id in selected_devices]
        
        # Create integration
        integration_id = f"supplier_{supplier_id}_{int(datetime.now().timestamp())}"
        
        integration = Integration(
            id=integration_id,
            name=integration_name,
            type=IntegrationType.IOT_DEVICE,
            description=f"Integration with {supplier_id} devices",
            devices=devices,
            endpoints=[],
            configuration={
                "supplier_id": supplier_id,
                "authentication": auth_result,
                "auto_generated": True
            },
            generated_code={},
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Generate code
        integration.generated_code = self.code_generator.generate_integration_code(integration)
        
        # Store integration
        self.integrations[integration_id] = integration
        
        return integration
    
    def _determine_integration_type(self, parsed_data: Dict[str, Any]) -> IntegrationType:
        """Determine integration type from parsed data"""
        
        data_type = parsed_data.get("type", "").lower()
        
        if data_type in ["rest_api", "api"]:
            return IntegrationType.REST_API
        elif data_type in ["iot_device", "device", "hardware"]:
            return IntegrationType.IOT_DEVICE
        elif data_type in ["mqtt"]:
            return IntegrationType.MQTT
        elif data_type in ["websocket"]:
            return IntegrationType.WEBSOCKET
        elif data_type in ["database", "db"]:
            return IntegrationType.DATABASE
        else:
            return IntegrationType.REST_API  # Default
    
    def _create_devices_from_data(self, parsed_data: Dict[str, Any]) -> List[HardwareDevice]:
        """Create device objects from parsed data"""
        
        devices = []
        
        if parsed_data.get("type") == "iot_device":
            device = HardwareDevice(
                id=f"device_{int(datetime.now().timestamp())}",
                name=parsed_data.get("name", "Unknown Device"),
                category=getattr(HardwareCategory, parsed_data.get("category", "sensors").upper(), HardwareCategory.SENSORS),
                manufacturer=parsed_data.get("manufacturer", "Unknown"),
                model=parsed_data.get("model", "Unknown"),
                description=parsed_data.get("description", ""),
                communication_protocols=parsed_data.get("protocols", []),
                data_formats=parsed_data.get("data_formats", ["JSON"]),
                capabilities=parsed_data.get("capabilities", []),
                connection_info=parsed_data.get("connection", {}),
                sample_code=parsed_data.get("sample_code")
            )
            devices.append(device)
        
        return devices
    
    def _create_endpoints_from_data(self, parsed_data: Dict[str, Any]) -> List[APIEndpoint]:
        """Create endpoint objects from parsed data"""
        
        endpoints = []
        
        if "endpoints" in parsed_data:
            for i, endpoint_data in enumerate(parsed_data["endpoints"]):
                endpoint = APIEndpoint(
                    id=f"endpoint_{i}_{int(datetime.now().timestamp())}",
                    name=endpoint_data.get("name", endpoint_data.get("summary", f"Endpoint {i+1}")),
                    url=endpoint_data.get("url", endpoint_data.get("path", "/")),
                    method=endpoint_data.get("method", "GET").upper(),
                    description=endpoint_data.get("description", ""),
                    parameters=endpoint_data.get("parameters", []),
                    headers=endpoint_data.get("headers", {}),
                    request_body=endpoint_data.get("request_body", endpoint_data.get("body")),
                    response_schema=endpoint_data.get("responses", {}),
                    authentication=endpoint_data.get("security", {})
                )
                endpoints.append(endpoint)
        
        return endpoints
    
    def get_integration(self, integration_id: str) -> Optional[Integration]:
        """Get integration by ID"""
        return self.integrations.get(integration_id)
    
    def list_integrations(self) -> List[Integration]:
        """List all integrations"""
        return list(self.integrations.values())
    
    def get_supported_suppliers(self) -> Dict[str, Dict[str, Any]]:
        """Get list of supported suppliers"""
        return self.supplier.supported_suppliers
    
    def get_supported_document_types(self) -> List[Dict[str, str]]:
        """Get list of supported document types"""
        return [
            {"type": doc_type.value, "name": doc_type.value.replace("_", " ").title()}
            for doc_type in DocumentType
        ]

# Demo function
async def demo_hardware_integration():
    """Demo of hardware integration system"""
    
    system = HardwareIntegrationSystem()
    
    print("🔧 MASS Framework Hardware/API Integration Demo")
    print("=" * 60)
    
    # Show supported document types
    print("\n📄 Supported Document Types:")
    doc_types = system.get_supported_document_types()
    for doc_type in doc_types:
        print(f"• {doc_type['name']}")
    
    # Show supported suppliers
    print("\n🏭 Supported Suppliers:")
    suppliers = system.get_supported_suppliers()
    for supplier_id, supplier_info in suppliers.items():
        print(f"• {supplier_info['name']} ({supplier_info['type']})")
        print(f"  Auth: {supplier_info['auth_type']}")
        if 'devices' in supplier_info:
            print(f"  Devices: {', '.join(supplier_info['devices'][:3])}...")
        print()
    
    # Demo: Create integration from supplier
    print("🔌 Creating Integration from Supplier (Arduino)...")
    try:
        integration = await system.create_integration_from_supplier(
            supplier_id="arduino",
            credentials={"api_key": "demo_arduino_key_123"},
            integration_name="My Arduino Sensors"
        )
        
        print(f"✅ Integration created: {integration.name}")
        print(f"   ID: {integration.id}")
        print(f"   Type: {integration.type.value}")
        print(f"   Devices: {len(integration.devices)}")
        
        # Show generated code files
        print("\n📁 Generated Code Files:")
        for filename, code_preview in integration.generated_code.items():
            print(f"• {filename} ({len(code_preview)} characters)")
        
        # Show device details
        if integration.devices:
            device = integration.devices[0]
            print(f"\n🔧 Device Details: {device.name}")
            print(f"   Manufacturer: {device.manufacturer}")
            print(f"   Model: {device.model}")
            print(f"   Protocols: {', '.join(device.communication_protocols)}")
            print(f"   Capabilities: {len(device.capabilities)} features")
        
    except Exception as e:
        print(f"❌ Error creating integration: {e}")
    
    # Demo: Parse API documentation
    print("\n📖 Parsing API Documentation...")
    
    # Create a sample API spec file
    sample_api_spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "IoT Sensor API",
            "version": "1.0.0",
            "description": "API for managing IoT sensors"
        },
        "servers": [
            {"url": "https://api.iot-sensors.com/v1"}
        ],
        "paths": {
            "/sensors": {
                "get": {
                    "summary": "List all sensors",
                    "description": "Get a list of all connected sensors",
                    "responses": {
                        "200": {
                            "description": "List of sensors",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Sensor"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/sensors/{sensorId}/data": {
                "get": {
                    "summary": "Get sensor data",
                    "description": "Get current data from a specific sensor",
                    "parameters": [
                        {
                            "name": "sensorId",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Sensor data",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/SensorData"}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    
    # Save sample spec to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_api_spec, f, indent=2)
        temp_spec_file = f.name
    
    try:
        api_integration = await system.create_integration_from_document(
            document_path=temp_spec_file,
            document_type=DocumentType.API_SPEC,
            integration_name="IoT Sensor API",
            description="API integration for IoT sensor management"
        )
        
        print(f"✅ API Integration created: {api_integration.name}")
        print(f"   Endpoints: {len(api_integration.endpoints)}")
        
        # Show endpoints
        print("\n🌐 API Endpoints:")
        for endpoint in api_integration.endpoints:
            print(f"• {endpoint.method} {endpoint.url}")
            print(f"  {endpoint.description}")
        
        # Show generated code preview
        if "api_client.py" in api_integration.generated_code:
            code_preview = api_integration.generated_code["api_client.py"][:300]
            print(f"\n💻 Generated Python Code Preview:")
            print("```python")
            print(code_preview + "...")
            print("```")
        
    except Exception as e:
        print(f"❌ Error creating API integration: {e}")
    
    finally:
        # Clean up temp file
        try:
            os.unlink(temp_spec_file)
        except:
            pass
    
    # Show integration summary
    print(f"\n📊 Integration Summary:")
    integrations = system.list_integrations()
    print(f"Total integrations created: {len(integrations)}")
    
    for integration in integrations:
        print(f"\n• {integration.name}")
        print(f"  Type: {integration.type.value}")
        print(f"  Devices: {len(integration.devices)}")
        print(f"  Endpoints: {len(integration.endpoints)}")
        print(f"  Generated files: {len(integration.generated_code)}")
    
    return {
        "system": system,
        "integrations": integrations,
        "sample_spec": sample_api_spec
    }

if __name__ == "__main__":
    # Run demo
    import asyncio
    asyncio.run(demo_hardware_integration())
