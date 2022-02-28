import jwt
from common import secret
from datetime import datetime



# Make access token from id user
def make_token(id, role):
    payload =  {
        "id": id,
        "role": role,
        'created_at': str(datetime.now())
    }
    return jwt.encode(payload,secret.token_key, algorithm='HS256')

# Find id from access token
def get_id_token(header_authorization):
    token = header_authorization.split(' ')[1]
    decoded = jwt.decode(token, secret.token_key, algorithms='HS256')
    return (decoded['id'], decoded['role'])
