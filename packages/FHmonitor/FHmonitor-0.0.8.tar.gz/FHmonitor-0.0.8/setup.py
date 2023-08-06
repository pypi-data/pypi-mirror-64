#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ["pymongo==3.4.0", "Adafruit-Blinka==4.1.0",
                "adafruit-circuitpython-busdevice==4.2.1"]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Margaret Johnson",
    author_email='contact@fithome.life',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Reads and stores atm90e32 power values.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='FHmonitor',
    name='FHmonitor',
    packages=find_packages(include=['FHmonitor', 'FHmonitor.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/bitknitting/FHmonitor',
    version='0.0.8',
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'hello_monitor=FHmonitor.command_line:hello_monitor',
            'start_service=FHmonitor.command_line:start_service',
            'status_service=FHmonitor.command_line:status_service',
            'calibrate_voltage=FHmonitor.command_line:calibrate_voltage',
            'calibrate_current=FHmonitor.command_line:calibrate_current',



        ]
    }
)
