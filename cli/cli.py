import sys
import fs
import db
import os

def main():
    dir_path = sys.argv[1]

    db.connect()

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
                if file not in dir_cache:
                    queue.append(file)
        else:
            dir_cache[current_file] = fs.get_file_description(current_file, dir_cache)
            db.index_file(current_file, dir_cache[current_file])
            print(current_file, ":", dir_cache[current_file])
    
    db.disconnect()


if __name__ == "__main__":
    main()
