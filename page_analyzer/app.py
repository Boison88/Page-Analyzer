import os
import requests
from dotenv import load_dotenv
from url_utilities import validate, normalize
from page_parser import get_page_data
from db import UrlCheckDatabase, UrlDatabase
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    url_for,
    abort
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
            return redirect(
                url_for('show_url', record_id=existing_record.get('id'))
            )

        flash('Страница успешно добавлена', 'success')
        return redirect(
            url_for('show_url', record_id=repo.save({'name': normalized_url}))
        )

    except Exception as ex:
        flash(
            'Error {raised_ex} while save url'.format(raised_ex=ex), 'danger'
        )
        return redirect(url_for('index'))


@app.route('/urls/<int:record_id>', methods=['GET'])
def show_url(record_id):
    repo = UrlDatabase()
    url_record = repo.find_url_id(record_id)
    if not url_record:
        return abort(404)

    url_checks = UrlCheckDatabase().find_all_checks(record_id)
    return render_template(
        'url_detail.html', record=url_record, url_checks=url_checks
    )


@app.route('/urls/<int:record_id>/checks', methods=['POST'])
def check_url(record_id):
    url_record = UrlDatabase().find_url_id(record_id)
    if not url_record:
        return abort(404)
    try:
        response = requests.get(url_record.get('name'))
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('show_url', record_id=record_id))

    checks = UrlCheckDatabase()
    new_check = {'status_code': response.status_code}
    new_check.update(get_page_data(response.content.decode()))
    checks.save_check(record_id, new_check)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url', record_id=record_id))


@app.errorhandler(404)
def show_error_page(error):
    return render_template('page404.html', title='Page not found'), 404


if __name__ == '__main__':
    app.run(debug=True)
