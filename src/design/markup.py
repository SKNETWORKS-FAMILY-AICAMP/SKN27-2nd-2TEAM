"""
Streamlit `st.html`에 넣는 HTML 문자열 조립.

- 공통 레이아웃은 여기서 인라인 스타일·클래스명을 맞추고, 색·타이포 토큰은 `common.COLORS` 및
  `get_*_css()`의 클래스(`.metric-card`, `.chart-card` 등)와 짝을 이룹니다.
- 표시 문구는 `ui_config.json`·`dashboard_modules.json`에서 넘기고, 사용자 입력값은 `_safe()`로 이스케이프합니다.
"""
from __future__ import annotations

import html
import re
from textwrap import dedent

from src.design.common import COLORS


def _safe(s: str) -> str:
    """텍스트를 HTML에 삽입하기 전 이스케이프 (XSS·깨짐 방지)."""
    return html.escape(str(s), quote=True)


def _safe_hex_color(value: str, *, fallback: str = "#94a3b8") -> str:
    """`style`에 넣는 배경색만 허용 (#RRGGBB). 그 외 값은 fallback으로 대체."""
    if isinstance(value, str) and re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        return value
    return fallback


def page_header_simple(title: str, description: str) -> str:
    """Home 등: 제목·설명만 (`common`의 `.page-header` 스타일 사용)."""
    return dedent(f"""
        <div class="page-header">
            <h2 class="page-title">{_safe(title)}</h2>
            <p class="page-description">{_safe(description)}</p>
        </div>
    """).strip()


def page_header_analysis(
    title: str,
    description: str,
    *,
    header_icon: str = "analytics",
) -> str:
    """분석 화면: 제목 앞에 머티리얼 아이콘 + primary 색 인라인."""
    return dedent(f"""
        <div class="page-header">
            <h2 class="page-title">
                <span class="material-symbols-outlined" style="font-size: 2rem; color: {COLORS['primary']};">{_safe(header_icon)}</span>
                {_safe(title)}
            </h2>
            <p class="page-description">{_safe(description)}</p>
        </div>
    """).strip()


def spacer_std() -> str:
    """섹션 간 여백 (`common`의 `.spacer-2_5` 높이)."""
    return '<div class="spacer-2_5"></div>'


def spacer_analysis_segment() -> str:
    """세그먼트 선택 아래 등, 조금 낮은 구간 스페이서."""
    return '<div class="spacer-2_5" style="height: 1.5rem;"></div>'


def spacer_height(height: str) -> str:
    """빈 `div`로 고정 높이만 확보 (폼·2열 정렬용)."""
    return f'<div style="height: {height};"></div>'


def sidebar_header(title: str, subtitle: str) -> str:
    """사이드바 상단 브랜딩 (`get_sidebar_css`의 `.sidebar-header`·타이틀과 짝)."""
    return dedent(f"""
        <div class="sidebar-header">
            <h1 class="sidebar-title">{_safe(title)}</h1>
            <p class="sidebar-subtitle">{_safe(subtitle)}</p>
        </div>
    """).strip()


def sidebar_spacer() -> str:
    """사이드바 하단 영역을 밀어 올리는 플렉스용 빈 블록."""
    return '<div class="sidebar-spacer"></div>'


def chart_trend_header(icon_material_name: str, title: str) -> str:
    """메인 트렌드 차트 위 제목 줄 (`get_charts_css`의 `.chart-header`·`.chart-icon-box`)."""
    return dedent(f"""
        <div class="chart-header">
            <div class="chart-title-wrapper">
                <div class="chart-icon-box">
                    <span class="material-symbols-outlined">{_safe(icon_material_name)}</span>
                </div>
                <h3 class="chart-title">{_safe(title)}</h3>
            </div>
        </div>
    """).strip()


def metric_card_html(
    icon_name: str,
    icon_style_class: str,
    title: str,
    value: str,
    change_text: str,
    *,
    is_positive: bool = True,
    emoji: str = "",
) -> str:
    """대시보드 상단 KPI 4칸 (`get_metrics_css`의 `.metric-card`·`.change-tag`)."""
    change_class = "positive" if is_positive else "negative"
    em = _safe(emoji) if emoji else ""
    return dedent(f"""
        <div class="metric-card h-full">
            <div class="metric-card-header">
                <span class="icon-badge {icon_style_class}">
                    <span class="material-symbols-outlined">{_safe(icon_name)}</span>
                </span>
                <span class="change-tag {change_class}">{_safe(change_text)}</span>
            </div>
            <div>
                <p class="metric-card-title">{_safe(title)}</p>
                <p class="metric-card-value">{_safe(value)} <span class="metric-card-emoji">{em}</span></p>
            </div>
        </div>
    """).strip()


