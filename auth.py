from flask import request, jsonify, g
from functools import wraps
from firebase_admin import auth

def get_token_from_header():
    header = request.headers.get('Authorization')
    if not header:
        return None
    parts = header.split(' ')
    if parts[0].lower() != 'bearer':
        return None
    return parts[1]

def firebase_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id_token = get_token_from_header()
        if not id_token:
            return jsonify({'error': 'Unauthorized: No token provided'}), 401

        try:
            decoded_token = auth.verify_id_token(id_token, check_revoked=True)
            g.user_id = decoded_token['uid']
        except auth.ExpiredIdTokenError:
            return jsonify({'error': 'Unauthorized: Token expired'}), 401
        except auth.RevokedIdTokenError:
            return jsonify({'error': 'Unauthorized: Token revoked'}), 401
        except auth.InvalidIdTokenError:
            return jsonify({'error': 'Unauthorized: Invalid token'}), 401
        except Exception as e:
            print(f"Auth Error: {e}")
            return jsonify({'error': 'Unauthorized: Token verification failed'}), 401

        return f(*args, **kwargs)
    return decorated_function