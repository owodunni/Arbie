"""Main init."""

from Arbie.exception import (  # noqa: F401
    DeployContractError,
    IERC20TokenError,
    PoolValueError,
    StateError,
)
from Arbie.settings_parser import SettingsParser  # noqa: F401

__version__ = "0.4.0"  # noqa: WPS410
__version_info__ = tuple(
    int(i) for i in __version__.split(".") if i.isdigit()
)  # noqa: WPS221
