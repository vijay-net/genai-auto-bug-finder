
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import os, tempfile
from ..bugfinder.engine import scan_file, scan_directory

app = FastAPI(title='GenAI Auto Bug Finder API', version='1.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.get('/health')
async def health():
    return {'status':'ok'}

@app.post('/scan/file')
async def scan_single_file(file: UploadFile = File(...)):
    tmpdir = tempfile.mkdtemp()
    path = os.path.join(tmpdir, file.filename)
    with open(path,'wb') as fh:
        fh.write(await file.read())
    return scan_file(path)

@app.post('/scan/dir')
async def scan_dir(path: str = Form(...)):
    return scan_directory(path)
