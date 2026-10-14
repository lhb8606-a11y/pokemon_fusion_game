# 포켓몬스터 퓨~~~전 얍!

1세대(No.1~151) 포켓몬 **2마리를 퓨전한 이미지**를 보고, 20초 안에 **두 마리 이름을 맞추는 파티용 게임**입니다.
Streamlit 앱 하나(`app.py`) + `manifest.json` + `images/` 폴더만 있으면 어디서든 돌아갑니다.

```
포켓몬스터 퓨~~~전 얍!
 ├ 1) 타이틀    : "아무 키나 누르세요"  (키보드 · 클릭 · 터치)
 ├ 2) 사용법    : 왼쪽(얼굴·색) + 오른쪽(몸통) → 하얀 빛 → 합성 포켓몬  예시 애니메이션
 └ 3) 게임      : 합성 포켓몬 + 20초 카운트 → 클릭하면 [합성2] 공개 → 클릭하면 [합성1] 공개 → 다음 문제
```

- 점수 없음, 자동 진행 없음. **버튼(또는 아무 키 / 화면 클릭)으로만** 넘어갑니다.
- 순서는 매번 랜덤이며, 준비된 문제를 **전부 보여준 뒤 자동으로 다시 섞어서** 처음부터 반복합니다.
- 새로고침하면 그냥 처음(타이틀)부터 다시 시작합니다.

---

## 1. 빠른 실행 (내 컴퓨터)

```bash
pip install -r requirements.txt
streamlit run app.py
```

브라우저가 자동으로 열립니다(기본 주소 `http://localhost:8501`).
폰/태블릿에서 보려면 같은 와이파이에서 `http://<PC의 IP>:8501` 로 접속하세요.

> OCR(이름 자동 인식)을 쓰려면 `tesseract` 실행 파일이 필요합니다.
> - Windows: https://github.com/UB-Mannheim/tesseract/wiki 설치
> - macOS: `brew install tesseract`
> - Ubuntu: `sudo apt install tesseract-ocr`
> Streamlit Cloud 에 배포할 때는 이 저장소의 `packages.txt` 가 자동 처리합니다.

---

## 2. 캡처 이미지 준비 (제일 중요)

### 2-1. 이미지를 어디에 올릴까? → **GitHub 저장소의 `captures/` 폴더를 추천**

| 방법 | 추천도 | 이유 |
|---|---|---|
| **GitHub 저장소 안 `captures/` 폴더** | ★★★ | 추가 설정 0, 무료, Streamlit Cloud 배포와 같은 저장소라 그대로 동작. `images/` + `manifest.json` 만 커밋되면 캡처 원본은 지워도 됩니다. |
| 구글 클라우드 스토리지(GCS) 버킷 | ★ | 버킷을 public + CORS 허용으로 설정해야 이미지가 화면에 뜹니다(안 하면 깨진 이미지). 과금/권한 설정도 필요합니다. |
| 구글 드라이브 공유 링크 | △ | `drive.google.com/file/d/<ID>/view` 형태의 링크는 이미지 태그로 못 씁니다. `https://lh3.googleusercontent.com/d/<ID>` 로 바꿔야 하고, 트래픽이 몰리면 차단될 수 있습니다. |

즉 **구글 클라우드 안 써도 됩니다.** 캡처 수십~수백 장(장당 100~500KB)이면 저장소 용량도 충분합니다.

> GCS/Drive 를 굳이 쓰고 싶다면: `manifest.json` 의 `fused`/`left`/`right` 값에
> `https://...` 절대 URL 을 넣어도 게임이 그대로 읽습니다(로컬 파일 경로 대신 URL 허용).

### 2-2. 넣고 → 변환 스크립트 실행

1. 캡처 파일들을 `captures/` 안에 넣습니다. (이름 아무거나, png/jpg/jpeg/webp/bmp)
2. 저장소 루트에서 실행:

```bash
python tools/build_manifest.py --src captures
```

이 스크립트가 캡처 한 장에서 **자동으로**
- 위쪽 = **합성(퓨전) 포켓몬**
- 아래 왼쪽 = **합성 1 (얼굴·색)**
- 아래 오른쪽 = **합성 2 (몸통)**

세 영역을 찾아 잘라내고(`images/001_fused.png` …), 캡처에 찍혀 있는 **영어 이름을 OCR 로 읽어 한글로 변환**한 뒤(1~151 이름표 `data/pokemon_names.json` 사용) `manifest.json` 을 만듭니다.

- 캡처 위/아래의 쓸데없는 부분(폰 상태바, 브라우저 주소창, 광고)은 **신경 쓰지 않아도 됩니다.** 알아서 잘라냅니다.
- 결과 확인: `images/` 폴더와 `manifest.json`. 확인용으로 `--debug` 를 주면 `crops_debug/` 에 잘라낸 위치가 표시된 그림이 저장됩니다.

```bash
python tools/build_manifest.py --src captures --debug     # 잘라낸 위치 확인
python tools/build_manifest.py --src captures --limit 5   # 앞 5장만 테스트
```

### 2-3. 이름을 못 읽었을 때 (OCR 실패 구제)

