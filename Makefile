.PHONY: help install up down test lint seed run-agent

help:
	@echo "AI Incident Copilot - Available commands:"
	@echo "  make install    Install Python dependencies"
	@echo "  make up         Start PostgreSQL with pgvector in Docker"
	@echo "  make down       Stop local Docker containers"
	@echo "  make seed       Seed historical post-mortems into PostgreSQL"
	@echo "  make test       Run test suite"
	@echo "  make run-agent  Execute local multi-agent triage simulation"

install:
	pip install -r requirements.txt

up:
	docker compose up -d

down:
	docker compose down

seed:
	docker compose exec -T postgres psql -U incident_user -d incident_memory < database/seed_incidents.sql

test:
	pytest tests/ -v

run-agent:
	python -m agent.graph
