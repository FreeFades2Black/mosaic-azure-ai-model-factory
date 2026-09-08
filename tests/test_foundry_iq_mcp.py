"""
==============================================================================
FOUNDRY IQ MCP & WEB KNOWLEDGE SOURCE TEST SUITE
==============================================================================
Validates Model Context Protocol (MCP) JSON-RPC 2.0 compliance,
Foundry IQ agentic retrieval, Web MCP grounding, and Agent orchestration.
==============================================================================
"""

import json
import pytest

from src.tools.foundry_iq_mcp_tool import FoundryIQMCPTool, CitationRecord, KnowledgeSourceResult
from src.mcp_servers.foundry_iq_mcp_server import FoundryIQMCPServer
from src.agents.clinical_analyst_agent import ClinicalAnalystAgent


@pytest.fixture
def mcp_tool():
    return FoundryIQMCPTool()


@pytest.fixture
def mcp_server(mcp_tool):
    return FoundryIQMCPServer(backend_tool=mcp_tool)


@pytest.fixture
def clinical_agent():
    return ClinicalAnalystAgent()


def test_mcp_tool_definitions(mcp_tool):
    """Verifies that MCP tool specifications conform to schema requirements."""
    tools = mcp_tool.list_mcp_tools()
    assert len(tools) >= 3
    tool_names = [t.name for t in tools]
    assert "foundry_iq_retrieve" in tool_names
    assert "web_knowledge_search" in tool_names
    assert "get_document_citation" in tool_names

    for t in tools:
        assert t.description is not None
        assert "type" in t.input_schema
        assert t.input_schema["type"] == "object"


def test_jsonrpc_payload_formatting(mcp_tool):
    """Verifies JSON-RPC 2.0 request payload construction."""
    payload_str = mcp_tool.format_jsonrpc_request("tools/call", {"name": "foundry_iq_retrieve", "arguments": {"query": "egfr"}})
    payload = json.loads(payload_str)

    assert payload["jsonrpc"] == "2.0"
    assert payload["method"] == "tools/call"
    assert "mcp-req-" in payload["id"]
    assert payload["params"]["name"] == "foundry_iq_retrieve"


def test_agentic_subquery_planning(mcp_tool):
    """Verifies decomposition of compound clinical queries into targeted subqueries."""
    compound_query = "Calculate eGFR for 62yo female and review KDIGO cisplatin dosing protocol"
    subqueries = mcp_tool.plan_subqueries(compound_query)

    assert len(subqueries) >= 2
    assert any("egfr" in sq.lower() for sq in subqueries)
    assert any("kdigo" in sq.lower() or "cisplatin" in sq.lower() for sq in subqueries)


def test_foundry_iq_retrieval(mcp_tool):
    """Verifies retrieval from enterprise Foundry IQ knowledge base."""
    result = mcp_tool.retrieve_foundry_iq("nephrology egfr renal dosing guidelines")

    assert result.status == "success"
    assert len(result.citations) > 0
    assert result.knowledge_base == "mosaic-clinical-iq-kb"
    assert "Cockcroft-Gault" in result.summary or "renal" in result.summary.lower()

    citation = result.citations[0]
    assert citation.source_title is not None
    assert citation.source_uri.startswith("https://")
    assert citation.relevance_score >= 0.50


def test_web_mcp_knowledge_search(mcp_tool):
    """Verifies real-time web search grounding across approved medical domains."""
    result = mcp_tool.search_web_mcp("CDC opioid MME threshold and prescribing guidelines")

    assert result.status == "success"
    assert len(result.citations) > 0
    assert any(c.domain in ["cdc.gov", "nih.gov", "pubmed.ncbi.nlm.nih.gov"] for c in result.citations)
    assert "MME" in result.summary or "opioid" in result.summary.lower()


def test_mcp_server_initialize(mcp_server):
    """Verifies MCP server 'initialize' handshake method."""
    init_request = {
        "jsonrpc": "2.0",
        "id": "req-init-1",
        "method": "initialize",
        "params": {"protocolVersion": "2024-11-05"},
    }
    response = mcp_server.handle_request(init_request)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "req-init-1"
    assert "result" in response
    assert response["result"]["protocolVersion"] == "2024-11-05"
    assert response["result"]["serverInfo"]["name"] == "mosaic-foundry-iq-mcp-server"


def test_mcp_server_tools_call(mcp_server):
    """Verifies tool invocation over MCP server JSON-RPC interface."""
    call_request = {
        "jsonrpc": "2.0",
        "id": "req-call-1",
        "method": "tools/call",
        "params": {
            "name": "foundry_iq_retrieve",
            "arguments": {"query": "oncology chemotherapy BSA dosing", "max_results": 2},
        },
    }
    response = mcp_server.handle_request(call_request)

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == "req-call-1"
    assert "result" in response
    assert response["result"]["isError"] is False
    assert len(response["result"]["content"]) > 0

    content_text = response["result"]["content"][0]["text"]
    parsed_content = json.loads(content_text)
    assert parsed_content["status"] == "success"
    assert len(parsed_content["citations"]) > 0


def test_mcp_server_resources_list_and_read(mcp_server):
    """Verifies resource discovery and reading via MCP protocol."""
    # List resources
    list_req = {"jsonrpc": "2.0", "id": "req-res-1", "method": "resources/list", "params": {}}
    list_resp = mcp_server.handle_request(list_req)
    assert "resources" in list_resp["result"]
    assert len(list_resp["result"]["resources"]) >= 3

    target_uri = list_resp["result"]["resources"][0]["uri"]

    # Read specific resource
    read_req = {
        "jsonrpc": "2.0",
        "id": "req-res-2",
        "method": "resources/read",
        "params": {"uri": target_uri},
    }
    read_resp = mcp_server.handle_request(read_req)
    assert "contents" in read_resp["result"]
    assert len(read_resp["result"]["contents"]) > 0
    assert len(read_resp["result"]["contents"][0]["text"]) > 0


def test_agent_hybrid_foundry_iq_and_code_interpreter(clinical_agent):
    """
    Verifies end-to-end multi-tool agent execution:
    1. Retrieves clinical guidelines from Foundry IQ
    2. Synthesizes & executes exact math in Code Interpreter
    3. Redacts PHI and verifies groundedness
    """
    query = (
        "Retrieve renal dosing protocol and calculate eGFR for a 62-year-old female "
        "weighing 68 kg with serum creatinine 1.4 mg/dL."
    )
    result = clinical_agent.run(query)

    assert result.safety_passed is True
    assert "code_interpreter" in result.tool_used
    assert "foundry_iq_mcp" in result.tool_used
    assert result.code_result is not None
    assert result.code_result.status == "success"
    assert abs(result.code_result.return_value - 44.73) < 0.05
    assert len(result.citations) > 0

    assert result.groundedness_score >= 4.0


def test_agent_web_mcp_grounding(clinical_agent):
    """Verifies agent invocation of Web MCP Knowledge Source for authoritative web queries."""
    query = "Search latest NIH PubMed studies regarding vancomycin renal elimination cutoffs."
    result = clinical_agent.run(query, use_web_sources=True)

    assert result.safety_passed is True
    assert "web_mcp" in result.tool_used
    assert len(result.citations) > 0
    assert any("pubmed" in c.lower() or "nih" in c.lower() for c in result.citations)
