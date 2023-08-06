# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import

import os
import locale
import gettext

import pkg_resources

import sys

IS_PY2 = int(sys.version[0:1]) < 3

# Change this variable to your app name!
#  The translation files will be under
#  @LOCALE_DIR@/@LANGUAGE@/LC_MESSAGES/@DOMAIN_NAME@.mo
DOMAIN_NAME = "messages"

LOCALE_DIR = pkg_resources.resource_filename(__name__, '')

DEFAULT_LANGUAGES = os.environ.get('LANG', '').split(':')
DEFAULT_LANGUAGES += ['en']

languages = []
try:
    lc, encoding = locale.getdefaultlocale()
except ValueError:
    lc, encoding = None, None
if lc:
    languages.append(lc)

languages += DEFAULT_LANGUAGES
mo_location = LOCALE_DIR

if IS_PY2:
    gettext.install(True, localedir=None, unicode=1)
else:
    gettext.install(True, localedir=None)

gettext.textdomain(DOMAIN_NAME)

gettext.bind_textdomain_codeset(DOMAIN_NAME, "UTF-8")

language = gettext.translation(
    DOMAIN_NAME,
    mo_location,
    languages=languages,
    fallback=True
)

tr = language.ugettext if IS_PY2 else language.gettext
