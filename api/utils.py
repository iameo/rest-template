import flask



def fetch_json():
    _json = flask.request.json
    return _json


def fetch_identity_if_logged_on():
    from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except Exception: #in prod, catching specific exceptions is much better
        return False
