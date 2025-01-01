"""
jpgImage = new JPGImage();
jpgImage.load(steganogramFile);
embeddingMethod = new JPGF5(jpgImage, (PointFilter) null);
embeddingMethod.extract(payloadExtracted, (EmbeddingProgress) null);
content = (FileBlock) payloadExtracted.getBlocks().get(0).getFileContent();
"""

import jpype.imports
from jpype.types import *

from utils.app_utils import get_stegstuite_path


class StegSuite:

    def __init__(self, filename, key):
        self.filename = filename
        self.key = key

    def extract(self):
        # jarLocation = "./stegosuite-0.7-win_amd64.jar"
        try:
            res = bytes(self.process())
        except Exception:
            res = ''
        return res

    def process(self):
        jarLocation = get_stegstuite_path()
        if not jpype.isJVMStarted():
            jpype.startJVM(classpath=[jarLocation])
        JPGF5 = JClass("org.stegosuite.image.embedding.jpg.JPGF5")
        JPGImage = JClass("org.stegosuite.image.format.JPGImage")
        File = JClass("java.io.File")
        Payload = JClass("org.stegosuite.model.payload.Payload")
        file = File(self.filename)
        img = JPGImage()
        img.load(file)
        embeddingMethod = JPGF5(img, None)
        payloadExtracted = Payload()
        payloadExtracted.setSteganoPassword(self.key)
        payloadExtracted.setEncryptionPassword(None)
        embeddingMethod.extract(payloadExtracted, None)
        res = payloadExtracted.getBlocks().get(0).getFileContent()
        return res


if __name__ == '__main__':
    key = '123'
    steg = StegSuite(r"D:\wgf\My Documents\GitHub\blog\IronManTeamTools\client\dist\tools\assets\encrypted\stegsuite.jpg", key)
    steg = StegSuite(r"F:\downloads\2025-01-01_152024.jpg", key)
    print(steg.extract())
