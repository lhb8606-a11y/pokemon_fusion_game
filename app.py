#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
포켓몬스터 퓨~~~전 얍!  (Streamlit 게임)

1세대(No.1~151) 포켓몬 2마리를 퓨전한 이미지를 보고
20초 안에 두 마리 이름을 맞춰보는 게임.

  streamlit run app.py
"""
from __future__ import annotations

import base64
import json
import mimetypes
import os
import random
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).parent
MANIFEST_PATH = ROOT / "manifest.json"
COUNTDOWN = 20
FALLBACK = {
    "fused": "assets/example_fused.png",
    "left": "assets/example_left.png",
    "right": "assets/example_right.png",
    "left_name": "라플레시아",
    "right_name": "럭키",
}
BGM_PATH = ROOT / "assets" / "bgm.mp3"

# --------------------------------------------------------------------- 자원
@st.cache_data(show_spinner=False)
def _data_uri(path_str: str, _mtime: float) -> str:
    p = Path(path_str)
    if not p.exists():
        return ""
    mime = mimetypes.guess_type(p.name)[0] or "image/png"
    return "data:%s;base64,%s" % (mime, base64.b64encode(p.read_bytes()).decode())


def asset_uri(value) -> str:
    if not value:
        return ""
    v = str(value)
    if v.startswith(("http://", "https://", "data:")):
        return v
    p = ROOT / v
    return _data_uri(str(p), p.stat().st_mtime if p.exists() else 0.0)


@st.cache_data(show_spinner=False)
def _load_manifest(path: str, _mtime: float, _size: int):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_manifest():
    if MANIFEST_PATH.exists():
        stt = MANIFEST_PATH.stat()
        return _load_manifest(str(MANIFEST_PATH), stt.st_mtime, stt.st_size)
    return {"entries": []}


@st.cache_data(show_spinner=False)
def _bgm_uri(path: str, _mtime: float) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return "data:audio/mpeg;base64," + base64.b64encode(p.read_bytes()).decode()


def bgm_uri() -> str:
    return _bgm_uri(str(BGM_PATH), BGM_PATH.stat().st_mtime if BGM_PATH.exists() else 0.0)


# --------------------------------------------------------------------- 스타일
CSS = """
<style>
@font-face{font-family:'Galmuri11';src:url('https://cdn.jsdelivr.net/gh/quiple/galmuri/dist/Galmuri11.woff2') format('woff2');font-display:swap;}
@font-face{font-family:'Galmuri11';font-weight:700;src:url('https://cdn.jsdelivr.net/gh/quiple/galmuri/dist/Galmuri11-Bold.woff2') format('woff2');font-display:swap;}

