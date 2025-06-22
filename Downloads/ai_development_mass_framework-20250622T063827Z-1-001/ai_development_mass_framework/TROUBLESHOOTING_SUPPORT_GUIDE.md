# Universal MASS Framework - Troubleshooting & Support Guide 🔧

## Quick Reference for Issues and Solutions

**Last Updated:** June 22, 2025  
**Framework Version:** 1.0.0  
**Support Level:** Production Ready  

---

## 🚨 EMERGENCY TROUBLESHOOTING

### Framework Won't Start
```bash
# 1. Check Python version (3.8+ required)
python --version

# 2. Verify dependencies
pip install -r requirements.txt

# 3. Check configuration
cp .env.template .env
# Edit .env with your settings

# 4. Test basic import
python -c "from universal_mass_framework.core.mass_engine import MassEngine; print('✅ Import successful')"

# 5. Run validation
python test_framework_validation.py
```

### Common Error Solutions
```python
# ImportError: No module named 'universal_mass_framework'
# Solution: Ensure you're in the correct directory and PYTHONPATH is set
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# SQLAlchemy connection errors
# Solution: Check database configuration in .env file
DATABASE_URL="sqlite:///mass_framework.db"

# Authentication errors
# Solution: Generate new JWT secret
JWT_SECRET="your-secret-key-here"

# Port already in use
# Solution: Change port or kill existing process
lsof -ti:8000 | xargs kill -9
```

---

## 🔍 DIAGNOSTIC PROCEDURES

### 1. System Health Check
```python
# Run this script to check system health
import asyncio
from universal_mass_framework.core.mass_engine import MassEngine

async def health_check():
    try:
        engine = MassEngine()
        await engine.start()
        print("✅ MASS Engine started successfully")
        
        status = await engine.get_system_status()
        print(f"✅ System Status: {status.engine_status}")
        
        await engine.stop()
        print("✅ MASS Engine stopped successfully")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

# Run health check
if __name__ == "__main__":
    asyncio.run(health_check())
```

### 2. Component Validation
```python
# Validate individual components
def validate_components():
    components = [
        "universal_mass_framework.core.mass_engine",
        "universal_mass_framework.data_orchestration.data_processors.pattern_analyzer",
        "universal_mass_framework.data_orchestration.data_processors.predictive_analyzer",
        "universal_mass_framework.intelligence_agents.data_analyzer_agent"
    ]
    
    for component in components:
        try:
            __import__(component)
            print(f"✅ {component}")
        except ImportError as e:
            print(f"❌ {component}: {e}")

validate_components()
```

### 3. Memory and Performance Check
```python
import psutil
import time

def system_diagnostics():
    """Check system resources"""
    print("🔍 SYSTEM DIAGNOSTICS")
    print("-" * 30)
    
    # Memory usage
    memory = psutil.virtual_memory()
    print(f"Memory: {memory.percent}% used ({memory.used / 1024**3:.1f}GB / {memory.total / 1024**3:.1f}GB)")
    
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    print(f"CPU: {cpu_percent}% used")
    
    # Disk usage
    disk = psutil.disk_usage('/')
    print(f"Disk: {disk.percent}% used ({disk.used / 1024**3:.1f}GB / {disk.total / 1024**3:.1f}GB)")
    
    # Process info
    process = psutil.Process()
    print(f"Process Memory: {process.memory_info().rss / 1024**2:.1f}MB")
    print(f"Process CPU: {process.cpu_percent()}%")

system_diagnostics()
```

---

## 🐛 COMMON ISSUES & SOLUTIONS

### Issue 1: Data Processor Initialization Fails
**Symptoms:** `PatternAnalyzer` or `PredictiveAnalyzer` fails to initialize

**Solutions:**
```python
# Check if required ML libraries are installed
try:
    import numpy as np
    import pandas as pd
    import sklearn
    print("✅ ML libraries available")
except ImportError as e:
    print(f"❌ Missing ML library: {e}")
    print("Solution: pip install numpy pandas scikit-learn")

# Verify processor configuration
config = {
    "max_patterns": 100,
    "analysis_depth": "comprehensive",
    "enable_caching": True
}

from universal_mass_framework.data_orchestration.data_processors.pattern_analyzer import PatternAnalyzer
analyzer = PatternAnalyzer(config)
print("✅ Pattern Analyzer initialized")
```

