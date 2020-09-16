import subprocess as sp
from pathlib import Path
import os
import tempfile
import contextlib
import shutil


from subprocess import CalledProcessError


__all__ = ['working_directory', 'working_file',
           'exec_cmd', 'exec_cmd_with_output', 'CalledProcessError',
           'process_flags', 'os_install', 'python3_install', 'python2_install',
           'python_install']


@contextlib.contextmanager
def working_directory(path=''):
    prev_cwd = os.getcwd()
    use_temp_dir = False

    if not path:
        use_temp_dir = True
        path = tempfile.mkdtemp()

    os.makedirs(path, exist_ok=True)
    os.chdir(path)

    try:
        yield
    finally:
        if use_temp_dir:
            shutil.rmtree(path)
        os.chdir(prev_cwd)


@contextlib.contextmanager
def working_file(path='', **kwargs):
    file_desc = None

    if not path:
        file_desc, path = tempfile.mkstemp()

    file_exists = os.path.exists(path)

    if not file_exists:
        Path(path).touch()

    f = open(path, **kwargs)

    try:
        yield f
    finally:
        f.close()

        if file_desc:
            os.close(file_desc)
            os.remove(path)

        if not file_exists:
            os.remove(path)


def exec_cmd(cmd, **kwargs):
    if isinstance(cmd, str):
        cmd = cmd.format(**kwargs).split()
    sp.check_call(cmd, stderr=sp.STDOUT)


def exec_cmd_with_output(cmd, **kwargs):
    if isinstance(cmd, str):
        cmd = cmd.format(**kwargs).split()
    return sp.check_output(cmd, stderr=sp.STDOUT)


def process_flags(flags, delete_flags=tuple()):
    if isinstance(flags, str):
        flags = flags.strip().split()
        if len(flags) == 1:
            flags = flags[0]

    if not isinstance(flags, str):
        flags = ' '.join(iter(flags))

    for flg in delete_flags:
        flags = flags.replace(flg, '')

    return flags


def os_install(*libraries, pre=''):
    sp.check_call(f'{pre} apt update'.split(), stderr=sp.STDOUT)
    sp.check_call(f'{pre} apt install -y'.split() + list(libraries), stderr=sp.STDOUT)
    sp.check_call(f'{pre} apt clean'.split(), stderr=sp.STDOUT)


def python3_install(*modules, pre=''):
    python_install('python3', modules, pre=pre)


def python2_install(*modules, pre=''):
    python_install('python', modules, pre=pre)


def python_install(python_executable, modules_iter, pre=''):
    sp.check_call(f'{pre} {python_executable} -m pip install'.split()
                  + list(modules_iter), stderr=sp.STDOUT)
