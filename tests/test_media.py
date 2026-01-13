# Test cases for media functionality
import pytest
from backend.models.media import Media

def test_media_model():\n    \"\"\"Test media model creation\"\"\"\n    media = Media(\n        filename=\"test.jpg\",\n        original_filename=\"test.jpg\",\n        file_path=\"/uploads/test.jpg\",\n        file_size=1024,\n        mime_type=\"image/jpeg\"\n    )\n    assert media.filename == \"test.jpg\"\n    assert media.mime_type == \"image/jpeg\"