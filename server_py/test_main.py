import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys

# Adjust path to import from src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from main import mcp_server # Import mcp_server directly

client = TestClient(mcp_server.app)

def test_get_context():
    resp = client.get("/mcp/v1/context")
    assert resp.status_code == 200
    data = resp.json()
    assert "tools" in data
    assert any(t["name"] == "gemini_ask" for t in data["tools"])
    assert any(t["name"] == "gemini_yolo" for t in data["tools"])

@patch('src.gemini_client.subprocess.run')
def test_run_gemini_ask(mock_run):
    mock_run.return_value.stdout = "answer"
    mock_run.return_value.stderr = ""
    mock_run.return_value.returncode = 0
    payload = {"tool_name": "gemini_ask", "params": {"question": "What is AI?"}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"] == "answer"
    assert data["stderr"] == ""

@patch('src.gemini_client.subprocess.run')
def test_run_gemini_ask_debug_env(mock_run, monkeypatch):
    monkeypatch.setenv("DEBUG", "true")
    mock_run.return_value.stdout = "debug answer"
    mock_run.return_value.stderr = ""
    mock_run.return_value.returncode = 0
    payload = {"tool_name": "gemini_ask", "params": {"question": "Debug test?"}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"] == "debug answer"
    assert data["stderr"] == ""
    monkeypatch.setenv("DEBUG", "false") # Reset for other tests

@patch('src.gemini_client.subprocess.run')
def test_run_gemini_yolo(mock_run):
    mock_run.return_value.stdout = "agent result"
    mock_run.return_value.stderr = ""
    mock_run.return_value.returncode = 0
    payload = {"tool_name": "gemini_yolo", "params": {"prompt": "Do something complex."}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"] == "agent result"
    assert data["stderr"] == ""

@patch('src.gemini_client.subprocess.run')
def test_run_gemini_git_commit(mock_run):
    mock_run.return_value.stdout = "commit ok"
    mock_run.return_value.stderr = ""
    mock_run.return_value.returncode = 0
    payload = {"tool_name": "gemini_git_commit", "params": {"branch_name": "feature/test"}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"] == "commit ok"
    assert data["stderr"] == ""

@patch('src.gemini_client.subprocess.run')
def test_run_gemini_git_pr(mock_run):
    mock_run.return_value.stdout = "pr ok"
    mock_run.return_value.stderr = ""
    mock_run.return_value.returncode = 0
    payload = {"tool_name": "gemini_git_pr", "params": {"commit_message": "fix: test", "branch_name": "feature/test", "pr_title": "Test PR"}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"] == "pr ok"
    assert data["stderr"] == ""

@patch('src.gemini_client.subprocess.run')
def test_run_gemini_git_diff(mock_run):
    mock_run.return_value.stdout = "diff summary"
    mock_run.return_value.stderr = ""
    mock_run.return_value.returncode = 0
    payload = {"tool_name": "gemini_git_diff", "params": {"diff_args": "HEAD~1"}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"] == "diff summary"
    assert data["stderr"] == ""

@patch('src.gemini_client.subprocess.run')
def test_run_unknown_tool(mock_run):
    payload = {"tool_name": "unknown_tool", "params": {}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stderr"].startswith("Unknown tool")
