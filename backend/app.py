"""
@files list:

Crypto_check_gui_html.html
petite-vue.es.js
Crypto_00_check.py
crypto_00_check_gui.py

@ requirements
pip install fastapi base58 base45 bubblepy base91
"""

from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, Request, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from cipher.Crypto_aes_CryptoJS import decrypt as aes_decrypt, decrypt_batch as aes_decrypt_batch
from cipher.Crypto_des_CryptoJS import decrypt as des_decrypt, decrypt_batch as des_decrypt_batch
from cipher.Crypto_rabbit_CryptoJS_302 import decrypt as rabbit_decrypt, decrypt_batch as rabbit_decrypt_batch
from cipher.cloacked_pixel_lsb_bf import decrypt_batch as lsb_aes_decrypt_batch
from cipher.misc_word_frequency02_word import word_count, char_count

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/main/assets", StaticFiles(directory="static/assets"), name="static")
templates = Jinja2Templates(directory=".")

# 避免和vue语法冲突 修改jinja2模版语法标签
templates.env.block_start_string = '(%'  # 修改块开始符号
templates.env.block_end_string = '%)'  # 修改块结束符号
templates.env.variable_start_string = '(('  # 修改变量开始符号
templates.env.variable_end_string = '))'  # 修改变量结束符号
templates.env.comment_start_string = '(#'  # 修改注释开始符号
templates.env.comment_end_string = '#)'  # 修改注释结束符号


@app.get("/")
async def redirect_to_static():
    return RedirectResponse(url="/main")


@app.get("/main")
async def static_endpoint(request: Request):
    return templates.TemplateResponse("static/index.html", {"request": request})


@app.get("/main/{rest_of_path:path}", response_class=HTMLResponse)
async def static_endpoint(request: Request):
    return templates.TemplateResponse("static/index.html", {"request": request})


@app.get("/api/get_wordlists", response_class=HTMLResponse)
async def get_wordlists():
    lst = [file.name for file in Path('wordlists').rglob('*') if not file.name == '.gitignore']
    return JSONResponse(lst)


import Crypto_00_check as check


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 排除列表后, 每个函数执行输入返回输出
def get_list(r):
    exclude = ['dec', 'base64', 'unittest']
    lst = [x for x in dir(check) if not str(x).startswith('__') and x not in exclude]
    d = {}
    # import inspect
    # all_functions = inspect.getmembers(check, inspect.isfunction)
    for method_name in lst:
        method = getattr(check, method_name)
        d[method_name] = method(r)
    return d


@app.post("/test", response_class=HTMLResponse)
async def decrypt(request: Request):
    r = await request.body()
    res = get_list(r)
    return JSONResponse(content=res)


@app.post("/api/frequency", response_class=HTMLResponse)
async def decrypt_lsb_aes(file: UploadFile = File(...), is_count_char: str = Form(False)):
    content = await file.read()
    if is_count_char == '1':
        return char_count(content.decode())
    return word_count(content.decode())


# async def decrypt_lsb_aes(enc: Annotated[str, Form()], file: Annotated[bytes, File()]):
@app.post("/api/lsb_aes", response_class=HTMLResponse)
async def decrypt_lsb_aes(wordlist: Annotated[str, Form()], file: UploadFile = File(...)):
    content = await file.read()
    res = lsb_aes_decrypt_batch(content, 'wordlists/' + wordlist)
    return res


@app.post("/api/aes", response_class=HTMLResponse)
async def decrypt_aes(request: Request):
    r = await request.json()
    enc = r.get('enc', '').encode()
    key = r.get('key', '').encode()
    file = r.get('file', '')
    alg = r.get('alg', '')

    if file:  # 批量爆破
        dic = {"AES": aes_decrypt_batch, "DES": des_decrypt_batch, "RABBIT": rabbit_decrypt_batch}

        res = dic[alg](enc, file)
        if not res:
            return '失败'
        return res

    dic = {"AES": aes_decrypt, "DES": des_decrypt, "RABBIT": rabbit_decrypt}
    res = dic[alg](enc, key)
    if not res:
        return '失败'
    return res


@app.post("/getInformation")
async def getInformation(info: Request):
    req_info = await info.body()
    # req_info = await info.json()
    return req_info


# from uvicorn import main
import uvicorn

if __name__ == '__main__':
    import webbrowser

    file = Path(__file__)

    webbrowser.open('http://127.0.0.1:8000')

    # filename = Path(__file__).stem
    # sys.argv = [__file__, f'{filename}:app', '--reload', '--port', '80']
    # sys.exit(main())
    # uvicorn.run(app='maincor:app', host="127.0.0.1", port=8000, reload=True, debug=True)
    # filename = __file__.split('/')[-1].split('.')[0]
    # uvicorn.run(app=f'{file.stem}:app', host="127.0.0.1", port=8000, reload=True, debug=True)
    uvicorn.run(app=f'{file.stem}:app', host="127.0.0.1", port=8000, reload=True)
