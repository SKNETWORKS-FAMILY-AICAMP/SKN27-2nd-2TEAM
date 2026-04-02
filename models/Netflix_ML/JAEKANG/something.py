import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
        # 날짜 컬럼 6개 만들기
        # 1. last_watch_date
        # 2. last_search_date
        # 3. last_review_date
        # 4. last_recommendation_click_date
        # 5. last_activity_date = 위 4개 중 가장 최근 날짜
        # 6. last_core_activity_date = watch/search 중 가장 최근 날짜
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

        # 4. recommendation 클릭 마지막 날짜
        rec_tmp = self.rec_logs[['user_id', 'recommendation_date', 'was_clicked']].copy()
        rec_tmp['recommendation_date'] = pd.to_datetime(rec_tmp['recommendation_date'], errors='coerce')

        rec_tmp['was_clicked_num'] = rec_tmp['was_clicked'].replace({
            True: 1, False: 0,
            'True': 1, 'False': 0,
            'true': 1, 'false': 0,
            1: 1, 0: 0
        })
        rec_tmp['was_clicked_num'] = pd.to_numeric(rec_tmp['was_clicked_num'], errors='coerce')

        rec_clicked_tmp = rec_tmp[rec_tmp['was_clicked_num'] == 1].copy()

        last_recommendation_click_date_map = (
            rec_clicked_tmp.groupby('user_id')['recommendation_date']
            .max()
            .to_dict()
        )

        # 5. new_user에 4개 날짜 컬럼 추가
        self.new_user['last_watch_date'] = self.new_user['user_id'].map(last_watch_date_map)
        self.new_user['last_search_date'] = self.new_user['user_id'].map(last_search_date_map)
        self.new_user['last_review_date'] = self.new_user['user_id'].map(last_review_date_map)
        self.new_user['last_recommendation_click_date'] = self.new_user['user_id'].map(last_recommendation_click_date_map)

        # 6. datetime 형식 통일
        date_cols = [
            'last_watch_date',
            'last_search_date',
            'last_review_date',
            'last_recommendation_click_date'
        ]

        for col in date_cols:
            self.new_user[col] = pd.to_datetime(self.new_user[col], errors='coerce')

        # 7. last_activity_date = 위 4개 중 가장 최근 날짜
        self.new_user['last_activity_date'] = self.new_user[date_cols].max(axis=1)

        # 8. last_core_activity_date = watch/search 중 가장 최근 날짜
        self.new_user['last_core_activity_date'] = self.new_user[
            ['last_watch_date', 'last_search_date']
        ].max(axis=1)

        # 9. 보기 좋게 date만 남기기
        out_date_cols = date_cols + ['last_activity_date', 'last_core_activity_date']

        for col in out_date_cols:
            self.new_user[col] = self.new_user[col].dt.date

        return self

    def add_estimated_churn_date_p50(self, p50_days=38):
        # -------------------------------------------------
        # 날짜 컬럼 + p50 추정 이탈일 + 검증 컬럼 생성
        #
        # 생성 컬럼:
        # - last_watch_date
        # - last_search_date
        # - last_review_date
        # - last_activity_date
        # - estimated_churn_date_p50
        # - is_p50_estimate_valid
        #
        # 정의:
        # - last_activity_date = max(last_watch_date, last_search_date, last_review_date)
        # - estimated_churn_date_p50 = max(last_watch_date, last_search_date) + p50_days
        # - is_p50_estimate_valid:
        #     True  -> last_activity_date가 estimated_churn_date_p50보다 늦지 않음
        #     False -> last_activity_date가 estimated_churn_date_p50보다 늦음
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

        # 4. new_user에 3개 날짜 컬럼 추가
        self.new_user['last_watch_date'] = self.new_user['user_id'].map(last_watch_date_map)
        self.new_user['last_search_date'] = self.new_user['user_id'].map(last_search_date_map)
        self.new_user['last_review_date'] = self.new_user['user_id'].map(last_review_date_map)

        # 5. datetime 형식 통일
        date_cols = ['last_watch_date', 'last_search_date', 'last_review_date']
        for col in date_cols:
            self.new_user[col] = pd.to_datetime(self.new_user[col], errors='coerce')

        # 6. last_activity_date = watch/search/review 중 가장 최근 날짜
        self.new_user['last_activity_date'] = self.new_user[date_cols].max(axis=1)

        # 7. 내부 계산용 core activity date = watch/search 중 가장 최근 날짜
        core_activity_date = self.new_user[['last_watch_date', 'last_search_date']].max(axis=1)

        # 8. p50 기반 추정 이탈일
        self.new_user['estimated_churn_date_p50'] = (
            core_activity_date + pd.to_timedelta(p50_days, unit='D')
        )

        # 9. 검증 컬럼
        # True  = 추정이 상대적으로 타당
        # False = 추정이 너무 빠름
        self.new_user['is_p50_estimate_valid'] = (
            self.new_user['last_activity_date'] <= self.new_user['estimated_churn_date_p50']
        )

        # 10. 보기 좋게 date만 남기기
        out_date_cols = [
            'last_watch_date',
            'last_search_date',
            'last_review_date',
            'last_activity_date',
            'estimated_churn_date_p50'
        ]

        for col in out_date_cols:
            self.new_user[col] = self.new_user[col].dt.date

        return self

    def add_final_estimated_churn_date(self):
        # -------------------------------------------------
        # 최종 추정 이탈일 컬럼 만들기
        #
        # 로직:
        # - is_active == True  -> 빈칸
        # - is_active == False and is_p50_estimate_valid == True  -> estimated_churn_date_p50
        # - is_active == False and is_p50_estimate_valid == False -> last_activity_date
        # -------------------------------------------------

        required_cols = [
            'is_active',
            'last_activity_date',
            'estimated_churn_date_p50',
            'is_p50_estimate_valid'
        ]

        for col in required_cols:
            if col not in self.new_user.columns:
                raise ValueError(f"'{col}' 컬럼이 없습니다. 먼저 필요한 컬럼을 생성하세요.")

        # 날짜형 변환
        self.new_user['last_activity_date'] = pd.to_datetime(
            self.new_user['last_activity_date'], errors='coerce'
        )
        self.new_user['estimated_churn_date_p50'] = pd.to_datetime(
            self.new_user['estimated_churn_date_p50'], errors='coerce'
        )

        # 기본값: 빈칸용 NaT
        self.new_user['final_estimated_churn_date'] = pd.NaT

        # churn 유저 조건
        churn_mask = self.new_user['is_active'] == False

        # p50 추정이 타당한 churn 유저
        valid_mask = churn_mask & (self.new_user['is_p50_estimate_valid'] == True)

        # p50 추정이 너무 빠른 churn 유저
        invalid_mask = churn_mask & (self.new_user['is_p50_estimate_valid'] == False)

        self.new_user.loc[valid_mask, 'final_estimated_churn_date'] = \
            self.new_user.loc[valid_mask, 'estimated_churn_date_p50']

        self.new_user.loc[invalid_mask, 'final_estimated_churn_date'] = \
            self.new_user.loc[invalid_mask, 'last_activity_date']

        # 보기 좋게 date만 남기기
        self.new_user['final_estimated_churn_date'] = pd.to_datetime(
            self.new_user['final_estimated_churn_date'], errors='coerce'
        ).dt.date

        return self

    def add_review_helpfulness_ratio(self):
        # -------------------------------------------------
        # review_helpfulness_ratio 만들기
        #
        # 정의:
        # user별 리뷰 유용성 비율 평균
        # = (helpful_votes / total_votes)의 user 평균
        #
        # 결측 처리:
        # - total_votes == 0 이면 비율 정의 불가 -> NaN
        # - 유효한 리뷰 비율이 하나도 없는 user는 최종 0으로 채움
        # -------------------------------------------------

        # 1. 필요한 컬럼만 복사
        review_tmp = self.reviews[['user_id', 'helpful_votes', 'total_votes']].copy()

        # 2. 숫자형 변환
        review_tmp['helpful_votes'] = pd.to_numeric(
            review_tmp['helpful_votes'],
            errors='coerce'
        )
        review_tmp['total_votes'] = pd.to_numeric(
            review_tmp['total_votes'],
            errors='coerce'
        )

        # 3. 리뷰 행 기준 helpfulness ratio 계산
        # total_votes가 0이면 비율은 정의 불가하므로 NaN 처리
        review_tmp['review_helpfulness_ratio_row'] = (
            review_tmp['helpful_votes']
            / review_tmp['total_votes'].replace(0, np.nan)
        )

        # 4. 혹시 이상값이 있으면 0~1 범위로 제한
        review_tmp['review_helpfulness_ratio_row'] = review_tmp[
            'review_helpfulness_ratio_row'
        ].clip(lower=0, upper=1)

        # 5. user별 평균 계산
        review_helpfulness_ratio_map = (
            review_tmp.groupby('user_id')['review_helpfulness_ratio_row']
            .mean()
            .to_dict()
        )

        # 6. new_user에 컬럼 추가
        # 유효한 리뷰 비율이 하나도 없는 user는 0으로 채움
        self.new_user['review_helpfulness_ratio'] = (
            self.new_user['user_id']
            .map(review_helpfulness_ratio_map)
            .fillna(0)
        )

        return self

    def add_binge_day_ratio(self):
        # -------------------------------------------------
        # binge_day_ratio 만들기
        #
        # 정의:
        # user별 시청일 중
        # "하루 총 시청시간 >= 180분" 인 날짜의 비율 * 100
        #
        # 예:
        # 시청한 날짜 10일 중 2일이 180분 이상이면
        # binge_day_ratio = 20
        #
        # 결측 처리:
        # - watch_duration_minutes가 없는 행은 NaN 처리
        # - 유효한 시청 날짜가 하나도 없는 user는 최종 0으로 채움
        # -------------------------------------------------

        # 1. 필요한 컬럼만 복사
        watch_tmp = self.watch[['user_id', 'watch_date', 'watch_duration_minutes']].copy()

        # 2. 날짜형 / 숫자형 변환
        watch_tmp['watch_date'] = pd.to_datetime(
            watch_tmp['watch_date'],
            errors='coerce'
        )
        watch_tmp['watch_duration_minutes'] = pd.to_numeric(
            watch_tmp['watch_duration_minutes'],
            errors='coerce'
        )

        # 3. 날짜에서 시간 제거
        # 하루 단위로 묶을 것이므로 normalize 사용
        watch_tmp['watch_date'] = watch_tmp['watch_date'].dt.normalize()

        # 4. user별 / 날짜별 총 시청시간 계산
        # 모든 값이 NaN인 날은 NaN 유지
        daily_watch_minutes = (
            watch_tmp.groupby(['user_id', 'watch_date'], as_index=False)
            .agg(
                daily_watch_minutes=(
                    'watch_duration_minutes',
                    lambda x: x.sum(min_count=1)
                )
            )
        )

        # 5. 유효한 시청시간이 있는 날짜만 사용
        daily_watch_minutes = daily_watch_minutes.dropna(subset=['daily_watch_minutes']).copy()

        # 6. binge 여부 계산
        # 하루 총 시청시간이 180분 이상이면 1, 아니면 0
        daily_watch_minutes['is_binge_day'] = (
            daily_watch_minutes['daily_watch_minutes'] >= 180
        ).astype(int)

        # 7. user별 binge day 비율 계산
        binge_day_ratio_map = (
            daily_watch_minutes.groupby('user_id')['is_binge_day']
            .mean()
            .mul(100)
            .to_dict()
        )

        # 8. new_user에 컬럼 추가
        # 유효한 시청 날짜가 하나도 없는 user는 0으로 채움
        self.new_user['binge_day_ratio'] = (
            self.new_user['user_id']
            .map(binge_day_ratio_map)
            .fillna(0)
        )

        return self

    def add_avg_search_duration_seconds(self):
        # -------------------------------------------------
        # avg_search_duration_seconds 만들기
        #
        # 정의:
        # user별 평균 검색 시간(초)
        #
        # 결측 처리:
        # - search_duration_seconds가 숫자가 아니면 NaN
        # - 유효한 검색 시간이 하나도 없는 user는 최종 0으로 채움
        # -------------------------------------------------

        # 1. 필요한 컬럼만 복사
        search_tmp = self.search_logs[['user_id', 'search_duration_seconds']].copy()

        # 2. 숫자형 변환
        search_tmp['search_duration_seconds'] = pd.to_numeric(
            search_tmp['search_duration_seconds'],
            errors='coerce'
        )

        # 3. user별 평균 검색 시간 계산
        avg_search_duration_seconds_map = (
            search_tmp.groupby('user_id')['search_duration_seconds']
            .mean()
            .to_dict()
        )

        # 4. new_user에 컬럼 추가
        # 검색 로그가 전혀 없는 user는 0으로 채움
        self.new_user['avg_search_duration_seconds'] = (
            self.new_user['user_id']
            .map(avg_search_duration_seconds_map)
            .fillna(0)
        )

        return self

    def get_data(self):
        return self.new_user.copy()