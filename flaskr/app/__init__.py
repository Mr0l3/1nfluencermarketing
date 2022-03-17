import os

from flask import Flask
from .engine import scraper, reports

def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    scrp = scraper.Scraper()
    
    # main page route
    @app.route('/', methods=['GET'])
    def index():
        if len(scrp.profiles) != 50:
            scrp.collect_profiles()

        return reports.Reports.general_report(scrp)


    # main page route with restriction
    @app.route('/<int:number_of_results>', methods=['GET'])
    def index_restricted(number_of_results):
        if len(scrp.profiles) != number_of_results:
            scrp.collect_profiles(number_of_results)

        return reports.Reports.general_report(scrp)


    # detailed report for profile
    @app.route('/report/<username>')
    def detailed_report(username):
        return reports.Reports.detailed_report(scrp, username)

    return app