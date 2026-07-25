"""
Career Recommendation Engine

This module combines all recommendation engines
into one interface for the Career Pipeline.
"""

# ==========================================================
# Imports
# ==========================================================

from app.engines.recommendation.course_engine import recommend_courses
from app.engines.recommendation.roadmap_engine import build_roadmap
from app.engines.recommendation.suggestion_engine import generate_suggestions


# ==========================================================
# Recommendation Engine
# ==========================================================

class RecommendationEngine:
    """
    Wrapper around all recommendation modules.
    """

    def generate(self, missing_skills):

        print("\nGenerating Recommendations...")

        # ------------------------------------------
        # Courses
        # ------------------------------------------

        courses = recommend_courses(
            missing_skills
        )

        print("Courses Generated")

        # ------------------------------------------
        # Roadmap
        # ------------------------------------------

        roadmap = build_roadmap(
            missing_skills
        )

        print("Roadmap Generated")

        # ------------------------------------------
        # Suggestions
        # ------------------------------------------

        suggestions = generate_suggestions(
            missing_skills
        )

        print("Suggestions Generated")

        return {

            "courses": courses,

            "roadmap": roadmap,

            "suggestions": suggestions

        }