# -*- mode: python ; coding: utf-8 -*-
import os
import sys
import streamlit
from PyInstaller.utils.hooks import copy_metadata

# Get streamlit directory
streamlit_dir = os.path.dirname(streamlit.__file__)

datas = [
    ('app.py', '.'),
    ('database.py', '.'),
    (os.path.join(streamlit_dir, 'static'), 'streamlit/static'),
    (os.path.join(streamlit_dir, 'runtime'), 'streamlit/runtime'),
]
datas += copy_metadata('streamlit')

block_cipher = None

a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'streamlit',
        'sqlite3',
        'pandas',
        'ultralytics',
        'cv2',
        'torch',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='run_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='run_app',
)
