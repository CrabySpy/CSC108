"""CSC108: Fall 2025 -- Assignment 3: arxiv.org metadata

Copyright and Usage Information
===============================

This code is provided solely for the personal and private use of students
taking CSC108 at the University of Toronto. Copying for purposes other than
this use is expressly prohibited. All forms of distribution of this code, 
whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2025 CSC108H1 Teaching Team
"""

from io import StringIO
import pytest
import checker_generic as checker

try:
    import arxiv_functions as arxiv
except ImportError:
    pass

MODULENAME = 'arxiv_functions'
PYTA_CONFIG = 'a3_pyta.json'
TARGET_LEN = 79
SEP = '='

CONSTANTS = {
    'ID': 'identifier',
    'TITLE': 'title',
    'CREATED': 'created',
    'MODIFIED': 'modified',
    'AUTHORS': 'authors',
    'ABSTRACT': 'abstract',
    'END': 'END'
}

DATA_FILE = """0001
Cats and Dogs Can Co-Exist
2023-08-20
2023-10-02
Smith,Jacqueline E.
Sharmin,Sadia

We show a formal proof that cats and dogs
can peacefully co-exist!
END
108
CSC108 is the Best Course Ever
2023-09-01

Smith,Jacqueline E.
Zavaleta-Bernuy,Angela 
Campbell,Jen

We present clear evidence that Introduction to
Computer Programming is the best course
END
"""

DATA_DICT = {'0001': {
    CONSTANTS['ID']: '0001',
    CONSTANTS['TITLE']: 'Cats and Dogs Can Co-Exist',
    CONSTANTS['CREATED']: '2023-08-20',
    CONSTANTS['MODIFIED']: '2023-10-02',
    CONSTANTS['AUTHORS']: [('Smith', 'Jacqueline E.'), ('Sharmin', 'Sadia')],
    CONSTANTS['ABSTRACT']: 'We show a formal proof that cats and dogs\n' +
    'can peacefully co-exist!'},
'108': {
    CONSTANTS['ID']: '108',
    CONSTANTS['TITLE']: 'CSC108 is the Best Course Ever',
    CONSTANTS['CREATED']: '2023-09-01',
    CONSTANTS['MODIFIED']: '',
    CONSTANTS['AUTHORS']: [('Smith', 'Jacqueline E.'), ('Zavaleta-Bernuy', 'Angela'),
              ('Campbell', 'Jen')],
    CONSTANTS['ABSTRACT']: 'We present clear evidence that Introduction to\n'
    + 'Computer Programming is the best course'}
}


