# -*- coding: utf-8 -*-
'''
.. note::

    license: GNU Lesser General Public License v3.0 (see LICENSE)
'''

from __future__ import unicode_literals
from __future__ import absolute_import

from ..utils.compat import (
    m3_is_string,
    #m3_unicode,
    m3_bytes
)
from ..utils import (
    check_strict,
    currencyISO,
    b_left_pad,
    b_right_pad,
    export_currency_code,
    export_decimal,
)
from ..utils import messages as msg
#from csb43.i18n import tr as _
from .record import RecordSequence


class Exchange(RecordSequence):
    '''
    Exchange record / (es) registro de cambio de divisa (24)
    '''

    def __init__(self, record=None,
                 **record_settings):
        '''
        :param record: csb record
        :type record: :class:`basestring` or `None`

        :param \*\*record_settings: see :class:`csb43.csb43.RecordSequence`

        :raises: :class:`csb43.utils.Csb43Exception`


        Create an :class:`Exchange` object from a `CSB43` string record::

            >>> record = '{: <80}'.format('240197800000000012345')
            >>> e = Exchange(record)
            >>> print(e.amount)
            123.45
            >>> print(e.sourceCurrency.alpha_3)
            EUR
            >>> print(e.sourceCurrency.numeric)
            978


        From an empty object to a `CSB43` string record::

            >>> from csb43.csb43 import Exchange
            >>> e = Exchange()
            >>> e.amount = 123.45
            >>> e.sourceCurrency = 'EUR'
            >>> bytes(e)
            b'240197800000000012345                                                           '


        '''
        super(Exchange, self).__init__(**record_settings)

        self.__originCurrency = None
        self.__amount = None
        self.__padding = None

        if record is not None:
            chk_args = self._get_check_args()

            record = self.str_encode(record)
            if not self.is_valid(record):
                self._raise_error(msg.BAD_RECORD(record))

            self._set_origin_currency_code(record[4:7], **chk_args)
            self._set_amount(record[7:21], **chk_args)
            self._set_padding(record[21:80], **chk_args)

    def is_valid(self, record):
        return m3_is_string(record)\
            and (22 <= len(record) <= 80) and (record[0:4] == b'2401')

    def _get_origin_currency_code(self):
        return self.__originCurrency

    # amount
    #
    # repr: bytes
    # user in: text
    # user out: currency

    @check_strict(br'^\d{14}$')
    def _set_amount(self, value, **chk_args):
        self.__amount = value

    @property
    def amount(self):
        """amount in the original currency / (es) cantidad en \
la divisa original

Quantities can be assigned as numbers or strings, and they will be truncated to
adjust the decimal format set for the object::

    >>> e = Exchange()
    >>> e.amount = 123
    >>> e.amount
    Decimal('123')
    >>> e.amount = 123.45
    >>> e.amount
    Decimal('123.45')
    >>> e.amount = '1234.56'
    >>> e.amount
    Decimal('1234.56')
    >>> e.amount = 1.2345
    >>> e.amount
    Decimal('1.23')"""
        if self.__amount is not None:
            return self._format_currency(self.__amount, debit=b'2')
        else:
            return None

    @amount.setter
    def amount(self, value):
        v = float(value)
        quantity, _ = self._unformat_currency(v)

        field = "%014d" % quantity
        self._set_amount(self.str_encode(field))

    # padding
    #
    # repr: text
    # user in: bytes,text
    # user out: text

    @check_strict(br'^.{59}$')
    def _set_padding(self, value, **chk_args):
        value = self.str_decode(value)
        self.__padding = value.rstrip(' ')

    @property
    def padding(self):
        "padding"
        return self.__padding

    @padding.setter
    def padding(self, value):
        value = self.str_encode(value)
        field = b_right_pad(value, 59)
        self._set_padding(field)

    # currency
    #
    # repr: bytes
    # user in: text, pycountry
    # user out: pycountry

    @check_strict(br'^\d{3}$')
    def _set_origin_currency_code(self, value, **chk_args):
        self.__originCurrency = value

    @property
    def sourceCurrency(self):
        """original currency / (es) divisa original

`ISO 4217` codes can be assigned::

    >>> e = Exchange()
    >>> e.sourceCurrency = 'USD'
    >>> e.sourceCurrency.alpha_3
    'USD'
    >>> e.sourceCurrency.numeric
    '840'
    >>> e.sourceCurrency = '978'
    >>> e.sourceCurrency.alpha_3
    'EUR'


As well as a :class:`pycountry.db.Currency` object::

    >>> import pycountry
    >>> e.sourceCurrency = pycountry.currencies.get(alpha_3='EUR')
    >>> e.sourceCurrency = pycountry.currencies.get(alpha_3='USD')
    >>> e.sourceCurrency.alpha_3
    'USD'
    >>> type(e.sourceCurrency)
    <class 'pycountry.db.Currency'>"""
        try:
            return currencyISO(self.str_decode(self.__originCurrency))
        except KeyError:
            return None

    @sourceCurrency.setter
    def sourceCurrency(self, value):
        value = self._parse_currency_code(value)
        if value:
            self._set_origin_currency_code(value)

    def __bytes__(self):
        ':rtype: representation of this object as a `CSB43` record'
        record = (b"2401" +
                  b_left_pad(self.__originCurrency or b'', 3, b"0") +
                  b_left_pad(self.__amount or b'', 14, b"0") +
                  b_right_pad(self.str_encode(self.padding) or b'', 59))
        return record

    def __iter__(self):
        return iter([m3_bytes(self)])

    def as_dict(self, decimal_fallback=None):
        '''
        :param decimal_fallback: decimal number fallback representation
        :type record: :class:`bool`

        :rtype: a representation of this object as a :class:`dict`. The keys \
        will be localised

        >>> e = Exchange()
        >>> e.sourceCurrency = "EUR"
        >>> e.amount = 1.23
        >>> e.as_dict() # doctest: +SKIP
        {'divisa_original': 'EUR', 'cantidad': Decimal('1.23')}

        '''
        return {
            msg.T_ORIGINAL_CURRENCY: export_currency_code(self.sourceCurrency),
            msg.T_AMOUNT: export_decimal(self.amount, fallback=decimal_fallback),
        }
