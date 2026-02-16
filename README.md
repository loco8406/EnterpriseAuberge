# Enterprise Computing CA - Microservices Application

## Overview
This application consists of three microservices:
1. **LLM Service** - Integrates with Mistral AI for language model responses
2. **Guardrails Service** - Manages text transformation rules stored in Firebase
3. **Auberge Service** - Orchestrates LLM calls with guardrail applications

## Prerequisites
- Anaconda Python distribution (no additional packages required)
- Mistral API key
- Firebase Realtime Database URL

## Installation

**No installation required** - This project uses only packages included in the standard Anaconda distribution (Flask, requests, re, os).

### Configuration

API keys and database URLs are configured directly in the source files:
- Edit `MISTRAL_API_KEY` in `llm.py` (line 8)
- Edit `FIREBASE_DB` in `guardrails.py` (line 8) and `database.py` (line 7)

Alternatively, set environment variables before running:
```bash
set MISTRAL_API_KEY=your_mistral_api_key
set FIREBASE_DB=your_firebase_database_url
```

## Running the Services

You need to run all three services simultaneously in separate terminals:

### Terminal 1 - LLM Service
```bash
python llm.py
```
Runs on: `http://localhost:3000`

### Terminal 2 - Guardrails Service
```bash
python guardrails.py
```
Runs on: `http://localhost:3001`

### Terminal 3 - Auberge Service
```bash
python auberge.py
```
Runs on: `http://localhost:3002`

## API Endpoints

### LLM Service
- **POST** `/llm`
  - Body: `{"prompt": "your question"}`
  - Response: `{"output": "AI response"}`

### Guardrails Service
- **PUT** `/guardrails/{id}`
  - Body: `{"regx": "regex_pattern", "sub": "replacement"}`
  - Response: 201 Created
  
- **GET** `/guardrails/{id}`
  - Response: `{"id": "...", "regx": "...", "sub": "..."}`
  
- **GET** `/guardrails`
  - Response: Array of all guardrails

### Auberge Service
- **POST** `/auberge`
  - Body: `{"prompt": "your question"}`
  - Response: `{"output": "AI response with guardrails applied"}`

## Running Tests

1. Ensure all three services are running
2. Run the test suite:
```bash
python -m unittest test5.py
```

## Test Cases

1. **test_001_llm** - Tests LLM service responds correctly
2. **test_002_guardrails** - Tests guardrail creation and retrieval
3. **test_003_guardrails** - Tests email regex guardrail
4. **test_004_guardrails** - Tests invalid regex validation
5. **test_005_auberge** - Tests full integration with multiple guardrails

## Architecture

```
┌─────────┐      ┌──────────────┐      ┌────────────┐
│ Client  │─────▶│   Auberge    │─────▶│  LLM       │
│         │      │  (Port 3002) │      │ (Port 3000)│
└─────────┘      └──────┬───────┘      └────────────┘
                        │                     │
                        ▼                     ▼
                 ┌──────────────┐      ┌─────────┐
                 │ Guardrails   │─────▶│Firebase │
                 │ (Port 3001)  │      │   DB    │
                 └──────────────┘      └─────────┘
```

## Files Description

- `llm.py` - LLM microservice (Mistral AI integration)
- `guardrails.py` - Guardrails microservice (regex rules management)
- `auberge.py` - Orchestration microservice
- `database.py` - Database helper utilities
- `test5.py` - Unit tests for all services
- `requirements.txt` - Notes on dependencies (Anaconda-compatible)

## Notes

- All services must be running for tests to pass
- Firebase database is cleared before each relevant test
- Guardrails are applied in the order they are stored
- This project runs on standard Anaconda without pip installations
