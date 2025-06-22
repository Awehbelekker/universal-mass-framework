"""
MASS Framework - Automated Social Login Setup & Integration System
================================================================

One-click social login setup that automatically configures OAuth providers,
generates landing pages, and handles user registration/login flow seamlessly.

Features:
- One-click OAuth provider setup
- Automatic landing page generation
- Smart user sync across platforms
- Auto-registration with profile data
- Customizable login UI components
- Real-time authentication status
- Social profile integration
- Multi-app support with shared authentication
"""

import os
import json
import asyncio
import aiohttp
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import jwt
from urllib.parse import urlencode, quote
import base64
import requests
from jinja2 import Template
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SocialProvider(Enum):
    """Supported social login providers"""
    GOOGLE = "google"
    FACEBOOK = "facebook"
    GITHUB = "github"
    MICROSOFT = "microsoft"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    APPLE = "apple"
    DISCORD = "discord"
    TWITCH = "twitch"

class LoginTheme(Enum):
    """Login page themes"""
    MODERN = "modern"
    MINIMAL = "minimal"
    CORPORATE = "corporate"
    COLORFUL = "colorful"
    DARK = "dark"
    CUSTOM = "custom"

@dataclass
class SocialProviderConfig:
    """Social provider configuration"""
    provider: SocialProvider
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: List[str] = field(default_factory=list)
    enabled: bool = True
    auto_register: bool = True
    sync_profile: bool = True
    button_text: str = ""
    button_color: str = ""
    icon_url: str = ""

@dataclass
class UserProfile:
    """Unified user profile from social providers"""
    user_id: str
    email: str
    name: str
    first_name: str = ""
    last_name: str = ""
    avatar_url: str = ""
    provider: SocialProvider = None
    provider_id: str = ""
    verified: bool = False
    locale: str = "en"
    timezone: str = ""
    created_at: datetime = None
    last_login: datetime = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class LoginPageConfig:
    """Login page configuration"""
    app_name: str
    app_logo: str = ""
    theme: LoginTheme = LoginTheme.MODERN
    background_image: str = ""
    primary_color: str = "#007bff"
    secondary_color: str = "#6c757d"
    custom_css: str = ""
    welcome_message: str = "Welcome! Sign in to continue"
    privacy_policy_url: str = ""
    terms_of_service_url: str = ""
    support_email: str = ""
    enable_remember_me: bool = True
    enable_guest_mode: bool = False
    redirect_after_login: str = "/dashboard"

