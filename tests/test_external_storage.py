"""Tests for external storage research module."""

import pytest
from pathlib import Path
from jc.external_storage import (
    ExternalStorageManager,
    StorageDevice,
    FileMetadata,
    discover_drives,
    get_drive_summary,
    search_files
)


def test_storage_device_creation():
    """Test StorageDevice dataclass."""
    device = StorageDevice(
        drive_letter="G:",
        mount_point="G:\\",
        total_size=1000000000,
        free_size=500000000,
        device_type="removable",
        label="USB Drive"
    )
    
    assert device.drive_letter == "G:"
    assert device.device_type == "removable"
    assert device.label == "USB Drive"
    assert device.indexed is False
    
    # Test to_dict
    data = device.to_dict()
    assert isinstance(data, dict)
    assert data['drive_letter'] == "G:"


def test_file_metadata_creation():
    """Test FileMetadata dataclass."""
    metadata = FileMetadata(
        path="G:\\test\\model.gguf",
        size=5000000,
        modified="2025-01-15T10:00:00",
        file_type=".gguf",
        drive="G:",
        keywords=["ai", "model", "llama"],
        description="AI/ML model file"
    )
    
    assert metadata.file_type == ".gguf"
    assert "ai" in metadata.keywords
    assert metadata.description == "AI/ML model file"


def test_storage_manager_init():
    """Test ExternalStorageManager initialization."""
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        manager = ExternalStorageManager(storage_dir=Path(tmpdir))
        
        assert manager.storage_dir.exists()
        assert isinstance(manager.devices, list)
        assert isinstance(manager.file_index, list)


def test_discover_drives():
    """Test drive discovery."""
    manager = ExternalStorageManager()
    devices = manager.discover_drives()
    
    # Should return a list (may be empty if no drives)
    assert isinstance(devices, list)
    
    # If devices found, check structure
    if devices:
        device = devices[0]
        assert hasattr(device, 'drive_letter')
        assert hasattr(device, 'total_size')
        assert hasattr(device, 'device_type')


def test_extract_keywords():
    """Test keyword extraction from paths."""
    manager = ExternalStorageManager()
    
    keywords = manager._extract_keywords("G:\\BunkerAI\\models\\llama-3.1-8B.gguf")
    
    # Should extract meaningful words
    assert "bunkerai" in keywords or "bunker" in keywords
    assert "models" in keywords
    assert "llama" in keywords
    
    # Should filter out short words and extensions
    assert "gguf" not in keywords or len(keywords) > 3


def test_generate_description():
    """Test description generation."""
    manager = ExternalStorageManager()
    
    path = Path("G:\\models\\llama.gguf")
    description = manager._generate_description(path, ['ai_models'])
    
    assert "AI/ML model" in description
    assert "models" in description.lower()


def test_search_files_empty():
    """Test searching with no indexed files."""
    manager = ExternalStorageManager()
    results = manager.search_files("test")
    
    assert isinstance(results, list)
    assert len(results) == 0


def test_search_files_with_data():
    """Test searching with indexed files."""
    manager = ExternalStorageManager()
    
    # Add test data
    manager.file_index = [
        FileMetadata(
            path="G:\\test\\model.gguf",
            size=5000000,
            modified="2025-01-15T10:00:00",
            file_type=".gguf",
            drive="G:",
            keywords=["ai", "model", "llama"],
            description="AI/ML model file"
        ),
        FileMetadata(
            path="G:\\docs\\readme.md",
            size=5000,
            modified="2025-01-15T10:00:00",
            file_type=".md",
            drive="G:",
            keywords=["readme", "docs"],
            description="Documentation"
        )
    ]
    
    # Search for AI models
    results = manager.search_files("model")
    assert len(results) == 1
    assert results[0].file_type == ".gguf"
    
    # Search for docs
    results = manager.search_files("readme")
    assert len(results) == 1
    assert results[0].file_type == ".md"
    
    # Search with file type filter
    results = manager.search_files("", file_types=[".gguf"])
    assert len(results) == 1
    assert results[0].file_type == ".gguf"


def test_find_ai_models():
    """Test finding AI models."""
    manager = ExternalStorageManager()
    
    # Add test data
    manager.file_index = [
        FileMetadata(
            path="G:\\model1.gguf",
            size=5000000,
            modified="2025-01-15T10:00:00",
            file_type=".gguf",
            drive="G:",
            keywords=["ai", "model"],
            description="AI model"
        ),
        FileMetadata(
            path="G:\\model2.safetensors",
            size=3000000,
            modified="2025-01-15T10:00:00",
            file_type=".safetensors",
            drive="G:",
            keywords=["ai", "model"],
            description="AI model"
        ),
        FileMetadata(
            path="G:\\readme.md",
            size=1000,
            modified="2025-01-15T10:00:00",
            file_type=".md",
            drive="G:",
            keywords=["docs"],
            description="Documentation"
        )
    ]
    
    models = manager.find_ai_models()
    
    assert len(models) == 2
    assert all(m.file_type in ['.gguf', '.safetensors'] for m in models)


def test_get_special_locations():
    """Test special location detection."""
    manager = ExternalStorageManager()
    
    # This will return locations that actually exist on the system
    special = manager.get_special_locations()
    
    assert isinstance(special, dict)
    # Keys should match SPECIAL_LOCATIONS
    for key in special.keys():
        assert key in manager.SPECIAL_LOCATIONS


def test_get_drive_summary():
    """Test drive summary generation."""
    manager = ExternalStorageManager()
    manager.discover_drives()
    
    summary = manager.get_drive_summary()
    
    assert isinstance(summary, str)
    assert "External Storage Summary" in summary
    assert "📦" in summary or "External Storage" in summary


def test_convenience_functions():
    """Test module-level convenience functions."""
    # These should not raise errors
    devices = discover_drives()
    assert isinstance(devices, list)
    
    summary = get_drive_summary()
    assert isinstance(summary, str)
    
    results = search_files("test")
    assert isinstance(results, list)
