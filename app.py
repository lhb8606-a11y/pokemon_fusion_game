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
    "fused": "@ex:fused",
    "left": "@ex:left",
    "right": "@ex:right",
    "left_name": "라플레시아",
    "right_name": "럭키",
}
BGM_PATH = ROOT / "bgm.mp3" if (ROOT / "bgm.mp3").exists() else ROOT / "assets" / "bgm.mp3"







# =====================================================================
#  캡처 자동 처리 (이 파일 안에 모두 포함 — 다른 폴더가 없어도 동작)
# =====================================================================
import csv as _csv

POKEMON_NAMES = json.loads('{"bulbasaur": {"en": "Bulbasaur", "ko": "이상해씨", "dex": 1}, "ivysaur": {"en": "Ivysaur", "ko": "이상해풀", "dex": 2}, "venusaur": {"en": "Venusaur", "ko": "이상해꽃", "dex": 3}, "charmander": {"en": "Charmander", "ko": "파이리", "dex": 4}, "charmeleon": {"en": "Charmeleon", "ko": "리자드", "dex": 5}, "charizard": {"en": "Charizard", "ko": "리자몽", "dex": 6}, "squirtle": {"en": "Squirtle", "ko": "꼬부기", "dex": 7}, "wartortle": {"en": "Wartortle", "ko": "어니부기", "dex": 8}, "blastoise": {"en": "Blastoise", "ko": "거북왕", "dex": 9}, "caterpie": {"en": "Caterpie", "ko": "캐터피", "dex": 10}, "metapod": {"en": "Metapod", "ko": "단데기", "dex": 11}, "butterfree": {"en": "Butterfree", "ko": "버터플", "dex": 12}, "weedle": {"en": "Weedle", "ko": "뿔충이", "dex": 13}, "kakuna": {"en": "Kakuna", "ko": "딱충이", "dex": 14}, "beedrill": {"en": "Beedrill", "ko": "독침붕", "dex": 15}, "pidgey": {"en": "Pidgey", "ko": "구구", "dex": 16}, "pidgeotto": {"en": "Pidgeotto", "ko": "피죤", "dex": 17}, "pidgeot": {"en": "Pidgeot", "ko": "피죤투", "dex": 18}, "rattata": {"en": "Rattata", "ko": "꼬렛", "dex": 19}, "raticate": {"en": "Raticate", "ko": "레트라", "dex": 20}, "spearow": {"en": "Spearow", "ko": "깨비참", "dex": 21}, "fearow": {"en": "Fearow", "ko": "깨비드릴조", "dex": 22}, "ekans": {"en": "Ekans", "ko": "아보", "dex": 23}, "arbok": {"en": "Arbok", "ko": "아보크", "dex": 24}, "pikachu": {"en": "Pikachu", "ko": "피카츄", "dex": 25}, "raichu": {"en": "Raichu", "ko": "라이츄", "dex": 26}, "sandshrew": {"en": "Sandshrew", "ko": "모래두지", "dex": 27}, "sandslash": {"en": "Sandslash", "ko": "고지", "dex": 28}, "nidoran♀": {"en": "Nidoran♀", "ko": "니드런♀", "dex": 29}, "nidorina": {"en": "Nidorina", "ko": "니드리나", "dex": 30}, "nidoqueen": {"en": "Nidoqueen", "ko": "니드퀸", "dex": 31}, "nidoran♂": {"en": "Nidoran♂", "ko": "니드런♂", "dex": 32}, "nidorino": {"en": "Nidorino", "ko": "니드리노", "dex": 33}, "nidoking": {"en": "Nidoking", "ko": "니드킹", "dex": 34}, "clefairy": {"en": "Clefairy", "ko": "삐삐", "dex": 35}, "clefable": {"en": "Clefable", "ko": "픽시", "dex": 36}, "vulpix": {"en": "Vulpix", "ko": "식스테일", "dex": 37}, "ninetales": {"en": "Ninetales", "ko": "나인테일", "dex": 38}, "jigglypuff": {"en": "Jigglypuff", "ko": "푸린", "dex": 39}, "wigglytuff": {"en": "Wigglytuff", "ko": "푸크린", "dex": 40}, "zubat": {"en": "Zubat", "ko": "주뱃", "dex": 41}, "golbat": {"en": "Golbat", "ko": "골뱃", "dex": 42}, "oddish": {"en": "Oddish", "ko": "뚜벅쵸", "dex": 43}, "gloom": {"en": "Gloom", "ko": "냄새꼬", "dex": 44}, "vileplume": {"en": "Vileplume", "ko": "라플레시아", "dex": 45}, "paras": {"en": "Paras", "ko": "파라스", "dex": 46}, "parasect": {"en": "Parasect", "ko": "파라섹트", "dex": 47}, "venonat": {"en": "Venonat", "ko": "콘팡", "dex": 48}, "venomoth": {"en": "Venomoth", "ko": "도나리", "dex": 49}, "diglett": {"en": "Diglett", "ko": "디그다", "dex": 50}, "dugtrio": {"en": "Dugtrio", "ko": "닥트리오", "dex": 51}, "meowth": {"en": "Meowth", "ko": "나옹", "dex": 52}, "persian": {"en": "Persian", "ko": "페르시온", "dex": 53}, "psyduck": {"en": "Psyduck", "ko": "고라파덕", "dex": 54}, "golduck": {"en": "Golduck", "ko": "골덕", "dex": 55}, "mankey": {"en": "Mankey", "ko": "망키", "dex": 56}, "primeape": {"en": "Primeape", "ko": "성원숭", "dex": 57}, "growlithe": {"en": "Growlithe", "ko": "가디", "dex": 58}, "arcanine": {"en": "Arcanine", "ko": "윈디", "dex": 59}, "poliwag": {"en": "Poliwag", "ko": "발챙이", "dex": 60}, "poliwhirl": {"en": "Poliwhirl", "ko": "슈륙챙이", "dex": 61}, "poliwrath": {"en": "Poliwrath", "ko": "강챙이", "dex": 62}, "abra": {"en": "Abra", "ko": "캐이시", "dex": 63}, "kadabra": {"en": "Kadabra", "ko": "윤겔라", "dex": 64}, "alakazam": {"en": "Alakazam", "ko": "후딘", "dex": 65}, "machop": {"en": "Machop", "ko": "알통몬", "dex": 66}, "machoke": {"en": "Machoke", "ko": "근육몬", "dex": 67}, "machamp": {"en": "Machamp", "ko": "괴력몬", "dex": 68}, "bellsprout": {"en": "Bellsprout", "ko": "모다피", "dex": 69}, "weepinbell": {"en": "Weepinbell", "ko": "우츠동", "dex": 70}, "victreebel": {"en": "Victreebel", "ko": "우츠보트", "dex": 71}, "tentacool": {"en": "Tentacool", "ko": "왕눈해", "dex": 72}, "tentacruel": {"en": "Tentacruel", "ko": "독파리", "dex": 73}, "geodude": {"en": "Geodude", "ko": "꼬마돌", "dex": 74}, "graveler": {"en": "Graveler", "ko": "데구리", "dex": 75}, "golem": {"en": "Golem", "ko": "딱구리", "dex": 76}, "ponyta": {"en": "Ponyta", "ko": "포니타", "dex": 77}, "rapidash": {"en": "Rapidash", "ko": "날쌩마", "dex": 78}, "slowpoke": {"en": "Slowpoke", "ko": "야돈", "dex": 79}, "slowbro": {"en": "Slowbro", "ko": "야도란", "dex": 80}, "magnemite": {"en": "Magnemite", "ko": "코일", "dex": 81}, "magneton": {"en": "Magneton", "ko": "레어코일", "dex": 82}, "farfetch’d": {"en": "Farfetch’d", "ko": "파오리", "dex": 83}, "doduo": {"en": "Doduo", "ko": "두두", "dex": 84}, "dodrio": {"en": "Dodrio", "ko": "두트리오", "dex": 85}, "seel": {"en": "Seel", "ko": "쥬쥬", "dex": 86}, "dewgong": {"en": "Dewgong", "ko": "쥬레곤", "dex": 87}, "grimer": {"en": "Grimer", "ko": "질퍽이", "dex": 88}, "muk": {"en": "Muk", "ko": "질뻐기", "dex": 89}, "shellder": {"en": "Shellder", "ko": "셀러", "dex": 90}, "cloyster": {"en": "Cloyster", "ko": "파르셀", "dex": 91}, "gastly": {"en": "Gastly", "ko": "고오스", "dex": 92}, "haunter": {"en": "Haunter", "ko": "고우스트", "dex": 93}, "gengar": {"en": "Gengar", "ko": "팬텀", "dex": 94}, "onix": {"en": "Onix", "ko": "롱스톤", "dex": 95}, "drowzee": {"en": "Drowzee", "ko": "슬리프", "dex": 96}, "hypno": {"en": "Hypno", "ko": "슬리퍼", "dex": 97}, "krabby": {"en": "Krabby", "ko": "크랩", "dex": 98}, "kingler": {"en": "Kingler", "ko": "킹크랩", "dex": 99}, "voltorb": {"en": "Voltorb", "ko": "찌리리공", "dex": 100}, "electrode": {"en": "Electrode", "ko": "붐볼", "dex": 101}, "exeggcute": {"en": "Exeggcute", "ko": "아라리", "dex": 102}, "exeggutor": {"en": "Exeggutor", "ko": "나시", "dex": 103}, "cubone": {"en": "Cubone", "ko": "탕구리", "dex": 104}, "marowak": {"en": "Marowak", "ko": "텅구리", "dex": 105}, "hitmonlee": {"en": "Hitmonlee", "ko": "시라소몬", "dex": 106}, "hitmonchan": {"en": "Hitmonchan", "ko": "홍수몬", "dex": 107}, "lickitung": {"en": "Lickitung", "ko": "내루미", "dex": 108}, "koffing": {"en": "Koffing", "ko": "또가스", "dex": 109}, "weezing": {"en": "Weezing", "ko": "또도가스", "dex": 110}, "rhyhorn": {"en": "Rhyhorn", "ko": "뿔카노", "dex": 111}, "rhydon": {"en": "Rhydon", "ko": "코뿌리", "dex": 112}, "chansey": {"en": "Chansey", "ko": "럭키", "dex": 113}, "tangela": {"en": "Tangela", "ko": "덩쿠리", "dex": 114}, "kangaskhan": {"en": "Kangaskhan", "ko": "캥카", "dex": 115}, "horsea": {"en": "Horsea", "ko": "쏘드라", "dex": 116}, "seadra": {"en": "Seadra", "ko": "시드라", "dex": 117}, "goldeen": {"en": "Goldeen", "ko": "콘치", "dex": 118}, "seaking": {"en": "Seaking", "ko": "왕콘치", "dex": 119}, "staryu": {"en": "Staryu", "ko": "별가사리", "dex": 120}, "starmie": {"en": "Starmie", "ko": "아쿠스타", "dex": 121}, "mr. mime": {"en": "Mr. Mime", "ko": "마임맨", "dex": 122}, "scyther": {"en": "Scyther", "ko": "스라크", "dex": 123}, "jynx": {"en": "Jynx", "ko": "루주라", "dex": 124}, "electabuzz": {"en": "Electabuzz", "ko": "에레브", "dex": 125}, "magmar": {"en": "Magmar", "ko": "마그마", "dex": 126}, "pinsir": {"en": "Pinsir", "ko": "쁘사이저", "dex": 127}, "tauros": {"en": "Tauros", "ko": "켄타로스", "dex": 128}, "magikarp": {"en": "Magikarp", "ko": "잉어킹", "dex": 129}, "gyarados": {"en": "Gyarados", "ko": "갸라도스", "dex": 130}, "lapras": {"en": "Lapras", "ko": "라프라스", "dex": 131}, "ditto": {"en": "Ditto", "ko": "메타몽", "dex": 132}, "eevee": {"en": "Eevee", "ko": "이브이", "dex": 133}, "vaporeon": {"en": "Vaporeon", "ko": "샤미드", "dex": 134}, "jolteon": {"en": "Jolteon", "ko": "쥬피썬더", "dex": 135}, "flareon": {"en": "Flareon", "ko": "부스터", "dex": 136}, "porygon": {"en": "Porygon", "ko": "폴리곤", "dex": 137}, "omanyte": {"en": "Omanyte", "ko": "암나이트", "dex": 138}, "omastar": {"en": "Omastar", "ko": "암스타", "dex": 139}, "kabuto": {"en": "Kabuto", "ko": "투구", "dex": 140}, "kabutops": {"en": "Kabutops", "ko": "투구푸스", "dex": 141}, "aerodactyl": {"en": "Aerodactyl", "ko": "프테라", "dex": 142}, "snorlax": {"en": "Snorlax", "ko": "잠만보", "dex": 143}, "articuno": {"en": "Articuno", "ko": "프리져", "dex": 144}, "zapdos": {"en": "Zapdos", "ko": "썬더", "dex": 145}, "moltres": {"en": "Moltres", "ko": "파이어", "dex": 146}, "dratini": {"en": "Dratini", "ko": "미뇽", "dex": 147}, "dragonair": {"en": "Dragonair", "ko": "신뇽", "dex": 148}, "dragonite": {"en": "Dragonite", "ko": "망나뇽", "dex": 149}, "mewtwo": {"en": "Mewtwo", "ko": "뮤츠", "dex": 150}, "mew": {"en": "Mew", "ko": "뮤", "dex": 151}}')

