"""Test pydantic-all-in-one."""

import pyd4all


def test_import() -> None:
    """Test that the package can be imported."""
    assert isinstance(pyd4all.__name__, str)
