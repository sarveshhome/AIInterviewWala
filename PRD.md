Act as a Principal Software Architect, Senior Python Architect, Senior React Native Architect, AI Engineer, and MongoDB Solution Architect.

Design and build a production-ready AI-powered mobile application called "AI Interview Coach" with the tagline:

"Make an impression with AI interview prep."

The application should use the Cohere LLM API (API key will be provided separately).

The solution must follow enterprise-level architecture and industry best practices, as if it were being developed by a FAANG engineering team.

=================================================
TECH STACK
=================================================

Frontend
---------
• React Native
• JSX
• Feature-Based Architecture
• Redux Toolkit
• React Query (TanStack Query)
• React Navigation
• Axios
• React Hook Form
• MMKV Storage
• NativeWind
• Reanimated
• Victory Charts
• Caching
• Lazy Loading
• Hook

Backend
--------
• Python
• FastAPI
• Clean Architecture
• CQRS
• Repository Pattern
• Unit of Work
• Dependency Injection
• SOLID Principles
• Domain Driven Design
• JWT Authentication
• OpenTelemetry
• Redis
• Celery
• Docker

Database
---------
• MongoDB Atlas

AI
---
• Cohere LLM API

=================================================
PROJECT OBJECTIVES
=================================================

The application should help experienced software engineers prepare for interviews using AI.

The AI should:

• Conduct mock interviews.
• Evaluate answers.
• Give scores.
• Explain mistakes.
• Suggest better answers.
• Generate follow-up questions.
• Track progress.
• Recommend learning paths.
• Analyze resumes.
• Conduct behavioral interviews.
• Conduct technical interviews.
• Conduct system design interviews.
• Conduct coding interviews.

=================================================
REQUIRED FEATURES
=================================================

1. Authentication
• Email Login
• Google Login
• LinkedIn Login
• JWT
• Refresh Token

2. Resume Upload
• PDF
• DOCX
• Resume parsing
• ATS score
• Skill extraction
• Experience extraction

3. Resume AI Analysis

Generate

• ATS score
• Missing skills
• Strong areas
• Weak areas
• Recommended improvements

4. AI Technical Interview

Support

.NET
React
React Native
Python
Kafka
GraphQL
Azure
AWS
GCP
Docker
Kubernetes
Microservices
MongoDB
SQL Server
Redis
System Design

The AI should:

Ask one question at a time.

Wait for the candidate answer.

Evaluate the answer.

Give a score.

Suggest an ideal answer.

Generate the next question.

5. Coding Interview

Support

Python
Java
C#
JavaScript
TypeScript

Evaluate

Correctness
Performance
Complexity
Naming
Architecture
Security
Best Practices

6. Behavioral Interview

Evaluate using STAR framework.

Return

Leadership
Communication
Ownership
Conflict Resolution
Decision Making

7. System Design Interview

Generate enterprise-level interview questions.

Evaluate

Scalability
Caching
Messaging
Database
Load Balancing
Trade-offs
Security
Cloud Architecture

8. Voice Interview

Speech-to-Text

AI Evaluation

Text-to-Speech

9. AI Career Coach

Provide recommendations for

Learning roadmap
Career growth
Salary improvement
Leadership skills
Architecture skills

10. Analytics Dashboard

Show

Interview history
Average score
Weak areas
Strong areas
Progress graph
Technology-wise performance

=================================================
BACKEND REQUIREMENTS
=================================================

Follow Clean Architecture.

Create folders for

domain/
application/
infrastructure/
presentation/
config/
tests/

Include

Repositories
Entities
Value Objects
DTOs
Use Cases
Interfaces
Dependency Injection
Exception Handling
Logging
Validation
Middleware

=================================================
FRONTEND REQUIREMENTS
=================================================

Follow Feature Architecture.

Create

features/
core/
shared/
navigation/
components/
services/
hooks/
models/

Use

Redux Toolkit
React Query
Axios
React Navigation

=================================================
DATABASE DESIGN
=================================================

Design MongoDB collections.

Include

users
interviews
questions
answers
feedback
analytics
resume
learningRoadmap

=================================================
REST APIs
=================================================

Generate REST APIs.

Examples

POST /auth/login

POST /resume/upload

POST /interview/start

POST /interview/answer

GET /dashboard

POST /chat

GET /analytics

=================================================
AI PROMPTS
=================================================

Create optimized Cohere prompts.

Examples

Resume Analysis

Technical Interview

Behavioral Interview

Coding Review

System Design Review

Career Coach

Learning Roadmap

Return structured JSON.

=================================================
OUTPUT FORMAT
=================================================

Provide:

1. Complete Software Architecture

2. High-Level Architecture Diagram

3. Folder Structure

4. Database Design

5. API Design

6. Domain Model

7. Use Cases

8. Sequence Diagrams

9. Class Diagrams

10. MongoDB Schema

11. Backend Source Code

12. React Native Source Code

13. Authentication Implementation

14. Cohere Integration

15. Docker Configuration

16. Docker Compose

17. Kubernetes Manifests

18. CI/CD Pipeline

19. Unit Tests

20. Integration Tests

21. Deployment Guide

22. Security Best Practices

23. Performance Optimization

24. Caching Strategy

25. Logging

26. Monitoring

27. Rate Limiting

28. Production Readiness Checklist

29. Coding Standards

30. Step-by-step implementation from scratch.

The generated project should be enterprise-grade, scalable, maintainable, production-ready, and suitable for a Senior Technical Lead with 15+ years of experience.