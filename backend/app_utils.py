from pathlib import Path
def get_pictools_path():
    file = Path(__file__)
    is_debug = r'IronManTeamTools\backend' in f'{file.absolute()}'
    if is_debug:
        steg_base_path = Path(__file__).parent.parent / 'client/dist/tools'
        pictools_path = steg_base_path / 'picture_tools'
    else:
        pictools_path = Path('.') / 'tools/picture_tools'
    return str(pictools_path.absolute())


if __name__ == '__main__':
    print(get_pictools_path())