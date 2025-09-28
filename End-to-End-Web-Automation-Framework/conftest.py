import pytest
from pages.page_manager import PageManager


@pytest.fixture(scope="class")
def pages():
    """Provides a fresh PageManager object per test class."""
    manager = PageManager()
    yield manager