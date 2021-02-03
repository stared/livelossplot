from setuptools import setup, find_packages
from os import path
import re


def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()


def version():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'livelossplot/version.py')) as f:
        version_file = f.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
        version = version_match.group(1)

    return version


setup(
    name='livelossplot',
    version=version(),
    python_requires=">=3.6",
    install_requires=[
        'ipython', 'matplotlib', 'bokeh',
        'numpy<1.20;python_version<"3.7"',
    ],
    description='Live training loss plot in Jupyter Notebook for Keras, PyTorch and others.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/stared/livelossplot',
    author='Piotr Migdał',
    author_email='pmigdal@gmail.com',
    keywords=['keras', 'pytorch', 'plot', 'chart', 'deep-learning'],
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Jupyter',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(),
    zip_safe=False
)
