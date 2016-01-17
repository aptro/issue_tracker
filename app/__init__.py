from flask import Flask
from flask import request, render_template, make_response, jsonify, Response
from utils import fetch_from_github_api

application = Flask(__name__)


@application.route('/')
def get():

    """
    return: serves the landing page for entering github url 
    """
    return render_template('index.html')

@application.route('/issues', methods=['POST'])
def post():

    """
    calls the utils.py funct--> fetch_from_github_api to perform calculation and gathering of data from github issue apis.
    return: response HTMl or error response for failure or other issues
    """
    url = request.form['github_url']
    info_list = url.lstrip('https://github.com/').split('/')
    info_list = filter(bool, info_list)
    try:
        if len(info_list) !=2:
            raise Exception('Issue with url')
        data = fetch_from_github_api(info_list[0], info_list[1])
    except Exception as exc:
        return Response(exc, mimetype="text/html")
    else:
        return render_template('issues.html', result=data)
        

@application.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({'error': str(e)}), 404)
