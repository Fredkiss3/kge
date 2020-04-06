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


def create_package_list(base_package):
    return [base_package] + [base_package + '.' + pkg for pkg in find_packages(base_package)]


setup(
    name="kge",
    version=info.get("version", "1.0"),
    url="https://github.com/Fredkiss3/kge",
    author='Fredhel KISSIE',
    author_email='fredkiss3@gmail.com',
    description='A 2D Game Engine Written in Python, running in Python and For Python Game Developpers',
    long_description=open('README.md').read(),
    packages=create_package_list("kge"),
    # include_package_data=True,
    package_data={
        "kge.extra.win32.Box2D": ["_Box2D.cp37-win32.pyd"],
        "kge.extra.win64.Box2D": ["_Box2D.cp37-win_amd64.pyd"],
    },
    long_description_content_type='text/markdown',
    install_requires=requirements,
    zip_safe=True,
    classifiers=[
        'Development Status :: 1 - Production/Stable',
        'Environment :: Win32 (MS Windows)',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.7',
        'Topic :: Games/Entertainment',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires=">= 3.7, < 3.8"
)