EXAMPLE_IMG = {
    "fused": "data:image/png;base64,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",
    "left": "data:image/png;base64,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",
    "right": "data:image/png;base64,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",
}


def load_names():
    table = POKEMON_NAMES
    idx = {norm(k): v for k, v in table.items()}
    idx.update({norm(v.get("ko")): v for v in table.values() if v.get("ko")})
    return table, idx


"""퓨전 캡처 자동 처리 코어 (폰 캡처 구조 대응 / 속도 개선판)

캡처 위치가 항상 같다는 점을 이용해 '정해진 구역'만 보고 잘라낸다.
이름은 주소창의 도련번호(...net/43/93)를 OCR 1회로 읽는다.
"""
import re
from difflib import SequenceMatcher

import cv2
import numpy as np
from PIL import Image

try:
    import pytesseract
except Exception:
    pytesseract = None

IMG_EXTS = ('.png', '.jpg', '.jpeg', '.webp', '.bmp')

# 캡처 안에서 포켓몬이 항상 있는 구역 (가로/세로 비율) — 여기만 검사
LAYOUT = {
    "fused": (0.18, 0.24, 0.82, 0.53),
    "left":  (0.04, 0.52, 0.50, 0.73),
    "right": (0.50, 0.52, 0.96, 0.73),
}
PERMALINK_BAND = (0.0, 0.84, 1.0, 1.0)


