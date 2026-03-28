import streamlit as st

def render_dashboard_modules():
    """대시보드 하단 3개 모듈 (플랜 분포, 이탈 사유, 최근 세션) 렌더링"""
    
    st.html('<div class="spacer-2_5"></div>')
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    # Module 1: Plan Distribution
    with col1:
        st.html("""
        <div class="metric-card h-full">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                <div class="icon-badge secondary">
                    <span class="material-symbols-outlined" style="font-size: 1rem;">pie_chart</span>
                </div>
                <h3 style="font-size: 1rem; font-weight: 700; margin: 0;">구독 플랜별 분포</h3>
            </div>
            <div style="display: flex; flex-direction: column; gap: 1.25rem;">
                <!-- Premium -->
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; font-weight: 700; margin-bottom: 0.5rem;">
                        <span style="color: #475569;">Premium (4K)</span>
                        <span style="color: #0f172a;">48%</span>
                    </div>
                    <div style="height: 0.375rem; width: 100%; background-color: #f1f5f9; border-radius: 9999px; overflow: hidden;">
                        <div style="height: 100%; background-color: #b91c1c; width: 48%;"></div>
                    </div>
                </div>
                <!-- Standard -->
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; font-weight: 700; margin-bottom: 0.5rem;">
                        <span style="color: #475569;">Standard (HD)</span>
                        <span style="color: #0f172a;">34%</span>
                    </div>
                    <div style="height: 0.375rem; width: 100%; background-color: #f1f5f9; border-radius: 9999px; overflow: hidden;">
                        <div style="height: 100%; background-color: #2563eb; width: 34%;"></div>
                    </div>
                </div>
                <!-- Basic -->
                <div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; font-weight: 700; margin-bottom: 0.5rem;">
                        <span style="color: #475569;">Basic with Ads</span>
                        <span style="color: #0f172a;">18%</span>
                    </div>
                    <div style="height: 0.375rem; width: 100%; background-color: #f1f5f9; border-radius: 9999px; overflow: hidden;">
                        <div style="height: 100%; background-color: #94a3b8; width: 18%;"></div>
                    </div>
                </div>
            </div>
        </div>
        """)

    # Module 2: Top Churn Reasons
    with col2:
        st.html("""
        <div class="metric-card h-full">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                <div class="icon-badge orange">
                    <span class="material-symbols-outlined" style="font-size: 1rem;">format_list_bulleted</span>
                </div>
                <h3 style="font-size: 1rem; font-weight: 700; margin: 0;">주요 이탈 사유</h3>
            </div>
            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background-color: #f8fafc; border-radius: 0.5rem;">
                    <span style="font-size: 0.6875rem; font-weight: 700; color: #475569;">보고 싶은 콘텐츠 부족</span>
                    <span style="font-size: 0.75rem; font-weight: 900; color: #b91c1c;">32%</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background-color: #f8fafc; border-radius: 0.5rem;">
                    <span style="font-size: 0.6875rem; font-weight: 700; color: #475569;">가격 부담 (구독료)</span>
                    <span style="font-size: 0.75rem; font-weight: 900; color: #b91c1c;">28%</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background-color: #f8fafc; border-radius: 0.5rem;">
                    <span style="font-size: 0.6875rem; font-weight: 700; color: #475569;">타 서비스 이동</span>
                    <span style="font-size: 0.75rem; font-weight: 900; color: #b91c1c;">22%</span>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem; background-color: #f8fafc; border-radius: 0.5rem;">
                    <span style="font-size: 0.6875rem; font-weight: 700; color: #475569;">사용 빈도 감소</span>
                    <span style="font-size: 0.75rem; font-weight: 900; color: #b91c1c;">18%</span>
                </div>
            </div>
        </div>
        """)

    # Module 3: Recent Analysis Sessions
    with col3:
        st.html("""
        <div class="metric-card h-full">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 1.5rem;">
                <div class="icon-badge tertiary">
                    <span class="material-symbols-outlined" style="font-size: 1rem;">history</span>
                </div>
                <h3 style="font-size: 1rem; font-weight: 700; margin: 0;">최근 분석 세션</h3>
            </div>
            <div style="display: flex; flex-direction: column; gap: 1.25rem;">
                <div style="display: flex; gap: 0.75rem; align-items: flex-start;">
                    <div style="width: 0.5rem; height: 0.5rem; margin-top: 0.375rem; border-radius: 9999px; background-color: #22c55e; flex-shrink: 0;"></div>
                    <div>
                        <p style="font-size: 0.75rem; font-weight: 700; color: #1e293b; margin: 0 0 0.25rem 0;">APAC 지역 이탈 패턴 분석 완료</p>
                        <p style="font-size: 0.5625rem; font-weight: 500; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">5분 전 • AI Agent Alpha</p>
                    </div>
                </div>
                <div style="display: flex; gap: 0.75rem; align-items: flex-start;">
                    <div style="width: 0.5rem; height: 0.5rem; margin-top: 0.375rem; border-radius: 9999px; background-color: #f97316; flex-shrink: 0;"></div>
                    <div>
                        <p style="font-size: 0.75rem; font-weight: 700; color: #1e293b; margin: 0 0 0.25rem 0;">광고 요금제 전환율 감소 감지</p>
                        <p style="font-size: 0.5625rem; font-weight: 500; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">2시간 전 • Batch #402</p>
                    </div>
                </div>
                <div style="display: flex; gap: 0.75rem; align-items: flex-start;">
                    <div style="width: 0.5rem; height: 0.5rem; margin-top: 0.375rem; border-radius: 9999px; background-color: #3b82f6; flex-shrink: 0;"></div>
                    <div>
                        <p style="font-size: 0.75rem; font-weight: 700; color: #1e293b; margin: 0 0 0.25rem 0;">분기별 리텐션 보고서 생성</p>
                        <p style="font-size: 0.5625rem; font-weight: 500; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin: 0;">4시간 전 • System Admin</p>
                    </div>
                </div>
            </div>
        </div>
        """)
