"""Settings API endpoints."""
import os
from typing import List, Optional, Literal
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path

from ...core.config import get_settings, Settings

router = APIRouter(prefix="/settings", tags=["settings"])


class SettingsResponse(BaseModel):
    """Response model for settings."""
    api_key_masked: Optional[str] = None
    base_url: Optional[str] = None
    model_name: str
    api_type: Literal["anthropic", "openai"]
    default_sources: List[str]
    default_limit: int
    language: str = "zh"


class SettingsUpdateRequest(BaseModel):
    """Request model for updating settings."""
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_name: Optional[str] = None
    api_type: Optional[Literal["anthropic", "openai"]] = None
    default_sources: Optional[List[str]] = None
    default_limit: Optional[int] = None
    language: Optional[str] = None


def mask_api_key(key: Optional[str]) -> Optional[str]:
    """Mask API key for display."""
    if not key or len(key) < 8:
        return None
    return key[:4] + "..." + key[-4:]


def update_env_file(updates: dict) -> bool:
    """Update .env file with new settings."""
    try:
        env_path = Path(__file__).parent.parent.parent.parent / ".env"

        # Read existing .env content
        env_content = ""
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                env_content = f.read()

        # Parse existing lines
        lines = env_content.split("\n")
        env_dict = {}
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                env_dict[key.strip()] = value.strip().strip('"').strip("'")

        # Update with new values
        env_mapping = {
            "api_key": "API_KEY",
            "base_url": "BASE_URL",
            "model_name": "MODEL_NAME",
            "api_type": "API_TYPE",
            "default_sources": "DEFAULT_SOURCES",
            "default_limit": "DEFAULT_LIMIT",
        }

        for key, env_key in env_mapping.items():
            if key in updates and updates[key] is not None:
                value = updates[key]
                if isinstance(value, list):
                    value = ",".join(value)
                env_dict[env_key] = str(value)

        # Write back to .env
        new_lines = []
        for key, value in env_dict.items():
            new_lines.append(f'{key}="{value}"')

        with open(env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(new_lines) + "\n")

        return True
    except Exception as e:
        print(f"Error updating .env file: {e}")
        return False


@router.get("", response_model=SettingsResponse)
async def get_settings_api():
    """Get current application settings."""
    settings = get_settings()

    # Get default values from environment or use defaults
    default_sources = os.getenv("DEFAULT_SOURCES", "github,hackernews,web").split(",")
    default_limit = int(os.getenv("DEFAULT_LIMIT", "50"))
    language = os.getenv("LANGUAGE", "zh")

    return SettingsResponse(
        api_key_masked=mask_api_key(settings.get_effective_api_key()),
        base_url=settings.base_url,
        model_name=settings.get_effective_model(),
        api_type=settings.api_type,
        default_sources=default_sources,
        default_limit=default_limit,
        language=language,
    )


@router.put("", response_model=dict)
async def update_settings_api(request: SettingsUpdateRequest):
    """Update application settings."""
    try:
        # Update .env file
        updates = request.model_dump(exclude_none=True)
        env_updated = update_env_file(updates)

        # Clear the settings cache to force reload
        get_settings.cache_clear()

        return {
            "success": True,
            "message": "Settings updated successfully",
            "env_file_updated": env_updated,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update settings: {str(e)}")


@router.post("/reset", response_model=dict)
async def reset_settings_api():
    """Reset settings to defaults."""
    try:
        default_values = {
            "model_name": "claude-sonnet-4-6",
            "api_type": "anthropic",
            "default_sources": ["github", "hackernews", "web"],
            "default_limit": 50,
            "language": "zh",
        }

        env_updated = update_env_file(default_values)
        get_settings.cache_clear()

        return {
            "success": True,
            "message": "Settings reset to defaults",
            "env_file_updated": env_updated,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset settings: {str(e)}")