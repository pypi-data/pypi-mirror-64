# -*- Mode: Python; coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2017 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
##  Author(s): Stoq Team <stoq-devel@async.com.br>
##

import datetime
from decimal import Decimal
import mock
import os

from stoqlib.lib.boleto import (BankInfo, custom_property, BILL_OPTION_CUSTOM,
                                get_bank_info_by_number, BankItau)
from stoqlib.lib.cnab.base import Record, Field
from stoqlib.lib.cnab.bb import BBCnab
from stoqlib.lib.cnab.febraban import FebrabanCnab, RecordP, RecordQ, RecordR
from stoqlib.lib.cnab.itau400 import ItauCnab400, ItauPaymentDetail
from stoqlib.lib.cnab.itau import ItauBatchHeader, ItauCnab
from stoqlib.lib.diffutils import diff_files
from stoqlib.lib.unittestutils import get_tests_datadir
from stoqlib.domain.test.domaintest import DomainTest


class TestBank(BankInfo):
    description = 'Test Bank'
    bank_number = 99
    foo = custom_property('foo', 8)

    campo_livre = '0' * 25

    options = dict(
        opcao_teste=BILL_OPTION_CUSTOM,
        segunda_opcao=BILL_OPTION_CUSTOM,
    )


class TestFebraban(DomainTest):
    def setUp(self):
        self.branch = self.create_branch()
        self.bank = self.create_bank_account(bank_branch=u'1102',
                                             bank_account=u'9000150',)
        company = self.create_company()
        self.create_address(person=company.person)
        group = self.create_payment_group(payer=company.person)
        self.payment = self.create_payment(date=datetime.date(2012, 7, 14),
                                           group=group)
        self.payment.identifier = 134
        self.payment.method.destination_account.bank = self.bank
        self.info = TestBank(self.payment)

    @mock.patch('stoqlib.lib.cnab.base.localnow')
    def test_record_p(self, localnow):
        localnow.return_value = datetime.datetime(2012, 4, 8, 12, 6)
        cnab = FebrabanCnab(self.branch, self.bank, self.info)
        record = RecordP(self.payment, self.info, registry_sequence=1)
        record.set_cnab(cnab)
        self.assertEqual(
            record.as_string(),
            ('0990001300001P 0101102 000009000150 000000000001'
             '34       11 2200134          1407201200000000000'
             '100000000002N14072012100000000000000000000000214'
             '072012000000000000000000000000000000000000000000'
             '000                         3000000090000000000 '))

    def test_record_q(self):
        # Company
        cnab = FebrabanCnab(self.branch, self.bank, self.info)
        record = RecordQ(self.payment, self.info, registry_sequence=1)
        record.set_cnab(cnab)
        self.assertEqual(
            record.as_string(),
            ('0990001300001Q 012000000000000000Dummy          '
             '                         Mainstreet 138, Compl  '
             '                 Cidade Araci   12345678Los Ange'
             'les    Ca0000000000000000                       '
             '                 000                            '))

        # Individual
        individual = self.create_individual()
        self.create_address(person=individual.person)
        group = self.create_payment_group(payer=individual.person)
        payment = self.create_payment(date=datetime.date(2012, 7, 14),
                                      group=group)
        record = RecordQ(payment, self.info, registry_sequence=1)
        record.set_cnab(cnab)
        self.assertEqual(
            record.as_string(),
            ('0990001300001Q 011000000000000000individual     '
             '                         Mainstreet 138, Compl  '
             '                 Cidade Araci   12345678Los Ange'
             'les    Ca0000000000000000                       '
             '                 000                            '))

    def test_record_r(self):
        cnab = FebrabanCnab(self.branch, self.bank, self.info)
        record = RecordR(self.payment, self.info, registry_sequence=1)
        record.set_cnab(cnab)
        self.assertEqual(
            record.as_string(),
            ('0990001300001R 010000000000000000000000000000000'
             '00000000000000000200000000000000000000000       '
             '                                                '
             '                                                '
             '       0000000000000000 000000000000  0         '))


