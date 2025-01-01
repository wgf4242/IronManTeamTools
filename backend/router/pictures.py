from fastapi import APIRouter
from fastapi import Form, File, UploadFile
from fastapi.responses import Response

from utils.app_utils import get_shared_object
from utils.pic_utils.picture_barcode_cleaner import clean_barcode
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


@router.post("/api/picture/fix-qrcode")
async def fix_qrcode_handler(file: UploadFile = File(...)):
    """修复二维码图片"""
    from tempfile import TemporaryFile

    try:
        content = await file.read()
        # Save content to a temporary file
        with TemporaryFile(delete=False) as temp_file:
            temp_file.write(content)
            temp_filename = temp_file.name
        
        # 调用修复函数
        fixed_image = clean_barcode(temp_filename)
        
        if fixed_image is None:
            return {"error": "无法修复图片"}
            
        return Response(
            content=fixed_image,
            media_type="image/png"
        )
    except Exception as e:
        return {"error": str(e)}
