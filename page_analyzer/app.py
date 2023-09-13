import os

from page_analyzer.urls import validate, normalize, get_page
from page_analyzer.db import (
    save_url_db,
    find_all_urls_db,
    find_url_id,
    find_url_name,
    save_check,
    find_all_checks,
)

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    url_for,
    abort,
    request
)


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['GET'])
def show_urls():
    url_records = find_all_urls_db()
    return render_template(
        'urls.html',
        records=url_records,
    )


@app.route('/urls', methods=['POST'])
def post_url():
    url_address = request.form.get('url')
    errors = validate(url_address)
    if errors:
        for error in errors:
            flash(error, 'danger')
        return render_template('index.html'), 422

    normalized_url = normalize(url_address)

    existing_record = find_url_name(normalized_url)
    if existing_record:
        flash('Страница уже существует', 'info')
        return redirect(
            url_for('show_url', record_id=existing_record.get('id'))
        )

    flash('Страница успешно добавлена', 'success')
    return redirect(
        url_for('show_url', record_id=save_url_db({'name': normalized_url}))
    )


@app.route('/urls/<int:record_id>', methods=['GET'])
def show_url(record_id):
    url_record = find_url_id(record_id)
    if not url_record:
        return abort(404)

    url_checks = find_all_checks(record_id)
    return render_template(
        'url_detail.html', record=url_record, url_checks=url_checks
    )


@app.route('/urls/<int:record_id>/checks', methods=['POST'])
def check_url(record_id):
    url_record = find_url_id(record_id)
    url_name = url_record.get('name')
    if not url_record:
        return abort(404)
    save_check(record_id, get_page(url_name))
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('show_url', record_id=record_id))


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        'errors.html',
        title='Page not found'
    ), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template(
        'errors.html',
        title='Внутренняя ошибка сервера'
    ), 500
