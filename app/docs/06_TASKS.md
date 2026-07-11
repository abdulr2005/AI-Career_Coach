# AI Career Coach Architecture

This document explains the overall architecture of AI Career Coach.

The platform is designed as a modular AI system.

Every component has one responsibility.

No module should know the implementation details of another module.

---

# High Level Architecture

                    User
                      │
                      │
                Frontend UI
                      │
                      │
                  FastAPI API
                      │
        ┌─────────────┴─────────────┐
        │                           │
        │                           │
    Database                    AI Engine
                                    │
        ┌───────────────────────────┼────────────────────────────┐
        │                           │                            │
        │                           │                            │
 Resume Analysis             Job Analysis                  Interview AI
        │                           │                            │
        ├──────────────┐            │                            │
        │              │            │                            │
 ATS Engine      Resume Parser   Matching Engine          Voice Analysis
        │                           │                            │
        │                           │                            │
 Recommendation Engine      Roadmap Engine            Vision Analysis
        │                           │                            │
        └──────────────┬────────────┴──────────────┬─────────────┘
                       │
                 LLM Career Assistant

---

# Layer 1

Frontend

Responsibilities

- User Interface
- Upload Resume
- Upload Job Description
- Display Reports
- Authentication
- Dashboard

The frontend never performs AI computations.

---

# Layer 2

Backend API

Responsibilities

- Receive requests
- Validate input
- Store user data
- Call AI modules
- Return responses

The backend never contains AI logic.

---

# Layer 3

Artificial Intelligence

This is the brain of the platform.

Modules include

Resume Analysis

ATS Engine

Job Description Analysis

Matching Engine

Roadmap Generator

Recommendation Engine

Interview AI

Voice AI

Vision AI

LLM Career Assistant

Each module works independently.

---

# Layer 4

Database

Stores

Users

CVs

Job Descriptions

Reports

Roadmaps

Courses

Interview Sessions

Chat History

Analytics

---

# AI Pipeline

Resume PDF

↓

Resume Cleaning

↓

Section Parsing

↓

Skill Extraction

↓

Experience Analysis

↓

Project Analysis

↓

Certification Analysis

↓

ATS Score

↓

Resume Report

---

Job Description

↓

Cleaning

↓

Section Detection

↓

Skill Extraction

↓

Requirement Extraction

↓

Responsibility Detection

↓

Experience Detection

↓

Job Profile

---

Resume Profile

+

Job Profile

↓

Matching Engine

↓

Similarity Analysis

↓

Missing Skills

↓

Strengths

↓

Weaknesses

↓

Recommendations

↓

Learning Roadmap

↓

Course Recommendation

↓

Interview Preparation

---

# AI Independence

Every AI module must

Receive structured input

Return structured output

Contain no UI code

Contain no database code

Contain no API code

Remain reusable

---

# API Communication

Frontend

↓

FastAPI

↓

AI Engine

↓

JSON Response

↓

Frontend

Only JSON should travel between layers.

---

# Scalability

Future AI models can be replaced without changing the frontend.

Future frontend frameworks can be replaced without changing AI.

Database can change independently.

Every layer is isolated.

---

# Long-Term Vision

The platform should become an intelligent career ecosystem capable of helping users from any profession.

Every future feature should fit into this architecture.