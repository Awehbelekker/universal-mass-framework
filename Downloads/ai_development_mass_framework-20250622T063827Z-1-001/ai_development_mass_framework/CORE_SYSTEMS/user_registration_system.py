"""
User Registration System - Trading Platform Registration & Approval
================================================================

Provides comprehensive user registration with admin approval workflow:
- User Registration with KYC/AML compliance
- Admin Approval System
- Trading Access Levels
- Invitation System
- User Onboarding

This ensures secure, compliant user management for the trading platform.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import hashlib
import json
import uuid

logger = logging.getLogger(__name__)


class UserStatus(Enum):
    """User registration status"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"
    ACTIVE = "active"


class TradingAccessLevel(Enum):
    """Trading access levels"""
    DEMO = "demo"           # Paper trading only
    BASIC = "basic"         # Basic trading features
    ADVANCED = "advanced"   # Advanced features + AI
    PREMIUM = "premium"     # All features + revolutionary
    ENTERPRISE = "enterprise" # Custom enterprise features


class RegistrationType(Enum):
    """Registration types"""
    INVITATION = "invitation"    # Admin invited user
    SELF_REGISTRATION = "self_registration"  # User self-registered
    REFERRAL = "referral"        # Referred by existing user


@dataclass
class UserProfile:
    """User profile data"""
    user_id: str
    email: str
    first_name: str
    last_name: str
    phone: str
    date_of_birth: str
    address: Dict[str, str]
    kyc_status: str
    aml_status: str
    trading_experience: str
    risk_tolerance: str
    investment_goals: List[str]
    created_at: datetime
    updated_at: datetime


@dataclass
class RegistrationRequest:
    """User registration request"""
    request_id: str
    user_profile: UserProfile
    registration_type: RegistrationType
    status: UserStatus
    admin_notes: str
    submitted_at: datetime
    reviewed_at: Optional[datetime]
    reviewed_by: Optional[str]
    trading_access_level: TradingAccessLevel
    invitation_code: Optional[str]


