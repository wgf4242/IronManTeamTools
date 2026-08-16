Pushd %~dp0
cd client
start "T" pnpm dev
popd 

cd backend
uv run app.py
