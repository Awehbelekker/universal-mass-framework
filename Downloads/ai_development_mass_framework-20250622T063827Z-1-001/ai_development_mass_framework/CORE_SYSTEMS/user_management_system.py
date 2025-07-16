import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from decimal import Decimal
import json

logger = logging.getLogger(__name__)

class UserRole(Enum):
    USER = "user"
    TRADER = "trader"
    ANALYST = "analyst"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

class UserStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    BANNED = "banned"

class KYCStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    UNDER_REVIEW = "under_review"

@dataclass
class UserProfile:
    """Complete user profile with all necessary information"""
    id: str
    firebase_uid: str
    email: str
    username: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.PENDING
    kyc_status: KYCStatus = KYCStatus.PENDING
    kyc_data: Optional[Dict[str, Any]] = None
    profile_picture: Optional[str] = None
    timezone: str = "UTC"
    language: str = "en"
    preferences: Optional[Dict[str, Any]] = None
    created_at: datetime = None
    updated_at: datetime = None
    last_login: Optional[datetime] = None
    is_approved: bool = False
    approval_date: Optional[datetime] = None
    approved_by: Optional[str] = None
    tenant_id: str = "default"
    permissions: List[str] = None
    trading_accounts: List[str] = None
    portfolios: List[str] = None
    ai_agents: List[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()
        if self.permissions is None:
            self.permissions = self._get_default_permissions()
        if self.trading_accounts is None:
            self.trading_accounts = []
        if self.portfolios is None:
            self.portfolios = []
        if self.ai_agents is None:
            self.ai_agents = []

    def _get_default_permissions(self) -> List[str]:
        """Get default permissions based on role"""
        base_permissions = ["view_dashboard", "view_profile"]
        
        if self.role == UserRole.USER:
            return base_permissions + ["paper_trading", "view_analytics"]
        elif self.role == UserRole.TRADER:
            return base_permissions + ["live_trading", "paper_trading", "view_analytics", "create_strategies"]
        elif self.role == UserRole.ANALYST:
            return base_permissions + ["view_analytics", "create_reports", "view_all_data"]
        elif self.role == UserRole.ADMIN:
            return base_permissions + ["user_management", "system_admin", "view_all_data", "approve_users"]
        elif self.role == UserRole.SUPER_ADMIN:
            return ["*"]  # All permissions
        else:
            return base_permissions

@dataclass
class UserApproval:
    """User approval request"""
    id: str
    user_id: str
    requested_by: str
    requested_at: datetime
    status: str = "pending"  # pending, approved, rejected
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    notes: Optional[str] = None
    kyc_verified: bool = False
    documents_verified: bool = False
    risk_assessment: Optional[str] = None

class UserManager:
    """Main user management system"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.users: Dict[str, UserProfile] = {}
        self.approvals: Dict[str, UserApproval] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        
    async def create_user(self, user_data: Dict[str, Any]) -> Tuple[bool, str, Optional[str]]:
        """Create a new user"""
        try:
            # Validate required fields
            required_fields = ['firebase_uid', 'email', 'username', 'first_name', 'last_name']
            for field in required_fields:
                if field not in user_data:
                    return False, f"Missing required field: {field}", None
            
            # Check if user already exists
            if await self._user_exists(user_data['firebase_uid']):
                return False, "User already exists", None
            
            # Check if username is available
            if await self._username_exists(user_data['username']):
                return False, "Username already taken", None
            
            # Create user profile
            user_id = str(uuid.uuid4())
            user_profile = UserProfile(
                id=user_id,
                firebase_uid=user_data['firebase_uid'],
                email=user_data['email'],
                username=user_data['username'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                phone=user_data.get('phone'),
                role=UserRole(user_data.get('role', 'user')),
                tenant_id=user_data.get('tenant_id', 'default'),
                preferences=user_data.get('preferences', {})
            )
            
            # Store user
            self.users[user_id] = user_profile
            
            # Create approval request if needed
            if user_profile.role in [UserRole.TRADER, UserRole.ANALYST, UserRole.ADMIN]:
                await self._create_approval_request(user_id, user_data.get('requested_by', 'system'))
            
            logger.info(f"User created: {user_id}")
            return True, "User created successfully", user_id
            
        except Exception as e:
            logger.error(f"User creation error: {e}")
            return False, f"User creation failed: {str(e)}", None
    
    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by ID"""
        try:
            if user_id not in self.users:
                return None
            
            user = self.users[user_id]
            return asdict(user)
            
        except Exception as e:
            logger.error(f"Get user error: {e}")
            return None
    
    async def get_user_by_firebase_uid(self, firebase_uid: str) -> Optional[Dict[str, Any]]:
        """Get user profile by Firebase UID"""
        try:
            for user in self.users.values():
                if user.firebase_uid == firebase_uid:
                    return asdict(user)
            return None
            
        except Exception as e:
            logger.error(f"Get user by Firebase UID error: {e}")
            return None
    
    async def update_user(self, user_id: str, update_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Update user profile"""
        try:
            if user_id not in self.users:
                return False, "User not found"
            
            user = self.users[user_id]
            
            # Update allowed fields
            allowed_fields = [
                'first_name', 'last_name', 'phone', 'timezone', 'language',
                'preferences', 'profile_picture'
            ]
            
            for field in allowed_fields:
                if field in update_data:
                    setattr(user, field, update_data[field])
            
            user.updated_at = datetime.utcnow()
            
            logger.info(f"User updated: {user_id}")
            return True, "User updated successfully"
            
        except Exception as e:
            logger.error(f"User update error: {e}")
            return False, f"User update failed: {str(e)}"
    
    async def approve_user(self, user_id: str, admin_id: str, notes: Optional[str] = None) -> Tuple[bool, str]:
        """Approve a user"""
        try:
            if user_id not in self.users:
                return False, "User not found"
            
            user = self.users[user_id]
            
            # Update user status
            user.status = UserStatus.ACTIVE
            user.is_approved = True
            user.approval_date = datetime.utcnow()
            user.approved_by = admin_id
            user.updated_at = datetime.utcnow()
            
            # Update approval request
            approval_id = await self._get_approval_id(user_id)
            if approval_id and approval_id in self.approvals:
                approval = self.approvals[approval_id]
                approval.status = "approved"
                approval.reviewed_by = admin_id
                approval.reviewed_at = datetime.utcnow()
                approval.notes = notes
            
            logger.info(f"User approved: {user_id} by {admin_id}")
            return True, "User approved successfully"
            
        except Exception as e:
            logger.error(f"User approval error: {e}")
            return False, f"User approval failed: {str(e)}"
    
    async def reject_user(self, user_id: str, admin_id: str, reason: str) -> Tuple[bool, str]:
        """Reject a user"""
        try:
            if user_id not in self.users:
                return False, "User not found"
            
            user = self.users[user_id]
            
            # Update user status
            user.status = UserStatus.SUSPENDED
            user.is_approved = False
            user.updated_at = datetime.utcnow()
            
            # Update approval request
            approval_id = await self._get_approval_id(user_id)
            if approval_id and approval_id in self.approvals:
                approval = self.approvals[approval_id]
                approval.status = "rejected"
                approval.reviewed_by = admin_id
                approval.reviewed_at = datetime.utcnow()
                approval.notes = reason
            
            logger.info(f"User rejected: {user_id} by {admin_id}")
            return True, "User rejected successfully"
            
        except Exception as e:
            logger.error(f"User rejection error: {e}")
            return False, f"User rejection failed: {str(e)}"
    
    async def suspend_user(self, user_id: str, admin_id: str, reason: str) -> Tuple[bool, str]:
        """Suspend a user"""
        try:
            if user_id not in self.users:
                return False, "User not found"
            
            user = self.users[user_id]
            user.status = UserStatus.SUSPENDED
            user.updated_at = datetime.utcnow()
            
            logger.info(f"User suspended: {user_id} by {admin_id}")
            return True, "User suspended successfully"
            
        except Exception as e:
            logger.error(f"User suspension error: {e}")
            return False, f"User suspension failed: {str(e)}"
    
    async def activate_user(self, user_id: str, admin_id: str) -> Tuple[bool, str]:
        """Activate a suspended user"""
        try:
            if user_id not in self.users:
                return False, "User not found"
            
            user = self.users[user_id]
            user.status = UserStatus.ACTIVE
            user.updated_at = datetime.utcnow()
            
            logger.info(f"User activated: {user_id} by {admin_id}")
            return True, "User activated successfully"
            
        except Exception as e:
            logger.error(f"User activation error: {e}")
            return False, f"User activation failed: {str(e)}"
    
    async def update_user_role(self, user_id: str, new_role: str, admin_id: str) -> Tuple[bool, str]:
        """Update user role"""
        try:
            if user_id not in self.users:
                return False, "User not found"
            
            user = self.users[user_id]
            old_role = user.role
            user.role = UserRole(new_role)
            user.permissions = user._get_default_permissions()
            user.updated_at = datetime.utcnow()
            
            logger.info(f"User role updated: {user_id} from {old_role} to {new_role} by {admin_id}")
            return True, "User role updated successfully"
            
        except Exception as e:
            logger.error(f"User role update error: {e}")
            return False, f"User role update failed: {str(e)}"
    
    async def get_pending_approvals(self) -> List[Dict[str, Any]]:
        """Get all pending approval requests"""
        try:
            pending_approvals = []
            
            for approval_id, approval in self.approvals.items():
                if approval.status == "pending":
                    user = self.users.get(approval.user_id)
                    if user:
                        approval_data = asdict(approval)
                        approval_data['user'] = asdict(user)
                        pending_approvals.append(approval_data)
            
            return pending_approvals
            
        except Exception as e:
            logger.error(f"Get pending approvals error: {e}")
            return []
    
    async def get_all_users(self, admin_id: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get all users with optional filtering"""
        try:
            # Check if admin has permission
            admin_user = await self._get_user_by_id(admin_id)
            if not admin_user or admin_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
                return []
            
            users_data = []
            for user in self.users.values():
                user_data = asdict(user)
                
                # Apply filters
                if filters:
                    if not self._apply_filters(user_data, filters):
                        continue
                
                users_data.append(user_data)
            
            return users_data
            
        except Exception as e:
            logger.error(f"Get all users error: {e}")
            return []
    
    async def get_user_statistics(self) -> Dict[str, Any]:
        """Get user statistics"""
        try:
            total_users = len(self.users)
            active_users = len([u for u in self.users.values() if u.status == UserStatus.ACTIVE])
            pending_users = len([u for u in self.users.values() if u.status == UserStatus.PENDING])
            suspended_users = len([u for u in self.users.values() if u.status == UserStatus.SUSPENDED])
            
            role_distribution = {}
            for user in self.users.values():
                role = user.role.value
                role_distribution[role] = role_distribution.get(role, 0) + 1
            
            kyc_status_distribution = {}
            for user in self.users.values():
                status = user.kyc_status.value
                kyc_status_distribution[status] = kyc_status_distribution.get(status, 0) + 1
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'pending_users': pending_users,
                'suspended_users': suspended_users,
                'role_distribution': role_distribution,
                'kyc_status_distribution': kyc_status_distribution,
                'approval_requests': len([a for a in self.approvals.values() if a.status == "pending"])
            }
            
        except Exception as e:
            logger.error(f"Get user statistics error: {e}")
            return {
                'total_users': 0,
                'active_users': 0,
                'pending_users': 0,
                'suspended_users': 0,
                'role_distribution': {},
                'kyc_status_distribution': {},
                'approval_requests': 0
            }
    
    async def check_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has a specific permission"""
        try:
            if user_id not in self.users:
                return False
            
            user = self.users[user_id]
            
            # Super admin has all permissions
            if user.role == UserRole.SUPER_ADMIN:
                return True
            
            # Check if permission is in user's permission list
            return permission in user.permissions
            
        except Exception as e:
            logger.error(f"Permission check error: {e}")
            return False
    
    async def add_trading_account(self, user_id: str, account_id: str) -> Tuple[bool, str]:
        """Add trading account to user"""
        try:
            if user_id not in self.users:
                return False, "User not found"
            
            user = self.users[user_id]
            if account_id not in user.trading_accounts:
                user.trading_accounts.append(account_id)
                user.updated_at = datetime.utcnow()
            
            return True, "Trading account added successfully"
            
        except Exception as e:
            logger.error(f"Add trading account error: {e}")
            return False, f"Add trading account failed: {str(e)}"
    
    async def add_portfolio(self, user_id: str, portfolio_id: str) -> Tuple[bool, str]:
        """Add portfolio to user"""
        try:
            if user_id not in self.users:
                return False, "User not found"
            
            user = self.users[user_id]
            if portfolio_id not in user.portfolios:
                user.portfolios.append(portfolio_id)
                user.updated_at = datetime.utcnow()
            
            return True, "Portfolio added successfully"
            
        except Exception as e:
            logger.error(f"Add portfolio error: {e}")
            return False, f"Add portfolio failed: {str(e)}"
    
    async def add_ai_agent(self, user_id: str, agent_id: str) -> Tuple[bool, str]:
        """Add AI agent to user"""
        try:
            if user_id not in self.users:
                return False, "User not found"
            
            user = self.users[user_id]
            if agent_id not in user.ai_agents:
                user.ai_agents.append(agent_id)
                user.updated_at = datetime.utcnow()
            
            return True, "AI agent added successfully"
            
        except Exception as e:
            logger.error(f"Add AI agent error: {e}")
            return False, f"Add AI agent failed: {str(e)}"
    
    # Helper methods
    async def _user_exists(self, firebase_uid: str) -> bool:
        """Check if user exists by Firebase UID"""
        return any(user.firebase_uid == firebase_uid for user in self.users.values())
    
    async def _username_exists(self, username: str) -> bool:
        """Check if username is already taken"""
        return any(user.username == username for user in self.users.values())
    
    async def _create_approval_request(self, user_id: str, requested_by: str) -> str:
        """Create approval request for user"""
        approval_id = str(uuid.uuid4())
        approval = UserApproval(
            id=approval_id,
            user_id=user_id,
            requested_by=requested_by,
            requested_at=datetime.utcnow()
        )
        self.approvals[approval_id] = approval
        return approval_id
    
    async def _get_approval_id(self, user_id: str) -> Optional[str]:
        """Get approval ID for user"""
        for approval_id, approval in self.approvals.items():
            if approval.user_id == user_id:
                return approval_id
        return None
    
    async def _get_user_by_id(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by ID"""
        return self.users.get(user_id)
    
    def _apply_filters(self, user_data: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Apply filters to user data"""
        try:
            for key, value in filters.items():
                if key in user_data:
                    if isinstance(value, list):
                        if user_data[key] not in value:
                            return False
                    else:
                        if user_data[key] != value:
                            return False
            return True
        except Exception:
            return True  # If filter fails, include the user 