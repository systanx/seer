# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Entropy-NewtonLC.py'],
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
    name='Entropy-NewtonLC',
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
    icon=['C:\\Users\\ergo\\Desktop\\entrega\\ENLC\\originalsinn_a_need_a_pc_pixel_logo_for_a_college_program_Newto_718f0d49-51e1-4763-a82c-5faf9e5a0fa8.ico'],
)
