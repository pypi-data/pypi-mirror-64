import tinycal

from setuptools import setup

setup(
    name='tinycal',
    version=tinycal.__version__,
    description='A Python implementation of cal utility',
    author='Chang-Yen Chih',
    author_email='michael66230@gmail.com',
    packages=['tinycal'],
    entry_points = {
        'console_scripts': ['tcal=tinycal.tcal:main'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
)
