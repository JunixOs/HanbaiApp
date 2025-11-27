from functools import wraps
from flask import abort
from flask_login import login_required, current_user

def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        @login_required
        def wrapper(*args, **kwargs):
            if not any(current_user.has_role(r) for r in roles):
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator