# Universal MASS Framework - Quick Start Guide 🚀

## Overview
The Universal MASS Framework is the "jQuery of AI" - making ANY system exponentially smarter with minimal integration effort.

## Quick Integration (5 Minutes)

### 1. Initialize Framework
```python
from universal_mass_framework.core.mass_engine import MassEngine, OperationType, OperationRequest

# Start the MASS Engine
mass_engine = MassEngine()
await mass_engine.start()
```

### 2. Analyze Patterns in ANY Data
```python
# Pattern Analysis
pattern_request = OperationRequest(
    operation_type=OperationType.PATTERN_ANALYSIS,
    data={
        "data": your_data_here,  # ANY format: list, dict, CSV, JSON
        "context": {"domain": "business", "analysis_type": "comprehensive"}
    }
)
result = await mass_engine.execute_operation(pattern_request)
print(f"Patterns found: {result.result_data['patterns_detected']}")
```

### 3. Generate Predictions
```python
# Predictive Analytics
prediction_request = OperationRequest(
    operation_type=OperationType.PREDICTION,
    data={
        "historical_data": time_series_data,
        "prediction_horizon": 24,  # Predict next 24 periods
        "target_variable": "revenue"
    }
)
result = await mass_engine.execute_operation(prediction_request)
print(f"Prediction: {result.result_data['predicted_values']}")
```

### 4. Detect Anomalies
```python
# Real-time Anomaly Detection
anomaly_request = OperationRequest(
    operation_type=OperationType.ANOMALY_DETECTION,
    data={
        "data": streaming_data,
        "context": {"sensitivity": "high", "alert_threshold": "medium"}
    }
)
result = await mass_engine.execute_operation(anomaly_request)
print(f"Anomalies detected: {result.result_data['anomalies_detected']}")
```

### 5. Generate Business Insights
```python
# AI-Powered Business Intelligence
insight_request = OperationRequest(
    operation_type=OperationType.INSIGHT_GENERATION,
    data={
        "data": business_data,
        "context": {"business_domain": "ecommerce", "goal": "optimization"}
    }
)
result = await mass_engine.execute_operation(insight_request)
print(f"Insights: {result.result_data['business_insights']}")
```

### 6. Analyze Correlations
```python
# Cross-Source Correlation Analysis
correlation_request = OperationRequest(
    operation_type=OperationType.CORRELATION_ANALYSIS,
    data={
        "sources": {
            "sales_data": sales_metrics,
            "user_data": user_behavior,
            "market_data": market_trends
        }
    }
)
result = await mass_engine.execute_operation(correlation_request)
print(f"Correlations found: {result.result_data['correlations_found']}")
```

## Advanced Usage

### Custom Configuration
```python
from universal_mass_framework.core.config_manager import MassConfig

config = MassConfig()
config.set("prediction_models", ["ensemble", "random_forest", "gradient_boosting"])
config.set("anomaly_sensitivity", "high")
config.set("trust_threshold", 0.8)

mass_engine = MassEngine(config)
```

### Real-time Processing
```python
# Stream processing setup
async def process_data_stream(data_stream):
    async for data_point in data_stream:
        # Real-time anomaly detection
        anomaly_request = OperationRequest(
            operation_type=OperationType.ANOMALY_DETECTION,
            data={"data": data_point},
            execution_mode=ExecutionMode.ASYNCHRONOUS
        )
        
        result = await mass_engine.execute_operation(anomaly_request)
        
        if result.result_data.get('anomalies_detected', 0) > 0:
            await send_alert(result.result_data['anomaly_details'])
```

### Multi-Agent Tasks
```python
# Complex multi-agent analysis
multi_agent_request = OperationRequest(
    operation_type=OperationType.MULTI_AGENT_TASK,
    data={
        "task_description": "Comprehensive business intelligence analysis",
        "task_data": {
            "sales_data": sales_data,
            "customer_data": customer_data,
            "market_data": market_data
        },
        "context": {
            "agents_required": ["data_analyzer", "predictive_agent", "pattern_detector"],
            "analysis_depth": "comprehensive"
        }
    }
)
result = await mass_engine.execute_operation(multi_agent_request)
```

## Integration Examples

