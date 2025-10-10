"""A simple checker for types of functions in bridge_functions.py

Copyright and Usage Information
===============================

This code is provided solely for the personal and private use of students 
taking the CSC108H1 course at the University of Toronto. Copying for purposes 
other than this use is expressly prohibited. All forms of distribution of 
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2025 CSC108H1 Teaching Team
"""

import checker_generic
import pytest

try:
    import bridge_functions as bf
except ImportError:
    pass


FILENAME = 'bridge_functions.py'
PYTA_CONFIG = 'a2_pyta.json'
TARGET_LEN = 79
SEP = '='

CONSTANTS = {
    'COLUMN_ID': 0,
    'COLUMN_NAME': 1,
    'COLUMN_HIGHWAY': 2,
    'COLUMN_LAT': 3,
    'COLUMN_LON': 4,
    'COLUMN_YEAR_BUILT': 5,
    'COLUMN_LAST_MAJOR_REHAB': 6,
    'COLUMN_LAST_MINOR_REHAB': 7,
    'COLUMN_NUM_SPANS': 8,
    'COLUMN_SPAN_DETAILS': 9,
    'COLUMN_DECK_LENGTH': 10,
    'COLUMN_LAST_INSPECTED': 11,
    'COLUMN_BCI': 12,
    'INDEX_BCI_YEARS': 0,
    'INDEX_BCI_SCORES': 1,
    'MISSING_BCI': -1.0,
    'EARTH_RADIUS': 6371,
}


def _check(func: callable, args: list, expected: type) -> tuple[bool, object]:
    """Check if a call to func(args) returns a result with type expected.

    Return (True, result-of-call) if the check succeeds.
    Return (False, error-or-failure-message) if anything goes wrong.
    """
    try:
        returned = func(*args)
    except Exception as exn:
        return False, _error_message(func, args, exn)

    if isinstance(returned, expected):
        return True, returned

    return False, _type_error_message(func, expected.__name__, returned)


def _check_nested_type(func: callable, args: list, tp: type):
    """Check if func(args) returns a list of elements of type tp.

    Return (True, result-of-call) if the check succeeds.
    Return (False, error-or-failure-message) if anything goes wrong.

    """

    success, result = _check(func, args, list)
    if not success:
        return False, result

    msg = _type_error_message(func, 'list of {}s'.format(tp.__name__), result)

    for item in result:
        if not isinstance(item, tp):
            return False, msg

    return True, result


def _type_error_message(func: callable, expected: str, got: object) -> str:
    """Return an error message for function func returning got, where the
    correct return type is expected.
    """
    return f'{func.__name__} should return a {expected}, but ' \
           f'instead it returned {got}.'


def _error_message(func: callable, args: list, error: Exception) -> str:
    """Return an error message: func(args) raised an error."""
    args = str.join(',', map(str, args))
    return f'The call {func.__name__}({args}) caused an error: {error}'


