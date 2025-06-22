"""
Real-Time Data Processor - Universal Data Processing Engine
==========================================================

Provides real-time data processing capabilities to transform, clean,
and prepare data from any source for intelligent analysis.

Features:
- Real-time data transformation
- Data cleaning and validation
- Format standardization
- Schema mapping and conversion
- Data enrichment and augmentation
- Performance optimization
- Error handling and recovery
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union
import pandas as pd
import numpy as np
from dataclasses import dataclass

from ...core.config_manager import MassConfig

logger = logging.getLogger(__name__)

@dataclass
class ProcessingResult:
    """Result of data processing"""
    processed_data: Dict[str, Any]
    processing_time: float
    records_processed: int
    errors_encountered: int
    quality_score: float
    metadata: Dict[str, Any]

class RealTimeDataProcessor:
    """
    Real-time data processor for universal data transformation and preparation
    """
    
    def __init__(self, config: MassConfig):
        """Initialize the real-time data processor"""
        self.config = config
        self.processing_rules = {}
        self.transformation_pipelines = {}
        self.performance_metrics = {
            "total_processed": 0,
            "average_processing_time": 0.0,
            "error_rate": 0.0,
            "throughput": 0.0
        }
        self.initialized = False
        
    async def initialize(self) -> bool:
        """Initialize the real-time data processor"""
        try:
            logger.info("Initializing Real-Time Data Processor...")
            
            # Initialize default processing rules
            await self._initialize_default_rules()
            
            # Initialize transformation pipelines
            await self._initialize_pipelines()
            
            self.initialized = True
            logger.info("✅ Real-Time Data Processor initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Real-Time Data Processor: {e}")
            return False
    
    async def process(
        self, 
        raw_data: Dict[str, Any], 
        context: str,
        processing_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process raw data from multiple sources in real-time
        
        Args:
            raw_data: Raw data from various sources
            context: Processing context for optimization
            processing_options: Additional processing options
            
        Returns:
            Processed and standardized data
        """
        start_time = datetime.now()
        
        try:
            logger.info(f"Processing real-time data for context: {context}")
            
            processing_options = processing_options or {}
            
            # Initialize result structure
            processed_data = {
                "sources": {},
                "unified_data": {},
                "metadata": {
                    "context": context,
                    "processing_start": start_time.isoformat(),
                    "sources_processed": list(raw_data.keys())
                }
            }
            
            total_records = 0
            total_errors = 0
            
            # Process each data source
            for source_name, source_data in raw_data.items():
                try:
                    # Process individual source
                    source_result = await self._process_source_data(
                        source_name, source_data, context, processing_options
                    )
                    
                    processed_data["sources"][source_name] = source_result
                    total_records += source_result.get("records_processed", 0)
                    total_errors += source_result.get("errors", 0)
                    
                except Exception as e:
                    logger.error(f"Failed to process source {source_name}: {e}")
                    processed_data["sources"][source_name] = {
                        "error": str(e),
                        "processed": False
                    }
                    total_errors += 1
            
            # Unify and standardize data across sources
            unified_data = await self._unify_data_sources(processed_data["sources"], context)
            processed_data["unified_data"] = unified_data
            
            # Calculate quality score
            quality_score = await self._calculate_quality_score(processed_data, total_records, total_errors)
            
            # Add processing metadata
            processing_time = (datetime.now() - start_time).total_seconds()
            processed_data["metadata"].update({
                "processing_end": datetime.now().isoformat(),
                "processing_time": processing_time,
                "total_records": total_records,
                "total_errors": total_errors,
                "quality_score": quality_score,
                "processor": "real_time_data_processor"
            })
            
            # Update performance metrics
            await self._update_performance_metrics(processing_time, total_records, total_errors)
            
            logger.info(f"✅ Real-time processing completed in {processing_time:.2f}s")
            return processed_data
            
        except Exception as e:
            logger.error(f"Real-time data processing failed: {e}")
            return {
                "error": str(e),
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "context": context
            }
    
    async def process_stream(
        self, 
        data_stream: asyncio.Queue, 
        context: str,
        callback: callable
    ) -> str:
        """Process a continuous data stream"""
        try:
            stream_id = f"stream_{datetime.now().timestamp()}"
            
            # Start stream processing task
            asyncio.create_task(
                self._process_data_stream(stream_id, data_stream, context, callback)
            )
            
            logger.info(f"Started stream processing: {stream_id}")
            return stream_id
            
        except Exception as e:
            logger.error(f"Failed to start stream processing: {e}")
            raise
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            **self.performance_metrics,
            "timestamp": datetime.now().isoformat(),
            "status": "operational" if self.initialized else "not_initialized"
        }
    
    # Private methods for data processing
    
    async def _initialize_default_rules(self) -> None:
        """Initialize default processing rules"""
        try:
            self.processing_rules = {
                "financial": {
                    "required_fields": ["symbol", "price", "timestamp"],
                    "transformations": ["normalize_currency", "validate_price"],
                    "enrichments": ["add_market_context", "calculate_indicators"]
                },
                "social": {
                    "required_fields": ["content", "timestamp", "platform"],
                    "transformations": ["clean_text", "extract_entities"],
                    "enrichments": ["sentiment_analysis", "topic_classification"]
                },
                "iot": {
                    "required_fields": ["sensor_id", "value", "timestamp"],
                    "transformations": ["validate_range", "interpolate_missing"],
                    "enrichments": ["add_location_context", "calculate_trends"]
                },
                "web": {
                    "required_fields": ["url", "content", "timestamp"],
                    "transformations": ["extract_metadata", "clean_html"],
                    "enrichments": ["extract_keywords", "classify_content"]
                },
                "business": {
                    "required_fields": ["id", "timestamp", "record_type"],
                    "transformations": ["standardize_format", "validate_data"],
                    "enrichments": ["calculate_metrics", "add_business_context"]
                }
            }
            
            logger.info("Default processing rules initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize default rules: {e}")
    
    async def _initialize_pipelines(self) -> None:
        """Initialize transformation pipelines"""
        try:
            self.transformation_pipelines = {
                "standardization": self._standardization_pipeline,
                "cleaning": self._cleaning_pipeline,
                "enrichment": self._enrichment_pipeline,
                "validation": self._validation_pipeline
            }
            
            logger.info("Transformation pipelines initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize pipelines: {e}")
    
    async def _process_source_data(
        self, 
        source_name: str, 
        source_data: Dict[str, Any], 
        context: str,
        options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process data from a specific source"""
        try:
            logger.debug(f"Processing source: {source_name}")
            
            # Determine processing rules based on source type
            rules = await self._get_processing_rules(source_name, context)
            
            # Apply transformation pipelines
            processed_records = []
            errors = 0
            
            # Extract records from source data
            records = await self._extract_records(source_data)
            
            for record in records:
                try:
                    # Apply processing pipeline
                    processed_record = await self._apply_processing_pipeline(record, rules)
                    processed_records.append(processed_record)
                    
                except Exception as e:
                    logger.warning(f"Failed to process record: {e}")
                    errors += 1
            
            return {
                "source_name": source_name,
                "records_processed": len(processed_records),
                "errors": errors,
                "processed_records": processed_records,
                "processing_rules_applied": rules,
                "metadata": {
                    "source_type": await self._identify_source_type(source_name),
                    "processing_timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to process source data: {e}")
            return {"error": str(e), "source_name": source_name}
    
    async def _extract_records(self, source_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract individual records from source data"""
        try:
            records = []
            
            # Handle different data structures
            if "readings" in source_data:  # IoT data
                records = source_data["readings"]
            elif "posts" in source_data:  # Social media data
                records = source_data["posts"]
            elif "records" in source_data:  # Business data
                records = source_data["records"]
            elif "content" in source_data:  # Web data
                records = [source_data]  # Single content item
            elif isinstance(source_data, list):
                records = source_data
            elif isinstance(source_data, dict):
                # Try to extract data from common keys
                for key in ["data", "items", "results", "entries"]:
                    if key in source_data and isinstance(source_data[key], list):
                        records = source_data[key]
                        break
                else:
                    # Treat as single record
                    records = [source_data]
            
            return records
            
        except Exception as e:
            logger.error(f"Failed to extract records: {e}")
            return []
    
    async def _get_processing_rules(self, source_name: str, context: str) -> Dict[str, Any]:
        """Get processing rules for a source and context"""
        try:
            # Identify source type
            source_type = await self._identify_source_type(source_name)
            
            # Get rules for source type
            rules = self.processing_rules.get(source_type, {})
            
            # Apply context-specific modifications
            if context == "financial_analysis" and source_type != "financial":
                # Add financial context rules
                rules = {**rules, "add_financial_context": True}
            elif context == "sentiment_analysis" and source_type != "social":
                # Add sentiment analysis rules
                rules = {**rules, "add_sentiment_analysis": True}
            
            return rules
            
        except Exception as e:
            logger.error(f"Failed to get processing rules: {e}")
            return {}
    
    async def _identify_source_type(self, source_name: str) -> str:
        """Identify the type of data source"""
        source_name_lower = source_name.lower()
        
        if any(keyword in source_name_lower for keyword in ["financial", "market", "stock", "crypto"]):
            return "financial"
        elif any(keyword in source_name_lower for keyword in ["social", "twitter", "reddit", "news"]):
            return "social"
        elif any(keyword in source_name_lower for keyword in ["iot", "sensor", "weather", "temperature"]):
            return "iot"
        elif any(keyword in source_name_lower for keyword in ["web", "website", "url", "html"]):
            return "web"
        elif any(keyword in source_name_lower for keyword in ["business", "crm", "erp", "database"]):
            return "business"
        else:
            return "generic"
    
    async def _apply_processing_pipeline(
        self, 
        record: Dict[str, Any], 
        rules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply processing pipeline to a record"""
        try:
            processed_record = record.copy()
            
            # Apply standardization
            processed_record = await self._standardization_pipeline(processed_record, rules)
            
            # Apply cleaning
            processed_record = await self._cleaning_pipeline(processed_record, rules)
            
            # Apply validation
            processed_record = await self._validation_pipeline(processed_record, rules)
            
            # Apply enrichment
            processed_record = await self._enrichment_pipeline(processed_record, rules)
            
            return processed_record
            
        except Exception as e:
            logger.error(f"Failed to apply processing pipeline: {e}")
            return record
    
    async def _standardization_pipeline(
        self, 
        record: Dict[str, Any], 
        rules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Standardize record format and fields"""
        try:
            standardized = record.copy()
            
            # Standardize timestamp field
            if "timestamp" in standardized:
                timestamp = standardized["timestamp"]
                if isinstance(timestamp, str):
                    try:
                        standardized["timestamp"] = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    except ValueError:
                        standardized["timestamp"] = datetime.now()
                elif not isinstance(timestamp, datetime):
                    standardized["timestamp"] = datetime.now()
            else:
                standardized["timestamp"] = datetime.now()
            
            # Standardize common fields
            if "value" in standardized and isinstance(standardized["value"], str):
                try:
                    standardized["value"] = float(standardized["value"])
                except ValueError:
                    pass
            
            # Add processing metadata
            standardized["_processing"] = {
                "standardized_at": datetime.now().isoformat(),
                "pipeline_stage": "standardization"
            }
            
            return standardized
            
        except Exception as e:
            logger.error(f"Standardization pipeline failed: {e}")
            return record
    
    async def _cleaning_pipeline(
        self, 
        record: Dict[str, Any], 
        rules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Clean and normalize record data"""
        try:
            cleaned = record.copy()
            
            # Clean text fields
            for key, value in cleaned.items():
                if isinstance(value, str):
                    # Basic text cleaning
                    cleaned[key] = value.strip()
                    
                    # Remove excessive whitespace
                    if len(value) > 10:  # Only for longer text
                        import re
                        cleaned[key] = re.sub(r'\s+', ' ', cleaned[key])
            
            # Remove null/empty values if specified in rules
            if rules.get("remove_empty", True):
                cleaned = {k: v for k, v in cleaned.items() if v is not None and v != ""}
            
            # Update processing metadata
            if "_processing" in cleaned:
                cleaned["_processing"]["cleaned_at"] = datetime.now().isoformat()
                cleaned["_processing"]["pipeline_stage"] = "cleaning"
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Cleaning pipeline failed: {e}")
            return record
    
    async def _validation_pipeline(
        self, 
        record: Dict[str, Any], 
        rules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Validate record data quality"""
        try:
            validated = record.copy()
            validation_errors = []
            
            # Check required fields
            required_fields = rules.get("required_fields", [])
            for field in required_fields:
                if field not in validated or validated[field] is None:
                    validation_errors.append(f"Missing required field: {field}")
            
            # Validate data types and ranges
            if "value" in validated:
                value = validated["value"]
                if isinstance(value, (int, float)):
                    # Check for reasonable ranges
                    if abs(value) > 1e10:  # Extremely large values
                        validation_errors.append(f"Value out of reasonable range: {value}")
            
            # Add validation results
            validated["_validation"] = {
                "is_valid": len(validation_errors) == 0,
                "errors": validation_errors,
                "validated_at": datetime.now().isoformat()
            }
            
            # Update processing metadata
            if "_processing" in validated:
                validated["_processing"]["validated_at"] = datetime.now().isoformat()
                validated["_processing"]["pipeline_stage"] = "validation"
            
            return validated
            
        except Exception as e:
            logger.error(f"Validation pipeline failed: {e}")
            return record
    
    async def _enrichment_pipeline(
        self, 
        record: Dict[str, Any], 
        rules: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enrich record with additional context and derived fields"""
        try:
            enriched = record.copy()
            
            # Add derived fields based on record type
            if "sensor_type" in enriched and enriched["sensor_type"] == "temperature":
                temp = enriched.get("value", 0)
                if isinstance(temp, (int, float)):
                    enriched["temperature_category"] = self._categorize_temperature(temp)
            
            # Add temporal enrichments
            if "timestamp" in enriched and isinstance(enriched["timestamp"], datetime):
                timestamp = enriched["timestamp"]
                enriched["_temporal"] = {
                    "hour": timestamp.hour,
                    "day_of_week": timestamp.weekday(),
                    "is_weekend": timestamp.weekday() >= 5,
                    "quarter": (timestamp.month - 1) // 3 + 1
                }
            
            # Add quality score
            enriched["_quality_score"] = await self._calculate_record_quality_score(enriched)
            
            # Update processing metadata
            if "_processing" in enriched:
                enriched["_processing"]["enriched_at"] = datetime.now().isoformat()
                enriched["_processing"]["pipeline_stage"] = "enrichment"
            
            return enriched
            
        except Exception as e:
            logger.error(f"Enrichment pipeline failed: {e}")
            return record
    
    def _categorize_temperature(self, temp: float) -> str:
        """Categorize temperature reading"""
        if temp < 0:
            return "freezing"
        elif temp < 10:
            return "cold"
        elif temp < 20:
            return "cool"
        elif temp < 30:
            return "warm"
        else:
            return "hot"
    
    async def _calculate_record_quality_score(self, record: Dict[str, Any]) -> float:
        """Calculate quality score for a record"""
        try:
            score = 1.0
            
            # Check for validation errors
            validation = record.get("_validation", {})
            if not validation.get("is_valid", True):
                score -= 0.3
            
            # Check for required fields
            required_fields = ["timestamp"]
            missing_fields = sum(1 for field in required_fields if field not in record)
            score -= missing_fields * 0.2
            
            # Check data completeness
            total_fields = len([k for k in record.keys() if not k.startswith("_")])
            if total_fields < 3:  # Minimum expected fields
                score -= 0.1
            
            return max(0.0, min(1.0, score))
            
        except Exception as e:
            logger.error(f"Failed to calculate record quality score: {e}")
            return 0.5
    
    async def _unify_data_sources(
        self, 
        processed_sources: Dict[str, Any], 
        context: str
    ) -> Dict[str, Any]:
        """Unify data from multiple sources into a coherent structure"""
        try:
            unified = {
                "records": [],
                "summary": {},
                "by_source": {},
                "unified_timestamp": datetime.now().isoformat()
            }
            
            total_records = 0
            total_quality_score = 0.0
            
            # Combine all records
            for source_name, source_result in processed_sources.items():
                if "processed_records" in source_result:
                    records = source_result["processed_records"]
                    unified["records"].extend(records)
                    
                    # Calculate source summary
                    source_summary = {
                        "record_count": len(records),
                        "average_quality": 0.0
                    }
                    
                    if records:
                        quality_scores = [r.get("_quality_score", 0.5) for r in records]
                        source_summary["average_quality"] = sum(quality_scores) / len(quality_scores)
                        total_quality_score += sum(quality_scores)
                    
                    unified["by_source"][source_name] = source_summary
                    total_records += len(records)
            
            # Create overall summary
            unified["summary"] = {
                "total_records": total_records,
                "total_sources": len(processed_sources),
                "average_quality_score": total_quality_score / max(1, total_records),
                "processing_context": context
            }
            
            # Sort records by timestamp
            unified["records"].sort(
                key=lambda x: x.get("timestamp", datetime.min),
                reverse=True
            )
            
            return unified
            
        except Exception as e:
            logger.error(f"Failed to unify data sources: {e}")
            return {"error": str(e)}
    
    async def _calculate_quality_score(
        self, 
        processed_data: Dict[str, Any], 
        total_records: int, 
        total_errors: int
    ) -> float:
        """Calculate overall processing quality score"""
        try:
            if total_records == 0:
                return 0.0
            
            # Base score on error rate
            error_rate = total_errors / max(1, total_records + total_errors)
            base_score = 1.0 - error_rate
            
            # Factor in individual record quality scores
            unified_data = processed_data.get("unified_data", {})
            records = unified_data.get("records", [])
            
            if records:
                record_quality_scores = [r.get("_quality_score", 0.5) for r in records]
                avg_record_quality = sum(record_quality_scores) / len(record_quality_scores)
                
                # Weighted combination
                quality_score = (base_score * 0.6) + (avg_record_quality * 0.4)
            else:
                quality_score = base_score
            
            return max(0.0, min(1.0, quality_score))
            
        except Exception as e:
            logger.error(f"Failed to calculate quality score: {e}")
            return 0.5
    
    async def _update_performance_metrics(
        self, 
        processing_time: float, 
        records_processed: int, 
        errors: int
    ) -> None:
        """Update performance metrics"""
        try:
            self.performance_metrics["total_processed"] += records_processed
            
            # Update average processing time
            current_avg = self.performance_metrics["average_processing_time"]
            total_operations = self.performance_metrics.get("operations_count", 0) + 1
            new_avg = ((current_avg * (total_operations - 1)) + processing_time) / total_operations
            self.performance_metrics["average_processing_time"] = new_avg
            self.performance_metrics["operations_count"] = total_operations
            
            # Update error rate
            total_records = self.performance_metrics["total_processed"]
            total_errors = self.performance_metrics.get("total_errors", 0) + errors
            self.performance_metrics["total_errors"] = total_errors
            self.performance_metrics["error_rate"] = total_errors / max(1, total_records)
            
            # Update throughput (records per second)
            self.performance_metrics["throughput"] = records_processed / max(0.001, processing_time)
            
        except Exception as e:
            logger.error(f"Failed to update performance metrics: {e}")
    
    async def _process_data_stream(
        self, 
        stream_id: str, 
        data_stream: asyncio.Queue, 
        context: str,
        callback: callable
    ) -> None:
        """Process continuous data stream"""
        try:
            logger.info(f"Processing data stream: {stream_id}")
            
            while True:
                try:
                    # Get data from stream (with timeout)
                    data_batch = await asyncio.wait_for(data_stream.get(), timeout=30.0)
                    
                    # Process the batch
                    processed_data = await self.process(data_batch, context)
                    
                    # Call callback with processed data
                    try:
                        callback(stream_id, processed_data)
                    except Exception as e:
                        logger.error(f"Stream callback failed for {stream_id}: {e}")
                    
                except asyncio.TimeoutError:
                    # No data in queue, continue monitoring
                    continue
                except Exception as e:
                    logger.error(f"Stream processing error for {stream_id}: {e}")
                    await asyncio.sleep(5)  # Brief pause before continuing
                    
        except Exception as e:
            logger.error(f"Data stream processing failed for {stream_id}: {e}")
    
    async def close(self) -> None:
        """Close the real-time data processor"""
        try:
            self.initialized = False
            logger.info("Real-Time Data Processor closed")
        except Exception as e:
            logger.error(f"Error closing real-time data processor: {e}")
