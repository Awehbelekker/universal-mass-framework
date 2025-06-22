"""
Security Enhancements Module for MASS Framework

This module provides comprehensive security features including:
- Authentication and authorization management
- Data encryption and protection
- Security monitoring and audit logging
- Network security and rate limiting
"""

import asyncio
import hashlib
import hmac
import json
import logging
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import jwt
import bcrypt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os


class SecurityLevel(Enum):
    """Security levels for different operations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AuditEventType(Enum):
    """Types of security audit events"""
    LOGIN = "login"
    LOGOUT = "logout"
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    SECURITY_VIOLATION = "security_violation"
    SYSTEM_EVENT = "system_event"


@dataclass
class SecurityConfig:
    """Security configuration settings"""
    jwt_secret_key: str = field(default_factory=lambda: secrets.token_urlsafe(32))
    jwt_expiration_hours: int = 24
    password_min_length: int = 8
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 30
    rate_limit_requests: int = 100
    rate_limit_window_minutes: int = 15
    encryption_key: Optional[bytes] = None
    enable_audit_logging: bool = True
    audit_log_retention_days: int = 90
    security_level: SecurityLevel = SecurityLevel.MEDIUM
    
    def __post_init__(self):
        if self.encryption_key is None:
            self.encryption_key = Fernet.generate_key()


@dataclass
class User:
    """User representation for authentication"""
    user_id: str
    username: str
    email: str
    password_hash: str
    roles: List[str]
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None


@dataclass
class AuditEvent:
    """Security audit event"""
    event_id: str
    event_type: AuditEventType
    user_id: Optional[str]
    resource: str
    action: str
    result: str
    timestamp: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    additional_data: Dict[str, Any] = field(default_factory=dict)


class AuthenticationManager:
    """Manages user authentication and authorization"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.users: Dict[str, User] = {}
        self.active_tokens: Dict[str, Dict[str, Any]] = {}
        self.rate_limit_tracker: Dict[str, List[float]] = {}
        
    async def register_user(self, username: str, email: str, password: str, 
                          roles: List[str] = None) -> User:
        """Register a new user"""
        if roles is None:
            roles = ["user"]
            
        # Validate password strength
        if not self._validate_password_strength(password):
            raise ValueError("Password does not meet security requirements")
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user_id = secrets.token_urlsafe(16)
        user = User(
            user_id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            roles=roles
        )
        
        self.users[user_id] = user
        return user
    
    async def authenticate_user(self, username: str, password: str, 
                              ip_address: str = None) -> Optional[str]:
        """Authenticate user and return JWT token"""
        # Find user by username
        user = None
        for u in self.users.values():
            if u.username == username:
                user = u
                break
        
        if not user:
            return None
        
        # Check if account is locked
        if user.locked_until and user.locked_until > datetime.utcnow():
            raise ValueError("Account is temporarily locked")
        
        # Check rate limiting
        if not self._check_rate_limit(ip_address or "unknown"):
            raise ValueError("Rate limit exceeded")
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            user.failed_login_attempts += 1
            
            # Lock account after too many failed attempts
            if user.failed_login_attempts >= self.config.max_login_attempts:
                user.locked_until = datetime.utcnow() + timedelta(
                    minutes=self.config.lockout_duration_minutes
                )
            
            return None
        
        # Reset failed attempts on successful login
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login = datetime.utcnow()
        
        # Generate JWT token
        token = self._generate_jwt_token(user)
        
        # Store active token
        self.active_tokens[token] = {
            'user_id': user.user_id,
            'username': user.username,
            'roles': user.roles,
            'issued_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(hours=self.config.jwt_expiration_hours)
        }
        
        return token
    
    async def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return user data"""
        try:
            # Check if token is in active tokens
            if token not in self.active_tokens:
                return None
            
            token_data = self.active_tokens[token]
            
            # Check if token is expired
            if token_data['expires_at'] < datetime.utcnow():
                del self.active_tokens[token]
                return None
            
            # Verify JWT signature
            payload = jwt.decode(token, self.config.jwt_secret_key, algorithms=['HS256'])
            
            return token_data
            
        except jwt.InvalidTokenError:
            return None
    
    async def check_permission(self, token: str, resource: str, action: str) -> bool:
        """Check if user has permission for specific resource and action"""
        token_data = await self.verify_token(token)
        if not token_data:
            return False
        
        # Simple role-based permission checking
        # In production, this would be more sophisticated
        user_roles = token_data.get('roles', [])
        
        # Admin has access to everything
        if 'admin' in user_roles:
            return True
        
        # Basic permission logic
        if action == 'read' and 'user' in user_roles:
            return True
        
        if action in ['create', 'update', 'delete'] and 'editor' in user_roles:
            return True
        
        return False
    
    def _validate_password_strength(self, password: str) -> bool:
        """Validate password meets security requirements"""
        if len(password) < self.config.password_min_length:
            return False
        
        # Check for uppercase, lowercase, digit, and special character
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        return has_upper and has_lower and has_digit and has_special
    
    def _generate_jwt_token(self, user: User) -> str:
        """Generate JWT token for user"""
        payload = {
            'user_id': user.user_id,
            'username': user.username,
            'roles': user.roles,
            'exp': datetime.utcnow() + timedelta(hours=self.config.jwt_expiration_hours),
            'iat': datetime.utcnow()
        }
        
        return jwt.encode(payload, self.config.jwt_secret_key, algorithm='HS256')
    
    def _check_rate_limit(self, identifier: str) -> bool:
        """Check if request is within rate limits"""
        now = time.time()
        window_start = now - (self.config.rate_limit_window_minutes * 60)
        
        # Clean old entries
        if identifier in self.rate_limit_tracker:
            self.rate_limit_tracker[identifier] = [
                timestamp for timestamp in self.rate_limit_tracker[identifier]
                if timestamp > window_start
            ]
        else:
            self.rate_limit_tracker[identifier] = []
        
        # Check if within limits
        if len(self.rate_limit_tracker[identifier]) >= self.config.rate_limit_requests:
            return False
        
        # Add current request
        self.rate_limit_tracker[identifier].append(now)
        return True


class DataEncryption:
    """Handles data encryption and decryption"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.cipher_suite = Fernet(config.encryption_key)
    
    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        encrypted_data = self.cipher_suite.encrypt(data.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
        decrypted_data = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted_data.decode('utf-8')
    
    def hash_sensitive_data(self, data: str, salt: str = None) -> Tuple[str, str]:
        """Hash sensitive data with salt"""
        if salt is None:
            salt = secrets.token_urlsafe(16)
        
        hash_obj = hashlib.pbkdf2_hmac('sha256', data.encode('utf-8'), 
                                      salt.encode('utf-8'), 100000)
        hash_str = base64.urlsafe_b64encode(hash_obj).decode('utf-8')
        
        return hash_str, salt
    
    def mask_sensitive_data(self, data: str, mask_char: str = '*') -> str:
        """Mask sensitive data for logging"""
        if len(data) <= 4:
            return mask_char * len(data)
        
        return data[:2] + mask_char * (len(data) - 4) + data[-2:]


class SecurityAuditor:
    """Manages security audit logging and monitoring"""
    
    def __init__(self, config: SecurityConfig):
        self.config = config
        self.audit_events: List[AuditEvent] = []
        self.logger = logging.getLogger(__name__)
        
        # Configure audit logging
        if config.enable_audit_logging:
            self._setup_audit_logging()
    
    async def log_event(self, event_type: AuditEventType, user_id: str = None,
                       resource: str = "", action: str = "", result: str = "",
                       ip_address: str = None, additional_data: Dict = None):
        """Log a security audit event"""
        event = AuditEvent(
            event_id=secrets.token_urlsafe(16),
            event_type=event_type,
            user_id=user_id,
            resource=resource,
            action=action,
            result=result,
            timestamp=datetime.utcnow(),
            ip_address=ip_address,
            additional_data=additional_data or {}
        )
        
        self.audit_events.append(event)
        
        # Log to file if configured
        if self.config.enable_audit_logging:
            self.logger.info(f"AUDIT: {event.event_type.value} | "
                           f"User: {event.user_id} | "
                           f"Resource: {event.resource} | "
                           f"Action: {event.action} | "
                           f"Result: {event.result}")
    
    async def get_audit_events(self, user_id: str = None, event_type: AuditEventType = None,
                              start_date: datetime = None, end_date: datetime = None) -> List[AuditEvent]:
        """Retrieve audit events with filtering"""
        events = self.audit_events
        
        if user_id:
            events = [e for e in events if e.user_id == user_id]
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        if start_date:
            events = [e for e in events if e.timestamp >= start_date]
        
        if end_date:
            events = [e for e in events if e.timestamp <= end_date]
        
        return events
    
    async def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Detect security anomalies in audit events"""
        anomalies = []
        
        # Detect multiple failed logins
        failed_logins = {}
        for event in self.audit_events:
            if event.event_type == AuditEventType.ACCESS_DENIED:
                key = f"{event.user_id}_{event.ip_address}"
                failed_logins[key] = failed_logins.get(key, 0) + 1
        
        for key, count in failed_logins.items():
            if count >= 5:  # Threshold for suspicious activity
                anomalies.append({
                    'type': 'multiple_failed_logins',
                    'key': key,
                    'count': count,
                    'severity': 'high'
                })
        
        # Detect unusual access patterns
        # (This is a simplified example - real implementation would be more sophisticated)
        
        return anomalies
    
    def _setup_audit_logging(self):
        """Setup audit logging configuration"""
        handler = logging.FileHandler('security_audit.log')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)


class SecurityManager:
    """Main security manager that coordinates all security components"""
    
    def __init__(self, config: SecurityConfig = None):
        self.config = config or SecurityConfig()
        self.auth_manager = AuthenticationManager(self.config)
        self.data_encryption = DataEncryption(self.config)
        self.auditor = SecurityAuditor(self.config)
    
    async def initialize(self):
        """Initialize security manager"""
        # Create default admin user if none exists
        if not self.auth_manager.users:
            await self.create_default_admin()
    
    async def create_default_admin(self):
        """Create default admin user"""
        try:
            admin_user = await self.auth_manager.register_user(
                username="admin",
                email="admin@mass-framework.com",
                password="AdminPass123!",
                roles=["admin", "editor", "user"]
            )
            
            await self.auditor.log_event(
                AuditEventType.SYSTEM_EVENT,
                user_id=admin_user.user_id,
                resource="user_management",
                action="create_admin",
                result="success"
            )
            
        except Exception as e:
            await self.auditor.log_event(
                AuditEventType.SYSTEM_EVENT,
                resource="user_management",
                action="create_admin",
                result=f"failed: {str(e)}"
            )
    
    async def authenticate_request(self, username: str, password: str,
                                 ip_address: str = None) -> Optional[str]:
        """Authenticate user request"""
        try:
            token = await self.auth_manager.authenticate_user(username, password, ip_address)
            
            await self.auditor.log_event(
                AuditEventType.LOGIN,
                resource="authentication",
                action="login",
                result="success" if token else "failed",
                ip_address=ip_address
            )
            
            return token
            
        except Exception as e:
            await self.auditor.log_event(
                AuditEventType.LOGIN,
                resource="authentication",
                action="login",
                result=f"failed: {str(e)}",
                ip_address=ip_address
            )
            raise
    
    async def authorize_request(self, token: str, resource: str, action: str) -> bool:
        """Authorize user request"""
        try:
            token_data = await self.auth_manager.verify_token(token)
            if not token_data:
                await self.auditor.log_event(
                    AuditEventType.ACCESS_DENIED,
                    resource=resource,
                    action=action,
                    result="invalid_token"
                )
                return False
            
            has_permission = await self.auth_manager.check_permission(token, resource, action)
            
            await self.auditor.log_event(
                AuditEventType.ACCESS_GRANTED if has_permission else AuditEventType.ACCESS_DENIED,
                user_id=token_data['user_id'],
                resource=resource,
                action=action,
                result="granted" if has_permission else "denied"
            )
            
            return has_permission
            
        except Exception as e:
            await self.auditor.log_event(
                AuditEventType.SECURITY_VIOLATION,
                resource=resource,
                action=action,
                result=f"error: {str(e)}"
            )
            return False
    
    async def get_security_metrics(self) -> Dict[str, Any]:
        """Get security metrics and statistics"""
        total_events = len(self.auditor.audit_events)
        
        # Count events by type
        event_counts = {}
        for event in self.auditor.audit_events:
            event_type = event.event_type.value
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        
        # Recent events (last 24 hours)
        recent_threshold = datetime.utcnow() - timedelta(hours=24)
        recent_events = [e for e in self.auditor.audit_events if e.timestamp >= recent_threshold]
        
        # Detect anomalies
        anomalies = await self.auditor.detect_anomalies()
        
        return {
            'total_events': total_events,
            'event_counts': event_counts,
            'recent_events_24h': len(recent_events),
            'active_users': len(self.auth_manager.users),
            'active_tokens': len(self.auth_manager.active_tokens),
            'anomalies_detected': len(anomalies),
            'security_level': self.config.security_level.value,
            'last_updated': datetime.utcnow().isoformat()
        }


# Example usage and testing
async def main():
    """Example usage of security enhancements"""
    # Initialize security manager
    config = SecurityConfig(
        security_level=SecurityLevel.HIGH,
        enable_audit_logging=True
    )
    
    security_manager = SecurityManager(config)
    await security_manager.initialize()
    
    print("Security Manager initialized successfully")
    
    # Demonstrate authentication
    try:
        # Register a test user
        await security_manager.auth_manager.register_user(
            username="testuser",
            email="test@example.com",
            password="TestPass123!",
            roles=["user"]
        )
        
        # Authenticate user
        token = await security_manager.authenticate_request("testuser", "TestPass123!")
        print(f"Authentication successful, token: {token[:20]}...")
        
        # Test authorization
        can_read = await security_manager.authorize_request(token, "data", "read")
        print(f"Can read data: {can_read}")
        
        can_delete = await security_manager.authorize_request(token, "data", "delete")
        print(f"Can delete data: {can_delete}")
        
        # Get security metrics
        metrics = await security_manager.get_security_metrics()
        print(f"Security metrics: {metrics}")
        
    except Exception as e:
        print(f"Security demo error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
