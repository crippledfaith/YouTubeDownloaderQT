import sys
from pathlib import Path
import os

def get_user_data_dir(appname):
    if sys.platform == "win32":
        import winreg
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders"
        )
        dir_,_ = winreg.QueryValueEx(key, "Local AppData")
        ans = Path(dir_).resolve(strict=False)
    elif sys.platform == 'darwin':
        ans = Path('~/Library/Application Support/').expanduser()
    else:
        ans=Path(getenv('XDG_DATA_HOME', "~/.local/share")).expanduser()
    finalPath = ans.joinpath(appname)
    if os.path.isdir(finalPath) == False:
        os.mkdir(finalPath)
    return finalPath