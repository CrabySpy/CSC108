"""CSC108: Fall 2025 -- Assignment 3: arxiv.org metadata

Instructions (READ THIS FIRST!)
===============================

Make sure that the files constants.py, a3_checker.py, and checker_generic.py
are in the same directory as this file.


Copyright and Usage Information
===============================

This code is provided solely for the personal and private use of students
taking CSC108 at the University of Toronto. Copying for purposes other than
this use is expressly prohibited. All forms of distribution of this code, 
whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2025 CSC108H1 Teaching Team
"""

import pprint # needed to format output
import copy  # needed in examples of functions that modify input dict
from typing import TextIO
from constants import (ID, TITLE, CREATED, MODIFIED, AUTHORS, ABSTRACT, END,
                       NameType, ArticleType, ArxivType)

##############################################################################
# Sample data for use in docstring examples
##############################################################################

# NOTE: Some dictionary keys are set using the values of provided constants.

EXAMPLE_ARXIV = {
    '5090': {
        ID: '5090',
        TITLE: "Increasing Students' Engagement to Reminder Emails",
        CREATED: '',
        MODIFIED: '2022-08-02',
        AUTHORS: [('Yanez', 'Fernando'), ('Zavaleta-Bernuy', 'Angela')],
        ABSTRACT: 'Our metric of interest is open email rates.'},
    '03221': {
        ID: '03221',
        TITLE: 'Stargazer: An Interactive Camera Robot for How-To Videos',
        CREATED: '2023-03-01',
        MODIFIED: '2023-03-06',
        AUTHORS: [('Grossman', 'Tovi')],
        ABSTRACT: 'We present Stargazer, a novel approach for assisting ' +
                  'with tutorial content creation.'},
    '0001': {
        ID: '0001',
        TITLE: 'Cats and Dogs Can Co-Exist',
        CREATED: '2023-08-20',
        MODIFIED: '2023-10-02',
        AUTHORS: [('Smith', 'Jacqueline E.'), ('Sharmin', 'Sadia')],
        ABSTRACT: 'We show a formal proof that cats and dogs\n' +
        'can peacefully co-exist!'},
    '108': {
        ID: '108',
        TITLE: 'CSC108 is the Best Course Ever',
        CREATED: '2023-09-01',
        MODIFIED: '',
        AUTHORS: [('Smith', 'Jacqueline E.'), ('Zavaleta-Bernuy', 'Angela'),
                  ('Campbell', 'Jen')],
        ABSTRACT: 'We present clear evidence that Introduction to\n'
        + 'Computer Programming is the best course'},
    '42': {
        ID: '42',
        TITLE: '',
        CREATED: '2023-05-04',
        MODIFIED: '2023-05-05',
        AUTHORS: [],
        ABSTRACT: 'This is a strange article with no title\n'
        + 'and no authors.\n\nIt also has a blank line in its abstract!'}
}

EXAMPLE_BY_AUTHOR = {
    ('Campbell', 'Jen'): ['108'],
    ('Grossman', 'Tovi'): ['03221'],
    ('Sharmin', 'Sadia'): ['0001'],
    ('Smith', 'Jacqueline E.'): ['0001', '108'],
    ('Yanez', 'Fernando'): ['5090'],
    ('Zavaleta-Bernuy', 'Angela'): ['108', '5090']
}


###############################################################################
# Helper function to use in your code later on.  Do not change this function.
###############################################################################
def clean_word(word: str) -> str:
    """Return word with all non-alphabetic characters removed and converted to 
    lowercase.
    
    Precondition: word contains no whitespace
    
    >>> clean_word('Hello!!!')
    'hello'
    >>> clean_word('12cat.dog?')
    'catdog'
    >>> clean_word("DON'T")
    'dont'
    """
    new_word = ''
    for ch in word:
        if ch.isalpha():
            new_word = new_word + ch.lower()
    return new_word


###############################################################################
# Task 1 - Working with ArxivType
###############################################################################
# TODO write your functions for Task 1 here
def created_in_year(metadata: ArxivType, article_id: str, published_year: int) -> bool:
    """Return True if and only if an article with the provided id occurs in the metadata and was published in the 
    given year.

    >>> example_arxiv = EXAMPLE_ARXIV
    >>> created_in_year(example_arxiv, "108", 2023)
    True
    >>> example_arxiv = EXAMPLE_ARXIV
    >>> created_in_year(example_arxiv, "323", 2023)
    False
    """

    year = 0

    if article_id in metadata:

        date = metadata[article_id][CREATED]
        year = int(date[:4])

    return year == published_year

def contains_keyword(metadata: ArxivType, keyword: str) -> list[str]:
    """Return a list of the IDs of articles that contain the given keyword 
    in their title, author names, and/or abstract. 

    >>> example_arxiv = EXAMPLE_ARXIV
    >>> contains_keyword(example_arxiv, "is")
    ['108', '42', '5090']
    >>> example_arxiv = EXAMPLE_ARXIV
    >>> contains_keyword(example_arxiv, "apple")
    []
    """

    result = []
    for article_key in metadata:
        if metadata[article_key][ID] not in result:
            
            words = create_list_of_words(metadata, article_key)
            clean_list_of_words(words)
            
            if keyword in words:
                result.append(metadata[article_key][ID])

    result.sort()

    return result

