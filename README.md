# 🧳 AI 여행 추천 CLI 앱

날짜를 입력하면 **LLM(Gemini)** 이 여행지·날씨·행사 정보를 **구조화된 JSON**으로 추천하고,
그 결과를 **카카오맵 Local API**의 입력으로 연결해 도시별 맛집을 검색한 뒤,
최종 **여행 리포트(Markdown)** 로 정리해주는 커맨드라인(CLI) 프로그램입니다.

> **핵심 흐름:** `날짜 입력 → LLM 추천(JSON) → 도시명 추출 → 맛집 검색(JSON) → 최종 리포트(MD)`

---

## ✨ 주요 기능

- 📅 **CLI 날짜 입력** — `argparse`로 `-date "YYYY-MM-DD"` 필수 입력 (형식 검증 포함)
- 🤖 **LLM 추천 (JSON)** — 추천 도시·날씨·행사·이유를 **JSON 스키마**로 강제 생성
- 🍜 **맛집 검색** — 추천 도시명을 입력으로 카카오맵에서 맛집 5곳 검색
- 📝 **최종 리포트 (Markdown)** — 추천·날씨·행사·맛집·1일 일정을 담은 리포트 생성
- 💾 **결과 저장** — `results/` 폴더에 **원본 JSON + 리포트 MD** 자동 저장
- 🛡️ **에러 처리** — 인증/네트워크/파싱 오류를 분류 처리하고 `errors` 섹션에 요약

---

## 🗂️ 프로젝트 구조

```
travel-recommender/
├── main.py              # 메인 실행 파일
├── .env                 # API 키 (⚠️ 깃허브에 올리지 않음!)
├── .env.example         # 키 없이 형식만 제공하는 예시 파일
├── .gitignore           # .env, results/ 등 제외 목록
├── README.md            # 프로젝트 설명 (이 파일)
└── results/             # 실행 결과 저장 폴더
    ├── raw_2024-06-15.json     # 원본 데이터 (추천 JSON + 맛집 + errors)
    └── report_2024-06-15.md    # 최종 여행 리포트 (Markdown)
```

---

## 🚀 실행 방법

```bash
python main.py -date "2024-06-15"
```

| 옵션 | 필수 | 설명 | 예시 |
|------|:----:|------|------|
| `-date` | ✅ | 여행 날짜 (YYYY-MM-DD) | `"2024-06-15"` |

> ⚠️ 날짜 형식이 올바르지 않으면 **사용법을 출력하고 종료**합니다.

### 실행 화면 예시
```
🤖 [1/3] 제미나이에게 여행지를 추천받는 중...
✅ 추천 도시: 제주 / 날씨: 초여름, 맑음 / 행사 2건

🍜 [2/3] 카카오맵에서 '제주' 맛집을 검색하는 중...
✅ 맛집 5곳 검색 완료

📝 [3/3] 최종 리포트를 생성하는 중...

✅ 원본 데이터 저장: results/raw_2024-06-15.json
✅ 최종 리포트 저장: results/report_2024-06-15.md
🎉 완료되었습니다!
```

---

