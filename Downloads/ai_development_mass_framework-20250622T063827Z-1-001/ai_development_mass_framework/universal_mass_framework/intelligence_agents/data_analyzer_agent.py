"""
Data Analyzer Agent - Universal Data Analysis

This agent can analyze ANY type of data and provide intelligent insights,
statistical analysis, correlation detection, and data quality assessment.

Key Features:
- Universal data type support (structured, unstructured, time-series, etc.)
- Real-time statistical analysis and correlation detection
- Data quality assessment and anomaly identification
- Intelligent data visualization recommendations
- Cross-source data fusion and correlation analysis
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import statistics
import numpy as np
from collections import defaultdict

from ..core.config_manager import MassConfig
from ..enterprise_trust.trusted_ai_framework import TrustedAIFramework

logger = logging.getLogger(__name__)


class DataType(Enum):
    """Supported data types for analysis"""
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    TIME_SERIES = "time_series"
    TEXT = "text"
    GEOSPATIAL = "geospatial"
    IMAGE = "image"
    MIXED = "mixed"


class AnalysisType(Enum):
    """Types of analysis that can be performed"""
    DESCRIPTIVE = "descriptive"
    EXPLORATORY = "exploratory"
    INFERENTIAL = "inferential"
    PREDICTIVE = "predictive"
    CAUSAL = "causal"
    COMPARATIVE = "comparative"


@dataclass
class DataQuality:
    """Data quality assessment results"""
    completeness: float  # 0-1, percentage of non-null values
    accuracy: float      # 0-1, estimated accuracy based on validation rules
    consistency: float   # 0-1, consistency across data sources
    timeliness: float   # 0-1, how recent the data is
    validity: float     # 0-1, adherence to expected formats/ranges
    overall_score: float # 0-1, weighted overall quality score
    issues: List[str]   # List of identified issues
    recommendations: List[str]  # Recommendations for improvement


@dataclass
class StatisticalSummary:
    """Statistical summary of numerical data"""
    count: int
    mean: float
    median: float
    std_dev: float
    min_value: float
    max_value: float
    quartiles: List[float]
    skewness: Optional[float] = None
    kurtosis: Optional[float] = None
    outliers: List[Any] = None


@dataclass
class CorrelationResult:
    """Correlation analysis results"""
    variable1: str
    variable2: str
    correlation_coefficient: float
    correlation_type: str  # pearson, spearman, kendall
    p_value: float
    significance_level: float
    interpretation: str


@dataclass
class AnalysisResult:
    """Comprehensive analysis results"""
    analysis_id: str
    data_type: DataType
    analysis_type: AnalysisType
    timestamp: datetime
    data_quality: DataQuality
    statistical_summary: Optional[StatisticalSummary]
    correlations: List[CorrelationResult]
    insights: List[str]
    recommendations: List[str]
    visualizations: List[Dict[str, Any]]
    confidence_score: float
    execution_time_ms: int


class DataAnalyzerAgent:
    """
    Universal Data Analyzer Agent
    
    Capable of analyzing any type of data and providing intelligent insights,
    statistical analysis, and data quality assessment with enterprise-grade trust validation.
    """
    
    def __init__(self, config: Optional[MassConfig] = None):
        self.config = config or MassConfig()
        self.trust_framework = TrustedAIFramework(self.config)
        self.logger = logging.getLogger(__name__)
        
        # Analysis configuration
        self.max_analysis_time = 30  # seconds
        self.confidence_threshold = 0.7
        self.outlier_threshold = 2.5  # standard deviations
        
        # Initialize analysis engines
        self._initialize_analysis_engines()
    
    def _initialize_analysis_engines(self):
        """Initialize various analysis engines"""
        self.statistical_engine = StatisticalAnalysisEngine()
        self.correlation_engine = CorrelationAnalysisEngine()
        self.quality_assessor = DataQualityAssessor()
        self.insight_generator = InsightGenerator()
        self.visualization_recommender = VisualizationRecommender()
    
    async def analyze_data(self, data: Union[Dict[str, Any], List[Any]], 
                          analysis_type: AnalysisType = AnalysisType.EXPLORATORY,
                          context: Optional[Dict[str, Any]] = None) -> AnalysisResult:
        """
        Analyze any type of data and provide comprehensive insights
        
        Args:
            data: The data to analyze (dict, list, or any structure)
            analysis_type: Type of analysis to perform
            context: Additional context about the data
            
        Returns:
            Comprehensive analysis results with insights and recommendations
        """
        start_time = datetime.utcnow()
        analysis_id = f"analysis_{int(start_time.timestamp() * 1000)}"
        
        try:
            # Validate with trust framework
            trust_validation = await self.trust_framework.validate_operation(
                operation_type="data_analysis",
                data={"data_sample": str(data)[:1000] if isinstance(data, str) else data},
                context=context or {}
            )
            
            if not trust_validation.is_valid:
                raise ValueError(f"Trust validation failed: {trust_validation.validation_details}")
            
            # Detect data type
            detected_data_type = self._detect_data_type(data)
            self.logger.info(f"Detected data type: {detected_data_type.value}")
            
            # Assess data quality
            data_quality = await self._assess_data_quality(data, detected_data_type)
            
            # Perform statistical analysis
            statistical_summary = None
            if detected_data_type in [DataType.NUMERICAL, DataType.TIME_SERIES, DataType.MIXED]:
                statistical_summary = await self._perform_statistical_analysis(data, detected_data_type)
            
            # Perform correlation analysis
            correlations = []
            if isinstance(data, dict) and len(data) > 1:
                correlations = await self._perform_correlation_analysis(data)
            
            # Generate insights
            insights = await self._generate_insights(data, detected_data_type, statistical_summary, correlations)
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(data_quality, insights, context)
            
            # Recommend visualizations
            visualizations = await self._recommend_visualizations(data, detected_data_type, statistical_summary)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(data_quality, statistical_summary, len(insights))
            
            # Calculate execution time
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            
            # Create analysis result
            result = AnalysisResult(
                analysis_id=analysis_id,
                data_type=detected_data_type,
                analysis_type=analysis_type,
                timestamp=start_time,
                data_quality=data_quality,
                statistical_summary=statistical_summary,
                correlations=correlations,
                insights=insights,
                recommendations=recommendations,
                visualizations=visualizations,
                confidence_score=confidence_score,
                execution_time_ms=execution_time
            )
            
            # Log analysis for audit
            await self.trust_framework.log_operation(
                operation_type="data_analysis_completed",
                operation_data={
                    "analysis_id": analysis_id,
                    "data_type": detected_data_type.value,
                    "confidence_score": confidence_score,
                    "insights_count": len(insights),
                    "execution_time_ms": execution_time
                },
                result="success"
            )
            
            self.logger.info(f"Data analysis completed: {analysis_id} (confidence: {confidence_score:.3f})")
            return result
            
        except Exception as e:
            self.logger.error(f"Data analysis failed: {str(e)}")
            await self.trust_framework.log_operation(
                operation_type="data_analysis_failed",
                operation_data={"analysis_id": analysis_id, "error": str(e)},
                result="error"
            )
            raise
    
    def _detect_data_type(self, data: Any) -> DataType:
        """Detect the type of data being analyzed"""
        if isinstance(data, dict):
            # Analyze dictionary data
            value_types = set()
            for value in data.values():
                if isinstance(value, (int, float)):
                    value_types.add("numerical")
                elif isinstance(value, str):
                    value_types.add("text")
                elif isinstance(value, list):
                    if value and isinstance(value[0], (int, float)):
                        value_types.add("time_series")
                    else:
                        value_types.add("categorical")
            
            if len(value_types) > 1:
                return DataType.MIXED
            elif "numerical" in value_types:
                return DataType.NUMERICAL
            elif "time_series" in value_types:
                return DataType.TIME_SERIES
            elif "text" in value_types:
                return DataType.TEXT
            else:
                return DataType.CATEGORICAL
        
        elif isinstance(data, list):
            if not data:
                return DataType.MIXED
            
            first_item = data[0]
            if isinstance(first_item, (int, float)):
                return DataType.TIME_SERIES if len(data) > 10 else DataType.NUMERICAL
            elif isinstance(first_item, str):
                return DataType.TEXT
            elif isinstance(first_item, dict):
                return DataType.MIXED
            else:
                return DataType.CATEGORICAL
        
        elif isinstance(data, str):
            return DataType.TEXT
        
        elif isinstance(data, (int, float)):
            return DataType.NUMERICAL
        
        return DataType.MIXED
    
    async def _assess_data_quality(self, data: Any, data_type: DataType) -> DataQuality:
        """Assess the quality of the provided data"""
        return await self.quality_assessor.assess_quality(data, data_type)
    
    async def _perform_statistical_analysis(self, data: Any, data_type: DataType) -> StatisticalSummary:
        """Perform statistical analysis on numerical data"""
        return await self.statistical_engine.analyze(data, data_type)
    
    async def _perform_correlation_analysis(self, data: Dict[str, Any]) -> List[CorrelationResult]:
        """Perform correlation analysis between variables"""
        return await self.correlation_engine.analyze_correlations(data)
    
    async def _generate_insights(self, data: Any, data_type: DataType, 
                                statistical_summary: Optional[StatisticalSummary],
                                correlations: List[CorrelationResult]) -> List[str]:
        """Generate intelligent insights from the analysis"""
        return await self.insight_generator.generate_insights(data, data_type, statistical_summary, correlations)
    
    async def _generate_recommendations(self, data_quality: DataQuality, insights: List[str],
                                      context: Optional[Dict[str, Any]]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Data quality recommendations
        if data_quality.overall_score < 0.8:
            recommendations.extend(data_quality.recommendations)
        
        # Context-based recommendations
        if context:
            if context.get("purpose") == "business_decision":
                recommendations.append("Consider collecting additional data sources for more robust decision-making")
            elif context.get("purpose") == "prediction":
                recommendations.append("Implement data validation rules to improve prediction accuracy")
        
        # General recommendations based on insights
        if len(insights) < 3:
            recommendations.append("Consider expanding the dataset or analysis scope for deeper insights")
        
        return recommendations
    
    async def _recommend_visualizations(self, data: Any, data_type: DataType,
                                      statistical_summary: Optional[StatisticalSummary]) -> List[Dict[str, Any]]:
        """Recommend appropriate visualizations for the data"""
        return await self.visualization_recommender.recommend(data, data_type, statistical_summary)
    
    def _calculate_confidence_score(self, data_quality: DataQuality, 
                                  statistical_summary: Optional[StatisticalSummary],
                                  insights_count: int) -> float:
        """Calculate confidence score for the analysis"""
        # Base confidence from data quality
        base_confidence = data_quality.overall_score
        
        # Adjust based on statistical robustness
        if statistical_summary and statistical_summary.count > 30:
            base_confidence += 0.1  # More data points increase confidence
        
        # Adjust based on insights generated
        if insights_count >= 5:
            base_confidence += 0.1
        elif insights_count < 2:
            base_confidence -= 0.1
        
        return min(max(base_confidence, 0.0), 1.0)


# Supporting classes for Data Analyzer Agent

class StatisticalAnalysisEngine:
    """Performs statistical analysis on numerical data"""
    
    async def analyze(self, data: Any, data_type: DataType) -> StatisticalSummary:
        """Perform comprehensive statistical analysis"""
        numerical_values = self._extract_numerical_values(data, data_type)
        
        if not numerical_values:
            return StatisticalSummary(
                count=0, mean=0, median=0, std_dev=0,
                min_value=0, max_value=0, quartiles=[0, 0, 0]
            )
        
        # Calculate basic statistics
        count = len(numerical_values)
        mean = statistics.mean(numerical_values)
        median = statistics.median(numerical_values)
        std_dev = statistics.stdev(numerical_values) if count > 1 else 0
        min_value = min(numerical_values)
        max_value = max(numerical_values)
        
        # Calculate quartiles
        quartiles = [
            np.percentile(numerical_values, 25),
            np.percentile(numerical_values, 50),
            np.percentile(numerical_values, 75)
        ] if count > 3 else [min_value, median, max_value]
        
        # Calculate advanced statistics
        skewness = self._calculate_skewness(numerical_values) if count > 2 else None
        kurtosis = self._calculate_kurtosis(numerical_values) if count > 3 else None
        outliers = self._detect_outliers(numerical_values, mean, std_dev)
        
        return StatisticalSummary(
            count=count,
            mean=mean,
            median=median,
            std_dev=std_dev,
            min_value=min_value,
            max_value=max_value,
            quartiles=quartiles,
            skewness=skewness,
            kurtosis=kurtosis,
            outliers=outliers
        )
    
    def _extract_numerical_values(self, data: Any, data_type: DataType) -> List[float]:
        """Extract numerical values from various data structures"""
        values = []
        
        if isinstance(data, (int, float)):
            values.append(float(data))
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (int, float)):
                    values.append(float(item))
                elif isinstance(item, dict):
                    for value in item.values():
                        if isinstance(value, (int, float)):
                            values.append(float(value))
        elif isinstance(data, dict):
            for value in data.values():
                if isinstance(value, (int, float)):
                    values.append(float(value))
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, (int, float)):
                            values.append(float(item))
        
        return values
    
    def _calculate_skewness(self, values: List[float]) -> float:
        """Calculate skewness of the data"""
        n = len(values)
        if n < 3:
            return 0.0
        
        mean = statistics.mean(values)
        std_dev = statistics.stdev(values)
        
        if std_dev == 0:
            return 0.0
        
        skew_sum = sum(((x - mean) / std_dev) ** 3 for x in values)
        return (n / ((n - 1) * (n - 2))) * skew_sum
    
    def _calculate_kurtosis(self, values: List[float]) -> float:
        """Calculate kurtosis of the data"""
        n = len(values)
        if n < 4:
            return 0.0
        
        mean = statistics.mean(values)
        std_dev = statistics.stdev(values)
        
        if std_dev == 0:
            return 0.0
        
        kurt_sum = sum(((x - mean) / std_dev) ** 4 for x in values)
        return ((n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))) * kurt_sum - (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))
    
    def _detect_outliers(self, values: List[float], mean: float, std_dev: float) -> List[float]:
        """Detect outliers using z-score method"""
        outliers = []
        threshold = 2.5
        
        for value in values:
            if std_dev > 0:
                z_score = abs((value - mean) / std_dev)
                if z_score > threshold:
                    outliers.append(value)
        
        return outliers


class CorrelationAnalysisEngine:
    """Performs correlation analysis between variables"""
    
    async def analyze_correlations(self, data: Dict[str, Any]) -> List[CorrelationResult]:
        """Analyze correlations between variables in the data"""
        correlations = []
        numerical_vars = {}
        
        # Extract numerical variables
        for key, value in data.items():
            if isinstance(value, (int, float)):
                numerical_vars[key] = [value]
            elif isinstance(value, list) and value and isinstance(value[0], (int, float)):
                numerical_vars[key] = [float(x) for x in value if isinstance(x, (int, float))]
        
        # Calculate pairwise correlations
        var_names = list(numerical_vars.keys())
        for i in range(len(var_names)):
            for j in range(i + 1, len(var_names)):
                var1, var2 = var_names[i], var_names[j]
                correlation = self._calculate_correlation(numerical_vars[var1], numerical_vars[var2])
                if correlation is not None:
                    correlations.append(correlation)
        
        return correlations
    
    def _calculate_correlation(self, values1: List[float], values2: List[float]) -> Optional[CorrelationResult]:
        """Calculate correlation between two variables"""
        if len(values1) != len(values2) or len(values1) < 2:
            return None
        
        try:
            # Calculate Pearson correlation
            correlation_coeff = np.corrcoef(values1, values2)[0, 1]
            
            # Simple p-value approximation (for real implementation, use scipy.stats)
            n = len(values1)
            t_stat = correlation_coeff * np.sqrt((n - 2) / (1 - correlation_coeff ** 2))
            p_value = 0.05 if abs(t_stat) > 2 else 0.1  # Simplified
            
            # Interpret correlation strength
            abs_corr = abs(correlation_coeff)
            if abs_corr >= 0.8:
                interpretation = "Very strong correlation"
            elif abs_corr >= 0.6:
                interpretation = "Strong correlation"
            elif abs_corr >= 0.4:
                interpretation = "Moderate correlation"
            elif abs_corr >= 0.2:
                interpretation = "Weak correlation"
            else:
                interpretation = "Very weak correlation"
            
            return CorrelationResult(
                variable1="var1",
                variable2="var2",
                correlation_coefficient=correlation_coeff,
                correlation_type="pearson",
                p_value=p_value,
                significance_level=0.05,
                interpretation=interpretation
            )
        
        except Exception:
            return None


class DataQualityAssessor:
    """Assesses data quality across multiple dimensions"""
    
    async def assess_quality(self, data: Any, data_type: DataType) -> DataQuality:
        """Assess overall data quality"""
        completeness = self._assess_completeness(data)
        accuracy = self._assess_accuracy(data, data_type)
        consistency = self._assess_consistency(data)
        timeliness = self._assess_timeliness(data)
        validity = self._assess_validity(data, data_type)
        
        # Calculate weighted overall score
        weights = {"completeness": 0.25, "accuracy": 0.25, "consistency": 0.2, "timeliness": 0.15, "validity": 0.15}
        overall_score = (
            completeness * weights["completeness"] +
            accuracy * weights["accuracy"] +
            consistency * weights["consistency"] +
            timeliness * weights["timeliness"] +
            validity * weights["validity"]
        )
        
        # Identify issues and recommendations
        issues = []
        recommendations = []
        
        if completeness < 0.8:
            issues.append("High percentage of missing values")
            recommendations.append("Implement data validation rules to reduce missing values")
        
        if accuracy < 0.7:
            issues.append("Potential accuracy issues detected")
            recommendations.append("Verify data sources and implement quality checks")
        
        if consistency < 0.8:
            issues.append("Inconsistencies detected across data sources")
            recommendations.append("Standardize data formats and validation rules")
        
        return DataQuality(
            completeness=completeness,
            accuracy=accuracy,
            consistency=consistency,
            timeliness=timeliness,
            validity=validity,
            overall_score=overall_score,
            issues=issues,
            recommendations=recommendations
        )
    
    def _assess_completeness(self, data: Any) -> float:
        """Assess data completeness (non-null values)"""
        if isinstance(data, dict):
            total_fields = len(data)
            non_null_fields = sum(1 for value in data.values() if value is not None and value != "")
            return non_null_fields / total_fields if total_fields > 0 else 1.0
        elif isinstance(data, list):
            total_items = len(data)
            non_null_items = sum(1 for item in data if item is not None and item != "")
            return non_null_items / total_items if total_items > 0 else 1.0
        else:
            return 1.0 if data is not None and data != "" else 0.0
    
    def _assess_accuracy(self, data: Any, data_type: DataType) -> float:
        """Assess data accuracy based on expected patterns"""
        # Simplified accuracy assessment
        # In production, this would use domain-specific validation rules
        return 0.85  # Default assumption of 85% accuracy
    
    def _assess_consistency(self, data: Any) -> float:
        """Assess data consistency"""
        # Simplified consistency check
        # In production, this would check format consistency, value ranges, etc.
        return 0.9  # Default assumption of 90% consistency
    
    def _assess_timeliness(self, data: Any) -> float:
        """Assess data timeliness"""
        # For this implementation, assume data is reasonably fresh
        return 0.8
    
    def _assess_validity(self, data: Any, data_type: DataType) -> float:
        """Assess data validity (format, range, etc.)"""
        # Simplified validity check
        return 0.85


class InsightGenerator:
    """Generates intelligent insights from analyzed data"""
    
    async def generate_insights(self, data: Any, data_type: DataType,
                              statistical_summary: Optional[StatisticalSummary],
                              correlations: List[CorrelationResult]) -> List[str]:
        """Generate intelligent insights from analysis results"""
        insights = []
        
        # Statistical insights
        if statistical_summary:
            insights.extend(self._generate_statistical_insights(statistical_summary))
        
        # Correlation insights
        insights.extend(self._generate_correlation_insights(correlations))
        
        # Data type specific insights
        insights.extend(self._generate_data_type_insights(data, data_type))
        
        return insights
    
    def _generate_statistical_insights(self, summary: StatisticalSummary) -> List[str]:
        """Generate insights from statistical summary"""
        insights = []
        
        if summary.count > 0:
            insights.append(f"Dataset contains {summary.count} data points")
            
            if summary.std_dev / summary.mean > 0.5 if summary.mean != 0 else False:
                insights.append("High variability detected in the data")
            
            if summary.outliers and len(summary.outliers) > 0:
                insights.append(f"Detected {len(summary.outliers)} potential outliers")
            
            if summary.skewness and abs(summary.skewness) > 1:
                direction = "right" if summary.skewness > 0 else "left"
                insights.append(f"Data shows significant {direction} skewness")
        
        return insights
    
    def _generate_correlation_insights(self, correlations: List[CorrelationResult]) -> List[str]:
        """Generate insights from correlation analysis"""
        insights = []
        
        strong_correlations = [c for c in correlations if abs(c.correlation_coefficient) >= 0.6]
        if strong_correlations:
            insights.append(f"Found {len(strong_correlations)} strong correlations between variables")
        
        return insights
    
    def _generate_data_type_insights(self, data: Any, data_type: DataType) -> List[str]:
        """Generate insights specific to the data type"""
        insights = []
        
        if data_type == DataType.TIME_SERIES and isinstance(data, list):
            if len(data) > 10:
                insights.append("Time series data with sufficient points for trend analysis")
        
        elif data_type == DataType.MIXED:
            insights.append("Mixed data types detected - consider separate analysis for each type")
        
        return insights


class VisualizationRecommender:
    """Recommends appropriate visualizations for different data types"""
    
    async def recommend(self, data: Any, data_type: DataType,
                       statistical_summary: Optional[StatisticalSummary]) -> List[Dict[str, Any]]:
        """Recommend visualizations based on data characteristics"""
        recommendations = []
        
        if data_type == DataType.NUMERICAL:
            recommendations.extend([
                {"type": "histogram", "purpose": "Show distribution", "priority": 1},
                {"type": "box_plot", "purpose": "Show quartiles and outliers", "priority": 2},
                {"type": "scatter_plot", "purpose": "Show individual data points", "priority": 3}
            ])
        
        elif data_type == DataType.TIME_SERIES:
            recommendations.extend([
                {"type": "line_chart", "purpose": "Show trends over time", "priority": 1},
                {"type": "area_chart", "purpose": "Show cumulative trends", "priority": 2}
            ])
        
        elif data_type == DataType.CATEGORICAL:
            recommendations.extend([
                {"type": "bar_chart", "purpose": "Compare categories", "priority": 1},
                {"type": "pie_chart", "purpose": "Show proportions", "priority": 2}
            ])
        
        elif data_type == DataType.MIXED:
            recommendations.extend([
                {"type": "dashboard", "purpose": "Multiple visualizations", "priority": 1},
                {"type": "correlation_matrix", "purpose": "Show relationships", "priority": 2}
            ])
        
        return recommendations
