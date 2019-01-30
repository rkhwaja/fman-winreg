from os.path import exists, expanduser, join
from shutil import copytree, rmtree

userDir = expanduser("~\\AppData\\Roaming\\fman\\Plugins\\User")
targetDir = join(userDir, "WinReg Plugin")
print(f"userDir: {userDir}")
print(f"targetDir: {targetDir}")
rmtree(targetDir, ignore_errors=True)
assert exists(targetDir) is False
copytree("WinReg Plugin", targetDir)
