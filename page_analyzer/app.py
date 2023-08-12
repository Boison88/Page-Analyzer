from dotenv import load_dotenv
import os
import requests
from validator import validate, normalize
from db import UrlCheckDatabase, UrlDatabase
from flask import (
    Flask,
    flash,
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
    url_address = requests.form.get('url')
    errors = validate(url_address)
    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('index.html',), 422

    normalized_url = normalize(url_address)
    try:
        repo = UrlDatabase()
        existing_record = repo.find_url_name(normalized_url)
        if existing_record:
            flash('Страница уже существует', 'info')
            return redirect(url_for('show_url', id=existing_record.get('id')))

        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('show_url', id=repo.save({'name': normalized_url})))

    except Exception as ex:
        flash('Error {raised_ex} while save url'.format(raised_ex=ex), 'danger')
        return redirect(url_for('index'))


@app.route('/urls/<int:id>', methods=['GET'])
def show_url(id):
    return render_template('url_detail.html')


@app.route('/urls/<int:id>/checks', methods=['POST'])
def check_url(id):
    pass


@app.errorhandler(404)
def show_error_page(error):
    return render_template('page404.html', title='Page not found'), 404


if __name__ == '__main__':
    app.run(debug=True)
