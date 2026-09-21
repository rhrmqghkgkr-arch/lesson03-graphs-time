import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ============================================================
# 기본 설정
# ============================================================
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data() -> pd.DataFrame:
    """KOBIS 일별 박스오피스 데이터를 불러오고 날짜 열을 datetime으로 변환한다."""
    df = pd.read_csv(DATA_URL, dtype={"날짜": str})
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.caption("KOBIS 일별 박스오피스 TOP10 데이터(1년치)를 시간의 흐름에 따라 살펴봅니다.")

st.divider()

# ============================================================
# 구역 1. 영화별 날짜에 따른 일일 관객수 변화
# ============================================================
st.header("1. 영화별 일일 관객수 변화")

movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list, key="movie_select_1")

movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

fig1 = go.Figure()
fig1.add_trace(
    go.Scatter(
        x=movie_df["날짜"],
        y=movie_df["일관객"],
        mode="lines+markers",
        name=selected_movie,
        line=dict(width=2),
        hovertemplate="날짜: %{x|%Y-%m-%d}<br>일일 관객수: %{y:,}명<extra></extra>",
    )
)
fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일일 관객수(명)",
    hovermode="x unified",
    margin=dict(l=10, r=10, t=30, b=10),
)

st.plotly_chart(fig1, use_container_width=True)

st.text_area(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예) 개봉 직후 관객수가 급등했다가 시간이 지나며 점차 줄어드는 패턴을 보인다.",
    key="insight_1",
)

st.divider()

# ============================================================
# 구역 2. 일관객 합계 상위 5편의 날짜별 일일 관객수 비교
# ============================================================
st.header("2. 누적 일관객 TOP 5 영화 비교")

top5_titles = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).head(5).index.tolist()
)

fig2 = go.Figure()
for title in top5_titles:
    t_df = df[df["영화명"] == title].sort_values("날짜")
    fig2.add_trace(
        go.Scatter(
            x=t_df["날짜"],
            y=t_df["일관객"],
            mode="lines",
            name=title,
            hovertemplate="날짜: %{x|%Y-%m-%d}<br>일일 관객수: %{y:,}명<extra>%{fullData.name}</extra>",
        )
    )

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일일 관객수(명)",
    hovermode="x unified",
    legend_title_text="영화명 (클릭하여 켜고 끄기)",
    margin=dict(l=10, r=10, t=30, b=10),
)

st.plotly_chart(fig2, use_container_width=True)

st.text_area(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예) 상위 5편 중에서도 특정 시기에 관객수가 집중되는 영화가 있고, 흥행 지속 기간에는 큰 차이가 있다.",
    key="insight_2",
)

st.divider()

# ============================================================
# 구역 3. (다음 그래프를 위한 자리 — 추후 추가 예정)
# ============================================================
st.header("3. 다음 그래프")
st.info("이 구역에는 다음 시간 관련 그래프가 추가될 예정입니다.")