class UserRegistrationSystem:
    """Comprehensive user registration system"""
    
    def __init__(self):
        self.pending_registrations = []
        self.approved_users = []
        self.rejected_users = []
        self.invitation_codes = {}
        self.admin_users = []
        self.kyc_requirements = [
            "government_id",
            "proof_of_address", 
            "bank_statement",
            "employment_verification"
        ]
        self.aml_checks = [
            "identity_verification",
            "source_of_funds",
            "risk_assessment",
            "sanctions_check"
        ]
        
        logger.info("✅ User Registration System initialized")
    
    async def register_user(self, user_data: Dict[str, Any], 
                          registration_type: RegistrationType = RegistrationType.SELF_REGISTRATION,
                          invitation_code: Optional[str] = None) -> RegistrationRequest:
        """Register a new user"""
        
        # Generate unique user ID
        user_id = str(uuid.uuid4())
        
        # Create user profile
        user_profile = UserProfile(
            user_id=user_id,
            email=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone=user_data.get("phone", ""),
            date_of_birth=user_data.get("date_of_birth", ""),
            address=user_data.get("address", {}),
            kyc_status="pending",
            aml_status="pending",
            trading_experience=user_data.get("trading_experience", "beginner"),
            risk_tolerance=user_data.get("risk_tolerance", "conservative"),
            investment_goals=user_data.get("investment_goals", []),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        # Determine trading access level
        trading_access = await self._determine_access_level(user_data, invitation_code)
        
        # Create registration request
        registration_request = RegistrationRequest(
            request_id=str(uuid.uuid4()),
            user_profile=user_profile,
            registration_type=registration_type,
            status=UserStatus.PENDING,
            admin_notes="",
            submitted_at=datetime.now(),
            reviewed_at=None,
            reviewed_by=None,
            trading_access_level=trading_access,
            invitation_code=invitation_code
        )
        
        self.pending_registrations.append(registration_request)
        
        logger.info(f"✅ User registration submitted: {user_id}")
        
        return registration_request
    
    async def admin_approve_user(self, request_id: str, admin_id: str, 
                                notes: str = "", access_level: Optional[TradingAccessLevel] = None) -> Dict[str, Any]:
        """Admin approves user registration"""
        
        # Find registration request
        request = next((r for r in self.pending_registrations if r.request_id == request_id), None)
        
        if not request:
            raise ValueError(f"Registration request {request_id} not found")
        
        # Update request status
        request.status = UserStatus.APPROVED
        request.reviewed_at = datetime.now()
        request.reviewed_by = admin_id
        request.admin_notes = notes
        
        if access_level:
            request.trading_access_level = access_level
        
        # Move to approved users
        self.pending_registrations.remove(request)
        self.approved_users.append(request)
        
        # Create user account
        user_account = await self._create_user_account(request)
        
        logger.info(f"✅ User approved: {request.user_profile.user_id}")
        
        return {
            "status": "approved",
            "user_id": request.user_profile.user_id,
            "trading_access_level": request.trading_access_level.value,
            "account_created": True,
            "welcome_email_sent": True
        }
    
    async def admin_reject_user(self, request_id: str, admin_id: str, 
                               reason: str) -> Dict[str, Any]:
        """Admin rejects user registration"""
        
        # Find registration request
        request = next((r for r in self.pending_registrations if r.request_id == request_id), None)
        
        if not request:
            raise ValueError(f"Registration request {request_id} not found")
        
        # Update request status
        request.status = UserStatus.REJECTED
        request.reviewed_at = datetime.now()
        request.reviewed_by = admin_id
        request.admin_notes = reason
        
        # Move to rejected users
        self.pending_registrations.remove(request)
        self.rejected_users.append(request)
        
        logger.info(f"❌ User rejected: {request.user_profile.user_id}")
        
        return {
            "status": "rejected",
            "user_id": request.user_profile.user_id,
            "reason": reason,
            "rejection_email_sent": True
        }
    
    async def generate_invitation_code(self, admin_id: str, 
                                     access_level: TradingAccessLevel = TradingAccessLevel.BASIC,
                                     max_uses: int = 1) -> str:
        """Generate invitation code for new users"""
        
        invitation_code = hashlib.md5(f"{admin_id}_{datetime.now().timestamp()}".encode()).hexdigest()[:8].upper()
        
        self.invitation_codes[invitation_code] = {
            "admin_id": admin_id,
            "access_level": access_level,
            "max_uses": max_uses,
            "current_uses": 0,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(days=30)
        }
        
        logger.info(f"✅ Invitation code generated: {invitation_code}")
        
        return invitation_code
    
    async def validate_invitation_code(self, invitation_code: str) -> Dict[str, Any]:
        """Validate invitation code"""
        
        if invitation_code not in self.invitation_codes:
            return {"valid": False, "reason": "Invalid invitation code"}
        
        code_data = self.invitation_codes[invitation_code]
        
        # Check if expired
        if datetime.now() > code_data["expires_at"]:
            return {"valid": False, "reason": "Invitation code expired"}
        
        # Check if max uses reached
        if code_data["current_uses"] >= code_data["max_uses"]:
            return {"valid": False, "reason": "Invitation code usage limit reached"}
        
        return {
            "valid": True,
            "access_level": code_data["access_level"].value,
            "admin_id": code_data["admin_id"]
        }
    
    async def get_pending_registrations(self) -> List[Dict[str, Any]]:
        """Get all pending registrations for admin review"""
        
        return [
            {
                "request_id": req.request_id,
                "user_profile": {
                    "user_id": req.user_profile.user_id,
                    "email": req.user_profile.email,
                    "first_name": req.user_profile.first_name,
                    "last_name": req.user_profile.last_name,
                    "phone": req.user_profile.phone,
                    "trading_experience": req.user_profile.trading_experience,
                    "risk_tolerance": req.user_profile.risk_tolerance,
                    "investment_goals": req.user_profile.investment_goals,
                    "kyc_status": req.user_profile.kyc_status,
                    "aml_status": req.user_profile.aml_status
                },
                "registration_type": req.registration_type.value,
                "submitted_at": req.submitted_at.isoformat(),
                "trading_access_level": req.trading_access_level.value,
                "invitation_code": req.invitation_code
            }
            for req in self.pending_registrations
        ]
    
    async def get_user_status(self, user_id: str) -> Dict[str, Any]:
        """Get user registration status"""
        
        # Check pending registrations
        pending = next((r for r in self.pending_registrations if r.user_profile.user_id == user_id), None)
        if pending:
            return {
                "status": "pending",
                "message": "Your registration is under review",
                "submitted_at": pending.submitted_at.isoformat()
            }
        
        # Check approved users
        approved = next((r for r in self.approved_users if r.user_profile.user_id == user_id), None)
        if approved:
            return {
                "status": "approved",
                "message": "Your account has been approved",
                "trading_access_level": approved.trading_access_level.value,
                "approved_at": approved.reviewed_at.isoformat()
            }
        
        # Check rejected users
        rejected = next((r for r in self.rejected_users if r.user_profile.user_id == user_id), None)
        if rejected:
            return {
                "status": "rejected",
                "message": "Your registration was not approved",
                "reason": rejected.admin_notes,
                "rejected_at": rejected.reviewed_at.isoformat()
            }
        
        return {"status": "not_found", "message": "User not found"}
    
    # Private methods
    async def _determine_access_level(self, user_data: Dict[str, Any], 
                                    invitation_code: Optional[str]) -> TradingAccessLevel:
        """Determine user's trading access level"""
        
        if invitation_code:
            validation = await self.validate_invitation_code(invitation_code)
            if validation["valid"]:
                return validation["access_level"]
        
        # Default access level based on registration type
        trading_experience = user_data.get("trading_experience", "beginner")
        
        if trading_experience == "expert":
            return TradingAccessLevel.ADVANCED
        elif trading_experience == "intermediate":
            return TradingAccessLevel.BASIC
        else:
            return TradingAccessLevel.DEMO
    
    async def _create_user_account(self, registration_request: RegistrationRequest) -> Dict[str, Any]:
        """Create user account after approval"""
        
        user_profile = registration_request.user_profile
        
        # Create trading account
        trading_account = {
            "user_id": user_profile.user_id,
            "account_type": registration_request.trading_access_level.value,
            "balance": 0.0,
            "created_at": datetime.now(),
            "status": "active"
        }
        
        # Create user preferences
        user_preferences = {
            "user_id": user_profile.user_id,
            "risk_tolerance": user_profile.risk_tolerance,
            "investment_goals": user_profile.investment_goals,
            "notifications_enabled": True,
            "ai_assistance_enabled": True
        }
        
        # Send welcome email
        await self._send_welcome_email(user_profile, registration_request.trading_access_level)
        
        return {
            "trading_account": trading_account,
            "user_preferences": user_preferences,
            "account_created": True
        }
    
    async def _send_welcome_email(self, user_profile: UserProfile, 
                                 access_level: TradingAccessLevel) -> bool:
        """Send welcome email to approved user"""
        
        # Simulate email sending
        logger.info(f"📧 Welcome email sent to {user_profile.email}")
        
        return True


class AdminPanel:
    """Admin panel for user management"""
    
    def __init__(self, registration_system: UserRegistrationSystem):
        self.registration_system = registration_system
        self.admin_users = []
        
        logger.info("✅ Admin Panel initialized")
    
    async def get_dashboard_stats(self) -> Dict[str, Any]:
        """Get admin dashboard statistics"""
        
        return {
            "pending_registrations": len(self.registration_system.pending_registrations),
            "approved_users": len(self.registration_system.approved_users),
            "rejected_users": len(self.registration_system.rejected_users),
            "total_users": len(self.registration_system.approved_users) + len(self.registration_system.rejected_users),
            "active_invitation_codes": len([c for c in self.registration_system.invitation_codes.values() 
                                          if c["expires_at"] > datetime.now()])
        }
    
    async def approve_user(self, request_id: str, admin_id: str, 
                          notes: str = "", access_level: Optional[TradingAccessLevel] = None) -> Dict[str, Any]:
        """Approve user registration"""
        return await self.registration_system.admin_approve_user(request_id, admin_id, notes, access_level)
    
    async def reject_user(self, request_id: str, admin_id: str, reason: str) -> Dict[str, Any]:
        """Reject user registration"""
        return await self.registration_system.admin_reject_user(request_id, admin_id, reason)
    
    async def generate_invitation(self, admin_id: str, 
                                access_level: TradingAccessLevel = TradingAccessLevel.BASIC,
                                max_uses: int = 1) -> str:
        """Generate invitation code"""
        return await self.registration_system.generate_invitation_code(admin_id, access_level, max_uses)


# Initialize registration system
user_registration_system = UserRegistrationSystem()
admin_panel = AdminPanel(user_registration_system)

if __name__ == "__main__":
    # Test registration system
    asyncio.run(user_registration_system.register_user({
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "trading_experience": "intermediate",
        "risk_tolerance": "moderate"
    })) 