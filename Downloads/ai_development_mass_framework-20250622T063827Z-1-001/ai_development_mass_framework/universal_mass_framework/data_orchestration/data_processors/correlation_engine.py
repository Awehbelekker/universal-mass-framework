"""
Universal MASS Framework - Correlation Engine
===========================================

Advanced cross-source data correlation analysis for the Universal MASS Framework.
This engine identifies relationships, patterns, and correlations across multiple
data sources to generate unified intelligence.

Key Features:
- Multi-source correlation analysis
- Real-time correlation detection
- Statistical correlation algorithms
- Causal relationship identification
- Cross-domain pattern correlation
- Temporal correlation analysis
"""

import asyncio
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import statistics
import json
from scipy.stats import pearsonr, spearmanr
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

logger = logging.getLogger(__name__)


class CorrelationType(Enum):
    """Types of correlations that can be detected"""
    STATISTICAL = "statistical"
    TEMPORAL = "temporal"
    CAUSAL = "causal"
    SEMANTIC = "semantic"
    BEHAVIORAL = "behavioral"
    MARKET = "market"
    OPERATIONAL = "operational"


class CorrelationStrength(Enum):
    """Strength levels for correlations"""
    WEAK = "weak"          # 0.0 - 0.3
    MODERATE = "moderate"  # 0.3 - 0.7
    STRONG = "strong"      # 0.7 - 0.9
    VERY_STRONG = "very_strong"  # 0.9 - 1.0


@dataclass
class CorrelationResult:
    """Result of correlation analysis between data sources"""
    correlation_id: str
    source_a: str
    source_b: str
    correlation_type: CorrelationType
    strength: CorrelationStrength
    coefficient: float
    confidence: float
    significance: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "correlation_id": self.correlation_id,
            "source_a": self.source_a,
            "source_b": self.source_b,
            "correlation_type": self.correlation_type.value,
            "strength": self.strength.value,
            "coefficient": self.coefficient,
            "confidence": self.confidence,
            "significance": self.significance,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class CorrelationPattern:
    """Pattern identified across multiple correlations"""
    pattern_id: str
    pattern_type: str
    correlations: List[CorrelationResult]
    strength: float
    confidence: float
    description: str
    implications: List[str]
    recommendations: List[str]


