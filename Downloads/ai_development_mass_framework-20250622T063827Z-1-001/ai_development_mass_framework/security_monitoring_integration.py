"""
🔒 SECURITY & MONITORING INTEGRATION
Production-ready security and monitoring integration for MASS Framework

This script integrates:
- Enterprise security hardening
- Real-time alerting and monitoring
- Comprehensive backtesting validation
- Production deployment readiness
"""

import asyncio
import logging
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path

# Import our security and monitoring modules
from security.enterprise_security_hardening import EnterpriseSecurityHardening, security_hardening
from monitoring.real_time_alerting import RealTimeAlertingSystem, AlertSeverity, AlertCategory, alerting_system
from trading.backtesting_engine import BacktestingEngine, BacktestConfig, BacktestMode

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/security_monitoring.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class SecurityMonitoringIntegration:
    """Comprehensive security and monitoring integration"""
    
    def __init__(self):
        self.security_hardening = security_hardening
        self.alerting_system = alerting_system
        self.backtesting_engine = None
        self.integration_active = False
        
        # Load configuration
        self.config = self._load_configuration()
        
        logger.info("Security and monitoring integration initialized")
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load integration configuration"""
        config = {
            'security': {
                'enable_monitoring': True,
                'enable_threat_detection': True,
                'enable_audit_logging': True,
                'secrets_rotation_interval_hours': 24,
                'max_failed_attempts': 5,
                'lockout_duration_minutes': 30
            },
            'alerting': {
                'email': {
                    'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
                    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
                    'username': os.getenv('EMAIL_USERNAME'),
                    'password': os.getenv('EMAIL_PASSWORD'),
                    'from_email': os.getenv('FROM_EMAIL'),
                    'to_emails': os.getenv('TO_EMAILS', '').split(',')
                },
                'slack': {
                    'webhook_url': os.getenv('SLACK_WEBHOOK_URL'),
                    'channel': os.getenv('SLACK_CHANNEL', '#alerts'),
                    'username': 'MASS Framework Alerts'
                },
                'webhook': {
                    'webhook_url': os.getenv('WEBHOOK_URL'),
                    'timeout': 10
                }
            },
            'backtesting': {
                'enable_validation': True,
                'validation_period_days': 365,
                'required_strategies': [
                    'momentum_rsi',
                    'mean_reversion_bollinger',
                    'breakout_atr',
                    'macd_crossover'
                ],
                'minimum_performance_thresholds': {
                    'sharpe_ratio': 0.5,
                    'max_drawdown': -0.2,
                    'win_rate': 0.4,
                    'profit_factor': 1.2
                }
            },
            'monitoring': {
                'check_interval_seconds': 60,
                'alert_thresholds': {
                    'cpu_usage_percent': 80,
                    'memory_usage_percent': 85,
                    'disk_usage_percent': 90,
                    'error_rate_percent': 5,
                    'response_time_ms': 2000
                }
            }
        }
        
        return config
    
    async def start_integration(self):
        """Start the complete security and monitoring integration"""
        try:
            logger.info("🚀 Starting Security & Monitoring Integration")
            
            # Create necessary directories
            self._create_directories()
            
            # Initialize security hardening
            await self._initialize_security_hardening()
            
            # Initialize alerting system
            await self._initialize_alerting_system()
            
            # Initialize backtesting validation
            await self._initialize_backtesting_validation()
            
            # Start monitoring
            await self._start_monitoring()
            
            self.integration_active = True
            logger.info("✅ Security & Monitoring Integration started successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to start integration: {e}")
            raise
    
    async def stop_integration(self):
        """Stop the integration"""
        try:
            self.integration_active = False
            
            # Stop security monitoring
            await self.security_hardening.stop_monitoring()
            
            # Stop alerting system
            await self.alerting_system.stop_monitoring()
            
            logger.info("🛑 Security & Monitoring Integration stopped")
            
        except Exception as e:
            logger.error(f"Error stopping integration: {e}")
    
    def _create_directories(self):
        """Create necessary directories"""
        directories = [
            'logs',
            'logs/security',
            'logs/monitoring',
            'logs/backtesting',
            'data/backtesting',
            'reports/security',
            'reports/backtesting'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    async def _initialize_security_hardening(self):
        """Initialize security hardening"""
        try:
            logger.info("🔒 Initializing Security Hardening")
            
            # Start security monitoring
            await self.security_hardening.start_monitoring()
            
            # Create security status report
            security_status = self.security_hardening.get_security_status()
            
            logger.info(f"Security Status: {json.dumps(security_status, indent=2)}")
            
            # Create security alert for initialization
            await self.alerting_system.create_alert(
                severity=AlertSeverity.INFO,
                category=AlertCategory.SECURITY,
                title="Security Hardening Initialized",
                message="Enterprise security hardening system has been successfully initialized",
                source="security_integration",
                metadata={'status': 'initialized', 'timestamp': datetime.utcnow().isoformat()}
            )
            
            logger.info("✅ Security Hardening initialized")
            
        except Exception as e:
            logger.error(f"❌ Security hardening initialization failed: {e}")
            raise
    
    async def _initialize_alerting_system(self):
        """Initialize alerting system"""
        try:
            logger.info("🚨 Initializing Alerting System")
            
            # Start alerting monitoring
            await self.alerting_system.start_monitoring()
            
            # Test alert
            await self.alerting_system.create_alert(
                severity=AlertSeverity.INFO,
                category=AlertCategory.INFRASTRUCTURE,
                title="Alerting System Online",
                message="Real-time alerting system has been successfully initialized",
                source="alerting_integration",
                metadata={'status': 'online', 'timestamp': datetime.utcnow().isoformat()}
            )
            
            logger.info("✅ Alerting System initialized")
            
        except Exception as e:
            logger.error(f"❌ Alerting system initialization failed: {e}")
            raise
    
    async def _initialize_backtesting_validation(self):
        """Initialize backtesting validation"""
        try:
            if not self.config['backtesting']['enable_validation']:
                logger.info("⏭️ Backtesting validation disabled")
                return
            
            logger.info("📊 Initializing Backtesting Validation")
            
            # Create backtesting configuration
            end_date = datetime.utcnow()
            start_date = end_date - timedelta(days=self.config['backtesting']['validation_period_days'])
            
            backtest_config = BacktestConfig(
                start_date=start_date,
                end_date=end_date,
                initial_capital=100000.0,
                mode=BacktestMode.HISTORICAL
            )
            
            self.backtesting_engine = BacktestingEngine(backtest_config)
            
            # Run validation for required strategies
            await self._validate_trading_strategies()
            
            logger.info("✅ Backtesting Validation initialized")
            
        except Exception as e:
            logger.error(f"❌ Backtesting validation initialization failed: {e}")
            raise
    
    async def _validate_trading_strategies(self):
        """Validate trading strategies"""
        try:
            strategies = self.config['backtesting']['required_strategies']
            thresholds = self.config['backtesting']['minimum_performance_thresholds']
            
            validation_results = {}
            
            for strategy in strategies:
                logger.info(f"Validating strategy: {strategy}")
                
                try:
                    # Run backtest
                    result = await self.backtesting_engine.run_backtest(
                        strategy_name=strategy,
                        symbol="AAPL",  # Use AAPL as test symbol
                        strategy_params={}
                    )
                    
                    # Check performance against thresholds
                    validation_passed = True
                    failed_checks = []
                    
                    if result.sharpe_ratio < thresholds['sharpe_ratio']:
                        validation_passed = False
                        failed_checks.append(f"Sharpe ratio {result.sharpe_ratio:.3f} < {thresholds['sharpe_ratio']}")
                    
                    if result.max_drawdown < thresholds['max_drawdown']:
                        validation_passed = False
                        failed_checks.append(f"Max drawdown {result.max_drawdown:.3f} < {thresholds['max_drawdown']}")
                    
                    if result.win_rate < thresholds['win_rate']:
                        validation_passed = False
                        failed_checks.append(f"Win rate {result.win_rate:.3f} < {thresholds['win_rate']}")
                    
                    if result.profit_factor < thresholds['profit_factor']:
                        validation_passed = False
                        failed_checks.append(f"Profit factor {result.profit_factor:.3f} < {thresholds['profit_factor']}")
                    
                    validation_results[strategy] = {
                        'passed': validation_passed,
                        'failed_checks': failed_checks,
                        'performance': {
                            'total_return': result.total_return,
                            'sharpe_ratio': result.sharpe_ratio,
                            'max_drawdown': result.max_drawdown,
                            'win_rate': result.win_rate,
                            'profit_factor': result.profit_factor
                        }
                    }
                    
                    # Create alert based on validation result
                    if validation_passed:
                        await self.alerting_system.create_alert(
                            severity=AlertSeverity.INFO,
                            category=AlertCategory.TRADING,
                            title=f"Strategy Validation Passed: {strategy}",
                            message=f"Trading strategy {strategy} passed all performance thresholds",
                            source="backtesting_validation",
                            metadata=validation_results[strategy]
                        )
                    else:
                        await self.alerting_system.create_alert(
                            severity=AlertSeverity.WARNING,
                            category=AlertCategory.TRADING,
                            title=f"Strategy Validation Failed: {strategy}",
                            message=f"Trading strategy {strategy} failed performance thresholds: {', '.join(failed_checks)}",
                            source="backtesting_validation",
                            metadata=validation_results[strategy]
                        )
                    
                except Exception as e:
                    logger.error(f"Strategy validation failed for {strategy}: {e}")
                    validation_results[strategy] = {
                        'passed': False,
                        'failed_checks': [f"Validation error: {str(e)}"],
                        'performance': {}
                    }
                    
                    await self.alerting_system.create_alert(
                        severity=AlertSeverity.ERROR,
                        category=AlertCategory.TRADING,
                        title=f"Strategy Validation Error: {strategy}",
                        message=f"Error during strategy validation: {str(e)}",
                        source="backtesting_validation",
                        metadata={'error': str(e)}
                    )
            
            # Save validation report
            self._save_validation_report(validation_results)
            
            logger.info(f"Strategy validation completed: {len([r for r in validation_results.values() if r['passed']])}/{len(strategies)} passed")
            
        except Exception as e:
            logger.error(f"Strategy validation failed: {e}")
            raise
    
    def _save_validation_report(self, validation_results: Dict[str, Any]):
        """Save validation report"""
        try:
            report = {
                'timestamp': datetime.utcnow().isoformat(),
                'validation_results': validation_results,
                'summary': {
                    'total_strategies': len(validation_results),
                    'passed_strategies': len([r for r in validation_results.values() if r['passed']]),
                    'failed_strategies': len([r for r in validation_results.values() if not r['passed']])
                }
            }
            
            report_path = f"reports/backtesting/validation_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=2)
            
            logger.info(f"Validation report saved: {report_path}")
            
        except Exception as e:
            logger.error(f"Failed to save validation report: {e}")
    
    async def _start_monitoring(self):
        """Start continuous monitoring"""
        try:
            logger.info("📊 Starting Continuous Monitoring")
            
            # Start monitoring loop
            asyncio.create_task(self._monitoring_loop())
            
            logger.info("✅ Continuous monitoring started")
            
        except Exception as e:
            logger.error(f"❌ Failed to start monitoring: {e}")
            raise
    
    async def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.integration_active:
            try:
                # Check security status
                await self._check_security_status()
                
                # Check system performance
                await self._check_system_performance()
                
                # Check trading system health
                await self._check_trading_health()
                
                # Wait for next check
                await asyncio.sleep(self.config['monitoring']['check_interval_seconds'])
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                await asyncio.sleep(30)  # Wait 30 seconds on error
    
    async def _check_security_status(self):
        """Check security status"""
        try:
            security_status = self.security_hardening.get_security_status()
            
            # Check for critical security issues
            if security_status.get('threat_report', {}).get('recent_threats', 0) > 10:
                await self.alerting_system.create_alert(
                    severity=AlertSeverity.CRITICAL,
                    category=AlertCategory.SECURITY,
                    title="High Security Threat Level",
                    message="Multiple security threats detected in recent monitoring period",
                    source="security_monitoring",
                    metadata=security_status
                )
            
            # Check for security violations
            audit_report = security_status.get('audit_report', {})
            if audit_report.get('security_violations', 0) > 50:
                await self.alerting_system.create_alert(
                    severity=AlertSeverity.WARNING,
                    category=AlertCategory.SECURITY,
                    title="High Security Violations",
                    message="Multiple security violations detected",
                    source="security_monitoring",
                    metadata=audit_report
                )
                
        except Exception as e:
            logger.error(f"Security status check failed: {e}")
    
    async def _check_system_performance(self):
        """Check system performance"""
        try:
            import psutil
            
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            thresholds = self.config['monitoring']['alert_thresholds']
            
            # Check CPU usage
            if cpu_percent > thresholds['cpu_usage_percent']:
                await self.alerting_system.create_alert(
                    severity=AlertSeverity.WARNING,
                    category=AlertCategory.PERFORMANCE,
                    title="High CPU Usage",
                    message=f"CPU usage is {cpu_percent:.1f}%",
                    source="system_monitoring",
                    metadata={'cpu_percent': cpu_percent, 'threshold': thresholds['cpu_usage_percent']}
                )
            
            # Check memory usage
            if memory.percent > thresholds['memory_usage_percent']:
                await self.alerting_system.create_alert(
                    severity=AlertSeverity.WARNING,
                    category=AlertCategory.PERFORMANCE,
                    title="High Memory Usage",
                    message=f"Memory usage is {memory.percent:.1f}%",
                    source="system_monitoring",
                    metadata={'memory_percent': memory.percent, 'threshold': thresholds['memory_usage_percent']}
                )
            
            # Check disk usage
            if disk.percent > thresholds['disk_usage_percent']:
                await self.alerting_system.create_alert(
                    severity=AlertSeverity.WARNING,
                    category=AlertCategory.PERFORMANCE,
                    title="High Disk Usage",
                    message=f"Disk usage is {disk.percent:.1f}%",
                    source="system_monitoring",
                    metadata={'disk_percent': disk.percent, 'threshold': thresholds['disk_usage_percent']}
                )
                
        except Exception as e:
            logger.error(f"System performance check failed: {e}")
    
    async def _check_trading_health(self):
        """Check trading system health"""
        try:
            # This would check trading system components
            # For now, we'll create a placeholder check
            
            # Simulate trading system health check
            trading_health = {
                'database_connected': True,
                'market_data_feed': True,
                'order_execution': True,
                'risk_management': True
            }
            
            # Check for any failed components
            failed_components = [k for k, v in trading_health.items() if not v]
            
            if failed_components:
                await self.alerting_system.create_alert(
                    severity=AlertSeverity.CRITICAL,
                    category=AlertCategory.TRADING,
                    title="Trading System Component Failure",
                    message=f"Failed components: {', '.join(failed_components)}",
                    source="trading_monitoring",
                    metadata={'failed_components': failed_components}
                )
                
        except Exception as e:
            logger.error(f"Trading health check failed: {e}")
    
    def get_integration_status(self) -> Dict[str, Any]:
        """Get integration status"""
        return {
            'integration_active': self.integration_active,
            'security_status': self.security_hardening.get_security_status(),
            'alerting_status': self.alerting_system.get_alert_statistics(),
            'configuration': self.config,
            'timestamp': datetime.utcnow().isoformat()
        }

async def main():
    """Main function"""
    try:
        logger.info("🚀 Starting MASS Framework Security & Monitoring Integration")
        
        # Create integration instance
        integration = SecurityMonitoringIntegration()
        
        # Start integration
        await integration.start_integration()
        
        # Keep running
        while True:
            await asyncio.sleep(60)
            
            # Log status every hour
            if datetime.utcnow().minute == 0:
                status = integration.get_integration_status()
                logger.info(f"Integration Status: {json.dumps(status, indent=2)}")
        
    except KeyboardInterrupt:
        logger.info("🛑 Received interrupt signal")
    except Exception as e:
        logger.error(f"❌ Integration failed: {e}")
        raise
    finally:
        if 'integration' in locals():
            await integration.stop_integration()

if __name__ == "__main__":
    asyncio.run(main()) 