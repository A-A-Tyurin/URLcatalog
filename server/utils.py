import os
import threading

from flask import request
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest

import server
from server import models


MISSED_KEYS_MESSAGE = 'Missed required keys: {}'
WRONG_TYPES_MESSAGE = 'Wrong types: {}'
EXCEPTED_TYPE_MESSAGE = 'For {key} excepted type {value}'
NOT_ALLOWED_EXTENTION = 'Supports only {} files'


def validate_json(scheme, ignore_for=['GET']):
    def decorator(route):
        def wrapper(*args, **kwargs):
            if request.method not in ignore_for and 'file' not in request.files:
                data = request.get_json()
                
                if missed_keys := [key for key in scheme if key not in data]:
                    raise BadRequest(MISSED_KEYS_MESSAGE.format(missed_keys))
                
                if bad_types := [
                    EXCEPTED_TYPE_MESSAGE.format(key=key, value=value)
                    for key, value
                    in scheme.items() if not isinstance(data[key], value)
                ]:
                    return BadRequest(WRONG_TYPES_MESSAGE.format(bad_types))

            return route(*args, **kwargs)
        return wrapper
    return decorator

def query_string_to_dict(query_string):
    params = {}
    for item in query_string.split('&'):
        if item:
            key, value = item.split('=')
            params[key] = value
    return params

def form_data_to_dict(**data):
    params = {}
    for key, value in data.items():
        if value:
            params[key] = value
    return params

class UploadThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        super().__init__(group, target, name, args, kwargs)
        self.data = None
    
    def run(self):
        try:
            if self._target is not None:
                self.data = self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs

def process_csv(file):    
    def run_background(path):
        background = UploadThread(
            target=models.URL.get_objects_from_csv,
            args=(path,)
        )
        background.start()
        background.join()
        return background.data
    
    def check_extention(filename):
        return ('.' in filename and 
                filename.rsplit('.', 1)[1].lower() in server.CONFIG.ALLOWED_EXTENSIONS)

    if not check_extention(file.filename):
        raise ValueError(NOT_ALLOWED_EXTENTION.format(server.CONFIG.ALLOWED_EXTENSIONS))
    
    filename = secure_filename(file.filename)
    path = os.path.join(server.CONFIG.UPLOAD_DIR, filename)
    file.save(path)
    return run_background(path)
