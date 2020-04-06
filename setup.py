from setuptools import setup, find_packages

# Parse version number from kge/__init__.py:
with open('kge/__init__.py') as f:
    info = {}
    for line in f.readlines():
        if line.startswith('version'):
            exec(line, info)
            break

requirements = []
with open("requirements.txt") as f:
    for line in f.readlines():
        requirements.append(line.replace("\n", ""))

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

def create_package_list(base_package):
    return [base_package] + [base_package + '.' + pkg for pkg in find_packages(base_package)]


setup(
    name="kge",
    version=info.get("version", "1.0"),
    url="https://github.com/Fredkiss3/kge",
    author='Fredhel KISSIE',
    author_email='fredkiss3@gmail.com',
    description='A 2D Game Engine Written in Python, running in Python and For Python Game Developpers',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=create_package_list("kge"),
    package_data={
        "kge.extra.win32.Box2D": ["_Box2D.cp37-win32.pyd"],
        "kge.extra.win64.Box2D": ["_Box2D.cp37-win_amd64.pyd"],
        "kge.extra.linux64.Box2D": ["_Box2D.cpython-36m-x86_64-linux-gnu.so"],
    },
    install_requires=requirements,
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires=">= 3.6, < 3.8"
)
