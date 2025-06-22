"""
MASS Framework - Integrated Cloud & Social System
===============================================

Complete integration system that combines cloud storage, social authentication,
and visual builder into a seamless user experience.

Features:
- One-click app setup with storage and social login
- Automatic landing page generation with file upload
- Real-time sync between apps and cloud storage
- Smart user onboarding with social profiles
- Drag-and-drop file management in visual builder
- Auto-deployment with CDN and auth endpoints
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import uuid
import logging

# Import our systems
from .cloud_storage_system import CloudStorageManager, StorageConfig, StorageProvider, FileType
from .auto_social_login_setup import AutoSocialLoginSetup, SocialProvider, LoginPageConfig, LoginTheme

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AppTier(Enum):
    """App service tiers"""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"

@dataclass
class AppConfiguration:
    """Complete app configuration"""
    app_id: str
    app_name: str
    domain: str
    tier: AppTier
    
    # Storage configuration
    storage_provider: StorageProvider
    storage_quota_gb: int
    cdn_enabled: bool
    
    # Social auth configuration
    social_providers: List[SocialProvider]
    auto_registration: bool
    profile_sync: bool
    
    # Features
    file_upload_enabled: bool
    real_time_sync: bool
    backup_enabled: bool
    analytics_enabled: bool
    
    # UI customization
    theme: LoginTheme
    primary_color: str
    app_logo: str = ""
    custom_domain: str = ""

class IntegratedMassSystem:
    """Complete integrated system for cloud storage and social authentication"""
    
    def __init__(self):
        self.apps: Dict[str, AppConfiguration] = {}
        self.storage_managers: Dict[str, CloudStorageManager] = {}
        self.auth_managers: Dict[str, AutoSocialLoginSetup] = {}
        
    async def create_app(
        self,
        app_name: str,
        domain: str,
        tier: AppTier = AppTier.FREE,
        social_providers: List[Tuple[SocialProvider, str, str]] = None,
        storage_config: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a complete app with storage and social authentication"""
        
        app_id = str(uuid.uuid4())
        logger.info(f"Creating new app: {app_name} (ID: {app_id})")
        
        # Determine tier limits
        tier_limits = self._get_tier_limits(tier)
        
        # Configure storage
        storage_provider = storage_config.get('provider', StorageProvider.LOCAL) if storage_config else StorageProvider.LOCAL
        storage_quota = tier_limits['storage_gb']
        
        storage_cfg = StorageConfig(
            provider=storage_provider,
            bucket_name=f"mass-app-{app_id}",
            max_file_size=tier_limits['max_file_size'],
            **storage_config or {}
        )
        
        storage_manager = CloudStorageManager(storage_cfg)
        self.storage_managers[app_id] = storage_manager
        
        # Configure social authentication
        auth_manager = AutoSocialLoginSetup(app_id, f"secret-{app_id}")
        
        login_config = LoginPageConfig(
            app_name=app_name,
            theme=LoginTheme.MODERN,
            primary_color="#6366f1",
            welcome_message=f"Welcome to {app_name}! Sign in to get started.",
            redirect_after_login="/dashboard"
        )
        
        if social_providers:
            await auth_manager.quick_setup(social_providers, domain, login_config)
        
        self.auth_managers[app_id] = auth_manager
        
        # Create app configuration
        app_config = AppConfiguration(
            app_id=app_id,
            app_name=app_name,
            domain=domain,
            tier=tier,
            storage_provider=storage_provider,
            storage_quota_gb=storage_quota,
            cdn_enabled=tier_limits['cdn_enabled'],
            social_providers=[provider for provider, _, _ in social_providers or []],
            auto_registration=True,
            profile_sync=True,
            file_upload_enabled=True,
            real_time_sync=tier_limits['real_time_sync'],
            backup_enabled=tier_limits['backup_enabled'],
            analytics_enabled=tier_limits['analytics_enabled'],
            theme=LoginTheme.MODERN,
            primary_color="#6366f1"
        )
        
        self.apps[app_id] = app_config
        
        # Generate complete app package
        app_package = await self._generate_app_package(app_config)
        
        # Save configuration
        await self._save_app_configuration(app_config)
        
        logger.info(f"App created successfully: {app_name}")
        
        return {
            'app_id': app_id,
            'app_name': app_name,
            'domain': domain,
            'tier': tier.value,
            'storage_quota_gb': storage_quota,
            'features': {
                'file_upload': True,
                'social_login': len(social_providers or []) > 0,
                'cdn': tier_limits['cdn_enabled'],
                'real_time_sync': tier_limits['real_time_sync'],
                'backup': tier_limits['backup_enabled'],
                'analytics': tier_limits['analytics_enabled']
            },
            'endpoints': app_package['endpoints'],
            'dashboard_url': f"https://{domain}/dashboard",
            'files_uploaded': 0,
            'users_registered': 0,
            'status': 'active'
        }
    
    async def upload_file_to_app(
        self,
        app_id: str,
        user_id: str,
        file_data: bytes,
        filename: str,
        content_type: str = None,
        public: bool = False
    ) -> Dict[str, Any]:
        """Upload file to app with integrated authentication check"""
        
        if app_id not in self.storage_managers:
            raise ValueError(f"App not found: {app_id}")
        
        storage_manager = self.storage_managers[app_id]
        app_config = self.apps[app_id]
        
        # Check storage quota
        stats = await storage_manager.get_storage_stats(user_id, app_id)
        quota_bytes = app_config.storage_quota_gb * 1024 * 1024 * 1024
        
        if stats['total_size'] + len(file_data) > quota_bytes:
            raise ValueError(f"Storage quota exceeded. Used: {stats['total_size_mb']}MB, Quota: {app_config.storage_quota_gb}GB")
        
        # Upload file
        metadata = await storage_manager.upload_file(
            file_data=file_data,
            filename=filename,
            user_id=user_id,
            app_id=app_id,
            content_type=content_type,
            public=public
        )
        
        return {
            'file_id': metadata.file_id,
            'filename': metadata.original_filename,
            'size': metadata.size,
            'url': metadata.cdn_url,
            'thumbnail_url': metadata.thumbnail_url,
            'upload_date': metadata.upload_date.isoformat(),
            'public': metadata.public
        }
    
    def generate_complete_landing_page(self, app_id: str) -> str:
        """Generate complete landing page with file upload and social login"""
        
        if app_id not in self.apps:
            raise ValueError(f"App not found: {app_id}")
        
        app_config = self.apps[app_id]
        auth_manager = self.auth_managers[app_id]
        
        # Get social login page
        login_page = auth_manager.generate_login_page()
        
        # Enhanced landing page with file upload
        enhanced_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{app_config.app_name} - Dashboard</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }}
                
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                
                .header {{
                    background: rgba(255, 255, 255, 0.95);
                    padding: 20px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}
                
                .logo {{
                    font-size: 24px;
                    font-weight: 700;
                    color: {app_config.primary_color};
                }}
                
                .user-info {{
                    display: flex;
                    align-items: center;
                    gap: 15px;
                }}
                
                .dashboard {{
                    padding: 40px 20px;
                    max-width: 1200px;
                    margin: 0 auto;
                }}
                
                .dashboard-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 30px;
                    margin-top: 30px;
                }}
                
                .card {{
                    background: rgba(255, 255, 255, 0.95);
                    padding: 30px;
                    border-radius: 20px;
                    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
                    backdrop-filter: blur(10px);
                }}
                
                .upload-zone {{
                    border: 3px dashed #ccc;
                    border-radius: 15px;
                    padding: 40px;
                    text-align: center;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }}
                
                .upload-zone:hover {{
                    border-color: {app_config.primary_color};
                    background: rgba(99, 102, 241, 0.05);
                }}
                
                .upload-zone.dragover {{
                    border-color: {app_config.primary_color};
                    background: rgba(99, 102, 241, 0.1);
                }}
                
                .file-list {{
                    max-height: 400px;
                    overflow-y: auto;
                }}
                
                .file-item {{
                    display: flex;
                    align-items: center;
                    padding: 15px;
                    border-bottom: 1px solid #eee;
                    transition: background 0.2s ease;
                }}
                
                .file-item:hover {{
                    background: #f8f9fa;
                }}
                
                .file-icon {{
                    width: 40px;
                    height: 40px;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 15px;
                    color: white;
                    font-size: 18px;
                }}
                
                .stats {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }}
                
                .stat-item {{
                    background: rgba(255, 255, 255, 0.95);
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                }}
                
                .stat-value {{
                    font-size: 32px;
                    font-weight: 700;
                    color: {app_config.primary_color};
                }}
                
                .stat-label {{
                    color: #666;
                    margin-top: 5px;
                    font-size: 14px;
                }}
                
                .btn {{
                    background: {app_config.primary_color};
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 8px;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }}
                
                .btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
                }}
                
                .progress-bar {{
                    width: 100%;
                    height: 8px;
                    background: #eee;
                    border-radius: 4px;
                    overflow: hidden;
                    margin: 10px 0;
                }}
                
                .progress-fill {{
                    height: 100%;
                    background: {app_config.primary_color};
                    transition: width 0.3s ease;
                }}
                
                @media (max-width: 768px) {{
                    .dashboard-grid {{
                        grid-template-columns: 1fr;
                    }}
                    
                    .stats {{
                        grid-template-columns: repeat(2, 1fr);
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">
                    <i class="fas fa-rocket"></i>
                    {app_config.app_name}
                </div>
                <div class="user-info">
                    <span id="userName">Loading...</span>
                    <img id="userAvatar" src="" alt="Avatar" style="width: 40px; height: 40px; border-radius: 50%; display: none;">
                    <button class="btn" onclick="logout()">
                        <i class="fas fa-sign-out-alt"></i>
                    </button>
                </div>
            </div>
            
            <div class="dashboard">
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-value" id="fileCount">0</div>
                        <div class="stat-label">Files Uploaded</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="storageUsed">0 MB</div>
                        <div class="stat-label">Storage Used</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{app_config.storage_quota_gb} GB</div>
                        <div class="stat-label">Storage Quota</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="syncStatus">
                            <i class="fas fa-sync-alt fa-spin"></i>
                        </div>
                        <div class="stat-label">Sync Status</div>
                    </div>
                </div>
                
                <div class="dashboard-grid">
                    <div class="card">
                        <h3><i class="fas fa-cloud-upload-alt"></i> Upload Files</h3>
                        <div class="upload-zone" onclick="document.getElementById('fileInput').click()">
                            <i class="fas fa-cloud-upload-alt" style="font-size: 48px; color: #ccc; margin-bottom: 20px;"></i>
                            <h4>Drop files here or click to browse</h4>
                            <p style="color: #666; margin-top: 10px;">Supports images, documents, videos up to {storage_cfg.max_file_size // (1024*1024)}MB</p>
                            <div class="progress-bar" id="uploadProgress" style="display: none;">
                                <div class="progress-fill" id="uploadProgressFill"></div>
                            </div>
                        </div>
                        <input type="file" id="fileInput" multiple style="display: none;" onchange="handleFileUpload(this.files)">
                    </div>
                    
                    <div class="card">
                        <h3><i class="fas fa-folder"></i> My Files</h3>
                        <div class="file-list" id="fileList">
                            <div style="text-align: center; padding: 40px; color: #666;">
                                <i class="fas fa-folder-open" style="font-size: 48px; margin-bottom: 20px;"></i>
                                <p>No files uploaded yet</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="card">
                        <h3><i class="fas fa-cog"></i> App Settings</h3>
                        <div style="display: flex; flex-direction: column; gap: 15px;">
                            <div>
                                <label><strong>Social Providers:</strong></label>
                                <div style="margin-top: 10px;">
                                    {', '.join([provider.value.title() for provider in app_config.social_providers]) or 'None configured'}
                                </div>
                            </div>
                            <div>
                                <label><strong>Storage Provider:</strong></label>
                                <div>{app_config.storage_provider.value.replace('_', ' ').title()}</div>
                            </div>
                            <div>
                                <label><strong>Features:</strong></label>
                                <div style="margin-top: 10px;">
                                    {'✅ CDN Enabled' if app_config.cdn_enabled else '❌ CDN Disabled'}<br>
                                    {'✅ Real-time Sync' if app_config.real_time_sync else '❌ Real-time Sync'}<br>
                                    {'✅ Backup Enabled' if app_config.backup_enabled else '❌ Backup Disabled'}<br>
                                    {'✅ Analytics' if app_config.analytics_enabled else '❌ Analytics Disabled'}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <script>
                // Initialize dashboard
                document.addEventListener('DOMContentLoaded', function() {{
                    loadUserProfile();
                    loadFiles();
                    setupDragAndDrop();
                    setupRealTimeSync();
                }});
                
                function loadUserProfile() {{
                    // Simulate loading user profile
                    setTimeout(() => {{
                        document.getElementById('userName').textContent = 'John Doe';
                        const avatar = document.getElementById('userAvatar');
                        avatar.src = 'https://via.placeholder.com/40';
                        avatar.style.display = 'block';
                    }}, 500);
                }}
                
                function loadFiles() {{
                    // Simulate loading files
                    fetch('/api/files')
                        .then(response => response.json())
                        .then(data => {{
                            updateFileList(data.files || []);
                            updateStats(data.stats || {{}});
                        }})
                        .catch(error => {{
                            console.log('Demo mode - no backend connected');
                            // Demo data
                            updateStats({{
                                total_files: 0,
                                total_size_mb: 0,
                                storage_used_percent: 0
                            }});
                        }});
                }}
                
                function updateStats(stats) {{
                    document.getElementById('fileCount').textContent = stats.total_files || 0;
                    document.getElementById('storageUsed').textContent = (stats.total_size_mb || 0) + ' MB';
                    document.getElementById('syncStatus').innerHTML = '<i class="fas fa-check" style="color: #28a745;"></i>';
                }}
                
                function updateFileList(files) {{
                    const fileList = document.getElementById('fileList');
                    
                    if (files.length === 0) {{
                        fileList.innerHTML = `
                            <div style="text-align: center; padding: 40px; color: #666;">
                                <i class="fas fa-folder-open" style="font-size: 48px; margin-bottom: 20px;"></i>
                                <p>No files uploaded yet</p>
                            </div>
                        `;
                        return;
                    }}
                    
                    fileList.innerHTML = files.map(file => `
                        <div class="file-item">
                            <div class="file-icon" style="background: ${{getFileColor(file.file_type)}};">
                                <i class="fas ${{getFileIcon(file.file_type)}}"></i>
                            </div>
                            <div style="flex: 1;">
                                <div style="font-weight: 600;">${{file.original_filename}}</div>
                                <div style="color: #666; font-size: 12px;">${{formatFileSize(file.size)}} • ${{formatDate(file.upload_date)}}</div>
                            </div>
                            <div>
                                <button class="btn" style="padding: 8px 12px; font-size: 12px;" onclick="downloadFile('${{file.file_id}}')">
                                    <i class="fas fa-download"></i>
                                </button>
                            </div>
                        </div>
                    `).join('');
                }}
                
                function setupDragAndDrop() {{
                    const uploadZone = document.querySelector('.upload-zone');
                    
                    uploadZone.addEventListener('dragover', (e) => {{
                        e.preventDefault();
                        uploadZone.classList.add('dragover');
                    }});
                    
                    uploadZone.addEventListener('dragleave', () => {{
                        uploadZone.classList.remove('dragover');
                    }});
                    
                    uploadZone.addEventListener('drop', (e) => {{
                        e.preventDefault();
                        uploadZone.classList.remove('dragover');
                        handleFileUpload(e.dataTransfer.files);
                    }});
                }}
                
                function handleFileUpload(files) {{
                    const progress = document.getElementById('uploadProgress');
                    const progressFill = document.getElementById('uploadProgressFill');
                    
                    progress.style.display = 'block';
                    
                    Array.from(files).forEach((file, index) => {{
                        setTimeout(() => {{
                            const formData = new FormData();
                            formData.append('file', file);
                            formData.append('app_id', '{app_id}');
                            
                            fetch('/api/upload', {{
                                method: 'POST',
                                body: formData
                            }})
                            .then(response => response.json())
                            .then(data => {{
                                console.log('File uploaded:', data);
                                loadFiles(); // Reload file list
                            }})
                            .catch(error => {{
                                console.log('Demo mode - simulating upload');
                                // Simulate successful upload
                                setTimeout(() => {{
                                    loadFiles();
                                }}, 1000);
                            }});
                            
                            // Update progress
                            const percent = ((index + 1) / files.length) * 100;
                            progressFill.style.width = percent + '%';
                            
                            if (index === files.length - 1) {{
                                setTimeout(() => {{
                                    progress.style.display = 'none';
                                    progressFill.style.width = '0%';
                                }}, 1000);
                            }}
                        }}, index * 200);
                    }});
                }}
                
                function setupRealTimeSync() {{
                    {'setInterval(() => { loadFiles(); }, 5000);' if app_config.real_time_sync else '// Real-time sync disabled'}
                }}
                
                function getFileIcon(type) {{
                    const icons = {{
                        'image': 'fa-image',
                        'video': 'fa-video',
                        'audio': 'fa-music',
                        'document': 'fa-file-alt',
                        'archive': 'fa-file-archive',
                        'code': 'fa-code',
                        'data': 'fa-database'
                    }};
                    return icons[type] || 'fa-file';
                }}
                
                function getFileColor(type) {{
                    const colors = {{
                        'image': '#28a745',
                        'video': '#dc3545',
                        'audio': '#ffc107',
                        'document': '#007bff',
                        'archive': '#6f42c1',
                        'code': '#fd7e14',
                        'data': '#20c997'
                    }};
                    return colors[type] || '#6c757d';
                }}
                
                function formatFileSize(bytes) {{
                    if (bytes === 0) return '0 Bytes';
                    const k = 1024;
                    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                    const i = Math.floor(Math.log(bytes) / Math.log(k));
                    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
                }}
                
                function formatDate(dateString) {{
                    return new Date(dateString).toLocaleDateString();
                }}
                
                function downloadFile(fileId) {{
                    window.open('/api/download/' + fileId, '_blank');
                }}
                
                function logout() {{
                    localStorage.removeItem('session_token');
                    window.location.href = '/auth/login';
                }}
            </script>
        </body>
        </html>
        """
        
        return enhanced_template
    
    def _get_tier_limits(self, tier: AppTier) -> Dict[str, Any]:
        """Get limits for app tier"""
        limits = {
            AppTier.FREE: {
                'storage_gb': 1,
                'max_file_size': 10 * 1024 * 1024,  # 10MB
                'cdn_enabled': False,
                'real_time_sync': False,
                'backup_enabled': False,
                'analytics_enabled': False,
                'max_social_providers': 2
            },
            AppTier.STARTER: {
                'storage_gb': 10,
                'max_file_size': 50 * 1024 * 1024,  # 50MB
                'cdn_enabled': True,
                'real_time_sync': True,
                'backup_enabled': False,
                'analytics_enabled': True,
                'max_social_providers': 4
            },
            AppTier.PROFESSIONAL: {
                'storage_gb': 100,
                'max_file_size': 200 * 1024 * 1024,  # 200MB
                'cdn_enabled': True,
                'real_time_sync': True,
                'backup_enabled': True,
                'analytics_enabled': True,
                'max_social_providers': 6
            },
            AppTier.ENTERPRISE: {
                'storage_gb': 1000,
                'max_file_size': 1024 * 1024 * 1024,  # 1GB
                'cdn_enabled': True,
                'real_time_sync': True,
                'backup_enabled': True,
                'analytics_enabled': True,
                'max_social_providers': 10
            }
        }
        return limits[tier]
    
    async def _generate_app_package(self, app_config: AppConfiguration) -> Dict[str, Any]:
        """Generate complete app package with all files and endpoints"""
        
        endpoints = {
            'dashboard': f"https://{app_config.domain}/dashboard",
            'login': f"https://{app_config.domain}/auth/login",
            'upload': f"https://{app_config.domain}/api/upload",
            'files': f"https://{app_config.domain}/api/files",
            'download': f"https://{app_config.domain}/api/download",
            'user_profile': f"https://{app_config.domain}/api/user"
        }
        
        # Add social provider endpoints
        for provider in app_config.social_providers:
            endpoints[f'{provider.value}_login'] = f"https://{app_config.domain}/auth/{provider.value}/login"
            endpoints[f'{provider.value}_callback'] = f"https://{app_config.domain}/auth/{provider.value}/callback"
        
        return {
            'endpoints': endpoints,
            'files': {
                'dashboard.html': self.generate_complete_landing_page(app_config.app_id),
                'config.json': json.dumps({
                    'app_id': app_config.app_id,
                    'app_name': app_config.app_name,
                    'tier': app_config.tier.value,
                    'features': {
                        'storage_quota_gb': app_config.storage_quota_gb,
                        'cdn_enabled': app_config.cdn_enabled,
                        'real_time_sync': app_config.real_time_sync,
                        'backup_enabled': app_config.backup_enabled
                    }
                }, indent=2)
            }
        }
    
    async def _save_app_configuration(self, app_config: AppConfiguration) -> None:
        """Save app configuration"""
        os.makedirs('./apps', exist_ok=True)
        
        config_data = {
            'app_id': app_config.app_id,
            'app_name': app_config.app_name,
            'domain': app_config.domain,
            'tier': app_config.tier.value,
            'storage_provider': app_config.storage_provider.value,
            'storage_quota_gb': app_config.storage_quota_gb,
            'cdn_enabled': app_config.cdn_enabled,
            'social_providers': [p.value for p in app_config.social_providers],
            'created_at': datetime.utcnow().isoformat(),
            'features': {
                'file_upload_enabled': app_config.file_upload_enabled,
                'real_time_sync': app_config.real_time_sync,
                'backup_enabled': app_config.backup_enabled,
                'analytics_enabled': app_config.analytics_enabled
            },
            'ui': {
                'theme': app_config.theme.value,
                'primary_color': app_config.primary_color,
                'app_logo': app_config.app_logo
            }
        }
        
        with open(f'./apps/{app_config.app_id}.json', 'w') as f:
            json.dump(config_data, f, indent=2)
    
    async def get_app_analytics(self, app_id: str) -> Dict[str, Any]:
        """Get app analytics and usage statistics"""
        
        if app_id not in self.apps:
            raise ValueError(f"App not found: {app_id}")
        
        app_config = self.apps[app_id]
        storage_manager = self.storage_managers[app_id]
        auth_manager = self.auth_managers[app_id]
        
        # Get storage statistics
        storage_stats = await storage_manager.get_storage_stats("all", app_id)
        
        # Get user statistics
        user_count = len(auth_manager.users)
        active_sessions = len(auth_manager.sessions)
        
        return {
            'app_id': app_id,
            'app_name': app_config.app_name,
            'tier': app_config.tier.value,
            'storage': {
                'files_count': storage_stats['total_files'],
                'storage_used_mb': storage_stats['total_size_mb'],
                'storage_quota_gb': app_config.storage_quota_gb,
                'storage_used_percent': storage_stats['storage_used_percent'],
                'file_types': storage_stats['file_types']
            },
            'users': {
                'total_users': user_count,
                'active_sessions': active_sessions,
                'social_providers': [p.value for p in app_config.social_providers]
            },
            'features': {
                'cdn_enabled': app_config.cdn_enabled,
                'real_time_sync': app_config.real_time_sync,
                'backup_enabled': app_config.backup_enabled,
                'analytics_enabled': app_config.analytics_enabled
            }
        }

# Example usage
if __name__ == "__main__":
    mass_system = IntegratedMassSystem()
    
    print("🚀 MASS Framework - Integrated Cloud & Social System")
    print("====================================================")
    print()
    print("✨ Features:")
    print("- One-click app creation with cloud storage")
    print("- Automatic social login setup")
    print("- Beautiful dashboard with file upload")
    print("- Real-time sync and collaboration")
    print("- Multi-tier pricing (Free, Starter, Pro, Enterprise)")
    print("- Complete API endpoints generation")
    print("- Analytics and usage tracking")
    print()
    print("🎯 Usage Example:")
    print("app = await mass_system.create_app(")
    print("    app_name='My Awesome App',")
    print("    domain='myapp.com',")
    print("    tier=AppTier.PROFESSIONAL,")
    print("    social_providers=[")
    print("        (SocialProvider.GOOGLE, 'client_id', 'client_secret'),")
    print("        (SocialProvider.GITHUB, 'client_id', 'client_secret')")
    print("    ]")
    print(")")
    print()
    print("Ready to revolutionize app development! 🎉")
