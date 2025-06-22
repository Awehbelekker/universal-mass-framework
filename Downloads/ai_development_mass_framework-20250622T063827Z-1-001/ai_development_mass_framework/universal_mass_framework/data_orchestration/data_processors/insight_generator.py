"""
Universal MASS Framework - Insight Generator
===========================================

Advanced business intelligence and insight generation engine for the Universal MASS Framework.
This component analyzes data patterns, trends, and correlations to generate actionable
business insights with confidence scoring and recommendations.

Key Features:
- Multi-dimensional insight generation
- Business intelligence analysis
- Trend analysis and forecasting
- Impact assessment and scoring
- Actionable recommendations
- Real-time insight updates
"""

import asyncio
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import statistics
import json

logger = logging.getLogger(__name__)


class InsightType(Enum):
    """Types of insights that can be generated"""
    TREND = "trend"
    ANOMALY = "anomaly"
    OPPORTUNITY = "opportunity"
    RISK = "risk"
    PREDICTION = "prediction"
    CORRELATION = "correlation"
    PERFORMANCE = "performance"
    OPTIMIZATION = "optimization"
    MARKET = "market"
    OPERATIONAL = "operational"


class InsightPriority(Enum):
    """Priority levels for insights"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class InsightCategory(Enum):
    """Categories of business insights"""
    FINANCIAL = "financial"
    OPERATIONAL = "operational"
    STRATEGIC = "strategic"
    TACTICAL = "tactical"
    CUSTOMER = "customer"
    MARKET = "market"
    TECHNICAL = "technical"
    RISK = "risk"


@dataclass
class BusinessInsight:
    """A generated business insight with supporting data"""
    insight_id: str
    title: str
    description: str
    insight_type: InsightType
    category: InsightCategory
    priority: InsightPriority
    confidence: float  # 0.0 to 1.0
    impact_score: float  # 0.0 to 1.0
    
    # Supporting data
    key_metrics: Dict[str, Any]
    evidence: List[Dict[str, Any]]
    correlations: List[str]
    
    # Recommendations
    recommendations: List[str]
    action_items: List[Dict[str, Any]]
    estimated_impact: str
    
    # Metadata
    data_sources: List[str]
    analysis_period: Dict[str, str]
    generated_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "insight_id": self.insight_id,
            "title": self.title,
            "description": self.description,
            "insight_type": self.insight_type.value,
            "category": self.category.value,
            "priority": self.priority.value,
            "confidence": self.confidence,
            "impact_score": self.impact_score,
            "key_metrics": self.key_metrics,
            "evidence": self.evidence,
            "correlations": self.correlations,
            "recommendations": self.recommendations,
            "action_items": self.action_items,
            "estimated_impact": self.estimated_impact,
            "data_sources": self.data_sources,
            "analysis_period": self.analysis_period,
            "generated_at": self.generated_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None
        }


@dataclass
class InsightContext:
    """Context for insight generation"""
    business_domain: str
    analysis_objectives: List[str]
    time_horizon: str
    stakeholders: List[str]
    constraints: Dict[str, Any]
    preferences: Dict[str, Any]


class InsightGenerator:
    """
    Universal Business Insight Generator
    
    CAPABILITIES:
    - Multi-source data analysis
    - Pattern recognition and trend analysis
    - Anomaly detection and risk assessment
    - Opportunity identification
    - Predictive insights
    - Performance optimization insights
    - Strategic recommendations
    """
    
    def __init__(self):
        """Initialize the insight generator"""
        self.insight_history = []
        self.insight_templates = self._initialize_insight_templates()
        self.analysis_algorithms = self._initialize_analysis_algorithms()
        
        # Performance tracking
        self.generation_stats = {
            "insights_generated": 0,
            "avg_confidence": 0.0,
            "avg_impact_score": 0.0,
            "success_rate": 0.0,
            "processing_time": 0.0
        }
    
    def _initialize_insight_templates(self) -> Dict[str, Dict[str, Any]]:
        """Initialize insight generation templates"""
        return {
            "trend_analysis": {
                "pattern": "trend_detected",
                "confidence_factors": ["data_quality", "trend_strength", "statistical_significance"],
                "template": "A {direction} trend has been detected in {metric} with {confidence}% confidence. The trend shows {change}% change over {period}."
            },
            "anomaly_detection": {
                "pattern": "anomaly_identified",
                "confidence_factors": ["deviation_magnitude", "historical_context", "data_reliability"],
                "template": "An anomaly has been detected in {metric}. The current value of {value} is {deviation}% {direction} from the expected range."
            },
            "opportunity_identification": {
                "pattern": "opportunity_found",
                "confidence_factors": ["market_conditions", "resource_availability", "risk_factors"],
                "template": "A {type} opportunity has been identified with potential {impact} impact. Key factors: {factors}."
            },
            "performance_optimization": {
                "pattern": "optimization_potential",
                "confidence_factors": ["efficiency_gap", "implementation_feasibility", "cost_benefit"],
                "template": "Performance optimization opportunity identified in {area}. Potential improvement: {improvement}% with {effort} implementation effort."
            },
            "risk_assessment": {
                "pattern": "risk_identified",
                "confidence_factors": ["probability", "impact_magnitude", "mitigation_options"],
                "template": "Risk identified in {area} with {probability} probability and {impact} potential impact. Immediate attention recommended."
            }
        }
    
    def _initialize_analysis_algorithms(self) -> Dict[str, Any]:
        """Initialize analysis algorithms"""
        return {
            "trend_detection": self._detect_trends,
            "anomaly_detection": self._detect_anomalies,
            "correlation_analysis": self._analyze_correlations,
            "performance_analysis": self._analyze_performance,
            "opportunity_analysis": self._identify_opportunities,
            "risk_analysis": self._assess_risks,
            "prediction_analysis": self._generate_predictions
        }
    
    async def generate_insights(self, data_sets: Dict[str, List[Dict[str, Any]]], 
                              context: InsightContext,
                              correlations: List[Dict[str, Any]] = None) -> List[BusinessInsight]:
        """
        Generate business insights from multiple data sources
        
        Args:
            data_sets: Dictionary of data sources and their data
            context: Business context for insight generation
            correlations: Pre-computed correlations between data sources
            
        Returns:
            List of generated business insights
        """
        start_time = datetime.utcnow()
        
        try:
            insights = []
            
            # Run all analysis algorithms
            for algorithm_name, algorithm_func in self.analysis_algorithms.items():
                try:
                    algorithm_insights = await algorithm_func(data_sets, context, correlations)
                    if algorithm_insights:
                        insights.extend(algorithm_insights)
                except Exception as e:
                    logger.error(f"Error in {algorithm_name}: {str(e)}")
                    continue
            
            # Rank and filter insights
            insights = self._rank_insights(insights)
            insights = self._filter_duplicate_insights(insights)
            
            # Add to history
            self.insight_history.extend(insights)
            
            # Update statistics
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            self._update_generation_stats(insights, processing_time)
            
            logger.info(f"Generated {len(insights)} business insights")
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return []
    
    async def _detect_trends(self, data_sets: Dict[str, List[Dict[str, Any]]], 
                           context: InsightContext,
                           correlations: List[Dict[str, Any]] = None) -> List[BusinessInsight]:
        """Detect trend patterns in data"""
        insights = []
        
        for source_name, data in data_sets.items():
            try:
                # Extract time series data
                time_series = self._extract_time_series_metrics(data)
                
                for metric_name, values in time_series.items():
                    if len(values) < 5:  # Need minimum data points
                        continue
                    
                    # Calculate trend
                    trend_info = self._calculate_trend(values)
                    
                    if trend_info and abs(trend_info['slope']) > 0.1:
                        confidence = min(0.95, trend_info['r_squared'])
                        
                        if confidence > 0.5:
                            insight = BusinessInsight(
                                insight_id=f"trend_{source_name}_{metric_name}_{int(datetime.utcnow().timestamp())}",
                                title=f"{trend_info['direction'].title()} Trend in {metric_name.title()}",
                                description=f"A {trend_info['direction']} trend has been detected in {metric_name} from {source_name}. "
                                          f"The trend shows {abs(trend_info['change_percent']):.1f}% change over the analysis period.",
                                insight_type=InsightType.TREND,
                                category=self._determine_category(source_name, metric_name),
                                priority=self._determine_priority(trend_info['change_percent'], confidence),
                                confidence=confidence,
                                impact_score=min(1.0, abs(trend_info['change_percent']) / 100),
                                key_metrics={
                                    "trend_direction": trend_info['direction'],
                                    "change_percent": trend_info['change_percent'],
                                    "slope": trend_info['slope'],
                                    "r_squared": trend_info['r_squared'],
                                    "data_points": len(values)
                                },
                                evidence=[
                                    {
                                        "type": "statistical_analysis",
                                        "description": f"Linear regression analysis with R² = {trend_info['r_squared']:.3f}",
                                        "confidence": trend_info['r_squared']
                                    }
                                ],
                                correlations=[],
                                recommendations=self._generate_trend_recommendations(trend_info, metric_name),
                                action_items=self._generate_trend_actions(trend_info, metric_name),
                                estimated_impact=self._estimate_trend_impact(trend_info),
                                data_sources=[source_name],
                                analysis_period={
                                    "start": values[0]["timestamp"].isoformat() if values else "",
                                    "end": values[-1]["timestamp"].isoformat() if values else ""
                                }
                            )
                            insights.append(insight)
                
            except Exception as e:
                logger.error(f"Error detecting trends in {source_name}: {str(e)}")
                continue
        
        return insights
    
    async def _detect_anomalies(self, data_sets: Dict[str, List[Dict[str, Any]]], 
                              context: InsightContext,
                              correlations: List[Dict[str, Any]] = None) -> List[BusinessInsight]:
        """Detect anomalies in data"""
        insights = []
        
        for source_name, data in data_sets.items():
            try:
                # Extract numeric metrics
                numeric_metrics = self._extract_numeric_metrics(data)
                
                for metric_name, values in numeric_metrics.items():
                    if len(values) < 10:  # Need minimum data for anomaly detection
                        continue
                    
                    # Detect anomalies using statistical methods
                    anomalies = self._detect_statistical_anomalies(values)
                    
                    if anomalies:
                        for anomaly in anomalies:
                            confidence = anomaly['confidence']
                            
                            if confidence > 0.7:
                                insight = BusinessInsight(
                                    insight_id=f"anomaly_{source_name}_{metric_name}_{int(datetime.utcnow().timestamp())}",
                                    title=f"Anomaly Detected in {metric_name.title()}",
                                    description=f"An anomaly has been detected in {metric_name} from {source_name}. "
                                              f"The value {anomaly['value']} is {anomaly['deviation']:.1f}% "
                                              f"{'above' if anomaly['direction'] == 'high' else 'below'} the expected range.",
                                    insight_type=InsightType.ANOMALY,
                                    category=self._determine_category(source_name, metric_name),
                                    priority=self._determine_anomaly_priority(anomaly),
                                    confidence=confidence,
                                    impact_score=min(1.0, abs(anomaly['deviation']) / 100),
                                    key_metrics={
                                        "anomaly_value": anomaly['value'],
                                        "expected_range": anomaly['expected_range'],
                                        "deviation_percent": anomaly['deviation'],
                                        "z_score": anomaly['z_score'],
                                        "direction": anomaly['direction']
                                    },
                                    evidence=[
                                        {
                                            "type": "statistical_analysis",
                                            "description": f"Z-score analysis: {anomaly['z_score']:.2f}",
                                            "confidence": confidence
                                        }
                                    ],
                                    correlations=[],
                                    recommendations=self._generate_anomaly_recommendations(anomaly, metric_name),
                                    action_items=self._generate_anomaly_actions(anomaly, metric_name),
                                    estimated_impact=self._estimate_anomaly_impact(anomaly),
                                    data_sources=[source_name],
                                    analysis_period={
                                        "start": (datetime.utcnow() - timedelta(hours=24)).isoformat(),
                                        "end": datetime.utcnow().isoformat()
                                    }
                                )
                                insights.append(insight)
                
            except Exception as e:
                logger.error(f"Error detecting anomalies in {source_name}: {str(e)}")
                continue
        
        return insights
    
    async def _analyze_correlations(self, data_sets: Dict[str, List[Dict[str, Any]]], 
                                  context: InsightContext,
                                  correlations: List[Dict[str, Any]] = None) -> List[BusinessInsight]:
        """Analyze correlations for insights"""
        insights = []
        
        if not correlations:
            return insights
        
        # Find strong correlations
        strong_correlations = [c for c in correlations if abs(c.get('coefficient', 0)) > 0.7]
        
        for correlation in strong_correlations:
            try:
                confidence = correlation.get('confidence', 0.5)
                
                if confidence > 0.6:
                    insight = BusinessInsight(
                        insight_id=f"correlation_{correlation.get('correlation_id', 'unknown')}",
                        title=f"Strong Correlation Between {correlation.get('source_a', '')} and {correlation.get('source_b', '')}",
                        description=f"A strong correlation (r={correlation.get('coefficient', 0):.2f}) has been detected between "
                                  f"{correlation.get('source_a', '')} and {correlation.get('source_b', '')}. "
                                  f"This suggests these metrics may be influenced by common factors.",
                        insight_type=InsightType.CORRELATION,
                        category=InsightCategory.STRATEGIC,
                        priority=InsightPriority.MEDIUM if abs(correlation.get('coefficient', 0)) > 0.8 else InsightPriority.LOW,
                        confidence=confidence,
                        impact_score=abs(correlation.get('coefficient', 0)),
                        key_metrics={
                            "correlation_coefficient": correlation.get('coefficient', 0),
                            "correlation_type": correlation.get('correlation_type', ''),
                            "significance": correlation.get('significance', 0)
                        },
                        evidence=[
                            {
                                "type": "correlation_analysis",
                                "description": f"Statistical correlation analysis",
                                "confidence": confidence
                            }
                        ],
                        correlations=[correlation.get('correlation_id', '')],
                        recommendations=self._generate_correlation_recommendations(correlation),
                        action_items=self._generate_correlation_actions(correlation),
                        estimated_impact="Medium - Can improve prediction accuracy",
                        data_sources=[correlation.get('source_a', ''), correlation.get('source_b', '')],
                        analysis_period={
                            "start": (datetime.utcnow() - timedelta(hours=24)).isoformat(),
                            "end": datetime.utcnow().isoformat()
                        }
                    )
                    insights.append(insight)
                
            except Exception as e:
                logger.error(f"Error analyzing correlation: {str(e)}")
                continue
        
        return insights
    
    async def _analyze_performance(self, data_sets: Dict[str, List[Dict[str, Any]]], 
                                 context: InsightContext,
                                 correlations: List[Dict[str, Any]] = None) -> List[BusinessInsight]:
        """Analyze performance metrics"""
        insights = []
        
        # Performance analysis logic would go here
        # This is a simplified example
        
        for source_name, data in data_sets.items():
            try:
                # Look for performance indicators
                performance_metrics = self._extract_performance_metrics(data)
                
                for metric_name, metric_data in performance_metrics.items():
                    if metric_data['current_value'] and metric_data['baseline']:
                        performance_change = ((metric_data['current_value'] - metric_data['baseline']) / metric_data['baseline']) * 100
                        
                        if abs(performance_change) > 10:  # Significant change
                            insight = BusinessInsight(
                                insight_id=f"performance_{source_name}_{metric_name}_{int(datetime.utcnow().timestamp())}",
                                title=f"Performance Change in {metric_name.title()}",
                                description=f"Performance change of {performance_change:.1f}% detected in {metric_name}",
                                insight_type=InsightType.PERFORMANCE,
                                category=InsightCategory.OPERATIONAL,
                                priority=InsightPriority.HIGH if abs(performance_change) > 25 else InsightPriority.MEDIUM,
                                confidence=0.8,
                                impact_score=min(1.0, abs(performance_change) / 100),
                                key_metrics={
                                    "current_value": metric_data['current_value'],
                                    "baseline": metric_data['baseline'],
                                    "change_percent": performance_change
                                },
                                evidence=[],
                                correlations=[],
                                recommendations=self._generate_performance_recommendations(performance_change, metric_name),
                                action_items=self._generate_performance_actions(performance_change, metric_name),
                                estimated_impact=self._estimate_performance_impact(performance_change),
                                data_sources=[source_name],
                                analysis_period={
                                    "start": (datetime.utcnow() - timedelta(hours=24)).isoformat(),
                                    "end": datetime.utcnow().isoformat()
                                }
                            )
                            insights.append(insight)
                
            except Exception as e:
                logger.error(f"Error analyzing performance in {source_name}: {str(e)}")
                continue
        
        return insights
    
    async def _identify_opportunities(self, data_sets: Dict[str, List[Dict[str, Any]]], 
                                    context: InsightContext,
                                    correlations: List[Dict[str, Any]] = None) -> List[BusinessInsight]:
        """Identify business opportunities"""
        insights = []
        
        # Opportunity identification logic
        # This is a simplified example focusing on growth opportunities
        
        for source_name, data in data_sets.items():
            try:
                growth_metrics = self._identify_growth_opportunities(data)
                
                for opportunity in growth_metrics:
                    if opportunity['potential_impact'] > 0.1:
                        insight = BusinessInsight(
                            insight_id=f"opportunity_{source_name}_{int(datetime.utcnow().timestamp())}",
                            title=f"Growth Opportunity: {opportunity['title']}",
                            description=opportunity['description'],
                            insight_type=InsightType.OPPORTUNITY,
                            category=InsightCategory.STRATEGIC,
                            priority=InsightPriority.HIGH if opportunity['potential_impact'] > 0.5 else InsightPriority.MEDIUM,
                            confidence=opportunity['confidence'],
                            impact_score=opportunity['potential_impact'],
                            key_metrics=opportunity['metrics'],
                            evidence=opportunity['evidence'],
                            correlations=[],
                            recommendations=opportunity['recommendations'],
                            action_items=opportunity['action_items'],
                            estimated_impact=opportunity['estimated_impact'],
                            data_sources=[source_name],
                            analysis_period={
                                "start": (datetime.utcnow() - timedelta(days=7)).isoformat(),
                                "end": datetime.utcnow().isoformat()
                            }
                        )
                        insights.append(insight)
                
            except Exception as e:
                logger.error(f"Error identifying opportunities in {source_name}: {str(e)}")
                continue
        
        return insights
    
    async def _assess_risks(self, data_sets: Dict[str, List[Dict[str, Any]]], 
                          context: InsightContext,
                          correlations: List[Dict[str, Any]] = None) -> List[BusinessInsight]:
        """Assess business risks"""
        insights = []
        
        # Risk assessment logic
        # This would include volatility analysis, threshold breaches, etc.
        
        return insights
    
    async def _generate_predictions(self, data_sets: Dict[str, List[Dict[str, Any]]], 
                                  context: InsightContext,
                                  correlations: List[Dict[str, Any]] = None) -> List[BusinessInsight]:
        """Generate predictive insights"""
        insights = []
        
        # Predictive analysis logic
        # This would include forecasting and prediction models
        
        return insights
    
    # Helper methods for data processing and analysis
    
    def _extract_time_series_metrics(self, data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Extract time series metrics from data"""
        time_series = {}
        
        for item in data:
            timestamp = self._extract_timestamp(item)
            if not timestamp:
                continue
                
            for key, value in item.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    if key not in time_series:
                        time_series[key] = []
                    
                    time_series[key].append({
                        'timestamp': timestamp,
                        'value': float(value)
                    })
        
        # Sort by timestamp
        for key in time_series:
            time_series[key].sort(key=lambda x: x['timestamp'])
        
        return time_series
    
    def _extract_numeric_metrics(self, data: List[Dict[str, Any]]) -> Dict[str, List[float]]:
        """Extract numeric metrics from data"""
        metrics = {}
        
        for item in data:
            for key, value in item.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    if key not in metrics:
                        metrics[key] = []
                    metrics[key].append(float(value))
        
        return metrics
    
    def _extract_performance_metrics(self, data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Extract performance metrics"""
        performance_keywords = ['response_time', 'throughput', 'cpu_usage', 'memory_usage', 'error_rate', 'success_rate']
        metrics = {}
        
        # Look for performance-related metrics
        for item in data:
            for key, value in item.items():
                if any(keyword in key.lower() for keyword in performance_keywords):
                    if isinstance(value, (int, float)):
                        if key not in metrics:
                            metrics[key] = {'values': [], 'current_value': None, 'baseline': None}
                        
                        metrics[key]['values'].append(float(value))
                        metrics[key]['current_value'] = float(value)
        
        # Calculate baselines (average of all values)
        for key in metrics:
            if metrics[key]['values']:
                metrics[key]['baseline'] = sum(metrics[key]['values']) / len(metrics[key]['values'])
        
        return metrics
    
    def _extract_timestamp(self, item: Dict[str, Any]) -> Optional[datetime]:
        """Extract timestamp from data item"""
        timestamp_fields = ['timestamp', 'time', 'date', 'created_at', 'updated_at']
        
        for field in timestamp_fields:
            if field in item:
                try:
                    if isinstance(item[field], str):
                        return pd.to_datetime(item[field])
                    elif isinstance(item[field], (int, float)):
                        return pd.to_datetime(item[field], unit='s')
                    elif isinstance(item[field], datetime):
                        return item[field]
                except:
                    continue
        
        return None
    
    def _calculate_trend(self, values: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Calculate trend information for time series data"""
        if len(values) < 2:
            return None
        
        try:
            # Extract x (time) and y (values) for linear regression
            x = np.arange(len(values))
            y = np.array([v['value'] for v in values])
            
            # Calculate linear regression
            slope, intercept = np.polyfit(x, y, 1)
            
            # Calculate R-squared
            y_pred = slope * x + intercept
            ss_res = np.sum((y - y_pred) ** 2)
            ss_tot = np.sum((y - np.mean(y)) ** 2)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            # Calculate change percentage
            if values[0]['value'] != 0:
                change_percent = ((values[-1]['value'] - values[0]['value']) / abs(values[0]['value'])) * 100
            else:
                change_percent = 0
            
            return {
                'slope': slope,
                'r_squared': r_squared,
                'change_percent': change_percent,
                'direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable'
            }
            
        except Exception as e:
            logger.error(f"Error calculating trend: {str(e)}")
            return None
    
    def _detect_statistical_anomalies(self, values: List[float]) -> List[Dict[str, Any]]:
        """Detect statistical anomalies using Z-score method"""
        if len(values) < 5:
            return []
        
        try:
            mean_val = np.mean(values)
            std_val = np.std(values)
            
            if std_val == 0:
                return []
            
            anomalies = []
            threshold = 2.5  # Z-score threshold
            
            for i, value in enumerate(values[-5:]):  # Check last 5 values
                z_score = abs((value - mean_val) / std_val)
                
                if z_score > threshold:
                    deviation = ((value - mean_val) / mean_val) * 100 if mean_val != 0 else 0
                    
                    anomalies.append({
                        'value': value,
                        'z_score': z_score,
                        'deviation': abs(deviation),
                        'direction': 'high' if value > mean_val else 'low',
                        'expected_range': (mean_val - 2*std_val, mean_val + 2*std_val),
                        'confidence': min(0.95, z_score / 5.0)  # Scale confidence based on Z-score
                    })
            
            return anomalies
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {str(e)}")
            return []
    
    def _identify_growth_opportunities(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify growth opportunities in data"""
        opportunities = []
        
        # Simple example: look for underutilized capacity
        if len(data) > 0:
            opportunities.append({
                'title': 'Data Growth Opportunity',
                'description': f'Growing data volume ({len(data)} records) indicates increasing activity',
                'potential_impact': min(1.0, len(data) / 1000),
                'confidence': 0.7,
                'metrics': {'data_volume': len(data)},
                'evidence': [{'type': 'volume_analysis', 'description': 'Increasing data volume'}],
                'recommendations': ['Monitor growth patterns', 'Scale infrastructure proactively'],
                'action_items': [{'action': 'capacity_planning', 'priority': 'medium', 'timeline': '1 week'}],
                'estimated_impact': 'Medium - supports business growth'
            })
        
        return opportunities
    
    # Recommendation generation methods
    
    def _generate_trend_recommendations(self, trend_info: Dict[str, Any], metric_name: str) -> List[str]:
        """Generate recommendations based on trend analysis"""
        recommendations = []
        
        if trend_info['direction'] == 'increasing':
            recommendations.extend([
                f"Monitor {metric_name} for sustained growth",
                "Consider scaling resources to support continued growth",
                "Analyze root causes of positive trend"
            ])
        elif trend_info['direction'] == 'decreasing':
            recommendations.extend([
                f"Investigate causes of decline in {metric_name}",
                "Implement corrective measures if needed",
                "Monitor closely for further deterioration"
            ])
        
        return recommendations
    
    def _generate_anomaly_recommendations(self, anomaly: Dict[str, Any], metric_name: str) -> List[str]:
        """Generate recommendations for anomalies"""
        return [
            f"Investigate the cause of the anomaly in {metric_name}",
            "Check for data quality issues or system problems",
            "Monitor closely for additional anomalies",
            "Consider adjusting alert thresholds if this becomes normal"
        ]
    
    def _generate_correlation_recommendations(self, correlation: Dict[str, Any]) -> List[str]:
        """Generate recommendations for correlations"""
        return [
            "Use correlation for predictive modeling",
            "Monitor both metrics together",
            "Investigate common underlying factors",
            "Consider correlation in decision making"
        ]
    
    def _generate_performance_recommendations(self, change_percent: float, metric_name: str) -> List[str]:
        """Generate performance recommendations"""
        if change_percent > 0:
            return [
                f"Performance improvement in {metric_name} - analyze success factors",
                "Document best practices",
                "Apply learnings to other areas"
            ]
        else:
            return [
                f"Performance decline in {metric_name} - immediate investigation needed",
                "Identify root causes",
                "Implement corrective actions"
            ]
    
    # Action item generation methods
    
    def _generate_trend_actions(self, trend_info: Dict[str, Any], metric_name: str) -> List[Dict[str, Any]]:
        """Generate action items for trends"""
        return [
            {
                "action": f"trend_analysis_{metric_name}",
                "description": f"Deep dive analysis of {metric_name} trend",
                "priority": "medium",
                "timeline": "1 week",
                "owner": "data_team"
            }
        ]
    
    def _generate_anomaly_actions(self, anomaly: Dict[str, Any], metric_name: str) -> List[Dict[str, Any]]:
        """Generate action items for anomalies"""
        return [
            {
                "action": f"anomaly_investigation_{metric_name}",
                "description": f"Investigate anomaly in {metric_name}",
                "priority": "high",
                "timeline": "24 hours",
                "owner": "ops_team"
            }
        ]
    
    def _generate_correlation_actions(self, correlation: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate action items for correlations"""
        return [
            {
                "action": "correlation_analysis",
                "description": "Analyze correlation for predictive modeling",
                "priority": "medium",
                "timeline": "2 weeks",
                "owner": "analytics_team"
            }
        ]
    
    def _generate_performance_actions(self, change_percent: float, metric_name: str) -> List[Dict[str, Any]]:
        """Generate action items for performance changes"""
        priority = "high" if abs(change_percent) > 25 else "medium"
        
        return [
            {
                "action": f"performance_review_{metric_name}",
                "description": f"Review performance change in {metric_name}",
                "priority": priority,
                "timeline": "3 days",
                "owner": "performance_team"
            }
        ]
    
    # Impact estimation methods
    
    def _estimate_trend_impact(self, trend_info: Dict[str, Any]) -> str:
        """Estimate impact of trend"""
        if abs(trend_info['change_percent']) > 50:
            return "High - Significant trend with major implications"
        elif abs(trend_info['change_percent']) > 20:
            return "Medium - Notable trend requiring attention"
        else:
            return "Low - Minor trend to monitor"
    
    def _estimate_anomaly_impact(self, anomaly: Dict[str, Any]) -> str:
        """Estimate impact of anomaly"""
        if anomaly['z_score'] > 4:
            return "Critical - Extreme anomaly requiring immediate action"
        elif anomaly['z_score'] > 3:
            return "High - Significant anomaly needing investigation"
        else:
            return "Medium - Anomaly worth monitoring"
    
    def _estimate_performance_impact(self, change_percent: float) -> str:
        """Estimate impact of performance change"""
        if abs(change_percent) > 30:
            return "High - Major performance impact"
        elif abs(change_percent) > 15:
            return "Medium - Noticeable performance impact"
        else:
            return "Low - Minor performance impact"
    
    # Utility methods
    
    def _determine_category(self, source_name: str, metric_name: str) -> InsightCategory:
        """Determine insight category based on source and metric"""
        source_lower = source_name.lower()
        metric_lower = metric_name.lower()
        
        if any(keyword in source_lower for keyword in ['financial', 'revenue', 'cost', 'profit']):
            return InsightCategory.FINANCIAL
        elif any(keyword in source_lower for keyword in ['customer', 'user', 'client']):
            return InsightCategory.CUSTOMER
        elif any(keyword in source_lower for keyword in ['market', 'competitor', 'industry']):
            return InsightCategory.MARKET
        elif any(keyword in metric_lower for keyword in ['performance', 'latency', 'throughput']):
            return InsightCategory.TECHNICAL
        elif any(keyword in metric_lower for keyword in ['risk', 'security', 'compliance']):
            return InsightCategory.RISK
        else:
            return InsightCategory.OPERATIONAL
    
    def _determine_priority(self, change_percent: float, confidence: float) -> InsightPriority:
        """Determine insight priority"""
        impact = abs(change_percent) * confidence
        
        if impact > 50:
            return InsightPriority.CRITICAL
        elif impact > 25:
            return InsightPriority.HIGH
        elif impact > 10:
            return InsightPriority.MEDIUM
        else:
            return InsightPriority.LOW
    
    def _determine_anomaly_priority(self, anomaly: Dict[str, Any]) -> InsightPriority:
        """Determine priority for anomaly"""
        if anomaly['z_score'] > 4:
            return InsightPriority.CRITICAL
        elif anomaly['z_score'] > 3:
            return InsightPriority.HIGH
        elif anomaly['z_score'] > 2.5:
            return InsightPriority.MEDIUM
        else:
            return InsightPriority.LOW
    
    def _rank_insights(self, insights: List[BusinessInsight]) -> List[BusinessInsight]:
        """Rank insights by priority and impact"""
        priority_weights = {
            InsightPriority.CRITICAL: 4,
            InsightPriority.HIGH: 3,
            InsightPriority.MEDIUM: 2,
            InsightPriority.LOW: 1
        }
        
        return sorted(insights, key=lambda x: (
            priority_weights.get(x.priority, 0),
            x.impact_score,
            x.confidence
        ), reverse=True)
    
    def _filter_duplicate_insights(self, insights: List[BusinessInsight]) -> List[BusinessInsight]:
        """Filter out duplicate insights"""
        seen_insights = set()
        unique_insights = []
        
        for insight in insights:
            # Create a simple hash based on type, sources, and key metrics
            insight_hash = f"{insight.insight_type.value}_{','.join(insight.data_sources)}_{hash(str(insight.key_metrics))}"
            
            if insight_hash not in seen_insights:
                seen_insights.add(insight_hash)
                unique_insights.append(insight)
        
        return unique_insights
    
    def _update_generation_stats(self, insights: List[BusinessInsight], processing_time: float):
        """Update generation statistics"""
        self.generation_stats["insights_generated"] += len(insights)
        
        if insights:
            avg_confidence = sum(i.confidence for i in insights) / len(insights)
            avg_impact = sum(i.impact_score for i in insights) / len(insights)
            
            # Update running averages
            total_insights = self.generation_stats["insights_generated"]
            prev_conf = self.generation_stats["avg_confidence"]
            prev_impact = self.generation_stats["avg_impact"]
            
            self.generation_stats["avg_confidence"] = (
                (prev_conf * (total_insights - len(insights))) + (avg_confidence * len(insights))
            ) / total_insights
            
            self.generation_stats["avg_impact_score"] = (
                (prev_impact * (total_insights - len(insights))) + (avg_impact * len(insights))
            ) / total_insights
        
        self.generation_stats["processing_time"] = processing_time
    
    async def get_insight_summary(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get summary of generated insights"""
        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        recent_insights = [
            insight for insight in self.insight_history 
            if insight.generated_at >= cutoff_time
        ]
        
        if not recent_insights:
            return {
                "summary": "No recent insights generated",
                "time_window_hours": time_window_hours,
                "total_insights": 0
            }
        
        # Calculate summary statistics
        priorities = [insight.priority.value for insight in recent_insights]
        categories = [insight.category.value for insight in recent_insights]
        types = [insight.insight_type.value for insight in recent_insights]
        
        return {
            "time_window_hours": time_window_hours,
            "total_insights": len(recent_insights),
            "priority_distribution": {p.value: priorities.count(p.value) for p in InsightPriority},
            "category_distribution": {c.value: categories.count(c.value) for c in InsightCategory},
            "type_distribution": {t.value: types.count(t.value) for t in InsightType},
            "average_confidence": sum(i.confidence for i in recent_insights) / len(recent_insights),
            "average_impact_score": sum(i.impact_score for i in recent_insights) / len(recent_insights),
            "generation_stats": self.generation_stats.copy()
        }


# Export the main classes
__all__ = ['InsightGenerator', 'BusinessInsight', 'InsightContext', 'InsightType', 'InsightPriority', 'InsightCategory']
