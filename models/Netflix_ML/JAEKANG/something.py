import pandas as pd

class NetflixFeatureBuilder:
    def __init__(self, user, watch=None, reviews=None, rec_logs=None, search_logs=None, movies=None):
        self.user = user.copy()
        self.new_user = user.copy()

        self.watch = watch
        self.reviews = reviews
        self.rec_logs = rec_logs
        self.search_logs = search_logs
        self.movies = movies

    def add_recommendation_click_rate(self):
        # -------------------------------------------------
        # recommendation_click_rate 만들기
        # 기준 테이블: user
        # 원본 로그: rec_logs
        # 중복 제거 없이, recommendation 로그 전체 행 기준으로 계산
        # 결과는 % 형태 정수값 (예: 0.3333 -> 33)
        # -------------------------------------------------

        # 1. recommendation 로그에서 필요한 컬럼만 가져오기
        rec_tmp = self.rec_logs[['user_id', 'recommendation_id', 'was_clicked']].copy()

        # 2. 클릭 여부를 0/1로 변환
        rec_tmp['was_clicked_num'] = rec_tmp['was_clicked'].replace({
            True: 1, False: 0,
            'True': 1, 'False': 0,
            'true': 1, 'false': 0,
            1: 1, 0: 0
        })

        # 3. 숫자형으로 변환
        rec_tmp['was_clicked_num'] = pd.to_numeric(rec_tmp['was_clicked_num'], errors='coerce')

        # 4. user별 recommendation_click_rate 계산
        df_rec_click_rate = (
            rec_tmp
            .groupby('user_id', as_index=False)
            .agg(recommendation_click_rate=('was_clicked_num', 'mean'))
        )

        # 5. 100 곱하고 소수점 제거
        df_rec_click_rate['recommendation_click_rate'] = (
            df_rec_click_rate['recommendation_click_rate'] * 100
        ).astype(int)

        # 6. user_id 기준으로 recommendation_click_rate를 맨 오른쪽 컬럼에 추가
        rec_click_rate_map = df_rec_click_rate.set_index('user_id')['recommendation_click_rate']

        self.new_user['recommendation_click_rate'] = (
            self.new_user['user_id']
            .map(rec_click_rate_map)
            .fillna(0)
            .astype(int)
        )
        return self

    def add_content_interactions(self):
        # -------------------------------------------------
        # content_interactions 만들기
        # 정의:
        # user별 (리뷰 작성 수 + 추천 클릭 수 + 검색 결과 클릭 수)
        # -------------------------------------------------

        # 1. reviews.csv -> user별 리뷰 작성 수
        review_count = (
            self.reviews.groupby('user_id')['review_id']
            .count()
            .to_dict()
        )

        # 2. recommendation_logs.csv -> user별 추천 클릭 수
        rec_tmp = self.rec_logs[['user_id', 'was_clicked']].copy()

        rec_tmp['was_clicked_num'] = rec_tmp['was_clicked'].replace({
            True: 1, False: 0,
            'True': 1, 'False': 0,
            'true': 1, 'false': 0,
            1: 1, 0: 0
        })

        rec_tmp['was_clicked_num'] = pd.to_numeric(rec_tmp['was_clicked_num'], errors='coerce')

        rec_click_count = (
            rec_tmp.groupby('user_id')['was_clicked_num']
            .sum()
            .to_dict()
        )

        # 3. search_logs.csv -> user별 검색 결과 클릭 수
        # clicked_result_position 값이 있으면 검색 결과를 클릭한 것으로 간주
        search_tmp = self.search_logs[['user_id', 'clicked_result_position']].copy()

        search_tmp['search_clicked'] = search_tmp['clicked_result_position'].notna().astype(int)

        search_click_count = (
            search_tmp.groupby('user_id')['search_clicked']
            .sum()
            .to_dict()
        )

        # 4. 기존 new_user에 content_interactions 컬럼 추가
        #    (new_user가 이미 recommendation_click_rate 등을 포함한 상태라고 가정)
        

        self.new_user['content_interactions'] = (
            self.new_user['user_id'].map(review_count).fillna(0)
            + self.new_user['user_id'].map(rec_click_count).fillna(0)
            + self.new_user['user_id'].map(search_click_count).fillna(0)
        ).astype(int)

        return self

    def add_rating_given(self):
        # -------------------------------------------------
        # rating_given 만들기
        # 정의:
        # user별 리뷰 평점 평균 -> 반올림 -> int 변환
        # -------------------------------------------------

        # 1. reviews에서 user별 평균 평점 계산
        rating_map = (
            self.reviews.groupby('user_id')['rating']
            .mean()          # user별 평균 평점
            .round(0)        # 반올림
            .astype(int)     # 정수형 변환
            .to_dict()
        )

        # 2. 기존 new_user에 rating_given 컬럼 추가
        

        self.new_user['rating_given'] = (
            self.new_user['user_id']
            .map(rating_map)
            .fillna(0)
            .astype(int)
        )

        return self

    def add_completion_rate(self):
        # -------------------------------------------------
        # completion_rate 만들기
        # 정의:
        # user별 완료 시청 비율
        # = 완료한 시청 수 / 전체 시청 수
        # 결과는 100 곱하고 소수점 아래 버린 int 값
        # -------------------------------------------------

        # 1. 필요한 컬럼만 복사
        watch_tmp = self.watch[['user_id', 'progress_percentage', 'action']].copy()

        # 2. progress_percentage 숫자형 변환
        watch_tmp['progress_percentage'] = pd.to_numeric(
            watch_tmp['progress_percentage'],
            errors='coerce'
        )

        # 3. 완료 여부 컬럼 만들기
        watch_tmp['is_completed'] = (
            (watch_tmp['action'].astype(str).str.lower() == 'completed') |
            (watch_tmp['progress_percentage'] >= 100)
        ).astype(int)

        # 4. user별 completion_rate 계산
        completion_rate_map = (
            (watch_tmp.groupby('user_id')['is_completed'].mean() * 100)
            .astype(int)   # 소수점 아래 버리기
            .to_dict()
        )

        # 5. new_user에 completion_rate 컬럼 추가


        self.new_user['completion_rate'] = (
            self.new_user['user_id']
            .map(completion_rate_map)
            .fillna(0)
            .astype(int)
        )

        return self

    def add_watch_sessions_per_week(self):
        # -------------------------------------------------
        # watch_sessions_per_week 만들기
        # 정의:
        # user별 주간 세션 수 평균 -> 반올림 -> int 변환
        # -------------------------------------------------

        # 1. 필요한 컬럼만 복사
        watch_tmp = self.watch[['user_id', 'session_id', 'watch_date']].copy()

        # 2. 날짜형 변환
        watch_tmp['watch_date'] = pd.to_datetime(watch_tmp['watch_date'], errors='coerce')

        # 3. 주 단위 컬럼 생성
        watch_tmp['watch_week'] = watch_tmp['watch_date'].dt.to_period('W')

        # 4. user별 / 주별 세션 수 계산
        weekly_session = (
            watch_tmp
            .groupby(['user_id', 'watch_week'])['session_id']
            .nunique()
            .reset_index(name='weekly_session_count')
        )

        # 5. user별 주간 세션 수 평균 계산 -> 반올림 -> int
        watch_sessions_per_week_map = (
            weekly_session
            .groupby('user_id')['weekly_session_count']
            .mean()
            .round(0)
            .astype(int)
            .to_dict()
        )


        self.new_user['watch_sessions_per_week'] = (
            self.new_user['user_id']
            .map(watch_sessions_per_week_map)
            .fillna(0)
            .astype(int)
        )

        return self

    def add_avg_watch_time_minutes(self):
        # -------------------------------------------------
        # avg_watch_time_minutes 만들기
        # 정의:
        # user별 하루 평균 시청 시간 -> 반올림 -> int 변환
        # -------------------------------------------------

        # 1. 필요한 컬럼만 복사
        watch_tmp = self.watch[['user_id', 'watch_date', 'watch_duration_minutes']].copy()

        # 2. 날짜형 / 숫자형 변환
        watch_tmp['watch_date'] = pd.to_datetime(watch_tmp['watch_date'], errors='coerce')
        watch_tmp['watch_duration_minutes'] = pd.to_numeric(
            watch_tmp['watch_duration_minutes'],
            errors='coerce'
        )

        # 3. user별, 날짜별 총 시청 시간 계산
        daily_watch = (
            watch_tmp
            .groupby(['user_id', 'watch_date'])['watch_duration_minutes']
            .sum()
            .reset_index(name='daily_watch_minutes')
        )

        # 4. user별 하루 평균 시청 시간 계산 -> 반올림 -> int
        avg_watch_time_map = (
            daily_watch
            .groupby('user_id')['daily_watch_minutes']
            .mean()
            .round(0)
            .astype(int)
            .to_dict()
        )

        # 5. new_user에 컬럼 추가
        

        self.new_user['avg_watch_time_minutes'] = (
            self.new_user['user_id']
            .map(avg_watch_time_map)
            .fillna(0)
            .astype(int)
        )

        return self

    def add_favorite_genre(self):
        # -------------------------------------------------
        # favorite_genre 만들기
        # 정의:
        # user별 가장 많이 본 장르
        # -------------------------------------------------

        # 1. 필요한 컬럼만 복사
        watch_tmp = self.watch[['user_id', 'movie_id']].copy()
        movies_tmp = self.movies[['movie_id', 'genre_primary']].copy()

        # 2. watch와 movies를 movie_id 기준으로 병합
        watch_genre = watch_tmp.merge(
            movies_tmp,
            on='movie_id',
            how='left'
        )

        # 3. user별 가장 많이 본 장르 찾기
        favorite_genre_map = (
            watch_genre
            .groupby('user_id')['genre_primary']
            .agg(lambda x: x.dropna().value_counts().idxmax() if not x.dropna().empty else None)
            .to_dict()
        )

        # 4. new_user에 컬럼 추가
        

        self.new_user['favorite_genre'] = (
            self.new_user['user_id']
            .map(favorite_genre_map)
            .fillna('Unknown')
        )

        return self

    def add_last_activity_date(self):


        # -------------------------------------------------
        # last_activity_date / days_since_last_activity 만들기
        # 정의:
        # last_activity_date
        #   = user별 최근 활동 날짜
        #   = watch_date, search_date, review_date, clicked recommendation_date 중 최댓값
        #
        # days_since_last_activity
        #   = 기준일 - last_activity_date
        #   = 기준일은 전체 활동 로그 중 가장 최근 날짜
        # -------------------------------------------------

        # 1. watch 활동
        watch_activity = self.watch[['user_id', 'watch_date']].copy()
        watch_activity = watch_activity.rename(columns={'watch_date': 'activity_date'})
        watch_activity['activity_date'] = pd.to_datetime(watch_activity['activity_date'], errors='coerce')

        # 2. search 활동
        search_activity = self.search_logs[['user_id', 'search_date']].copy()
        search_activity = search_activity.rename(columns={'search_date': 'activity_date'})
        search_activity['activity_date'] = pd.to_datetime(search_activity['activity_date'], errors='coerce')

        # 3. review 활동
        review_activity = self.reviews[['user_id', 'review_date']].copy()
        review_activity = review_activity.rename(columns={'review_date': 'activity_date'})
        review_activity['activity_date'] = pd.to_datetime(review_activity['activity_date'], errors='coerce')

        # 4. recommendation 활동 (클릭한 경우만 활동으로 인정)
        rec_tmp = self.rec_logs[['user_id', 'recommendation_date', 'was_clicked']].copy()

        rec_tmp['was_clicked_num'] = rec_tmp['was_clicked'].replace({
            True: 1, False: 0,
            'True': 1, 'False': 0,
            'true': 1, 'false': 0,
            1: 1, 0: 0
        })

        rec_tmp['was_clicked_num'] = pd.to_numeric(rec_tmp['was_clicked_num'], errors='coerce')
        rec_tmp['recommendation_date'] = pd.to_datetime(rec_tmp['recommendation_date'], errors='coerce')

        rec_activity = rec_tmp.loc[rec_tmp['was_clicked_num'] == 1, ['user_id', 'recommendation_date']].copy()
        rec_activity = rec_activity.rename(columns={'recommendation_date': 'activity_date'})

        # 5. 모든 활동 로그 합치기
        activity_log = pd.concat(
            [watch_activity, search_activity, review_activity, rec_activity],
            axis=0,
            ignore_index=True
        )

        # 날짜 없는 행 제거
        activity_log = activity_log.dropna(subset=['activity_date'])

        # 6. user별 마지막 활동일 map 만들기
        last_activity_map = (
            activity_log
            .groupby('user_id')['activity_date']
            .max()
            .to_dict()
        )

        # 7. 기준일 설정
        reference_date = activity_log['activity_date'].max()

        # 8. new_user에 컬럼 추가

        self.new_user['last_activity_date'] = (
            self.new_user['user_id']
            .map(last_activity_map)
        )

        # 날짜 형식 정리
        self.new_user['last_activity_date'] = pd.to_datetime(
            self.new_user['last_activity_date'],
            errors='coerce'
        )

        # 9. days_since_last_activity 추가
        self.new_user['days_since_last_activity'] = (
            (reference_date - self.new_user['last_activity_date']).dt.days
            .fillna(0)
            .astype(int)
        )

        # 10. last_activity_date는 보기 좋게 날짜만 남기기
        self.new_user['last_activity_date'] = self.new_user['last_activity_date'].dt.date

        return self

    def add_last_activity_date(self):
        # -------------------------------------------------
        # 날짜 컬럼 4개 만들기
        # - last_watch_date
        # - last_search_date
        # - last_review_date
        # - last_activity_date = 위 3개 중 가장 최근 날짜
        # recommendation 날짜는 제외
        # -------------------------------------------------

        # 1. watch 마지막 날짜
        watch_tmp = self.watch[['user_id', 'watch_date']].copy()
        watch_tmp['watch_date'] = pd.to_datetime(watch_tmp['watch_date'], errors='coerce')

        last_watch_date_map = (
            watch_tmp.groupby('user_id')['watch_date']
            .max()
            .to_dict()
        )

        # 2. search 마지막 날짜
        search_tmp = self.search_logs[['user_id', 'search_date']].copy()
        search_tmp['search_date'] = pd.to_datetime(search_tmp['search_date'], errors='coerce')

        last_search_date_map = (
            search_tmp.groupby('user_id')['search_date']
            .max()
            .to_dict()
        )

        # 3. review 마지막 날짜
        review_tmp = self.reviews[['user_id', 'review_date']].copy()
        review_tmp['review_date'] = pd.to_datetime(review_tmp['review_date'], errors='coerce')

        last_review_date_map = (
            review_tmp.groupby('user_id')['review_date']
            .max()
            .to_dict()
        )

        # 4. new_user에 각 날짜 컬럼 추가
        self.new_user['last_watch_date'] = self.new_user['user_id'].map(last_watch_date_map)
        self.new_user['last_search_date'] = self.new_user['user_id'].map(last_search_date_map)
        self.new_user['last_review_date'] = self.new_user['user_id'].map(last_review_date_map)

        # 5. datetime 형식 통일
        date_cols = [
            'last_watch_date',
            'last_search_date',
            'last_review_date'
        ]

        for col in date_cols:
            self.new_user[col] = pd.to_datetime(self.new_user[col], errors='coerce')

        # 6. 마지막 활동일 = 위 3개 날짜 중 최대값
        self.new_user['last_activity_date'] = self.new_user[date_cols].max(axis=1)

        # 7. 보기 좋게 날짜만 남기기
        for col in date_cols + ['last_activity_date']:
            self.new_user[col] = self.new_user[col].dt.date

        return self

    def add_estimated_churn_date_p90(self, p90_days=124):
        # -------------------------------------------------
        # p90 기반 추정 이탈일 + 검증 컬럼 만들기
        #
        # 전제:
        # self.new_user 에 아래 컬럼이 이미 있어야 함
        # - last_watch_date
        # - last_search_date
        # - last_review_date
        # - last_activity_date
        #
        # 생성 컬럼:
        # 1. estimated_churn_date_p90
        # 2. is_p90_estimate_valid
        #    True  = 추정이 상대적으로 타당
        #    False = 추정이 너무 빠름
        # -------------------------------------------------

        required_cols = [
            'last_watch_date',
            'last_search_date',
            'last_review_date',
            'last_activity_date'
        ]

        for col in required_cols:
            if col not in self.new_user.columns:
                raise ValueError(f"'{col}' 컬럼이 없습니다. 먼저 add_last_activity_date()를 실행하세요.")

        # 1. 날짜형 변환
        for col in required_cols:
            self.new_user[col] = pd.to_datetime(self.new_user[col], errors='coerce')

        # 2. 핵심 활동일 = watch + search 중 최대
        self.new_user['last_core_activity_date'] = self.new_user[
            ['last_watch_date', 'last_search_date']
        ].max(axis=1)

        # 3. p90 기반 추정 이탈일
        self.new_user['estimated_churn_date_p90'] = (
            self.new_user['last_core_activity_date'] + pd.to_timedelta(p90_days, unit='D')
        )

        # 4. 추정 타당성 검증
        # True  = last_activity_date가 p90 추정일을 넘지 않음 -> 추정이 상대적으로 타당
        # False = last_activity_date가 p90 추정일 이후에도 있음 -> 추정이 너무 빠름
        self.new_user['is_p90_estimate_valid'] = (
            self.new_user['last_activity_date'] <= self.new_user['estimated_churn_date_p90']
        )

        # 5. 보기 좋게 date만 남기기
        date_cols = [
            'last_core_activity_date',
            'estimated_churn_date_p90'
        ]

        for col in date_cols:
            self.new_user[col] = self.new_user[col].dt.date

        return self

    def get_data(self):
        return self.new_user.copy()