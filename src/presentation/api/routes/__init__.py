"""
API routes initialization.
"""

from .cv import cv_router
from .job import job_router
from .match import match_router

__all__ = ["cv_router", "job_router", "match_router"]
