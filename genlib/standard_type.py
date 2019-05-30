"""
    Standard Type

    Standard Types are types of objects which can hold data, but also have other
    properties specified by the JSON Schema.
"""

import ipaddress

import aniso8601
import rfc3987
from fqdn import *

from consts import *


class StandardType(object):
    def __init__(self):
        super().__init__()
        # The defined type
        self.type = None
        # Maps in class property names to in file property names.
        self._property_names = {}
        # Value
        self._value = None
        # Pattern
        self._pattern = None

        # Minimum
        self._minimum = None
        # Maximum
        self._maximum = None

        # Const
        self._const = None
        # Enums
        self._enumerations = None

        # Format
        self._format = None

    def load_from_object(self, input_data):
        load_worked = False
        if type(self.type) is list:
            types = self.type
        else:
            types = [self.type]

        for vtype in types:
            load_worked = self.load_value_type(vtype, input_data)
            if load_worked:
                break

        if not load_worked:
            error_msg = f"'{input_data}' did not match any of the types {types}"
            raise (ValueError(error_msg))

    def load_value_type(self, vtype, input_data) -> bool:
        if vtype == TypeConsts.String and type(input_data) is str:
            self._value = input_data
            if self._pattern:
                p = re.compile(self._pattern)
                if not p.match(self._value):
                    raise ValueError("did not match pattern.")
            if self._format:
                self._parse_string_format(input_data)
            return True

        if vtype == TypeConsts.Number and (type(input_data) is float or
                                           type(input_data) is int):
            self._value = input_data
            if self._minimum:
                if self._value >= self._minimum:
                    return True
                else:
                    error_string = f"{self._value} is less then the Minimum of {self._minimum}"
                    raise ValueError(error_string)

            if self._maximum:
                if self._value <= self._maximum:
                    return True
                else:
                    error_string = f"{self._value} is greater then the Maximum of {self._maximum}"
                    raise ValueError(error_string)

            return True

        if vtype == TypeConsts.Boolean:
            if type(input_data) is not bool:
                error_string = f"{input_data} is not a boolean type"
                raise ValueError(error_string)
            self._value = input_data
            return True

        return False

    def dump_to_object(self, hide_empty=True):
        pass

    def _parse_string_format(self, input_data):
        if self._format in ["date-time", "time", "date"]:
            if self._format == "date-time":
                self._value = aniso8601.parse_datetime(input_data)
                return True
            if self._format == "date":
                self._value = aniso8601.parse_date(input_data)
                return True
            if self._format == "time":
                self._value = aniso8601.parse_time(input_data)
                return True

        if self._format in ["email", "idn-email"]:
            if self._format == "email":
                email_5621_pattern = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
                if re.match(email_5621_pattern, input_data):
                    return True
                errortext = f"""the supplied email '{input_data}' was not valid."""
                raise ValueError(errortext)

            if self._format == "idn-email":
                errortext = f"""the supplied idn-email format rfc-6531 is not supported"""
                raise ValueError(errortext)

        if self._format in ["hostname", "idn-hostname"]:
            if self._format == "hostname":
                if FQDN(input_data).is_valid:
                    return True
            if self._format == "idn-hostname":
                errortext = f"""the supplied idn-hostname format is not supported"""
                raise ValueError(errortext)

        if self._format in ["ipv4", "ipv6"]:
            ipaddress.ip_address(input_data)
            return True

        if self._format in ["uri", "iri"]:
            if self._format == "uri":
                if rfc3987.match(input_data, rule='URI'):
                    return True
                else:
                    errortext = f"url:'{input_data}' not a valid url."
                    raise ValueError(errortext)

            if self._format == "iri":
                if rfc3987.match(input_data, rule='IRI'):
                    return True
                else:
                    errortext = f"iri:'{input_data}' not a valid iri."
                    raise ValueError(errortext)

        errortext = f"""the string format type:'{self._format}' is not valid."""
        raise ValueError(errortext)

    @property
    def value(self):
        if self._const:
            return self.const
        return self._value

    @value.setter
    def value(self, newvalue):
        if self._const:
            raise ValueError("Const Object, you cannot change the value.")
        if self._enumerations:
            if newvalue not in self._enumerations:
                errorstring = f"Enumeration Object, the value '{newvalue}' must be one of:'{self._enumerations}'"
                raise ValueError(errorstring)
        self._value = newvalue

    @property
    def enumerations(self):
        return self._enumerations

    @enumerations.setter
    def enumerations(self, value):
        if value is None:
            self._enumerations = None
        if type(value) is not str and type(value) is not list and type(value) is not int:
            raise ValueError("Enumerations must be of type: List, String, or Int")
        if type(value) is not list:
            value = [value]
        self._enumerations = value

    @property
    def pattern(self):
        return self._pattern

    @pattern.setter
    def pattern(self, newvalue):
        self._pattern = newvalue

    @property
    def minimum(self):
        return self._minimum

    @minimum.setter
    def minimum(self, newvalue):
        if newvalue is None:
            self._minimum = None
            return

        if type(newvalue) is not int and type(newvalue) is not float:
            error_string = f"setting for minimum was an invalid type, needs to be numeric, not {str(type(newvalue))}"
            raise ValueError(error_string)

        if self._maximum is not None:
            if newvalue > self._maximum:
                error_string = f"Minimum of {newvalue} was greater then Maximum of {self._maximum}"
                raise ValueError(error_string)
        self._minimum = newvalue

    @property
    def maximum(self):
        return self._maximum

    @maximum.setter
    def maximum(self, newvalue):
        if newvalue is None:
            self._maximum = None
            return

        if type(newvalue) is not int and type(newvalue) is not float:
            error_string = f"setting for maximum was an invalid type, needs to be numeric, not {str(type(newvalue))}"
            raise ValueError(error_string)

        if self._minimum is not None:
            if newvalue < self._minimum:
                error_string = f"Minimum of {self._minimum} was greater then Maximum of {newvalue}"
                raise ValueError(error_string)
        self._maximum = newvalue

    @property
    def const(self):
        return self._const

    @const.setter
    def const(self, value):
        self._const = value

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, value):
        self._format = value
