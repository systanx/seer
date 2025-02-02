# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Entropy-Fourier.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Entropy-Fourier',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\ergo\\Desktop\\entrega\\EF\\originalsinn_i_need_a_pixel_art_for_a_pc_app_that_discribe_tran_04ccde0f-3d6c-4dc5-8f31-94b426f06d0b.ico'],
)
