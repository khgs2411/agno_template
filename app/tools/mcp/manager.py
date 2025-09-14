"""MCP Manager with lazy loading and caching."""

import os
from typing import Dict, List, Any, Union, Optional
from app.utils.log import logger
from agno.tools.mcp import MCPTools

from .registry import (
    get_mcp_definition,
    get_group_definitions,
    list_available_mcps,
    list_available_groups,
)


class MCPManager:
    """Manager for MCP tools with lazy loading, caching, and retry logic."""

    _cache: Dict[str, MCPTools] = {}
    _retry_config = {
        "max_attempts": 3,
        "base_delay": 1.0,
        "max_delay": 5.0,
    }

    @classmethod
    def get(cls, name: Union[str, List[str]], immediate: bool = False):
        # Clean up stale connections in development mode
        cls._cleanup_stale_connections()
        """
        Get MCP tools by name(s).

        Args:
            name: Single MCP name or list of MCP names
            immediate: If True, create connections immediately. If False (default), use lazy loading.

        Returns:
            List of MCP tools (lazy-loaded by default)
        """
        if isinstance(name, str):
            names = [name]
        else:
            names = name

        # Get configurations for all requested MCPs
        configs = []
        for mcp_name in names:
            config = get_mcp_definition(mcp_name)
            config["_name"] = mcp_name  # Add name for caching
            configs.append(config)

        if immediate:
            # Create connections immediately
            tools = []
            for config in configs:
                mcp_name = config["_name"]

                # Check cache first
                if mcp_name in cls._cache:
                    tools.append(cls._cache[mcp_name])
                    continue

                # Create new connection
                mcp_tool = cls._create_mcp_with_retry(config)
                if mcp_tool is not None:
                    cls._cache[mcp_name] = mcp_tool
                    tools.append(mcp_tool)

            return tools
        else:
            # Return lazy-loading list (default behavior)
            return _LazyMCPList(configs)

    @classmethod
    def get_group(cls, group_name: str, immediate: bool = False):
        # Clean up stale connections in development mode
        cls._cleanup_stale_connections()
        """
        Get MCP tools for a group.

        Args:
            group_name: Name of the MCP group
            immediate: If True, create connections immediately. If False (default), use lazy loading.

        Returns:
            List of MCP tools (lazy-loaded by default)
        """
        configs = get_group_definitions(group_name)

        # Add names for caching
        group_mcps = list_available_groups()
        if group_name in group_mcps:
            from .registry import MCP_GROUPS

            for i, mcp_name in enumerate(MCP_GROUPS[group_name]):
                configs[i]["_name"] = mcp_name

        if immediate:
            # Create connections immediately
            tools = []
            for config in configs:
                mcp_name = config.get("_name", "unknown")

                # Check cache first
                if mcp_name in cls._cache:
                    tools.append(cls._cache[mcp_name])
                    continue

                # Create new connection
                mcp_tool = cls._create_mcp_with_retry(config)
                if mcp_tool is not None:
                    if mcp_name != "unknown":
                        cls._cache[mcp_name] = mcp_tool
                    tools.append(mcp_tool)

            return tools
        else:
            # Return lazy-loading list (default behavior)
            return _LazyMCPList(configs)

    @classmethod
    def _create_mcp_with_retry(cls, config: Dict[str, Any]) -> Optional[MCPTools]:
        """Create MCP tools with retry logic for development mode."""
        is_dev = cls.is_development_mode()
        max_attempts = cls._retry_config["max_attempts"] if is_dev else 1
        base_delay = cls._retry_config["base_delay"]

        mcp_name = config.get("_name", "unknown")

        # Remove internal fields and description from config (MCPTools doesn't accept description)
        clean_config = {
            k: v
            for k, v in config.items()
            if not k.startswith("_") and k != "description"
        }

        for attempt in range(max_attempts):
            try:
                logger.info(
                    f"Creating MCP connection for '{mcp_name}' (attempt {attempt + 1}/{max_attempts})"
                )
                return MCPTools(**clean_config)

            except Exception as e:
                logger.warning(
                    f"MCP connection '{mcp_name}' attempt {attempt + 1} failed: {e}"
                )

                if not is_dev or attempt == max_attempts - 1:
                    # In production or final attempt
                    if not is_dev:
                        raise
                    else:
                        logger.error(
                            f"All attempts failed for MCP '{mcp_name}'. Continuing without this tool."
                        )
                        return None

                # In development, wait before retry (exponential backoff)
                delay = min(base_delay * (2**attempt), cls._retry_config["max_delay"])
                logger.info(
                    f"Retrying MCP '{mcp_name}' connection in {delay} seconds..."
                )
                import time

                time.sleep(delay)

        return None

    @classmethod
    def list_available(cls) -> List[str]:
        """List all available MCP names."""
        return list_available_mcps()

    @classmethod
    def list_groups(cls) -> List[str]:
        """List all available group names."""
        return list_available_groups()

    @classmethod
    def get_tools(cls, name: Union[str, List[str]], immediate: bool = False) -> List:
        """
        Get MCP tools as a flattened list, suitable for combining with other tools.
        This is a convenience method that ensures you get individual tools, not a nested list.
        """
        tools_list = cls.get(name, immediate=immediate)

        # If it's our LazyMCPList, return it directly (it's already a list)
        if isinstance(tools_list, _LazyMCPList):
            return tools_list

        # If it's a regular list, return it
        if isinstance(tools_list, list):
            return tools_list

        # Fallback - wrap single tool in list
        return [tools_list]

    @classmethod
    def clear_cache(cls) -> None:
        """Clear cached MCP instances. Useful for development/testing."""
        logger.info("Clearing MCP tools cache")
        cls._cache.clear()

    @classmethod
    def _cleanup_stale_connections(cls):
        """Clean up potentially stale MCP connections during development."""
        if cls.is_development_mode():
            try:
                # Clear cache to prevent reusing potentially broken connections
                stale_count = len(cls._cache)
                cls._cache.clear()
                if stale_count > 0:
                    logger.info(
                        f"Cleared {stale_count} potentially stale MCP connections during hot reload"
                    )
            except Exception as e:
                logger.warning(f"Error during MCP cleanup: {e}")

    @classmethod
    def is_development_mode(cls) -> bool:
        """Check if we're in development mode."""
        debug = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")
        env = os.getenv("ENVIRONMENT", "").lower()
        return debug or env in ("development", "dev", "local")

    @classmethod
    def is_mcp_disabled(cls) -> bool:
        """Check if MCP tools are explicitly disabled."""
        return os.getenv("DISABLE_MCP", "false").lower() in ("true", "1", "yes")


