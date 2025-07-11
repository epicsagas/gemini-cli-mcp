import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

def test_get_context():
    resp = client.get("/mcp/v1/context")
    assert resp.status_code == 200
    data = resp.json()
    assert "tools" in data
    assert any(t["name"] == "gemini_ask" for t in data["tools"])
    assert any(t["name"] == "gemini_agent" for t in data["tools"])

@patch("subprocess.run")
def test_run_gemini_ask(mock_run):
    mock_run.return_value.stdout = "answer"
    mock_run.return_value.stderr = ""
    payload = {"tool_name": "gemini_ask", "params": {"question": "What is AI?"}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"] == "answer"
    assert data["stderr"] == ""

# --- Add test for DEBUG logging ---
@patch("subprocess.run")
def test_run_gemini_ask_debug_env(mock_run, monkeypatch):
    monkeypatch.setenv("DEBUG", "true")
    mock_run.return_value.stdout = "debug answer"
    mock_run.return_value.stderr = ""
    payload = {"tool_name": "gemini_ask", "params": {"question": "Debug test?"}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"] == "debug answer"
    assert data["stderr"] == ""

@patch("subprocess.run")
def test_run_gemini_agent(mock_run):
    mock_run.return_value.stdout = "agent result"
    mock_run.return_value.stderr = ""
    payload = {"tool_name": "gemini_agent", "params": {"prompt": "Do something complex."}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"] == "agent result"
    assert data["stderr"] == ""

@patch("subprocess.run")
def test_run_gemini_git_commit(mock_run):
    mock_run.return_value.stdout = "commit ok"
    mock_run.return_value.stderr = ""
    payload = {"tool_name": "gemini_git_commit", "params": {"branch_name": "feature/test"}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"] == "commit ok"
    assert data["stderr"] == ""

@patch("subprocess.run")
def test_run_gemini_git_pr(mock_run):
    mock_run.return_value.stdout = "pr ok"
    mock_run.return_value.stderr = ""
    payload = {"tool_name": "gemini_git_pr", "params": {"commit_message": "fix: test", "branch_name": "feature/test", "pr_title": "Test PR"}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"] == "pr ok"
    assert data["stderr"] == ""

@patch("subprocess.run")
def test_run_gemini_git_diff(mock_run):
    mock_run.return_value.stdout = "diff summary"
    mock_run.return_value.stderr = ""
    payload = {"tool_name": "gemini_git_diff", "params": {"diff_args": "HEAD~1"}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stdout"] == "diff summary"
    assert data["stderr"] == ""

@patch("subprocess.run")
def test_run_unknown_tool(mock_run):
    payload = {"tool_name": "unknown_tool", "params": {}}
    resp = client.post("/mcp/v1/tools", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["stderr"].startswith("Unknown tool") 