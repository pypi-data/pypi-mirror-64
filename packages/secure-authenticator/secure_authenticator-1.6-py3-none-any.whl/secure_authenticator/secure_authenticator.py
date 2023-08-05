import jwt
secret = "GvzNJpweLFASst8fnwGb"

def get_user(token):
    try:
        d = jwt.decode(token, secret, algorithms=['HS256'])
        if d["issuer"] == "y para k quieres saber esso jajaj saludos":
            return {"user": d["sub"]}
        else:
            if d["sub"] == "admin":
                return {"error": "You are not allowed to create admin tokens, dont be evil"}
            else:
                return {"user": d["sub"]}
    except Exception as e:
        return None


def create_token(username):
    return jwt.encode({'sub': username, 'issuer': 'pkp-ctf'}, secret, algorithm='HS256')
