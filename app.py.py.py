import random
from datetime import datetime
import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="간호사 3교대 맞춤형 수면 및 휴식 가이드",
    page_icon="🩺",
    layout="centered",
)

# --- 1. 함수 정의(def): 상단 배너 및 접속 상태 표시 ---
def render_header():
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
            <p style="margin: 10px 0 0 0; font-size: 1.0rem; color: #dbeafe; line-height: 1.5;">
                불규칙한 듀티 속에서도 지치지 않도록, 현재 근무 형태와 휴식 시간을 분석해<br>
                피로 위험도 진단과 딱 맞는 회복 행동 가이드를 처방해 드립니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "connected" not in st.session_state:
        st.session_state.connected = True
        st.session_state.connect_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.toast("🩺 오늘도 고생 많으셨습니다! 수면 가이드 앱에 접속되었습니다.", icon="✨")

    st.caption(f"🟢 **시스템 상태:** 사용자 접속 완료 (접속 시간: {st.session_state.connect_time})")
    st.divider()


# --- 2. 함수 정의(def) & 선택 구조(if/elif/else): 피로도 점수 계산 ---
def calculate_fatigue_score(selected_shift, remaining_hours):
    # 선택 구조 1: 근무 형태에 따른 기본 피로 점수 부여
    if "나이트" in selected_shift:
        base_score = random.randint(55, 68)
    elif "이브닝" in selected_shift:
        base_score = random.randint(42, 58)
    else:
        base_score = random.randint(30, 48)

    # 선택 구조 2: 남은 휴식 시간이 11시간 이하일 경우 가산점 15점 추가
    if remaining_hours <= 11:
        bonus_score = 15
    else:
        bonus_score = 0

    total = base_score + bonus_score

    # 선택 구조 3: 총점에 따른 상태 판정 (위험 / 주의 / 양호)
    if total >= 70:
        status = "위험"
        badge = "🔴"
    elif total >= 50:
        status = "주의"
        badge = "🟡"
    else:
        status = "양호"
        badge = "🟢"

    return total, bonus_score, status, badge


# --- 3. 함수 정의(def) & 리스트 & for 반복문: 맞춤 행동 가이드 테이블 생성 ---
def create_action_guide_table(status):
    # 리스트(list): 3가지 핵심 행동 목록
    core_actions = [
        "수면 안대 착용과 스마트폰 끄기",
        "스트레칭 하기",
        "햇빛받기",
    ]

    # 상태별 세부 가이드 리스트를 담은 딕셔너리
    action_tips = {
        "수면 안대 착용과 스마트폰 끄기": {
            "위험": [
                "암막 커튼과 수면 안대를 즉시 착용하고, 스마트폰은 방 밖에 두어 알림을 완전 차단하세요.",
                "나이트/이브닝 직후 빛 노출을 막기 위해 선글라스 착용 후 귀가하고, 침실 조명을 0%로 낮추세요.",
                "방해 금지 모드를 켜고 귀마개와 수면 안대를 함께 착용해 얕은 잠을 방지하세요.",
            ],
            "주의": [
                "취침 30분 전 스마트폰을 무음 모드로 전환하고 수면 안대로 잔빛을 가려주세요.",
                "블루라이트 차단 모드를 켜고, 침대에 눕기 직전 수면 안대를 착용해 뇌에 수면 신호를 주세요.",
                "알람만 울리도록 설정한 뒤 스마트폰 화면을 뒤집어 두고 안대를 착용하세요.",
            ],
            "양호": [
                "쾌적한 숙면을 위해 가벼운 수면 안대를 착용하고 스마트폰은 머리맡에서 멀리 두세요.",
                "취침 전 15분간 디지털 디톡스를 실천하며 편안한 수면 환경을 만드세요.",
                "은은한 무드등을 끄고 수면 안대를 활용해 깊은 서파 수면 비율을 높여보세요.",
            ],
        },
        "스트레칭 하기": {
            "위험": [
                "장시간 서 있느라 뭉친 종아리와 허리를 위해 누워서 하는 다리 올리기(L자 다리) 10분을 필수로 진행하세요.",
                "무리한 운동은 피하고, 침대 위에서 목·어깨·발목 관절을 천천히 풀어주는 이완 스트레칭만 5분 하세요.",
                "폼롤러나 마사지볼로 발바닥과 승모근의 긴장을 가볍게 풀어준 뒤 바로 누우세요.",
            ],
            "주의": [
                "교대 근무로 긴장된 교감신경을 낮추기 위해 고양이 자세와 허리 비틀기 스트레칭을 10분간 해주세요.",
                "따뜻한 샤워 후 뭉친 종아리 근육을 주물러 주고 가벼운 전신 기지개로 혈액순환을 도우세요.",
                "호흡과 함께 어깨를 크게 돌리고 햄스트링 스트레칭으로 하체 부종을 완화하세요.",
            ],
            "양호": [
                "컨디션 유지를 위해 15분 정도 가벼운 요가나 전신 스트레칭으로 몸의 활력을 깨워보세요.",
                "관절 가동 범위를 넓히는 동적 스트레칭으로 다음 듀티를 위한 체력을 비축하세요.",
                "목과 손목, 발목의 피로를 풀어주는 루틴 스트레칭으로 몸의 균형을 잡아주세요.",
            ],
        },
        "햇빛받기": {
            "위험": [
                "⚠️ 지금은 햇빛을 피해야 합니다! 나이트 퇴근길이라면 선글라스로 햇빛을 차단하고, 기상 직후에만 10분 쬐세요.",
                "수면 직전 햇빛 노출은 멜라토닌을 억제합니다. 완전히 자고 일어난 직후 창가에서 15분간 빛을 보세요.",
                "생체리듬 혼란이 극심한 상태입니다. 기상 후 30분 이내에 햇빛을 쬐어 생체시계를 재설정하세요.",
            ],
            "주의": [
                "기상 후 커튼을 활짝 열고 베란다나 산책로에서 15~20분간 자연광을 쬐어 세로토닌 분비를 유도하세요.",
                "오후 출근 전 20분 정도 가볍게 산책하며 햇빛을 받으면 근무 중 졸음을 줄일 수 있습니다.",
                "실내 조명 대신 낮 시간 동안 창가에서 햇빛을 받으며 수분을 충분히 섭취하세요.",
            ],
            "양호": [
                "야외에서 20~30분간 햇빛을 받으며 가볍게 걸어보세요. 비타민
