# Multi AI Agent — Run & Development notes

Quick notes to run the project locally and why some files insert the project root into PYTHONPATH.

Recommended (clean) way to run

- Start backend (FastAPI) from the project root:

  ```powershell
  cd C:\path\to\multi-ai-agent
  .venv\Scripts\uvicorn app.backend.api:app --host 127.0.0.1 --port 9999
  ```

- Start frontend (Streamlit) from the project root:

  ```powershell
  cd C:\path\to\multi-ai-agent
  .venv\Scripts\streamlit run app/frontend/ui.py
  ```

Why some modules insert the project root into sys.path

Modules like `app/frontend/ui.py` and `app/main.py` add the project root to `sys.path` so package-style imports
(e.g. `from app.config.settings import settings`) work when the file is executed directly from different working directories
(for example running `python app/main.py` vs `python -m app.main` or using `streamlit run`). This is a pragmatic convenience so the app is friendlier to local runs.

Best practice

- Prefer running services from the project root or using `python -m` so imports are handled naturally.
- The small sys.path insertion is an intentional convenience for local development, but a production deployment should rely on proper packaging and environment configuration.
