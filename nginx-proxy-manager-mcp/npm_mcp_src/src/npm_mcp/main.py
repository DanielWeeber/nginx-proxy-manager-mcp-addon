"""Entry point for npm-mcp server."""

import argparse
import logging
import sys
from .config import settings


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stderr,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="NPM MCP Server")
    parser.add_argument("--transport", choices=["stdio", "http"], default=settings.mcp_transport)
    parser.add_argument("--host", default=settings.mcp_host)
    parser.add_argument("--port", type=int, default=settings.mcp_port)
    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)
    from .server import mcp

    if args.transport == "stdio":
        logger.info("Starting MCP server in stdio mode")
        mcp.run(transport="stdio")
    else:
        logger.info(f"Starting MCP server in HTTP mode on {settings.mcp_host}:{settings.mcp_port}")
        mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
