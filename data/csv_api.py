import flask
from flask import jsonify


blueprint = flask.Blueprint('csv_api', __name__, template_folder='templates')


@blueprint.route('/api/<company>', methods=['GET'])
def get_company(company):
    try:
        return open(f'csv_files/{company}.csv', mode='rb').read()
    except Exception:
        return jsonify({})
