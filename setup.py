#!/usr/bin/python

import os
import sys
import shutil
import stat

def main(argv):
    if len(argv) < 2:
        print('Usage: "sudo python setup.py install" or "sudo python setup uninstall"')
    elif argv[1] == "install":
        sudo_username = os.getenv("SUDO_USER")
        if sudo_username:
            home_dir = "/home/" + sudo_username
        else:
            home_dir = os.getenv("HOME")
        install_dir = home_dir + "/.timekeeper"
        print("Timekeeper files will be stored to" + install_dir)
    
        try:
            os.mkdir(install_dir)
            shutil.copy("tkutil.py", install_dir + "/tkutil.py")
            shutil.copy("backend.py", install_dir + "/backend.py")
            shutil.copy("timekp.py", install_dir + "/timekp.py")
            os.chmod(install_dir + "/timekp.py", stat.S_IRWXU)
            os.symlink(install_dir + "/timekp.py", "/usr/bin/timekp")
            ids = os.stat(home_dir)
            
            os.chown(install_dir, ids.st_uid, ids.st_gid)
            os.chown("/usr/bin/timekp", ids.st_uid, ids.st_gid)
            os.chown(install_dir + "/tkutil.py", ids.st_uid, ids.st_gid)
            os.chown(install_dir + "/backend.py", ids.st_uid, ids.st_gid)
            os.chown(install_dir + "/timekp.py", ids.st_uid, ids.st_gid)
            os.chown("/usr/bin/timekp", ids.st_uid, ids.st_gid)
            
            print("Successfully installed, run timekp for help")
        except OSError:
            print("Permission denied, please ensure that you have the write access")
            print('Usage: "sudo python setup.py install" or "sudo python setup uninstall"')
            return
      
    elif argv[1] == "uninstall":
        sudo_username = os.getenv("SUDO_USER")
        if sudo_username:
            home_dir = "/home/" + sudo_username
        else:
            home_dir = os.getenv("HOME")
        install_dir = home_dir + "/.timekeeper"

        try:
            shutil.rmtree(install_dir)
            os.remove("/usr/bin/timekp")
            print("Timekeeper successfully uninstalled")
        except OSError:
            print("Permission denied, please ensure that you have the write access")
            print('Usage: "sudo python setup.py install" or "sudo python setup uninstall"')
            return
            
if __name__ == '__main__':
    main(sys.argv)

def target(*args):
    return main, None
