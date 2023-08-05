from setuptools import setup


with open('README.rst', 'r') as f:
    long_description = f.read().split('\n\n-----\n\n', 1)[1].lstrip()

with open('HISTORY.rst', 'r') as f:
    long_description += '\n' + f.read()

setup(
    name='meeshkan-daemonocle',
    version='1.0.3',
    description='A Python library for creating super fancy Unix daemons',
    long_description=long_description,
    url='https://github.com/meeshkan/daemonocle',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='daemon daemonize fork unix cli',
    packages=['daemonocle'],
    install_requires=[
        'click',
        'psutil',
    ],
    extras_require={
        'test': [
            'flake8',
            'pytest',
            'pytest-cov',
            'python-coveralls',
        ],
    },
)
