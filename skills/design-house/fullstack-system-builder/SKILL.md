---
name: fullstack-system-builder
description: End-to-end full-stack software architecture standard. Use when building production-grade web applications with modern backend, database, cache, authentication, and frontend stacks.
---

# Fullstack System Builder Skill

This skill defines the modern full-stack engineering blueprint for high-performance, type-safe web applications.

## 1. Recommended Tech Stacks

### Stack A: Next.js + Tailwind + Prisma / Drizzle + PostgreSQL
- **Frontend**: Next.js (App Router, Server Components), Tailwind CSS v4, Lucide Icons, Shadcn UI.
- **Backend**: Next.js Server Actions & Route Handlers or Fastify/Express microservices.
- **Database**: PostgreSQL with Prisma ORM or Drizzle ORM.
- **Cache / Queue**: Redis + BullMQ for asynchronous worker jobs.

### Stack B: FastAPI + React / Vite + SQLAlchemy + PostgreSQL
- **Frontend**: Vite + React, TanStack Query, Tailwind CSS, Framer Motion.
- **Backend**: FastAPI (Python 3.12+), Pydantic v2, Async SQLAlchemy.
- **Database**: PostgreSQL (with pgvector for AI semantic embeddings).
- **Background Tasks**: Celery / ARQ / Redis.

## 2. API Design & Security Standards

1. **Authentication**: Auth.js / NextAuth, Clerk, Supabase Auth, or standard JWT with HTTP-only cookies.
2. **Input Validation**: Strict Zod schemas on TypeScript frontends, Pydantic on Python backends.
3. **Database Migrations**: Always manage schema changes through declarative migrations (`npx prisma migrate dev` or `alembic revision --autogenerate`).
4. **Environment Secrets**: Never commit `.env` secrets; provide `.env.example` templates.
