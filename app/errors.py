from flask import render_template, make_response
from app import app


@app.errorhandler(404)
def not_found():
    return make_response(render_template("404.html"), 404)


@app.errorhandler(500)
def server_error():
    return make_response(render_template("500.html"), 500)
