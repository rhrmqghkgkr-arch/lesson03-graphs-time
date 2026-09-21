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
# 구역 3. 날짜별 TOP10 일관객 합계
# ============================================================
st.header("3. 날짜별 박스오피스 TOP10 일관객 합계")

daily_total = df.groupby("날짜")["일관객"].sum().reset_index()
top3_days = daily_total.sort_values("일관객", ascending=False).head(3)

fig3 = go.Figure()
fig3.add_trace(
    go.Scatter(
        x=daily_total["날짜"],
        y=daily_total["일관객"],
        mode="lines",
        fill="tozeroy",
        name="TOP10 일관객 합계",
        hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 관객수: %{y:,}명<extra></extra>",
    )
)

# 합계가 가장 컸던 3일 표시
fig3.add_trace(
    go.Scatter(
        x=top3_days["날짜"],
        y=top3_days["일관객"],
        mode="markers",
        marker=dict(size=10, color="crimson"),
        name="합계 TOP 3일",
        hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계 관객수: %{y:,}명<extra></extra>",
        showlegend=True,
    )
)

for _, row in top3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=row["날짜"].strftime("%Y-%m-%d"),
        showarrow=True,
        arrowhead=2,
        yshift=10,
    )

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="TOP10 일관객 합계(명)",
    hovermode="x unified",
    margin=dict(l=10, r=10, t=30, b=10),
)

st.plotly_chart(fig3, use_container_width=True)

st.text_area(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예) 대작 영화들이 동시에 개봉하거나 연휴와 겹치는 날짜에 전체 관객수가 급증한다.",
    key="insight_3",
)

st.divider()

# ============================================================
# 구역 4. 누적 일관객 TOP 10 영화
# ============================================================
st.header("4. 누적 일관객 TOP 10 영화")

movie_summary = (
    df.groupby("영화명")
    .agg(합계관객=("일관객", "sum"), 순위진입일수=("영화명", "count"))
    .reset_index()
)
top10_movies = movie_summary.sort_values("합계관객", ascending=False).head(10)
# 관객이 많은 영화가 위로 오도록 오름차순으로 정렬해 그린다
top10_movies = top10_movies.sort_values("합계관객", ascending=True)

fig4 = go.Figure()
fig4.add_trace(
    go.Bar(
        x=top10_movies["합계관객"],
        y=top10_movies["영화명"],
        orientation="h",
        customdata=top10_movies["순위진입일수"],
        hovertemplate=(
            "영화: %{y}<br>"
            "합계 관객수: %{x:,}명<br>"
            "TOP10 진입 일수: %{customdata}일<extra></extra>"
        ),
    )
)

fig4.update_layout(
    xaxis_title="합계 관객수(명)",
    yaxis_title="영화명",
    margin=dict(l=10, r=10, t=30, b=10),
)

st.plotly_chart(fig4, use_container_width=True)

st.text_area(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예) 상위권 영화라고 해서 반드시 TOP10 진입 일수가 긴 것은 아니며, 짧은 기간 폭발적으로 흥행한 영화도 있다.",
    key="insight_4",
)

st.divider()

# ============================================================
# 구역 5. 월 × 요일별 일관객 합계 히트맵
# ============================================================
st.header("5. 월 × 요일별 일관객 합계")

weekday_order = ["월", "화", "수", "목", "금", "토", "일"]
weekday_map = dict(zip(range(7), weekday_order))

heat_df = df.copy()
heat_df["월"] = heat_df["날짜"].dt.month
heat_df["요일"] = heat_df["날짜"].dt.dayofweek.map(weekday_map)

pivot = (
    heat_df.groupby(["요일", "월"])["일관객"]
    .sum()
    .unstack("월")
    .reindex(index=weekday_order)
    .sort_index(axis=1)
)

fig5 = go.Figure(
    data=go.Heatmap(
        z=pivot.values,
        x=[f"{m}월" for m in pivot.columns],
        y=pivot.index,
        colorscale="YlOrRd",
        hovertemplate="%{x} %{y}요일<br>합계 관객수: %{z:,}명<extra></extra>",
        colorbar=dict(title="합계<br>관객수"),
    )
)

fig5.update_layout(
    xaxis_title="월",
    yaxis_title="요일",
    margin=dict(l=10, r=10, t=30, b=10),
)

st.plotly_chart(fig5, use_container_width=True)

st.text_area(
    "📝 이 그래프로 알 수 있는 것",
    placeholder="예) 주말(금~일)에 관객수가 뚜렷하게 높고, 특정 월에는 대작 개봉 효과로 평일에도 관객수가 높게 나타난다.",
    key="insight_5",
)

st.divider()

# ============================================================
# 구역 6. (다음 그래프를 위한 자리 — 추후 추가 예정)
# ============================================================
st.header("6. 다음 그래프")
st.info("이 구역에는 다음 시간 관련 그래프가 추가될 예정입니다.")