def norm(s):
    s = (s or '').lower().replace('♀', 'f').replace('♂', 'm')
    return re.sub(r'[^a-z0-9가-힣]', '', s)


def match_name(text, idx, threshold=0.78):
    """OCR 문자열에서 1세대 포켓몬 이름 찾기 (영어 이름만 사용)"""
    if not text:
        return None
    en = {k: v for k, v in idx.items() if k.isascii() and len(k) >= 3}
    joined = norm(text)
    if joined in en:
        return en[joined]
    for key, val in en.items():
        if len(key) >= 4 and key in joined:
            return val
    best, bestr = None, 0.0
    for tok in re.split(r'[^A-Za-z0-9♀♂]+', text):
        t = norm(tok)
        if len(t) < 4:
            continue
        for key, val in en.items():
            if abs(len(key) - len(t)) > 3:
                continue
            r = SequenceMatcher(None, t, key).ratio()
            if key.startswith(t) or t.startswith(key):
                r += 0.08
            if r > bestr:
                best, bestr = val, r
    return best if bestr >= threshold else None


def by_dex(table, dex):
    for v in table.values():
        if v.get("dex") == dex:
            return v
    return None


def lookup_ko(name, table):
    name = (name or "").strip()
    for v in table.values():
        if v.get("ko") == name:
            return v
    return table.get(name.lower())


