"""Application-wide structured logging helper.

In production this can be replaced by loguru or structlog.  For the skeleton we
stick to the built-in `logging` module so that no extra dependency is required
at this stage.
"""

import logging
import sys


def configure_logging(level: str = "INFO") -> None:  # pragma: no cover
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        stream=sys.stdout,
    )


# Expose a convenience logger for modules that do not need their own
logger = logging.getLogger("app")
