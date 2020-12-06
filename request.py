import requests
from base64 import b64encode

def get():
    #request_result = requests.get("http://127.0.0.1:5000/login",auth=('test','password'))
    userAndPass = b64encode(b"username:password").decode("ascii")    
    request_result = requests.get("http://127.0.0.1:5000/login",headers={'Authorization': 'Basic %s' % userAndPass })    
    request_token = request_result.json()['token']
    
    requset2 = requests.get("http://127.0.0.1:5000/protected",params={'token':request_token})   
    return requset2.json()
