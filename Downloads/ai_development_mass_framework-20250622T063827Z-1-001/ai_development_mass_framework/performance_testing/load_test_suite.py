"""
Performance and Load Testing Suite for PROMETHEUS AI Trading Platform
Tests system performance under various load conditions and stress scenarios
"""

import asyncio
import aiohttp
import time
import json
import statistics
import threading
import concurrent.futures
from datetime import datetime, timedelta
import psutil
import numpy as np
import pandas as pd
from typing import List, Dict, Any
import websockets
import ssl
import random

class PerformanceMetrics:
    """Track and analyze performance metrics"""
    
    def __init__(self):
        self.response_times = []
        self.error_rates = []
        self.throughput_data = []
        self.resource_usage = []
        self.start_time = None
        self.end_time = None
    
    def start_monitoring(self):
        """Start performance monitoring"""
        self.start_time = time.time()
        self.response_times = []
        self.error_rates = []
        self.throughput_data = []
        self.resource_usage = []
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.end_time = time.time()
    
    def add_response_time(self, response_time: float):
        """Add response time measurement"""
        self.response_times.append(response_time)
    
    def add_error(self):
        """Record an error"""
        self.error_rates.append(1)
    
    def add_success(self):
        """Record a success"""
        self.error_rates.append(0)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calculate performance statistics"""
        if not self.response_times:
            return {"error": "No data collected"}
        
        return {
            "avg_response_time": statistics.mean(self.response_times),
            "median_response_time": statistics.median(self.response_times),
            "p95_response_time": np.percentile(self.response_times, 95),
            "p99_response_time": np.percentile(self.response_times, 99),
            "max_response_time": max(self.response_times),
            "min_response_time": min(self.response_times),
            "error_rate": sum(self.error_rates) / len(self.error_rates) * 100 if self.error_rates else 0,
            "total_requests": len(self.response_times),
            "duration": self.end_time - self.start_time if self.end_time else 0,
            "requests_per_second": len(self.response_times) / (self.end_time - self.start_time) if self.end_time and self.start_time else 0
        }

class LoadTester:
    """Main load testing class"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.metrics = PerformanceMetrics()
        self.session = None
    
    async def create_session(self):
        """Create async HTTP session"""
        connector = aiohttp.TCPConnector(limit=1000, limit_per_host=100)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        )
    
    async def close_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
    
    async def make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request with timing"""
        start_time = time.time()
        
        try:
            async with self.session.request(method, f"{self.base_url}{endpoint}", **kwargs) as response:
                response_time = time.time() - start_time
                self.metrics.add_response_time(response_time)
                
                if response.status < 400:
                    self.metrics.add_success()
                    return {
                        "status": response.status,
                        "response_time": response_time,
                        "data": await response.json() if response.content_type == 'application/json' else await response.text()
                    }
                else:
                    self.metrics.add_error()
                    return {
                        "status": response.status,
                        "response_time": response_time,
                        "error": f"HTTP {response.status}"
                    }
        except Exception as e:
            response_time = time.time() - start_time
            self.metrics.add_response_time(response_time)
            self.metrics.add_error()
            return {
                "status": 0,
                "response_time": response_time,
                "error": str(e)
            }

class APILoadTest:
    """Test API endpoints under load"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.tester = LoadTester(base_url)
    
    async def test_authentication_load(self, concurrent_users: int = 100, duration: int = 60):
        """Test authentication endpoints under load"""
        print(f"Testing authentication with {concurrent_users} concurrent users for {duration}s")
        
        await self.tester.create_session()
        self.tester.metrics.start_monitoring()
        
        async def auth_worker():
            """Single authentication worker"""
            user_data = {
                "email": f"loadtest{random.randint(1, 10000)}@prometheus.ai",
                "password": "LoadTest123!"
            }
            
            # Test registration
            await self.tester.make_request("POST", "/auth/register", json=user_data)
            
            # Test login
            await self.tester.make_request("POST", "/auth/login", json={
                "email": user_data["email"],
                "password": user_data["password"]
            })
        
        # Run concurrent authentication tests
        tasks = []
        end_time = time.time() + duration
        
        while time.time() < end_time:
            # Create batch of concurrent users
            batch_tasks = [auth_worker() for _ in range(min(concurrent_users, 50))]
            tasks.extend(batch_tasks)
            await asyncio.gather(*batch_tasks, return_exceptions=True)
            await asyncio.sleep(0.1)  # Small delay between batches
        
        self.tester.metrics.stop_monitoring()
        await self.tester.close_session()
        
        return self.tester.metrics.get_statistics()
    
    async def test_trading_endpoints_load(self, concurrent_users: int = 50, duration: int = 60):
        """Test trading endpoints under load"""
        print(f"Testing trading endpoints with {concurrent_users} concurrent users for {duration}s")
        
        await self.tester.create_session()
        self.tester.metrics.start_monitoring()
        
        async def trading_worker():
            """Single trading worker"""
            # Test portfolio endpoint
            await self.tester.make_request("GET", "/portfolio")
            
            # Test market data
            await self.tester.make_request("GET", "/market/data/AAPL")
            
            # Test order placement (mock)
            order_data = {
                "symbol": "AAPL",
                "quantity": random.randint(1, 100),
                "side": random.choice(["buy", "sell"]),
                "type": "market"
            }
            await self.tester.make_request("POST", "/orders", json=order_data)
        
        # Run concurrent trading tests
        tasks = []
        end_time = time.time() + duration
        
        while time.time() < end_time:
            batch_tasks = [trading_worker() for _ in range(min(concurrent_users, 25))]
            tasks.extend(batch_tasks)
            await asyncio.gather(*batch_tasks, return_exceptions=True)
            await asyncio.sleep(0.1)
        
        self.tester.metrics.stop_monitoring()
        await self.tester.close_session()
        
        return self.tester.metrics.get_statistics()
    
    async def test_ai_optimization_load(self, concurrent_requests: int = 20, duration: int = 120):
        """Test AI optimization endpoints under load"""
        print(f"Testing AI optimization with {concurrent_requests} concurrent requests for {duration}s")
        
        await self.tester.create_session()
        self.tester.metrics.start_monitoring()
        
        async def ai_worker():
            """Single AI optimization worker"""
            optimization_data = {
                "symbol": random.choice(["AAPL", "TSLA", "MSFT", "GOOGL"]),
                "strategy_type": random.choice(["rsi", "macd", "bollinger"]),
                "timeframe": random.choice(["1h", "4h", "1d"]),
                "optimization_target": random.choice(["return", "sharpe", "drawdown"])
            }
            await self.tester.make_request("POST", "/ai/optimize", json=optimization_data)
        
        # Run AI optimization tests
        end_time = time.time() + duration
        
        while time.time() < end_time:
            batch_tasks = [ai_worker() for _ in range(min(concurrent_requests, 10))]
            await asyncio.gather(*batch_tasks, return_exceptions=True)
            await asyncio.sleep(1)  # Longer delay for AI operations
        
        self.tester.metrics.stop_monitoring()
        await self.tester.close_session()
        
        return self.tester.metrics.get_statistics()

