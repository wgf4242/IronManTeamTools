from fastapi import UploadFile, File
from fastapi import FastAPI, Request, Form, File, UploadFile

from fastapi import APIRouter

from utils.app_utils import get_shared_object
from utils.picture_handler import stegsuite, image_steganography_handler

router = APIRouter()


def is_png_or_jpg(data):
    if data.startswith(b'\x89PNG'):
        return 'png'
    if data.startswith(b'\xff\xd8\xff'):
        return 'jpg'


@router.post("/api/picture/upload")
async def upload_picture(file: UploadFile = File(...), key: str = Form(None)):
    from tempfile import TemporaryFile

    txt = await file.read()
    f = TemporaryFile(delete=False, )
    f.write(txt)
    f.close()

    filename = f.name
    state = get_shared_object()

    result = {}
    if not state.get_data('pic1'):
        state.set_data('pic1', txt)
        state.set_data('pic1_name', filename)

    dic = {
        'jpg': [stegsuite, ],
        'png': [image_steganography_handler]
    }

    handle_name = is_png_or_jpg(txt)
    for handler in dic[handle_name]:
        try:
            res_data = handler(filename, key)
            result.update(res_data)
        except Exception as e:
            print(e)
    return result
