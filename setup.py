from setuptools import setup

setup(
    name='montecarlocli',
    version='0.1',
    py_modules=['montecarlocli'],
    install_requires=[
        'Click',
        'numpy',
        'colorama',
        'pandas',
        'scipy',
    ],
    entry_points='''
    [console_scripts]
    montecarlocli=montecarlocli:cli
    '''
)