class TestItau(DomainTest):

    def setUp(self):
        self.branch = self.create_branch()
        self.bank = self.create_bank_account(bank_branch=u'1102',
                                             bank_account=u'134',)
        company = self.create_company()
        self.create_address(person=company.person)
        group = self.create_payment_group(payer=company.person)
        self.payment = self.create_payment(date=datetime.date(2012, 7, 14),
                                           group=group)
        self.payment.identifier = 134
        self.payment.method.destination_account.bank = self.bank
        self.info = BankItau(self.payment)
        self.bank.add_bill_option(u'carteira', u'109')
        self.bank.add_bill_option(u'instrucao_1', u'1')
        self.bank.add_bill_option(u'instrucao_2', u'20')
        self.bank.add_bill_option(u'prazo', u'20')

    def test_person_facets_400(self):
        # Company
        cnab = ItauCnab400(self.branch, self.bank, self.info)
        record = ItauPaymentDetail(self.payment, self.info, registry_sequence=1)
        record.set_cnab(cnab)
        self.assertEqual(
            record.as_string(),
            ('10200000000000000110200001342    0000Test payment '
             '            000001340000000000000109              '
             '       I01000000013414071200000000010003410000099N'
             '14071201200000000000000000000000000000000000000000'
             '0000000000000000000200000000000000Dummy           '
             '                        Mainstreet 138, Compl     '
             '              Cidade Araci12345678Los Angeles    C'
             'a                                  00000020 000001'))

        # Individual
        individual = self.create_individual()
        self.create_address(person=individual.person)
        group = self.create_payment_group(payer=individual.person)
        payment = self.create_payment(date=datetime.date(2012, 7, 14),
                                      group=group)
        payment.identifier = 9143
        record = ItauPaymentDetail(payment, self.info, registry_sequence=1)
        record.set_cnab(cnab)
        self.assertEqual(
            record.as_string(),
            ('10200000000000000110200001342    0000Test payment '
             '            000001340000000000000109              '
             '       I01000000914314071200000000010003410000099N'
             '14071201200000000000000000000000000000000000000000'
             '0000000000000000000100000000000000individual      '
             '                        Mainstreet 138, Compl     '
             '              Cidade Araci12345678Los Angeles    C'
             'a                                  00000020 000001'))

    def test_batch_header_240(self):
        cnab = ItauCnab(self.branch, self.bank, self.info)
        header = ItauBatchHeader()
        header.set_cnab(cnab)
        self.assertEqual(header.credit_date, cnab.get_value('create_date'))


class FooRecord(Record):
    size = 5
    fields = [Field('foo', int, 5)]


class TestRecord(DomainTest):
    def test_replace_fields(self):
        class Foo(Record):
            size = 5
            fields = [Field('foo', int, 5)]

        class Bar(Foo):
            size = 5
            replace_fields = dict(
                foo=[Field('bar', int, 3), Field('bin', str, 2)]
            )

        f = Foo(foo=1)
        self.assertEqual(f.as_string(), '00001')

        b = Bar(bar=1, bin='teste')
        self.assertEqual(b.as_string(), '001te')

    def test_get_value(self):
        class Foo(Record):
            some_property = 4
            size = 5
            fields = [Field('some_property', int, 5)]

        foo = Foo()
        self.assertEqual(foo.get_value('some_property'), 4)


