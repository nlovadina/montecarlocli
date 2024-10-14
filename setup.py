from setuptools import setup

setup(
    name='montecarlocli',
    version='0.4',
    py_modules=['montecarlocli'],
    install_requires=[
        'Click',
        'numpy',
        'rich',
        'pandas',
        'scipy',
    ],
    entry_points='''
    [console_scripts]
    montecarlocli=montecarlocli:cli
    '''
)