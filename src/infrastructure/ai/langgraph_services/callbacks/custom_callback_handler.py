from typing import Any, Dict, List, Optional
import logging
import time

from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.outputs import LLMResult
from langgraph.types import Interrupt, Command

from pyboxen import boxen

class CustomCallbackHandler(BaseCallbackHandler):
    """
    Callback handler personalizado que monitora execução de chains,
    LLMs, ferramentas e coleta métricas detalhadas.
    """

    def __init__(
        self,
        log_file: Optional[str] = None,
        verbose: bool = True,
        log_level: str = "INFO"
    ):
        self.verbose = verbose
        self.log_file = log_file
        self.start_times = {}
        self.metrics = {
            "llm_calls": 0,
            "tool_calls": 0,
            "total_tokens": 0,
            "errors": []
        }

        self.logger = logging.getLogger(f"{__name__}.{id(self)}")
        self.logger.setLevel(getattr(logging, log_level.upper()))

        if log_file and not self.logger.handlers:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, log_level.upper()))
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s \n')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        if verbose and not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, log_level.upper()))
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s \n')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs: Any
    ) -> None:
        """Chamado quando LLM inicia"""
        run_id = kwargs.get('run_id', 'unknown')
        self.start_times[f"llm_{run_id}"] = time.time()
        self.metrics["llm_calls"] += 1

        model_name = serialized.get('name', 'Unknown')
        self.logger.info("LLM Start - Model: %s, Prompts: %d", model_name, len(prompts))

        if self.verbose and len(prompts) > 0:
            prompt_preview = prompts[0][:100] + "..." if len(prompts[0]) > 100 else prompts[0]
            self.logger.debug("First prompt preview: %s", prompt_preview)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Chamado quando LLM termina"""
        run_id = kwargs.get('run_id', 'unknown')
        start_key = f"llm_{run_id}"

        if start_key in self.start_times:
            duration = time.time() - self.start_times[start_key]
            del self.start_times[start_key]
        else:
            duration = 0

        # Contar tokens se disponível
        tokens = 0
        if response.llm_output and 'token_usage' in response.llm_output:
            tokens = response.llm_output['token_usage'].get('total_tokens', 0)
            self.metrics["total_tokens"] += tokens

        self.logger.info(
            "LLM End - Duration: %.2fs, Generations: %d",
            duration,
            len(response.generations)
        )

        if tokens > 0:
            usage = response.llm_output['token_usage']
            self.logger.info(
                "Token usage - Total: %s, "
                "Prompt: %s, "
                "Completion: %s",
                usage.get('total_tokens', 'N/A'),
                usage.get('prompt_tokens', 'N/A'),
                usage.get('completion_tokens', 'N/A')
            )

    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        """Chamado quando LLM falha"""
        self.metrics["errors"].append({
            "type": "llm_error",
            "error": str(error),
            "timestamp": time.time()
        })

        self.logger.error("LLM Error: %s", error)

    def on_chain_start(self, serialized, inputs, **kwargs):
        run_id = kwargs.get("run_id")
        parent_run_id = kwargs.get("parent_run_id")
        tags = kwargs.get("tags", [])
        metadata = kwargs.get("metadata", {})

        node_name = (
            metadata.get("langgraph_node")
            or serialized.get("name")
            or "unknown_node"
        )

        self.start_times[f"chain_{run_id}"] = time.time()

        self.logger.info(
            "Node Start | node=%s | run_id=%s | parent=%s | tags=%s",
            node_name, run_id, parent_run_id, tags
        )

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Chamado quando chain termina"""
        run_id = kwargs.get('run_id', 'unknown')
        start_key = f"chain_{run_id}"

        if start_key in self.start_times:
            duration = time.time() - self.start_times[start_key]
            del self.start_times[start_key]
        else:
            duration = 0

        self.logger.info("Chain End - Duration: %.2fs, Outputs: %s", duration, list(outputs.keys()))

    def on_chain_error(self, error: Exception, **kwargs: Any) -> None:
        """Chamado quando chain falha.

        Diferencia interrupções do LangGraph (usadas para revisão humana
        de ações sensíveis) e comandos de controle de fluxo de erros reais
        de execução da chain.
        """

        run_id = kwargs.get("run_id", "unknown")

        # Tratar Command como controle de fluxo, não erro
        if isinstance(error, Command):
            graph = getattr(error, "graph", "unknown")
            update = getattr(error, "update", {})

            self.logger.info(
                "Chain Command (flow control) - run_id=%s, graph=%s",
                run_id,
                graph,
            )

            if self.verbose:
                try:
                    self.__boxen_print(
                        (
                            f"Graph: {graph}\nUpdate keys:"
                            f" {list(update.keys()) if isinstance(update, dict) else 'N/A'}"
                        ),
                        color="cyan",
                        title="LangGraph Command",
                    )
                except Exception:
                    self.logger.debug("Falha ao formatar resumo do comando", exc_info=True)

            return

        if isinstance(error, Interrupt):
            value = getattr(error, "value", {}) or {}
            action_requests = value.get("action_requests", []) or []
            review_configs = value.get("review_configs", []) or []

            self.logger.warning(
                "Chain Interrupt (sensitive action) - run_id=%s, pending_actions=%d",
                run_id,
                len(action_requests),
            )

            try:
                if action_requests:
                    lines = [
                        "Ação sensível proposta pelo agente (requer aprovação humana)",
                        "",
                    ]
                    for idx, ar in enumerate(action_requests, 1):
                        name = ar.get("name", "unknown")
                        desc = ar.get("description", "")
                        lines.append(f"{idx}. {name}")
                        if desc:
                            lines.append(f"   {desc}")

                    if review_configs:
                        lines.append("")
                        lines.append(f"Opções de decisão: {review_configs}")

                    self.__boxen_print(
                        "\n".join(lines),
                        color="yellow",
                        title="Sensitive Action Interrupt",
                    )
            except Exception:
                self.logger.warning("Falha ao formatar resumo da interrupção", exc_info=True)

            return

        # Apenas erros reais são registrados como erros
        self.metrics["errors"].append({
            "type": "chain_error",
            "error": str(error),
            "timestamp": time.time()
        })

        self.logger.error("Chain Error: %s", error)

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        **kwargs: Any
    ) -> None:
        """Chamado quando ferramenta inicia"""
        run_id = kwargs.get('run_id', 'unknown')
        self.start_times[f"tool_{run_id}"] = time.time()
        self.metrics["tool_calls"] += 1

        tool_name = serialized.get('name', 'Unknown Tool')
        input_preview = input_str[:100] + "..." if len(input_str) > 100 else input_str
        self.logger.info("Tool Start - %s, Input: %s", tool_name, input_preview)

    def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Chamado quando ferramenta termina"""
        run_id = kwargs.get('run_id', 'unknown')
        start_key = f"tool_{run_id}"

        if start_key in self.start_times:
            duration = time.time() - self.start_times[start_key]
            del self.start_times[start_key]
        else:
            duration = 0

        output_preview = output[:100] + "..." if len(output) > 100 else output
        self.logger.info("Tool End - Duration: %.2fs, Output: %s", duration, output_preview)

    def on_tool_error(self, error: Exception, **kwargs: Any) -> None:
        """Chamado quando ferramenta falha"""
        self.metrics["errors"].append({
            "type": "tool_error",
            "error": str(error),
            "timestamp": time.time()
        })

        self.logger.error("Tool Error: %s", error)

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> None:
        """Chamado quando agente executa uma ação"""
        self.logger.info("Agent Action - Tool: %s, Input: %s", action.tool, action.tool_input)
        self.logger.debug("Agent Action Log: %s", action.log)

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Chamado quando agente termina"""
        self.logger.info("Agent Finish - Output: %s", finish.return_values)
        self.logger.debug("Agent Finish Log: %s", finish.log)

    def on_text(self, text: str, **kwargs: Any) -> None:
        """Chamado para texto intermediário"""
        if text.strip():
            self.logger.debug("Text: %s", text.strip())

    def get_metrics(self) -> Dict[str, Any]:
        """Retorna métricas coletadas"""
        return self.metrics

    def reset_metrics(self) -> None:
        """Reseta métricas"""
        self.metrics = {
            "llm_calls": 0,
            "tool_calls": 0,
            "total_tokens": 0,
            "errors": []
        }

    def print_summary(self) -> None:
        """Imprime resumo das métricas"""
        summary_lines = [
            "=" * 50,
            "RESUMO DA EXECUÇÃO",
            "=" * 50,
            f"Chamadas LLM: {self.metrics['llm_calls']}",
            f"Chamadas de Ferramenta: {self.metrics['tool_calls']}",
            f"Total de Tokens: {self.metrics['total_tokens']}",
            f"Erros: {len(self.metrics['errors'])}"
        ]

        if self.metrics['errors']:
            summary_lines.append("\nDetalhes dos Erros:")
            for i, error in enumerate(self.metrics['errors'], 1):
                summary_lines.append(f"  {i}. [{error['type']}] {error['error']}")

        summary_lines.append("=" * 50)

        summary = "\n".join(summary_lines)
        self.logger.info("Execution Summary:\n%s", summary)

    def __boxen_print(self, *args, **kwargs):
        """Imprime o resumo em uma caixa estilizada sem prefixos de log."""
        # Use saída direta para evitar timestamps/prefixos do logger que desalinhariam a caixa
        print(boxen(*args, **kwargs), flush=True)

    def on_chat_model_start(self, serialized, messages, **kwargs):
        for message in messages[0]:
            if message.type == "system":
                self.__boxen_print(
                    message.content,
                    color="blue",
                    title="System Message"
                )
            elif message.type == "human":
                self.__boxen_print(
                    message.content,
                    color="green",
                    title="Human Message"
                )
            elif message.type == "ai" and "function_call" in message.content:
                call = message.additional_kwargs.get("function_call", {})
                self.__boxen_print(
                    "Running tool %s with arguments: %s"
                    % (call.get('name', 'Unknown'), call.get('arguments', '{}')),
                    color="yellow",
                    title="AI Message"
                )
            elif message.type == "ai":
                self.__boxen_print(
                    message.content,
                    color="magenta",
                    title="AI Message"
                )
            elif message.type == "function":
                self.__boxen_print(
                    f"Function call: {message.content}",
                    color="cyan",
                    title="Function Call"
                )
            elif message.type == "tool":
                self.__boxen_print(
                    f"Tool response: {message.content}",
                    color="yellow",
                    title="Tool Message"
                )
            else:
                self.__boxen_print(
                    f"Unknown message type: {message.type}",
                    color="red",
                    title="Unknown Message"
                )