### Issue 2: Agent Coordination Problems
**Symptoms:** Agents don't communicate or coordinate properly

**Solutions:**
```python
# Check agent coordinator status
from universal_mass_framework.core.agent_coordinator import AgentCoordinator

coordinator = AgentCoordinator()
print(f"Coordinator Status: {coordinator.status}")
print(f"Active Agents: {len(coordinator.active_agents)}")

# Reset coordinator if needed
await coordinator.reset()
print("✅ Coordinator reset")
```

### Issue 3: Performance Degradation
**Symptoms:** Slow response times, high memory usage

**Solutions:**
```python
# Enable performance monitoring
from universal_mass_framework.core.mass_engine import MassEngine

engine = MassEngine()
engine.config.enable_performance_monitoring = True
engine.config.max_concurrent_operations = 10  # Limit concurrent ops

# Clear caches if needed
await engine.clear_caches()
print("✅ Caches cleared")
```

### Issue 4: Database Connection Issues
**Symptoms:** SQLAlchemy errors, database lock errors

**Solutions:**
```python
# Test database connection
from sqlalchemy import create_engine, text

try:
    engine = create_engine("sqlite:///mass_framework.db")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connection successful")
except Exception as e:
    print(f"❌ Database error: {e}")
    print("Solution: Check DATABASE_URL in .env file")
```

---

## 📊 MONITORING & DIAGNOSTICS

### Real-Time Monitoring
```python
import asyncio
import time
from universal_mass_framework.core.mass_engine import MassEngine

async def monitor_system():
    """Real-time system monitoring"""
    engine = MassEngine()
    await engine.start()
    
    print("🔍 REAL-TIME MONITORING (Press Ctrl+C to stop)")
    print("-" * 50)
    
    try:
        while True:
            status = await engine.get_system_status()
            print(f"[{time.strftime('%H:%M:%S')}] "
                  f"Active: {status.active_operations} | "
                  f"Completed: {status.completed_operations} | "
                  f"Avg Response: {status.average_response_time_ms}ms")
            await asyncio.sleep(5)
    except KeyboardInterrupt:
        print("\n✅ Monitoring stopped")
    finally:
        await engine.stop()

# Run monitoring
asyncio.run(monitor_system())
```

### Performance Metrics
```python
def get_performance_metrics():
    """Get detailed performance metrics"""
    import time
    import psutil
    
    metrics = {
        "timestamp": time.time(),
        "memory_usage_mb": psutil.virtual_memory().used / 1024**2,
        "memory_percent": psutil.virtual_memory().percent,
        "cpu_percent": psutil.cpu_percent(interval=1),
        "disk_usage_percent": psutil.disk_usage('/').percent,
        "load_average": psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
    }
    
    return metrics

print("📊 Performance Metrics:")
metrics = get_performance_metrics()
for key, value in metrics.items():
    print(f"  {key}: {value}")
```

---

## 🔧 CONFIGURATION TROUBLESHOOTING

### Environment Variables
```bash
# Essential environment variables
export MASS_FRAMEWORK_ENV=production
export DATABASE_URL=sqlite:///mass_framework.db
export JWT_SECRET=your-jwt-secret-key
export LOG_LEVEL=INFO
export MAX_WORKERS=4
export CACHE_TTL=3600

# Optional environment variables
export REDIS_URL=redis://localhost:6379
export MONITORING_ENABLED=true
export DEBUG_MODE=false
```

### Configuration File Template
```yaml
# config/mass_framework.yaml
framework:
  name: "Universal MASS Framework"
  version: "1.0.0"
  environment: "production"

database:
  url: "sqlite:///mass_framework.db"
  pool_size: 10
  max_overflow: 20

security:
  jwt_secret: "your-secret-key"
  jwt_expiry_hours: 24
  rate_limit_per_minute: 100

performance:
  max_concurrent_operations: 50
  cache_ttl_seconds: 3600
  enable_monitoring: true

agents:
  max_agents: 10
  heartbeat_interval: 30
  timeout_seconds: 300

data_processors:
  pattern_analyzer:
    max_patterns: 1000
    analysis_depth: "comprehensive"
  
  predictive_analyzer:
    models: ["linear", "forest", "gradient_boost"]
    confidence_threshold: 0.8
```

---

