"""
Data Sources Module - Universal Data Integration
==============================================

This module provides universal data source integration capabilities
for the MASS Framework, enabling real-world data intelligence from
ANY data source.

Supported Data Sources:
- Financial Markets (stocks, forex, crypto, commodities)
- Social Media Intelligence (Twitter, Reddit, News, Sentiment)
- IoT and Sensor Data (temperature, GPS, industrial sensors)
- Web Content (websites, APIs, feeds)
- Business Systems (CRM, ERP, databases)
- Government Data (economic indicators, regulations)
- Academic Research (papers, studies, datasets)
- News and Media Feeds
- Custom Data Sources (user-defined adapters)

Each data source provides:
- Real-time data streaming
- Historical data access
- Data quality validation
- Automatic error handling
- Rate limiting and compliance
- Security and privacy controls
"""

from .financial_sources import FinancialDataSources
from .social_sources import SocialMediaSources
from .iot_sources import IoTDataSources
from .web_sources import WebDataSources
from .business_sources import BusinessDataSources
from .government_sources import GovernmentDataSources
from .news_sources import NewsDataSources
from .custom_sources import CustomDataSources

__all__ = [
    'FinancialDataSources',
    'SocialMediaSources',
    'IoTDataSources',
    'WebDataSources',
    'BusinessDataSources',
    'GovernmentDataSources',
    'NewsDataSources',
    'CustomDataSources'
]