class AutoSocialLoginSetup:
    """Automated social login setup and management system"""
    
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.providers: Dict[SocialProvider, SocialProviderConfig] = {}
        self.users: Dict[str, UserProfile] = {}
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.login_config = LoginPageConfig(app_name="MASS Framework App")
        
        # Initialize provider templates
        self._init_provider_templates()
    
    def _init_provider_templates(self):
        """Initialize OAuth provider templates with default configurations"""
        self.provider_templates = {
            SocialProvider.GOOGLE: {
                'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
                'token_url': 'https://oauth2.googleapis.com/token',
                'user_info_url': 'https://www.googleapis.com/oauth2/v2/userinfo',
                'scopes': ['openid', 'email', 'profile'],
                'button_text': 'Sign in with Google',
                'button_color': '#db4437',
                'icon_url': '/static/icons/google.svg'
            },
            SocialProvider.FACEBOOK: {
                'auth_url': 'https://www.facebook.com/v18.0/dialog/oauth',
                'token_url': 'https://graph.facebook.com/v18.0/oauth/access_token',
                'user_info_url': 'https://graph.facebook.com/me',
                'scopes': ['email', 'public_profile'],
                'button_text': 'Continue with Facebook',
                'button_color': '#1877f2',
                'icon_url': '/static/icons/facebook.svg'
            },
            SocialProvider.GITHUB: {
                'auth_url': 'https://github.com/login/oauth/authorize',
                'token_url': 'https://github.com/login/oauth/access_token',
                'user_info_url': 'https://api.github.com/user',
                'scopes': ['user:email'],
                'button_text': 'Sign in with GitHub',
                'button_color': '#333',
                'icon_url': '/static/icons/github.svg'
            },
            SocialProvider.MICROSOFT: {
                'auth_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
                'token_url': 'https://login.microsoftonline.com/common/oauth2/v2.0/token',
                'user_info_url': 'https://graph.microsoft.com/v1.0/me',
                'scopes': ['openid', 'email', 'profile'],
                'button_text': 'Sign in with Microsoft',
                'button_color': '#0078d4',
                'icon_url': '/static/icons/microsoft.svg'
            },
            SocialProvider.LINKEDIN: {
                'auth_url': 'https://www.linkedin.com/oauth/v2/authorization',
                'token_url': 'https://www.linkedin.com/oauth/v2/accessToken',
                'user_info_url': 'https://api.linkedin.com/v2/people/~',
                'scopes': ['r_liteprofile', 'r_emailaddress'],
                'button_text': 'Sign in with LinkedIn',
                'button_color': '#0077b5',
                'icon_url': '/static/icons/linkedin.svg'
            },
            SocialProvider.TWITTER: {
                'auth_url': 'https://twitter.com/i/oauth2/authorize',
                'token_url': 'https://api.twitter.com/2/oauth2/token',
                'user_info_url': 'https://api.twitter.com/2/users/me',
                'scopes': ['tweet.read', 'users.read'],
                'button_text': 'Sign in with X (Twitter)',
                'button_color': '#1da1f2',
                'icon_url': '/static/icons/twitter.svg'
            }
        }
    
    async def quick_setup(
        self, 
        providers: List[Tuple[SocialProvider, str, str]], 
        domain: str,
        page_config: Optional[LoginPageConfig] = None
    ) -> Dict[str, Any]:
        """Quick setup for multiple social providers"""
        
        logger.info(f"Starting quick setup for {len(providers)} providers")
        
        # Update login page config
        if page_config:
            self.login_config = page_config
        
        setup_results = []
        
        for provider, client_id, client_secret in providers:
            try:
                # Configure provider
                redirect_uri = f"https://{domain}/auth/{provider.value}/callback"
                template = self.provider_templates[provider]
                
                config = SocialProviderConfig(
                    provider=provider,
                    client_id=client_id,
                    client_secret=client_secret,
                    redirect_uri=redirect_uri,
                    scopes=template['scopes'],
                    button_text=template['button_text'],
                    button_color=template['button_color'],
                    icon_url=template['icon_url']
                )
                
                self.providers[provider] = config
                
                # Test configuration
                test_result = await self._test_provider_config(config)
                
                setup_results.append({
                    'provider': provider.value,
                    'status': 'success' if test_result else 'warning',
                    'message': 'Configuration saved' if test_result else 'Config saved but test failed',
                    'auth_url': self._get_auth_url(provider),
                    'callback_url': redirect_uri
                })
                
                logger.info(f"Provider {provider.value} configured successfully")
                
            except Exception as e:
                setup_results.append({
                    'provider': provider.value,
                    'status': 'error',
                    'message': str(e)
                })
                logger.error(f"Failed to configure {provider.value}: {e}")
        
        # Generate login page
        login_page_html = self.generate_login_page()
        
        # Generate API endpoints
        api_endpoints = self._generate_api_endpoints()
        
        # Save configuration
        await self._save_configuration()
        
        return {
            'setup_results': setup_results,
            'login_page': login_page_html,
            'api_endpoints': api_endpoints,
            'total_providers': len(providers),
            'successful_providers': len([r for r in setup_results if r['status'] == 'success']),
            'configuration_saved': True
        }
    
    def generate_login_page(self) -> str:
        """Generate complete login page HTML"""
        
        template = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ config.app_name }} - Sign In</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: {{ 'url(' + config.background_image + ')' if config.background_image else 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }};
            background-size: cover;
            background-position: center;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .login-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            max-width: 400px;
            width: 100%;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        .logo {
            width: 80px;
            height: 80px;
            margin: 0 auto 20px;
            border-radius: 50%;
            background: {{ config.primary_color }};
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: white;
        }
        
        .app-name {
            font-size: 28px;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
        }
        
        .welcome-message {
            color: #718096;
            margin-bottom: 30px;
            font-size: 16px;
        }
        
        .social-buttons {
            display: flex;
            flex-direction: column;
            gap: 15px;
        }
        
        .social-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 15px 20px;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            text-decoration: none;
            color: white;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .social-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        
        .social-btn i {
            margin-right: 12px;
            font-size: 18px;
        }
        
        .divider {
            margin: 30px 0;
            position: relative;
            text-align: center;
        }
        
        .divider::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 0;
            right: 0;
            height: 1px;
            background: #e2e8f0;
        }
        
        .divider span {
            background: rgba(255, 255, 255, 0.95);
            padding: 0 20px;
            color: #718096;
            font-size: 14px;
        }
        
        .footer-links {
            margin-top: 30px;
            font-size: 14px;
        }
        
        .footer-links a {
            color: #718096;
            text-decoration: none;
            margin: 0 10px;
        }
        
        .footer-links a:hover {
            color: {{ config.primary_color }};
        }
        
        .status-indicator {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 14px;
            font-weight: 600;
            color: white;
            background: #48bb78;
            display: none;
        }
        
        .status-indicator.show {
            display: block;
            animation: slideIn 0.3s ease;
        }
        
        @keyframes slideIn {
            from { transform: translateX(100%); }
            to { transform: translateX(0); }
        }
        
        {{ config.custom_css }}
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            {% if config.app_logo %}
                <img src="{{ config.app_logo }}" alt="{{ config.app_name }}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">
            {% else %}
                <i class="fas fa-rocket"></i>
            {% endif %}
        </div>
        
        <h1 class="app-name">{{ config.app_name }}</h1>
        <p class="welcome-message">{{ config.welcome_message }}</p>
        
        <div class="social-buttons">
            {% for provider in providers %}
            <a href="/auth/{{ provider.provider.value }}/login" 
               class="social-btn" 
               style="background-color: {{ provider.button_color }};"
               onclick="showStatus('Connecting to {{ provider.provider.value }}...')">
                <i class="{{ provider_icons[provider.provider.value] }}"></i>
                {{ provider.button_text }}
            </a>
            {% endfor %}
        </div>
        
        {% if config.enable_guest_mode %}
        <div class="divider">
            <span>or</span>
        </div>
        
        <a href="/guest" class="social-btn" style="background-color: {{ config.secondary_color }};">
            <i class="fas fa-user"></i>
            Continue as Guest
        </a>
        {% endif %}
        
        <div class="footer-links">
            {% if config.privacy_policy_url %}
            <a href="{{ config.privacy_policy_url }}">Privacy Policy</a>
            {% endif %}
            {% if config.terms_of_service_url %}
            <a href="{{ config.terms_of_service_url }}">Terms of Service</a>
            {% endif %}
            {% if config.support_email %}
            <a href="mailto:{{ config.support_email }}">Support</a>
            {% endif %}
        </div>
    </div>
    
    <div class="status-indicator" id="statusIndicator"></div>
    
    <script>
        function showStatus(message) {
            const indicator = document.getElementById('statusIndicator');
            indicator.textContent = message;
            indicator.classList.add('show');
            
            setTimeout(() => {
                indicator.classList.remove('show');
            }, 3000);
        }
        
        // Handle OAuth callbacks
        const urlParams = new URLSearchParams(window.location.search);
        const error = urlParams.get('error');
        const success = urlParams.get('success');
        
        if (error) {
            showStatus('Login failed: ' + error);
        } else if (success) {
            showStatus('Login successful! Redirecting...');
            setTimeout(() => {
                window.location.href = '{{ config.redirect_after_login }}';
            }, 1500);
        }
        
        // Auto-detect system theme
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.body.style.filter = 'invert(0.1)';
        }
    </script>
