"""Builder of the FastAPI application instance.

This is separate from main.py as the app needs to be created
inside the loop on Azure."""
# pylint: disable=import-outside-toplevel

import typing

if typing.TYPE_CHECKING:
    import fastapi


def build_app() -> "fastapi.FastAPI":
    """Builds and returns a FastAPI application instance with the necessary
    routers and middleware.

    Returns:
        fastapi.FastAPI: The FastAPI application instance.

    Notes:
        Imports inside the function to avoid circular imports.
    """
    import logging

    import fastapi
    from fastapi.middleware import cors

    from src.core import settings
    from src.routers.features import views as feature_views
    from src.routers.surfaces import views as surface_views

    config = settings.get_settings()

    settings.initialize_logger()
    logger = logging.getLogger(config.LOGGER_NAME)

    api = fastapi.APIRouter(prefix="/api")
    api.include_router(feature_views.router)
    api.include_router(surface_views.router)

    logger.info("Starting API.")
    app = fastapi.FastAPI()
    app.include_router(api)

    logger.info("Adding CORS middleware.")
    app.add_middleware(
        cors.CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
