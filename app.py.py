import random
from datetime import datetime
import pandas as pd
import streamlit as st

# 1. [리스트] 근무 형태 및 핵심 행동 리스트 정의
SHIFT_LIST = [
    "데이 (Day / 07:00 ~ 15:00)",
    "이브닝 (Evening / 15:00 ~ 23:00)",
    "나이트 (Night / 23:00 ~ 07:00)",
]

ACTION_LIST = [
    "수면 안대 착용과 스마트폰 끄기",
    "스트레칭 하기",
    "햇빛받기",
]

# 행동별·상태별 세부 가이드 데이터
ACTION_TIPS = {
    "수면 안대 착용과 스마트폰 끄기": {
        "위험": [
            "암막 커튼과 수면 안대를 즉시 착용하고, 스마트폰은 방 밖에 두어 알림을 완전 차단하세요.",
            "방해 금지 모드를 켜고 귀마개와 수면 안대를 함께 착용해 얕은 잠을 방지하세요.",
        ],
        "주의": [
            "취침 30분 전 스마트폰을 무음 모드로 전환하고 수면 안대로 잔빛을 가려주세요.",
            "블루라이트 차단 모드를 켜고, 침대에 눕기 직전 수면 안대를 착용해 수면 신호를 주세요.",
        ],
        "양호": [
            "쾌적한 숙면을 위해 가벼운 수면 안대를 착용하고 스마트폰은 머리맡에서 멀리 두세요.",
            "취침 전 15분간 디지털 디톡스를 실천하며 편안한 수면 환경을 만드세요.",
        ],
    },
    "스트레칭 하기": {
        "위험": [
            "장시간 서 있느라 뭉친 종아리와 허리를 위해 누워서 하는 L자 다리 자세를 10분간 진행하세요.",
            "무리한 운동은 피하고, 침대 위에서 목·어깨·발목 관절을 천천히 풀어주는 이완 스트레칭만 5분 하세요.",
        ],
        "주의": [
            "교대 근무로 긴장된 교감신경을 낮추기 위해 고양이 자세와 허리 비틀기 스트레칭을 10분간 해주세요.",
            "따뜻한 샤워 후 뭉친 종아리 근육을 주물러 주고 가벼운 전신 기지개로 혈액순환을 도우세요.",
        ],
        "양호": [
            "컨디션 유지를 위해 15분 정도 가벼운 요가나 전신 스트레칭으로 몸의 활력을 깨워보세요.",
            "목과 손목, 발목의 피로를 풀어주는 루틴 스트레칭으로 몸의 균형을 잡아주세요.",
        ],
    },
    "햇빛받기": {
        "위험": [
            "⚠️ 지금은 햇빛을 피해야 합니다! 퇴근길 선글라스로 빛을 차단하고, 자고 일어난 직후에만 10분 쬐세요.",
            "생체리듬 혼란이 극심한 상태입니다. 완전히 기상한 후 30분 이내에 창가에서 15분간 빛을 보세요.",
        ],
        "주의": [
            "기상 후 커튼을 활짝 열고 베란다나 산책로에서 15~20분간 자연광을 쬐어 세로토닌 분비를 유도하세요.",
            "오후 출근 전 20분 정도 가볍게 산책하며 햇빛을 받으면 근무 중 졸음을 줄일 수 있습니다.",
        ],
        "양호": [
            "야외에서 20~30분간 햇빛을 받으며 가볍게 걸어보세요. 비타민 D 합성과 생체리듬 유지에 최고입니다.",
            "맑은 공기와 함께 햇빛을 쬐며 기분 전환을 하고 최상의 컨디션을 유지하세요.",
        ],
    },
}


# 2. [함수 정의(def) & 선택구조(if-elif-else)] 피로 점수 계산 및 상태 판정 함수
def evaluate_fatigue(selected_shift, remaining_hours):
    # 근무 형태에 따른 기본 점수 부여 (선택 구조 1)
    if "나이트" in selected_shift:
        base_score = random.randint(55, 68)
    elif "이브닝" in selected_shift:
        base_score = random.randint(42, 58)
    else:
        base_score = random.randint(30, 48)

    # 남은 휴식 시간이 11시간 이하일 경우 가산점 15점 추가 (선택 구조 2)
    if remaining_hours <= 11:
        bonus_score = 15
    else:
        bonus_score = 0

    total_score = base_score + bonus_score

    # 총점에 따른 위험도 상태 판정 (선택 구조 3)
    if total_score >= 70:
        status = "위험"
        icon = "🔴"
    elif total_score >= 50:
        status = "주의"
        icon = "🟡"
    else:
        status = "양호"
        icon = "🟢"

    return total_score, bonus_score, status, icon


# 3. [함수 정의(def) & for 반복문] 행동 가이드 테이블 데이터 생성 함수
def create_guide_table(status):
    guide_rows = []  # 결과를 담을 빈 리스트

    # 핵심 행동 리스트를 순회하며 맞춤 가이드 추출 (for 구문)
    for index, action in enumerate(ACTION_LIST, start=1):
        selected_tip = random.choice(ACTION_TIPS[action][status])
        guide_rows.append(
            {
                "순서": f"{index}단계",
                "핵심 행동": action,
                f"맞춤 실행 가이드 ({status} 단계)": selected_tip,
            }
        )

    return pd.DataFrame(guide_rows)


# 4. [함수 정의(def)] 메인 웹앱 UI 실행 함수
def main():
    st.set_page_config(
        page_title="간호사 3교대 맞춤형 수면·휴식 가이드",
        page_icon="🩺",
        layout="centered",
    )

    # 상단 그라데이션 배너
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #2563eb 100%);
            padding: 30px 24px;
            border-radius: 16px;
            color: white;
            text-align: center;
            margin-bottom: 16px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        ">
            <h1 style="margin: 0; font-size: 1.9rem; font-weight: 700;">
                🩺 간호사 3교대 맞춤형 수면·휴식 가이드
            </h1>
            <p style="margin: 10px 0 0 0; font-
