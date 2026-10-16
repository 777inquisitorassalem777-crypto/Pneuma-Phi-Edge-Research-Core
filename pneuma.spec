# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for PNEUMA Symbiosis (build on Windows)

block_cipher = None

hidden = [
    'pneuma', 'pneuma.cli', 'pneuma.sensors.simulator', 'pneuma.analytics.engine',
    'pneuma.reflection.module', 'pneuma.intuition.module', 'pneuma.ethics.core',
    'pneuma.archetypal.layer', 'pneuma.safety.guard', 'pneuma.reporting.report',
    'sophia', 'sophia.blue_matrix', 'sophia.blue_matrix.matrix',
    'sophia.blue_matrix.channels', 'sophia.blue_matrix.filters',
    'sophia.blue_matrix.adapters', 'sophia.wisdom.layer',
    'sophia.evolution.loop', 'sophia.passport.identity',
    'symbiosis.orchestrator',
]

a = Analysis(
    ['scripts/launcher.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('docs', 'docs'),
        ('README.md', '.'),
    ],
    hiddenimports=hidden,
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PNEUMA-Symbiosis',
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
)
