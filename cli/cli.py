import sys
import fs
import db
import os
import ai
import typer
from typing import Annotated

def main(
    command: Annotated[str, typer.Argument(help="The command to run")],
    path: Annotated[str, typer.Option(help="The path of the directory to index")] = "",
    query: Annotated[str, typer.Option(help="The query to run")] = "",
    paths: Annotated[str, typer.Option(help="The indexed paths to search in")] = ""
):
    if command == "index" and not path:
        print("You must provide a path to index.")
        sys.exit(1)
    
    if command == "query" and not query:
        print("You must provide a query to run.")
        sys.exit(1)
    
    db.connect()
    if command == "index":
        index(path)
    elif command == "query":
        print(query_files(query, paths))
    db.disconnect()


def index(dir_path):

    dir_cache = db.get_all_files_caches()

    queue = [os.path.abspath(dir_path)]
    while queue:
        current_file = queue.pop(0)

        if os.path.isdir(current_file):
            dir_cache[current_file] = fs.get_directory_description(current_file, dir_cache)
            db.index_file(current_file, dir_cache[current_file])
            print(current_file, ":", dir_cache[current_file])

            files = fs.list_files_in_dir(current_file)

            for file in files:
                if file not in dir_cache or os.path.isdir(current_file) or db.get_file_outdated(file):
                    queue.append(file)
        else:
            dir_cache[current_file] = fs.get_file_description(current_file, dir_cache)
            db.index_file(current_file, dir_cache[current_file])
            print(current_file, ":", dir_cache[current_file])

def query_files(query, paths=None):
    files = db.get_all_files()

    if paths:
        paths = set(paths.split(','))
        files = [file for file in files if file.path in paths or any([file.path.startswith(path) for path in paths])]

    return ai.make_request(f"""
You have the following query:
                               
{query}

You have the following files in your system:

Path | Description
-----
{'\n'.join([f"{file.path} | {file.description}" for file in files])}

Given the above files, specify up to 10 files that fit the query. Consider both the the name and description of the files.

Answer clearly and concisely. Answer only with the full filepaths of the files with a single newline separating the paths and nothing else. If there are no files that fit the query, answer with `None`.
""").strip()

if __name__ == "__main__":
    typer.run(main)