# --------------------------------------------------------------- 영역 검출
def _bg_color(rgb):
    h, w, _ = rgb.shape
    b = 2
    border = np.concatenate([rgb[:b].reshape(-1, 3), rgb[-b:].reshape(-1, 3),
                             rgb[:, :b].reshape(-1, 3), rgb[:, -b:].reshape(-1, 3)])
    q = (border // 8).astype(np.int32)
    keys = q[:, 0] * 1024 + q[:, 1] * 32 + q[:, 2]
    vals, counts = np.unique(keys, return_counts=True)
    return border[keys == vals[np.argmax(counts)]].mean(axis=0)


def _mask(rgb):
    """배경도 아니고 색이 있는 픽셀 = 포켓몬 그림 후보"""
    bg = _bg_color(rgb)
    diff = (np.abs(rgb.astype(np.int16) - bg[None, None, :].astype(np.int16)).max(axis=2) > 30)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    colorful = (hsv[:, :, 1] > 55) & (hsv[:, :, 2] > 60)
    return (diff & colorful).astype(np.uint8) * 255


def _best_blob(mask, win):
    x0, y0, x1, y1 = win
    sub = mask[y0:y1, x0:x1]
    if sub.size == 0:
        return None
    k = max(3, int(round(min(sub.shape[:2]) / 40)) | 1)
    sub = cv2.morphologyEx(sub, cv2.MORPH_CLOSE,
                           cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)), iterations=2)
    n, lab, stats, cent = cv2.connectedComponentsWithStats(sub, 8)
    best = None
    for i in range(1, n):
        x, y, w, h, a = [int(v) for v in stats[i]]
        if a < 0.0015 * sub.size or w < 6 or h < 6:
            continue
        if w > 0.92 * (x1 - x0) and h < 0.15 * (y1 - y0):   # 가로로 긴 선/테두리
            continue
        if h > 0.92 * (y1 - y0) and w < 0.15 * (x1 - x0):
            continue
        if best is None or a > best['area']:
            best = {'x': x0 + x, 'y': y0 + y, 'w': w, 'h': h, 'area': a}
    return best


