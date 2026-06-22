"""Domain exceptions raised by the Penn Courses client.

Tools catch these and translate them into friendly, structured results so the
calling model receives actionable text instead of a stack trace.
"""

from __future__ import annotations


class PennCoursesError(Exception):
    """Base class for all penn-course-mcp errors."""


class CourseNotFound(PennCoursesError):
    """A requested course (or section) does not exist for the given semester."""

    def __init__(self, code: str, semester: str | None = None):
        self.code = code
        self.semester = semester
        suffix = f" in {semester}" if semester else ""
        super().__init__(f"Course '{code}' was not found{suffix}.")


class ReviewAuthRequired(PennCoursesError):
    """The detailed review endpoint requires an authenticated Penn session."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(
            f"Detailed reviews for '{code}' require authentication. "
            "Set PENN_COURSES_SESSION_COOKIE to enable them."
        )


class UpstreamError(PennCoursesError):
    """The upstream API returned an unexpected error or was unreachable."""

    def __init__(self, message: str, status: int | None = None):
        self.status = status
        super().__init__(message)
