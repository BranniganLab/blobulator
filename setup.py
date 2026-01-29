
from setuptools import setup, find_packages
from glob import glob

setup(
    name='blobulator',
    version='0.9.8',
    description='Edge Detection in Protein Sequences',
    url='https://github.com/BranniganLab/blobulator',
    author='Brannigan Lab',
    author_email='grace.brannigan@rutgers.edu',
    packages=find_packages(),
    install_requires=['Bio', 'numpy>=1.22.0','pandas>=1.4.0', 'matplotlib>=3.5.0', 'importlib_resources>=1.4', 'wtforms', 'flask', 'flask_restful', 'flask_cors', 'flask_session', 'svglib', 'reportlab'],
    include_package_data=True,
    data_files=[("data", glob("blobulator/data/*"))],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.10'
    ],
)
