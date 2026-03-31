import pandas as pd
from IPython.display import display

# ─────────────────────────────────────────
# 1. 데이터 기본 정보 확인
# ─────────────────────────────────────────
def check_data_info(Netflix: pd.DataFrame) -> None:
    """데이터 크기, 상위 행, 컬럼 정보 출력"""
    print(f"데이터셋 모양: {Netflix.shape}")
    display(Netflix.head())
    Netflix.info()


# ─────────────────────────────────────────
# 1-1. 컬럼별 결측치 프로파일링
# ─────────────────────────────────────────
def _recommend_missing_strategy(dtype_name: str, missing_rate: float) -> str:
    """dtype + 결측비율 기반 처리 전략 후보를 제안한다."""
    if missing_rate == 0:
        return "keep(no_missing)"
    if missing_rate > 0.40:
        return "drop_candidate(high_missing)"

    numeric_markers = ("int", "float", "bool")
    if any(marker in dtype_name.lower() for marker in numeric_markers):
        if missing_rate < 0.05:
            return "median_impute"
        if missing_rate < 0.30:
            return "group_median_or_median"
        return "zero_or_group_median"

    if missing_rate < 0.05:
        return "mode_impute"
    if missing_rate < 0.30:
        return "mode_or_unknown"
    return "unknown_label_or_drop"


