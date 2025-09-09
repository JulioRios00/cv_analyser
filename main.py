#!/usr/bin/env python3
"""
CV Analyzer startup script.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    import uvicorn

    from src.config import settings

    print(f"Starting {settings.app_name} v{settings.app_version}")
    print(
        f"Server will be available at: http://{settings.host}:{settings.port}"
    )
    print(f"API Documentation: http://{settings.host}:{settings.port}/docs")
    print(f"Health Check: http://{settings.host}:{settings.port}/health")
    print()

    if not settings.is_ai_configured():
        print("❌ Google API key not configured!")

    uvicorn.run(
        "src.presentation.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
