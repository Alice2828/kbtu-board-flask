from flask import Flask, request, Response, jsonify, abort
import pymongo
from static.users import UserCollection
from static.posts import PostCollection
from werkzeug import exceptions

app = Flask(__name__)
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client['kbtuBoard']
userdb = UserCollection(db['users'])
postdb = PostCollection(db['posts'])


@app.route('/api/users')
def users():
    return userdb.get_users()


@app.route('/api/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user():
    data = request.get_json()
    if data is None:
        data = {}
    if request.method == 'GET':
        return userdb.get_user(**data)
    elif request.method == 'POST':
        return userdb.add_user(data)
    elif request.method == 'DELETE':
        return userdb.delete_user(**data)
    elif request.method == 'PUT':
        return userdb.update_user(data)
    raise exceptions.MethodNotAllowed


@app.route('/api/posts', methods=['GET'])
def posts():
    data = request.get_json()
    if data is None:
        data = {}
    return postdb.get_posts(**data)


@app.route('/api/post', methods=['GET', 'POST', 'PUT', 'DELETE'])
def post():
    data = request.get_json()
    if data is None:
        data = {}
    if request.method == 'GET':
        return postdb.get_post(**data)
    elif request.method == 'POST':
        return postdb.create_post()
    elif request.method == 'PUT':
        return postdb.update_post(data.get('filter'), data.get('update'))
    elif request.method == 'DELETE':
        return postdb.delete_post(**data)
    raise exceptions.MethodNotAllowed


@app.errorhandler(403)
def error_403(e):
    return jsonify(dict(error='This is a secret you will never know.'))


@app.errorhandler(404)
def error_404(e):
    return jsonify(dict(error='This page does not exist.'))


@app.errorhandler(405)
def error_405(e):
    return jsonify(dict(error='There is no such method available for this page.'))


@app.errorhandler(500)
def error_500(e):
    return jsonify(dict(error='Krivorukiy programmist.'))


if __name__ == '__main__':
    app.run()
