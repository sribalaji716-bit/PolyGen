\# PolyGen – Generative Text-to-3D Asset Pipeline



\## Project Overview

PolyGen is a Generative AI project designed to transform

text descriptions into 3D assets.



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



backend/

\- main.py

\- api/

\- schemas/

\- services/

\- storage/

\- tests/



\## Run the Backend



```bash

uvicorn backend.main:app --reload

