"""
🚨 REAL-TIME ALERTING AND MONITORING SYSTEM
Production-grade alerting for MASS Framework

This module provides comprehensive real-time alerting including:
- Security incident alerts
- System performance alerts
- Trading anomaly detection
- Infrastructure health monitoring
- Automated incident response
- Multi-channel notifications
"""

import asyncio
import logging
import json
import time
import os
import smtplib
import requests
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import uuid
from pathlib import Path
import aiohttp
import websockets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configure alerting logger
alert_logger = logging.getLogger("monitoring.alerts")
alert_logger.setLevel(logging.INFO)

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class AlertCategory(Enum):
    """Alert categories"""
    SECURITY = "security"
    PERFORMANCE = "performance"
    TRADING = "trading"
    INFRASTRUCTURE = "infrastructure"
    DATABASE = "database"
    NETWORK = "network"
    AI_SYSTEM = "ai_system"
    USER_ACTIVITY = "user_activity"

class NotificationChannel(Enum):
    """Notification channels"""
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"
    DASHBOARD = "dashboard"
    PAGERDUTY = "pagerduty"

@dataclass
class Alert:
    """Alert record"""
    alert_id: str
    timestamp: datetime
    severity: AlertSeverity
    category: AlertCategory
    title: str
    message: str
    source: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved: bool = False
    resolved_at: Optional[datetime] = None
    notification_sent: bool = False

@dataclass
class AlertRule:
    """Alert rule configuration"""
    rule_id: str
    name: str
    description: str
    condition: str
    severity: AlertSeverity
    category: AlertCategory
    enabled: bool = True
    threshold: Optional[float] = None
    time_window_seconds: int = 300
    notification_channels: List[NotificationChannel] = field(default_factory=list)
    auto_resolve: bool = False
    auto_resolve_after_hours: int = 24

