"""Web UI channel implementation using aiohttp."""

import asyncio
import json
import os
from typing import Any

from aiohttp import web
from loguru import logger

from nanobot.bus.events import OutboundMessage
from nanobot.bus.queue import MessageBus
from nanobot.channels.base import BaseChannel
from nanobot.config.schema import Base
from pydantic import Field
from nanobot.session.manager import SessionManager
from nanobot.config.paths import get_workspace_path

class WebConfig(Base):
    enabled: bool = False
    port: int = 8080
    host: str = "127.0.0.1"
    allow_from: list[str] = Field(default_factory=lambda: ["*"])

class WebChannel(BaseChannel):
    name = "web"
    display_name = "Web UI"

    @classmethod
    def default_config(cls) -> dict[str, Any]:
        return WebConfig().model_dump(by_alias=True)

    def __init__(self, config: Any, bus: MessageBus):
        if isinstance(config, dict):
            config = WebConfig.model_validate(config)
        super().__init__(config, bus)
        self.config: WebConfig = config
        self._app = web.Application()
        self._app.router.add_get("/", self.handle_index)
        self._app.router.add_get("/ws", self.handle_websocket)
        self._runner = None
        self._site = None
        self._websockets = set()
        self.session_manager = SessionManager(get_workspace_path())

    async def handle_index(self, request: web.Request) -> web.Response:
        html_path = os.path.join(os.path.dirname(__file__), "web_ui.html")
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        return web.Response(text=html, content_type='text/html')

    async def handle_websocket(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self._websockets.add(ws)
        
        try:
            self.session_manager.invalidate("web:web_chat")
            session = self.session_manager.get_or_create("web:web_chat")
            history = session.messages
            for msg in history:
                role = msg.get("role")
                content = msg.get("content")
                
                if role == "assistant" and not content:
                    tool_calls = msg.get("tool_calls", [])
                    for tc in tool_calls:
                        if isinstance(tc, dict) and tc.get("type") == "function":
                            func = tc.get("function", {})
                            if func.get("name") == "message":
                                try:
                                    args = json.loads(func.get("arguments", "{}"))
                                    content = args.get("content")
                                except Exception:
                                    pass

                if role in ("user", "assistant") and content:
                    await ws.send_json({
                        "type": "history",
                        "role": role,
                        "content": content
                    })
        except Exception as e:
            logger.error(f"Failed to load history: {e}")
        
        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    data = json.loads(msg.data)
                    if data.get("type") == "message":
                        content = data.get("content", "")
                        await self._handle_message(
                            sender_id="web_user",
                            chat_id="web_chat",
                            content=content
                        )
        finally:
            self._websockets.remove(ws)
            
        return ws

    async def start(self) -> None:
        self._running = True
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        self._site = web.TCPSite(self._runner, self.config.host, self.config.port)
        await self._site.start()
        logger.info(f"Web UI started at http://{self.config.host}:{self.config.port}")
        
        while self._running:
            await asyncio.sleep(1)

    async def stop(self) -> None:
        self._running = False
        for ws in set(self._websockets):
            await ws.close()
        if self._runner:
            await self._runner.cleanup()

    async def send(self, msg: OutboundMessage) -> None:
        if not self._websockets:
            return
            
        # Only send messages meant for the web channel
        if msg.channel != self.name:
            return
            
        is_progress = msg.metadata.get("_progress", False)
        payload = {
            "type": "progress" if is_progress else "message",
            "content": msg.content
        }
        
        for ws in self._websockets:
            try:
                await ws.send_json(payload)
            except Exception as e:
                logger.error(f"Failed to send to websocket: {e}")
