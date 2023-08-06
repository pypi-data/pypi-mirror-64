# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import print_function

import datetime

from .. import csb43


def sample1():
    f = csb43.File(strict=False)

    for n in range(2):
        ac = csb43.Account(strict=f.strict_mode)

        ac.currency = "EUR"
        ac.shortName = "José Müller Muñiz Avinyò"
        ac.accountNumber = "%010d" % n
        ac.bankCode = "0001"
        ac.branchCode = "0005"
        ac.informationMode = 1
        ac.initialBalance = 10 ** n

        f.add_account(ac)

        for idx, m in enumerate(range(3)):
            t = csb43.Transaction(
                strict=ac.strict_mode,
                informationMode=ac.informationMode
            )
            t.transactionDate = datetime.date(
                year=2012,
                month=2,
                day=n + 1
            )
            t.valueDate = t.transactionDate
            t.documentNumber = n * 10 + m
            t.sharedItem = 12
            t.ownItem = 123
            t.reference1 = "1" * 12
            t.reference2 = "2" * 16
            t.amount = '53.2'

            if idx == 0:
                e = csb43.Exchange()
                e.sourceCurrency = 'USD'
                e.amount = '60.87'

                t.add_exchange(e)

            f.add_transaction(t)

        ac.initialDate = ac.transactions[0].transactionDate
        ac.finalDate = ac.transactions[-1].transactionDate

        f.close_account()

    f.close_file()

    return f