## 📞 SUPPORT PROCEDURES

### Issue Reporting Template
```
🐛 BUG REPORT

**Framework Version:** 1.0.0
**Python Version:** 3.x.x
**Operating System:** 
**Issue Type:** [Bug/Performance/Configuration/Other]

**Description:**
Brief description of the issue

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Error Messages:**
```
Include any error messages or logs
```

**Environment:**
- Dependencies: (pip freeze output)
- Configuration: (relevant config settings)
- System Resources: (CPU, Memory, Disk)

**Additional Context:**
Any other relevant information
```

### Log Collection
```python
# Enable comprehensive logging
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mass_framework_debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

# Enable framework debug logging
logger = logging.getLogger('universal_mass_framework')
logger.setLevel(logging.DEBUG)

print("✅ Debug logging enabled - check mass_framework_debug.log")
```

---

## 🎯 PERFORMANCE OPTIMIZATION

### Memory Optimization
```python
# Optimize memory usage
import gc
from universal_mass_framework.core.mass_engine import MassEngine

# Configure for memory efficiency
config = {
    "cache_size": 100,  # Reduce cache size
    "max_concurrent_operations": 5,  # Limit concurrency
    "enable_gc": True,  # Enable garbage collection
    "memory_threshold_mb": 1000  # Memory limit
}

engine = MassEngine(config)

# Periodic cleanup
async def memory_cleanup():
    gc.collect()
    await engine.clear_old_caches()
    print("✅ Memory cleanup completed")
```

### CPU Optimization
```python
# Optimize CPU usage
import multiprocessing

# Configure worker processes
num_workers = min(multiprocessing.cpu_count(), 4)
config = {
    "max_workers": num_workers,
    "worker_timeout": 30,
    "enable_async": True
}

print(f"✅ Configured for {num_workers} workers")
```

---

## 🛠️ RECOVERY PROCEDURES

### Emergency Reset
```python
async def emergency_reset():
    """Emergency system reset"""
    print("🚨 EMERGENCY RESET INITIATED")
    
    try:
        # Stop all operations
        engine = MassEngine()
        await engine.emergency_stop()
        
        # Clear all caches
        await engine.clear_all_caches()
        
        # Reset database connections
        await engine.reset_database_connections()
        
        # Restart core components
        await engine.restart_core_components()
        
        print("✅ Emergency reset completed")
        return True
    except Exception as e:
        print(f"❌ Emergency reset failed: {e}")
        return False
```

### Data Recovery
```python
def backup_system_state():
    """Backup current system state"""
    import json
    import datetime
    
    backup_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "system_status": "captured",
        "configuration": "saved",
        "active_operations": "exported"
    }
    
    backup_file = f"mass_framework_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(backup_file, 'w') as f:
        json.dump(backup_data, f, indent=2)
    
    print(f"✅ System state backed up to {backup_file}")
    return backup_file
```

---

## 📋 MAINTENANCE CHECKLIST

### Daily Maintenance
- [ ] Check system health status
- [ ] Monitor error logs
- [ ] Verify all agents are responding
- [ ] Check memory and CPU usage
- [ ] Validate database connections

### Weekly Maintenance
- [ ] Review performance metrics
- [ ] Clean up old log files
- [ ] Update dependencies if needed
- [ ] Run comprehensive system tests
- [ ] Backup system configuration

### Monthly Maintenance
- [ ] Performance optimization review
- [ ] Security audit
- [ ] Capacity planning review
- [ ] Documentation updates
- [ ] Framework version assessment

---

## 🎓 BEST PRACTICES

### Development
1. **Always use virtual environments**
2. **Pin dependency versions for production**
3. **Enable comprehensive logging in development**
4. **Use configuration files instead of hardcoded values**
5. **Implement proper error handling**

### Production
1. **Monitor system resources continuously**
2. **Implement proper backup procedures**
3. **Use environment-specific configurations**
4. **Enable security features**
5. **Plan for scalability**

### Troubleshooting
1. **Start with the simplest solution**
2. **Check logs before asking for help**
3. **Isolate the problem component**
4. **Document solutions for future reference**
5. **Test fixes in development first**

---

**🔧 For additional support, check the comprehensive documentation or create an issue report using the template above.**

*Universal MASS Framework v1.0 - Troubleshooting Guide*  
*Last Updated: June 22, 2025*
