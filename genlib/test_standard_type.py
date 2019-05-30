import json
import unittest

from standard_type import *


class TestStandardType(unittest.TestCase):
    def test_fail_to_create_when_no_types(self):
        testobj = StandardType()

        test_data = """ "test string" """
        obj = json.loads(test_data)

        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

    def test_create_boolean(self):
        testobj = StandardType()
        testobj.type = TypeConsts.Boolean

        test_data = """true"""
        obj = json.loads(test_data)
        testobj.load_from_object(obj)

        assert (testobj.value is True)

        test_data = """false"""
        obj = json.loads(test_data)
        testobj.load_from_object(obj)

        assert (testobj.value is False)

    def test_create_boolean_cant_be_number_or_string(self):
        testobj = StandardType()
        testobj.type = TypeConsts.Boolean

        test_data = """0"""
        obj = json.loads(test_data)
        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

        test_data = """1"""
        obj = json.loads(test_data)
        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

        test_data = """ "true" """
        obj = json.loads(test_data)
        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

    def test_create_string(self):
        testobj = StandardType()
        testobj.type = TypeConsts.String

        test_data = """ "test string" """
        obj = json.loads(test_data)
        testobj.load_from_object(obj)

        assert (testobj.value == "test string")

    def test_create_string_regex_does_match(self):
        testobj = StandardType()
        testobj.type = TypeConsts.String
        testobj.pattern = "[0-9][0-9][0-9]\\.[0-9][0-9]"

        test_data = """ "350.00" """
        obj = json.loads(test_data)
        testobj.load_from_object(obj)

        assert (testobj.value == "350.00")

    def test_create_string_regex_does_not_match(self):
        testobj = StandardType()
        testobj.type = TypeConsts.String
        testobj.pattern = "[0-9][0-9][0-9]\\.[0-9][0-9]$"

        test_data = """ "350.XX" """
        obj = json.loads(test_data)

        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

        test_data = """ "350.000" """
        obj = json.loads(test_data)

        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

    def test_create_multiple_types(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String, TypeConsts.Number]

        test_data = """ "350.00" """
        obj = json.loads(test_data)
        testobj.load_from_object(obj)
        self.assertEqual("350.00", testobj.value)

        test_data = """350"""
        obj = json.loads(test_data)
        testobj.load_from_object(obj)
        self.assertEqual(350, testobj.value)

    def test_create_multiple_types_fails(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String, TypeConsts.String]

        test_data = """350"""
        obj = json.loads(test_data)

        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

    def test_supports_minimum_field_for_number_type(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.Number]
        testobj.minimum = 351

        test_data = """350"""
        obj = json.loads(test_data)

        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

    def test_supports_maximum_field_for_number_type(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.Number]
        testobj.maximum = 349

        test_data = """350"""
        obj = json.loads(test_data)

        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

    def test_maximum_and_minimum_values_are_not_invalid(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.Number]

        # Maximum can't be less then the Minimum
        testobj.minimum = 351
        with self.assertRaises(ValueError):
            testobj.maximum = 350

        # Reset the Maximum and the Minimum
        testobj.minimum = None
        testobj.maximum = None

        # Minimum and maximum should be valid as the same.
        testobj.minimum = 351
        testobj.maximum = 351

        # Reset the Maximum and the Minimum
        testobj.minimum = None
        testobj.maximum = None

        # Maximum should can be set independently.
        testobj.maximum = 50

    def test_handles_const(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.const = "THIS IS A STRING"

        self.assertEqual(testobj.value, "THIS IS A STRING")

    def test_handles_const_setting(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.const = "THIS IS A STRING"

        with self.assertRaises(ValueError):
            testobj.value = "XXXXXX"

    def test_enumerations(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.enumerations = ["A", "B", "C"]

        testobj.value = "A"
        self.assertEqual("A", testobj.value)

        testobj.value = "B"
        self.assertEqual("B", testobj.value)

        testobj.value = "C"
        self.assertEqual("C", testobj.value)

    def test_enumerations_does_not_match(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.enumerations = ["A", "B", "C"]

        test_data = """350"""
        obj = json.loads(test_data)

        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

    def test_enumerations_throws_invalid_types(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        with self.assertRaises(ValueError):
            testobj.enumerations = {"not a valid enumeration type": 0}

    def test_enumerations_accepts_single_enumerations(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.enumerations = "valid enumeration type"

        test_data = """ "valid enumeration type" """
        obj = json.loads(test_data)
        testobj.load_from_object(obj)

        self.assertEqual(testobj.value, "valid enumeration type")

    def test_string_throws_on_bad_format(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "bad_format_keyword"

        test_data = """ "djflskjdflk" """
        obj = json.loads(test_data)
        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

    def test_string_format_datetime(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "date-time"

        test_data = """ "2018-11-13T20:20:39+00:00" """
        obj = json.loads(test_data)
        testobj.load_from_object(obj)

    def test_string_format_date(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "date"

        test_data = """ "2018-11-13" """
        obj = json.loads(test_data)
        testobj.load_from_object(obj)

    def test_string_format_time(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "time"

        test_data = """ "20:20:39+00:00" """
        obj = json.loads(test_data)
        testobj.load_from_object(obj)

    def test_string_format_email_rfc5322(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "email"

        test_data = """ "email@knockrentals.com" """
        obj = json.loads(test_data)
        testobj.load_from_object(obj)

    def test_string_format_email_rfc6531_not_supported(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "email"

        test_data = """ "john.smith@(comment)example.com" """
        obj = json.loads(test_data)
        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

    def test_string_format_throw_bad_email(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "email"

        test_data = """ "bad_email@.com" """
        obj = json.loads(test_data)
        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

    def test_string_format_hostname_valid(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "hostname"

        test_data = """ "knockrentals.com" """
        obj = json.loads(test_data)
        testobj.load_from_object(obj)

    def test_string_format_hostname_invalid(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "hostname"

        test_data = """ "knockrentals.-.x.com" """
        obj = json.loads(test_data)
        with self.assertRaises(ValueError):
            testobj.load_from_object(obj)

    def test_string_format_ipv4_valid_tests(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "ipv4"

        tests = [
            "127.0.0.1",
            "192.168.1.1",
            "192.168.1.255",
            "255.255.255.255",
            "0.0.0.0",
            "1.1.1.01"
        ]

        for test in tests:
            test_data = f""" "{test}" """
            obj = json.loads(test_data)
            testobj.load_from_object(obj)

    def test_string_format_ipv4_invalid_tests(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "ipv4"

        tests = [
            "30.168.1.255.1",
            "127.1",
            "192.168.1.256",
            "-1.2.3.4",
            "3...3"
        ]

        for test in tests:
            test_data = f""" "{test}" """
            obj = json.loads(test_data)
            with self.assertRaises(ValueError):
                testobj.load_from_object(obj)

    def test_string_format_ipv6_invalid_tests(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "ipv6"

        tests = [
            "1200::AB00:1234::2552:7777:1313",
            "1200:0000:AB00:1234:O000:2552:7777:1313"
        ]

        for test in tests:
            test_data = f""" "{test}" """
            obj = json.loads(test_data)
            with self.assertRaises(ValueError):
                testobj.load_from_object(obj)

    def test_string_format_ipv6_valid_tests(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "ipv4"

        tests = [
            "1200:0000:AB00:1234:0000:2552:7777:1313",
            "21DA:D3:0:2F3B:2AA:FF:FE28:9C5A"
        ]

        for test in tests:
            test_data = f""" "{test}" """
            obj = json.loads(test_data)
            testobj.load_from_object(obj)

    def test_string_format_valid_uris(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "uri"

        tests = [
            "http://www.google.com",
            "http://microsoft.com"
        ]

        for test in tests:
            test_data = f""" "{test}" """
            obj = json.loads(test_data)
            testobj.load_from_object(obj)

    def test_string_format_invalid_uris(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "uri"

        tests = [
            "xxx.xxx.xxx.xxx",
            "192.168.0.1",
            "http://fdasdf.fdsfîășîs.fss/ăîăî"
        ]

        for test in tests:
            test_data = f""" "{test}" """
            obj = json.loads(test_data)
            with self.assertRaises(ValueError):
                testobj.load_from_object(obj)

    def test_string_format_valid_iris(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "iri"

        tests = [
            "http://fdasdf.fdsfîășîs.fss/ăîăî",
            "http://microsoft.com"
        ]

        for test in tests:
            test_data = f""" "{test}" """
            obj = json.loads(test_data)
            testobj.load_from_object(obj)

    def test_string_format_invalid_iris(self):
        testobj = StandardType()
        testobj.type = [TypeConsts.String]

        testobj.format = "iri"

        tests = [
            "xxx.xxx.xxx.xxx",
            "192.168.0.1"
        ]

        for test in tests:
            test_data = f""" "{test}" """
            obj = json.loads(test_data)
            with self.assertRaises(ValueError):
                testobj.load_from_object(obj)


if __name__ == '__main__':
    unittest.main()
