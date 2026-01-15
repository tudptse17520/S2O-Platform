from flask import jsonify

def init_error_handler(app):

    @app.errorhandler(Exception)
    def handle_exception(e):
        return jsonify({
            "error": str(e)
        }), 500
