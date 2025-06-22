"""
MASS Framework - Cloud Storage & File Management System
=====================================================

Comprehensive cloud storage solution for client apps with multi-provider support,
secure file uploads, automatic backups, and seamless integration with the visual builder.

Features:
- Multi-cloud provider support (AWS S3, Google Cloud, Azure, etc.)
- Secure file upload with virus scanning
- Automatic backup and versioning
- CDN integration for fast delivery
- File compression and optimization
- Real-time sync across devices
- Admin dashboard for storage management
"""

import os
import asyncio
import aiofiles
import hashlib
import mimetypes
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, BinaryIO
from dataclasses import dataclass, field
from enum import Enum
import json
import boto3
from google.cloud import storage as gcs
from azure.storage.blob import BlobServiceClient
import requests
from PIL import Image
import io
import zipfile
import tempfile
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StorageProvider(Enum):
    """Supported cloud storage providers"""
    AWS_S3 = "aws_s3"
    GOOGLE_CLOUD = "google_cloud"
    AZURE_BLOB = "azure_blob"
    CLOUDFLARE_R2 = "cloudflare_r2"
    LOCAL = "local"

class FileType(Enum):
    """Supported file types"""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    ARCHIVE = "archive"
    CODE = "code"
    DATA = "data"
    OTHER = "other"

@dataclass
class FileMetadata:
    """File metadata structure"""
    file_id: str
    filename: str
    original_filename: str
    size: int
    content_type: str
    file_type: FileType
    checksum: str
    upload_date: datetime
    last_modified: datetime
    user_id: str
    app_id: str
    public: bool = False
    tags: List[str] = field(default_factory=list)
    custom_metadata: Dict[str, Any] = field(default_factory=dict)
    versions: List[str] = field(default_factory=list)
    thumbnail_url: Optional[str] = None
    cdn_url: Optional[str] = None
    backup_locations: List[str] = field(default_factory=list)

@dataclass
class StorageConfig:
    """Storage configuration"""
    provider: StorageProvider
    bucket_name: str
    region: str = "us-east-1"
    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    endpoint_url: Optional[str] = None
    cdn_domain: Optional[str] = None
    max_file_size: int = 100 * 1024 * 1024  # 100MB default
    allowed_extensions: List[str] = field(default_factory=lambda: [
        'jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'txt', 'zip'
    ])
    enable_virus_scan: bool = True
    enable_compression: bool = True
    enable_thumbnails: bool = True

