from flask import Flask, request, jsonify
import db
import ai

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

    files = db.get_all_files()

    if paths:
        paths = paths.split(',')
        files = [file for file in files if file.path in paths]

    response = ai.make_request(f"""
You have the following query:
                               
{query}

You have the following files in your system:

Path | Description
-----
{'\n'.join([f"{file.path} | {file.description}" for file in files])}

Given the above files, specify up to 10 files that fit the query. Consider both the the name and description of the files.

Answer clearly and concisely. Answer only with the full filepaths of the files with a single newline separating the paths and nothing else. If there are no files that fit the query, answer with `None`.
""")

    return jsonify({"response": response})

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