def analysis_form_section_title(icon_name: str, title: str) -> str:
    """분석 좌측 열: 시뮬레이터 폼 위 ‘파라미터 조정’ 제목 행 (인라인 flex)."""
    return dedent(f"""
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                <div class="icon-badge primary">
                    <span class="material-symbols-outlined" style="font-size: 1rem;">{_safe(icon_name)}</span>
                </div>
                <h3 style="font-size: 1.125rem; font-weight: 700; margin: 0;">{_safe(title)}</h3>
            </div>
            """).strip()


def analysis_kpi_current_card(
    current_prob: float,
    *,
    kpi_label: str,
    badge_current: str,
) -> str:
    """우측 열: 베이스라인 이탈율 카드 (회색 좌측 보더·Current 뱃지)."""
    return dedent(f"""
            <div class="metric-card" style="border-left: 4px solid #e2e8f0; padding: 1rem;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                        <span style="padding: 0.35rem; background-color: #f1f5f9; border-radius: 0.5rem; color: #94a3b8; display: inline-flex; font-size: 1rem;">
                            <span class="material-symbols-outlined" style="font-size: 1.1rem;">trending_flat</span>
                        </span>
                        <span style="font-size: 0.65rem; font-weight: 700; color: #94a3b8; background-color: #f8fafc; padding: 0.2rem 0.45rem; border-radius: 0.25rem;">{_safe(badge_current)}</span>
                    </div>
                    <p style="font-size: 0.55rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 0.15rem 0;">{_safe(kpi_label)}</p>
                    <p style="font-size: 1.4rem; font-weight: 900; color: #0f172a; margin: 0; line-height: 1.2;">{current_prob}%</p>
                </div>
            </div>
            """).strip()


def analysis_kpi_simulated_card(
    projected_prob: float,
    *,
    kpi_label: str,
    trend_icon: str,
    delta_text: str,
    delta_color: str,
    delta_bg: str,
) -> str:
    """우측 열: 시뮬 결과 이탈율 카드 (primary 좌측 보더·델타 뱃지·트렌드 아이콘)."""
    dc = _safe_hex_color(delta_color, fallback="#dc2626")
    dbg = _safe_hex_color(delta_bg, fallback="#fef2f2")
    return dedent(f"""
            <div class="metric-card" style="border-left: 4px solid {COLORS['primary']}; padding: 1rem;">
                <div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
                        <span style="padding: 0.35rem; background-color: {COLORS['primary_light']}; border-radius: 0.5rem; color: {COLORS['primary']}; display: inline-flex;">
                            <span class="material-symbols-outlined" style="font-size: 1.1rem;">{_safe(trend_icon)}</span>
                        </span>
                        <span style="font-size: 0.65rem; font-weight: 700; color: {dc}; background-color: {dbg}; padding: 0.2rem 0.45rem; border-radius: 0.25rem;">{_safe(delta_text)}</span>
                    </div>
                    <p style="font-size: 0.55rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; margin: 0 0 0.15rem 0;">{_safe(kpi_label)}</p>
                    <p style="font-size: 1.4rem; font-weight: 900; color: {COLORS['primary']}; margin: 0; line-height: 1.2;">{projected_prob}%</p>
                </div>
            </div>
            """).strip()


def analysis_ai_comment_card(
    *,
    segment_name: str,
    projected_prob: float,
    risk_text: str,
    title: str,
    summary_template: str,
    is_high_risk: bool,
) -> str:
    """요약 문단 (`chart-card` 박스 + 위험도별 아이콘·배경 톤)."""
    summary = summary_template.format(
        segment=_safe(segment_name),
        projected=_safe(f"{projected_prob}%"),
    )
    badge = "primary" if is_high_risk else "positive"
    bg = "#fef2f2" if is_high_risk else "#f0fdf4"
    risk_color = "#dc2626" if is_high_risk else "#16a34a"
    risk_icon = "warning" if is_high_risk else "check_circle"
    return dedent(f"""
        <div class="chart-card" style="padding: 1rem 1.25rem;">
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.75rem;">
                <div class="icon-badge {badge}" style="background-color: {bg}; color: {risk_color};">
                    <span class="material-symbols-outlined" style="font-size: 0.95rem;">{risk_icon}</span>
                </div>
                <h3 style="font-size: 0.98rem; font-weight: 700; margin: 0;">{_safe(title)}</h3>
            </div>
            <p style="color: #475569; font-size: 0.75rem; line-height: 1.55; margin: 0;">
                {summary}
                <br><br>
                {_safe(risk_text)}
            </p>
        </div>
        """).strip()


