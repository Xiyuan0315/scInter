# setup.py

from setuptools import setup, find_packages

setup(
    name='adata_plot',
    version='0.1.0',
    description='A package for plotting single-cell data with Altair and Scanpy',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='xiyuan315@outlook.com',
    url='https://github.com/yourusername/adata_plot',  # Update with your repo URL
    packages=find_packages(),
    install_requires=[
        'altair>=4.1.0',
        'scanpy>=1.8.0',
        'pandas>=1.3.0',
        'vegafusion>=1.0.0'  # If using vegafusion for Altair
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