### E-Commerce Platform
```python
# Sales trend analysis and prediction
sales_analysis = await mass_engine.execute_operation(OperationRequest(
    operation_type=OperationType.PATTERN_ANALYSIS,
    data={"data": daily_sales_data, "context": {"domain": "ecommerce"}}
))

# Customer behavior prediction
customer_prediction = await mass_engine.execute_operation(OperationRequest(
    operation_type=OperationType.PREDICTION,
    data={"historical_data": customer_interactions, "prediction_horizon": 7}
))

# Fraud detection
fraud_detection = await mass_engine.execute_operation(OperationRequest(
    operation_type=OperationType.ANOMALY_DETECTION,
    data={"data": transaction_data, "context": {"sensitivity": "high"}}
))
```

### Financial Services
```python
# Market trend analysis
market_patterns = await mass_engine.execute_operation(OperationRequest(
    operation_type=OperationType.PATTERN_ANALYSIS,
    data={"data": market_data, "context": {"domain": "finance"}}
))

# Risk assessment
risk_prediction = await mass_engine.execute_operation(OperationRequest(
    operation_type=OperationType.PREDICTION,
    data={"historical_data": portfolio_data, "target_variable": "risk_score"}
))
```

### Healthcare Analytics
```python
# Patient outcome prediction
outcome_prediction = await mass_engine.execute_operation(OperationRequest(
    operation_type=OperationType.PREDICTION,
    data={"historical_data": patient_data, "target_variable": "outcome"}
))

# Treatment effectiveness analysis
treatment_insights = await mass_engine.execute_operation(OperationRequest(
    operation_type=OperationType.INSIGHT_GENERATION,
    data={"data": treatment_data, "context": {"domain": "healthcare"}}
))
```

## Performance Optimization

### Batch Processing
```python
# Process multiple requests efficiently
requests = [
    OperationRequest(OperationType.PATTERN_ANALYSIS, {"data": dataset1}),
    OperationRequest(OperationType.PREDICTION, {"historical_data": dataset2}),
    OperationRequest(OperationType.ANOMALY_DETECTION, {"data": dataset3})
]

results = await asyncio.gather(*[
    mass_engine.execute_operation(req) for req in requests
])
```

### Caching and Optimization
```python
# Enable caching for repeated analyses
config.set("enable_caching", True)
config.set("cache_ttl", 3600)  # 1 hour

# Performance monitoring
status = await mass_engine.get_system_status()
print(f"System performance: {status.performance_metrics}")
```

## Error Handling

### Robust Error Management
```python
try:
    result = await mass_engine.execute_operation(request)
    
    if result.status == "success":
        print(f"Analysis completed: {result.result_data}")
    else:
        print(f"Analysis failed: {result.result_data.get('error')}")
        
except Exception as e:
    print(f"System error: {str(e)}")
    # Framework includes automatic retry and fallback mechanisms
```

## Monitoring and Diagnostics

### System Health Check
```python
# Get system status
status = await mass_engine.get_system_status()
print(f"System uptime: {status.uptime}")
print(f"Operations processed: {status.total_operations}")
print(f"Success rate: {status.success_rate}")

# Get performance metrics
metrics = await mass_engine.get_performance_metrics()
print(f"Average response time: {metrics.average_response_time}ms")
print(f"Throughput: {metrics.operations_per_second} ops/sec")
```

## Best Practices

### 1. Data Preparation
- Ensure data quality and consistency
- Provide relevant context for better insights
- Use appropriate data types and formats

### 2. Configuration Optimization
- Tune sensitivity settings based on your domain
- Configure appropriate confidence thresholds
- Enable caching for repeated operations

### 3. Performance Monitoring
- Monitor system performance metrics
- Set up alerts for anomalies and errors
- Regularly review and optimize configurations

### 4. Security and Compliance
- Use enterprise trust framework features
- Implement proper access controls
- Monitor and audit all operations

## Support and Documentation

### Getting Help
- Review comprehensive documentation
- Check error logs for troubleshooting
- Monitor system performance metrics
- Contact support for enterprise assistance

### Additional Resources
- Full API documentation
- Integration examples
- Performance tuning guides
- Security best practices

---

**🚀 Ready to transform your system with AI intelligence? Start with these simple examples and scale up to enterprise-wide intelligence enhancement!**
