"""
The setup package to install SeleniumBase dependencies and plugins
(Uses selenium 3.x and is compatible with Python 2.7+ and Python 3.6+)
"""

from setuptools import setup, find_packages  # noqa
from os import path


this_directory = path.abspath(path.dirname(__file__))
long_description = None
try:
    with open(path.join(this_directory, 'README.md'), 'rb') as f:
        long_description = f.read().decode('utf-8')
except IOError:
    long_description = 'Reliable Browser Automation & Testing Framework'

setup(
    name='seleniumbase',
    version='1.23.13',
    description='Reliable Browser Automation & Testing Framework',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/seleniumbase/SeleniumBase',
    platforms=["Windows", "Linux", "Unix", "Mac OS-X"],
    author='Michael Mintz',
    author_email='mdmintz@gmail.com',
    maintainer='Michael Mintz',
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Internet",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
        "Topic :: Software Development :: Testing :: Traffic Generation",
        "Topic :: Utilities",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Framework :: Pytest",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        'pip',
        'setuptools',
        'six',
        'nose',
        'ipdb',
        'unittest2',
        'idna==2.8',  # Must stay in sync with "requests"
        'chardet==3.0.4',  # Must stay in sync with "requests"
        'urllib3==1.25.3',  # Must stay in sync with "requests"
        'requests>=2.22.0',
        'selenium==3.141.0',
        'pluggy>=0.12.0',
        'pytest>=4.6.2',
        'pytest-cov>=2.7.1',
        'pytest-forked>=1.0.2',
        'pytest-html>=1.20.0',
        'pytest-metadata>=1.8.0',
        'pytest-ordering>=0.6',
        'pytest-rerunfailures>=7.0',
        'pytest-xdist>=1.28.0',
        'parameterized>=0.7.0',
        'beautifulsoup4>=4.6.0',  # Keep at >=4.6.0 while using "bs4"
        'pyopenssl>=19.0.0',
        'colorama>=0.4.1',
        'pyotp>=2.2.7',
        'boto>=2.49.0',
        'flake8>=3.7.7',
        'certifi>=2019.3.9',
        'PyVirtualDisplay==0.2.1',  # Keep at 0.2.1 (later versions are slow)
    ],
    packages=[
        'seleniumbase',
        'seleniumbase.common',
        'seleniumbase.config',
        'seleniumbase.console_scripts',
        'seleniumbase.core',
        'seleniumbase.drivers',
        'seleniumbase.extensions',
        'seleniumbase.fixtures',
        'seleniumbase.masterqa',
        'seleniumbase.plugins',
        'seleniumbase.utilities',
        'seleniumbase.utilities.selenium_grid',
        'seleniumbase.utilities.selenium_ide',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'seleniumbase = seleniumbase.console_scripts.run:main',
        ],
        'nose.plugins': [
            'base_plugin = seleniumbase.plugins.base_plugin:Base',
            'selenium = seleniumbase.plugins.selenium_plugin:SeleniumBrowser',
            'page_source = seleniumbase.plugins.page_source:PageSource',
            'screen_shots = seleniumbase.plugins.screen_shots:ScreenShots',
            'test_info = seleniumbase.plugins.basic_test_info:BasicTestInfo',
            ('db_reporting = '
             'seleniumbase.plugins.db_reporting_plugin:DBReporting'),
            's3_logging = seleniumbase.plugins.s3_logging_plugin:S3Logging',
        ],
        'pytest11': ['seleniumbase = seleniumbase.plugins.pytest_plugin']
    }
)

# print(os.system("cat seleniumbase.egg-info/PKG-INFO"))
print("\n*** SeleniumBase Installation Complete! ***\n")
