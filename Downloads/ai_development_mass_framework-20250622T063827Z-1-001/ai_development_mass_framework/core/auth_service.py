"""
Authentication Service for MASS Framework
Handles JWT-based authentication, user management, and security
"""

import jwt
import bcrypt
import secrets
import json
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import logging
import os
import traceback
from core.database_manager import DatabaseManager

logger = logging.getLogger(__name__)

class UserRole(Enum):
    ADMIN = "admin"
    DEVELOPER = "developer"
    ANALYST = "analyst"
    VIEWER = "viewer"

class Permission(Enum):
    # AI Agent Permissions
    USE_AI_AGENTS = "use_ai_agents"
    MANAGE_AI_AGENTS = "manage_ai_agents"
    
    # Collaboration Permissions
    CREATE_COLLABORATIONS = "create_collaborations"
    MANAGE_COLLABORATIONS = "manage_collaborations"
    VIEW_COLLABORATIONS = "view_collaborations"
    
    # Project Permissions
    ANALYZE_PROJECTS = "analyze_projects"
    MANAGE_PROJECTS = "manage_projects"
    VIEW_PROJECTS = "view_projects"
    
    # System Permissions
    ADMIN_SYSTEM = "admin_system"
    VIEW_ANALYTICS = "view_analytics"
    MANAGE_USERS = "manage_users"
    
    # API Permissions
    API_ACCESS = "api_access"
    ADMIN_API = "admin_api"

@dataclass
class User:
    """User model"""
    id: str
    username: str
    email: str
    password_hash: str
    role: UserRole
    tenant_id: str
    is_active: bool = True
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class AuthToken:
    """Authentication token model"""
    token: str
    user_id: str
    expires_at: datetime
    token_type: str = "access"
    
@dataclass
class LoginCredentials:
    """Login credentials model"""
    username: str
    password: str
    tenant_id: Optional[str] = None

