from setuptools import setup

with open ("README.md" , 'r')as fh:
    long_description = fh.read()
setup(
    name = "Echelon8_test",
    version = '0.0.1',
    description = "Backtesting Engine",
    py_modules = ['echelon'],
    package_dir = {'':'src'},
    #"""https://pypi.org/classifiers/"""
    classifiers = [
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
    ],
    long_description = long_description,
    long_description_content_type = "text/markdown",
    install_requires = [
        'pandas~=0.22.0',
        'numpy~=1.18.2',
        'dash_html_components~=0.10.0',
        'statsmodels~=0.9.0',
        'dash~=0.21.0',
        'plotly~=2.5.1',
        'dash_core_components~=0.22.1',
        'matplotlib~=2.2.2',
        'seaborn~=0.8.1',

    ],
    url='https://github.com/sking8484/echelon',author='Darst King',author_email = "sking8484@gmail.com"
)