def profile_missing_values(df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
    """컬럼별 결측치 현황과 전략 후보를 DataFrame으로 반환/출력."""
    total_rows = len(df)
    missing_count = df.isnull().sum()

    profile = pd.DataFrame({
        "column": df.columns,
        "missing_count": missing_count.values,
        "missing_rate": (missing_count / total_rows).values,
        "dtype": [str(dtype) for dtype in df.dtypes.values],
        "nunique": df.nunique(dropna=True).values,
    }).sort_values(by=["missing_rate", "missing_count"], ascending=False)

    # 결측 구간을 명시해 컬럼군별 처리 우선순위를 빠르게 확인한다.
    profile["missing_bucket"] = pd.cut(
        profile["missing_rate"],
        bins=[-1e-9, 0, 0.05, 0.30, 1.0],
        labels=["0%", "(0%,5%)", "[5%,30%]", ">30%"],
    )

    profile["strategy_candidate"] = profile.apply(
        lambda row: _recommend_missing_strategy(row["dtype"], float(row["missing_rate"])),
        axis=1,
    )

    zero_cnt = int((profile["missing_rate"] == 0).sum())
    low_cnt = int(((profile["missing_rate"] > 0) & (profile["missing_rate"] < 0.05)).sum())
    mid_cnt = int(((profile["missing_rate"] >= 0.05) & (profile["missing_rate"] <= 0.30)).sum())
    high_cnt = int((profile["missing_rate"] > 0.30).sum())

    print("=== 결측치 구간 요약 ===")
    print(f"0%: {zero_cnt}개 컬럼")
    print(f"(0%, 5%): {low_cnt}개 컬럼")
    print(f"[5%, 30%]: {mid_cnt}개 컬럼")
    print(f">30%: {high_cnt}개 컬럼")

    display_cols = [
        "column",
        "missing_count",
        "missing_rate",
        "missing_bucket",
        "dtype",
        "nunique",
        "strategy_candidate",
    ]
    display(profile[display_cols].head(top_n))
    return profile


# ─────────────────────────────────────────
# 2. 불필요한 컬럼 제거
# ─────────────────────────────────────────
def drop_columns(train: pd.DataFrame, test: pd.DataFrame) -> pd.Series:
    """제출용 user_id 저장 후 불필요한 컬럼 제거."""
    # 후속 submission 저장을 위해 test의 user_id를 보존한다.
    test_user_id = test['user_id'].copy()

    print(f'before: {train.shape} / {test.shape}')

    drop_cols = ['user_id', 'email', 'first_name', 'last_name',
                'created_at', 'country', 'state_province', 'city']

    for df in [train, test]:
        df.drop(columns=drop_cols, axis=1, inplace=True)

    print(f'after: {train.shape} / {test.shape}')
    train.info()

    return test_user_id


# ─────────────────────────────────────────
# 2-1. 인코딩 직전 전처리(날짜 분해 / ID 제거 / 검증)
# ─────────────────────────────────────────
def split_date_columns(train: pd.DataFrame, test: pd.DataFrame) -> list:
    """*_date, *_at 컬럼을 year/month/day로 분해하고 원본을 제거한다."""
    date_cols = [
        col for col in train.columns
        if (col.endswith("_date") or col.endswith("_at")) and col in test.columns
    ]
    created_cols = []

    for col in date_cols:
        tr_raw = train[col]
        te_raw = test[col]
        tr_dt = pd.to_datetime(tr_raw, errors="coerce")
        te_dt = pd.to_datetime(te_raw, errors="coerce")

        # 결측이 아닌 값 중 파싱 실패가 있으면 인코딩 전 즉시 중단한다.
        tr_invalid = int((tr_raw.notna() & tr_dt.isna()).sum())
        te_invalid = int((te_raw.notna() & te_dt.isna()).sum())
        if tr_invalid or te_invalid:
            raise ValueError(
                f"[pre-encode fail] date parse 실패: {col} (train={tr_invalid}, test={te_invalid})"
            )

        for df, dt in [(train, tr_dt), (test, te_dt)]:
            df[f"{col}_year"] = dt.dt.year.astype("Int64")
            df[f"{col}_month"] = dt.dt.month.astype("Int64")
            df[f"{col}_day"] = dt.dt.day.astype("Int64")

        created_cols.extend([f"{col}_year", f"{col}_month", f"{col}_day"])

    for df in [train, test]:
        df.drop(columns=date_cols, inplace=True, errors="ignore")

    print(f"date columns split: {len(date_cols)} -> created {len(created_cols)}")
    return date_cols


def drop_id_like_columns(train: pd.DataFrame, test: pd.DataFrame) -> list:
    """ID성 고유값 컬럼(user_id/email/*_id)을 제거한다."""
    id_like_cols = []
    for col in train.columns:
        if col not in test.columns:
            continue
        lower_col = col.lower()
        if lower_col == "user_id" or lower_col == "email" or lower_col.endswith("_id"):
            id_like_cols.append(col)

    for df in [train, test]:
        df.drop(columns=id_like_cols, inplace=True, errors="ignore")

    print(f"id-like columns dropped: {id_like_cols}")
    return id_like_cols


def convert_non_numeric_to_category(train: pd.DataFrame, test: pd.DataFrame) -> list:
    """숫자형이 아닌 공통 컬럼을 모두 category dtype으로 변환한다."""
    converted_cols = []
    for col in train.columns:
        if col not in test.columns:
            continue
        if (not pd.api.types.is_numeric_dtype(train[col])) or (not pd.api.types.is_numeric_dtype(test[col])):
            tr_series = train[col].astype("string")
            te_series = test[col].astype("string")
            categories = sorted(
                pd.concat([tr_series, te_series], axis=0).dropna().astype(str).unique().tolist()
            )
            cat_dtype = pd.CategoricalDtype(categories=categories)
            train[col] = tr_series.astype(cat_dtype)
            test[col] = te_series.astype(cat_dtype)
            converted_cols.append(col)

    print(f"converted to category ({len(converted_cols)}): {converted_cols}")
    return converted_cols


def validate_before_encoding(train: pd.DataFrame, test: pd.DataFrame) -> None:
    """인코딩 직전 필수 검증 게이트(실패 시 즉시 중단)."""
    if list(train.columns) != list(test.columns):
        raise ValueError("[pre-encode fail] train/test 컬럼 구성이 다릅니다.")

    remain_date_cols = [c for c in train.columns if c.endswith("_date") or c.endswith("_at")]
    if remain_date_cols:
        raise ValueError(f"[pre-encode fail] 날짜 원본 컬럼 잔존: {remain_date_cols}")

    remain_id_cols = [
        c for c in train.columns
        if c.lower() == "user_id" or c.lower() == "email" or c.lower().endswith("_id")
    ]
    if remain_id_cols:
        raise ValueError(f"[pre-encode fail] ID성 컬럼 잔존: {remain_id_cols}")

    tr_missing = int(train.isnull().sum().sum())
    te_missing = int(test.isnull().sum().sum())
    if tr_missing or te_missing:
        raise ValueError(f"[pre-encode fail] 결측치 잔존(train={tr_missing}, test={te_missing})")

    remain_object_cols = sorted(set(
        train.select_dtypes(include=["object"]).columns.tolist()
        + test.select_dtypes(include=["object"]).columns.tolist()
    ))
    if remain_object_cols:
        raise ValueError(f"[pre-encode fail] object dtype 잔존: {remain_object_cols}")

    print("pre-encode validation: PASS")


# ─────────────────────────────────────────
# 3. 결측치 처리
# ─────────────────────────────────────────
def get_age_group(age) -> str:
    """나이 → 연령대 변환"""
    if pd.isna(age) : return 'Unknown'
    if age < 20     : return '10s'
    elif age < 40   : return '20-30s'
    elif age < 60   : return '40-50s'
    else            : return '60s+'


def fill_missing_values(train: pd.DataFrame, test: pd.DataFrame) -> None:
    """컬럼군별 결측치 처리 (기존 핵심 로직 + search/rec/review/watch 확장)."""

    # 처리 전 결측치 현황
    print('=== 처리 전 결측치 현황 ===')
    print(f'train: {train.isnull().sum().sum()}')
    print(f'test : {test.isnull().sum().sum()}')

    # 1) 핵심 사용자 컬럼 처리: 기존 방향 유지
    age_median  = train['age'].median()
    gender_mode = train['gender'].mode()[0]

    for df in [train, test]:
        df['age']    = df['age'].fillna(age_median)
        df['gender'] = df['gender'].fillna(gender_mode)

    # 2) 연령대 임시 컬럼 생성
    for df in [train, test]:
        df['age_group'] = df['age'].apply(get_age_group)

    # 3) 10대 monthly_spend 결측치 -> 0
    for df in [train, test]:
        df.loc[(df['age_group'] == '10s') & (df['monthly_spend'].isna()), 'monthly_spend'] = 0

    # 4) 사용자 지출/가구 컬럼은 연령대 중앙값 -> 전체 중앙값 순으로 보정
    fill_cols = ['monthly_spend', 'household_size']

    for col in fill_cols:
        medians        = train.groupby('age_group')[col].median()
        overall_median = train[col].median()

        for df in [train, test]:
            df[col] = df[col].fillna(df['age_group'].map(medians))
            df[col] = df[col].fillna(overall_median)

    # 5) 임시 컬럼 삭제
    for df in [train, test]:
        actual_drop = [c for c in ['age_group'] if c in df.columns]
        df.drop(columns=actual_drop, inplace=True)

    # 6) watch 저/중결측 컬럼 보정
    watch_median_cols = [
        "watch_user_rating",
        "watch_number_of_episodes",
        "watch_box_office_revenue",
        "watch_production_budget",
    ]
    for col in watch_median_cols:
        if col in train.columns and col in test.columns:
            train_median = train[col].median()
            for df in [train, test]:
                df[col] = df[col].fillna(train_median)

    if "watch_number_of_seasons" in train.columns and "watch_number_of_seasons" in test.columns:
        if "watch_content_type" in train.columns:
            season_group_median = train.groupby("watch_content_type")["watch_number_of_seasons"].median()
            for df in [train, test]:
                df["watch_number_of_seasons"] = df["watch_number_of_seasons"].fillna(
                    df["watch_content_type"].map(season_group_median)
                )
        season_overall_median = train["watch_number_of_seasons"].median()
        for df in [train, test]:
            df["watch_number_of_seasons"] = df["watch_number_of_seasons"].fillna(season_overall_median)

    if "watch_genre_secondary" in train.columns and "watch_genre_secondary" in test.columns:
        genre_mode = train["watch_genre_secondary"].mode(dropna=True)
        genre_fill = genre_mode.iloc[0] if not genre_mode.empty else "Unknown"
        for df in [train, test]:
            df["watch_genre_secondary"] = df["watch_genre_secondary"].fillna(genre_fill)

    # 7) recommendation 그룹: 수치형 중앙값, 범주형/ID는 Unknown
    rec_numeric_cols = [
        "rec_recommendation_score",
        "rec_was_clicked",
        "rec_position_in_list",
        "rec_event_count",
    ]
    rec_categorical_cols = [
        "rec_time_of_day",
        "rec_recommendation_id",
        "rec_movie_id",
        "rec_recommendation_type",
        "rec_device_type",
        "rec_algorithm_version",
    ]
    for col in rec_numeric_cols:
        if col in train.columns and col in test.columns:
            col_median = train[col].median()
            for df in [train, test]:
                df[col] = df[col].fillna(col_median)
    for col in rec_categorical_cols:
        if col in train.columns and col in test.columns:
            for df in [train, test]:
                df[col] = df[col].fillna("Unknown")
    if "rec_recommendation_date" in train.columns and "rec_recommendation_date" in test.columns:
        for df in [train, test]:
            # 날짜 분해를 위해 파싱 가능한 기준일로 채운다.
            df["rec_recommendation_date"] = df["rec_recommendation_date"].fillna("1970-01-01")

    # 8) search 그룹: 행동 의미를 반영해 숫자/범주형 분리 보정
    search_median_cols = ["search_results_returned", "search_search_duration_seconds"]
    search_zero_cols = ["search_had_typo", "search_used_filters", "search_event_count"]
    search_unknown_cols = [
        "search_search_id",
        "search_search_query",
        "search_device_type",
        "search_location_country",
    ]
    for col in search_median_cols:
        if col in train.columns and col in test.columns:
            col_median = train[col].median()
            for df in [train, test]:
                df[col] = df[col].fillna(col_median)
    for col in search_zero_cols:
        if col in train.columns and col in test.columns:
            for df in [train, test]:
                df[col] = df[col].fillna(0)
    for col in search_unknown_cols:
        if col in train.columns and col in test.columns:
            for df in [train, test]:
                df[col] = df[col].fillna("Unknown")
    if "search_search_date" in train.columns and "search_search_date" in test.columns:
        for df in [train, test]:
            # 날짜 분해를 위해 파싱 가능한 기준일로 채운다.
            df["search_search_date"] = df["search_search_date"].fillna("1970-01-01")
    if "search_clicked_result_position" in train.columns and "search_clicked_result_position" in test.columns:
        for df in [train, test]:
            # 클릭 없음을 명확히 구분하기 위해 -1을 사용한다.
            df["search_clicked_result_position"] = df["search_clicked_result_position"].fillna(-1)

    # 9) review 그룹: 리뷰 없음 상태를 보존하는 방식으로 보정
    review_zero_cols = [
        "review_rating",
        "review_sentiment_score",
        "review_is_verified_watch",
        "review_helpful_votes",
        "review_total_votes",
        "review_event_count",
    ]
    review_no_review_cols = [
        "review_sentiment",
        "review_review_text",
        "review_review_id",
        "review_movie_id",
        "review_device_type",
    ]
    for col in review_zero_cols:
        if col in train.columns and col in test.columns:
            for df in [train, test]:
                df[col] = df[col].fillna(0)
    for col in review_no_review_cols:
        if col in train.columns and col in test.columns:
            for df in [train, test]:
                df[col] = df[col].fillna("NoReview")
    if "review_review_date" in train.columns and "review_review_date" in test.columns:
        for df in [train, test]:
            # 날짜 분해를 위해 파싱 가능한 기준일로 채운다.
            df["review_review_date"] = df["review_review_date"].fillna("1970-01-01")

    # 처리 후 결측치 현황
    print('=== 처리 후 결측치 현황 ===')
    print(f'train: {train.isnull().sum().sum()}')
    print(f'test : {test.isnull().sum().sum()}')