`python tools/build_manifest.py` 마지막에 `[확인 필요]` 목록과 `needs_review.txt` 가 나옵니다.
그 파일들의 이름만 직접 적어주면 됩니다. `manual_names.csv` 예시:

```csv
file,left,right
KakaoTalk_20261014_101.png,Vileplume,Chansey
Screenshot_2026-10-14-11.png,Pikachu,Gyarados
```

```bash
python tools/build_manifest.py --src captures --names-csv manual_names.csv
```

(이름은 영어 원문 또는 한글 둘 다 인식합니다. `left` = 아래 왼쪽 = 얼굴·색, `right` = 아래 오른쪽 = 몸통)

### 2-4. 중복 제거

같은 조합(`합성1`, `합성2` 이름이 완전히 동일)은 자동으로 한 번만 들어갑니다.

- 기본값 `--dedupe ordered` : (라플레시아,럭키) 와 (럭키,라플레시아) 는 **다른 그림**이므로 둘 다 유지
- 완전히 같은 두 마리 조합이면 순서 상관없이 하나만 남기려면: `--dedupe unordered`
- 전혀 걸러내지 않으려면: `--dedupe none`

### 2-5. 이름표(1~151) 다시 만들기 (보통 불필요)

`data/pokemon_names.json` 은 이미 1~151 전부 들어 있습니다(영어/한글/도감번호).
새로 받고 싶을 때만: `python tools/build_names.py`

---

## 3. GitHub 업로드 + Streamlit Cloud 배포

```bash
git init
git add .
git commit -m "포켓몬스터 퓨~~~전 얍!"
git branch -M main
git remote add origin https://github.com/<아이디>/<저장소>.git
git push -u origin main
```

1. https://share.streamlit.io 접속 → GitHub 로그인
2. **New app** → 저장소 / 브랜치(`main`) / 메인 파일 경로 `app.py` 선택
3. **Deploy** (최초 1~2분, `packages.txt` 로 tesseract 까지 자동 설치)
4. 발급된 `https://<앱이름>.streamlit.app` 주소를 폰·태블릿에서 열면 게임 시작

> 저장소에 `captures/` 원본까지 올리면 용량이 커집니다. 로컬에서 `build_manifest.py` 를 돌린 뒤
> **`images/` + `manifest.json` 만** 올려도 게임은 정상 동작합니다.

---

## 4. 배경음악(BGM)

- 포함된 `assets/bgm.mp3` 는 **저작권 문제가 없는 오리지널 8비트 스타일 루프**입니다(직접 합성, `tools/make_bgm.py`).
- 왼쪽 아래 `♪ BGM 켜기` 버튼을 누르면 재생되고, 화면이 넘어가도 **계속 이어집니다**(끄기도 같은 버튼).
- 원하는 음원이 있으면 `assets/bgm.mp3` 를 **같은 이름으로 교체**하면 그대로 사용됩니다.
  (저작권이 있는 음원 사용은 본인 책임입니다. 파일이 없으면 BGM 없이 조용히 동작합니다.)

---

## 5. 자주 바꾸고 싶은 값

| 바꾸고 싶은 것 | 위치 |
|---|---|
| 제한시간 20초 | `app.py` 의 `COUNTDOWN = 20` |
| 버튼 문구 / 안내문 | `app.py` 의 `screen_play()` 안 `label`, `tip` |
| 색/폰트 | `app.py` 의 `CSS` (상단) |
| 잘라내기 여백 | `tools/build_manifest.py --pad 0.07` (크게 = 여백 많이) |
| 폰트 | `CSS` 의 `@font-face` (Galmuri 픽셀폰트, 로드 실패 시 시스템 고딕으로 자동 대체) |

---

## 6. 파일 구조

```
app.py                     게임 본체 (Streamlit)
manifest.json              게임 문제 목록 (build_manifest.py 가 생성)
images/                    잘라낸 합성/왼쪽/오른쪽 이미지
data/pokemon_names.json    1~151 영어/한글 이름표
tools/build_manifest.py    캡처 → 잘라내기 + OCR + 중복제거 → manifest.json
tools/build_names.py       1~151 이름표 생성(포켓API)
tools/make_bgm.py          오리지널 칩튠 BGM 생성
tools/preview_static.py    (개발용) 화면 디자인 정적 미리보기 생성
tests/test_app.py          게임 흐름 자동 테스트
assets/                    예시 이미지 + bgm.mp3
captures/                  ★ 캡처 원본을 넣는 폴더
requirements.txt           파이썬 패키지 (Streamlit Cloud 자동 설치)
packages.txt               시스템 패키지(tesseract) (Streamlit Cloud 자동 설치)
.streamlit/config.toml     테마/서버 설정
```

---

## 7. 참고

- 게임 화면은 폰(세로) / 태블릿 / PC 모두에 맞춰 자동으로 크기가 조절됩니다.
- 키보드 인식(아무 키)은 같은 도메인 iframe 안에서 동작합니다. 특정 브라우저/보안 설정에서 키 입력이 막히면
  **큰 노란 버튼이나 화면 아무 곳을 클릭/터치**하면 됩니다.
- 포켓몬 이미지/이름의 권리는 각 권리자(닌텐도·게임프리크·크리에이처스)에게 있습니다. 개인/비공개 용도로만 사용하세요.