class DataCorrelationEngine:
    """
    Universal Data Correlation Engine
    
    CAPABILITIES:
    - Cross-source statistical correlation analysis
    - Temporal pattern correlation detection
    - Causal relationship identification
    - Real-time correlation monitoring
    - Multi-dimensional correlation analysis
    - Correlation-based predictions
    """
    
    def __init__(self, config=None):
        """Initialize the correlation engine"""
        self.config = config
        self.correlation_cache = {}
        self.correlation_history = []
        self.correlation_patterns = {}
        self.correlation_thresholds = {
            CorrelationStrength.WEAK: 0.3,
            CorrelationStrength.MODERATE: 0.7,
            CorrelationStrength.STRONG: 0.9,
            CorrelationStrength.VERY_STRONG: 1.0
        }
        
        # Performance metrics
        self.processing_stats = {
            "correlations_processed": 0,
            "patterns_detected": 0,
            "avg_processing_time": 0.0,
            "cache_hit_rate": 0.0
        }
    
    async def find_correlations(self, data_sets: Dict[str, List[Dict[str, Any]]], 
                              context: Dict[str, Any] = None) -> List[CorrelationResult]:
        """
        Find correlations between multiple data sources
        
        Args:
            data_sets: Dictionary of data sources and their data
            context: Analysis context and parameters
            
        Returns:
            List of correlation results
        """
        start_time = datetime.utcnow()
        
        try:
            correlations = []
            data_source_names = list(data_sets.keys())
            
            # Analyze correlations between all pairs of data sources
            for i in range(len(data_source_names)):
                for j in range(i + 1, len(data_source_names)):
                    source_a = data_source_names[i]
                    source_b = data_source_names[j]
                    
                    # Get correlation from cache if available
                    cache_key = f"{source_a}_{source_b}_{hash(str(context))}"
                    if cache_key in self.correlation_cache:
                        cached_result = self.correlation_cache[cache_key]
                        if (datetime.utcnow() - cached_result['timestamp']).seconds < 300:  # 5 min cache
                            correlations.append(cached_result['correlation'])
                            continue
                    
                    # Perform correlation analysis
                    correlation = await self._analyze_correlation(
                        source_a, data_sets[source_a],
                        source_b, data_sets[source_b],
                        context
                    )
                    
                    if correlation:
                        correlations.append(correlation)
                        
                        # Cache the result
                        self.correlation_cache[cache_key] = {
                            'correlation': correlation,
                            'timestamp': datetime.utcnow()
                        }
            
            # Detect correlation patterns
            patterns = await self._detect_correlation_patterns(correlations, context)
            
            # Update statistics
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            self._update_processing_stats(len(correlations), processing_time)
            
            logger.info(f"Found {len(correlations)} correlations across {len(data_source_names)} data sources")
            
            return correlations
            
        except Exception as e:
            logger.error(f"Error finding correlations: {str(e)}")
            return []
    
    async def _analyze_correlation(self, source_a: str, data_a: List[Dict[str, Any]],
                                 source_b: str, data_b: List[Dict[str, Any]],
                                 context: Dict[str, Any] = None) -> Optional[CorrelationResult]:
        """
        Analyze correlation between two data sources
        """
        try:
            # Statistical correlation analysis
            statistical_corr = await self._calculate_statistical_correlation(data_a, data_b)
            
            # Temporal correlation analysis
            temporal_corr = await self._calculate_temporal_correlation(data_a, data_b)
            
            # Semantic correlation analysis
            semantic_corr = await self._calculate_semantic_correlation(data_a, data_b)
            
            # Determine the strongest correlation
            correlations = [
                (CorrelationType.STATISTICAL, statistical_corr),
                (CorrelationType.TEMPORAL, temporal_corr),
                (CorrelationType.SEMANTIC, semantic_corr)
            ]
            
            # Select the strongest significant correlation
            best_correlation = max(correlations, key=lambda x: abs(x[1]['coefficient']) if x[1] else 0)
            
            if best_correlation[1] and abs(best_correlation[1]['coefficient']) > 0.1:
                correlation_type, corr_data = best_correlation
                
                return CorrelationResult(
                    correlation_id=f"corr_{source_a}_{source_b}_{int(datetime.utcnow().timestamp())}",
                    source_a=source_a,
                    source_b=source_b,
                    correlation_type=correlation_type,
                    strength=self._determine_correlation_strength(abs(corr_data['coefficient'])),
                    coefficient=corr_data['coefficient'],
                    confidence=corr_data['confidence'],
                    significance=corr_data['significance'],
                    metadata={
                        'data_points_a': len(data_a),
                        'data_points_b': len(data_b),
                        'analysis_method': corr_data.get('method', 'unknown'),
                        'context': context
                    }
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error analyzing correlation between {source_a} and {source_b}: {str(e)}")
            return None
    
    async def _calculate_statistical_correlation(self, data_a: List[Dict[str, Any]], 
                                               data_b: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Calculate statistical correlation between two datasets
        """
        try:
            # Extract numerical features
            numeric_a = self._extract_numeric_features(data_a)
            numeric_b = self._extract_numeric_features(data_b)
            
            if not numeric_a or not numeric_b:
                return None
            
            # Align data by timestamp if available
            aligned_a, aligned_b = self._align_data_by_time(numeric_a, numeric_b)
            
            if len(aligned_a) < 3 or len(aligned_b) < 3:
                return None
            
            # Calculate Pearson correlation
            correlation, p_value = pearsonr(aligned_a, aligned_b)
            
            # Calculate confidence based on sample size and p-value
            confidence = min(0.95, 1.0 - p_value) if p_value < 0.05 else 0.0
            
            return {
                'coefficient': correlation,
                'confidence': confidence,
                'significance': 1.0 - p_value,
                'method': 'pearson',
                'sample_size': len(aligned_a)
            }
            
        except Exception as e:
            logger.error(f"Error calculating statistical correlation: {str(e)}")
            return None
    
    async def _calculate_temporal_correlation(self, data_a: List[Dict[str, Any]], 
                                            data_b: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Calculate temporal correlation with lag analysis
        """
        try:
            # Extract time series data
            ts_a = self._extract_time_series(data_a)
            ts_b = self._extract_time_series(data_b)
            
            if not ts_a or not ts_b:
                return None
            
            # Convert to pandas series for easier manipulation
            series_a = pd.Series([point['value'] for point in ts_a], 
                               index=[point['timestamp'] for point in ts_a])
            series_b = pd.Series([point['value'] for point in ts_b], 
                               index=[point['timestamp'] for point in ts_b])
            
            # Resample to common frequency
            common_index = pd.date_range(
                start=max(series_a.index.min(), series_b.index.min()),
                end=min(series_a.index.max(), series_b.index.max()),
                freq='H'  # Hourly frequency
            )
            
            series_a_resampled = series_a.reindex(common_index, method='nearest')
            series_b_resampled = series_b.reindex(common_index, method='nearest')
            
            # Remove NaN values
            valid_mask = series_a_resampled.notna() & series_b_resampled.notna()
            series_a_clean = series_a_resampled[valid_mask]
            series_b_clean = series_b_resampled[valid_mask]
            
            if len(series_a_clean) < 3:
                return None
            
            # Calculate cross-correlation
            correlation = series_a_clean.corr(series_b_clean)
            
            # Calculate lagged correlations
            max_lag = min(24, len(series_a_clean) // 4)  # Up to 24 hours or 1/4 of data
            lag_correlations = []
            
            for lag in range(-max_lag, max_lag + 1):
                if lag == 0:
                    continue
                    
                if lag > 0:
                    lagged_corr = series_a_clean[:-lag].corr(series_b_clean[lag:])
                else:
                    lagged_corr = series_a_clean[-lag:].corr(series_b_clean[:lag])
                
                if not np.isnan(lagged_corr):
                    lag_correlations.append((lag, lagged_corr))
            
            # Find best lag correlation
            if lag_correlations:
                best_lag, best_lag_corr = max(lag_correlations, key=lambda x: abs(x[1]))
                if abs(best_lag_corr) > abs(correlation):
                    correlation = best_lag_corr
            
            # Calculate confidence based on data quality
            confidence = min(0.9, len(series_a_clean) / 100) if abs(correlation) > 0.1 else 0.0
            
            return {
                'coefficient': correlation,
                'confidence': confidence,
                'significance': min(0.95, abs(correlation)),
                'method': 'temporal_cross_correlation',
                'best_lag': best_lag if 'best_lag' in locals() else 0,
                'sample_size': len(series_a_clean)
            }
            
        except Exception as e:
            logger.error(f"Error calculating temporal correlation: {str(e)}")
            return None
    
    async def _calculate_semantic_correlation(self, data_a: List[Dict[str, Any]], 
                                            data_b: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Calculate semantic correlation based on content similarity
        """
        try:
            # Extract textual content
            text_a = self._extract_text_content(data_a)
            text_b = self._extract_text_content(data_b)
            
            if not text_a or not text_b:
                return None
            
            # Simple semantic similarity using keyword overlap
            keywords_a = self._extract_keywords(text_a)
            keywords_b = self._extract_keywords(text_b)
            
            if not keywords_a or not keywords_b:
                return None
            
            # Calculate Jaccard similarity
            intersection = len(keywords_a.intersection(keywords_b))
            union = len(keywords_a.union(keywords_b))
            
            if union == 0:
                return None
            
            jaccard_similarity = intersection / union
            
            # Convert to correlation-like metric
            correlation = (jaccard_similarity - 0.5) * 2  # Scale from [-1, 1]
            
            # Calculate confidence based on content volume
            confidence = min(0.8, (len(keywords_a) + len(keywords_b)) / 200)
            
            return {
                'coefficient': correlation,
                'confidence': confidence,
                'significance': min(0.9, jaccard_similarity),
                'method': 'semantic_jaccard',
                'keyword_overlap': intersection,
                'total_keywords': union
            }
            
        except Exception as e:
            logger.error(f"Error calculating semantic correlation: {str(e)}")
            return None
    
    def _extract_numeric_features(self, data: List[Dict[str, Any]]) -> List[float]:
        """Extract numeric features from data"""
        numeric_values = []
        
        for item in data:
            for key, value in item.items():
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    numeric_values.append(float(value))
                elif isinstance(value, str) and value.replace('.', '').replace('-', '').isdigit():
                    try:
                        numeric_values.append(float(value))
                    except ValueError:
                        continue
        
        return numeric_values[:100]  # Limit to prevent memory issues
    
    def _extract_time_series(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract time series data points"""
        time_series = []
        
        for item in data:
            timestamp = None
            value = None
            
            # Look for timestamp fields
            for ts_field in ['timestamp', 'time', 'date', 'created_at', 'updated_at']:
                if ts_field in item:
                    try:
                        if isinstance(item[ts_field], str):
                            timestamp = pd.to_datetime(item[ts_field])
                        elif isinstance(item[ts_field], (int, float)):
                            timestamp = pd.to_datetime(item[ts_field], unit='s')
                        else:
                            timestamp = item[ts_field]
                        break
                    except:
                        continue
            
            # Look for numeric value fields
            for val_field in ['value', 'price', 'count', 'volume', 'amount', 'score']:
                if val_field in item and isinstance(item[val_field], (int, float)):
                    value = float(item[val_field])
                    break
            
            if timestamp and value is not None:
                time_series.append({
                    'timestamp': timestamp,
                    'value': value
                })
        
        return sorted(time_series, key=lambda x: x['timestamp'])
    
    def _extract_text_content(self, data: List[Dict[str, Any]]) -> str:
        """Extract textual content from data"""
        text_content = []
        
        for item in data:
            for key, value in item.items():
                if isinstance(value, str) and len(value) > 3:
                    text_content.append(value.lower())
        
        return ' '.join(text_content)
    
    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract keywords from text"""
        # Simple keyword extraction (in production, use NLP libraries)
        words = text.replace(',', ' ').replace('.', ' ').split()
        keywords = set()
        
        for word in words:
            word = word.strip().lower()
            if len(word) > 3 and word.isalpha():
                keywords.add(word)
        
        # Remove common stop words
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'this', 'that', 'these', 'those'}
        keywords = keywords - stop_words
        
        return keywords
    
    def _align_data_by_time(self, data_a: List[float], data_b: List[float]) -> Tuple[List[float], List[float]]:
        """Align two datasets by taking equal-length samples"""
        min_length = min(len(data_a), len(data_b))
        
        if min_length == 0:
            return [], []
        
        # Take samples from the middle to avoid edge effects
        start_a = max(0, (len(data_a) - min_length) // 2)
        start_b = max(0, (len(data_b) - min_length) // 2)
        
        aligned_a = data_a[start_a:start_a + min_length]
        aligned_b = data_b[start_b:start_b + min_length]
        
        return aligned_a, aligned_b
    
    def _determine_correlation_strength(self, coefficient: float) -> CorrelationStrength:
        """Determine correlation strength from coefficient"""
        abs_coeff = abs(coefficient)
        
        if abs_coeff >= 0.9:
            return CorrelationStrength.VERY_STRONG
        elif abs_coeff >= 0.7:
            return CorrelationStrength.STRONG
        elif abs_coeff >= 0.3:
            return CorrelationStrength.MODERATE
        else:
            return CorrelationStrength.WEAK
    
    async def _detect_correlation_patterns(self, correlations: List[CorrelationResult], 
                                         context: Dict[str, Any] = None) -> List[CorrelationPattern]:
        """
        Detect patterns across multiple correlations
        """
        try:
            patterns = []
            
            # Group correlations by strength
            strong_correlations = [c for c in correlations if c.strength in [CorrelationStrength.STRONG, CorrelationStrength.VERY_STRONG]]
            
            if len(strong_correlations) >= 2:
                # Multi-source convergence pattern
                convergence_pattern = CorrelationPattern(
                    pattern_id=f"convergence_{int(datetime.utcnow().timestamp())}",
                    pattern_type="multi_source_convergence",
                    correlations=strong_correlations,
                    strength=sum(abs(c.coefficient) for c in strong_correlations) / len(strong_correlations),
                    confidence=min(c.confidence for c in strong_correlations),
                    description=f"Strong correlations detected across {len(strong_correlations)} data source pairs",
                    implications=[
                        "Multiple data sources are moving in similar patterns",
                        "High likelihood of common underlying factors",
                        "Increased confidence in trend predictions"
                    ],
                    recommendations=[
                        "Monitor these sources for early trend detection",
                        "Use correlation for predictive modeling",
                        "Consider these sources as leading indicators"
                    ]
                )
                patterns.append(convergence_pattern)
            
            # Temporal cascade pattern
            temporal_correlations = [c for c in correlations if c.correlation_type == CorrelationType.TEMPORAL]
            if len(temporal_correlations) >= 2:
                temporal_pattern = CorrelationPattern(
                    pattern_id=f"temporal_{int(datetime.utcnow().timestamp())}",
                    pattern_type="temporal_cascade",
                    correlations=temporal_correlations,
                    strength=sum(abs(c.coefficient) for c in temporal_correlations) / len(temporal_correlations),
                    confidence=sum(c.confidence for c in temporal_correlations) / len(temporal_correlations),
                    description="Temporal correlations indicating cause-effect relationships",
                    implications=[
                        "Time-lagged relationships between data sources",
                        "Potential predictive indicators identified",
                        "Sequential dependency patterns detected"
                    ],
                    recommendations=[
                        "Use leading indicators for forecasting",
                        "Implement early warning systems",
                        "Monitor for cascade effects"
                    ]
                )
                patterns.append(temporal_pattern)
            
            logger.info(f"Detected {len(patterns)} correlation patterns")
            return patterns
            
        except Exception as e:
            logger.error(f"Error detecting correlation patterns: {str(e)}")
            return []
    
    def _update_processing_stats(self, num_correlations: int, processing_time: float):
        """Update processing statistics"""
        self.processing_stats["correlations_processed"] += num_correlations
        
        # Update average processing time
        prev_avg = self.processing_stats["avg_processing_time"]
        total_processed = self.processing_stats["correlations_processed"]
        
        if total_processed > 0:
            self.processing_stats["avg_processing_time"] = (
                (prev_avg * (total_processed - num_correlations)) + processing_time
            ) / total_processed
    
    async def get_correlation_summary(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """
        Get summary of recent correlations
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=time_window_hours)
        recent_correlations = [
            corr for corr in self.correlation_history 
            if corr.timestamp >= cutoff_time
        ]
        
        if not recent_correlations:
            return {
                "summary": "No recent correlations found",
                "time_window_hours": time_window_hours,
                "total_correlations": 0
            }
        
        # Calculate summary statistics
        strengths = [corr.strength.value for corr in recent_correlations]
        coefficients = [abs(corr.coefficient) for corr in recent_correlations]
        
        summary = {
            "time_window_hours": time_window_hours,
            "total_correlations": len(recent_correlations),
            "strength_distribution": {
                strength.value: strengths.count(strength.value) 
                for strength in CorrelationStrength
            },
            "average_coefficient": sum(coefficients) / len(coefficients),
            "max_coefficient": max(coefficients),
            "correlation_types": {
                corr_type.value: len([c for c in recent_correlations if c.correlation_type == corr_type])
                for corr_type in CorrelationType
            },
            "processing_stats": self.processing_stats.copy()
        }
        
        return summary
    
    async def get_top_correlations(self, limit: int = 10, 
                                 min_strength: CorrelationStrength = CorrelationStrength.MODERATE) -> List[Dict[str, Any]]:
        """
        Get top correlations by strength
        """
        # Filter by minimum strength
        filtered_correlations = [
            corr for corr in self.correlation_history 
            if self._correlation_strength_value(corr.strength) >= self._correlation_strength_value(min_strength)
        ]
        
        # Sort by coefficient strength
        sorted_correlations = sorted(
            filtered_correlations, 
            key=lambda x: abs(x.coefficient), 
            reverse=True
        )
        
        return [corr.to_dict() for corr in sorted_correlations[:limit]]
    
    def _correlation_strength_value(self, strength: CorrelationStrength) -> float:
        """Convert correlation strength to numeric value for comparison"""
        strength_values = {
            CorrelationStrength.WEAK: 0.1,
            CorrelationStrength.MODERATE: 0.3,
            CorrelationStrength.STRONG: 0.7,
            CorrelationStrength.VERY_STRONG: 0.9
        }
        return strength_values.get(strength, 0.0)


# Export the main class
__all__ = ['DataCorrelationEngine', 'CorrelationResult', 'CorrelationPattern', 'CorrelationType', 'CorrelationStrength']
