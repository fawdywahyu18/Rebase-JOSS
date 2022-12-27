from setuptools import setup

setup(
    name='rebase_os',
    version='0.1.0',
    py_modules=['rebase_os'],
    install_requires=[
        'numpy==1.23.5',
        'openpyxl==3.0.10',
        'pandas==1.5.2',
        ],
    entry_points='''
        [console_scripts]
        rebase_os=rebase_os:rebase_os
    ''',
)