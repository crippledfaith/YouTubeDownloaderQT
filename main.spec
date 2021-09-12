# -*- mode: python ; coding: utf-8 -*-
# pyinstaller  main.spec

block_cipher = None


a = Analysis(['main.py'],
             pathex=['E:\doc\Programming\Python\YouTubeDownloaderQT\YouTubeDownloaderQT'],
             binaries=[],
             datas=[('icon.ico', '.'),('ffmpeg.exe', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Youtube Downloader QT',
          debug=False,
          strip=False,
          upx=True,
          console=False , 
          icon='icon.ico' )
