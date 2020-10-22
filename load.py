import pandas as pd


def load_data():
    """Return the movies and ratings data in a pandas dataframe.

    Read the csv files from data folder and 
    merge them into just one dataframe.

    Drop some unnecesary columns and change the 
    columns data type.

    Drop movies with less than 40000 votes and 
    create a new decade column."""

    # load movies data
    movies = pd.read_csv('./data/movies.csv')
    movies = movies.convert_dtypes()
    movies.loc[[83917], ['year']] = 2019
    movies['year'] = movies['year'].astype(int)

    # load ratings data
    ratings = pd.read_csv('./data/ratings.csv')
    ratings.drop(ratings.columns.difference([
        'imdb_title_id', 'weighted_average_vote', 'total_votes', 'mean_vote',
        'median_vote', 'allgenders_0age_avg_vote', 'allgenders_0age_votes',
        'allgenders_18age_avg_vote', 'allgenders_18age_votes',
        'allgenders_30age_avg_vote', 'allgenders_30age_votes',
        'allgenders_45age_avg_vote', 'allgenders_45age_votes',
        'males_allages_avg_vote', 'males_allages_votes', 'males_0age_avg_vote',
        'males_0age_votes', 'males_18age_avg_vote', 'males_18age_votes',
        'males_30age_avg_vote', 'males_30age_votes', 'males_45age_avg_vote',
        'males_45age_votes', 'females_allages_avg_vote',
        'females_allages_votes', 'females_0age_avg_vote', 'females_0age_votes',
        'females_18age_avg_vote', 'females_18age_votes',
        'females_30age_avg_vote', 'females_30age_votes',
        'females_45age_avg_vote', 'females_45age_votes',
        'top1000_voters_rating', 'top1000_voters_votes', 'us_voters_rating',
        'us_voters_votes', 'non_us_voters_rating', 'non_us_voters_votes']), axis=1, inplace=True)
    ratings = ratings.convert_dtypes()

    # merge dataframes
    data = pd.merge(movies, ratings, how='outer', on='imdb_title_id')
    # include only movies with more than 40000 votes
    data = data[data['votes'] >= 40000]
    data['decade'] = pd.cut(data.year, [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2021],
                            include_lowest=True, right=False)
    data['decade'] = data['decade'].astype(str)

    return data