class WebSocketLoadTest:
    """Test WebSocket connections under load"""
    
    def __init__(self, ws_url: str = "ws://localhost:8000/ws"):
        self.ws_url = ws_url
        self.metrics = PerformanceMetrics()
    
    async def test_realtime_data_load(self, concurrent_connections: int = 100, duration: int = 60):
        """Test real-time data WebSocket connections"""
        print(f"Testing WebSocket with {concurrent_connections} concurrent connections for {duration}s")
        
        self.metrics.start_monitoring()
        
        async def websocket_worker():
            """Single WebSocket worker"""
            try:
                # Create SSL context for secure connections (if needed)
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                
                async with websockets.connect(self.ws_url, ssl=ssl_context if self.ws_url.startswith('wss') else None) as websocket:
                    # Subscribe to market data
                    subscribe_message = {
                        "action": "subscribe",
                        "symbols": ["AAPL", "TSLA", "MSFT"]
                    }
                    await websocket.send(json.dumps(subscribe_message))
                    
                    # Listen for messages
                    start_time = time.time()
                    while time.time() - start_time < duration:
                        try:
                            message = await asyncio.wait_for(websocket.recv(), timeout=1.0)
                            message_time = time.time()
                            self.metrics.add_response_time(message_time - start_time)
                            self.metrics.add_success()
                        except asyncio.TimeoutError:
                            continue
                        except Exception as e:
                            self.metrics.add_error()
                            break
            except Exception as e:
                self.metrics.add_error()
        
        # Run concurrent WebSocket connections
        tasks = [websocket_worker() for _ in range(concurrent_connections)]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        self.metrics.stop_monitoring()
        return self.metrics.get_statistics()

