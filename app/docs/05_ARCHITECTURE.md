# Project Architecture

The project is divided into two completely independent parts.

Part One

Artificial Intelligence

Responsible for:

Resume Analysis

ATS

Matching

Recommendation

Roadmaps

Interview AI

Speech Analysis

Vision Analysis

LLMs

------------------------------------------------

Part Two

Software Engineering

Responsible for:

Authentication

Database

Backend

Frontend

Deployment

Docker

Security

Monitoring

------------------------------------------------

The only connection between both parts is the API.

The backend sends data.

The AI returns structured results.

Nothing else should be shared between both systems.

This keeps the project scalable and allows both developers to work independently.