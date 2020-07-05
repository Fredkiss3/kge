"""
This file is intended to help compiling a C++ KGE APP
"""

import os
import sys
import time
from glob import glob
lib_dir = "E:\\PROJETS PERSOS\\CC\\Programmes\\C++\\KGE\\KGE"

libs = [
    "spdlog"
]


def vendor_files() -> str:
    v_dir = os.path.join(lib_dir, "vendor")
    vendor_paths = [
        os.path.join(v_dir, lib) for lib in libs
    ]

    # glob all of the paths and then flatten the list into one
    sources_files = sum([glob(os.path.join(path, "*.cpp"))
                         for path in vendor_paths], [])

    sources_files = list(map(lambda path: f'"{path}"', sources_files))
    return " ".join(sources_files)


def lib_files() -> str:
    src_dir = os.path.join(lib_dir, "src")
    source_paths = [
        src_dir,
        os.path.join(src_dir, 'KGE'),
        os.path.join(src_dir, 'KGE', 'Core'),
        #os.path.join(src_dir, 'KGE', 'Utils'),
        os.path.join(src_dir, 'KGE', 'Physics'),
    ]

    # glob all of the paths and then flatten the list into one
    sources_files = sum([glob(os.path.join(path, "*.cpp"))
                         for path in source_paths], [])

    sources_files = list(map(lambda path: f'"{path}"', sources_files))

    return " ".join(sources_files)


def setup(file: str, warning: str = None):
    exe = file[:(file.find(".cpp"))] + ".exe"

    cmd = f"""g++ -I "E:\\PROJETS PERSOS\\CC\\Programmes\\C++\\KGE\\KGE\\src" -I "E:\\PROJETS PERSOS\\CC\\Programmes\\C++\\KGE\\KGE\\vendor"  -o "E:\\PROJETS PERSOS\\CC\\Programmes\\C++\\KGE\\bin\\{exe}"  {file} {lib_files()} {vendor_files()} -std=c++17 """
    if warning is not None:
        cmd += f" {warning}"
    print(cmd)
    print()
    dep = time.time()
    print(f"\x1B[94mCompiling...\033[0m")
    res = os.system(cmd)
    print(
        f"\x1B[94mTook \033[0m\x1B[33m{time.time() - dep} seconds\033[0m to compile\033[0m")
    if res == 0:
        print("\x1B[92mCompiled Successfully !\033[0m")
    else:
        print("\x1B[91mNot Compiled !\033[0m")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        warn = None
        if (len(sys.argv)) > 2:
            warn = sys.argv[2]
        setup(sys.argv[1], warn)
