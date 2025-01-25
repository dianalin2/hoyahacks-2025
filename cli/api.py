from flask import Flask, request, jsonify
import db
import cli

app = Flask(__name__)

db.connect()

@app.route('/all')
def folder():
    return jsonify({"response": db.get_all_files_caches()})


@app.route('/query')
def query():
    query = request.args.get('query')
    paths = request.args.get('paths')

    if query is None:
        return jsonify({"response": "Please provide a query parameter"})
    
    return jsonify({"response": cli.query_files(query, paths)})

if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