class AuthenticationService:
    """JWT-based authentication service"""
    
    def __init__(self, secret_key: Optional[str] = None, token_expiry_hours: int = 24, db_manager: Optional[DatabaseManager] = None):
        self.secret_key = secret_key or os.getenv("JWT_SECRET_KEY", secrets.token_urlsafe(32))
        self.token_expiry_hours = token_expiry_hours
        self.algorithm = "HS256"
        self.db_manager = db_manager or DatabaseManager()
        self.role_permissions = self._define_role_permissions()
        
        # Initialize database tables
        self._init_auth_tables()
    
    def _define_role_permissions(self) -> Dict[UserRole, List[Permission]]:
        """Define permissions for each role"""
        return {
            UserRole.ADMIN: [
                Permission.USE_AI_AGENTS,
                Permission.MANAGE_AI_AGENTS,
                Permission.CREATE_COLLABORATIONS,
                Permission.MANAGE_COLLABORATIONS,
                Permission.VIEW_COLLABORATIONS,
                Permission.ANALYZE_PROJECTS,
                Permission.MANAGE_PROJECTS,
                Permission.VIEW_PROJECTS,
                Permission.ADMIN_SYSTEM,
                Permission.VIEW_ANALYTICS,
                Permission.MANAGE_USERS,
                Permission.API_ACCESS,
                Permission.ADMIN_API
            ],
            UserRole.DEVELOPER: [
                Permission.USE_AI_AGENTS,
                Permission.CREATE_COLLABORATIONS,
                Permission.VIEW_COLLABORATIONS,
                Permission.ANALYZE_PROJECTS,
                Permission.VIEW_PROJECTS,
                Permission.API_ACCESS
            ],
            UserRole.ANALYST: [
                Permission.USE_AI_AGENTS,
                Permission.VIEW_COLLABORATIONS,
                Permission.ANALYZE_PROJECTS,
                Permission.VIEW_PROJECTS,
                Permission.VIEW_ANALYTICS,
                Permission.API_ACCESS
            ],
            UserRole.VIEWER: [
                Permission.VIEW_COLLABORATIONS,
                Permission.VIEW_PROJECTS,
                Permission.API_ACCESS
            ]
        }
    
    def _init_auth_tables(self):
        """Initialize authentication database tables"""
        try:
            # Users table
            self.db_manager.execute_query("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    role TEXT NOT NULL,
                    tenant_id TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    metadata TEXT
                )
            """)
            
            # Sessions table
            self.db_manager.execute_query("""
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    token_hash TEXT NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # API Keys table
            self.db_manager.execute_query("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    key_hash TEXT NOT NULL,
                    name TEXT NOT NULL,
                    permissions TEXT,
                    expires_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # Audit log table
            self.db_manager.execute_query("""
                CREATE TABLE IF NOT EXISTS auth_audit_log (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    action TEXT NOT NULL,
                    resource TEXT,
                    details TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success BOOLEAN DEFAULT TRUE
                )
            """)
            
            logger.info("Authentication tables initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize auth tables: {str(e)}")
            raise
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification failed: {str(e)}")
            return False
    
    def create_user(
        self, 
        username: str, 
        email: str, 
        password: str, 
        role: UserRole,
        tenant_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> User:
        print(f"DEBUG: create_user received metadata: {metadata} (type: {type(metadata)})")
        import traceback
        traceback.print_stack()
        user_id = secrets.token_urlsafe(16)
        password_hash = self.hash_password(password)
        user = User(
            id=user_id,
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            tenant_id=tenant_id,
            created_at=datetime.now(timezone.utc),
            metadata=metadata or {}
        )
        try:
            # Always serialize metadata to JSON string for DB
            metadata_json = json.dumps(user.metadata or {})
            print(f"DEBUG: Final metadata_json before insert: {metadata_json} (type: {type(metadata_json)})")
            created_at_str = user.created_at.isoformat()
            print(f"DEBUG: INSERT PARAMS: id={user.id}, username={user.username}, email={user.email}, password_hash={user.password_hash}, role={user.role.value}, tenant_id={user.tenant_id}, created_at={created_at_str}, metadata_json={metadata_json} (type: {type(metadata_json)})")
            self.db_manager.execute_query(
                """INSERT INTO users 
                   (id, username, email, password_hash, role, tenant_id, created_at, metadata)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (user.id, user.username, user.email, user.password_hash, 
                 user.role.value, user.tenant_id, created_at_str, metadata_json)
            )
            self._log_auth_event(user.id, "USER_CREATED", f"User {username} created")
            logger.info(f"User created successfully: {username}")
            return user
        except Exception as e:
            import traceback
            print(f"[DEBUG] create_user exception: {e}")
            print(f"[DEBUG] create_user params: id={user.id}, username={user.username}, email={user.email}, password_hash={user.password_hash}, role={user.role.value}, tenant_id={user.tenant_id}, created_at={user.created_at}, metadata_json={metadata_json}")
            traceback.print_exc()
            logger.error(f"Failed to create user {username}: {str(e)}")
            raise
    
    def authenticate_user(self, credentials: LoginCredentials) -> Optional[User]:
        """Authenticate user with username/password"""
        import sys
        print(f"[DEBUG] authenticate_user called. id(self)={id(self)} db_manager={self.db_manager}", file=sys.stderr)
        print(f"[DEBUG] authenticate_user: credentials={credentials}", file=sys.stderr)
        try:
            # Query user from database
            result = self.db_manager.fetch_one(
                "SELECT * FROM users WHERE username = ? AND is_active = 1",
                (credentials.username,)
            )
            print(f"[DEBUG] authenticate_user: DB result for username={credentials.username}: {result}", file=sys.stderr)
            if not result:
                self._log_auth_event(None, "LOGIN_FAILED", f"User not found: {credentials.username}")
                return None
              # Convert result to User object
            user = User(
                id=result['id'],
                username=result['username'],
                email=result['email'],
                password_hash=result['password_hash'],
                role=UserRole(result['role']),
                tenant_id=result['tenant_id'],
                is_active=bool(result['is_active']),
                created_at=result['created_at'],
                last_login=result['last_login'],
                metadata=json.loads(result['metadata']) if result['metadata'] else {}
            )
            print(f"[DEBUG] authenticate_user: User object created: {user}", file=sys.stderr)
            # Verify password
            if not self.verify_password(credentials.password, user.password_hash):
                self._log_auth_event(user.id, "LOGIN_FAILED", "Invalid password")
                print(f"[DEBUG] authenticate_user: Invalid password for user {user.username}", file=sys.stderr)
                return None
            
            # Check tenant if specified
            if credentials.tenant_id and user.tenant_id != credentials.tenant_id:
                self._log_auth_event(user.id, "LOGIN_FAILED", "Invalid tenant")
                print(f"[DEBUG] authenticate_user: Invalid tenant for user {user.username}", file=sys.stderr)
                return None
            
            print(f"[DEBUG] authenticate_user: Authentication successful for user {user.username}", file=sys.stderr)
            return user
        except Exception as e:
            print(f"[DEBUG] authenticate_user: Exception: {e}\n{traceback.format_exc()}", file=sys.stderr)
            logger.error(f"Failed to authenticate user {credentials.username}: {str(e)}")
            raise
    
    def generate_token(self, user: User) -> AuthToken:
        """Generate JWT token for authenticated user"""
        expires_at = datetime.now(timezone.utc) + timedelta(hours=self.token_expiry_hours)
        
        payload = {
            'user_id': user.id,
            'username': user.username,
            'role': user.role.value,
            'tenant_id': user.tenant_id,
            'exp': expires_at,
            'iat': datetime.now(timezone.utc),
            'jti': secrets.token_urlsafe(16)  # JWT ID
        }
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        
        # Store session in database
        session_id = secrets.token_urlsafe(16)
        token_hash = self.hash_password(token)
        
        self.db_manager.execute_query(
            """INSERT INTO user_sessions (id, user_id, token_hash, expires_at)
               VALUES (?, ?, ?, ?)""",
            (session_id, user.id, token_hash, expires_at)
        )
        
        auth_token = AuthToken(
            token=token,
            user_id=user.id,
            expires_at=expires_at
        )
        
        self._log_auth_event(user.id, "TOKEN_GENERATED", "JWT token generated")
        return auth_token
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Check if session exists and is active
            session = self.db_manager.fetch_one(
                """SELECT * FROM user_sessions 
                   WHERE user_id = ? AND expires_at > ? AND is_active = 1""",
                (payload['user_id'], datetime.now(timezone.utc))
            )
            
            if not session:
                self._log_auth_event(payload.get('user_id'), "TOKEN_INVALID", "Session not found or expired")
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            self._log_auth_event(None, "TOKEN_EXPIRED", "JWT token expired")
            return None
        except jwt.InvalidTokenError as e:
            self._log_auth_event(None, "TOKEN_INVALID", f"Invalid JWT token: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Token verification failed: {str(e)}")
            return None
    
    def revoke_token(self, token: str) -> bool:
        """Revoke a JWT token by deactivating the session"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Deactivate session
            self.db_manager.execute_query(
                "UPDATE user_sessions SET is_active = 0 WHERE user_id = ?",
                (payload['user_id'],)
            )
            
            self._log_auth_event(payload['user_id'], "TOKEN_REVOKED", "JWT token revoked")
            return True
            
        except Exception as e:
            logger.error(f"Token revocation failed: {str(e)}")
            return False
    
    def get_user_permissions(self, user: User) -> List[Permission]:
        """Get permissions for a user based on their role"""
        return self.role_permissions.get(user.role, [])
    
    def has_permission(self, user: User, permission: Permission) -> bool:
        """Check if user has a specific permission"""
        user_permissions = self.get_user_permissions(user)
        return permission in user_permissions
    
    def require_permission(self, user: User, permission: Permission) -> bool:
        """Require user to have a specific permission, raise exception if not"""
        if not self.has_permission(user, permission):
            self._log_auth_event(user.id, "PERMISSION_DENIED", f"Permission denied: {permission.value}")
            raise PermissionError(f"User does not have permission: {permission.value}")
        return True
    
    def create_api_key(
        self, 
        user: User, 
        name: str, 
        permissions: List[Permission] = None,
        expires_at: datetime = None
    ) -> str:
        """Create an API key for a user"""
        api_key = f"mass_{secrets.token_urlsafe(32)}"
        key_hash = self.hash_password(api_key)
        key_id = secrets.token_urlsafe(16)
        
        # Default to user's permissions if not specified
        if permissions is None:
            permissions = self.get_user_permissions(user)
        
        try:
            self.db_manager.execute_query(
                """INSERT INTO api_keys (id, user_id, key_hash, name, permissions, expires_at)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (key_id, user.id, key_hash, name, 
                 ','.join([p.value for p in permissions]), expires_at)
            )
            
            self._log_auth_event(user.id, "API_KEY_CREATED", f"API key created: {name}")
            return api_key
            
        except Exception as e:
            logger.error(f"Failed to create API key: {str(e)}")
            raise
    
    def verify_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Verify an API key and return user info"""
        try:
            # Find all active API keys
            results = self.db_manager.fetch_all(
                """SELECT ak.*, u.username, u.role, u.tenant_id 
                   FROM api_keys ak
                   JOIN users u ON ak.user_id = u.id
                   WHERE ak.is_active = 1 
                   AND (ak.expires_at IS NULL OR ak.expires_at > ?)""",
                (datetime.now(timezone.utc),)
            )
            if not results:
                return None
            for result in results:
                key_hash = result['key_hash']
                if self.verify_password(api_key, key_hash):
                    return {
                        'user_id': result['user_id'],
                        'username': result['username'],
                        'role': result['role'],
                        'tenant_id': result['tenant_id'],
                        'permissions': result['permissions'].split(',') if result['permissions'] else [],
                        'api_key_name': result['name']
                    }
            return None
        except Exception as e:
            logger.error(f"API key verification failed: {str(e)}")
            return None
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        try:
            result = self.db_manager.fetch_one(
                "SELECT * FROM users WHERE id = ? AND is_active = 1",
                (user_id,)
            )
            
            if not result:
                return None
            
            # Parse created_at and last_login as datetime if needed
            created_at = result['created_at']
            if isinstance(created_at, str):
                from datetime import datetime
                created_at = datetime.fromisoformat(created_at)
            last_login = result['last_login']
            if last_login and isinstance(last_login, str):
                from datetime import datetime
                last_login = datetime.fromisoformat(last_login)
            
            return User(
                id=result['id'],
                username=result['username'],
                email=result['email'],
                password_hash=result['password_hash'],
                role=UserRole(result['role']),
                tenant_id=result['tenant_id'],
                is_active=bool(result['is_active']),
                created_at=created_at,
                last_login=last_login,
                metadata=json.loads(result['metadata']) if result['metadata'] else {}
            )
            
        except Exception as e:
            logger.error(f"Failed to get user by ID {user_id}: {str(e)}")
            return None
    
    def update_user_role(self, user_id: str, new_role: UserRole, admin_user: User) -> bool:
        """Update user role (admin only)"""
        try:
            # Check admin permissions
            self.require_permission(admin_user, Permission.MANAGE_USERS)
            
            self.db_manager.execute_query(
                "UPDATE users SET role = ? WHERE id = ?",
                (new_role.value, user_id)
            )
            
            self._log_auth_event(
                admin_user.id, 
                "USER_ROLE_UPDATED", 
                f"User {user_id} role updated to {new_role.value}"
            )
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update user role: {str(e)}")
            return False
    
    def deactivate_user(self, user_id: str, admin_user: User) -> bool:
        """Deactivate a user account (admin only)"""
        try:
            # Check admin permissions
            self.require_permission(admin_user, Permission.MANAGE_USERS)
            
            # Deactivate user
            self.db_manager.execute_query(
                "UPDATE users SET is_active = 0 WHERE id = ?",
                (user_id,)
            )
            
            # Deactivate all sessions
            self.db_manager.execute_query(
                "UPDATE user_sessions SET is_active = 0 WHERE user_id = ?",
                (user_id,)
            )
            
            # Deactivate all API keys
            self.db_manager.execute_query(
                "UPDATE api_keys SET is_active = 0 WHERE user_id = ?",
                (user_id,)
            )
            
            self._log_auth_event(admin_user.id, "USER_DEACTIVATED", f"User {user_id} deactivated")
            return True
            
        except Exception as e:
            logger.error(f"Failed to deactivate user: {str(e)}")
            return False
    
    def get_auth_stats(self, admin_user: User) -> Dict[str, Any]:
        """Get authentication statistics (admin only)"""
        try:
            print(f"[DEBUG] get_auth_stats: id(self)={id(self)} id(self.db_manager)={id(self.db_manager)} id(self.db_manager._external_connection)={id(self.db_manager._external_connection) if hasattr(self.db_manager, '_external_connection') else None}", flush=True)
            self.require_permission(admin_user, Permission.VIEW_ANALYTICS)
            # Get user counts by role
            role_counts = {}
            for role in UserRole:
                count_row = self.db_manager.fetch_one(
                    "SELECT COUNT(*) FROM users WHERE role = ? AND is_active = 1",
                    (role.value,)
                )
                count = count_row[0] if count_row else 0
                role_counts[role.value] = count
            # Get active sessions count
            session_row = self.db_manager.fetch_one(
                "SELECT COUNT(*) FROM user_sessions WHERE expires_at > ? AND is_active = 1",
                (datetime.now(timezone.utc),)
            )
            active_sessions = session_row[0] if session_row else 0
            # Get recent login activity
            recent_logins = self.db_manager.fetch_all(
                """SELECT action, COUNT(*) as count 
                   FROM auth_audit_log 
                   WHERE action IN ('LOGIN_SUCCESS', 'LOGIN_FAILED') 
                   AND timestamp > ? 
                   GROUP BY action""",
                (datetime.now(timezone.utc) - timedelta(days=7),)
            )
            recent_activity = {row[0]: row[1] for row in recent_logins} if recent_logins else {}
            return {
                'role_counts': role_counts,
                'active_sessions': active_sessions,
                'recent_activity': recent_activity,
                'total_users': sum(role_counts.values())
            }
        except Exception as e:
            logger.error(f"Failed to get auth stats: {str(e)}")
            return {                'role_counts': {},
                'active_sessions': 0,
                'recent_activity': {},
                'total_users': 0
            }
    
    def _log_auth_event(
        self, 
        user_id: Optional[str], 
        action: str, 
        details: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        success: bool = True
    ):
        """Log authentication events for audit purposes"""
        try:
            event_id = secrets.token_urlsafe(16)
            
            self.db_manager.execute_query(
                """INSERT INTO auth_audit_log 
                   (id, user_id, action, details, ip_address, user_agent, success)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (event_id, user_id, action, details, ip_address, user_agent, success)
            )
            
        except Exception as e:
            logger.error(f"Failed to log auth event: {str(e)}")

# Global authentication service instance
# Allow resetting for test isolation
def set_global_auth_service(new_auth_service: AuthenticationService) -> None:
    global auth_service
    auth_service = new_auth_service

# Default instance
auth_service = AuthenticationService()

# Helper functions for common operations
def create_default_admin(auth_service_instance: Optional[AuthenticationService] = None) -> Optional[User]:
    print(f"DEBUG: create_default_admin called with auth_service_instance: {auth_service_instance}")
    """Create default admin user if none exists"""
    auth_service_to_use = auth_service_instance or auth_service
    try:
        # Check if any admin users exist
        result = auth_service_to_use.db_manager.fetch_one(
            "SELECT COUNT(*) as admin_count FROM users WHERE role = 'admin' AND is_active = 1"
        )
        print(f"DEBUG: create_default_admin admin_count result: {result}")
        if result and result.get('admin_count', 0) == 0:
            # Create default admin
            admin_metadata = {"created_by": "system", "is_default": True}
            print(f"DEBUG: create_default_admin metadata: {admin_metadata} (type: {type(admin_metadata)})")
            admin_user = auth_service_to_use.create_user(
                username="admin",
                email="admin@mass-framework.com",
                password="admin123",  # Should be changed immediately
                role=UserRole.ADMIN,
                tenant_id="default",
                metadata=admin_metadata
            )
            logger.info("Default admin user created successfully")
            logger.warning("Default admin password is 'admin123' - CHANGE IMMEDIATELY!")
            return admin_user
        else:
            logger.info("Admin users already exist, skipping default creation")
            return None
    except Exception as e:
        import traceback
        print(f"[DEBUG] create_default_admin exception: {e}")
        traceback.print_exc()
        logger.error(f"Failed to create default admin: {str(e)}")
        return None

def login(username: str, password: str, tenant_id: Optional[str] = None) -> Optional[AuthToken]:
    """Convenience function for user login"""
    credentials = LoginCredentials(username=username, password=password, tenant_id=tenant_id)
    user = auth_service.authenticate_user(credentials)
    
    if user:
        return auth_service.generate_token(user)
    return None

def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Convenience function for token verification"""
    return auth_service.verify_token(token)
