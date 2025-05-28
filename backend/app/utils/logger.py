"""Application-wide structured logging helper.

Uses python-json-logger for structured JSON logging.
"""

import logging
import sys
from python_json_logger import jsonlogger

# Custom fields to include in JSON logs
# See https://github.com/madzak/python-json-logger?tab=readme-ov-file#custom-fields
# for examples of adding custom fields.
# We can also add fields dynamically when logging: logger.info("message", extra={"key": "value"})
SUPPORTED_JSON_FIELDS = (
    "asctime",
    "filename",
    "funcName",
    "levelname", # Renamed to "level" by default by JsonFormatter
    "levelno",
    "lineno",
    "module",
    "message", # Renamed to "message" from "msg" by default
    "name",
    # "pathname", # Too verbose
    "process",
    "processName",
    "thread",
    "threadName",
    # "otelTraceID", # For OpenTelemetry, if used
    # "otelSpanID",  # For OpenTelemetry, if used
)

# More concise format string for the JsonFormatter
# The JsonFormatter will automatically rename 'levelname' to 'level' and 'asctime' to 'timestamp' (by default)
# if those are part of its `rename_fields`. We will use the default renaming.
# The format string here defines which attributes of the LogRecord are processed.
LOG_RECORD_FORMAT_STR = " ".join(f"%({field})" for field in SUPPORTED_JSON_FIELDS)


def configure_logging(level: str = "INFO") -> None:  # pragma: no cover
    """Configure logging to use JSON format."""
    
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Remove any existing handlers to avoid duplicate logs
    # (e.g., if basicConfig was called before or by a library)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()

    # Use a standard StreamHandler to output to stdout
    log_handler = logging.StreamHandler(sys.stdout)

    # Use JsonFormatter
    # The `format` kwarg to JsonFormatter defines which LogRecord attributes are captured.
    # The `rename_fields` kwarg (defaulting to {'levelname': 'level', 'asctime': 'timestamp'})
    # controls renaming of fields in the final JSON output.
    # `json_ensure_ascii=False` allows non-ASCII characters.
    formatter = jsonlogger.JsonFormatter(
        fmt=LOG_RECORD_FORMAT_STR,
        rename_fields={'levelname': 'level', 'asctime': 'timestamp'},
        json_ensure_ascii=False
    )
    
    log_handler.setFormatter(formatter)
    root_logger.addHandler(log_handler)

    # Configure loggers for common libraries to be less verbose if needed
    # logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    # logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    # logging.getLogger("fastapi").setLevel(logging.INFO)


# Expose a convenience logger for modules that do not need their own
# This will inherit the root logger's configuration.
logger = logging.getLogger("app")