def _dashboard_module_title_row(icon_badge: str, icon_name: str, title: str) -> str:
    """하단 3모듈 공통: 아이콘 배지 + 모듈 제목 한 줄."""
    return dedent(f"""
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                <div class="icon-badge {icon_badge}">
                    <span class="material-symbols-outlined" style="font-size: 1rem;">{_safe(icon_name)}</span>
                </div>
                <h3 style="font-size: 1rem; font-weight: 700; margin: 0;">{_safe(title)}</h3>
            </div>
            """).strip()


def dashboard_plan_module(payload: dict) -> str:
    """플랜 분포: 가로 막대(퍼센트 폭) 리스트 (`dashboard_modules.json` plan_distribution)."""
    rows_html = []
    for r in payload["rows"]:
        pct = int(r["pct"])
        bc = _safe_hex_color(r["bar_color"])
        lbl = _safe(r["label"])
        rows_html.append(
            dedent(f"""
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; font-weight: 700; margin-bottom: 0.5rem;">
                        <span style="color: #475569;">{lbl}</span>
                        <span style="color: #0f172a;">{pct}%</span>
                    </div>
                    <div style="height: 0.375rem; width: 100%; background-color: #f1f5f9; border-radius: 9999px; overflow: hidden;">
                        <div style="height: 100%; background-color: {bc}; width: {pct}%;"></div>
                    </div>
                </div>
            """).strip()
        )
    header = _dashboard_module_title_row(
        payload["icon_badge"], payload["icon"], payload["title"]
    )
    return dedent(f"""
        <div class="metric-card h-full">
            {header}
            <div style="display: flex; flex-direction: column; gap: 1.25rem;">
                {"".join(rows_html)}
            </div>
        </div>
    """).strip()


def dashboard_churn_reasons_module(payload: dict) -> str:
    """이탈 사유: 슬레이트 배경 행 + 우측 강조 퍼센트."""
    rows_html = []
    for r in payload["rows"]:
        rows_html.append(
            dedent(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background-color: #f8fafc; border-radius: 0.5rem;">
                    <span style="font-size: 0.6875rem; font-weight: 700; color: #475569;">{_safe(r["label"])}</span>
                    <span style="font-size: 0.75rem; font-weight: 900; color: #b91c1c;">{_safe(r["value"])}</span>
                </div>
            """).strip()
        )
    header = _dashboard_module_title_row(
        payload["icon_badge"], payload["icon"], payload["title"]
    )
    return dedent(f"""
        <div class="metric-card h-full">
            {header}
            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                {"".join(rows_html)}
            </div>
        </div>
    """).strip()


def dashboard_sessions_module(payload: dict) -> str:
    """최근 세션: 컬러 도트 + 제목·메타 텍스트 타임라인."""
    rows_html = []
    for r in payload["rows"]:
        dc = _safe_hex_color(r["dot_color"])
        rows_html.append(
            dedent(f"""
                <div style="display: flex; gap: 0.75rem; align-items: flex-start;">
                    <div style="width: 0.5rem; height: 0.5rem; margin-top: 0.375rem; border-radius: 9999px; background-color: {dc}; flex-shrink: 0;"></div>
                    <div>
                        <p style="font-size: 0.75rem; font-weight: 700; color: #1e293b; margin: 0 0 0.25rem 0;">{_safe(r["title"])}</p>
                        <p style="font-size: 0.5625rem; font-weight: 500; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">{_safe(r["meta"])}</p>
                    </div>
                </div>
            """).strip()
        )
    header = _dashboard_module_title_row(
        payload["icon_badge"], payload["icon"], payload["title"]
    )
    return dedent(f"""
        <div class="metric-card h-full">
            {header}
            <div style="display: flex; flex-direction: column; gap: 1.25rem;">
                {"".join(rows_html)}
            </div>
        </div>
    """).strip()