def create_list_of_words(metadata: ArxivType, article_key: str) -> list[str]:
    """Return a list of words contain all words from the article's title, author names, and abstract."""

    title_words = metadata[article_key][TITLE].split()

    authors_words = []
    for author in metadata[article_key][AUTHORS]:
        for name in author:
            authors_words.append(name)

    abstract_words = metadata[article_key][ABSTRACT].split()

    all_words = title_words + authors_words + abstract_words

    return all_words

def clean_list_of_words(words: list[str]) -> None:
    """Clean all words in list words with all non-alphabetic characters removed and converted to 
    lowercase.
    
    >>> words = ['Hello!!!', '12cat.dog?', "DON'T"]
    >>> clean_list_of_words(words)
    >>> words
    ['hello', 'catdog', 'dont']

    >>> words = ['ABC-d123', '000', '']
    >>> clean_list_of_words(words)
    >>> words
    ['abcd', '', '']
    """

    for i in range(len(words)):
        words[i] = clean_word(words[i])
    
def average_author_count(metadata: ArxivType,) -> float:
    """Return the average number of authors per article in the arxiv metadata.
    
    >>> example_arxiv = EXAMPLE_ARXIV
    >>> average_author_count(example_arxiv)
    1.6
    >>> example_arxiv = EXAMPLE_ARXIV
    >>> average_author_count(example_arxiv)
    1.6
    """

    num_of_article = 0
    num_of_authors = 0
    
    for article_key in metadata:
        num_of_article += 1
        for author in metadata[article_key][AUTHORS]:
            num_of_authors += 1

    if num_of_article == 0:
        return 0.0
    
    return num_of_authors / num_of_article

###############################################################################
# Task 2 - Reading in the arxiv metadata
###############################################################################

def read_arxiv_file(f: TextIO) -> ArxivType:
    """Return an ArxivType dictionary containing the arxiv metadata in f.

    Note: example calls for functions that take open files are not necessary.
    """

    # TODO write the body of the function here
    

# TODO write any helper functions you need for Task 2 here


###############################################################################
# Task 3 - Working with Authors and Coauthors
###############################################################################

def make_author_to_articles(id_to_article: ArxivType
                            ) -> dict[NameType, list[str]]:
    """Return a dict that maps each author name to a list (sorted in
    lexicographic order) of IDs of articles written by that author,
    based on the information in id_to_article.

    >>> make_author_to_articles(EXAMPLE_ARXIV) == EXAMPLE_BY_AUTHOR
    True
    >>> make_author_to_articles({})
    {}
    """
    # We have provided the docstring for this function as an example of how
    # to compare dictionaries in a docstring example

    # TODO write the body of the function here


# TODO write the rest of your Task 3 functions here


###############################################################################
# Task 4 - Prolific Authors
###############################################################################


# TODO write your Task 4 functions here

def keep_prolific_authors(id_to_article: ArxivType,
                          min_publications: int) -> None:
    """Update id_to_article so that it contains only articles published by
    authors with min_publications or more articles published. As long
    as at least one of the authors has min_publications, the article
    is kept.

    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 2)
    >>> len(arxiv_copy)
    3
    >>> '108' in arxiv_copy and '5090' in arxiv_copy and '0001' in arxiv_copy
    True
    >>> arxiv_copy = copy.deepcopy(EXAMPLE_ARXIV)
    >>> keep_prolific_authors(arxiv_copy, 3)
    >>> arxiv_copy
    {}
    """

    # We have provided you with this docstring as an example of how to use 
    # the function copy.deepcopy in docstring examples for functions that
    # modify an argument.

    # TODO write the body of the function here


if __name__ == '__main__':

    pass  # do not delete or comment out this line

    # uncomment the lines below to run doctest on your code
    # note that doctest requires your docstring examples to be perfectly
    # formatted, and we will not be running doctest on your code
    import doctest
    doctest.testmod()

    # uncomment the lines below to work with the small data set
    # example_data = open('example_data.txt')
    # example_arxiv = read_arxiv_file(example_data)
    # example_data.close()
    # if example_arxiv == EXAMPLE_ARXIV:
    #     print('The dict returned by read_arxiv_file matches EXAMPLE_ARXIV!')
    #     print('This is a good sign, but do more of your own testing!')
    # else:
    #     # If you are getting this message, try setting a breakpoint on the line
    #     # that calls read_arxiv_file above and running the debugger
    #     print('Not quite! You got:')
    #     pprint.pprint(example_arxiv)
    #     print()
    #     print('If you are getting this message, then the dictionary produced')
    #     print('by your read_arxiv_file function does not match the provided')
    #     print('EXAMPLE_ARXIV. Scroll up to see the dictionary your function')
    #     print('produced. You may want to write more testing code to help')
    #     print('figure out why it does not match.')


    # uncomment the lines below to work with a larger data set
    #large_file = open('data.txt')
    #large_data = read_arxiv_file(large_file)
    #large_file.close()

    #auth_to_articles = make_author_to_articles(large_data)
    #most_published_authors = get_most_published_authors(large_data)
    #print(most_published_authors)
    #print(get_coauthors(large_data, ('Varanasi', 'Mahesh K.')))  # one
    #print(get_coauthors(large_data, ('Chablat', 'Damien')))  # many
