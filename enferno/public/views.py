from flask import Flask, request, abort, Response, redirect, url_for, flash, Blueprint, send_from_directory, session
from flask.templating import render_template
from flask_security.decorators import roles_required, login_required
from bit import Key, PrivateKey, PrivateKeyTestnet
import json

bp_public = Blueprint('public', __name__, static_folder='../static')


@bp_public.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=10800'
    return response


@bp_public.route('/')
def index():
    return render_template('index.html')


# APIs to handle bitcoin tasks


@bp_public.route('/api/generate/', methods=['POST'])
def api_generate():
    k = Key()
    address = {
        'address': k.address,
        'segwit_address': k.segwit_address,
        'pem': k.to_hex()

    }
    session['pem']= k.to_hex()

    return Response(json.dumps(address), mimetype='application/json'), 200


@bp_public.route('/download/')
def download():
    print (session['pem'])
    return Response(
        session['pem'],
        mimetype="text/plain",
        headers={"Content-disposition":
                 "attachment; filename=wallet.txt"})


@bp_public.route('/robots.txt')
def static_from_root():
    return send_from_directory(bp_public.static_folder, request.path[1:])
