

\# PolyGen - Generative Text-to-3D Asset Pipeline



\## Project Overview

PolyGen is a Generative AI project designed to transform text descriptions into 3D assets.



\## Current Features

\- FastAPI backend

\- Prompt input API

\- Prompt validation using Pydantic

\- Health check endpoint

\- Automated API testing using Pytest



\## Technology Stack

\- Python 3.13

\- FastAPI

\- Pydantic

\- Uvicorn

\- Pytest

\- Blender



\## Backend Structure

```text

backend/

├── main.py

├── api/

├── schemas/

├── services/

├── storage/

│   ├── uploads/

│   └── generated/

└── tests/

```



\## Run the Backend

```bash

uvicorn backend.main:app --reload

```



\## API Documentation

http://127.0.0.1:8000/docs



\## Run Tests

```bash

python -m pytest backend/tests -v

```



\## Current Development Status

Backend foundation and prompt validation completed.

Actual 3D generation integration is pending.




