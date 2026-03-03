#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import platform
import os
import subprocess
from setuptools import setup, Extension, find_packages

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

libraries = ["crypto"]
include_dirs = []
library_dirs = []
extra_compile_args = []
extra_link_args = []

if platform.system() == "Windows":
    for path in [
        os.environ.get("OPENSSL_ROOT_DIR", ""),
        r"C:\Program Files\OpenSSL-Win64",
        r"C:\Program Files\OpenSSL",
        r"C:\OpenSSL-Win64",
    ]:
        if path and os.path.isdir(path):
            include_dirs.append(os.path.join(path, "include"))
            library_dirs.append(os.path.join(path, "lib"))
            break
    libraries = ["libcrypto"]
    extra_compile_args = ["/O2", "/GL"]
    extra_link_args = ["/LTCG"]

elif platform.system() == "Darwin":
    try:
        prefix = subprocess.check_output(
            ["brew", "--prefix", "openssl"],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        include_dirs.append(prefix + "/include")
        library_dirs.append(prefix + "/lib")
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    extra_compile_args = ["-O3", "-flto", "-fomit-frame-pointer"]
    extra_link_args = ["-flto"]

else:
    extra_compile_args = ["-O3", "-flto", "-fomit-frame-pointer"]
    extra_link_args = ["-flto"]

setup(
    name="TgCrypto",
    version="1.2.9",
    description="Fast and Portable Cryptography Extension Library for Pyrofork",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/fjralf",
    download_url="https://github.com/fjralf/tgcrypto/releases/latest",
    author="rick",
    author_email="riaescf@gmail.com",
    license="LGPLv3+",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    keywords="pyrogram pyrofork telegram crypto cryptography encryption mtproto extension library aes",
    project_urls={
        "Tracker": "https://github.com/fjralf/tgcrypto/issues",
        "Community": "https://t.me/pyrogram",
        "Source": "https://github.com/fjralf/tgcrypto",
        "Documentation": "https://pyrogram.com",
    },
    python_requires="~=3.10",
    packages=find_packages(),
    install_requires=[],
    test_suite="tests",
    zip_safe=False,
    ext_modules=[
        Extension(
            "tgcrypto",
            sources=[
                "tgcrypto/tgcrypto.c",
                "tgcrypto/aes256.c",
                "tgcrypto/ige256.c",
                "tgcrypto/ctr256.c",
                "tgcrypto/cbc256.c"
            ],
            libraries=libraries,
            include_dirs=include_dirs,
            library_dirs=library_dirs,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
        )
    ]
)