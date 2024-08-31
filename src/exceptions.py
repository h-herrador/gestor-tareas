from flask import redirect, url_for

def error(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        return redirect(url_for('exception'))