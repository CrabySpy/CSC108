"""CSC108H1: Fall 2025 -- Assignment 1: Mystery Message Functions

Instructions (READ THIS FIRST!)
===============================

Make sure that the files a1_checker.py, a1_pyta.json, checker_generic.py
and mystery_message_game.py are in the same folder as this file
(mm_functions.py).

Copyright and Usage Information
===============================

This code is provided solely for the personal and private use of students 
taking the CSC108H1 course at the University of Toronto. Copying for purposes 
other than this use is expressly prohibited. All forms of distribution of 
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2025 CSC108H1 Teaching Team
"""

# points earned on each occurrence of a correctly guessed consonant
CONSONANT_POINTS = 1

# cost of buying a vowel, does not depend on the number of occurrences
VOWEL_COST = 1

# points earned on each occurrence of hidden consonants at the time of
# solving the puzzle
CONSONANT_BONUS = 2

# players' names
PLAYER_ONE = 'Player One'
PLAYER_TWO = 'Player Two'

# menu options
CONSONANT = 'C'  # guess a consonant
VOWEL = 'V'      # buy a vowel
SOLVE = 'S'      # try to solve the puzzle
QUIT = 'Q'       # quit the game

# symbol used for hidden characters
HIDDEN = '^'

# Game types
HUMAN = 'P1'             # one player, human
HUMAN_HUMAN = 'PVP'      # two players, human+human (player vs player)
HUMAN_COMPUTER = 'PVE'   # two players, human+computer (player vs environment)

# computer difficulty levels
EASY = 'E'  # computer plays the "easy" strategy
HARD = 'H'  # computer plays the "hard" strategy

# all consonants and all vowels
ALL_CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
ALL_VOWELS = 'aeiou'

# the order in which a computer player, hard difficulty level, will
# guess consonants
PRIORITY_CONSONANTS = 'tnrslhdcmpfygbwvkqxjz'


# We provide this function as an example.
# This function is already complete. You must not modify it.
def is_win(view: str, message: str) -> bool:
    """Return True if and only if message and view are a winning
    combination. That is, if and only if message and view are the same.

    >>> is_win('banana', 'banana')
    True
    >>> is_win('a^^le', 'apple')
    False
    >>> is_win('app', 'apple')
    False
    """

    return message == view


# We provide this function as an example of using a function as a helper.
# This function is already complete. You must not modify it.
def is_game_over(view: str, message: str, move: str) -> bool:
    """Return True if and only if message and view are a winning
    combination or move is QUIT.

    >>> is_game_over('a^^le', 'apple', VOWEL)
    False
    >>> is_game_over('a^^le', 'apple', 'Q')
    True
    >>> is_game_over('apple', 'apple', 'S')
    True
    """

    return move == QUIT or is_win(view, message)


# Helper function for computer_chooses_solve
# This function is already complete. You must not modify it.
def half_revealed(view: str) -> bool:
    """Return True if and only if at least half of the alphabetic
    characters in view are revealed.

    >>> half_revealed('')
    True
    >>> half_revealed('x')
    True
    >>> half_revealed('^')
    False
    >>> half_revealed('a^,^c!')
    True
    >>> half_revealed('a^b^^e ^c^d^^d')
    False
    """

    num_hidden = view.count(HIDDEN)
    num_alphabetic = 0
    for char in view:
        if char.isalpha():
            num_alphabetic = num_alphabetic + 1
    return num_alphabetic >= num_hidden


# Implement the required functions below.
#
# We have provided the complete docstring (but not the body!) for the first
# function you are to write.  Write a function body for the function
# is_human.
#
# The header and docstring of is_human is an example of where and how to use
# constants in the docstring. We use the default values of constants in
# the docstring examples, but must use the constants in the function body.

def is_human(current_player: str, game_type: str) -> bool:
    """Return True if and only if current_player represents a human in a
    game of type game_type.

    current_player is PLAYER_ONE or PLAYER_TWO.
    game_type is HUMAN, HUMAN_HUMAN, or HUMAN_COMPUTER.

    In a HUMAN game or a HUMAN_HUMAN game, a player is always
    human. In a HUMAN_COMPUTER game, PLAYER_ONE is human and
    PLAYER_TWO is computer.

    >>> is_human('Player One', 'P1')
    True
    >>> is_human('Player One', 'PVP')
    True
    >>> is_human('Player Two', 'PVP')
    True
    >>> is_human('Player One', 'PVE')
    True
    >>> is_human('Player Two', 'PVE')
    False
    """

    # Complete the body of this function.
    return not (game_type == HUMAN_COMPUTER and current_player == PLAYER_TWO)


def is_one_player_game(game_type: str) -> bool:
    """Return True if and only if the type of game being played 
    is a one-player game.
    
    game_type is HUMAN, HUMAN_HUMAN, or HUMAN_COMPUTER.

    >>> is_one_player_game("P1")
    True
    >>> is_one_player_game("PVP")
    False
    >>> is_one_player_game("PVE")
    False
    """

    return game_type == HUMAN


