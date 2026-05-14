import os
import requests
import json
from dotenv import load_dotenv

# 환경 변수 로드 (API 키 관리를 위해)
load_dotenv()

# --- 설정 ---
CONTENT_API_KEY = os.getenv("CONTENT_API_KEY", "a0485238fcd41d9a4") # 제공된 키 사용
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "admin_api_key_placeholder") # 실제 키로 대체 필요
GHOST_URL = "YOUR_GHOST_SUBDOMAIN" # 실제 Ghost URL로 대체 필요

def generate_content(topic: str) -> dict:
    """
    Content API를 호출하여 주어진 주제로 블로그 콘텐츠를 생성합니다.
    """
    print(f"콘텐츠 생성 요청: 주제='{topic}'")
    headers = {
        "Authorization": f"Bearer {CONTENT_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "topic": topic,
        "style": "blog"
    }
    try:
        response = requests.post("https://api.content.example.com/generate", headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"콘텐츠 생성 중 오류 발생: {e}")
        return None

def publish_to_ghost(content_data: dict, title: str) -> bool:
    """
    생성된 콘텐츠를 Ghost에 발행합니다. (Admin API 활용 가정)
    """
    print(f"Ghost 발행 요청: 제목='{title}'")
    headers = {
        "Authorization": f"Bearer {ADMIN_API_KEY}",
        "Content-Type": "application/json"
    }
    # Ghost API에 맞는 데이터 포맷으로 변환 필요 (가정)
    payload = {
        "title": title,
        "content": content_data.get("generated_text", "No content found")
    }
    try:
        response = requests.post(f"{GHOST_URL}/publish", headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        print("Ghost 발행 성공.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Ghost 발행 중 오류 발생: {e}")
        return False

def run_pipeline(topic: str):
    """
    콘텐츠 생성부터 Ghost 발행까지의 전체 파이프라인을 실행합니다.
    """
    print("--- 블로그 자동화 파이프라인 시작 ---")
    
    # 1. 콘텐츠 생성
    content_result = generate_content(topic)
    
    if not content_result:
        print("🛑 콘텐츠 생성 실패. 파이프라인 중단.")
        return

    print("✅ 콘텐츠 생성 완료. 다음 단계: Ghost 발행")
    
    # 2. Ghost 발행
    title = f"자동 생성 블로그 포스팅: {topic}"
    success = publish_to_ghost(content_result, title)
    
    if success:
        print("✨ 전체 파이프라인 성공적으로 완료되었습니다.")
    else:
        print("❌ Ghost 발행 실패. 로그 확인 필요.")

if __name__ == "__main__":
    # 실행 예시
    target_topic = input("자동화할 블로그 주제를 입력하세요 (예: AI의 미래): ")
    if target_topic:
        run_pipeline(target_topic)
    else:
        print("주제가 입력되지 않아 파이프라인을 실행하지 않습니다.")