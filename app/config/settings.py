# standard imports
from typing import List

# package imports
from pydantic import BaseModel


class Settings(BaseModel):
    """
    All configuration parameters for the FastAPI application
    """

    # Cross-Origin Resource Sharing settings
    CORS_enabled: bool
    CORS_allow_origins: List[str]
    CORS_allow_credentials: bool
    CORS_allow_methods: List[str]
    CORS_allow_headers: List[str]

    @classmethod
    def get_default_settings(self):
        return Settings(
            CORS_enabled=True,
            CORS_allow_origins=["*"],
            CORS_allow_credentials=True,
            CORS_allow_methods=["*"],
            CORS_allow_headers=["*"],
        )
