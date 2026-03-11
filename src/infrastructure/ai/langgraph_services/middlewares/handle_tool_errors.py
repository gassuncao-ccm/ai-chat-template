from typing import Callable
from langchain.agents.middleware import AgentMiddleware
from langchain_core.messages import ToolMessage


class HandleToolErrorsMiddleware(AgentMiddleware):
    """Middleware to handle tool execution errors with custom messages."""
    def wrap_tool_call(self, request, handler: Callable):
        """Synchronous tool error handler."""
        try:
            return handler(request)
        except Exception as e:
            tool_name = None
            try:
                tool_name = request.tool_call.get("name")
            except Exception:  # pragma: no cover
                tool_name = None

            tool_label = f"'{tool_name}'" if tool_name else "a ferramenta"
            return ToolMessage(
                content=(
                    f"Erro ao executar {tool_label}. "
                    f"Revise os parâmetros e tente novamente. ({str(e)})"
                ),
                tool_call_id=request.tool_call["id"]
            )

    async def awrap_tool_call(self, request, handler: Callable):
        """Asynchronous tool error handler."""
        try:
            return await handler(request)
        except Exception as e:
            tool_name = None
            try:
                tool_name = request.tool_call.get("name")
            except Exception:  # pragma: no cover
                tool_name = None

            tool_label = f"'{tool_name}'" if tool_name else "a ferramenta"
            return ToolMessage(
                content=(
                    f"Erro ao executar {tool_label}. "
                    f"Revise os parâmetros e tente novamente. ({str(e)})"
                ),
                tool_call_id=request.tool_call["id"]
            )

handle_tool_errors = HandleToolErrorsMiddleware()
