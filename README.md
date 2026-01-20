# Data Engineering Take-Home Test


This repository contains the starter code and instructions for the Senior Data Engineer Take-Home Test.

## Getting Started

1.  Read [INSTRUCTIONS.md](INSTRUCTIONS.md) **entirely** and **carefully** before beginning.
2.  Install dependencies ([uv](https://github.com/astral-sh/uv) recommended):
    ```bash
    uv sync
    ```
3.  Configure environment variables:
    ```bash
    cp .env.example .env
    # Add your KoboToolbox API token (provided via email) to .env
    ```
4.  Verify setup by running the starter pipeline:
    ```bash
    uv run main.py
    ```

## Files

*   `INSTRUCTIONS.md`: The detailed take-home test instructions.
*   `main.py`: Starter code for the ingestion pipeline.
*   `pyproject.toml` / `uv.lock`: Dependency management files.
