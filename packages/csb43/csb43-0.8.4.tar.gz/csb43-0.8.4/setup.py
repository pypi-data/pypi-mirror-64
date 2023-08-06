from __future__ import print_function
from __future__ import unicode_literals

import os
import codecs
from setuptools import find_packages, setup
import csb43

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top
# level README file and 2) it's easier to type in the README file than to put
# a raw string in below ...


def read(fname):
    try:
        with codecs.open(os.path.join(os.path.dirname(__file__), fname),
                         'r', 'utf-8') as f:
            return f.read()
    except Exception:
        return ''


try:
    from babel.messages import frontend as babel  # noqa: F401

    entry_points = """
    [distutils.commands]
    compile_catalog = babel:compile_catalog
    extract_messages = babel:extract_messages
    init_catalog = babel:init_catalog
    update_catalog = babel:update_catalog
    """
except ImportError:
    pass

requirements = ["pycountry>=16.10.23rc1"]

req_openpyxl = "openpyxl<2.5.0"
req_tablib = "tablib>=0.11.3,<1.0.0"

config = {
    'name': "csb43",
    'version': csb43.__version__,
    'author': "wmj",
    'author_email': "wmj.py@gmx.com",
    'description': csb43.__doc__,
    'license': "LGPL",
    'keywords': (
        "csb csb43 aeb aeb43 homebank ofx Spanish bank ods tsv "
        "xls xlsx excel yaml json html"
    ),
    'url': "https://bitbucket.org/wmj/csb43",
    'packages': find_packages(),
    'long_description': (
        read('README.rst') + read('INSTALL') + read('CHANGELOG')
    ),
    'scripts': ["csb2format"],
    #'requires': requirements,
    'install_requires': requirements,
    'tests_require': requirements + ["lxml"],
    'include_package_data': True,
    'extras_require': {
        'babel': ["Babel"],
        'yaml': ['PyYAML'],
        'formats': [req_tablib, req_openpyxl],
        'all': ["PyYAML", req_tablib, req_openpyxl],
    },
    'test_suite': 'csb43.tests',
    #'package_data': {
    #    'i18n': ['csb43/i18n/*']
    #},
    'classifiers': ["Programming Language :: Python",
                    "Programming Language :: Python :: 3",
                    "Development Status :: 4 - Beta",
                    "Environment :: Console",
                    "Topic :: Utilities",
                    "Topic :: Office/Business :: Financial",
                    "License :: OSI Approved :: GNU Lesser General "
                    "Public License v3 (LGPLv3)"]
}


setup(**config)
