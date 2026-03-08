"""Configuration management using Pydantic Settings."""
from typing import List, Optional, Literal
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM API Configuration (支持 Anthropic 和 OpenAI 格式)
    api_key: Optional[str] = None  # API密钥
    base_url: Optional[str] = None  # API基础URL (如: https://api.anthropic.com 或 https://api.openai.com/v1)
    model_name: str = "claude-sonnet-4-6"  # 模型名称
    api_type: Literal["anthropic", "openai"] = "anthropic"  # API类型

    # Legacy support (向后兼容)
    anthropic_api_key: Optional[str] = None
    claude_model: Optional[str] = None

    # Other API Keys
    github_token: Optional[str] = None
    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    twitter_bearer_token: Optional[str] = None

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/trend_analyzer"
    redis_url: str = "redis://localhost:6379/0"

    # App Settings
    app_name: str = "Tech Trend Analyzer"
    debug: bool = False
    log_level: str = "INFO"

    # Collector Settings
    collector_timeout: int = 30
    collector_max_retries: int = 3
    collector_concurrent_limit: int = 5

    # Analysis Settings
    max_tokens: int = 4096
    analysis_timeout: int = 60

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_effective_api_key(self) -> Optional[str]:
        """获取有效的API密钥（支持新旧配置方式）"""
        return self.api_key or self.anthropic_api_key

    def get_effective_model(self) -> str:
        """获取有效的模型名称（支持新旧配置方式）"""
        return self.model_name or self.claude_model or "claude-sonnet-4-6"

    def get_effective_base_url(self) -> str:
        """获取有效的API基础URL"""
        if self.base_url:
            return self.base_url
        # 默认URL
        if self.api_type == "openai":
            return "https://api.openai.com/v1"
        return "https://api.anthropic.com"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()