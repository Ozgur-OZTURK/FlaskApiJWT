from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'

def authentication(f):
    @wraps(f)
    def token_control(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': 'Token is invalid'}) ,403

        try:
            data =jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid'}),403

        return f(*args,**kwargs)
    return token_control

@app.route("/unprotected")
def unprotected():
    return jsonify({'message':'Unproteced page'})

@app.route("/protected")
@authentication
def protected():
    return jsonify({'message':'Proteced page'})

@app.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'password':
        token = jwt.encode({'user' : auth.username, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=15)}, app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')})

    return make_response("Could not verify!", 401, {'flask-api-header': 'Could not verify!'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

