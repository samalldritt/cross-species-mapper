""" View definitions for the features router. """
import logging

import fastapi
from fastapi import status
from src import settings
from src.routers.features import controller, schemas

router = fastapi.APIRouter(prefix="/features", tags=["features"])

config = settings.get_settings()
LOGGER_NAME = config.LOGGER_NAME
logger = logging.getLogger(LOGGER_NAME)


@router.get(
    "/cross_species",
    responses={status.HTTP_200_OK: {"model": list[schemas.FeatureSimilarity]}},
)
def get_feature_similarity(
    seed_species: str = fastapi.Query(
        ..., example="human", description="The species to fetch the hemispheres for."
    ),
    seed_side: str = fastapi.Query(
        ..., example="left", description="The hemisphere to fetch the surfaces for."
    ),
    seed_vertex: int = fastapi.Query(
        ...,
        example=1,
        description="The vertex to fetch the feature similarity for, 0-indexed.",
    ),
) -> dict[str, list[float]]:
    """Fetches the human and macaque feature matrices.

    Args:
        species: The species where the seed is, valid values are
            'human' and 'macaque'.
        side: The hemisphere where the seed is, valid values are 'left' and
            'right'.
        vertex: The vertex to fetch the feature similarity for, 0-indexed.

    Returns:
        A Pydantic BaseClass containing the feature vectors for similarity to
        the seed vertex.
    """
    logger.info("Calling GET /surfaces/similarity endpoint.")
    return controller.get_cross_species_features(seed_species, seed_side, seed_vertex)


@router.get(
    "/nimare",
    response_model=schemas.NiMareFeatures,
    summary="Get NeuroQuery features for a surface.",
    description="Get NeuroQuery features for a surface.",
    responses={
        status.HTTP_200_OK: {
            "description": "NeuroQuery features for a surface.",
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Invalid coordinates."},
    },
)
async def get_nimare_features(
    x: float = fastapi.Query(..., description="The x coordinate."),
    y: float = fastapi.Query(..., description="The y coordinate."),
    z: float = fastapi.Query(..., description="The z coordinate."),
) -> schemas.NiMareFeatures:
    """Get NeuroQuery features for a surface."""
    logger.info("Calling POST /features/neurosynth endpoint.")
    return controller.get_nimare_features(x, y, z)