def _win(pil, frac):
    W, H = pil.size
    return (int(frac[0] * W), int(frac[1] * H), int(frac[2] * W), int(frac[3] * H))


def find_blobs(path, debug_dir=None):
    """캡처 → {fused,left,right} 영역. 정해진 구역만 검사하므로 빠르다."""
    pil = Image.open(path).convert('RGB')
    rgb = np.asarray(pil)
    mask = _mask(rgb)
    boxes = {}
    for key in ("fused", "left", "right"):
        b = _best_blob(mask, _win(pil, LAYOUT[key]))
        if b:
            boxes[key] = b
    if debug_dir:
        import os
        os.makedirs(debug_dir, exist_ok=True)
        viz = rgb.copy()
        for k, b in boxes.items():
            cv2.rectangle(viz, (b['x'], b['y']), (b['x'] + b['w'], b['y'] + b['h']), (255, 0, 0), 2)
        Image.fromarray(viz).save(os.path.join(debug_dir, 'debug_' + os.path.basename(path)))
    return pil, (boxes if len(boxes) == 3 else None), None


def find_blobs_auto(path):
    """예비: 정해진 구역에서 못 찾았을 때 전체에서 찾는다(느리지만 구조가 다른 캡처 대응)."""
    pil = Image.open(path).convert('RGB')
    rgb = np.asarray(pil)
    H, W, _ = rgb.shape
    mask = _mask(rgb)
    k = max(3, int(round(min(H, W) / 90)) | 1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE,
                            cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)), iterations=2)
    n, lab, stats, cent = cv2.connectedComponentsWithStats(mask, 8)
    blobs = []
    for i in range(1, n):
        x, y, w, h, a = [int(v) for v in stats[i]]
        if y + h / 2.0 < 0.045 * H or y > 0.93 * H:
            continue
        if w > 0.85 * W and h < 0.22 * H:
            continue
        if a < 0.00035 * W * H or w < 0.015 * W or h < 0.012 * H:
            continue
        if not (0.25 <= w / max(1.0, h) <= 3.2):
            continue
        blobs.append({'x': x, 'y': y, 'w': w, 'h': h, 'area': a})
    if not blobs:
        return pil, None
    blobs.sort(key=lambda b: -b['area'])
    fused = next((b for b in blobs if (b['y'] + b['h'] / 2.0) < 0.62 * H), blobs[0])
    low = [b for b in blobs if b is not fused and b['y'] > fused['y'] + fused['h'] - 0.02 * H]
    lefts = [b for b in low if b['x'] + b['w'] / 2.0 < 0.5 * W]
    rights = [b for b in low if b['x'] + b['w'] / 2.0 >= 0.5 * W]
    if lefts and rights:
        return pil, {'fused': fused, 'left': max(lefts, key=lambda b: b['area']),
                     'right': max(rights, key=lambda b: b['area'])}
    return pil, None


