"""Spawn tool for creating background subagents."""

from typing import TYPE_CHECKING, Any

from nanobot.agent.tools.base import Tool

if TYPE_CHECKING:
    from nanobot.agent.subagent import SubagentManager


class SpawnTool(Tool):
    """Tool to spawn a subagent for background task execution."""

    def __init__(self, manager: "SubagentManager"):
        self._manager = manager
        self._origin_channel = "cli"
        self._origin_chat_id = "direct"
        self._session_key = "cli:direct"

    def set_context(self, channel: str, chat_id: str) -> None:
        """Set the origin context for subagent announcements."""
        self._origin_channel = channel
        self._origin_chat_id = chat_id
        self._session_key = f"{channel}:{chat_id}"

    @property
    def name(self) -> str:
        return "spawn"

    @property
    def description(self) -> str:
        return (
            "Spawn a new subagent or send a message to an existing one. "
            "Subagents run in the background and maintain conversation history. "
            "Use this to delegate complex tasks or converse with specialized agents."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "The task or message for the subagent",
                },
                "agent_id": {
                    "type": "string",
                    "description": "Optional ID of an existing subagent to message. Leave empty to spawn a new one.",
                },
                "agent_type": {
                    "type": "string",
                    "description": "Optional specialization (e.g., 'frontend', 'database'). Defaults to 'general'.",
                },
                "label": {
                    "type": "string",
                    "description": "Optional short label for a new subagent (for display)",
                },
            },
            "required": ["task"],
        }

    async def execute(self, task: str, agent_id: str | None = None, agent_type: str = "general", label: str | None = None, **kwargs: Any) -> str:
        """Spawn a subagent or message an existing one to execute the given task."""
        return await self._manager.spawn(
            task=task,
            agent_id=agent_id,
            agent_type=agent_type,
            label=label,
            origin_channel=self._origin_channel,
            origin_chat_id=self._origin_chat_id,
            session_key=self._session_key,
        )
