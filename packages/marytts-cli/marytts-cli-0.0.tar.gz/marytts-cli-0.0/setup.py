from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='marytts-cli',
    version='0.0',
    description=str(
        'A command-line client for the HTTP server '
        'of the MaryTTS Text-To-Speech System.'
    ),
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/x3a/marytts-cli',
    author='trevor',
    author_email='trevor@destroyed.today',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='marytts tts text-to-speech synthesis',
    packages=find_packages(),
    python_requires='>=3',
    install_requires=['requests==2.23.0'],
    extras_require={
        'doc': ['pdoc3', 'argparse-manpage'],
        'test': ['coverage'],
    },
    data_files=[('share/man/man1', ['doc/man/marytts-cli.1'])],
    entry_points={},
    project_urls={},
)
