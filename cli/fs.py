import ai
import glob
import magic
import cv2
from PIL import Image


def list_files_in_dir(dir_path):
    return glob.glob(dir_path + '/*')

def get_all_ancestor_dirs(dir_path):
    for i in range(len(dir_path)):
        if dir_path[i] == '/':
            yield dir_path[:i]

def get_directory_description(dir_path, dir_cache):
    files = list_files_in_dir(dir_path)

    if len(files) == 0:
        return "The directory is empty."
    
    return ai.make_request(f"""
You have a directory with the following path: `{dir_path}`.

The directory `{dir_path}` contains the following files: `{files}`.

The descriptions of all the ancestor directories are as follows:
{'\n'.join([f"`{d}`: `{dir_cache[d]}`" for d in get_all_ancestor_dirs(dir_path) if d in dir_cache])}

Give me a brief description of the directory. Consider the path of the directory, the name of the directory, and the files in the directory.a

Answer clearly and concisely, in less than 10 words. Answer only with the description and nothing else.
""")

def get_file_contents(file_path):
    try:
        img = Image.open(file_path)
        return "image", img
    except:
        mime = magic.from_file(file_path, mime=True)

        if "text" in mime:
            return "text", open(file_path).read()
        elif "video" in mime:
            return "video", extract_frames(file_path)
        else:
            return "data", open(file_path, 'rb').read()

def extract_frames(file_path, num_frames = 2):
    frames = []
    video = cv2.VideoCapture(file_path)

    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    #extracting frame from video
    for frame_number in range(0, total_frames, total_frames // num_frames):
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video.read()

        if ret:
            #convert from opencv to pillow
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            frames.append(pil_image)
    
    video.release()
    return frames


def get_file_description(file_path, dir_cache):
    file_path = file_path.strip()

    file_type, file_contents = get_file_contents(file_path)

    if file_type == "image":
        return ai.make_request(f"""
You have an image with the following path: `{file_path}`.

The image `{file_path}` is attached below.

The descriptions of all the ancestor directories are as follows:
{'\n'.join([f"`{d}`: `{dir_cache[d]}`" for d in get_all_ancestor_dirs(file_path) if d in dir_cache])}

Give me a brief description of the image. Consider the path of the image, the name of the image, and the content of the image.

Answer clearly and concisely, in less than 10 words. Answer only with the description and nothing else.
""", file_contents)
    
    elif file_type == "text":
        return ai.make_request(f"""
You have a text file with the following path: `{file_path}`.

The descriptions of all the ancestor directories are as follows:
{'\n'.join([f"`{d}`: `{dir_cache[d]}`" for d in get_all_ancestor_dirs(file_path) if d in dir_cache])}

The text file `{file_path}` contains the following content (truncated to 1000 characters):
```
{file_contents[:1000]}
```

Give me a brief description of the text. Consider the path of the text file, the name of the text file, and the content of the text file.

Answer clearly and concisely, in less than 10 words. Answer only with the description and nothing else.
""")
    
    elif file_type == "video":
        # frames = extract_frames(file_path)
        # descriptions = []
        # for frame in frames[:5]:
        description = ai.make_request(f"""
You have an image extracted from a video at the following path: `{file_path}`.

Five image frames from the video `{file_path}` are attached below.

The descriptions of all the ancestor directories are as follows:
{'\n'.join([f"`{d}`: `{dir_cache[d]}`" for d in get_all_ancestor_dirs(file_path) if d in dir_cache])}

Give me a brief description of the image. Consider the path of the image, the name of the image, and the content of the image.

Answer clearly and concisely, in less than 10 words. Answer only with the description and nothing else.
""", file_contents)
            # descriptions.append(description)
        return description
    
    else:
        return ai.make_request(f"""
You have a file with the following path: `{file_path}`.

The descriptions of all the ancestor directories are as follows:
{'\n'.join([f"`{d}`: `{dir_cache[d]}`" for d in get_all_ancestor_dirs(file_path) if d in dir_cache])}

The previously given file contains the following content (in hex) (truncated to 100 bytes):
```
{file_contents.hex()[:200]}
```

Give me a brief description of the file. Consider the path of the file, the name of the file, and the content of the file.

Answer clearly and concisely, in less than 10 words. Answer only with the description and nothing else.
    """)

    
    
                