class EmailNotifier:
    """Email notification service"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.smtp_server = config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = config.get('smtp_port', 587)
        self.username = config.get('username')
        self.password = config.get('password')
        self.from_email = config.get('from_email')
        self.to_emails = config.get('to_emails', [])
        
    async def send_alert(self, alert: Alert) -> bool:
        """Send alert via email"""
        try:
            if not all([self.username, self.password, self.from_email, self.to_emails]):
                alert_logger.warning("Email configuration incomplete")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = ', '.join(self.to_emails)
            msg['Subject'] = f"[{alert.severity.value.upper()}] {alert.title}"
            
            # Create HTML body
            html_body = self._create_alert_html(alert)
            msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            alert_logger.info(f"Alert email sent: {alert.alert_id}")
            return True
            
        except Exception as e:
            alert_logger.error(f"Failed to send email alert: {e}")
            return False
    
    def _create_alert_html(self, alert: Alert) -> str:
        """Create HTML email body"""
        severity_colors = {
            AlertSeverity.INFO: "#3498db",
            AlertSeverity.WARNING: "#f39c12",
            AlertSeverity.ERROR: "#e74c3c",
            AlertSeverity.CRITICAL: "#8e44ad"
        }
        
        color = severity_colors.get(alert.severity, "#95a5a6")
        
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .alert {{ border-left: 4px solid {color}; padding: 15px; margin: 10px 0; background-color: #f8f9fa; }}
                .severity {{ font-weight: bold; color: {color}; }}
                .timestamp {{ color: #666; font-size: 12px; }}
                .metadata {{ background-color: #fff; padding: 10px; margin: 10px 0; border-radius: 4px; }}
            </style>
        </head>
        <body>
            <div class="alert">
                <div class="severity">{alert.severity.value.upper()}</div>
                <h2>{alert.title}</h2>
                <p>{alert.message}</p>
                <div class="timestamp">Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}</div>
                <div class="timestamp">Source: {alert.source}</div>
                <div class="metadata">
                    <strong>Metadata:</strong><br>
                    <pre>{json.dumps(alert.metadata, indent=2)}</pre>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

class SlackNotifier:
    """Slack notification service"""
    
    def __init__(self, config: Dict[str, Any]):
        self.webhook_url = config.get('webhook_url')
        self.channel = config.get('channel', '#alerts')
        self.username = config.get('username', 'MASS Framework Alerts')
        
    async def send_alert(self, alert: Alert) -> bool:
        """Send alert via Slack"""
        try:
            if not self.webhook_url:
                alert_logger.warning("Slack webhook URL not configured")
                return False
            
            # Create Slack message
            severity_emoji = {
                AlertSeverity.INFO: ":information_source:",
                AlertSeverity.WARNING: ":warning:",
                AlertSeverity.ERROR: ":x:",
                AlertSeverity.CRITICAL: ":rotating_light:"
            }
            
            emoji = severity_emoji.get(alert.severity, ":bell:")
            
            payload = {
                "channel": self.channel,
                "username": self.username,
                "text": f"{emoji} *{alert.severity.value.upper()}: {alert.title}*",
                "attachments": [
                    {
                        "color": self._get_severity_color(alert.severity),
                        "fields": [
                            {
                                "title": "Message",
                                "value": alert.message,
                                "short": False
                            },
                            {
                                "title": "Source",
                                "value": alert.source,
                                "short": True
                            },
                            {
                                "title": "Time",
                                "value": alert.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC'),
                                "short": True
                            }
                        ],
                        "footer": "MASS Framework Alerting System"
                    }
                ]
            }
            
            # Add metadata if present
            if alert.metadata:
                metadata_text = "\n".join([f"• {k}: {v}" for k, v in alert.metadata.items()])
                payload["attachments"][0]["fields"].append({
                    "title": "Details",
                    "value": metadata_text,
                    "short": False
                })
            
            # Send to Slack
            async with aiohttp.ClientSession() as session:
                async with session.post(self.webhook_url, json=payload) as response:
                    if response.status == 200:
                        alert_logger.info(f"Slack alert sent: {alert.alert_id}")
                        return True
                    else:
                        alert_logger.error(f"Slack API error: {response.status}")
                        return False
                        
        except Exception as e:
            alert_logger.error(f"Failed to send Slack alert: {e}")
            return False
    
    def _get_severity_color(self, severity: AlertSeverity) -> str:
        """Get color for severity level"""
        colors = {
            AlertSeverity.INFO: "#3498db",
            AlertSeverity.WARNING: "#f39c12",
            AlertSeverity.ERROR: "#e74c3c",
            AlertSeverity.CRITICAL: "#8e44ad"
        }
        return colors.get(severity, "#95a5a6")

class WebhookNotifier:
    """Generic webhook notification service"""
    
    def __init__(self, config: Dict[str, Any]):
        self.webhook_url = config.get('webhook_url')
        self.headers = config.get('headers', {'Content-Type': 'application/json'})
        self.timeout = config.get('timeout', 10)
        
    async def send_alert(self, alert: Alert) -> bool:
        """Send alert via webhook"""
        try:
            if not self.webhook_url:
                alert_logger.warning("Webhook URL not configured")
                return False
            
            # Prepare payload
            payload = {
                "alert_id": alert.alert_id,
                "timestamp": alert.timestamp.isoformat(),
                "severity": alert.severity.value,
                "category": alert.category.value,
                "title": alert.title,
                "message": alert.message,
                "source": alert.source,
                "metadata": alert.metadata
            }
            
            # Send webhook
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json=payload,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    if response.status in [200, 201, 202]:
                        alert_logger.info(f"Webhook alert sent: {alert.alert_id}")
                        return True
                    else:
                        alert_logger.error(f"Webhook error: {response.status}")
                        return False
                        
        except Exception as e:
            alert_logger.error(f"Failed to send webhook alert: {e}")
            return False

class RealTimeAlertingSystem:
    """Real-time alerting and monitoring system"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.alerts: List[Alert] = []
        self.alert_rules: Dict[str, AlertRule] = {}
        self.notifiers: Dict[NotificationChannel, Any] = {}
        self.monitoring_active = False
        self.monitoring_task = None
        
        # Initialize notifiers
        self._initialize_notifiers()
        
        # Load default alert rules
        self._load_default_alert_rules()
        
        alert_logger.info("Real-time alerting system initialized")
    
    def _initialize_notifiers(self):
        """Initialize notification channels"""
        try:
            # Email notifier
            if self.config.get('email'):
                self.notifiers[NotificationChannel.EMAIL] = EmailNotifier(self.config['email'])
            
            # Slack notifier
            if self.config.get('slack'):
                self.notifiers[NotificationChannel.SLACK] = SlackNotifier(self.config['slack'])
            
            # Webhook notifier
            if self.config.get('webhook'):
                self.notifiers[NotificationChannel.WEBHOOK] = WebhookNotifier(self.config['webhook'])
                
        except Exception as e:
            alert_logger.error(f"Failed to initialize notifiers: {e}")
    
    def _load_default_alert_rules(self):
        """Load default alert rules"""
        default_rules = [
            AlertRule(
                rule_id="high_cpu_usage",
                name="High CPU Usage",
                description="Alert when CPU usage exceeds 80%",
                condition="cpu_usage > 80",
                severity=AlertSeverity.WARNING,
                category=AlertCategory.PERFORMANCE,
                threshold=80.0,
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK]
            ),
            AlertRule(
                rule_id="high_memory_usage",
                name="High Memory Usage",
                description="Alert when memory usage exceeds 85%",
                condition="memory_usage > 85",
                severity=AlertSeverity.WARNING,
                category=AlertCategory.PERFORMANCE,
                threshold=85.0,
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK]
            ),
            AlertRule(
                rule_id="database_connection_failure",
                name="Database Connection Failure",
                description="Alert when database connection fails",
                condition="database_status == 'failed'",
                severity=AlertSeverity.CRITICAL,
                category=AlertCategory.DATABASE,
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK, NotificationChannel.WEBHOOK]
            ),
            AlertRule(
                rule_id="security_violation",
                name="Security Violation",
                description="Alert on security violations",
                condition="security_event == True",
                severity=AlertSeverity.CRITICAL,
                category=AlertCategory.SECURITY,
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK, NotificationChannel.WEBHOOK]
            ),
            AlertRule(
                rule_id="trading_anomaly",
                name="Trading Anomaly",
                description="Alert on unusual trading activity",
                condition="trading_anomaly == True",
                severity=AlertSeverity.ERROR,
                category=AlertCategory.TRADING,
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK]
            ),
            AlertRule(
                rule_id="ai_system_failure",
                name="AI System Failure",
                description="Alert when AI system components fail",
                condition="ai_system_status == 'failed'",
                severity=AlertSeverity.CRITICAL,
                category=AlertCategory.AI_SYSTEM,
                notification_channels=[NotificationChannel.EMAIL, NotificationChannel.SLACK, NotificationChannel.WEBHOOK]
            )
        ]
        
        for rule in default_rules:
            self.alert_rules[rule.rule_id] = rule
    
    async def start_monitoring(self):
        """Start continuous monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_task = asyncio.create_task(self._monitoring_loop())
        alert_logger.info("Alert monitoring started")
    
    async def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring_active = False
        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass
        alert_logger.info("Alert monitoring stopped")
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Check for auto-resolve conditions
                await self._check_auto_resolve()
                
                # Clean up old alerts
                await self._cleanup_old_alerts()
                
                # Wait for next cycle
                await asyncio.sleep(60)  # Check every minute
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                alert_logger.error(f"Monitoring loop error: {e}")
                await asyncio.sleep(30)  # Wait 30 seconds on error
    
    async def _check_auto_resolve(self):
        """Check for alerts that should auto-resolve"""
        current_time = datetime.utcnow()
        
        for alert in self.alerts:
            if alert.resolved or not alert.acknowledged:
                continue
            
            # Check if alert should auto-resolve
            for rule in self.alert_rules.values():
                if rule.auto_resolve and alert.category == rule.category:
                    time_since_ack = current_time - alert.acknowledged_at
                    if time_since_ack.total_seconds() > (rule.auto_resolve_after_hours * 3600):
                        alert.resolved = True
                        alert.resolved_at = current_time
                        alert_logger.info(f"Alert auto-resolved: {alert.alert_id}")
    
    async def _cleanup_old_alerts(self):
        """Clean up old alerts"""
        current_time = datetime.utcnow()
        cutoff_time = current_time - timedelta(days=30)  # Keep 30 days
        
        old_alerts = [alert for alert in self.alerts if alert.timestamp < cutoff_time]
        for alert in old_alerts:
            self.alerts.remove(alert)
        
        if old_alerts:
            alert_logger.info(f"Cleaned up {len(old_alerts)} old alerts")
    
    async def create_alert(self, severity: AlertSeverity, category: AlertCategory, 
                          title: str, message: str, source: str, 
                          metadata: Dict[str, Any] = None) -> Alert:
        """Create and send a new alert"""
        try:
            alert = Alert(
                alert_id=str(uuid.uuid4()),
                timestamp=datetime.utcnow(),
                severity=severity,
                category=category,
                title=title,
                message=message,
                source=source,
                metadata=metadata or {}
            )
            
            # Add to alerts list
            self.alerts.append(alert)
            
            # Send notifications
            await self._send_notifications(alert)
            
            alert_logger.info(f"Alert created: {alert.alert_id} - {title}")
            return alert
            
        except Exception as e:
            alert_logger.error(f"Failed to create alert: {e}")
            raise
    
    async def _send_notifications(self, alert: Alert):
        """Send notifications for alert"""
        try:
            # Get notification channels for this alert category
            channels = self._get_notification_channels(alert)
            
            # Send to each channel
            for channel in channels:
                if channel in self.notifiers:
                    notifier = self.notifiers[channel]
                    success = await notifier.send_alert(alert)
                    
                    if success:
                        alert.notification_sent = True
                        alert_logger.info(f"Notification sent via {channel.value}")
                    else:
                        alert_logger.warning(f"Failed to send notification via {channel.value}")
            
        except Exception as e:
            alert_logger.error(f"Failed to send notifications: {e}")
    
    def _get_notification_channels(self, alert: Alert) -> List[NotificationChannel]:
        """Get notification channels for alert"""
        channels = []
        
        # Check alert rules for this category
        for rule in self.alert_rules.values():
            if rule.category == alert.category and rule.enabled:
                channels.extend(rule.notification_channels)
        
        # Remove duplicates
        return list(set(channels))
    
    async def acknowledge_alert(self, alert_id: str, acknowledged_by: str) -> bool:
        """Acknowledge an alert"""
        try:
            alert = next((a for a in self.alerts if a.alert_id == alert_id), None)
            if not alert:
                return False
            
            alert.acknowledged = True
            alert.acknowledged_by = acknowledged_by
            alert.acknowledged_at = datetime.utcnow()
            
            alert_logger.info(f"Alert acknowledged: {alert_id} by {acknowledged_by}")
            return True
            
        except Exception as e:
            alert_logger.error(f"Failed to acknowledge alert: {e}")
            return False
    
    async def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert"""
        try:
            alert = next((a for a in self.alerts if a.alert_id == alert_id), None)
            if not alert:
                return False
            
            alert.resolved = True
            alert.resolved_at = datetime.utcnow()
            
            alert_logger.info(f"Alert resolved: {alert_id}")
            return True
            
        except Exception as e:
            alert_logger.error(f"Failed to resolve alert: {e}")
            return False
    
    def get_active_alerts(self) -> List[Alert]:
        """Get all active (non-resolved) alerts"""
        return [alert for alert in self.alerts if not alert.resolved]
    
    def get_alerts_by_severity(self, severity: AlertSeverity) -> List[Alert]:
        """Get alerts by severity"""
        return [alert for alert in self.alerts if alert.severity == severity]
    
    def get_alerts_by_category(self, category: AlertCategory) -> List[Alert]:
        """Get alerts by category"""
        return [alert for alert in self.alerts if alert.category == category]
    
    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics"""
        total_alerts = len(self.alerts)
        active_alerts = len(self.get_active_alerts())
        
        severity_counts = {}
        for severity in AlertSeverity:
            severity_counts[severity.value] = len(self.get_alerts_by_severity(severity))
        
        category_counts = {}
        for category in AlertCategory:
            category_counts[category.value] = len(self.get_alerts_by_category(category))
        
        return {
            'total_alerts': total_alerts,
            'active_alerts': active_alerts,
            'resolved_alerts': total_alerts - active_alerts,
            'severity_distribution': severity_counts,
            'category_distribution': category_counts,
            'monitoring_active': self.monitoring_active
        }

# Global alerting system instance
alerting_system = RealTimeAlertingSystem() 