</body>
</html>""")
        
        provider_icons = {
            'google': 'fab fa-google',
            'facebook': 'fab fa-facebook-f',
            'github': 'fab fa-github',
            'microsoft': 'fab fa-microsoft',
            'linkedin': 'fab fa-linkedin-in',
            'twitter': 'fab fa-twitter',
            'apple': 'fab fa-apple',
            'discord': 'fab fa-discord',
            'twitch': 'fab fa-twitch'
        }
        
        return template.render(
            config=self.login_config,
            providers=list(self.providers.values()),
            provider_icons=provider_icons
        )
    
    def _get_auth_url(self, provider: SocialProvider) -> str:
        """Generate OAuth authorization URL"""
        config = self.providers[provider]
        template = self.provider_templates[provider]
        
        params = {
            'client_id': config.client_id,
            'redirect_uri': config.redirect_uri,
            'scope': ' '.join(config.scopes),
            'response_type': 'code',
            'state': self._generate_state_token(provider)
        }
        
        # Provider-specific parameters
        if provider == SocialProvider.GOOGLE:
            params['access_type'] = 'offline'
            params['prompt'] = 'consent'
        elif provider == SocialProvider.MICROSOFT:
            params['response_mode'] = 'query'
        elif provider == SocialProvider.FACEBOOK:
            params['display'] = 'popup'
        
        return f"{template['auth_url']}?{urlencode(params)}"
    
    async def handle_oauth_callback(
        self, 
        provider: SocialProvider, 
        code: str, 
        state: str
    ) -> Dict[str, Any]:
        """Handle OAuth callback and complete authentication"""
        
        # Verify state token
        if not self._verify_state_token(state, provider):
            raise ValueError("Invalid state token")
        
        config = self.providers[provider]
        template = self.provider_templates[provider]
        
        # Exchange code for access token
        token_data = await self._exchange_code_for_token(provider, code)
        access_token = token_data.get('access_token')
        
        if not access_token:
            raise ValueError("Failed to obtain access token")
        
        # Get user profile
        user_profile = await self._get_user_profile(provider, access_token)
        
        # Check if user exists or create new user
        existing_user = self._find_user_by_provider(provider, user_profile['id'])
        
        if existing_user:
            # Update existing user
            existing_user.last_login = datetime.utcnow()
            if config.sync_profile:
                existing_user.name = user_profile.get('name', existing_user.name)
                existing_user.avatar_url = user_profile.get('picture', existing_user.avatar_url)
            user = existing_user
        else:
            # Create new user
            if config.auto_register:
                user = UserProfile(
                    user_id=self._generate_user_id(),
                    email=user_profile.get('email', ''),
                    name=user_profile.get('name', ''),
                    first_name=user_profile.get('given_name', ''),
                    last_name=user_profile.get('family_name', ''),
                    avatar_url=user_profile.get('picture', ''),
                    provider=provider,
                    provider_id=user_profile['id'],
                    verified=user_profile.get('verified_email', False),
                    locale=user_profile.get('locale', 'en'),
                    created_at=datetime.utcnow(),
                    last_login=datetime.utcnow(),
                    metadata=user_profile
                )
                self.users[user.user_id] = user
            else:
                raise ValueError("Auto-registration is disabled")
        
        # Create session
        session_token = self._create_session(user)
        
        # Save user data
        await self._save_user_profile(user)
        
        return {
            'success': True,
            'user': self._user_to_dict(user),
            'session_token': session_token,
            'redirect_url': self.login_config.redirect_after_login
        }
    
    async def _exchange_code_for_token(self, provider: SocialProvider, code: str) -> Dict[str, Any]:
        """Exchange authorization code for access token"""
        config = self.providers[provider]
        template = self.provider_templates[provider]
        
        data = {
            'client_id': config.client_id,
            'client_secret': config.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': config.redirect_uri
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(template['token_url'], data=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise ValueError(f"Token exchange failed: {response.status}")
    
    async def _get_user_profile(self, provider: SocialProvider, access_token: str) -> Dict[str, Any]:
        """Get user profile from provider"""
        template = self.provider_templates[provider]
        
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Provider-specific adjustments
        if provider == SocialProvider.FACEBOOK:
            url = f"{template['user_info_url']}?fields=id,name,email,first_name,last_name,picture"
        else:
            url = template['user_info_url']
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise ValueError(f"Failed to get user profile: {response.status}")
    
    def _generate_api_endpoints(self) -> Dict[str, str]:
        """Generate API endpoint documentation"""
        endpoints = {
            'login_page': '/auth/login',
            'logout': '/auth/logout',
            'user_profile': '/auth/user',
            'session_check': '/auth/session',
        }
        
        for provider in self.providers.keys():
            provider_name = provider.value
            endpoints[f'{provider_name}_login'] = f'/auth/{provider_name}/login'
            endpoints[f'{provider_name}_callback'] = f'/auth/{provider_name}/callback'
        
        return endpoints
    
    def _generate_state_token(self, provider: SocialProvider) -> str:
        """Generate secure state token for OAuth"""
        data = {
            'provider': provider.value,
            'timestamp': datetime.utcnow().isoformat(),
            'random': secrets.token_hex(16)
        }
        return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()
    
    def _verify_state_token(self, state: str, provider: SocialProvider) -> bool:
        """Verify state token"""
        try:
            data = json.loads(base64.urlsafe_b64decode(state.encode()).decode())
            return (
                data['provider'] == provider.value and
                datetime.fromisoformat(data['timestamp']) > datetime.utcnow() - timedelta(hours=1)
            )
        except:
            return False
    
    def _generate_user_id(self) -> str:
        """Generate unique user ID"""
        return hashlib.md5(f"{datetime.utcnow().isoformat()}{secrets.token_hex(16)}".encode()).hexdigest()
    
    def _find_user_by_provider(self, provider: SocialProvider, provider_id: str) -> Optional[UserProfile]:
        """Find user by social provider ID"""
        for user in self.users.values():
            if user.provider == provider and user.provider_id == provider_id:
                return user
        return None
    
    def _create_session(self, user: UserProfile) -> str:
        """Create user session"""
        session_data = {
            'user_id': user.user_id,
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': (datetime.utcnow() + timedelta(days=30)).isoformat()
        }
        session_token = jwt.encode(session_data, self.app_secret, algorithm='HS256')
        self.sessions[session_token] = session_data
        return session_token
    
    async def _test_provider_config(self, config: SocialProviderConfig) -> bool:
        """Test provider configuration"""
        # Basic validation
        return bool(config.client_id and config.client_secret and config.redirect_uri)
    
    async def _save_configuration(self) -> None:
        """Save configuration to file"""
        config_data = {
            'app_id': self.app_id,
            'providers': {
                provider.value: {
                    'client_id': config.client_id,
                    'client_secret': config.client_secret,
                    'redirect_uri': config.redirect_uri,
                    'scopes': config.scopes,
                    'enabled': config.enabled,
                    'auto_register': config.auto_register,
                    'sync_profile': config.sync_profile
                }
                for provider, config in self.providers.items()
            },
            'login_config': {
                'app_name': self.login_config.app_name,
                'theme': self.login_config.theme.value,
                'primary_color': self.login_config.primary_color,
                'welcome_message': self.login_config.welcome_message,
                'redirect_after_login': self.login_config.redirect_after_login
            }
        }
        
        os.makedirs('./config', exist_ok=True)
        with open(f'./config/social_auth_{self.app_id}.json', 'w') as f:
            json.dump(config_data, f, indent=2)
    
    async def _save_user_profile(self, user: UserProfile) -> None:
        """Save user profile"""
        os.makedirs('./users', exist_ok=True)
        with open(f'./users/{user.user_id}.json', 'w') as f:
            json.dump(self._user_to_dict(user), f, indent=2, default=str)
    
    def _user_to_dict(self, user: UserProfile) -> Dict[str, Any]:
        """Convert user profile to dictionary"""
        return {
            'user_id': user.user_id,
            'email': user.email,
            'name': user.name,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'avatar_url': user.avatar_url,
            'provider': user.provider.value if user.provider else None,
            'provider_id': user.provider_id,
            'verified': user.verified,
            'locale': user.locale,
            'timezone': user.timezone,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'metadata': user.metadata
        }

# Usage example
if __name__ == "__main__":
    # Initialize the setup system
    app_setup = AutoSocialLoginSetup("my-app-123", "super-secret-key")
    
    # Configure login page
    login_config = LoginPageConfig(
        app_name="My Awesome App",
        theme=LoginTheme.MODERN,
        primary_color="#6366f1",
        welcome_message="Sign in to access your dashboard",
        redirect_after_login="/dashboard",
        enable_guest_mode=True
    )
    
    # Example quick setup (you would get these from OAuth provider consoles)
    providers = [
        (SocialProvider.GOOGLE, "your-google-client-id", "your-google-client-secret"),
        (SocialProvider.GITHUB, "your-github-client-id", "your-github-client-secret"),
        (SocialProvider.FACEBOOK, "your-facebook-app-id", "your-facebook-app-secret"),
    ]
    
    print("Automated Social Login Setup System")
    print("==================================")
    print("Features:")
    print("- One-click OAuth provider setup")
    print("- Automatic login page generation")
    print("- Smart user registration and sync")
    print("- Multi-provider authentication")
    print("- Customizable UI themes")
    print("- Session management")
    print("- Real-time status updates")
    print("\nRun quick_setup() to configure your social login providers!")
