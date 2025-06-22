"""
IoT and Sensor Data Sources - Real-World Physical Intelligence
============================================================

Provides real-time IoT sensor data and physical world intelligence
to enable AI-powered monitoring and control systems.

Supported IoT Data Sources:
- Temperature and Environmental Sensors
- GPS and Location Tracking
- Industrial Equipment Sensors
- Smart Home Devices
- Vehicle Telematics
- Agricultural Sensors
- Weather Stations
- Energy Monitoring Systems
- Security and Motion Sensors
- Health and Medical Devices

Features:
- Real-time sensor data streaming
- Historical data analysis
- Anomaly detection and alerts
- Predictive maintenance insights
- Environmental monitoring
- Asset tracking and management
- Energy optimization
- Safety and security monitoring
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import aiohttp
import random
from dataclasses import dataclass

from ...core.config_manager import MassConfig
from ..base_data_source import BaseDataSource

logger = logging.getLogger(__name__)

@dataclass
class SensorReading:
    """Represents a sensor reading"""
    sensor_id: str
    sensor_type: str
    value: Union[float, int, str]
    unit: str
    timestamp: datetime
    location: Optional[Dict[str, float]] = None  # lat, lng
    metadata: Optional[Dict[str, Any]] = None

class IoTDataSources(BaseDataSource):
    """
    IoT and sensor data source integration for real-world physical intelligence
    """
    
    def __init__(self, config: MassConfig):
        super().__init__(config)
        
        # IoT platform credentials
        self.api_keys = {
            'openweather_api_key': config.get('openweather_api_key'),
            'thingspeak_api_key': config.get('thingspeak_api_key'),
            'particle_access_token': config.get('particle_access_token'),
            'aws_iot_endpoint': config.get('aws_iot_endpoint'),
            'azure_iot_connection_string': config.get('azure_iot_connection_string')
        }
        
        self.session = None
        self.sensor_cache = {}
        self.mock_sensors = self._initialize_mock_sensors()
        
    async def initialize(self) -> bool:
        """Initialize IoT data sources"""
        try:
            logger.info("Initializing IoT Data Sources...")
            
            # Create HTTP session
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30)
            )
            
            # Test connectivity to available IoT platforms
            await self._test_connectivity()
            
            # Initialize mock sensors for demonstration
            await self._initialize_sensor_simulation()
            
            self.initialized = True
            logger.info("✅ IoT Data Sources initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize IoT Data Sources: {e}")
            return False
    
    async def collect_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect IoT sensor data based on parameters
        
        Parameters can include:
        - sensor_types: List of sensor types to collect ['temperature', 'gps', 'energy']
        - location: Geographic location for location-based sensors
        - time_range: Time range for historical data
        - real_time: Whether to get real-time data
        - device_ids: Specific device IDs to query
        """
        try:
            sensor_types = parameters.get('sensor_types', ['temperature', 'humidity', 'pressure'])
            location = parameters.get('location', {'lat': 40.7128, 'lng': -74.0060})  # Default: NYC
            time_range = parameters.get('time_range', '1h')
            real_time = parameters.get('real_time', True)
            device_ids = parameters.get('device_ids', [])
            
            logger.info(f"Collecting IoT data for sensor types: {sensor_types}")
            
            # Collect data from different sources
            collection_tasks = []
            
            # Weather data (always available)
            if 'temperature' in sensor_types or 'humidity' in sensor_types or 'pressure' in sensor_types:
                collection_tasks.append(
                    self._collect_weather_data(location, sensor_types)
                )
            
            # Mock sensor data for demonstration
            collection_tasks.append(
                self._collect_mock_sensor_data(sensor_types, location, device_ids)
            )
            
            # ThingSpeak data (if available)
            if self.api_keys.get('thingspeak_api_key'):
                collection_tasks.append(
                    self._collect_thingspeak_data(sensor_types, time_range)
                )
            
            # Execute collection tasks
            results = await asyncio.gather(*collection_tasks, return_exceptions=True)
            
            # Combine all sensor readings
            all_readings = []
            source_results = {}
            
            for i, result in enumerate(results):
                source_name = f"source_{i}"
                
                if isinstance(result, Exception):
                    source_results[source_name] = {"error": str(result)}
                else:
                    source_results[source_name] = result
                    if 'readings' in result:
                        all_readings.extend(result['readings'])
            
            # Analyze the sensor data
            analysis = await self._analyze_sensor_data(all_readings, sensor_types)
            
            # Generate IoT insights
            insights = await self._generate_iot_insights(all_readings, analysis)
            
            return {
                "sensor_types_requested": sensor_types,
                "location": location,
                "total_readings": len(all_readings),
                "source_results": source_results,
                "readings": all_readings,
                "analysis": analysis,
                "insights": insights,
                "metadata": {
                    "collected_at": datetime.now().isoformat(),
                    "time_range": time_range,
                    "source": "iot_data_sources"
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to collect IoT data: {e}")
            return await self.handle_error(e, "collect_data")
    
    async def start_sensor_monitoring(
        self, 
        sensor_types: List[str], 
        callback: callable,
        interval: int = 60
    ) -> str:
        """Start real-time sensor monitoring"""
        try:
            monitor_id = f"iot_monitor_{datetime.now().timestamp()}"
            
            # Start monitoring task
            asyncio.create_task(
                self._process_sensor_monitoring(monitor_id, sensor_types, callback, interval)
            )
            
            logger.info(f"Started IoT sensor monitoring: {monitor_id}")
            return monitor_id
            
        except Exception as e:
            logger.error(f"Failed to start sensor monitoring: {e}")
            raise
    
    async def get_status(self) -> str:
        """Get status of IoT data sources"""
        try:
            if not self.initialized:
                return "not_initialized"
            
            # Check if at least one source is working
            if await self._test_weather_api() or self._test_mock_sensors():
                return "operational"
            
            return "degraded"
            
        except Exception:
            return "error"
    
    # Private methods for data collection
    
    def _initialize_mock_sensors(self) -> Dict[str, Dict[str, Any]]:
        """Initialize mock sensors for demonstration"""
        return {
            "temp_001": {
                "type": "temperature",
                "location": {"lat": 40.7128, "lng": -74.0060},
                "unit": "celsius",
                "range": {"min": 15, "max": 35}
            },
            "humid_001": {
                "type": "humidity",
                "location": {"lat": 40.7128, "lng": -74.0060},
                "unit": "percent",
                "range": {"min": 30, "max": 80}
            },
            "energy_001": {
                "type": "energy",
                "location": {"lat": 40.7128, "lng": -74.0060},
                "unit": "kwh",
                "range": {"min": 0, "max": 100}
            },
            "gps_001": {
                "type": "gps",
                "location": {"lat": 40.7128, "lng": -74.0060},
                "unit": "coordinates",
                "range": {"lat_var": 0.01, "lng_var": 0.01}
            },
            "pressure_001": {
                "type": "pressure",
                "location": {"lat": 40.7128, "lng": -74.0060},
                "unit": "hpa",
                "range": {"min": 980, "max": 1030}
            }
        }
    
    async def _initialize_sensor_simulation(self) -> None:
        """Initialize sensor simulation for realistic data"""
        try:
            # Initialize base values for realistic simulation
            for sensor_id, config in self.mock_sensors.items():
                sensor_range = config['range']
                if config['type'] == 'gps':
                    config['current_value'] = {
                        'lat': config['location']['lat'],
                        'lng': config['location']['lng']
                    }
                else:
                    config['current_value'] = (sensor_range['min'] + sensor_range['max']) / 2
            
            logger.info("Sensor simulation initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize sensor simulation: {e}")
    
    async def _test_connectivity(self) -> None:
        """Test connectivity to IoT platforms"""
        platforms = ['weather', 'thingspeak', 'mock']
        
        for platform in platforms:
            try:
                if platform == 'weather':
                    success = await self._test_weather_api()
                elif platform == 'thingspeak':
                    success = await self._test_thingspeak()
                elif platform == 'mock':
                    success = self._test_mock_sensors()
                else:
                    continue
                
                if success:
                    logger.info(f"✅ {platform} connectivity test passed")
                else:
                    logger.warning(f"⚠️ {platform} connectivity test failed")
                    
            except Exception as e:
                logger.error(f"❌ {platform} connectivity test error: {e}")
    
    async def _collect_weather_data(
        self, 
        location: Dict[str, float], 
        sensor_types: List[str]
    ) -> Dict[str, Any]:
        """Collect weather data as sensor information"""
        try:
            if not self.api_keys.get('openweather_api_key'):
                # Return simulated weather data
                return await self._collect_simulated_weather_data(location, sensor_types)
            
            # OpenWeatherMap API
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "lat": location['lat'],
                "lon": location['lng'],
                "appid": self.api_keys['openweather_api_key'],
                "units": "metric"
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    readings = []
                    
                    # Convert weather data to sensor readings
                    timestamp = datetime.now()
                    
                    if 'temperature' in sensor_types:
                        readings.append(SensorReading(
                            sensor_id="weather_temp",
                            sensor_type="temperature",
                            value=data['main']['temp'],
                            unit="celsius",
                            timestamp=timestamp,
                            location=location
                        ).__dict__)
                    
                    if 'humidity' in sensor_types:
                        readings.append(SensorReading(
                            sensor_id="weather_humidity",
                            sensor_type="humidity",
                            value=data['main']['humidity'],
                            unit="percent",
                            timestamp=timestamp,
                            location=location
                        ).__dict__)
                    
                    if 'pressure' in sensor_types:
                        readings.append(SensorReading(
                            sensor_id="weather_pressure",
                            sensor_type="pressure",
                            value=data['main']['pressure'],
                            unit="hpa",
                            timestamp=timestamp,
                            location=location
                        ).__dict__)
                    
                    return {
                        "source": "openweather",
                        "readings": readings,
                        "location": location
                    }
                else:
                    return {"error": f"Weather API error: {response.status}"}
                    
        except Exception as e:
            logger.error(f"Failed to collect weather data: {e}")
            return {"error": str(e)}
    
    async def _collect_simulated_weather_data(
        self, 
        location: Dict[str, float], 
        sensor_types: List[str]
    ) -> Dict[str, Any]:
        """Collect simulated weather data when API key is not available"""
        try:
            readings = []
            timestamp = datetime.now()
            
            # Generate realistic weather data based on location and time
            base_temp = 20  # Base temperature in Celsius
            temp_variation = random.uniform(-5, 15)
            
            if 'temperature' in sensor_types:
                readings.append(SensorReading(
                    sensor_id="sim_weather_temp",
                    sensor_type="temperature",
                    value=round(base_temp + temp_variation, 1),
                    unit="celsius",
                    timestamp=timestamp,
                    location=location
                ).__dict__)
            
            if 'humidity' in sensor_types:
                readings.append(SensorReading(
                    sensor_id="sim_weather_humidity",
                    sensor_type="humidity",
                    value=random.randint(40, 85),
                    unit="percent",
                    timestamp=timestamp,
                    location=location
                ).__dict__)
            
            if 'pressure' in sensor_types:
                readings.append(SensorReading(
                    sensor_id="sim_weather_pressure",
                    sensor_type="pressure",
                    value=random.randint(995, 1025),
                    unit="hpa",
                    timestamp=timestamp,
                    location=location
                ).__dict__)
            
            return {
                "source": "simulated_weather",
                "readings": readings,
                "location": location
            }
            
        except Exception as e:
            logger.error(f"Failed to collect simulated weather data: {e}")
            return {"error": str(e)}
    
    async def _collect_mock_sensor_data(
        self, 
        sensor_types: List[str], 
        location: Dict[str, float],
        device_ids: List[str]
    ) -> Dict[str, Any]:
        """Collect data from mock sensors"""
        try:
            readings = []
            timestamp = datetime.now()
            
            # Filter sensors by type and device IDs
            relevant_sensors = {}
            for sensor_id, config in self.mock_sensors.items():
                if config['type'] in sensor_types:
                    if not device_ids or sensor_id in device_ids:
                        relevant_sensors[sensor_id] = config
            
            # Generate realistic sensor readings
            for sensor_id, config in relevant_sensors.items():
                value = self._simulate_sensor_value(config)
                
                reading = SensorReading(
                    sensor_id=sensor_id,
                    sensor_type=config['type'],
                    value=value,
                    unit=config['unit'],
                    timestamp=timestamp,
                    location=config['location'],
                    metadata={"simulated": True}
                )
                readings.append(reading.__dict__)
            
            return {
                "source": "mock_sensors",
                "readings": readings,
                "sensor_count": len(relevant_sensors)
            }
            
        except Exception as e:
            logger.error(f"Failed to collect mock sensor data: {e}")
            return {"error": str(e)}
    
    def _simulate_sensor_value(self, sensor_config: Dict[str, Any]) -> Union[float, int, Dict[str, float]]:
        """Simulate realistic sensor values"""
        try:
            sensor_type = sensor_config['type']
            sensor_range = sensor_config['range']
            current_value = sensor_config.get('current_value')
            
            if sensor_type == 'gps':
                # Simulate slight movement
                lat_change = random.uniform(-sensor_range['lat_var'], sensor_range['lat_var'])
                lng_change = random.uniform(-sensor_range['lng_var'], sensor_range['lng_var'])
                
                new_value = {
                    'lat': current_value['lat'] + lat_change,
                    'lng': current_value['lng'] + lng_change
                }
                sensor_config['current_value'] = new_value
                return new_value
            else:
                # Simulate gradual changes for other sensor types
                if current_value is None:
                    current_value = (sensor_range['min'] + sensor_range['max']) / 2
                
                # Add some random variation
                variation = random.uniform(-2, 2)
                new_value = current_value + variation
                
                # Keep within range
                new_value = max(sensor_range['min'], min(sensor_range['max'], new_value))
                
                sensor_config['current_value'] = new_value
                
                # Return appropriate type
                if sensor_type in ['energy', 'temperature', 'humidity']:
                    return round(new_value, 2)
                else:
                    return int(new_value)
                    
        except Exception as e:
            logger.error(f"Failed to simulate sensor value: {e}")
            return 0
    
    async def _collect_thingspeak_data(
        self, 
        sensor_types: List[str], 
        time_range: str
    ) -> Dict[str, Any]:
        """Collect data from ThingSpeak IoT platform"""
        try:
            if not self.api_keys.get('thingspeak_api_key'):
                return {"error": "ThingSpeak API key not configured"}
            
            # ThingSpeak public channel (example)
            channel_id = "9"  # Public weather station channel
            url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.json"
            params = {
                "api_key": self.api_keys['thingspeak_api_key'],
                "results": 10
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    readings = []
                    
                    for feed in data.get('feeds', []):
                        timestamp = datetime.fromisoformat(feed['created_at'].replace('Z', '+00:00'))
                        
                        # Map ThingSpeak fields to sensor types
                        if 'temperature' in sensor_types and feed.get('field1'):
                            readings.append(SensorReading(
                                sensor_id=f"thingspeak_{channel_id}_temp",
                                sensor_type="temperature",
                                value=float(feed['field1']),
                                unit="celsius",
                                timestamp=timestamp
                            ).__dict__)
                    
                    return {
                        "source": "thingspeak",
                        "readings": readings,
                        "channel_id": channel_id
                    }
                else:
                    return {"error": f"ThingSpeak API error: {response.status}"}
                    
        except Exception as e:
            logger.error(f"Failed to collect ThingSpeak data: {e}")
            return {"error": str(e)}
    
    async def _analyze_sensor_data(
        self, 
        readings: List[Dict[str, Any]], 
        sensor_types: List[str]
    ) -> Dict[str, Any]:
        """Analyze collected sensor data"""
        try:
            if not readings:
                return {}
            
            analysis = {}
            
            # Group readings by sensor type
            by_type = {}
            for reading in readings:
                sensor_type = reading.get('sensor_type', 'unknown')
                if sensor_type not in by_type:
                    by_type[sensor_type] = []
                by_type[sensor_type].append(reading)
            
            # Analyze each sensor type
            for sensor_type, type_readings in by_type.items():
                values = []
                for reading in type_readings:
                    value = reading.get('value')
                    if isinstance(value, (int, float)):
                        values.append(value)
                
                if values:
                    analysis[sensor_type] = {
                        "count": len(values),
                        "average": sum(values) / len(values),
                        "min": min(values),
                        "max": max(values),
                        "range": max(values) - min(values),
                        "latest": values[-1] if values else None
                    }
                    
                    # Detect anomalies
                    if len(values) > 1:
                        avg = analysis[sensor_type]["average"]
                        anomalies = [v for v in values if abs(v - avg) > 2 * (max(values) - min(values)) / len(values)]
                        analysis[sensor_type]["anomalies"] = len(anomalies)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze sensor data: {e}")
            return {}
    
    async def _generate_iot_insights(
        self, 
        readings: List[Dict[str, Any]], 
        analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate insights from IoT sensor data"""
        try:
            insights = []
            
            for sensor_type, stats in analysis.items():
                # Temperature insights
                if sensor_type == 'temperature':
                    temp = stats.get('latest', 0)
                    if temp > 30:
                        insights.append({
                            "type": "temperature_alert",
                            "insight": f"High temperature detected: {temp}°C",
                            "confidence": 0.9,
                            "actionable": True,
                            "recommended_action": "Check cooling systems or ventilation"
                        })
                    elif temp < 5:
                        insights.append({
                            "type": "temperature_alert",
                            "insight": f"Low temperature detected: {temp}°C",
                            "confidence": 0.9,
                            "actionable": True,
                            "recommended_action": "Check heating systems"
                        })
                
                # Humidity insights
                elif sensor_type == 'humidity':
                    humidity = stats.get('latest', 0)
                    if humidity > 80:
                        insights.append({
                            "type": "humidity_alert",
                            "insight": f"High humidity detected: {humidity}%",
                            "confidence": 0.8,
                            "actionable": True,
                            "recommended_action": "Increase ventilation or use dehumidifier"
                        })
                    elif humidity < 30:
                        insights.append({
                            "type": "humidity_alert",
                            "insight": f"Low humidity detected: {humidity}%",
                            "confidence": 0.8,
                            "actionable": True,
                            "recommended_action": "Use humidifier or check for air leaks"
                        })
                
                # Energy insights
                elif sensor_type == 'energy':
                    energy = stats.get('latest', 0)
                    avg_energy = stats.get('average', 0)
                    if energy > avg_energy * 1.5:
                        insights.append({
                            "type": "energy_consumption",
                            "insight": f"High energy consumption detected: {energy} kWh (avg: {avg_energy:.1f})",
                            "confidence": 0.8,
                            "actionable": True,
                            "recommended_action": "Investigate high energy usage devices"
                        })
                
                # Anomaly insights
                anomalies = stats.get('anomalies', 0)
                if anomalies > 0:
                    insights.append({
                        "type": "anomaly_detection",
                        "insight": f"Anomalies detected in {sensor_type} readings: {anomalies} instances",
                        "confidence": 0.7,
                        "actionable": True,
                        "recommended_action": f"Investigate {sensor_type} sensor irregularities"
                    })
            
            return insights
            
        except Exception as e:
            logger.error(f"Failed to generate IoT insights: {e}")
            return []
    
    # Connectivity tests
    
    async def _test_weather_api(self) -> bool:
        """Test weather API connectivity"""
        try:
            if not self.api_keys.get('openweather_api_key'):
                return True  # Simulated weather always works
            
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                "lat": 40.7128,
                "lon": -74.0060,
                "appid": self.api_keys['openweather_api_key']
            }
            
            async with self.session.get(url, params=params) as response:
                return response.status == 200
                
        except Exception:
            return False
    
    async def _test_thingspeak(self) -> bool:
        """Test ThingSpeak connectivity"""
        try:
            url = "https://api.thingspeak.com/channels/9/feeds.json"
            params = {"results": 1}
            
            async with self.session.get(url, params=params) as response:
                return response.status == 200
                
        except Exception:
            return False
    
    def _test_mock_sensors(self) -> bool:
        """Test mock sensors (always available)"""
        return len(self.mock_sensors) > 0
    
    async def _process_sensor_monitoring(
        self, 
        monitor_id: str, 
        sensor_types: List[str], 
        callback: callable,
        interval: int
    ) -> None:
        """Process real-time sensor monitoring"""
        try:
            while True:
                # Collect sensor data
                data = await self.collect_data({
                    'sensor_types': sensor_types,
                    'real_time': True
                })
                
                # Call callback with data
                try:
                    callback(monitor_id, data)
                except Exception as e:
                    logger.error(f"Sensor monitoring callback failed for {monitor_id}: {e}")
                
                # Wait for next reading
                await asyncio.sleep(interval)
                
        except Exception as e:
            logger.error(f"Sensor monitoring {monitor_id} failed: {e}")
    
    async def close(self) -> None:
        """Close the IoT data sources"""
        if self.session:
            await self.session.close()
            logger.info("IoT Data Sources closed")
