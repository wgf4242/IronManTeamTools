# IronManTeamTools

本机环境 Python 3.10.3

## 用户使用说明
1. pip install -r requirements.txt
2. 安装nodejs
3. python app.py
4. 添加爆破字典: 将文件放在wordlists里。

## 开发者环境部署
1. 安装好nodejs环境。
2. pip install -r requirements.txt
3. 命令行执行 npm install -g pnpm
4. 进入 client 目录 执行 pnpm install

build.bat: 开发者build一键部署加启动



# TODO List

* binary fuzz 前面补0及后面补0
* encode , rot bruteforce
* 爆破进度条
* img
  * FixPNG
  * 盲水印 2,3
  * pin yu mang shui 2,3 
  * PNG IDAT检测
* r fences bruteforce
* 3种 ook
* crc32 爆破
* zip 循环解压套娃zip
  
* √ 文件逆序
* √ 判断2种字符  字符替换成0 1 ，2种替换。转binary, 提示morse 培根等
