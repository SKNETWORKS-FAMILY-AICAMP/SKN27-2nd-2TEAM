import pandas as pd

def _safe_mode(series: pd.Series):
    """범주형 집계 시 최빈값(없으면 NA) 반환."""
    mode_values = series.mode(dropna=True)
    if mode_values.empty:
        return pd.NA
    return mode_values.iloc[0]


def _aggregate_by_user(df: pd.DataFrame, prefix: str) -> pd.DataFrame:
    """이벤트 테이블을 user_id 기준 1행으로 집계."""
    if df.empty:
        return pd.DataFrame(columns=["user_id"])

    work_df = df.copy()
    agg_map = {}

    # 날짜/시간 정보는 최근 이벤트(max) 기준으로 집계한다.
    for col in work_df.columns:
        if col == "user_id":
            continue
        if "date" in col.lower() or "time" in col.lower():
            agg_map[col] = "max"

    # 수치형은 평균(기본), 이벤트량 성격 컬럼은 합계로 집계한다.
    numeric_cols = [
        col for col in work_df.select_dtypes(include=["number", "bool"]).columns
        if col != "user_id"
    ]
    sum_keywords = ("count", "duration", "votes", "results", "sessions")
    for col in numeric_cols:
        if col in agg_map:
            continue
        if any(key in col.lower() for key in sum_keywords):
            agg_map[col] = "sum"
        else:
            agg_map[col] = "mean"

    # 범주형/문자형은 최빈값으로 대표값을 만든다.
    object_cols = [
        col for col in work_df.select_dtypes(include=["object", "category"]).columns
        if col != "user_id" and col not in agg_map
    ]
    for col in object_cols:
        agg_map[col] = _safe_mode

    aggregated = work_df.groupby("user_id", as_index=False).agg(agg_map)
    aggregated = aggregated.rename(
        columns={col: f"{prefix}_{col}" for col in aggregated.columns if col != "user_id"}
    )
    aggregated[f"{prefix}_event_count"] = work_df.groupby("user_id")["user_id"].size().values
    return aggregated


def merge_all_data(
    user: pd.DataFrame,
    watch: pd.DataFrame,
    movies: pd.DataFrame,
    rec_logs: pd.DataFrame,
    search_logs: pd.DataFrame,
    reviews: pd.DataFrame,
) -> pd.DataFrame:
    """users를 기준으로 각 로그 테이블을 user_id 집계 후 병합한다."""
    # watch 로그에 영화 메타데이터를 붙여 user 시청 행위를 풍부하게 만든다.
    watch_movies = watch.merge(movies, on="movie_id", how="left")

    # 중복 user_id를 각 테이블 내부에서 먼저 통합한다.
    agg_watch = _aggregate_by_user(watch_movies, "watch")
    agg_rec = _aggregate_by_user(rec_logs, "rec")
    agg_search = _aggregate_by_user(search_logs, "search")
    agg_review = _aggregate_by_user(reviews, "review")

    # users를 기준으로 left merge 하여 "1 user = 1 row" 형태를 보장한다.
    netflix = user.copy()
    for agg_df in [agg_watch, agg_rec, agg_search, agg_review]:
        netflix = netflix.merge(agg_df, on="user_id", how="left")

    if len(netflix) != len(user):
        raise ValueError("병합 결과 행 수가 users 기준 행 수와 다릅니다.")

    return netflix