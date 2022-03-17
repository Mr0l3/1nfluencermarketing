from flask import render_template
from pandas import DataFrame
import pandas as pd
from .scraper import Scraper

# Needed por plotting
import base64
from io import BytesIO
from matplotlib.figure import Figure


class Reports():
    def __init__(self, scraper: Scraper) -> None:
        pass

    @staticmethod
    def general_report(scraper: Scraper) -> str:
        data = scraper.profiles
        
        # Format data
        for i in range(len(data)):
            date = data[i]['joined_twitter'][:10]
            data[i]['joined_twitter'] = date

        return render_template('general-report.html', len = len(data), profiles = data)

    
    @staticmethod
    def detailed_report(scraper: Scraper, username: str) -> str:
        # find profile data
        for profile in scraper.profiles:
            if profile['username'] == username:
                prof_data = profile
        
        # retrieve posts information
        if profile['posts_count'] > 5000:
            posts = scraper.get_profiles_posts(username, number_posts=500)
        elif profile['posts_count'] > 500:
            posts = scraper.get_profiles_posts(username, number_posts=int(profile['posts_count'] * 0.1))
        else:
            posts = scraper.get_profiles_posts(username)

        # get only date, excluding time
        for i in range(len(posts)):
            posts[i]['date'] = posts[i]['date'][:10]

        df = DataFrame(posts)

        # convert date column type to datetime type
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')

        fig = Figure(figsize=(10,6))
        ax = fig.subplots()
        buf = BytesIO()
        plot_data = {}

        # tweets per day
        tweets_per_day_df = DataFrame(df.groupby(df.index.date)['favorites'].count())

        # plot
        ax.plot(tweets_per_day_df)
        ax.set_title('Tweets per day')

        # mean and median per day
        day_mean = round(tweets_per_day_df.mean().values[0], 2)
        day_median = round(tweets_per_day_df.median().values[0], 2)

        # save the plot in base64 format
        fig.savefig(buf, format='png', bbox_inches='tight')
        plot_data['days_plot'] = base64.b64encode(buf.getbuffer()).decode('ascii')

        
        # recreate fig (we need to do this for a new plot)
        fig = Figure(figsize=(10,6))
        ax = fig.subplots()
        buf = BytesIO()

        # tweets per month
        tweets_per_month_df = DataFrame(df.groupby([df.index.year, df.index.month])['favorites'].count())

        # reindex dataframe
        tweets_per_month_df.index.rename(['year', 'month'], inplace=True)
        tweets_per_month_df.reset_index(inplace=True)
        tweets_per_month_df = tweets_per_month_df.astype({'year': str, 'month': str})
        tweets_per_month_df['date'] = tweets_per_month_df['year'] + '-' + tweets_per_month_df['month']
        tweets_per_month_df['date'] = pd.to_datetime(tweets_per_month_df['date'], format='%Y-%m')
        tweets_per_month_df.drop(['year', 'month'], axis=1, inplace=True)
        tweets_per_month_df.set_index('date', inplace=True)

        # plot
        ax.plot(tweets_per_month_df)
        ax.set_title('Tweets per month')

        # mean and median per month
        month_mean = round(tweets_per_month_df.mean().values[0], 2)
        month_median = round(tweets_per_month_df.median().values[0], 2)

        print(f'tweets per month lenght: {len(tweets_per_month_df)}')

        #save the plot in base 64 format
        fig.savefig(buf, format='png', bbox_inches='tight')
        plot_data['months_plot'] = base64.b64encode(buf.getbuffer()).decode('ascii')

        
        # recreate fig (we need to do this for a new plot)
        fig = Figure(figsize=(10,6))
        ax = fig.subplots()
        buf = BytesIO()

        # tweets per week
        tweets_per_week_df = DataFrame(df.groupby(pd.Grouper(freq='W-MON'))['favorites'].count())
        ax.plot(tweets_per_week_df)
        ax.set_title('Tweets per week')

        # mean and median per week
        week_mean = round(tweets_per_week_df.mean().values[0], 2)
        week_median = round(tweets_per_week_df.median().values[0], 2)

        #save the plot in base 64 format
        fig.savefig(buf, format='png', bbox_inches='tight')
        plot_data['weeks_plot'] = base64.b64encode(buf.getbuffer()).decode('ascii')


        stats = {'day': {'mean': day_mean, 'median': day_median},
            'week': {'mean': week_mean, 'median': week_median},
            'month': {'mean': month_mean, 'median': week_median}}

        return render_template('detailed-report.html', plot_data=plot_data, stats=stats, profile=prof_data)
