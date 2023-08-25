from flask_login import current_user
from functools import wraps

# Verificação de admin
def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.usr_role != "lab_pcp" or current_user.usr_role != "aprop_admin":
            return ''
        return func(*args, **kwargs)
    return decorated_view

# Verificação de laboratório
def lab_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.usr_role != "lab_pcp" or current_user.usr_role != "lab_sgs":
            return ''
        return func(*args, **kwargs)
    return decorated_view

# Verificação de admin laboratório
def lab_admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.usr_role != "lab_pcp":
            return ''
        return func(*args, **kwargs)
    return decorated_view

# Verificação de paradas
def aprop_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.usr_role != "aprop_admin" or current_user.usr_role != "aprop_operador":
            return ''
        return func(*args, **kwargs)
    return decorated_view

# Verificação de admin paradas
def aprop_admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.usr_role != "aprop_admin":
            return ''
        return func(*args, **kwargs)
    return decorated_view