## 🔧 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/여러분의_아이디/travel-recommender.git
cd travel-recommender
```
<!-- ⭐️ 위 주소를 본인 깃허브 저장소 주소로 바꿔주세요! -->

### 2. 라이브러리 설치
```bash
pip install google-generativeai requests python-dotenv
```

---

## 🔑 API 키 설정 방법

이 프로그램은 **2개의 외부 API**를 사용합니다.

| API | 용도 | 발급처 |
|-----|------|--------|
| **Google Gemini** | 여행지 추천 (LLM) | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| **Kakao Local** | 맛집 검색 | [Kakao Developers](https://developers.kakao.com/) → 내 애플리케이션 → **REST API 키** |

> ⚠️ 카카오는 **[내 애플리케이션 → 카카오맵]** 에서 사용 설정을 **ON** 해야 검색이 됩니다.
> 401/403 오류가 나면 **키 값 / 권한 설정 / 헤더명 오타**를 점검하세요.

### 🔒 키 설정 (환경변수 / .env)

**API 키는 코드에 직접 작성하지 않습니다.** 프로젝트 폴더에 `.env` 파일을 만들어 아래처럼 저장하세요.

```
GEMINI_API_KEY=발급받은_제미나이_키
KAKAO_API_KEY=발급받은_카카오_REST_API_키
```

> 💡 저장소에는 실제 키 대신 형식만 담은 **`.env.example`** 파일을 함께 올려두면, 다른 사람이 따라 하기 쉽습니다.

---

## 🔐 API 키 유출 방지 (보안 주의사항)

> **가장 중요한 부분입니다!** API 키가 유출되면 요금 폭탄·오남용 위험이 있습니다.

- ✅ `.gitignore`에 **`.env`를 반드시 포함**하여 깃허브에 올라가지 않게 합니다.
- ✅ 키는 코드가 아닌 **환경변수/.env**에서 `os.getenv()`로 읽어옵니다.
- ✅ README·로그·결과 파일(`results/`)에 **키가 노출되지 않도록** 주의합니다.
- ✅ 실수로 키를 커밋했다면 **즉시 키를 재발급(폐기)** 하세요. (커밋 기록에 남습니다!)

**`.gitignore` 예시:**
```
.env
results/
__pycache__/
*.pyc
```

---

## 📂 결과물 확인 방법

실행이 끝나면 `results/` 폴더에 아래 **2종류 파일**이 생성됩니다.

### 1. 원본 데이터 JSON — `results/raw_YYYY-MM-DD.json`
1차 추천 결과 + 맛집 검색 결과 + 오류 요약이 함께 담깁니다.

```json
{
  "date": "2024-06-15",
  "recommendation": {
    "recommended_city": "제주",
    "weather": "초여름, 대체로 맑고 온화함",
    "events": ["제주 수국 축제", "성산일출봉 여름 행사"],
    "reason": "6월 중순 만개하는 수국을 감상하기 좋습니다. ..."
  },
  "restaurants": [
    {
      "name": "낭뜰에쉼팡",
      "address": "제주특별자치도 제주시 ...",
      "category": "음식점 > 한식",
      "url": "http://place.map.kakao.com/...",
      "x": "126.xxxx",
      "y": "33.xxxx"
    }
  ],
  "errors": []
}
```

> 📌 **맛집 필드 매핑:** 카카오 응답의 `place_name → name`, `road_address_name/address_name → address`,
> `category_name → category`, `place_url → url`, 좌표 `x`(경도/lng), `y`(위도/lat)를 저장합니다.

### 2. 최종 리포트 Markdown — `results/report_YYYY-MM-DD.md`
사람이 읽기 좋은 형태의 여행 리포트입니다. 포함 항목:
- 추천 지역 + 추천 이유 요약
- 날씨 요약
- 행사/축제 목록
- 맛집 리스트 (0건이면 **"데이터 없음"** 표기)
- **1일 일정 제안** (오전 / 오후 / 저녁)

---

## 🛠️ 에러 처리 정책

| 상황 | 처리 방식 |
|------|-----------|
| **API 키 미설정** | 즉시 종료 + 설정 방법 안내 출력 |
| **맵 API 실패** (네트워크/인증/쿼터) | 맛집 섹션을 **"데이터 없음"** 처리하고 리포트는 계속 생성 |
| **LLM JSON 파싱 실패** | "필수 키만 JSON으로 다시 출력"하도록 재시도 **1회** |
| **검색 결과 0건** | 중단 없이 "데이터 없음" 상태로 다음 단계 진행 |

> 발생한 오류는 내부 `errors` 리스트에 쌓여 **원본 JSON의 `errors` 섹션**에 요약됩니다. (오류가 없으면 빈 배열 `[]`)

---

## 🎓 학습 목표 (이 과제로 배우는 것)

이 프로젝트를 완성하면 아래를 스스로 설명할 수 있습니다.

1. **REST API의 요청/응답 구조와 GET/POST 차이**
   - `GET`: 데이터를 **조회**할 때 사용 (예: 카카오 맛집 검색 — 파라미터를 URL 쿼리로 전달)
   - `POST`: 데이터를 **생성/전송**할 때 사용 (예: LLM에 프롬프트 본문을 담아 요청)
2. **LLM 출력을 JSON으로 구조화**하여 다음 단계(장소 검색)의 입력으로 연결하는 흐름
3. **외부 API 대표 오류**(인증 401/403 · 쿼터 429 · 네트워크 · 파싱)와 대응 원칙
4. **API 키를 .env/환경변수로 관리하는 이유** (보안·재사용성·유출 방지)

---

## 🧰 사용 기술

- **Python 3** (`argparse`, `json`, `os`, `datetime`)
- **Google Gemini API** (`google-generativeai`)
- **Kakao Local API** (`requests`)
- **python-dotenv** (환경 변수 관리)

---

## 📄 라이선스

MIT License
