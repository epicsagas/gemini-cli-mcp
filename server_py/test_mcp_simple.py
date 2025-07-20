#!/usr/bin/env python3
"""
간단한 MCP 서버 프로세스 테스트
"""

import subprocess
import time
import os
import signal

def test_mcp_server():
    """MCP 서버의 프로세스 동작을 테스트합니다."""
    print("=== MCP 서버 프로세스 테스트 ===")
    
    # 현재 프로세스 ID 출력
    print(f"현재 프로세스 ID: {os.getpid()}")
    
    # MCP 서버 시작
    print("\nMCP 서버 시작...")
    process = subprocess.Popen(
        ["python", "main.py", "--verbose"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print(f"MCP 서버 PID: {process.pid}")
    print(f"부모 프로세스 ID: {os.getpid()}")
    
    # 프로세스가 살아있는지 확인
    time.sleep(1)
    if process.poll() is None:
        print("✅ MCP 서버가 실행 중입니다 (단일 프로세스)")
        print(f"프로세스 상태: {process.poll()}")
        
        # 프로세스 정보 출력
        try:
            import psutil
            proc = psutil.Process(process.pid)
            print(f"프로세스 이름: {proc.name()}")
            print(f"프로세스 상태: {proc.status()}")
            print(f"스레드 수: {proc.num_threads()}")
            print(f"메모리 사용량: {proc.memory_info().rss / 1024 / 1024:.2f} MB")
        except Exception as e:
            print(f"프로세스 정보 조회 실패: {e}")
    else:
        print("❌ MCP 서버가 종료되었습니다")
        stdout, stderr = process.communicate()
        print(f"stdout: {stdout}")
        print(f"stderr: {stderr}")
    
    # 프로세스 종료
    print("\nMCP 서버 종료...")
    process.terminate()
    process.wait()
    print("✅ MCP 서버가 종료되었습니다")

def test_multiple_instances():
    """여러 MCP 서버 인스턴스 테스트"""
    print("\n=== 다중 인스턴스 테스트 ===")
    
    processes = []
    
    # 3개의 MCP 서버 인스턴스 시작
    for i in range(3):
        print(f"\nMCP 서버 {i+1} 시작...")
        process = subprocess.Popen(
            ["python", "main.py", "--verbose"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        processes.append(process)
        print(f"MCP 서버 {i+1} PID: {process.pid}")
    
    # 모든 프로세스가 살아있는지 확인
    time.sleep(1)
    alive_count = 0
    for i, process in enumerate(processes):
        if process.poll() is None:
            print(f"✅ MCP 서버 {i+1} 실행 중 (PID: {process.pid})")
            alive_count += 1
        else:
            print(f"❌ MCP 서버 {i+1} 종료됨 (PID: {process.pid})")
    
    print(f"\n총 {alive_count}개의 MCP 서버가 실행 중입니다")
    
    # 모든 프로세스 종료
    print("\n모든 MCP 서버 종료...")
    for process in processes:
        process.terminate()
        process.wait()
    
    print("✅ 모든 MCP 서버가 종료되었습니다")

if __name__ == "__main__":
    try:
        test_mcp_server()
        test_multiple_instances()
    except KeyboardInterrupt:
        print("\n테스트 중단됨")
    except Exception as e:
        print(f"오류 발생: {e}") 