@echo off
::client
Pushd %~dp0
cd client
echo %cd%
call pnpm build
popd 

reg delete HKEY_CLASSES_ROOT\.js /v "Content Type" /f
reg delete HKEY_CLASSES_ROOT\.js /v PerceivedType /f

::Pushd %~dp0
::cd backend
::::copy * ..\client\dist\
::robocopy backend ..\client\dist\ /s /XD .idea /XD __pycache__
::echo %cd%
::popd


echo release file in client\dist\
echo start by this command below:
echo 开发者用这个启动
echo cd client\dist\ ^&^& python app.py