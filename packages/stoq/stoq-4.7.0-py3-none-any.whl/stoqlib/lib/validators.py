# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

##
## Copyright (C) 2005, 2006 Async Open Source <http://www.async.com.br>
## All rights reserved
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., or visit: http://www.gnu.org/.
##
"""Validators for stoq applications"""

from decimal import Decimal
import datetime
import os
import re

from kiwi.datatypes import converter, ValidationError

from stoqlib.lib.algorithms import modulo11
from stoqlib.lib.formatters import raw_phone_number, raw_postal_code
from stoqlib.lib.translation import stoqlib_gettext

_ = stoqlib_gettext

POSTAL_CODE_CHAR_LEN = 8

#
# Date validatores
#


def is_date_in_interval(date, start_date, end_date):
    """Check if a certain date is within a given interval

    Ignores the hours on the bounding dates and accepts None values for them.
    We choose to return False if there is no interval to check. If a sale has a value
    for an bounding date but not the other, only the former will be considered.
    """
    if not start_date and not end_date:
        return False

    assert isinstance(date, datetime.datetime)
    date = date.date()
    q1 = q2 = True
    if start_date:
        assert isinstance(start_date, datetime.datetime)
        q1 = date >= start_date.date()
    if end_date:
        assert isinstance(end_date, datetime.datetime)
        q2 = date <= end_date.date()

    return q1 and q2

#
# Phone number validators
#


def validate_phone_number(phone_number):
    if not isinstance(phone_number, str):
        return False

    phone_number = raw_phone_number(phone_number)
    if phone_number and phone_number[0] == '0':
        phone_number = phone_number[1:]

    return len(phone_number) in range(7, 12)

#
# Adress validators
#


def validate_postal_code(postal_code):
    if not postal_code:
        return False
    return len(raw_postal_code(postal_code)) == POSTAL_CODE_CHAR_LEN


def validate_area_code(code):
    """Validates Brazilian area codes"""
    if isinstance(code, str):
        try:
            code = converter.from_string(int, code)
        except ValidationError:
            return False

    # Valid brazilian codes are on the range of 10-99
    return 10 <= code <= 99


#
# Document Validators
#


def validate_cpf(cpf):
    cpf = ''.join(re.findall(r'\d', str(cpf)))

    if not cpf or len(cpf) != 11:
        return False

    # FIXME: use modulo11 from algorithms.py

    # With the first 9 digits, we calculate the last two digits (verifiers)
    new = list(map(int, cpf))[:9]

    while len(new) < 11:
        s = sum([(len(new) + 1 - i) * v for i, v in enumerate(new)]) % 11

        if s > 1:
            verifier_digit = 11 - s
        else:
            verifier_digit = 0

        if cpf[len(new)] != str(verifier_digit):
            return False
        else:
            new.append(verifier_digit)

    return True


def validate_cnpj(cnpj):
    """Validates a cnpj.

    :param cnpj: the cnpj to validate. Can be a string or number. If it's a
      string, only the digits will be used.
    """
    cnpj = ''.join(re.findall(r'\d', str(cnpj)))

    if not cnpj or len(cnpj) != 14:
        return False

    # FIXME: use modulo11 from algorithms.py

    # With the first 12 digts, we calculate the last 2 digits (verifiers)
    new = list(map(int, cnpj))[:12]

    verification_base = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    while len(new) < 14:
        s = sum([x * y for (x, y) in zip(new, verification_base)]) % 11

        if s > 1:
            verifier_digit = 11 - s
        else:
            verifier_digit = 0

        if cnpj[len(new)] != str(verifier_digit):
            return False
        else:
            new.append(verifier_digit)
            verification_base.insert(0, 6)

    return True


def validate_cfop(cfop):
    """Validates C.F.O.P. code

    Valid C.F.O.P. format: '9.999', where 9 is any digit in 0-9.
    """
    if not isinstance(cfop, str):
        return False

    if not '.' in cfop:
        return False

    first_part, last_part = cfop.split('.')
    if not first_part.isdigit() or not last_part.isdigit():
        return False
    if not len(first_part) == 1 or not len(last_part) == 3:
        return False

    return True

#
# Misc validators
#


def _validate_type(type_, value):
    if isinstance(value, str):
        try:
            # Just converting to see if any errors are raised.
            converter.from_string(type_, value)
        except ValidationError:
            return False
    else:
        if not isinstance(value, type_):
            return False

    return True


def validate_int(value):
    """Validates an integer.

    Returns if the value is a valid integer, or, in case it's a string,
    if it can be converted to an integer.
    """
    return _validate_type(int, value)


def validate_decimal(value):
    """Validates an Decimal.

    Returns if the value is a valid Decimal, or, in case it's a string,
    if it can be converted to an Decimal.
    """
    return _validate_type(Decimal, value)


def validate_directory(path):
    """Find out if a directory exists"""
    return os.path.exists(os.path.expanduser(path))


def validate_percentage(value):
    """Se if a given value is a valid percentage.

    Works for int, float, Decimal and basestring (if it
    can be converted to Decimal).
    """
    if isinstance(value, str):
        try:
            value = converter.from_string(Decimal, value)
        except ValidationError:
            return False

    return 0 <= value <= 100


def validate_email(value):
    """Try to validate an email address.
    """
    exp = r"^[^@]+@[a-zA-Z0-9][\w\.-]*[a-zA-Z0-9]\.[a-zA-Z][a-zA-Z\.]*[a-zA-Z]$"
    return re.match(exp, value) is not None


def validate_cst(cst):
    """Try to validate a CST to PIS/COFINS tax."""
    valid_cst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 49, 50, 51, 52, 53, 54, 55, 56, 60,
                 61, 62, 63, 64, 65, 66, 67, 70, 71, 72, 73, 74, 75, 98, 99]
    if cst in valid_cst:
        return True

    return False


def validate_invoice_key(key):
    if len(key) != 44:
        return False

    return int(key[-1]) == modulo11(key[:-1])


def validate_vehicle_license_plate(value):
    """Validate Vehicle License Plate"""
    if len(value) not in (6, 7):
        return False

    # Despite most license plates are in uppercase, we should allow lowercase
    exp = '^[a-zA-Z]{2,3}[0-9]{4}|[a-zA-Z]{3,4}[0-9]{3}$'
    return re.match(exp, value)
