from flask import abort, Blueprint, request

import server
from server.models import URL
from server.utils import (
    get_log_records, process_csv, validate_json, query_string_to_dict, 
)


routes_v1 = Blueprint('routes_v1', __name__)

@routes_v1.route('/', methods=['GET', 'POST'])
@validate_json(scheme={'url': str})
def index():
    if request.method == 'GET':
        filter_params = query_string_to_dict(request.query_string.decode('utf-8'))
        return [
            url.to_dict() for url in URL.query.filter_by(**filter_params).all()
        ], 200

    if request.method == 'POST':
        if 'file' in request.files:
            total, urls = process_csv(request.files['file'])
            URL.save_from_objects_list(urls)
            return {
                'total': total,
                'uploaded': len(urls),
                'errors': total - len(urls),
            }, 201

        url = URL.from_string(request.json['url']).save()
        return url.to_dict(), 201

@routes_v1.route('/<int:id>', methods=['GET'])
def get_url_by_id(id):
    if url := URL.query.get(id):
        return url.to_dict(), 200
    abort(404)

@routes_v1.route('/<uuid>', methods=['GET'])
def get_url_by_uuid(uuid):
    if url := URL.query.filter_by(uuid=uuid).first():
        return url.to_dict(), 200
    abort(404)

@routes_v1.route('/log', methods=['GET'])
def get_log():
    return get_log_records(20), 200
