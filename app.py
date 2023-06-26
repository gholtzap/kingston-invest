import os

from flask import Flask, render_template, request
from flask_assets import Environment, Bundle

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from alpha_vantage.timeseries import TimeSeries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates

import os
import base64
from io import BytesIO
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
AV_API_KEY = os.getenv('AV_API_KEY')

tickers = []

sns.set_context("notebook")

app = Flask(__name__)
assets = Environment(app)
assets.load_path = ['static/css']

scss = Bundle('styles.scss', filters='pyscss', output='styles.css')
assets.register('scss_all', scss)
scss.build()

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class TickerForm(FlaskForm):
    ticker = StringField('Ticker', validators=[DataRequired()])
    date = StringField('Date (YYYY-MM-DD)', validators=[DataRequired()])
    submit = SubmitField('Submit')


def save_stock_data(ticker, date):
    try:
        ts = TimeSeries(key=AV_API_KEY)
        data, meta_data = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
        data = data.loc[date:]
        return data
    except ValueError:
        print(f'{ticker} is an invalid ticker')
        return None


def plot_graph(data, ticker):
    with plt.style.context('dark_background'):
        color = sns.color_palette("flare")[0]
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(data['4. close'], color=color, linewidth=2.0)
        ax.fill_between(data.index, data['4. close'], color=color, alpha=0.1)

        min_close = data['4. close'].min()
        max_close = data['4. close'].max()
        padding = (max_close - min_close) * 0.1
        ax.set_ylim([min_close - padding, max_close + padding])

        ax.set_title(
            f'Stock Performance of {ticker}', color='white', fontsize=30)
        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Closing Price', color='white')
        ax.grid(True, linewidth=0.5, color='#d3d3d3', linestyle='-')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.tick_params(colors='white')

        return fig


@app.route('/collage')
def collage():

    big_tech_names = os.listdir('./static/images/big_tech')
    cancelled_names = os.listdir('./static/images/cancelled')
    misc_names = os.listdir('./static/images/misc')

    big_tech_images = [image.replace('\\', '/') for image in big_tech_names]
    cancelled_images = [image.replace('\\', '/') for image in cancelled_names]
    misc_images = [image.replace('\\', '/') for image in misc_names]

    return render_template(
        'collage.html',
        big_tech_images=big_tech_images,
        cancelled_images=cancelled_images,
        misc_images=misc_images,
    )


@app.route('/tracker', methods=['GET', 'POST'])
def tracker():
    form = TickerForm()
    plot_url = None

    if form.validate_on_submit():
        ticker = form.ticker.data
        date = form.date.data

        data = save_stock_data(ticker, date)
        if data is None:
            return render_template('error.html', message=f'An error occurred when trying to get data for {ticker}')
        else:
            try:
                fig = plot_graph(data, ticker)
            except TypeError as e:
                return render_template('error.html', message=f'An error occurred when trying to plot data: {str(e)}')
    return render_template('tracker.html', form=form, plot_url=plot_url)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