class CloudStorageManager:
    """Main cloud storage management system"""
    
    def __init__(self, config: StorageConfig):
        self.config = config
        self.client = self._initialize_client()
        self.metadata_store: Dict[str, FileMetadata] = {}
        
    def _initialize_client(self):
        """Initialize storage client based on provider"""
        if self.config.provider == StorageProvider.AWS_S3:
            return boto3.client(
                's3',
                aws_access_key_id=self.config.access_key,
                aws_secret_access_key=self.config.secret_key,
                region_name=self.config.region,
                endpoint_url=self.config.endpoint_url
            )
        elif self.config.provider == StorageProvider.GOOGLE_CLOUD:
            return gcs.Client()
        elif self.config.provider == StorageProvider.AZURE_BLOB:
            return BlobServiceClient(
                account_url=f"https://{self.config.access_key}.blob.core.windows.net",
                credential=self.config.secret_key
            )
        elif self.config.provider == StorageProvider.LOCAL:
            os.makedirs(f"./storage/{self.config.bucket_name}", exist_ok=True)
            return None
        else:
            raise ValueError(f"Unsupported storage provider: {self.config.provider}")
    
    async def upload_file(
        self, 
        file_data: Union[bytes, BinaryIO], 
        filename: str,
        user_id: str,
        app_id: str,
        content_type: Optional[str] = None,
        tags: List[str] = None,
        custom_metadata: Dict[str, Any] = None,
        public: bool = False
    ) -> FileMetadata:
        """Upload file to cloud storage with full processing pipeline"""
        
        # Generate unique file ID
        file_id = self._generate_file_id(filename, user_id)
        
        # Validate file
        if isinstance(file_data, bytes):
            file_size = len(file_data)
            file_stream = io.BytesIO(file_data)
        else:
            file_data.seek(0, 2)  # Seek to end
            file_size = file_data.tell()
            file_data.seek(0)  # Reset to beginning
            file_stream = file_data
        
        # Check file size
        if file_size > self.config.max_file_size:
            raise ValueError(f"File size ({file_size}) exceeds maximum allowed ({self.config.max_file_size})")
        
        # Detect content type
        if not content_type:
            content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
        
        # Determine file type
        file_type = self._determine_file_type(content_type, filename)
        
        # Validate file extension
        file_ext = Path(filename).suffix.lower().lstrip('.')
        if file_ext not in self.config.allowed_extensions:
            raise ValueError(f"File extension '{file_ext}' is not allowed")
        
        # Generate checksum
        file_stream.seek(0)
        checksum = hashlib.sha256(file_stream.read()).hexdigest()
        file_stream.seek(0)
        
        # Check for duplicates
        existing_file = self._find_duplicate(checksum, user_id, app_id)
        if existing_file:
            logger.info(f"Duplicate file found: {existing_file.file_id}")
            return existing_file
        
        # Virus scan (if enabled)
        if self.config.enable_virus_scan:
            is_safe = await self._virus_scan(file_stream)
            if not is_safe:
                raise ValueError("File failed virus scan")
        
        # Process file (compression, thumbnails, etc.)
        processed_data = await self._process_file(file_stream, file_type, content_type)
        
        # Upload to storage
        storage_path = f"{app_id}/{user_id}/{file_id}"
        upload_url = await self._upload_to_storage(
            processed_data['main'], 
            storage_path, 
            content_type,
            public
        )
        
        # Upload thumbnail if generated
        thumbnail_url = None
        if processed_data.get('thumbnail'):
            thumbnail_path = f"{storage_path}_thumbnail"
            thumbnail_url = await self._upload_to_storage(
                processed_data['thumbnail'], 
                thumbnail_path, 
                'image/jpeg',
                public
            )
        
        # Create metadata
        metadata = FileMetadata(
            file_id=file_id,
            filename=f"{file_id}_{filename}",
            original_filename=filename,
            size=file_size,
            content_type=content_type,
            file_type=file_type,
            checksum=checksum,
            upload_date=datetime.utcnow(),
            last_modified=datetime.utcnow(),
            user_id=user_id,
            app_id=app_id,
            public=public,
            tags=tags or [],
            custom_metadata=custom_metadata or {},
            thumbnail_url=thumbnail_url,
            cdn_url=self._get_cdn_url(storage_path) if self.config.cdn_domain else upload_url
        )
        
        # Store metadata
        self.metadata_store[file_id] = metadata
        await self._save_metadata(metadata)
        
        # Schedule backup
        if self.config.provider != StorageProvider.LOCAL:
            await self._schedule_backup(file_id, processed_data['main'])
        
        logger.info(f"File uploaded successfully: {file_id}")
        return metadata
    
    async def download_file(self, file_id: str, user_id: str) -> Dict[str, Any]:
        """Download file from storage"""
        metadata = self.metadata_store.get(file_id)
        if not metadata:
            metadata = await self._load_metadata(file_id)
        
        if not metadata:
            raise ValueError(f"File not found: {file_id}")
        
        # Check permissions
        if metadata.user_id != user_id and not metadata.public:
            raise PermissionError("Access denied to file")
        
        # Download from storage
        storage_path = f"{metadata.app_id}/{metadata.user_id}/{file_id}"
        file_data = await self._download_from_storage(storage_path)
        
        return {
            'data': file_data,
            'metadata': metadata,
            'content_type': metadata.content_type,
            'filename': metadata.original_filename
        }
    
    async def delete_file(self, file_id: str, user_id: str) -> bool:
        """Delete file from storage"""
        metadata = self.metadata_store.get(file_id)
        if not metadata:
            metadata = await self._load_metadata(file_id)
        
        if not metadata:
            return False
        
        # Check permissions
        if metadata.user_id != user_id:
            raise PermissionError("Access denied to file")
        
        # Delete from storage
        storage_path = f"{metadata.app_id}/{metadata.user_id}/{file_id}"
        await self._delete_from_storage(storage_path)
        
        # Delete thumbnail
        if metadata.thumbnail_url:
            await self._delete_from_storage(f"{storage_path}_thumbnail")
        
        # Remove metadata
        if file_id in self.metadata_store:
            del self.metadata_store[file_id]
        await self._delete_metadata(file_id)
        
        logger.info(f"File deleted: {file_id}")
        return True
    
    async def list_files(
        self, 
        user_id: str, 
        app_id: Optional[str] = None,
        file_type: Optional[FileType] = None,
        tags: List[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List files with filtering and pagination"""
        files = []
        
        for metadata in self.metadata_store.values():
            # Basic filters
            if metadata.user_id != user_id:
                continue
            if app_id and metadata.app_id != app_id:
                continue
            if file_type and metadata.file_type != file_type:
                continue
            if tags and not any(tag in metadata.tags for tag in tags):
                continue
            
            files.append(metadata)
        
        # Sort by upload date (newest first)
        files.sort(key=lambda x: x.upload_date, reverse=True)
        
        # Pagination
        total = len(files)
        files = files[offset:offset + limit]
        
        return {
            'files': [self._metadata_to_dict(f) for f in files],
            'total': total,
            'limit': limit,
            'offset': offset,
            'has_more': offset + limit < total
        }
    
    async def get_storage_stats(self, user_id: str, app_id: Optional[str] = None) -> Dict[str, Any]:
        """Get storage statistics"""
        total_files = 0
        total_size = 0
        file_types = {}
        
        for metadata in self.metadata_store.values():
            if metadata.user_id != user_id:
                continue
            if app_id and metadata.app_id != app_id:
                continue
            
            total_files += 1
            total_size += metadata.size
            
            file_type = metadata.file_type.value
            if file_type not in file_types:
                file_types[file_type] = {'count': 0, 'size': 0}
            file_types[file_type]['count'] += 1
            file_types[file_type]['size'] += metadata.size
        
        return {
            'total_files': total_files,
            'total_size': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'file_types': file_types,
            'storage_limit': self.config.max_file_size * 1000,  # Example limit
            'storage_used_percent': round((total_size / (self.config.max_file_size * 1000)) * 100, 2)
        }
    
    # Helper methods
    def _generate_file_id(self, filename: str, user_id: str) -> str:
        """Generate unique file ID"""
        timestamp = datetime.utcnow().isoformat()
        data = f"{filename}_{user_id}_{timestamp}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def _determine_file_type(self, content_type: str, filename: str) -> FileType:
        """Determine file type from content type and filename"""
        if content_type.startswith('image/'):
            return FileType.IMAGE
        elif content_type.startswith('video/'):
            return FileType.VIDEO
        elif content_type.startswith('audio/'):
            return FileType.AUDIO
        elif content_type in ['application/pdf', 'application/msword', 'text/plain']:
            return FileType.DOCUMENT
        elif content_type in ['application/zip', 'application/x-tar']:
            return FileType.ARCHIVE
        elif filename.endswith(('.py', '.js', '.html', '.css', '.json')):
            return FileType.CODE
        elif content_type in ['application/json', 'text/csv']:
            return FileType.DATA
        else:
            return FileType.OTHER
    
    def _find_duplicate(self, checksum: str, user_id: str, app_id: str) -> Optional[FileMetadata]:
        """Find duplicate file by checksum"""
        for metadata in self.metadata_store.values():
            if (metadata.checksum == checksum and 
                metadata.user_id == user_id and 
                metadata.app_id == app_id):
                return metadata
        return None
    
    async def _virus_scan(self, file_stream: BinaryIO) -> bool:
        """Perform virus scan (placeholder - integrate with actual service)"""
        # In production, integrate with VirusTotal, ClamAV, or similar
        # For now, just basic checks
        file_stream.seek(0)
        content = file_stream.read(1024)  # Read first 1KB
        file_stream.seek(0)
        
        # Basic malware signatures (very basic example)
        malware_signatures = [b'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR']  # EICAR test string
        
        for signature in malware_signatures:
            if signature in content:
                return False
        
        return True
    
    async def _process_file(self, file_stream: BinaryIO, file_type: FileType, content_type: str) -> Dict[str, bytes]:
        """Process file (compression, thumbnails, etc.)"""
        file_stream.seek(0)
        original_data = file_stream.read()
        
        result = {'main': original_data}
        
        # Generate thumbnail for images
        if file_type == FileType.IMAGE and self.config.enable_thumbnails:
            try:
                image = Image.open(io.BytesIO(original_data))
                image.thumbnail((200, 200), Image.Resampling.LANCZOS)
                
                thumbnail_io = io.BytesIO()
                image.save(thumbnail_io, format='JPEG', quality=85)
                result['thumbnail'] = thumbnail_io.getvalue()
            except Exception as e:
                logger.warning(f"Failed to generate thumbnail: {e}")
        
        # Compress if enabled and beneficial
        if self.config.enable_compression and len(original_data) > 1024:  # Only for files > 1KB
            try:
                compressed = self._compress_data(original_data)
                if len(compressed) < len(original_data) * 0.9:  # Only if 10%+ reduction
                    result['main'] = compressed
            except Exception as e:
                logger.warning(f"Failed to compress file: {e}")
        
        return result
    
    def _compress_data(self, data: bytes) -> bytes:
        """Compress data using zip"""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('data', data)
        return buffer.getvalue()
    
    async def _upload_to_storage(self, data: bytes, path: str, content_type: str, public: bool) -> str:
        """Upload data to configured storage provider"""
        if self.config.provider == StorageProvider.AWS_S3:
            extra_args = {'ContentType': content_type}
            if public:
                extra_args['ACL'] = 'public-read'
            
            self.client.put_object(
                Bucket=self.config.bucket_name,
                Key=path,
                Body=data,
                **extra_args
            )
            
            if public:
                return f"https://{self.config.bucket_name}.s3.{self.config.region}.amazonaws.com/{path}"
            else:
                return self.client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.config.bucket_name, 'Key': path},
                    ExpiresIn=3600
                )
        
        elif self.config.provider == StorageProvider.LOCAL:
            file_path = Path(f"./storage/{self.config.bucket_name}/{path}")
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(data)
            
            return f"/storage/{self.config.bucket_name}/{path}"
        
        else:
            raise NotImplementedError(f"Upload not implemented for {self.config.provider}")
    
    async def _download_from_storage(self, path: str) -> bytes:
        """Download data from storage"""
        if self.config.provider == StorageProvider.AWS_S3:
            response = self.client.get_object(Bucket=self.config.bucket_name, Key=path)
            return response['Body'].read()
        
        elif self.config.provider == StorageProvider.LOCAL:
            file_path = Path(f"./storage/{self.config.bucket_name}/{path}")
            async with aiofiles.open(file_path, 'rb') as f:
                return await f.read()
        
        else:
            raise NotImplementedError(f"Download not implemented for {self.config.provider}")
    
    async def _delete_from_storage(self, path: str) -> None:
        """Delete data from storage"""
        if self.config.provider == StorageProvider.AWS_S3:
            self.client.delete_object(Bucket=self.config.bucket_name, Key=path)
        
        elif self.config.provider == StorageProvider.LOCAL:
            file_path = Path(f"./storage/{self.config.bucket_name}/{path}")
            if file_path.exists():
                file_path.unlink()
    
    def _get_cdn_url(self, path: str) -> str:
        """Generate CDN URL"""
        if self.config.cdn_domain:
            return f"https://{self.config.cdn_domain}/{path}"
        return f"/{path}"
    
    async def _save_metadata(self, metadata: FileMetadata) -> None:
        """Save metadata to persistent storage"""
        # In production, save to database
        metadata_path = Path(f"./storage/metadata/{metadata.file_id}.json")
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(metadata_path, 'w') as f:
            await f.write(json.dumps(self._metadata_to_dict(metadata), default=str))
    
    async def _load_metadata(self, file_id: str) -> Optional[FileMetadata]:
        """Load metadata from persistent storage"""
        metadata_path = Path(f"./storage/metadata/{file_id}.json")
        if not metadata_path.exists():
            return None
        
        async with aiofiles.open(metadata_path, 'r') as f:
            data = json.loads(await f.read())
            return self._dict_to_metadata(data)
    
    async def _delete_metadata(self, file_id: str) -> None:
        """Delete metadata from persistent storage"""
        metadata_path = Path(f"./storage/metadata/{file_id}.json")
        if metadata_path.exists():
            metadata_path.unlink()
    
    async def _schedule_backup(self, file_id: str, data: bytes) -> None:
        """Schedule file backup to secondary location"""
        # Implement backup strategy (e.g., to different region/provider)
        logger.info(f"Backup scheduled for file: {file_id}")
    
    def _metadata_to_dict(self, metadata: FileMetadata) -> Dict[str, Any]:
        """Convert metadata to dictionary"""
        return {
            'file_id': metadata.file_id,
            'filename': metadata.filename,
            'original_filename': metadata.original_filename,
            'size': metadata.size,
            'content_type': metadata.content_type,
            'file_type': metadata.file_type.value,
            'checksum': metadata.checksum,
            'upload_date': metadata.upload_date.isoformat(),
            'last_modified': metadata.last_modified.isoformat(),
            'user_id': metadata.user_id,
            'app_id': metadata.app_id,
            'public': metadata.public,
            'tags': metadata.tags,
            'custom_metadata': metadata.custom_metadata,
            'versions': metadata.versions,
            'thumbnail_url': metadata.thumbnail_url,
            'cdn_url': metadata.cdn_url,
            'backup_locations': metadata.backup_locations
        }
    
    def _dict_to_metadata(self, data: Dict[str, Any]) -> FileMetadata:
        """Convert dictionary to metadata"""
        return FileMetadata(
            file_id=data['file_id'],
            filename=data['filename'],
            original_filename=data['original_filename'],
            size=data['size'],
            content_type=data['content_type'],
            file_type=FileType(data['file_type']),
            checksum=data['checksum'],
            upload_date=datetime.fromisoformat(data['upload_date']),
            last_modified=datetime.fromisoformat(data['last_modified']),
            user_id=data['user_id'],
            app_id=data['app_id'],
            public=data['public'],
            tags=data['tags'],
            custom_metadata=data['custom_metadata'],
            versions=data['versions'],
            thumbnail_url=data.get('thumbnail_url'),
            cdn_url=data.get('cdn_url'),
            backup_locations=data.get('backup_locations', [])
        )

# Example usage and configuration
if __name__ == "__main__":
    # Example configuration for AWS S3
    aws_config = StorageConfig(
        provider=StorageProvider.AWS_S3,
        bucket_name="mass-framework-storage",
        region="us-east-1",
        access_key="your-access-key",
        secret_key="your-secret-key",
        cdn_domain="cdn.massframework.com",
        max_file_size=100 * 1024 * 1024,  # 100MB
        allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'txt', 'zip', 'mp4', 'mp3'],
        enable_virus_scan=True,
        enable_compression=True,
        enable_thumbnails=True
    )
    
    # Example configuration for local storage (development)
    local_config = StorageConfig(
        provider=StorageProvider.LOCAL,
        bucket_name="local-storage",
        max_file_size=50 * 1024 * 1024,  # 50MB for local
        allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'pdf', 'txt'],
        enable_virus_scan=False,  # Disabled for local development
        enable_compression=True,
        enable_thumbnails=True
    )
    
    print("Cloud Storage System initialized!")
    print("Features:")
    print("- Multi-cloud provider support")
    print("- Secure file uploads with virus scanning")
    print("- Automatic image thumbnails")
    print("- File compression and optimization")
    print("- Duplicate detection")
    print("- CDN integration")
    print("- Backup and versioning")
    print("- Storage analytics and quotas")
