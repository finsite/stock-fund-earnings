"""Processor for stock earnings data (EPS, revenue, margins)."""

from typing import Any

from app.utils.setup_logger import setup_logger
from app.utils.types import validate_dict

logger = setup_logger(__name__)

REQUIRED_KEYS = ["symbol", "fiscal_date", "eps", "revenue", "net_income"]


def process(payloads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Process a batch of earnings data messages.

    Validates and enriches each message. Filters out invalid entries.

    Parameters
    ----------
    payloads : list[dict[str, Any]]
        A list of messages from the poller or queue.

    Returns
    -------
    list[dict[str, Any]]
        Cleaned and validated messages ready for output.
    """
    results: list[dict[str, Any]] = []

    for item in payloads:
        if not validate_dict(item, REQUIRED_KEYS):
            logger.warning("⚠️ Skipping message: missing required earnings fields: %s", item)
            continue

        try:
            # Optionally enrich or normalize fields here
            item["eps"] = float(item["eps"])
            item["revenue"] = float(item["revenue"])
            item["net_income"] = float(item["net_income"])
            results.append(item)
        except Exception as e:
            logger.exception("❌ Failed to process earnings data: %s | Error: %s", item, e)

    return results
