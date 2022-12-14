from pydantic import BaseSettings


class Settings(BaseSettings):
    """Read variables from evelopment with Settings declaration."""

    # Base
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str

    # Database
    db_async_connection_str: str

    # Test Database
    db_async_test_connection_str: str
