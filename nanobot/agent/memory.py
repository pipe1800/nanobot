"""Memory system for persistent agent memory using memU."""

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any

import httpx
from loguru import logger

if TYPE_CHECKING:
    from nanobot.config.schema import MemuConfig


class MemUClient:
    """Client for interacting with the memU-server."""

    def __init__(self, config: MemuConfig):
        self.config = config
        self.base_url = config.url.rstrip("/")
        self.headers = {}
        if config.api_key:
            self.headers["Authorization"] = f"Bearer {config.api_key}"
        self.headers["Content-Type"] = "application/json"

    async def retrieve(self, query: str) -> str:
        """Retrieve relevant memory context from memU."""
        if not self.config.enabled:
            return ""

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/retrieve",
                    headers=self.headers,
                    json={"query": query, "user_id": "Pipe", "agent_id": "Lumi"},
                    timeout=60.0,
                )
                response.raise_for_status()
                data = response.json()
                
                # Format the retrieved memory into a markdown string
                if isinstance(data, dict):
                    if "response" in data:
                        return data["response"]
                    if "results" in data and isinstance(data["results"], list):
                        return "\n".join(f"- {item}" for item in data["results"])
                    if "result" in data and isinstance(data["result"], dict):
                        items = data["result"].get("items", [])
                        if not items:
                            return ""
                        
                        formatted_items = []
                        for item in items:
                            if isinstance(item, dict) and "content" in item:
                                formatted_items.append(f"- {item['content']}")
                            else:
                                formatted_items.append(f"- {item}")
                        return "\n".join(formatted_items)
                
                return json.dumps(data, ensure_ascii=False, indent=2)
        except httpx.HTTPStatusError as e:
            logger.warning(f"Failed to retrieve memory from memU: {e} - {e.response.text}")
            return ""
        except Exception as e:
            logger.warning(f"Failed to retrieve memory from memU: {e}")
            return ""

    async def memorize(self, messages: list[dict[str, Any]]) -> None:
        """Send a conversation chunk to memU for continuous learning."""
        if not self.config.enabled or not messages:
            return

        try:
            # Format messages for memU
            # memU expects: {"conversation": [{"role": "user", "content": {"text": "..."}, "created_at": "..."}], "user_id": "..."}
            formatted_messages = []
            for msg in messages:
                # Skip tool results and system messages
                if msg.get("role") in ("tool", "system"):
                    continue
                    
                if not msg.get("content"):
                    continue
                
                content = msg["content"]
                if isinstance(content, list):
                    text_parts = [c["text"] for c in content if c.get("type") == "text"]
                    content = "\n".join(text_parts)
                
                formatted_msg = {
                    "role": msg["role"],
                    "content": {"text": content},
                }
                if "timestamp" in msg:
                    formatted_msg["created_at"] = msg["timestamp"]
                
                formatted_messages.append(formatted_msg)

            if not formatted_messages:
                return

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/memorize",
                    headers=self.headers,
                    json={"conversation": formatted_messages, "user_id": "Pipe", "agent_id": "Lumi"},
                    timeout=30.0,
                )
                response.raise_for_status()
                logger.debug(f"Successfully sent {len(formatted_messages)} messages to memU")
        except httpx.HTTPStatusError as e:
            logger.warning(f"Failed to memorize conversation in memU: {e} - {e.response.text}")
        except Exception as e:
            logger.warning(f"Failed to memorize conversation in memU: {e}")