class TestChecker:
    """A simple checker (NOT a full tester!) for assignment functions."""

    def test_contains_keyword(self) -> None:
        """A simple check for contains_keyword."""
        self._check_list_of_type(arxiv.contains_keyword,
                                 [DATA_DICT, 'is'], str)

    def test_created_in_year(self) -> None:
        """A simple check for created_in_year."""

        self._check_simple_type(arxiv.created_in_year,
                                [DATA_DICT, '008', 2021], bool)
        
    def test_average_author_count(self) -> None:
        """A simple check for average_author_count."""
        self._check_simple_type(arxiv.average_author_count, [DATA_DICT], float)

    def test_read_arxiv_file(self) -> None:
        """A simple check for read_arxiv_file."""

        print('\nChecking read_arxiv_file...')

        result = checker.returns_dict_of(
            arxiv.read_arxiv_file, [StringIO(DATA_FILE)], str, dict)
        assert result[0] is True, result[1]

        valid_keys = {'identifier', 'title', 'created', 'modified',
                      'authors', 'abstract'}
        msg = 'Value corresponding to key "{}" should be a {}.'
        for article in result[1].values():
            assert isinstance(article['authors'], list) and \
                            _all_names(article['authors']), \
                            msg.format('authors', 'list of names')
            for key in valid_keys - {'authors'}:
                assert article[key] is None or \
                                isinstance(article[key], str), \
                                msg.format(key, 'str or None')

        print('  check complete')

    def test_make_author_to_article(self) -> None:
        """A simple check for make_author_to_articles."""

        print('\nChecking make_author_to_articles...')

        result = checker.type_check_simple(
            arxiv.make_author_to_articles, [DATA_DICT], dict)
        assert result[0] is True, result[1]

        msg = ('make_author_to_articles should return a dict in which\n'
               'keys are names (Tuple[str, str]) and values are lists of\n'
               'article IDs (List[str]).')

        for key, value in result[1].items():
            assert _is_name(key) and \
                            isinstance(value, list) and \
                            all(isinstance(elt, str) for elt in value), \
                            msg

        print('  check complete')

    def test_get_coauthors(self) -> None:
        """A simple check for get_coauthors."""

        self._check_list_of_names(arxiv.get_coauthors,
                                  [DATA_DICT, ('Smith', 'Jacqueline E.')])

    def test_get_most_published_authors(self) -> None:
        """A simple check for get_most_published_authors."""

        self._check_list_of_names(arxiv.get_most_published_authors,
                                  [DATA_DICT])

    def test_suggest_collaborators(self) -> None:
        """A simple check for suggest_collaborators."""

        self._check_list_of_names(arxiv.suggest_collaborators,
                                  [DATA_DICT, ('Smith', 'Jacqueline E.')])

    def test_has_prolific_authors(self) -> None:
        """A simple check for has_prolific_authors."""

        by_author = {
            ('Campbell', 'Jen'): ['108'],
            ('Sharmin', 'Sadia'): ['0001'],
            ('Smith', 'Jacqueline E.'): ['0001', '108'],
            ('Zavaleta-Bernuy', 'Angela'): ['108']
        }

        self._check_simple_type(arxiv.has_prolific_authors,
                                [by_author, DATA_DICT['108'], 2],
                                bool)

    def test_keep_prolific_authors(self) -> None:
        """A simple check for keep_prolific_authors: only checks that the
        return value is None."""

        self._check_simple_type(arxiv.keep_prolific_authors,
                                [DATA_DICT, 2],
                                type(None))

    def test_check_constants(self) -> None:
        """Check that values of constants are not changed."""

        print('\nChecking that constants refer to their original values')
        self._check_constants(CONSTANTS, arxiv)
        print('  check complete')

    def _check_list_of_names(self, func: callable, args: list) -> None:
        """Check that func called with arguments args returns a
        List[constants.NameType]. Display progress and outcome of the
        check.

        """

        print('\nChecking {}...'.format(func.__name__))

        result = checker.type_check_simple(func, args, list)
        assert result[0] is True, result[1]

        msg = ('{} should return a list of tuples of two strs:\n'
               '[(lastname1, firstname1), (lastname2, firstname2), ...]\n'
               'Test your function thoroughly!').format(func.__name__)
        assert _all_names(result[1]) is True, msg

        print('  check complete')

    def _check_simple_type(self, func: callable, args: list,
                           expected: type) -> None:
        """Check that func called with arguments args returns a value of type
        expected. Display the progress and the result of the check.

        """

        print('\nChecking {}...'.format(func.__name__))
        result = checker.type_check_simple(func, args, expected)
        assert result[0] is True, result[1]
        print('  check complete')

    def _check_list_of_type(self, func: callable, args: list, typ: type) -> None:
        """Check that func called with arguments args returns a list with
        values of the type expected. Display the progress and the result of
        the check.
        """

        print('\nChecking {}...'.format(func.__name__))
        result = checker.returns_list_of(func, args, typ)
        assert result[0] is True, result[1]
        print('  check complete')

    def _check_constants(self, name2value: dict[str, any], mod: any) -> None:
        """Check that, for each (name, value) pair in name2value, the value of
        a variable named name in module mod is value.

        """

        for name, expected in name2value.items():
            actual = getattr(mod, name)
            msg = 'The value of {} should be {} but is {}.'.format(
                name, expected, actual)
            assert expected == actual, msg


def _all_names(obj: any) -> bool:
    """Return whether every item in obj is of type constants.NameType."""

    return all(_is_name(name) for name in obj)


def _is_name(obj: any) -> bool:
    """Return whether obj is a name, i.e. a Tuple[str, str]."""

    return (isinstance(obj, tuple) and len(obj) == 2 and
            isinstance(obj[0], str) and isinstance(obj[1], str))


checker.ensure_no_io(MODULENAME)

print(''.center(TARGET_LEN, SEP))
print(' Start: checking coding style '.center(TARGET_LEN, SEP))
checker.run_pyta(MODULENAME + '.py', PYTA_CONFIG)
print(' End checking coding style '.center(TARGET_LEN, SEP))

print(' Start: checking type contracts '.center(TARGET_LEN, SEP))
pytest.main(['--show-capture', 'no', '--disable-warnings', '--tb=short',
             'a3_checker.py', "--capture=sys", "-W", "ignore:Module already imported:pytest.PytestWarning"])

print(' End checking type contracts '.center(TARGET_LEN, SEP))

print('\nScroll up to see ALL RESULTS:')
print('  - checking coding style')
print('  - checking type contract\n')
