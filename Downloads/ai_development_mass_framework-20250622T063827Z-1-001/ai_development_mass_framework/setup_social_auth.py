"""
Environment Setup Script for MASS Framework Social Authentication

This script helps users set up their environment for social media authentication
by providing templates, validation, and setup guidance.
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import secrets
import subprocess
import sys


@dataclass
class SocialProvider:
    name: str
    client_id_var: str
    client_secret_var: str
    redirect_uri_var: str
    setup_url: str
    instructions: List[str]


class SocialAuthSetup:
    """Setup and configuration helper for social authentication"""
    
    def __init__(self):
        self.providers = self._get_provider_configs()
        self.env_file = ".env"
        self.env_template_file = ".env.template"
    
    def _get_provider_configs(self) -> Dict[str, SocialProvider]:
        return {
            "google": SocialProvider(
                name="Google",
                client_id_var="GOOGLE_CLIENT_ID",
                client_secret_var="GOOGLE_CLIENT_SECRET",
                redirect_uri_var="GOOGLE_REDIRECT_URI",
                setup_url="https://console.developers.google.com/",
                instructions=[
                    "1. Go to Google Cloud Console",
                    "2. Create a new project or select existing",
                    "3. Enable Google+ API",
                    "4. Create OAuth2 credentials",
                    "5. Add your domain to authorized origins",
                    "6. Add redirect URI: http://localhost:8000/auth/google/callback"
                ]
            ),
            "facebook": SocialProvider(
                name="Facebook",
                client_id_var="FACEBOOK_CLIENT_ID",
                client_secret_var="FACEBOOK_CLIENT_SECRET",
                redirect_uri_var="FACEBOOK_REDIRECT_URI",
                setup_url="https://developers.facebook.com/",
                instructions=[
                    "1. Go to Facebook Developers",
                    "2. Create a new app",
                    "3. Add Facebook Login product",
                    "4. Configure OAuth redirect URIs",
                    "5. Add redirect URI: http://localhost:8000/auth/facebook/callback",
                    "6. Request email permission if needed"
                ]
            ),
            "github": SocialProvider(
                name="GitHub",
                client_id_var="GITHUB_CLIENT_ID",
                client_secret_var="GITHUB_CLIENT_SECRET",
                redirect_uri_var="GITHUB_REDIRECT_URI",
                setup_url="https://github.com/settings/developers",
                instructions=[
                    "1. Go to GitHub Developer Settings",
                    "2. Create a new OAuth App",
                    "3. Set Authorization callback URL",
                    "4. Add redirect URI: http://localhost:8000/auth/github/callback",
                    "5. Note Client ID and Client Secret"
                ]
            ),
            "microsoft": SocialProvider(
                name="Microsoft",
                client_id_var="MICROSOFT_CLIENT_ID",
                client_secret_var="MICROSOFT_CLIENT_SECRET",
                redirect_uri_var="MICROSOFT_REDIRECT_URI",
                setup_url="https://portal.azure.com/",
                instructions=[
                    "1. Go to Azure Portal",
                    "2. Create or select Azure AD app",
                    "3. Add platform configuration",
                    "4. Configure redirect URI",
                    "5. Add redirect URI: http://localhost:8000/auth/microsoft/callback",
                    "6. Grant necessary permissions"
                ]
            ),
            "linkedin": SocialProvider(
                name="LinkedIn",
                client_id_var="LINKEDIN_CLIENT_ID",
                client_secret_var="LINKEDIN_CLIENT_SECRET",
                redirect_uri_var="LINKEDIN_REDIRECT_URI",
                setup_url="https://www.linkedin.com/developers/",
                instructions=[
                    "1. Go to LinkedIn Developers",
                    "2. Create a new app",
                    "3. Request access to Sign In with LinkedIn",
                    "4. Configure authorized redirect URLs",
                    "5. Add redirect URI: http://localhost:8000/auth/linkedin/callback"
                ]
            ),
            "twitter": SocialProvider(
                name="Twitter",
                client_id_var="TWITTER_CLIENT_ID",
                client_secret_var="TWITTER_CLIENT_SECRET",
                redirect_uri_var="TWITTER_REDIRECT_URI",
                setup_url="https://developer.twitter.com/",
                instructions=[
                    "1. Go to Twitter Developer Portal",
                    "2. Create a new app",
                    "3. Enable OAuth 2.0",
                    "4. Configure callback URLs",
                    "5. Add redirect URI: http://localhost:8000/auth/twitter/callback",
                    "6. Note App ID and App Secret"
                ]
            )
        }
    
    def create_env_template(self) -> None:
        """Create .env template file with all required variables"""
        template_content = []
        template_content.append("# MASS Framework Environment Configuration")
        template_content.append("# Copy this file to .env and fill in your actual values")
        template_content.append("")
        
        # Core configuration
        template_content.append("# Core Configuration")
        template_content.append("JWT_SECRET=your-jwt-secret-key-here")
        template_content.append("DATABASE_URL=sqlite:///mass_framework.db")
        template_content.append("REDIS_URL=redis://localhost:6379")
        template_content.append("")
        
        # Social authentication providers
        template_content.append("# Social Authentication Providers")
        template_content.append("# Configure the providers you want to enable")
        template_content.append("")
        
        for key, provider in self.providers.items():
            template_content.append(f"# {provider.name} OAuth2 Configuration")
            template_content.append(f"# Setup URL: {provider.setup_url}")
            template_content.append(f"{provider.client_id_var}=your-{key}-client-id")
            template_content.append(f"{provider.client_secret_var}=your-{key}-client-secret")
            template_content.append(f"{provider.redirect_uri_var}=http://localhost:8000/auth/{key}/callback")
            template_content.append("")
        
        # Additional configuration
        template_content.append("# Optional Configuration")
        template_content.append("DEBUG=true")
        template_content.append("LOG_LEVEL=INFO")
        template_content.append("FRONTEND_URL=http://localhost:3000")
        template_content.append("API_URL=http://localhost:8000")
        template_content.append("")
        
        # Write template file
        with open(self.env_template_file, 'w') as f:
            f.write('\n'.join(template_content))
        
        print(f"✅ Created {self.env_template_file}")
        print(f"📋 Copy to {self.env_file} and configure your OAuth2 credentials")
    
    def validate_environment(self) -> Dict[str, Any]:
        """Validate current environment configuration"""
        validation_results = {
            "valid": True,
            "configured_providers": [],
            "missing_providers": [],
            "errors": []
        }
        
        # Check core variables
        core_vars = ["JWT_SECRET"]
        for var in core_vars:
            if not os.getenv(var):
                validation_results["errors"].append(f"Missing core variable: {var}")
                validation_results["valid"] = False
        
        # Check provider configurations
        for key, provider in self.providers.items():
            client_id = os.getenv(provider.client_id_var)
            client_secret = os.getenv(provider.client_secret_var)
            
            if client_id and client_secret:
                validation_results["configured_providers"].append({
                    "name": provider.name,
                    "key": key,
                    "client_id_set": bool(client_id),
                    "client_secret_set": bool(client_secret)
                })
            else:
                validation_results["missing_providers"].append({
                    "name": provider.name,
                    "key": key,
                    "client_id_var": provider.client_id_var,
                    "client_secret_var": provider.client_secret_var
                })
        
        return validation_results
    
    def print_setup_instructions(self, provider_key: Optional[str] = None) -> None:
        """Print setup instructions for specific provider or all providers"""
        if provider_key and provider_key in self.providers:
            providers_to_show = {provider_key: self.providers[provider_key]}
        else:
            providers_to_show = self.providers
        
        print("🔐 SOCIAL AUTHENTICATION SETUP INSTRUCTIONS")
        print("=" * 60)
        
        for key, provider in providers_to_show.items():
            print(f"\n📱 {provider.name} Setup:")
            print(f"Setup URL: {provider.setup_url}")
            print("Instructions:")
            for instruction in provider.instructions:
                print(f"  {instruction}")
            
            print(f"\nEnvironment Variables:")
            print(f"  {provider.client_id_var}=your-client-id")
            print(f"  {provider.client_secret_var}=your-client-secret")
            print(f"  {provider.redirect_uri_var}=http://localhost:8000/auth/{key}/callback")
    
    def install_dependencies(self) -> None:
        """Install required dependencies for social authentication"""
        dependencies = [
            "cryptography>=41.0.0",
            "authlib>=1.2.1",
            "passlib[bcrypt]>=1.7.4",
            "aiohttp>=3.9.0"
        ]
        
        print("📦 Installing social authentication dependencies...")
        
        for dep in dependencies:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"✅ Installed {dep}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {dep}: {e}")
    
    def generate_jwt_secret(self) -> str:
        """Generate a secure JWT secret"""
        return secrets.token_urlsafe(32)
    
    def setup_interactive(self) -> None:
        """Interactive setup wizard"""
        print("🚀 MASS Framework Social Authentication Setup Wizard")
        print("=" * 60)
        
        # Check if .env exists
        if os.path.exists(self.env_file):
            print(f"📁 Found existing {self.env_file}")
            overwrite = input("Do you want to update it? (y/N): ").lower().startswith('y')
            if not overwrite:
                print("Setup cancelled.")
                return
        
        # Create or update .env file
        env_content = {}
        
        # Load existing .env if it exists
        if os.path.exists(self.env_file):
            with open(self.env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key, value = line.strip().split('=', 1)
                        env_content[key] = value
        
        # Core configuration
        print("\n🔧 Core Configuration:")
        
        current_jwt = env_content.get("JWT_SECRET", "")
        if not current_jwt:
            jwt_secret = self.generate_jwt_secret()
            print(f"Generated JWT Secret: {jwt_secret[:20]}...")
            env_content["JWT_SECRET"] = jwt_secret
        else:
            print(f"Using existing JWT Secret: {current_jwt[:20]}...")
        
        # Database URL
        db_url = input(f"Database URL [{env_content.get('DATABASE_URL', 'sqlite:///mass_framework.db')}]: ").strip()
        if db_url:
            env_content["DATABASE_URL"] = db_url
        elif "DATABASE_URL" not in env_content:
            env_content["DATABASE_URL"] = "sqlite:///mass_framework.db"
        
        # Social providers
        print("\n📱 Social Provider Configuration:")
        print("Configure the social media providers you want to enable.")
        print("You can skip providers and configure them later.")
        
        for key, provider in self.providers.items():
            print(f"\n--- {provider.name} ---")
            configure = input(f"Configure {provider.name}? (y/N): ").lower().startswith('y')
            
            if configure:
                print(f"Setup URL: {provider.setup_url}")
                
                client_id = input(f"{provider.client_id_var}: ").strip()
                if client_id:
                    env_content[provider.client_id_var] = client_id
                
                client_secret = input(f"{provider.client_secret_var}: ").strip()
                if client_secret:
                    env_content[provider.client_secret_var] = client_secret
                
                # Set default redirect URI
                default_redirect = f"http://localhost:8000/auth/{key}/callback"
                redirect_uri = input(f"{provider.redirect_uri_var} [{default_redirect}]: ").strip()
                env_content[provider.redirect_uri_var] = redirect_uri or default_redirect
        
        # Write .env file
        with open(self.env_file, 'w') as f:
            f.write("# MASS Framework Environment Configuration\n")
            f.write("# Generated by Social Authentication Setup Wizard\n\n")
            
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
        
        print(f"\n✅ Configuration saved to {self.env_file}")
        
        # Validate configuration
        validation = self.validate_environment()
        print("\n📊 Configuration Summary:")
        print(f"  Configured providers: {len(validation['configured_providers'])}")
        print(f"  Missing providers: {len(validation['missing_providers'])}")
        
        if validation['configured_providers']:
            print("  ✅ Ready providers:")
            for provider in validation['configured_providers']:
                print(f"    • {provider['name']}")
        
        if validation['missing_providers']:
            print("  ⚠️  Not configured:")
            for provider in validation['missing_providers']:
                print(f"    • {provider['name']}")
        
        print(f"\n🚀 Setup complete! Run your MASS Framework with social authentication enabled.")


def main():
    """Main setup function"""
    setup = SocialAuthSetup()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "template":
            setup.create_env_template()
        elif command == "validate":
            validation = setup.validate_environment()
            print(json.dumps(validation, indent=2))
        elif command == "install":
            setup.install_dependencies()
        elif command == "instructions":
            provider = sys.argv[2] if len(sys.argv) > 2 else None
            setup.print_setup_instructions(provider)
        elif command == "interactive":
            setup.setup_interactive()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: template, validate, install, instructions, interactive")
    else:
        setup.setup_interactive()


if __name__ == "__main__":
    main()
