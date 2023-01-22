from flask import Blueprint, flash, render_template, redirect, request, session, url_for

import server
from server.models import URL
from server.utils import get_log_records, form_data_to_dict, process_csv


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
        try:
            if 'file' in request.files:
                total, urls = process_csv(request.files['file'])
                URL.save_from_objects_list(urls)
                flash(f'Total urls: {total}, {len(urls)} added, {total-len(urls)} errors')
            if url_text := request.form.get('url'):
                url = URL.from_string(url_text).save()
                flash(f'{url} added')
        except ValueError as error:
            flash(f'Error: {error}')
        return redirect(url_for('views.index'))

@routes.route('/delete/<int:id>', methods=['POST'])
def delete_url(id):
    if url := URL.query.get(id):
        url.delete()
        flash(f'{url} deleted')
    return redirect(url_for('views.index'))

@routes.route('/log/', methods=['GET'])
def get_log():
    return render_template('log.html', logs=get_log_records(20))
