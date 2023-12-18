"""
Main file for the app
"""
import asyncio

from . import run_application


async def main() -> None:
    """
    Start the app.
    """
    await run_application()


if __name__ == "__main__":
    asyncio.run(main())
