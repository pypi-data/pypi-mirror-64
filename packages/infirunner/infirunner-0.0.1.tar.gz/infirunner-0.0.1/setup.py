from setuptools import setup

setup(
    name='infirunner',
    version='0.0.1',
    packages=['infirunner'],
    install_requires=[
        'click',
        'colorama',
        'python-box',
        'gputil',
        'flufl.lock'
    ],
    extras_require={'all': ['torch', 'numpy', 'statsmodels', 'scipy', 'pandas']},
    url='',
    license='',
    author='Ziyang Hu',
    author_email='',
    description=''
)
