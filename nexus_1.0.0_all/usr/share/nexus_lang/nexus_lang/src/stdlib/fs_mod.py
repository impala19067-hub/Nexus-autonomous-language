"""
Nexus File System Automation Standard Library
"""
import os
import shutil
import glob
import time

class FSModule:
    @staticmethod
    def read(path: str) -> str:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write(path: str, content: str) -> bool:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(str(content))
        return True

    @staticmethod
    def append(path: str, content: str) -> bool:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'a', encoding='utf-8') as f:
            f.write(str(content))
        return True

    @staticmethod
    def exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def is_file(path: str) -> bool:
        return os.path.isfile(path)

    @staticmethod
    def is_dir(path: str) -> bool:
        return os.path.isdir(path)

    @staticmethod
    def list_dir(path: str) -> list[str]:
        if not os.path.exists(path):
            return []
        return os.listdir(path)

    @staticmethod
    def mkdir(path: str) -> bool:
        os.makedirs(path, exist_ok=True)
        return True

    @staticmethod
    def remove(path: str) -> bool:
        if os.path.isfile(path):
            os.remove(path)
            return True
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return True
        return False

    @staticmethod
    def copy(src: str, dst: str) -> bool:
        if os.path.isfile(src):
            shutil.copy2(src, dst)
            return True
        elif os.path.isdir(src):
            shutil.copytree(src, dst, dirs_exist_ok=True)
            return True
        return False

    @staticmethod
    def move(src: str, dst: str) -> bool:
        shutil.move(src, dst)
        return True

    @staticmethod
    def find_files(pattern: str, search_dir: str = ".") -> list[str]:
        return glob.glob(os.path.join(search_dir, pattern), recursive=True)