def crop_with_pad(pil, box, pad):
    W, H = pil.size
    px, py = int(box['w'] * pad) + 3, int(box['h'] * pad) + 3
    return pil.crop((max(0, box['x'] - px), max(0, box['y'] - py),
                     min(W, box['x'] + box['w'] + px), min(H, box['y'] + box['h'] + py)))


# --------------------------------------------------------------- 글자 읽기
def _ocr(pil, box, psm=6, upscale=None):
    x0, y0, x1, y1 = [int(v) for v in box]
    if x1 - x0 < 6 or y1 - y0 < 6:
        return ""
    g = cv2.cvtColor(np.asarray(pil.crop((x0, y0, x1, y1))), cv2.COLOR_RGB2GRAY)
    if upscale is None:
        upscale = max(1.0, 1200.0 / max(1, g.shape[1]))
    if upscale > 1.05:
        g = cv2.resize(g, None, fx=upscale, fy=upscale, interpolation=cv2.INTER_CUBIC)
    g = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    try:
        return pytesseract.image_to_string(g, config='--psm %d' % psm).strip()
    except Exception:
        return ""


def ocr_permalink_dex(pil):
    """주소창 'Permalink: ...net/43/93' → (왼쪽 도감번호, 오른쪽 도감번호). OCR 1회."""
    W, H = pil.size
    box = (int(PERMALINK_BAND[0] * W), int(PERMALINK_BAND[1] * H),
           int(PERMALINK_BAND[2] * W), int(PERMALINK_BAND[3] * H))
    for psm in (6, 11):
        t = _ocr(pil, box, psm=psm, upscale=max(2.0, 1600.0 / max(1, W)))
        m = re.search(r'net/(\d{1,3})/(\d{1,3})', t.replace(' ', ''))
        if m:
            d1, d2 = int(m.group(1)), int(m.group(2))
            if 1 <= d1 <= 151 and 1 <= d2 <= 151:
                return d1, d2
    return None


