from .pic_utils.image_steganography import Image_Steganography
from .pic_utils.stegosuite import StegSuite
def stegsuite(file_path, key):
    steg = StegSuite(file_path, key)
    return {"stegsuite" : steg.extract()}

def image_steganography_handler(file_path, key):
    engine = Image_Steganography(file_path, key=key)
    embed = engine.embed()
    decrypt = engine.decrypt()
    return {
        "image_steganography_decrypt" : decrypt.decode('utf-8', 'ignore') ,
        "image_steganography_embed" : embed.decode('utf-8', 'ignore') }

