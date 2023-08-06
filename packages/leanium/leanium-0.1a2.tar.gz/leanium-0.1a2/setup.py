from setuptools import setup, find_packages

def readme():
    try:
        with open('README.md', 'r') as f:
            return f.read()
    except (FileNotFoundError, IOError) as e:
        return 'A lean wrapper around Selenium to handle common try, except, else scenarios'

setup(
    name='leanium',
    version='0.1alpha2',
    packages=find_packages(),
    install_requires=['selenium==3.141.0'],
    description='A lean wrapper around Selenium to handle common try, except, else scenarios',
    long_description=readme(),
    author='Brenden Hyde',
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3"
    ]
)