class TestChecker:
    """Sanity checker for assignment functions."""
    module = bf

    def create_example_bridge_1(self) -> list:
        """Return a bridge in our list-format to use for doctest examples.

        This bridge is the same as the bridge from row 3 of the dataset.
        """

        return [
            1, 'Highway 24 Underpass at Highway 403',
            '403', 43.167233, -80.275567, '1965', '2014', '2009', 4,
            [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012',
            [['2013', '2012', '2011', '2010', '2009', '2008', '2007',
              '2006', '2005', '2004', '2003', '2002', '2001', '2000'],
             [-1.0, 72.3, -1.0, 69.5, -1.0, 70.0, -1.0,
              70.3, -1.0, 70.5, -1.0, 70.7, 72.9, -1.0]]
        ]

    def create_data(self) -> None:
        """Create some test data that can be reused."""
        self.test_bridge = self.create_example_bridge_1()
        self.bridge_copy = self.create_example_bridge_1()

    def test_find_bridge_by_id(self) -> None:
        """Check the type contract of function find_bridge_by_id."""
        self.create_data()
        self._check(bf.find_bridge_by_id, [[self.test_bridge], 1], list)
        self._check_no_mutation(bf.find_bridge_by_id, self.test_bridge,
                                self.bridge_copy)

    def test_find_bridges_in_radius(self) -> None:
        """Check the type contract of function find_bridges_in_radius."""
        self.create_data()
        self._check(bf.find_bridges_in_radius, [[self.test_bridge], 43.10,
                                                -80.15, 50, []], int, True)
        self._check_no_mutation(bf.find_bridges_in_radius, self.test_bridge,
                                self.bridge_copy)

    def test_get_bridge_condition(self) -> None:
        """Check the type contract of function get_bridge_condition."""
        self.create_data()
        self._check(bf.get_bridge_condition, [[self.test_bridge], 1], float)
        self._check_no_mutation(bf.get_bridge_condition, self.test_bridge,
                                self.bridge_copy)

    def test_calculate_average_condition(self) -> None:
        """Check the type contract of function calculate_average_condition."""
        self.create_data()
        self._check(bf.calculate_average_condition,
                    [self.test_bridge, 2011, 2013], float)
        self._check_no_mutation(bf.get_bridge_condition, self.test_bridge,
                                self.bridge_copy)

    def test_inspect_bridge(self) -> None:
        """Check the type contract of function inspect_bridge."""
        self.create_data()
        self._check(bf.inspect_bridge,
                    [[self.test_bridge], 1, '02/14/2021', 0.0],
                    type(None))
        self._check_mutation(bf.inspect_bridge, self.test_bridge,
                             self.bridge_copy)

    def test_rehabilitate_bridge(self) -> None:
        """Check the type contract of function rehabilitate_bridge."""
        self.create_data()
        self._check(bf.rehabilitate_bridge, [[self.test_bridge], [1], '', False],
                    type(None))
        self._check_mutation(bf.rehabilitate_bridge, self.test_bridge, self.bridge_copy)

    def test_find_worst_bci(self) -> None:
        """Check the type contract of function find_worst_bci."""
        self.create_data()
        self._check(bf.find_worst_bci, [[self.test_bridge], [1]], int)
        self._check_no_mutation(bf.find_worst_bci, self.test_bridge,
                                self.bridge_copy)

    def test_map_route(self) -> None:
        """Check the type contract of function map_route."""
        self.create_data()
        self._check(bf.map_route, [[self.test_bridge], 43.10, -80.15, 3, 500],
                    int, True)
        self._check_no_mutation(bf.map_route, self.test_bridge,
                                self.bridge_copy)

    def test_clean_span_data(self) -> None:
        """Check the type contract of function clean_span_data."""
        self.create_data()
        self._check(bf.clean_span_data,
                    ['Total=64  (1)=12;(2)=19;(3)=21;(4)=12;'], float, True)

    def test_clean_length_data(self) -> None:
        """Check the type contract of function clean_length_data."""
        self.create_data()
        self._check(bf.clean_length_data, ['1'], float)

    def test_clean_bci_data(self) -> None:
        """Check the type contract of function clean_bci_data."""
        self.create_data()
        my_years = []
        my_scores = ['', '71.5']
        scores_copy = my_scores.copy()

        self._check(bf.clean_bci_data, [my_years, 2013, my_scores], type(None))
        self._check_mutation(bf.clean_bci_data, my_scores, scores_copy)
        self._check_mutation(bf.clean_bci_data, my_years, [])

    def test_trim_from_end(self) -> None:
        """Check the type contract of function trim_from_end."""
        self.create_data()
        my_lst = ['72.3', '']
        my_copy = my_lst.copy()

        self._check(bf.trim_from_end, [my_lst, 1], type(None))
        self._check_mutation(bf.trim_from_end, my_lst, my_copy)

    def _check(self, func: callable, args: list, desired_type: type,
               nested: bool = False) -> None:
        """Check that func called with arguments args returns a value of type
        ret_type. Display the progress and the result of the check.
        """
        if not nested:
            result, message = _check(func, args, desired_type)
        else:
            result, message = _check_nested_type(func, args, desired_type)

        print(message)
        assert result is True, message

    def _check_no_mutation(self, func: callable, actual, expected) -> None:
        """Check that func does not mutate the argument actual so that it still
        matches expected.
        """
        assert expected == actual, '{0} should not mutate its arguments'.format(
            func.__name__)

    def _check_mutation(self, func: callable, actual, expected) -> None:
        """Check that func mutates the argument actual so that it is different
        from expected.
        """
        assert expected != actual, '{0} should mutate its list argument'.format(
            func.__name__)

    def test_check_constants(self) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.
        """

        for name, expected in CONSTANTS.items():
            actual = getattr(self.module, name)
            msg = 'The value of constant {} should be {} but is {}.'.format(
                name, expected, actual)
            assert expected == actual, msg


print(''.center(TARGET_LEN, SEP))
print(' Start: checking coding style with PythonTA '.center(TARGET_LEN, SEP))
checker_generic.run_pyta(FILENAME, PYTA_CONFIG)
print(' End checking coding style with PythonTA '.center(TARGET_LEN, SEP))

print(' Start: checking type contracts '.center(TARGET_LEN, SEP))
pytest.main(['--show-capture', 'no', '--disable-warnings', '--tb=short',
    'a2_checker.py', "--capture=sys", "-W", "ignore:Module already imported:pytest.PytestWarning"])
print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style with Python TA')
print('  - checking type contract\n')
