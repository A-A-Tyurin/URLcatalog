from flask import Blueprint, render_template, redirect, request, session, url_for

import server
from server.models import URL
from server.utils import form_data_to_dict, process_csv


routes = Blueprint('views', __name__)

@routes.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['search_filter'] = form_data_to_dict(**request.form)
    
    search_filter = session.get('search_filter', {})
    filter = [getattr(URL, key).contains(value) for key, value in search_filter.items()]
    page = request.args.get('page', 1, type=int)

    return render_template(
        'index.html',
        filter=search_filter,
        delete_url='views.delete_url',
        urls=URL.query
                .filter(*filter)
                .paginate(page=page, per_page=server.CONFIG.ROWS_PER_PAGE)
    )

@routes.route('/add', methods=['GET', 'POST'])
def add_url():
    if request.method == 'GET':
        return render_template('add_url.html')

    if request.method == 'POST':
        if 'file' in request.files:
            _, urls = process_csv(request.files['file'])
            URL.save_from_objects_list(urls)
        if url_text := request.form.get('url'):
            URL.from_string(url_text).save()
        return redirect(url_for('views.index'))

@routes.route('/delete/<int:id>', methods=['POST'])
def delete_url(id):
    if url := URL.query.get(id):
        url.delete()
    return redirect(url_for('views.index'))

@routes.route('/log/', methods=['GET'])
def get_log():
    with open(server.CONFIG.LOG_PATH, 'r', encoding='utf-8') as log:
        records = log.readlines()[:-21:-1]
    return render_template('log.html', logs=records)