:root{
  --ink:#1f2233; --sub:#7b8298; --red:#ee1515; --yellow:#ffcb05;
  --blue:#3b4cca; --card:#ffffff; --line:#e3e7f3;
}
html,body,[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(1100px 520px at 50% -10%, #ffffff 0%, #eef1fa 45%, #e2e7f7 100%);
  font-family:'Galmuri11','Pretendard','Apple SD Gothic Neo','Malgun Gothic',system-ui,sans-serif;
  color:var(--ink);
}
[data-testid="stHeader"]{background:transparent;}
[data-testid="stToolbar"]{right:8px;}
iframe{background:transparent !important;}
.block-container{padding:0.6rem 0.7rem 3rem;max-width:780px;}

/* ---- 게임 버튼 ---- */
div.stButton > button{
  width:100%; min-height:66px; border-radius:18px; border:3px solid var(--ink);
  background:linear-gradient(180deg,#ffd93d,#ffc400); color:var(--ink);
  font-family:inherit; font-size:19px; font-weight:700; letter-spacing:.5px;
  box-shadow:0 6px 0 var(--ink); transition:transform .06s ease, box-shadow .06s ease, filter .15s;
}
div.stButton > button:hover{border-color:var(--ink); color:var(--ink); filter:brightness(1.04);}
div.stButton > button:active{transform:translateY(5px); box-shadow:0 1px 0 var(--ink);}
div.stButton > button:focus:not(:active){border-color:var(--ink); color:var(--ink);}

/* ---- 보조 텍스트 ---- */
.pf-note{text-align:center;color:var(--sub);font-size:13px;margin:10px 0 0;line-height:1.7;}
.pf-note b{color:var(--blue);}
.pf-sep{height:1px;background:linear-gradient(90deg,transparent,var(--line),transparent);margin:14px 0;}
[data-testid="stSidebar"]{font-family:inherit;}
[data-testid="stSidebar"] *{font-family:inherit;}
</style>
"""

def _html(html_str: str, height: int):
    """HTML 조각을 iframe 컴포넌트로 렌더링.

    Streamlit 1.4x+ 는 st.iframe 을 제공한다(components.html 은 폐기 예정).
    st.iframe 은 HTML 문자열을 그대로 넣고 JS + same-origin 접근을 허용하므로
    아무 키/화면 클릭 브리지와 BGM 주입에 그대로 쓸 수 있다.
    """
    fn = getattr(st, "iframe", None)
    if fn is not None:
        try:
            fn(html_str, height=height)
            return
        except Exception:
            pass
    components.html(html_str, height=height, scrolling=False)


COMPONENT_CSS = """
<style>
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;margin:0;background:transparent;overflow:hidden;color:#1f2233;
  font-family:'Galmuri11','Pretendard','Apple SD Gothic Neo','Malgun Gothic',system-ui,sans-serif;}
.wrap{height:100%;display:flex;flex-direction:column;gap:8px}
</style>
"""

JS_HEAD = "<script>"


# --------------------------------------------------------------------- 화면
def screen_title(count: int, bgm: str):
    html = COMPONENT_CSS + """
<style>
.t{height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;text-align:center;padding:6px}
.ball{width:78px;height:78px;border-radius:50%;border:4px solid #1f2233;position:relative;overflow:hidden;
  background:linear-gradient(180deg,#ee1515 0 47%,#1f2233 47% 53%,#fff 53% 100%);
  box-shadow:0 6px 0 rgba(31,34,51,.25);animation:spin 6s linear infinite}
.ball::after{content:'';position:absolute;left:50%;top:50%;width:26px;height:26px;margin:-13px 0 0 -13px;
  background:#fff;border:4px solid #1f2233;border-radius:50%}
@keyframes spin{to{transform:rotate(360deg)}}
h1{font-size:clamp(26px,7.4vw,44px);line-height:1.25;letter-spacing:-.5px}
h1 .pop{display:inline-block;color:#ee1515;text-shadow:2px 2px 0 #ffcb05,4px 4px 0 rgba(31,34,51,.18)}
.sub{color:#5b6280;font-size:clamp(12px,3.4vw,15px)}
.cta{margin-top:6px;background:#3b4cca;color:#fff;border-radius:14px;padding:12px 20px;font-size:clamp(15px,4.4vw,19px);
  box-shadow:0 5px 0 #1f2233;animation:beat 1.5s ease-in-out infinite}
@keyframes beat{0%,100%{transform:scale(1)}50%{transform:scale(1.045)}}
.meta{color:#7b8298;font-size:clamp(11px,3.1vw,13px);line-height:1.8}
.meta b{color:#1f2233}
</style>
<div class="t">
  <div class="ball"></div>
  <h1>포켓몬스터<span class="pop"> 퓨~~~전 얍!</span></h1>
  <p class="sub">1세대 포켓몬 No.1 ~ 151 · 두 마리가 하나로!</p>
  <div class="cta">아무 키나 누르세요</div>
  <p class="meta">키보드 · 마우스 클릭 · 터치 모두 OK<br>
     준비된 퓨전 포켓몬 <b>__COUNT__</b> 마리</p>
</div>
""".replace("__COUNT__", str(count))
    _html(html, 380)


def screen_tutorial(ex_left: str, ex_right: str, ex_fused: str, lname: str, rname: str, bgm: str):
    """사용법(퓨전 예시) 화면 — 단순 flex 구조(절대좌표/JS 타이머 미사용)."""
    html = COMPONENT_CSS + """
<style>
.tut{height:100%;display:flex;flex-direction:column;gap:6px;padding:2px}
.head{text-align:center;font-size:clamp(12px,3.5vw,16px);color:#3b4cca}
.card{flex:1;min-height:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:linear-gradient(180deg,#ffffff,#f2f5ff);border:3px solid #1f2233;border-radius:20px;
  box-shadow:0 6px 0 #1f2233;padding:8px;gap:6px}
.row{display:flex;align-items:center;justify-content:center;gap:8px;width:100%}
.row img{max-height:120px;max-width:38%;object-fit:contain}
.plus{font-size:26px;font-weight:700;color:#7b8298}
.glow{width:74%;height:6px;border-radius:6px;background:#fff;
  box-shadow:0 0 14px 8px #ffffff,0 0 26px 14px #eef1ff;animation:blink 1.8s ease-in-out infinite}
@keyframes blink{0%,100%{opacity:.45}50%{opacity:1}}
.light{font-size:clamp(11px,3.1vw,13px);color:#7b8298}
.fused{max-height:212px;max-width:78%;object-fit:contain;animation:pop .9s ease-out both}
@keyframes pop{0%{transform:scale(.84)}60%{transform:scale(1.04)}100%{transform:scale(1)}}
.steps{display:flex;flex-direction:column;gap:2px;text-align:center}
.steps p{font-size:clamp(11px,3.2vw,14px);color:#5b6280}
.steps p.big{font-size:clamp(13px,3.9vw,18px);font-weight:700;color:#ee1515}
.steps p.big2{font-size:clamp(12px,3.6vw,16px);font-weight:700;color:#1f2233}
</style>
<div class="tut">
  <div class="head">퓨전 방법 : <b>왼쪽 = 얼굴 · 색</b> ＋ <b>오른쪽 = 몸통 형태</b></div>
  <div class="card">
    <div class="row">
      <img src="__L__"><span class="plus">＋</span><img src="__R__">
    </div>
    <div class="glow"></div>
    <div class="light">하얀 빛과 함께 하나로 합쳐집니다!</div>
    <img class="fused" src="__F__">
  </div>
  <div class="steps">
    <p class="big">이렇게 만들어집니다!</p>
    <p class="big2">이제 포켓몬 2마리 이름을 맞춰보세요!</p>
    <p>__LNAME__ ＋ __RNAME__ → 이 두 마리가 합쳐진 모습입니다</p>
  </div>
</div>
""".replace("__L__", ex_left).replace("__R__", ex_right).replace("__F__", ex_fused) \
   .replace("__LNAME__", lname or "?").replace("__RNAME__", rname or "?")
    _html(html, 560)


def screen_play(entry: dict, pos: int, total: int, reveal: int, lap: int, bgm: str):
    fused = asset_uri(entry.get("fused"))
    left_img = asset_uri(entry.get("left"))
    right_img = asset_uri(entry.get("right"))
    lname = entry.get("left_name") or "?"
    rname = entry.get("right_name") or "?"

    def slot(num, who, img, name, filled):
        if filled:
            return (
                '<div class="slot filled"><div class="label">%s</div>'
                '<img src="%s"><div class="name">%s</div></div>' % (who, img, name)
            )
        return (
            '<div class="slot"><div class="label">%s</div><div class="q">%s</div>'
            '<div class="hintq">정답 공개 대기</div></div>' % (who, num)
        )

    left_slot = slot("1", "합성 1 · 얼굴·색", left_img, lname, reveal >= 2)
    right_slot = slot("2", "합성 2 · 몸통", right_img, rname, reveal >= 1)
    tip = {
        0: "20초 안에 두 마리 이름을 맞춰보세요! (버튼/화면 클릭/아무 키)",
        1: "합성 2 공개! 한 번 더 누르면 합성 1이 공개됩니다",
        2: "정답 확인 완료! 다음 문제로 넘어가세요",
    }[reveal]

    html = COMPONENT_CSS + """
<style>
.top{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:0 2px}
.pill{background:#fff;border:2px solid #1f2233;border-radius:999px;padding:5px 12px;font-size:clamp(11px,3.1vw,13px);box-shadow:0 3px 0 rgba(31,34,51,.18)}
.pill b{color:#3b4cca}
.timer{position:relative;width:58px;height:58px;flex:0 0 auto}
.timer svg{width:100%;height:100%;transform:rotate(-90deg)}
.timer .bgc{fill:#fff;stroke:#e6e9f2;stroke-width:5}
.timer .arc{fill:none;stroke:#3b4cca;stroke-width:5;stroke-linecap:round;
  stroke-dasharray:113.1;stroke-dashoffset:0;transition:stroke-dashoffset 1s linear,stroke .3s}
.timer.done .arc{stroke:#ee1515}
.timer .num{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
  font-size:21px;font-weight:700;color:#3b4cca}
.timer.done .num{color:#ee1515;font-size:15px}
.card{flex:1;min-height:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;
  background:linear-gradient(180deg,#ffffff,#f3f6ff);border:3px solid #1f2233;border-radius:20px;
  box-shadow:0 6px 0 #1f2233;padding:8px;position:relative;overflow:hidden}
.card img{width:auto;height:100%;max-width:100%;object-fit:contain;display:block;
  filter:drop-shadow(0 8px 12px rgba(31,34,51,.16))}
.card .tag{position:absolute;top:6px;left:0;right:0;text-align:center;font-size:clamp(10px,2.9vw,12px);color:#7b8298}
.slots{display:flex;gap:8px}
.slot{flex:1;background:#fff;border:3px dashed #b9c0d8;border-radius:16px;padding:6px;min-height:132px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px}
.slot.filled{border:3px solid #1f2233;box-shadow:0 5px 0 rgba(31,34,51,.18);animation:pop .35s ease-out}
.slot img{max-height:112px;max-width:100%;object-fit:contain}
@media(min-width:620px){.slot img{max-height:152px}}
.slot .label{font-size:clamp(9px,2.6vw,11px);color:#7b8298}
.slot .name{font-size:clamp(15px,4.2vw,19px);font-weight:700;color:#ee1515}
.slot .q{font-size:34px;font-weight:700;color:#ccd2e4}
.slot .hintq{font-size:9px;color:#b9c0d8}
.tip{text-align:center;font-size:clamp(11px,3.2vw,14px);color:#5b6280;padding:0 2px}
@keyframes pop{0%{transform:scale(.86);opacity:0}100%{transform:scale(1);opacity:1}}
</style>
<div class="wrap">
  <div class="top">
    <div class="pill">문제 <b>__POS__</b> / __TOTAL____LAP__</div>
    <div class="timer" id="timer">
      <svg viewBox="0 0 44 44"><circle class="bgc" cx="22" cy="22" r="18"></circle>
      <circle class="arc" id="arc" cx="22" cy="22" r="18"></circle></svg>
      <div class="num" id="num">__SEC__</div>
    </div>
  </div>
  <div class="card">
    <div class="tag">합성(퓨전) 포켓몬</div>
    <img src="__FUSED__">
  </div>
  <div class="slots">__LS__ __RS__</div>
  <div class="tip">__TIP__</div>
</div>
<script>
(function(){
  var t=__SEC__, arc=document.getElementById('arc'), num=document.getElementById('num'),
      box=document.getElementById('timer'), C=113.1;
  function paint(){
    num.textContent = t>0 ? String(t) : 'END';
    arc.style.strokeDashoffset = String(C*(1 - Math.max(t,0)/__SEC__));
  }
  paint();
  var iv=setInterval(function(){ t--; paint(); if(t<=0){ clearInterval(iv); box.classList.add('done');
    document.querySelector('.tip').innerHTML='시간 종료! 정답을 확인해 보세요'; } },1000);
})();
</script>
""".replace("__POS__", str(pos)).replace("__TOTAL__", str(total)) \
   .replace("__LAP__", (" · %d바퀴" % lap) if lap > 1 else "") \
   .replace("__SEC__", str(COUNTDOWN)) \
   .replace("__FUSED__", fused).replace("__LS__", left_slot).replace("__RS__", right_slot) \
   .replace("__TIP__", tip)
    _html(html, 600)


# ------------------------------------------------------------------- 키 브리지
def key_bridge(bgm: str):
    """아무 키 / 화면 아무 곳 클릭 → 메인 버튼 클릭.  BGM 은 부모 문서에 심어 리런에도 유지."""
    js = """
<style>html,body{margin:0;padding:0;background:transparent}</style>
<script>
(function(){
  var p, d;
  try{ p = window.parent; d = p.document; }catch(e){ return; }
  function mainBtn(){
    var list = d.querySelectorAll('[data-testid="stButton"] button, .stButton button');
    for(var i=0;i<list.length;i++){
      var b=list[i];
      if(b.closest('[data-testid="stSidebar"]')) continue;
      if(b.closest('[data-testid="stToolbar"]')||b.closest('header')) continue;
      if(b.disabled) continue;
      return b;
    }
    return null;
  }
  function fire(){ var b=mainBtn(); if(b){ b.click(); return true; } return false; }
  if(!d.__pfKey){
    d.__pfKey = true;
    d.addEventListener('keydown', function(e){
      if(e.repeat || e.ctrlKey || e.metaKey || e.altKey) return;
      var k=e.key||'';
      if(k==='Shift'||k==='Control'||k==='Alt'||k==='Meta'||k==='Tab'||k==='Escape'||k==='CapsLock'||/^F\\d+$/.test(k)) return;
      var t=e.target;
      if(t && (t.tagName==='INPUT'||t.tagName==='TEXTAREA'||t.isContentEditable)) return;
      if(fire()) e.preventDefault();
    }, true);
    d.addEventListener('click', function(e){
      var t=e.target;
      if(!t || !t.closest) return;
      if(t.closest('[data-testid="stSidebar"]')) return;
      if(t.closest('button')||t.closest('a')||t.closest('input')||t.closest('select')) return;
      if(t.closest('[data-testid="stToolbar"]')||t.closest('header')) return;
      if(!t.closest('[data-testid="stMain"]') && !t.closest('section.main') && !t.closest('.main')) return;
      fire();
    }, true);
  }
  try{
    var src = '__BGM__';
    if(src && !d.__pfBgm){
      var a = d.createElement('audio');
      a.src = src; a.loop = true; a.volume = 0.4;
      a.style.display='none';
      d.body.appendChild(a);
      d.__pfBgm = a;
      var btn = d.createElement('div');
      btn.textContent = '♪ BGM 켜기';
      btn.setAttribute('style','position:fixed;left:10px;bottom:10px;z-index:99999;background:#fff;border:2px solid #1f2233;border-radius:999px;padding:6px 12px;font-size:12px;cursor:pointer;box-shadow:0 3px 0 rgba(31,34,51,.25);font-family:inherit');
      btn.addEventListener('click', function(ev){
        ev.stopPropagation();
        if(a.paused){ a.play(); btn.textContent='♪ BGM 끄기'; }
        else { a.pause(); btn.textContent='♪ BGM 켜기'; }
      }, true);
      d.body.appendChild(btn);
      d.__pfBgmBtn = btn;
    }
    if(d.__pfBgm && d.__pfBgm.paused && !d.__pfBgmUserOff){
      var pr = d.__pfBgm.play();
      if(pr && pr.catch){ pr.catch(function(){}); }
      if(d.__pfBgmBtn) d.__pfBgmBtn.textContent = '♪ BGM 끄기';
    }
    if(d.__pfBgmBtn){
      d.__pfBgmBtn.addEventListener('click', function(){ /* keep state */ });
    }
  }catch(e){}
})();
</script>
""".replace("__BGM__", bgm or "")
    _html(js, 18)


# ------------------------------------------------------------------- 게임 상태
def start_play(n: int, reset: bool = True):
    S = st.session_state
    if n <= 0:
        S.order, S.pos, S.reveal, S.lap = [], 0, 0, 1
        return
    if reset or "order" not in S or len(S.order) != n:
        S.order = list(range(n))
        random.shuffle(S.order)
        S.pos = 0
        S.reveal = 0
        S.lap = 1


def next_question(n: int):
    S = st.session_state
    S.reveal = 0
    S.pos += 1
    if S.pos >= len(S.order) or S.pos >= n:
        S.order = list(range(n))
        random.shuffle(S.order)
        S.pos = 0
        S.lap = S.get("lap", 1) + 1


def main():
    st.set_page_config(
        page_title="포켓몬스터 퓨~~~전 얍!",
        page_icon="⚡",
        layout="centered",
        initial_sidebar_state="collapsed",
    )
    st.markdown(CSS, unsafe_allow_html=True)
    S = st.session_state

    data = load_manifest()
    entries = data.get("entries", []) or []
    n = len(entries)
    bgm = bgm_uri()

    if "phase" not in S:
        S.phase = "title"

    # 개발/미리보기 전용 (PF_DEV=1 로 실행했을 때만): ?p=tutorial|play&r=0|1|2
    if os.environ.get("PF_DEV") == "1":
        qp = st.query_params
        if qp.get("p") in ("title", "tutorial", "play"):
            S.phase = qp.get("p")
        if qp.get("r") in ("0", "1", "2"):
            S.reveal = int(qp.get("r"))
    if n and ("order" not in S or len(S.order) != n):
        start_play(n, reset=True)

    # ---------------- 사이드바 (보조 도구) ----------------
    with st.sidebar:
        st.markdown("### ⚙ 설정")
        st.caption("1세대 퓨전 포켓몬 %d마리 준비됨" % n)
        if st.button("🔄 처음부터 다시 시작", use_container_width=True):
            S.phase = "title"
            start_play(n, reset=True)
            st.rerun()
        if st.button("🔀 순서 다시 섞기", use_container_width=True):
            start_play(n, reset=True)
            st.rerun()
        st.divider()
        st.caption("BGM : 왼쪽 아래 `♪ BGM` 버튼으로 켜고 끌 수 있어요.")

    key_bridge(bgm)

    # ---------------- 데이터 없음 ----------------
    if n == 0:
        st.markdown("## 포켓몬스터 퓨~~~전 얍!")
        st.warning(
            "아직 퓨전 이미지가 없습니다.\n\n"
            "1. `captures/` 폴더에 캡처한 이미지를 넣고\n"
            "2. `python tools/build_manifest.py --src captures` 를 실행하세요.\n\n"
            "(`manifest.json` + `images/` 가 만들어집니다)"
        )
        return

    # ---------------- 1. 타이틀 ----------------
    if S.phase == "title":
        screen_title(n, bgm)
        if st.button("▶  아무 키나 누르세요  (시작)", use_container_width=True):
            S.phase = "tutorial"
            st.rerun()
        st.markdown(
            '<p class="pf-note">키보드는 <b>아무 키</b>, 모바일은 <b>화면 터치</b>로 넘어갑니다.</p>',
            unsafe_allow_html=True,
        )
        return

    # ---------------- 2. 사용법(퓨전 예시) ----------------
    if S.phase == "tutorial":
        ex = entries[0] if entries else FALLBACK
        screen_tutorial(
            asset_uri(ex.get("left") or FALLBACK["left"]),
            asset_uri(ex.get("right") or FALLBACK["right"]),
            asset_uri(ex.get("fused") or FALLBACK["fused"]),
            ex.get("left_name") or FALLBACK["left_name"],
            ex.get("right_name") or FALLBACK["right_name"],
            bgm,
        )
        if st.button("▶  아무 키나 눌러서 게임 시작", use_container_width=True):
            S.phase = "play"
            start_play(n, reset=True)
            st.rerun()
        st.markdown(
            '<p class="pf-note">왼쪽 포켓몬 = <b>얼굴·색</b> / 오른쪽 포켓몬 = <b>몸통 형태</b></p>',
            unsafe_allow_html=True,
        )
        return

    # ---------------- 3. 게임 ----------------
    if not S.order:
        start_play(n, reset=True)
    idx = S.order[S.pos]
    entry = entries[idx % n]
    reveal = S.get("reveal", 0)
    lap = S.get("lap", 1)

    screen_play(entry, S.pos + 1, n, reveal, lap, bgm)

    if reveal == 0:
        label = "👀  정답 공개  (합성 2 · 몸통)"
    elif reveal == 1:
        label = "👀  정답 공개  (합성 1 · 얼굴)"
    else:
        label = "▶  다음 문제"

    if st.button(label, use_container_width=True):
        if reveal >= 2:
            next_question(n)
        else:
            S.reveal = reveal + 1
        st.rerun()

    st.markdown(
        '<p class="pf-note">키보드 <b>아무 키</b> · 화면 <b>아무 곳 클릭/터치</b> 로도 진행됩니다.</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
