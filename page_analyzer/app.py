from dotenv import load_dotenv
import validators.url as url_validator
import os
import requests
from db import UrlCheckDatabase, UrlDatabase
from flask import (
    Flask,
    flash,
    get_flashed_messages,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET'])
def show_urls():
    url_records = UrlDatabase().find_all()
    return render_template(
        'urls.html',
        records=url_records,
    )


@app.route('/urls', methods=['POST'])
def post_url():
    data = requests.form.get('url')
    print(data)
    if not url_validator(data):
        flash('Некорректный URL', category='danger')
        if len(data) > 255:
            flash('URL превышает 255 символов', category='danger')
        elif len(data) > 255:
            flash('URL обязателен', category='danger')
    return redirect(url_for('show_urls'))


@app.route('/urls/<int:id>', methods=['GET'])
def show_url(id):
    return render_template('url_detail.html')


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    pass


@app.errorhandler(404)
def show_error_page(error):
    return render_template(
        'page404.html',
        title='Page not found',
    )

if __name__ == '__main__':
    app.run(debug=True)
