import pandas as pd

def merge_all_data(user: pd.DataFrame, watch: pd.DataFrame, movies: pd.DataFrame,

                rec_logs: pd.DataFrame, search_logs: pd.DataFrame, reviews: pd.DataFrame) -> pd.DataFrame:


    # watch에 movies 정보 먼저 붙이기
    watch_movies = watch.merge(movies, on='movie_id', how='left')

    # 각 테이블에서 user_id + 고유 컬럼만 선택
    watch_cols = ['user_id', 'session_id', 'movie_id', 'watch_date', 'watch_duration_minutes',
                    'progress_percentage', 'action', 'quality', 'location_country',
                    'is_download', 'user_rating',
                    'title', 'content_type', 'genre_primary', 'genre_secondary',
                    'release_year', 'duration_minutes', 'rating', 'language',
                    'imdb_rating', 'is_netflix_original']

    rec_cols    = ['user_id', 'recommendation_id', 'movie_id', 'recommendation_date',
                    'recommendation_type', 'recommendation_score', 'was_clicked',
                    'position_in_list', 'time_of_day', 'algorithm_version']

    search_cols = ['user_id', 'search_id', 'search_query', 'search_date',
                    'results_returned', 'clicked_result_position',
                    'search_duration_seconds', 'had_typo', 'used_filters', 'location_country']

    review_cols = ['user_id', 'review_id', 'movie_id', 'rating', 'review_date',
                    'is_verified_watch', 'helpful_votes', 'total_votes',
                    'sentiment', 'sentiment_score']

    # user 기준으로 순차 병합
    Netflix = user.copy()
    for df, cols in [(watch_movies, watch_cols),
                        (rec_logs,     rec_cols),
                        (search_logs,  search_cols),
                        (reviews,      review_cols)]:
        Netflix = Netflix.merge(df[cols], on='user_id', how='left')

    return Netflix