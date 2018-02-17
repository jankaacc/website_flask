from functools import wraps


from flask import url_for, redirect, request, session, abort


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def author_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_author'):
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function