def ocr_name_near(pil, box, idx):
    """포켓몬 그림 위(이름 상자) 글자 읽기 — 2구역만 시도"""
    W, H = pil.size
    x, y, w, h = box['x'], box['y'], box['w'], box['h']
    for fh, fw in ((1.6, 0.8), (2.2, 1.2)):
        y0, y1 = max(0, int(y - fh * h)), max(1, int(y - 0.04 * h))
        x0, x1 = max(0, int(x - fw * w)), min(W, int(x + w + fw * w))
        for psm in (6, 7):
            m = match_name(_ocr(pil, (x0, y0, x1, y1), psm=psm), idx)
            if m:
                return m
    return None


def process_capture(path, idx, table, manual_pair=None, pad=0.07, debug_dir=None):
    """캡처 1장 → 잘라낸 3그림 + 한글 이름. 실패하면 None."""
    pil, boxes, _ = find_blobs(path, debug_dir=debug_dir)
    if boxes is None:                     # 폰 캡처가 아니면 예비 검출로 한 번 더
        pil, boxes = find_blobs_auto(path)
    if boxes is None:
        return None
    warn = []
    ln = rn = None
    if manual_pair:
        l, r = manual_pair
        ln = (idx.get(norm(l)) or lookup_ko(l, table)) if l else None
        rn = (idx.get(norm(r)) or lookup_ko(r, table)) if r else None

    if pytesseract is not None and (ln is None or rn is None):
        perm = ocr_permalink_dex(pil)              # 1) 주소창 도감번호 (빠름)
        if perm:
            ln = ln or by_dex(table, perm[0])
            rn = rn or by_dex(table, perm[1])
            if ln is None or rn is None:
                warn.append("주소창 번호 %d/%d 를 이름표에서 찾지 못함" % perm)
        if ln is None or rn is None:               # 2) 주소창 실패한 쪽만 이름표 OCR
            ln = ln or ocr_name_near(pil, boxes['left'], idx)
            rn = rn or ocr_name_near(pil, boxes['right'], idx)

    out = {k: crop_with_pad(pil, boxes[k], pad) for k in ("fused", "left", "right")}
    out.update(left_name=ln, right_name=rn, warn=warn)
    return out

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
    if v.startswith("@ex:"):
        return EXAMPLE_IMG[v[4:]]
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


# ------------------------------------------------- captures/ 자동 처리
CAPTURES_DIR = ROOT / "captures"
MANUAL_CSV = ROOT / "manual_names.csv"
IMG_EXTS = (".png", ".jpg", ".jpeg", ".webp", ".bmp")


def _pil_uri(img) -> str:
    import io
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def _capture_files():
    """캡처 이미지 찾기: captures 폴더 + 저장소 맨 위(루트)에 바로 올린 이미지 모두."""
    found = []
    for d in (CAPTURES_DIR, ROOT):
        if d.exists() and d.is_dir():
            for p in sorted(d.iterdir()):
                if p.is_file() and p.suffix.lower() in IMG_EXTS:
                    found.append(p)
    return found


def _capture_signature():
    files = _capture_files()
    sig = tuple((str(p.relative_to(ROOT)), p.stat().st_size, int(p.stat().st_mtime)) for p in files)
    if MANUAL_CSV.exists():
        sig += (("manual_names.csv", MANUAL_CSV.stat().st_size, int(MANUAL_CSV.stat().st_mtime)),)
    return sig


@st.cache_data(show_spinner=False, max_entries=2000)
def _process_one(name, size, mtime, m_l, m_r):
    """캡처 1장만 처리(파일별 캐시) — 새로 올린 캡처만 계산하므로 빠르다."""
    table, idx = load_names()
    pair = (m_l, m_r) if (m_l or m_r) else None
    try:
        r = process_capture(str(ROOT / name), idx, table, pair)
    except Exception as e:
        return {"error": str(e)}
    if r is None:
        return None
    return {
        "fused": _pil_uri(r["fused"]),
        "left": _pil_uri(r["left"]),
        "right": _pil_uri(r["right"]),
        "left_name": r["left_name"]["ko"] if r["left_name"] else None,
        "right_name": r["right_name"]["ko"] if r["right_name"] else None,
        "warn": r.get("warn", []),
    }


