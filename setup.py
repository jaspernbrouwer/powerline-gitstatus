# vim:fileencoding=utf-8:noet

from setuptools import setup

setup(
    name         = 'powerline-gitstatus',
    description  = 'A Powerline segment for showing the status of a Git working copy',
    version      = '1.2.0',
    keywords     = 'powerline git status prompt',
    license      = 'MIT',
    author       = 'Jasper N. Brouwer',
    author_email = 'jasper@nerdsweide.nl',
    url          = 'https://github.com/jaspernbrouwer/powerline-gitstatus',
    packages     = ['powerline_gitstatus'],
    classifiers  = [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Terminals'
    ]
)
