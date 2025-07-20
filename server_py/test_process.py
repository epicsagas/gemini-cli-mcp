#!/usr/bin/env python3
"""
MCP 서버의 프로세스 동작을 테스트하는 스크립트
"""

import subprocess
import time
import psutil
import os
import signal

def get_process_info(pid):
    """프로세스 정보를 가져옵니다."""
    try:
        process = psutil.Process(pid)
        return {
            'pid': pid,
            'name': process.name(),
            'cmdline': ' '.join(process.cmdline()),
            'status': process.status(),
            'num_threads': process.num_threads(),
            'memory_info': process.memory_info()._asdict()
        }
    except psutil.NoSuchProcess:
        return None

def monitor_processes():
    """현재 실행 중인 Python 프로세스들을 모니터링합니다."""
    print("=== 현재 실행 중인 Python 프로세스들 ===")
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if 'python' in proc.info['name'].lower():
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if 'main.py' in cmdline or 'gemini-cli-mcp' in cmdline:
                    print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}")
                    print(f"Command: {cmdline}")
                    print(f"Status: {proc.status()}")
                    print(f"Threads: {proc.num_threads()}")
                    print("---")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def test_stdio_mode():
    """STDIO 모드에서의 프로세스 동작을 테스트합니다."""
    print("\n=== STDIO 모드 테스트 ===")
    
    # 시작 전 프로세스 확인
    print("시작 전 프로세스:")
    monitor_processes()
    
    # MCP 서버 시작
    print("\nMCP 서버 시작...")
    process = subprocess.Popen(
        ["python", "main.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print(f"MCP 서버 PID: {process.pid}")
    
    # 프로세스 상태 확인
    time.sleep(2)
    print("\n서버 시작 후 프로세스:")
    monitor_processes()
    
    # 프로세스 종료
    process.terminate()
    process.wait()
    
    print("\n서버 종료 후 프로세스:")
    monitor_processes()

def test_http_mode():
    """HTTP 모드에서의 프로세스 동작을 테스트합니다."""
    print("\n=== HTTP 모드 테스트 ===")
    
    # 시작 전 프로세스 확인
    print("시작 전 프로세스:")
    monitor_processes()
    
    # MCP 서버 시작 (HTTP 모드)
    print("\nMCP 서버 시작 (HTTP 모드)...")
    process = subprocess.Popen(
        ["python", "main.py", "--http"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print(f"MCP 서버 PID: {process.pid}")
    
    # 프로세스 상태 확인
    time.sleep(2)
    print("\n서버 시작 후 프로세스:")
    monitor_processes()
    
    # 프로세스 종료
    process.terminate()
    process.wait()
    
    print("\n서버 종료 후 프로세스:")
    monitor_processes()

if __name__ == "__main__":
    try:
        test_stdio_mode()
        test_http_mode()
    except KeyboardInterrupt:
        print("\n테스트 중단됨")
    except Exception as e:
        print(f"오류 발생: {e}") 