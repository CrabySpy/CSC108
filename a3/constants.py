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

from typing import TypedDict

##############################################################################
# Constants and Types
##############################################################################

ID = 'identifier'
TITLE = 'title'
CREATED = 'created'
MODIFIED = 'modified'
AUTHORS = 'authors'
ABSTRACT = 'abstract'
END = 'END'

# We store names as tuples of two strs: (last-name, first-name(s)).
NameType = tuple[str, str]

# ArticleType is a dict with keys ID, TITLE, CREATED, MODIFIED,
# AUTHORS, and ABSTRACT.
# Note: each key is a str (the value of a constant shown above)
ArticleType = TypedDict('ArticleType', {
    ID: str,
    TITLE: str,
    CREATED: str,
    MODIFIED: str,
    AUTHORS: list[NameType],
    ABSTRACT: str
})

# ArxivType is a dict that maps article identifiers to articles,
# i.e. to values of type ArticleType.
ArxivType = dict[str, ArticleType]