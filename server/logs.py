from flask import current_app, request

from server.views import routes

@routes.before_app_request
def log_request():
    current_app.logger.info(f'REQUEST:{request}')

@routes.after_app_request
def log_response(response):
    if response.status_code in [200, 201]:
        current_app.logger.info(f'RESPONSE: {response}')
    return response

@routes.errorhandler(Exception)
def handle_exception(error):
    current_app.logger.error(error)
    return error