class _LazyMCPList(list):
    """Internal lazy-loading list for MCP tools."""

    def __init__(self, mcp_configs: List[Dict[str, Any]]):
        super().__init__()
        self._configs = mcp_configs
        self._loaded = False
        self._load_attempted = False

    def _ensure_loaded(self):
        """Load MCP tools if not already loaded."""
        if not self._loaded and not self._load_attempted:
            self._load_attempted = True

            # Check if MCP is explicitly disabled
            if MCPManager.is_mcp_disabled():
                logger.info("MCP tools disabled via DISABLE_MCP environment variable")
                self._loaded = True
                return

            # In development mode, add extra delay to avoid hot reload conflicts
            if MCPManager.is_development_mode():
                import time

                time.sleep(0.1)  # Small delay to let hot reload settle

            try:
                for config in self._configs:
                    mcp_tool = MCPManager._create_mcp_with_retry(config)
                    if mcp_tool is not None:
                        super().append(mcp_tool)
                self._loaded = True
            except Exception as e:
                # In development mode, gracefully handle connection failures
                if MCPManager.is_development_mode():
                    logger.error(f"Failed to load MCP tools: {e}")
                    logger.info(
                        "Agent will continue without MCP tools due to hot reload conflict"
                    )
                    logger.info(
                        "Tip: Set DISABLE_MCP=true to completely disable MCP during development"
                    )
                    self._loaded = True  # Mark as loaded to prevent retry loops
                else:
                    # In production, re-raise the exception
                    raise

    def __iter__(self):
        self._ensure_loaded()
        return super().__iter__()

    def __len__(self):
        self._ensure_loaded()
        return super().__len__()

    def __getitem__(self, index):
        self._ensure_loaded()
        return super().__getitem__(index)

    def __bool__(self):
        self._ensure_loaded()
        return len(self) > 0

    def append(self, item):
        self._ensure_loaded()
        super().append(item)

    def extend(self, items):
        self._ensure_loaded()
        super().extend(items)

    def insert(self, index, item):
        self._ensure_loaded()
        super().insert(index, item)
