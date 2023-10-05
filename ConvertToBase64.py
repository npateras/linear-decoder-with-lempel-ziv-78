import base64

def stringToBase64(text):
    return base64.b64encode(text.encode('utf-8'))