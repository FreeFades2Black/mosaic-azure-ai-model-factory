"""
==============================================================================
MOSAIC AZURE FOUNDRY IQ & WEB KNOWLEDGE MCP SERVER
==============================================================================
Enterprise Model Context Protocol (MCP) server implementation (JSON-RPC 2.0)
exposing Azure AI Foundry IQ Knowledge Bases and authoritative Web Grounding.
==============================================================================
"""

import json
import logging
import sys
from typing import Any, Dict, List, Optional

from ..tools.foundry_iq_mcp_tool import FoundryIQMCPTool

logger = logging.getLogger(__name__)


class FoundryIQMCPServer:
    """
    Standard MCP (Model Context Protocol) Server exposing Foundry IQ Knowledge Base
    and Web Search grounding capabilities to MCP-compatible AI agent hosts.
    """

    PROTOCOL_VERSION = "2024-11-05"
    SERVER_NAME = "mosaic-foundry-iq-mcp-server"
    SERVER_VERSION = "1.0.0"

    def __init__(self, backend_tool: Optional[FoundryIQMCPTool] = None):
        self.backend = backend_tool or FoundryIQMCPTool()

    def handle_request(self, request_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Processes a single JSON-RPC 2.0 MCP request and returns the response."""
        req_id = request_payload.get("id")
        method = request_payload.get("method")
        params = request_payload.get("params", {})

        if not method:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32600, "message": "Invalid Request: Missing 'method' field."},
            }

        try:
            if method == "initialize":
                return self._handle_initialize(req_id, params)
            elif method == "notifications/initialized":
                return {"jsonrpc": "2.0", "id": req_id, "result": {}}
            elif method == "tools/list":
                return self._handle_tools_list(req_id)
            elif method == "tools/call":
                return self._handle_tools_call(req_id, params)
            elif method == "resources/list":
                return self._handle_resources_list(req_id)
            elif method == "resources/read":
                return self._handle_resources_read(req_id, params)
            elif method == "ping":
                return {"jsonrpc": "2.0", "id": req_id, "result": {}}
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Method not found: '{method}'"},
                }
        except Exception as exc:
            logger.exception("Error executing MCP method %s: %s", method, exc)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": f"Internal server error: {str(exc)}"},
            }

    def _handle_initialize(self, req_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handles MCP 'initialize' handshake."""
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": self.PROTOCOL_VERSION,
                "capabilities": {
                    "tools": {"listChanged": False},
                    "resources": {"subscribe": False, "listChanged": False},
                    "prompts": {"listChanged": False},
                },
                "serverInfo": {
                    "name": self.SERVER_NAME,
                    "version": self.SERVER_VERSION,
                },
                "instructions": (
                    "This MCP server provides enterprise knowledge grounding via Azure AI Foundry IQ "
                    "and live authoritative web literature search (NIH, PubMed, CDC, FDA) for clinical agents."
                ),
            },
        }

    def _handle_tools_list(self, req_id: Any) -> Dict[str, Any]:
        """Returns the list of available MCP tools."""
        tools = self.backend.list_mcp_tools()
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": t.name,
                        "description": t.description,
                        "inputSchema": t.input_schema,
                    }
                    for t in tools
                ]
            },
        }

    def _handle_tools_call(self, req_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Executes tool calls conforming to MCP content specification."""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})

        if not tool_name:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32602, "message": "Invalid params: 'name' is required for tools/call."},
            }

        res = self.backend.execute_mcp_tool_call(tool_name, arguments)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(res, indent=2),
                    }
                ],
                "isError": res.get("status") == "error",
            },
        }

    def _handle_resources_list(self, req_id: Any) -> Dict[str, Any]:
        """Returns available resources (Foundry IQ knowledge docs)."""
        resources = [
            {
                "uri": doc["uri"],
                "name": doc["title"],
                "description": f"Domain: {doc['domain']} | Tags: {', '.join(doc['tags'])}",
                "mimeType": "application/pdf",
            }
            for doc in self.backend.ENTERPRISE_KNOWLEDGE_STORE
        ]
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"resources": resources},
        }

    def _handle_resources_read(self, req_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """Reads specific resource content."""
        uri = params.get("uri")
        for doc in self.backend.ENTERPRISE_KNOWLEDGE_STORE:
            if doc["uri"] == uri:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "contents": [
                            {
                                "uri": doc["uri"],
                                "mimeType": "text/plain",
                                "text": doc["content"],
                            }
                        ]
                    },
                }
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32002, "message": f"Resource not found: '{uri}'"},
        }

    def run_stdio(self) -> None:
        """Runs the MCP server over standard input/output (stdio JSON-RPC loop)."""
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                req = json.loads(line)
                resp = self.handle_request(req)
                sys.stdout.write(json.dumps(resp) + "\n")
                sys.stdout.flush()
            except Exception as e:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {"code": -32700, "message": f"Parse error: {str(e)}"},
                }
                sys.stdout.write(json.dumps(err_resp) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    server = FoundryIQMCPServer()
    server.run_stdio()
