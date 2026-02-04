from flask import jsonify

def standardize_response(data=None, message="Success", code=200):
    response = {
        "status": "success" if 200 <= code < 300 else "error",
        "message": message,
        "data": data
    }
    return jsonify(response), code
