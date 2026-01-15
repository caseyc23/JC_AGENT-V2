"""External Storage Research Module for JC Agent.

This module enables JC to access and research information from external drives,
USB storage, and mounted volumes. Perfect for local AI models, project files,
and offline knowledge bases.

For JC - "One more because I am a champion" 🏆
"""

from __future__ import annotations

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class StorageDevice:
    """Represents an external storage device."""
    drive_letter: str
    mount_point: str
    total_size: int
    free_size: int
    device_type: str  # 'fixed', 'removable', 'network', 'cdrom'
    label: Optional[str] = None
    indexed: bool = False
    last_indexed: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class FileMetadata:
    """Metadata for indexed files."""
    path: str
    size: int
    modified: str
    file_type: str
    drive: str
    keywords: List[str]
    description: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


class ExternalStorageManager:
    """Manages external storage devices for JC Agent research."""
    
    # Important file patterns to index
    RESEARCH_PATTERNS = {
        # AI/ML Models
        'ai_models': ['.gguf', '.safetensors', '.pt', '.pth', '.onnx', '.bin', '.model'],
        # Documentation
        'docs': ['.md', '.txt', '.pdf', '.docx', '.html', '.rst'],
        # Code
        'code': ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs'],
        # Data
        'data': ['.json', '.csv', '.xml', '.yaml', '.yml', '.sql', '.db', '.sqlite'],
        # Configs
        'config': ['.ini', '.conf', '.cfg', '.toml', '.env'],
        # Media
        'media': ['.jpg', '.png', '.gif', '.mp4', '.mp3', '.wav'],
    }
    
    # Drives/folders of special interest (from user's attachments)
    SPECIAL_LOCATIONS = {
        'bunker_ai': ['g:', 'g:\\bunkerai.app'],  # Local Llama model
        'lm_studio': ['f:\\.lmstudio', 'f:\\models'],  # LM Studio models
        'projects': ['f:\\git hub insurance app', 'f:\\jc-redd-ai'],  # User projects
        'gemini': ['f:\\.gemini'],  # Gemini workspace
        'claude': ['f:\\.claude'],  # Claude workspace
    }
    
    def __init__(self, storage_dir: Optional[Path] = None):
        """Initialize external storage manager.
        
        Args:
            storage_dir: Directory to store index metadata
        """
        if storage_dir is None:
            storage_dir = Path.home() / ".jc-agent" / "external-storage"
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        self.index_file = self.storage_dir / "storage-index.json"
        self.devices: List[StorageDevice] = []
        self.file_index: List[FileMetadata] = []
        
        # Load existing index
        self._load_index()
    
    def discover_drives(self) -> List[StorageDevice]:
        """Discover all available storage devices.
        
        Returns:
            List of detected storage devices
        """
        devices = []
        
        try:
            if os.name == 'nt':  # Windows
                import string
                import ctypes
                
                # Check all drive letters
                available_drives = []
                bitmask = ctypes.windll.kernel32.GetLogicalDrives()
                for letter in string.ascii_uppercase:
                    if bitmask & 1:
                        available_drives.append(f"{letter}:")
                    bitmask >>= 1
                
                for drive in available_drives:
                    try:
                        # Get drive info
                        drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive + "\\")
                        type_map = {
                            0: 'unknown',
                            1: 'invalid',
                            2: 'removable',
                            3: 'fixed',
                            4: 'network',
                            5: 'cdrom',
                            6: 'ramdisk'
                        }
                        
                        # Get volume info
                        volume_name = ctypes.create_unicode_buffer(1024)
                        ctypes.windll.kernel32.GetVolumeInformationW(
                            ctypes.c_wchar_p(drive + "\\"),
                            volume_name,
                            ctypes.sizeof(volume_name),
                            None, None, None, None, 0
                        )
                        
                        # Get space info
                        free_bytes = ctypes.c_ulonglong(0)
                        total_bytes = ctypes.c_ulonglong(0)
                        ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                            drive + "\\",
                            None,
                            ctypes.pointer(total_bytes),
                            ctypes.pointer(free_bytes)
                        )
                        
                        device = StorageDevice(
                            drive_letter=drive,
                            mount_point=drive + "\\",
                            total_size=total_bytes.value,
                            free_size=free_bytes.value,
                            device_type=type_map.get(drive_type, 'unknown'),
                            label=volume_name.value if volume_name.value else None
                        )
                        devices.append(device)
                        
                    except Exception as e:
                        logger.warning(f"Could not get info for drive {drive}: {e}")
                        
            else:  # Unix/Mac
                import shutil
                
                # Common mount points
                mount_points = ['/mnt', '/media', '/Volumes']
                
                for mount_base in mount_points:
                    if os.path.exists(mount_base):
                        for item in os.listdir(mount_base):
                            mount_path = os.path.join(mount_base, item)
                            if os.path.ismount(mount_path):
                                try:
                                    usage = shutil.disk_usage(mount_path)
                                    device = StorageDevice(
                                        drive_letter=item,
                                        mount_point=mount_path,
                                        total_size=usage.total,
                                        free_size=usage.free,
                                        device_type='removable',
                                        label=item
                                    )
                                    devices.append(device)
                                except Exception as e:
                                    logger.warning(f"Could not get info for {mount_path}: {e}")
        
        except Exception as e:
            logger.error(f"Error discovering drives: {e}")
        
        self.devices = devices
        return devices
    
    def index_drive(self, drive: str, max_files: int = 10000) -> int:
        """Index important files on a drive.
        
        Args:
            drive: Drive letter or mount point (e.g., 'G:', '/mnt/usb')
            max_files: Maximum number of files to index
            
        Returns:
            Number of files indexed
        """
        indexed_count = 0
        
        try:
            drive_path = Path(drive)
            if not drive_path.exists():
                logger.warning(f"Drive {drive} not found")
                return 0
            
            logger.info(f"Indexing drive: {drive}")
            
            # Get all extensions we care about
            extensions = set()
            for category_exts in self.RESEARCH_PATTERNS.values():
                extensions.update(category_exts)
            
            # Walk the drive
            for root, dirs, files in os.walk(drive_path):
                # Skip system directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in [
                    'System Volume Information', '$RECYCLE.BIN', 'Windows',
                    'Program Files', 'Program Files (x86)', '__pycache__',
                    'node_modules', '.git'
                ]]
                
                for filename in files:
                    if indexed_count >= max_files:
                        break
                    
                    file_path = Path(root) / filename
                    file_ext = file_path.suffix.lower()
                    
                    # Check if this file type is interesting
                    if file_ext not in extensions:
                        continue
                    
                    try:
                        stat = file_path.stat()
                        
                        # Categorize file
                        categories = []
                        for category, exts in self.RESEARCH_PATTERNS.items():
                            if file_ext in exts:
                                categories.append(category)
                        
                        # Extract keywords from path
                        keywords = self._extract_keywords(str(file_path))
                        keywords.extend(categories)
                        
                        # Create metadata
                        metadata = FileMetadata(
                            path=str(file_path),
                            size=stat.st_size,
                            modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                            file_type=file_ext,
                            drive=drive,
                            keywords=list(set(keywords)),
                            description=self._generate_description(file_path, categories)
                        )
                        
                        self.file_index.append(metadata)
                        indexed_count += 1
                        
                    except Exception as e:
                        logger.debug(f"Could not index {file_path}: {e}")
                
                if indexed_count >= max_files:
                    break
            
            # Update device info
            for device in self.devices:
                if device.drive_letter == drive or device.mount_point == drive:
                    device.indexed = True
                    device.last_indexed = datetime.now().isoformat()
            
            # Save index
            self._save_index()
            
            logger.info(f"Indexed {indexed_count} files from {drive}")
            
        except Exception as e:
            logger.error(f"Error indexing drive {drive}: {e}")
        
        return indexed_count
    
    def search_files(
        self,
        query: str,
        file_types: Optional[List[str]] = None,
        drives: Optional[List[str]] = None,
        limit: int = 50
    ) -> List[FileMetadata]:
        """Search indexed files.
        
        Args:
            query: Search query (matches path, keywords, description)
            file_types: Filter by file extensions (e.g., ['.py', '.md'])
            drives: Filter by drives
            limit: Maximum results
            
        Returns:
            List of matching file metadata
        """
        query_lower = query.lower()
        results = []
        
        for file_meta in self.file_index:
            # Apply filters
            if file_types and file_meta.file_type not in file_types:
                continue
            
            if drives and file_meta.drive not in drives:
                continue
            
            # Check if query matches
            matches = False
            
            # Check path
            if query_lower in file_meta.path.lower():
                matches = True
            
            # Check keywords
            if any(query_lower in kw.lower() for kw in file_meta.keywords):
                matches = True
            
            # Check description
            if file_meta.description and query_lower in file_meta.description.lower():
                matches = True
            
            if matches:
                results.append(file_meta)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_special_locations(self) -> Dict[str, List[str]]:
        """Get special locations that have been detected.
        
        Returns:
            Dictionary of special location names to available paths
        """
        found = {}
        
        for name, paths in self.SPECIAL_LOCATIONS.items():
            available = []
            for path in paths:
                if os.path.exists(path):
                    available.append(path)
            
            if available:
                found[name] = available
        
        return found
    
    def find_ai_models(self) -> List[FileMetadata]:
        """Find all AI models on external drives.
        
        Returns:
            List of AI model files
        """
        return self.search_files(
            query='',
            file_types=['.gguf', '.safetensors', '.pt', '.pth', '.onnx']
        )
    
    def find_projects(self) -> Dict[str, List[str]]:
        """Find project directories.
        
        Returns:
            Dictionary of project types to paths
        """
        projects = {
            'python': [],
            'node': [],
            'git': [],
            'other': []
        }
        
        for file_meta in self.file_index:
            path = Path(file_meta.path)
            
            # Check for project markers
            if path.name == 'pyproject.toml' or path.name == 'setup.py':
                projects['python'].append(str(path.parent))
            elif path.name == 'package.json':
                projects['node'].append(str(path.parent))
            elif path.name == '.git':
                projects['git'].append(str(path.parent))
        
        return projects
    
    def get_drive_summary(self) -> str:
        """Get a summary of all discovered drives.
        
        Returns:
            Human-readable summary
        """
        if not self.devices:
            self.discover_drives()
        
        lines = ["📦 External Storage Summary:\n"]
        
        for device in self.devices:
            # Convert bytes to GB
            total_gb = device.total_size / (1024**3)
            free_gb = device.free_size / (1024**3)
            used_pct = ((device.total_size - device.free_size) / device.total_size * 100) if device.total_size > 0 else 0
            
            label = device.label or "Unlabeled"
            indexed = "✓ Indexed" if device.indexed else "✗ Not indexed"
            
            lines.append(
                f"  {device.drive_letter} ({label}) - {device.device_type}\n"
                f"    Size: {total_gb:.1f}GB total, {free_gb:.1f}GB free ({used_pct:.0f}% used)\n"
                f"    Status: {indexed}"
            )
            
            if device.last_indexed:
                lines.append(f"    Last indexed: {device.last_indexed}")
            
            lines.append("")
        
        # Add special locations
        special = self.get_special_locations()
        if special:
            lines.append("\n🎯 Special Locations Found:")
            for name, paths in special.items():
                lines.append(f"  {name}:")
                for path in paths:
                    lines.append(f"    - {path}")
        
        # Add index stats
        lines.append(f"\n📊 Index Statistics:")
        lines.append(f"  Total files indexed: {len(self.file_index)}")
        
        # Count by type
        type_counts = {}
        for file_meta in self.file_index:
            type_counts[file_meta.file_type] = type_counts.get(file_meta.file_type, 0) + 1
        
        if type_counts:
            lines.append("  Files by type:")
            for file_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                lines.append(f"    {file_type}: {count}")
        
        return "\n".join(lines)
    
    def _extract_keywords(self, path: str) -> List[str]:
        """Extract keywords from file path.
        
        Args:
            path: File path
            
        Returns:
            List of keywords
        """
        keywords = []
        
        # Split path and extract words
        parts = Path(path).parts
        for part in parts:
            # Split on common separators
            words = part.replace('-', ' ').replace('_', ' ').replace('.', ' ').split()
            # Filter out short words and numbers
            words = [w.lower() for w in words if len(w) > 2 and not w.isdigit()]
            keywords.extend(words)
        
        return keywords
    
    def _generate_description(self, path: Path, categories: List[str]) -> str:
        """Generate a description for a file.
        
        Args:
            path: File path
            categories: File categories
            
        Returns:
            Description string
        """
        parts = []
        
        if 'ai_models' in categories:
            parts.append("AI/ML model file")
        if 'docs' in categories:
            parts.append("Documentation")
        if 'code' in categories:
            parts.append("Source code")
        if 'data' in categories:
            parts.append("Data file")
        
        # Add parent folder info
        parent = path.parent.name
        if parent and parent not in ['.', '..']:
            parts.append(f"in {parent}")
        
        return " ".join(parts) if parts else path.name
    
    def _load_index(self):
        """Load index from disk."""
        try:
            if self.index_file.exists():
                with open(self.index_file, 'r') as f:
                    data = json.load(f)
                
                # Load devices
                self.devices = [StorageDevice(**d) for d in data.get('devices', [])]
                
                # Load file index
                self.file_index = [FileMetadata(**f) for f in data.get('files', [])]
                
                logger.info(f"Loaded index: {len(self.devices)} devices, {len(self.file_index)} files")
        
        except Exception as e:
            logger.error(f"Error loading index: {e}")
    
    def _save_index(self):
        """Save index to disk."""
        try:
            data = {
                'devices': [d.to_dict() for d in self.devices],
                'files': [f.to_dict() for f in self.file_index],
                'updated': datetime.now().isoformat()
            }
            
            with open(self.index_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info("Index saved successfully")
        
        except Exception as e:
            logger.error(f"Error saving index: {e}")


# Global instance
_storage_manager: Optional[ExternalStorageManager] = None


def get_storage_manager() -> ExternalStorageManager:
    """Get or create the global storage manager instance.
    
    Returns:
        ExternalStorageManager instance
    """
    global _storage_manager
    if _storage_manager is None:
        _storage_manager = ExternalStorageManager()
    return _storage_manager


# Convenience functions for easy access

def discover_drives() -> List[StorageDevice]:
    """Discover all available storage devices."""
    return get_storage_manager().discover_drives()


def index_drive(drive: str, max_files: int = 10000) -> int:
    """Index files on a drive."""
    return get_storage_manager().index_drive(drive, max_files)


def search_files(query: str, **kwargs) -> List[FileMetadata]:
    """Search indexed files."""
    return get_storage_manager().search_files(query, **kwargs)


def get_drive_summary() -> str:
    """Get summary of all drives."""
    return get_storage_manager().get_drive_summary()


def find_ai_models() -> List[FileMetadata]:
    """Find all AI models."""
    return get_storage_manager().find_ai_models()
