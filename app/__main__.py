"""
Main file for the app
"""
import asyncio
import logging

from . import run_application

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Start the app.
    """
    await run_application()


if __name__ == "__main__":
    asyncio.run(main())
