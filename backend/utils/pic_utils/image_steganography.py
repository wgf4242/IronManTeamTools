"""
namespace Image_Steganography_Engine
{
	public class Steg_Engine {
        public byte[] Embed(Bitmap InImage)
    }
}


Password窗口在
private void StegEng_Decode_Async_Finished(byte[] OutData)
{
    flag2 = MyProject.Forms.LoginForm.ShowDialog() == DialogResult.OK;

"""
import os
import clr
from utils.app_utils import get_Image_Steganography_path


# script_dir = os.path.dirname(os.path.abspath(__file__))
script_dir =get_Image_Steganography_path()
drawing_dll_path = os.path.join(script_dir, 'System.Drawing.dll')
engine_dll = os.path.join(script_dir, 'Image Steganography Engine.dll')
engine_exe = os.path.join(script_dir, 'Image Steganography.exe')

clr.AddReference(drawing_dll_path)
clr.AddReference(engine_dll)
clr.AddReference(engine_exe)
from System.Drawing import Image
from Image_Steganography_Engine import Steg_Engine
from Image_Steganography import ImgSteg_Win
from System import Array, Byte


class Image_Steganography:
    def __init__(self, filename,  key=None):
        self.key = key
        self.engine = Steg_Engine()
        self.image = Image.FromFile(filename)
        self.cipher =ImgSteg_Win()

    def embed(self) -> bytearray:
        data = self.engine.Embed(self.image)
        self.data = bytearray(data)
        # if self.key:
        #     print(self.decrypt())
        return self.data

    def decrypt(self):
        return bytearray(self.cipher.AESCryptByte(self.key, self.data, False))

if __name__ == '__main__':
    filename = r'F:\Fshare\del1\vmware\test\654321\step1\654321.png'
    key = '654321'

    engine = Image_Steganography(filename, key=key)
    result = engine.embed()
    print(result)
    print(engine.decrypt())
    # print(engine.decrypt())