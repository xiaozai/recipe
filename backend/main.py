#!/usr/bin/env python
"""Entry point for the Tech Trend Analyzer backend."""
import uvicorn
from app import create_app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )