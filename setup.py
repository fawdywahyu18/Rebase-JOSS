from setuptools import setup

setup(
    name='rebase_os',
    version='0.1.0',
    py_modules=['rebase_os'],
    install_requires=[
        'et-xmlfile==1.1.0',
        'numpy==1.24.1',
        'openpyxl==3.0.10',
        'pandas==1.5.2',
        'python-dateutil==2.8.2',
        'pytz==2022.7',
        'six==1.16.0',
        ],
    entry_points='''
        [console_scripts]
        rebase_os=rebase_os:rebase_os
    ''',
)
