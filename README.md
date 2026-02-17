# Auberge - Microservices Application

## Overview
Three microservices for LLM integration with content sanitization:
1. **LLM Service** (port 3000) - Mistral AI integration
2. **Guardrails Service** (port 3001) - Text transformation rules in Firebase
3. **Auberge Service** (port 3002) - LLM orchestration with guardrails

## Setup

Set environment variables:
```powershell
$env:MISTRAL_API_KEY = "your_api_key"
$env:FIREBASE_DB = "your_firebase_url"
```

Uses standard Anaconda packages (Flask, requests, re, os).

## Running Services

Start all three in separate terminals:
```powershell
python llm.py       # Port 3000
python guardrails.py  # Port 3001
python auberge.py   # Port 3002
```

## API Endpoints

**LLM** `POST /llm` - `{"prompt": "..."}`
**Guardrails** `PUT /guardrails/{id}` - `{"regx": "...", "sub": "..."}`
**Guardrails** `GET /guardrails/{id}` | `GET /guardrails` | `DELETE /guardrails/{id}`
**Auberge** `POST /auberge` - `{"prompt": "..."}` (applies guardrails to prompt & output)

## Testing

Run all tests (services must be running):
```powershell
python -m unittest test5 -v
```

Tests: LLM integration, guardrail CRUD, regex validation, full integration.

## Architecture

Auberge → LLM + Guardrails → Firebase
