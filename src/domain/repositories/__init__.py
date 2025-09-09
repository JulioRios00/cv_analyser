"""
Repository interfaces defining contracts for data access.
These are abstractions that will be implemented by infrastructure layer.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities import CV, Job, Match


class CVRepository(ABC):
    """Abstract repository for CV data operations."""

    @abstractmethod
    async def save(self, cv: CV) -> CV:
        """Save a CV and return the saved entity with ID."""
        pass

    @abstractmethod
    async def find_by_id(self, cv_id: str) -> Optional[CV]:
        """Find a CV by its ID."""
        pass

    @abstractmethod
    async def find_all(self, limit: int = 100, offset: int = 0) -> List[CV]:
        """Find all CVs with pagination."""
        pass

    @abstractmethod
    async def delete(self, cv_id: str) -> bool:
        """Delete a CV by ID. Returns True if deleted, False if not found."""
        pass


class JobRepository(ABC):
    """Abstract repository for Job data operations."""

    @abstractmethod
    async def save(self, job: Job) -> Job:
        """Save a job and return the saved entity with ID."""
        pass

    @abstractmethod
    async def find_by_id(self, job_id: str) -> Optional[Job]:
        """Find a job by its ID."""
        pass

    @abstractmethod
    async def find_all(self, limit: int = 100, offset: int = 0) -> List[Job]:
        """Find all jobs with pagination."""
        pass

    @abstractmethod
    async def delete(self, job_id: str) -> bool:
        """Delete a job by ID. Returns True if deleted, False if not found."""
        pass


class MatchRepository(ABC):
    """Abstract repository for Match data operations."""

    @abstractmethod
    async def save(self, match: Match) -> Match:
        """Save a match and return the saved entity with ID."""
        pass

    @abstractmethod
    async def find_by_id(self, match_id: str) -> Optional[Match]:
        """Find a match by its ID."""
        pass

    @abstractmethod
    async def find_by_cv_and_job(self, cv_id: str, job_id: str) -> List[Match]:
        """Find matches between a specific CV and job."""
        pass

    @abstractmethod
    async def find_by_cv_id(self, cv_id: str) -> List[Match]:
        """Find all matches for a specific CV."""
        pass

    @abstractmethod
    async def find_by_job_id(self, job_id: str) -> List[Match]:
        """Find all matches for a specific job."""
        pass

    @abstractmethod
    async def find_all(self, limit: int = 100, offset: int = 0) -> List[Match]:
        """Find all matches with pagination."""
        pass

    @abstractmethod
    async def delete(self, match_id: str) -> bool:
        """
        Delete a match by ID. Returns True if deleted, False if not found.
        """
        pass