class TestCnab(DomainTest):
    def setUp(self):
        self.branch = self.create_branch()
        self.bank = self.create_bank_account(bank_branch=u'1102',
                                             bank_account=u'9000150',)
        self.bank.add_bill_option(u'especie_documento', u'DM')
        payment = self.create_payment()
        payment.method.destination_account.bank = self.bank
        self.info = TestBank(payment)

    def test_get_value(self):
        cnab = FebrabanCnab(self.branch, self.bank, self.info)
        cnab.some_property = 84
        self.assertEqual(cnab.get_value('some_property'), 84)

    def test_add_record(self):
        cnab = FebrabanCnab(self.branch, self.bank, self.info)
        record = cnab.add_record(FooRecord)
        self.assertEqual(record.get_value('bank_number'), 99)

    def test_total_records(self):
        cnab = FebrabanCnab(self.branch, self.bank, self.info)
        self.assertEqual(cnab.total_records, 0)
        cnab.add_record(FooRecord)
        self.assertEqual(cnab.total_records, 1)

    def test_total_registries(self):
        cnab = FebrabanCnab(self.branch, self.bank, self.info)
        cnab.add_record(FebrabanCnab.FileHeader)
        cnab.add_record(FebrabanCnab.BatchHeader)
        cnab.add_record(FooRecord)
        cnab.add_record(FooRecord)
        cnab.add_record(FooRecord)
        bt = cnab.add_record(FebrabanCnab.BatchTrailer)
        cnab.add_record(FebrabanCnab.FileTrailer)

        self.assertEqual(bt.total_registries, 4)

    def test_as_string(self):
        cnab = FebrabanCnab(self.branch, self.bank, self.info)
        cnab.add_record(FooRecord, foo=3)
        self.assertEqual(cnab.as_string(), '00003\r\n')


class CnabTestMixin(object):
    cnab_class = BBCnab

    def _get_expected(self, filename, content):
        fname = get_tests_datadir(filename)
        if not os.path.exists(fname):
            open(fname, 'w').write(content)
        return fname

    def _compare_files(self, content, basename):
        expected = basename + '-expected.txt'
        output = basename + '-output.txt'

        with open(output, 'w') as fh:
            fh.write(content)
        expected = self._get_expected(expected, content)
        diff = diff_files(expected, output)
        os.unlink(output)
        if diff:
            raise AssertionError('%s\n%s' % ("Files differ, output:", diff))

    def _create_payments(self):
        bank = self.create_bank_account(bank_branch=u'1102',
                                        bank_account=u'12345',)
        method = self.get_payment_method(u'bill')
        method.destination_account.bank = bank
        self.create_bill_options(bank)

        sale = self.create_sale()
        sale.identifier = 123
        self.add_product(sale)
        sale.order(self.current_user)
        payments = self.add_payments(sale, method_type=u'bill',
                                     date=datetime.datetime(2011, 5, 30),
                                     installments=10)
        for i, payment in enumerate(payments, 400):
            payment.identifier = i
        sale.client = self.create_client()
        address = self.create_address()
        address.person = sale.client.person
        sale.confirm(self.current_user)
        return payments

    def create_bill_options(self, bank):
        """Create bill options hook.

        Implement in subclasse when needed"""
        pass

    @mock.patch('stoqlib.lib.cnab.base.localnow')
    def test_generation(self, localnow):
        localnow.return_value = datetime.datetime(2012, 4, 8, 12, 6)
        info = get_bank_info_by_number(self.bank_number)
        payments = self._create_payments()
        with self.sysparam(BILL_PENALTY=Decimal(11),
                           BILL_INTEREST=Decimal('0.4'),
                           BILL_DISCOUNT=Decimal('123.45')):
            cnab = info.get_cnab(payments)
        self._compare_files(cnab, 'cnab-%03d' % self.bank_number)


class TestBBCnab(CnabTestMixin, DomainTest):
    bank_number = 1


class TestCaixaCnab(CnabTestMixin, DomainTest):
    bank_number = 104

    def create_bill_options(self, bank):
        bank.add_bill_option(u'codigo_beneficiario', u'123456')
        bank.add_bill_option(u'codigo_convenio', u'123456')


class TestItauCnab(CnabTestMixin, DomainTest):
    bank_number = 341

    def create_bill_options(self, bank):
        bank.add_bill_option(u'carteira', u'109')
        bank.add_bill_option(u'instrucao_1', u'80')
        bank.add_bill_option(u'instrucao_2', u'8')
        bank.add_bill_option(u'prazo', u'2')
