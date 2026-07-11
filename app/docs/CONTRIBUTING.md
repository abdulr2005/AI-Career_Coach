# Contributing

First of all, thank you for taking the time to contribute to AI Career Coach.

This project is built to help people, not to generate profit.

If your work helps even one person find a better career, then your contribution has already made a difference.

---

# Before You Start

Please read the documentation inside the docs folder.

Recommended reading order:

1. PROJECT_VISION.md
2. CURRENT_PROGRESS.md
3. ARCHITECTURE.md
4. TASKS.md

These documents explain the project before you start writing code.

---

# Development Philosophy

Keep everything modular.

Avoid writing large files.

One file should have one responsibility.

Avoid hardcoding values.

Always think about scalability.

Write readable code.

Future developers should understand your code without asking questions.

---

# Folder Rules

Artificial Intelligence code belongs inside

app/engines/

or

app/ai/

Backend code belongs inside

app/api/

app/services/

Database code belongs inside

app/database/

Shared utilities belong inside

app/utils/

Configuration belongs inside

app/core/

Never mix responsibilities.

---

# Branch Strategy

main

Stable production branch.

develop

Current development branch.

feature/<feature-name>

Every new feature should have its own branch.

Examples

feature/job-matching

feature/interview-ai

feature/chatbot

feature/roadmap

---

# Commit Messages

Good examples

feat: add job matching engine

fix: improve project splitter

docs: update architecture

refactor: simplify ATS analyzer

Avoid messages like

update

fix

changes

done

---

# Pull Requests

Before opening a Pull Request:

Make sure the project runs.

Remove debugging code.

Remove unused imports.

Write meaningful commit messages.

Explain what was changed.

---

# Coding Style

Follow PEP8.

Use descriptive function names.

Avoid duplicated code.

Write reusable modules.

Document complex logic.

---

# AI Modules

Every AI module should:

Receive structured input.

Return structured output.

Avoid UI logic.

Avoid database logic.

Remain completely independent.

---

# Backend Modules

Backend should never implement AI logic.

Backend only:

Receives requests.

Calls AI modules.

Returns responses.

Stores user data.

Handles authentication.

---

# Documentation

Every important feature should include documentation.

If you create a new module, explain:

What it does.

Input.

Output.

Dependencies.

Example usage.

---

# Final Goal

The goal is not simply to write code.

The goal is to build a platform that genuinely helps people improve their careers.

Every contribution should move the project closer to that vision.