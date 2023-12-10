"""
@files list:

Crypto_check_gui_html.html
petite-vue.es.js
Crypto_00_check.py
crypto_00_check_gui.py

@ requirements
pip install fastapi base58 base45 bubblepy base91
"""

import sys

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.mount("/static", StaticFiles(directory="."), name="static")
templates = Jinja2Templates(directory=".")

# 避免和vue语法冲突 修改jinja2模版语法标签
templates.env.block_start_string = '(%'  # 修改块开始符号
templates.env.block_end_string = '%)'  # 修改块结束符号
templates.env.variable_start_string = '(('  # 修改变量开始符号
templates.env.variable_end_string = '))'  # 修改变量结束符号
templates.env.comment_start_string = '(#'  # 修改注释开始符号
templates.env.comment_end_string = '#)'  # 修改注释结束符号


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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


@app.post("/getInformation")
async def getInformation(info: Request):
    req_info = await info.body()
    # req_info = await info.json()
    return req_info

# 最后加强它方便防止和前面冲突
app.mount("/", StaticFiles(directory=".", html=True), name="static")

# from uvicorn import main
import uvicorn

if __name__ == '__main__':
    from pathlib import Path
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
