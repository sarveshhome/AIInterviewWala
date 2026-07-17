"""Entrypoint for uvicorn: `uvicorn main:app --reload`."""
from presentation.app import app

if __name__ == "__main__":
    import uvicorn
    from config.settings import settings

    uvicorn.run("presentation.app:app", host=settings.app_host, port=settings.app_port,
                reload=settings.app_debug, log_level=settings.log_level.lower())