def _process_captures(sig):
    """캡처 목록 → 게임 문제 목록. 파일별 캐시 덕분에 추가분만 계산한다."""
    manual = {}
    if MANUAL_CSV.exists():
        with open(MANUAL_CSV, encoding="utf-8-sig", newline="") as f:
            for row in _csv.DictReader(f):
                if row.get("file"):
                    manual[row["file"].strip()] = ((row.get("left") or "").strip(),
                                                   (row.get("right") or "").strip())
    names = [x for x in sig if x[0] != "manual_names.csv"]
    entries, seen, problems = [], set(), []
    bar = st.progress(0.0, text="캡처 정리 중…")
    for i, (name, size, mtime) in enumerate(names):
        bar.progress((i + 1) / max(1, len(names)), text="캡처 정리 중… %d / %d" % (i + 1, len(names)))
        m = manual.get(Path(name).name, ("", ""))
        r = _process_one(name, size, mtime, m[0], m[1])
        if r is None:
            problems.append((Path(name).name, "합성/좌/우 그림을 찾지 못함"))
            continue
        if "error" in r:
            problems.append((Path(name).name, "오류: %s" % r["error"]))
            continue
        if r["left_name"] and r["right_name"]:
            key = (r["left_name"], r["right_name"])
            if key in seen:
                continue
            seen.add(key)
        else:
            problems.append((Path(name).name, "이름을 읽지 못함"))
        for w in r.get("warn", []):
            problems.append((Path(name).name, w))
        entries.append({"id": "%03d" % (len(entries) + 1), "source": Path(name).name,
                        "fused": r["fused"], "left": r["left"], "right": r["right"],
                        "left_name": r["left_name"] or "?", "right_name": r["right_name"] or "?"})
    bar.empty()
    return {"entries": entries, "problems": problems, "total_files": len(names)}


def load_entries():
    """미리 정리된 manifest.json 이 있으면 그것을 바로 쓰고(가장 빠름),
    없으면 올려둔 캡처를 그때 처리한다."""
    data = load_manifest()
    if data.get("precomputed") and data.get("entries"):
        return {"entries": data["entries"], "problems": [], "total_files": 0, "mode": "precomputed"}
    sig = _capture_signature()
    if [x for x in sig if x[0] != "manual_names.csv"]:
        return _process_captures(sig)
    ents = [e for e in (data.get("entries", []) or [])
            if str(e.get("fused", "")).startswith(("http", "data:")) or (ROOT / str(e.get("fused", ""))).exists()]
    return {"entries": ents, "problems": [], "total_files": 0, "mode": "manifest"}


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

    data = load_entries()
    entries = data["entries"]
    problems = data.get("problems", [])
    if not entries:  # 캡처가 아직 없으면 내장 예시 1문제로 동작
        entries = [dict(FALLBACK, id="000", source="example")]
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
        if problems:
            st.divider()
            st.markdown("**확인이 필요한 캡처 %d장**" % len(problems))
            for f, why in problems[:50]:
                st.caption("· %s — %s" % (f, why))

    key_bridge(bgm)

    # ---------------- 데이터 없음 ----------------
    if n == 0:
        st.markdown("## 포켓몬스터 퓨~~~전 얍!")
        st.warning(
            "아직 퓨전 이미지가 없습니다.\n\n"
            "GitHub 저장소의 `captures` 폴더에 캡처 이미지를 올려주세요. "
            "올리고 1~2분 뒤 이 페이지를 새로고침하면 자동으로 게임에 들어갑니다."
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
        ex = FALLBACK  # 예시는 항상 고정(문제 스포일러 방지)
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