def current_player_score(p1_score: int,
                         p2_score: int,
                         current_player: str) -> int:
    """Return the score of the current player.

    >>> current_player_score(3, 5, "Player One")
    3
    >>> current_player_score(3, 5, "Player Two")
    5
    """

    if current_player == PLAYER_ONE:
        return p1_score
    return p2_score

    
def is_bonus_letter(view: str,
                    letter: str,
                    message: str) -> bool:
    """Return True if and if the second argument letter 
    is hidden and a consonants.
    
    >>> is_bonus_letter("a^^le", "p", "apple")
    True
    >>> is_bonus_letter("appl^", "e", "apple")
    False
    >>> is_bonus_letter("^ello", "", "Hello")
    True  
    """

    for i in range(len(view)):
        if (view[i] == HIDDEN
                and letter == message[i]
                and letter in ALL_CONSONANTS):
            return True
    return False
    
                      
def get_updated_char_view(view: str,
                          message: str,
                          updating_i: int,
                          letter: str) -> str:
    """Return The function returns a single character string that is
    the updated view of that one character: if the guess is correct, the
    updated view should be the revealed character; otherwise it should
    be the unchanged character from the view before the function was called.

    Precondition: 0 <= updating_i <= len(message)
    
    >>> get_updated_char_view("appl^", "apple", 5, "e")
    "apple"
    >>> get_updated_char_view("appl^", "apple", 2, "e")
    "appl^"
    >>> get_updated_char_view("appl^", "apple", 5, "y")
    "appl^"
    >>> get_updated_char_view("appl^", "apple", 3, "y")
    "appl^"
    """

    if view[updating_i] != HIDDEN:
        return view[updating_i]
    elif letter == message[updating_i]:
        return letter
    return HIDDEN


def calculate_score(score: int, occurrences: int, move: str) -> int:
    """Return the updated score depending on the player's current move.

    Precondition: move == CONSONANT or move == VOWEL

    >>> calculate_score(3, 3, "V")
    2
    >>> calculate_score(3, 1, "C")
    4
    >>> calculate_score(3, 0, "C")
    3
    """

    if move == VOWEL:
        return score - VOWEL_COST
    else:
        return score + occurrences
    

def next_player(current_player: str, occurences: int, game_type: str) -> str:
    """Return the player to play the next turn according to the game type.

    >>> next_player("Player One", 1, 'P1")
    "Player One"
    >>> next_player("Player One", 0, 'PVP")
    "Player Two"
    >>> next_player("Player One", 2, 'PVP")
    "Player One"
    >>> next_player("Player One", 0, 'PVE")
    "Player Two"
    """

    if game_type == HUMAN or occurences != 0:
        return current_player
    elif current_player == PLAYER_ONE:
        return PLAYER_TWO
    else:
        return PLAYER_ONE
    

def is_fully_hidden(view: str,index: int, message: str) -> bool:
    """Return True if and only if the character at the given index of 
    the message is not revealed anywhere in the current view.

    Precondition: 0 <= updating_i <= len(message)

    >>> is_fully_hidden("Hel^^", 3, "Hello")
    False
    >>> is_fully_hidden("Hel^^", 4, "Hello")
    True
    >>> is_fully_hidden("A^^le" 1, "Apple")
    True
    >>> is_fully_hidden("Ap^le" 2, "Apple")
    False
    """
    
    for char in view:
        if char == message[index]:
            return False
    return True

def computer_chooses_solve(view: str,
                           difficulty: str,
                           consonants_not_guessed: str) -> bool:
    """Return True if and if only if the computer choose to solve,
    while the strategy depends on the difficulty of the game.
    
    HARD: The computer solve if at least half of the letters have been revealed
    or if there are no more consonants to guess
    
    EASY: The computer only solve if therre is no more consonants to choose from
    
    >>> computer_chooses_solve("H^ppy", "E", "")
    True
    >>> computer_chooses_solve("H^ppy", "H", "")
    True
    >>> computer_chooses_solve("H^^^y", "E", "p")
    False
    >>> computer_chooses_solve("Ha^^y", "H", "p")
    True
    """
    if consonants_not_guessed == "":
        return True
    if difficulty == HARD:
        return half_revealed(view)
    return False

def remove_at_index(letters: str, index: int) -> str:
    """Return the string of letters that the charaters at 
    location [index] is removed.If the index numberis 
    outside the range, return the oringial letters.

    Precondition: index >= 0

    >>> remove_at_index("aeiou", 1)
    "aiou"
    >>> remove_at_index("bcdfghjklmnpqrstvwxyz", 1)
    "bdfghjklmnpqrstvwxyz"
    >>> remove_at_index("aeiou", 5)
    "aeiou"
    """

    if index > len(letters):
        return letters
    else:
        return letters[:index] + letters[index + 1:]
    
    
# Now define the other functions described in the handout.
# Follow the Function Design Recipe to produce complete functions for
# is_one_player_game, current_player_score, is_bonus_letter, 
# get_updated_char_view, calculate_score, next_player, is_fully_hidden,
# computer_chooses_solve, and remove_at_index.