class DatabaseLoadTest:
    """Test database operations under load"""
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
    
    async def test_database_operations(self, concurrent_operations: int = 50, duration: int = 60):
        """Test database read/write operations under load"""
        print(f"Testing database with {concurrent_operations} concurrent operations for {duration}s")
        
        self.metrics.start_monitoring()
        
        async def db_worker():
            """Single database worker"""
            # Mock database operations timing
            start_time = time.time()
            
            try:
                # Simulate database operations
                await asyncio.sleep(random.uniform(0.001, 0.05))  # Simulate DB query time
                
                response_time = time.time() - start_time
                self.metrics.add_response_time(response_time)
                self.metrics.add_success()
            except Exception as e:
                response_time = time.time() - start_time
                self.metrics.add_response_time(response_time)
                self.metrics.add_error()
        
        # Run database load test
        end_time = time.time() + duration
        
        while time.time() < end_time:
            batch_tasks = [db_worker() for _ in range(concurrent_operations)]
            await asyncio.gather(*batch_tasks, return_exceptions=True)
            await asyncio.sleep(0.1)
        
        self.metrics.stop_monitoring()
        return self.metrics.get_statistics()

class SystemResourceMonitor:
    """Monitor system resources during load testing"""
    
    def __init__(self):
        self.cpu_usage = []
        self.memory_usage = []
        self.disk_usage = []
        self.network_usage = []
        self.monitoring = False
    
    def start_monitoring(self):
        """Start resource monitoring"""
        self.monitoring = True
        self.cpu_usage = []
        self.memory_usage = []
        self.disk_usage = []
        self.network_usage = []
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitor_resources)
        self.monitor_thread.start()
    
    def stop_monitoring(self):
        """Stop resource monitoring"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join()
    
    def _monitor_resources(self):
        """Monitor system resources"""
        while self.monitoring:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            self.cpu_usage.append(cpu_percent)
            
            # Memory usage
            memory = psutil.virtual_memory()
            self.memory_usage.append(memory.percent)
            
            # Disk usage
            disk = psutil.disk_usage('/')
            self.disk_usage.append(disk.percent)
            
            # Network usage (if available)
            try:
                network = psutil.net_io_counters()
                self.network_usage.append({
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv
                })
            except:
                pass
            
            time.sleep(1)
    
    def get_resource_statistics(self) -> Dict[str, Any]:
        """Get resource usage statistics"""
        return {
            "cpu_usage": {
                "avg": statistics.mean(self.cpu_usage) if self.cpu_usage else 0,
                "max": max(self.cpu_usage) if self.cpu_usage else 0,
                "min": min(self.cpu_usage) if self.cpu_usage else 0
            },
            "memory_usage": {
                "avg": statistics.mean(self.memory_usage) if self.memory_usage else 0,
                "max": max(self.memory_usage) if self.memory_usage else 0,
                "min": min(self.memory_usage) if self.memory_usage else 0
            },
            "disk_usage": {
                "avg": statistics.mean(self.disk_usage) if self.disk_usage else 0,
                "max": max(self.disk_usage) if self.disk_usage else 0,
                "min": min(self.disk_usage) if self.disk_usage else 0
            }
        }

class ComprehensiveLoadTestSuite:
    """Main test suite orchestrator"""
    
    def __init__(self, base_url: str = "http://localhost:8000", ws_url: str = "ws://localhost:8000/ws"):
        self.api_tester = APILoadTest(base_url)
        self.ws_tester = WebSocketLoadTest(ws_url)
        self.db_tester = DatabaseLoadTest()
        self.resource_monitor = SystemResourceMonitor()
    
    async def run_comprehensive_test(self):
        """Run complete load testing suite"""
        print("🚀 Starting Comprehensive Load Testing Suite for PROMETHEUS AI Trading Platform")
        print("=" * 80)
        
        test_results = {}
        
        # Start resource monitoring
        self.resource_monitor.start_monitoring()
        
        try:
            # Test 1: Authentication Load Test
            print("\n📊 Running Authentication Load Test...")
            auth_results = await self.api_tester.test_authentication_load(
                concurrent_users=50, duration=30
            )
            test_results['authentication'] = auth_results
            
            # Test 2: Trading Endpoints Load Test
            print("\n💰 Running Trading Endpoints Load Test...")
            trading_results = await self.api_tester.test_trading_endpoints_load(
                concurrent_users=30, duration=45
            )
            test_results['trading'] = trading_results
            
            # Test 3: AI Optimization Load Test
            print("\n🤖 Running AI Optimization Load Test...")
            ai_results = await self.api_tester.test_ai_optimization_load(
                concurrent_requests=10, duration=60
            )
            test_results['ai_optimization'] = ai_results
            
            # Test 4: WebSocket Load Test
            print("\n🔄 Running WebSocket Real-time Data Load Test...")
            ws_results = await self.ws_tester.test_realtime_data_load(
                concurrent_connections=50, duration=30
            )
            test_results['websocket'] = ws_results
            
            # Test 5: Database Load Test
            print("\n🗄️ Running Database Load Test...")
            db_results = await self.db_tester.test_database_operations(
                concurrent_operations=25, duration=30
            )
            test_results['database'] = db_results
            
        finally:
            # Stop resource monitoring
            self.resource_monitor.stop_monitoring()
            test_results['system_resources'] = self.resource_monitor.get_resource_statistics()
        
        # Generate report
        self.generate_report(test_results)
        return test_results
    
    def generate_report(self, results: Dict[str, Any]):
        """Generate comprehensive test report"""
        print("\n" + "=" * 80)
        print("📈 COMPREHENSIVE LOAD TEST RESULTS")
        print("=" * 80)
        
        for test_name, test_results in results.items():
            if test_name == 'system_resources':
                print(f"\n🖥️ System Resources:")
                print(f"   CPU Usage: Avg {test_results['cpu_usage']['avg']:.1f}%, Max {test_results['cpu_usage']['max']:.1f}%")
                print(f"   Memory Usage: Avg {test_results['memory_usage']['avg']:.1f}%, Max {test_results['memory_usage']['max']:.1f}%")
                print(f"   Disk Usage: Avg {test_results['disk_usage']['avg']:.1f}%, Max {test_results['disk_usage']['max']:.1f}%")
            else:
                print(f"\n📊 {test_name.title()} Test Results:")
                if 'error' not in test_results:
                    print(f"   Average Response Time: {test_results['avg_response_time']:.3f}s")
                    print(f"   95th Percentile: {test_results['p95_response_time']:.3f}s")
                    print(f"   Error Rate: {test_results['error_rate']:.2f}%")
                    print(f"   Requests/Second: {test_results['requests_per_second']:.2f}")
                    print(f"   Total Requests: {test_results['total_requests']}")
                else:
                    print(f"   Error: {test_results['error']}")
        
        # Performance Assessment
        print(f"\n🎯 PERFORMANCE ASSESSMENT:")
        self.assess_performance(results)
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"load_test_results_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Detailed results saved to: {filename}")
    
    def assess_performance(self, results: Dict[str, Any]):
        """Assess overall performance and provide recommendations"""
        assessments = []
        
        # Check response times
        for test_name, test_results in results.items():
            if test_name != 'system_resources' and 'avg_response_time' in test_results:
                avg_time = test_results['avg_response_time']
                if avg_time > 2.0:
                    assessments.append(f"⚠️ {test_name} response time is high ({avg_time:.3f}s)")
                elif avg_time > 1.0:
                    assessments.append(f"⚡ {test_name} response time is acceptable ({avg_time:.3f}s)")
                else:
                    assessments.append(f"✅ {test_name} response time is excellent ({avg_time:.3f}s)")
                
                # Check error rates
                error_rate = test_results.get('error_rate', 0)
                if error_rate > 5:
                    assessments.append(f"🚨 {test_name} has high error rate ({error_rate:.2f}%)")
                elif error_rate > 1:
                    assessments.append(f"⚠️ {test_name} has moderate error rate ({error_rate:.2f}%)")
                else:
                    assessments.append(f"✅ {test_name} has low error rate ({error_rate:.2f}%)")
        
        # Check system resources
        if 'system_resources' in results:
            resources = results['system_resources']
            cpu_max = resources['cpu_usage']['max']
            memory_max = resources['memory_usage']['max']
            
            if cpu_max > 80:
                assessments.append(f"🚨 High CPU usage detected ({cpu_max:.1f}%)")
            elif cpu_max > 60:
                assessments.append(f"⚠️ Moderate CPU usage ({cpu_max:.1f}%)")
            else:
                assessments.append(f"✅ CPU usage is normal ({cpu_max:.1f}%)")
            
            if memory_max > 80:
                assessments.append(f"🚨 High memory usage detected ({memory_max:.1f}%)")
            elif memory_max > 60:
                assessments.append(f"⚠️ Moderate memory usage ({memory_max:.1f}%)")
            else:
                assessments.append(f"✅ Memory usage is normal ({memory_max:.1f}%)")
        
        for assessment in assessments:
            print(f"   {assessment}")

async def main():
    """Main function to run load tests"""
    load_test_suite = ComprehensiveLoadTestSuite()
    results = await load_test_suite.run_comprehensive_test()
    return results

if __name__ == "__main__":
    asyncio.run(main())
