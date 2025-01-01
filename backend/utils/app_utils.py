from pathlib import Path
import configparser

CONFIG_FILE_PATH = 'config/tools.ini'

folder = Path(__file__).parent
is_debug = r'IronManTeamTools\backend' in f'{folder.absolute()}'
if is_debug:
    tool_base_dir = folder.parent.parent / 'client/dist'
else:
    tool_base_dir = folder / '../'

def read_config():
    """读取配置文件并返回配置对象"""
    config = configparser.ConfigParser()
    config.read(folder.parent / CONFIG_FILE_PATH, encoding='utf-8')
    return config


def get_base_path():
    return tool_base_dir


def get_pictools_path():
    """返回图片工具路径"""
    base_path = get_base_path()
    config = read_config()
    pictools_path = base_path.joinpath(config['paths']['picture_tools'])
    return pictools_path


def get_stegstuite_path():
    """返回 StegSuite 路径"""
    config = read_config()
    path = get_pictools_path().joinpath(config['paths']['stegosuite'])
    return path

def get_Image_Steganography_path():
    """返回 StegSuite 路径"""
    config = read_config()
    path = get_pictools_path() / config['paths']['Image_Steganography']
    return path


class SharedObject:
    _instance = None  # 类属性用于存储单例实例

    def __new__(cls):
        if cls._instance is None:
            print("Creating the SharedObject instance.")
            cls._instance = super(SharedObject, cls).__new__(cls)
            # 初始化你的全局状态或数据结构
            cls._instance.data_store = {}
        return cls._instance

    def set_data(self, key, value):
        """设置数据"""
        self.data_store[key] = value

    def get_data(self, key):
        """获取数据"""
        return self.data_store.get(key)

    def delete_data(self, key):
        """删除数据"""
        if key in self.data_store:
            del self.data_store[key]

    def clean_data(self, key):
        self.data_store = {}


def get_shared_object():
    return SharedObject()


if __name__ == '__main__':
    print(get_pictools_path())
    print(get_stegstuite_path())
    print(get_Image_Steganography_path())
