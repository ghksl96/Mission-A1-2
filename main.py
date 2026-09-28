import requests   # ← 맨 위 import 부분에 추가!

# 카카오맵에서 맛집을 검색하는 함수
def search_restaurants(city):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": f"KakaoAK {os.getenv('KAKAO_API_KEY')}"
    }
    params = {
        "query": f"{city} 맛집",
        "size": 5
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    return data["documents"]
import argparse           # 터미널에서 날짜를 입력받기 위한 도구
import os                 # 컴퓨터의 환경(비밀 키 등)을 다루는 도구
import google.generativeai as genai   # 제미나이를 쓰기 위한 도구
import json   # JSON 글자를 진짜 데이터로 바꾸는 도구
from dotenv import load_dotenv   # .env 파일을 읽는 도구

# 1. .env 파일 속 비밀 키들을 불러온다
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")   # 제미나이 키 꺼내기
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY")     # 카카오 키 꺼내기


# 2. 터미널에서 날짜를 입력받는 함수
def get_date_from_user():
    parser = argparse.ArgumentParser(description="여행 추천 AI 프로그램")
    parser.add_argument(
        "-date",                       # 이렇게 -date 라고 입력하게 됨
        required=True,                 # 반드시 입력해야 함
        help="여행 날짜 (예: 2024-06-15)"
    )
    args = parser.parse_args()
    return args.date

# Gemini에게 여행지를 추천받는 함수
def get_travel_recommendations(travel_date):
    # 1. 제미나이에게 내 키로 로그인
    genai.configure(api_key=GEMINI_API_KEY)

    # 2. 사용할 모델 선택
    model = genai.GenerativeModel("gemini-3.8-flash")

    # 3. 제미나이에게 줄 명령(프롬프트) 작성
    prompt = f"""
    너는 여행 전문가야. {travel_date}에 여행하기 좋은 국내 여행지 3곳을 추천해줘.

    반드시 아래 JSON 형식으로만 답변해. 다른 설명은 절대 쓰지 마.

    {{
      "recommendations": [
        {{
          "city": "도시 이름",
          "reason": "추천 이유 (한 문장)"
        }}
      ]
    }}
    """

    # 4. 제미나이에게 질문 보내고 답 받기
    response = model.generate_content(prompt)

    # 5. 답변 내용을 돌려주기
    return response.text


# 제미나이 답변(글자)을 진짜 데이터로 바꾸는 함수
def parse_recommendations(raw_text):
    # 1. 앞뒤 공백 제거
    text = raw_text.strip()

    # 2. ```json 이나 ``` 껍데기가 있으면 벗겨내기
    if text.startswith("```"):
        text = text.split("```")[1]       # 백틱 사이 내용만 꺼내기
        if text.startswith("json"):
            text = text[4:]               # 맨 앞 "json" 글자 제거
        text = text.strip()

    # 3. 글자 → 진짜 데이터(딕셔너리)로 변환
    data = json.loads(text)

    # 4. 추천 목록만 꺼내서 돌려주기
    return data["recommendations"]

def save_report(report, travel_date):
    # 파일 이름: results/여행리포트_2024-06-15.txt
    filename = f"results/여행리포트_{travel_date}.txt"

    # 파일 쓰기 (utf-8: 한글/이모지 안 깨지게!)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n✅ 리포트가 저장되었습니다: {filename}")

# 3. 프로그램의 시작점
def main():
    travel_date = get_date_from_user()
    print("\n🤖 제미나이에게 여행지를 추천받는 중...\n")

    raw_result = get_travel_recommendations(travel_date)
    recommendations = parse_recommendations(raw_result)

    # ⭐️ 화면 출력 + 저장할 내용을 함께 만들기
    report = ""   # 저장할 글자를 여기에 쌓는다!

    report += "=" * 40 + "\n"
    report += f"  📅 {travel_date} 여행 추천 리포트\n"
    report += "=" * 40 + "\n"

    for i, place in enumerate(recommendations, start=1):
        city = place["city"]
        reason = place["reason"]

        report += f"\n【 {i}. {city} 】\n"
        report += f"👉 추천 이유: {reason}\n"
        report += f"\n🍜 {city} 추천 맛집:\n"

        restaurants = search_restaurants(city)
        for r in restaurants:
            report += f"   - {r['place_name']} ({r['category_name']})\n"

        report += "-" * 40 + "\n"

    # ⭐️ 다 쌓았으면 화면에 출력!
    print(report)

    # ⭐️ 그리고 파일로 저장!
    save_report(report, travel_date)


# 이 파일을 직접 실행했을 때만 main()을 작동시킴
if __name__ == "__main__":
    main()