"""CSC108H1: Fall 2025 -- Assignment 2: Ontario Bridges

Instructions (READ THIS FIRST!)
===============================

Make sure that the files a2_checker.py and checker_generic.py are in the same
directory as this file.

The data used for this assignment is a subset of the data found in:
https://data.ontario.ca/dataset/bridge-conditions

Copyright and Usage Information
===============================

This code is provided solely for the personal and private use of students 
taking the CSC108 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of 
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2025 CSC108H1 Teaching Team
"""

import csv
import math

###############################################################################
# Constants to use you in your code
###############################################################################
COLUMN_ID = 0
COLUMN_NAME = 1
COLUMN_HIGHWAY = 2
COLUMN_LAT = 3
COLUMN_LON = 4
COLUMN_YEAR_BUILT = 5
COLUMN_LAST_MAJOR_REHAB = 6
COLUMN_LAST_MINOR_REHAB = 7
COLUMN_NUM_SPANS = 8
COLUMN_SPAN_DETAILS = 9
COLUMN_DECK_LENGTH = 10
COLUMN_LAST_INSPECTED = 11
COLUMN_BCI = 12

INDEX_BCI_YEARS = 0
INDEX_BCI_SCORES = 1
MISSING_BCI = -1.0

EARTH_RADIUS = 6371


###############################################################################
# Sample data for use in docstring examples
###############################################################################

# These bridges that are the bridges from rows 3, 4, and 33 of the dataset.

EXAMPLE_BRIDGES = \
    [[1, 'Highway 24 Underpass at Highway 403',
    '403', 43.167233, -80.275567, '1965', '2014', '2009', 4,
    [12.0, 19.0, 21.0, 12.0], 65.0, '04/13/2012',
    [['2013', '2012', '2011', '2010', '2009', '2008', '2007',
      '2006', '2005', '2004', '2003', '2002', '2001', '2000'],
     [MISSING_BCI, 72.3, MISSING_BCI, 69.5, MISSING_BCI, 70.0, MISSING_BCI,
      70.3, MISSING_BCI, 70.5, MISSING_BCI, 70.7, 72.9, MISSING_BCI]]],
    
    [2, 'WEST STREET UNDERPASS', 
     '403', 43.164531, -80.251582, '1963', '2014', '2007', 4,
     [12.2, 18.0, 18.0, 12.2], 61.0, '04/13/2012',
     [['2013', '2012', '2011', '2010', '2009', '2008', '2007',
       '2006', '2005', '2004', '2003', '2002', '2001', '2000'],
      [MISSING_BCI, 71.5, MISSING_BCI, 68.1, MISSING_BCI, 69.0, MISSING_BCI,
       69.4, MISSING_BCI, 69.4, MISSING_BCI, 70.3, 73.3, MISSING_BCI]]
     ],  
    
    [3, 'STOKES RIVER BRIDGE', '6', 
     45.036739, -81.33579, '1958', '2013', '', 1,
     [16.0], 18.4, '08/28/2013',
     [['2013', '2012', '2011', '2010', '2009', '2008', '2007',
       '2006', '2005', '2004', '2003', '2002', '2001', '2000'],
      [85.1, MISSING_BCI, 67.8, MISSING_BCI, 67.4, MISSING_BCI, 69.2,
       70.0, 70.5, MISSING_BCI, 75.1, MISSING_BCI, 90.1, MISSING_BCI]]
    ]
]  


###############################################################################
# Helper function to use in your code later on. You do not need to change it.
###############################################################################
def calculate_distance(lat1: float, lon1: float,
                       lat2: float, lon2: float) -> float:
    """Return the distance in kilometers between the two locations defined by
    (lat1, lon1) and (lat2, lon2), rounded to the nearest meter.

    >>> calculate_distance(43.659777, -79.397383, 43.657129, -79.399439)
    0.338
    >>> calculate_distance(43.42, -79.24, 53.32, -113.30)
    2713.226
    """

    # This function uses the haversine function to find the
    # distance between two locations. You do NOT need to understand why it
    # works. You will just need to call on the function and work with what it
    # returns.
    # Based on code at goo.gl/JrPG4j

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = (math.radians(lon1), math.radians(lat1),
                              math.radians(lon2), math.radians(lat2))

    # haversine formula t
    lon_diff = lon2 - lon1
    lat_diff = lat2 - lat1
    a = (math.sin(lat_diff / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(lon_diff / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    return round(c * EARTH_RADIUS, 3)

###############################################################################
# Part 1 - Querying the data
###############################################################################
def find_bridge_by_id(bridges: list[list], bridge_id: int) -> list:
    """Return the data for the bridge with id bridge_id from bridges.

    If there is no bridge with the bridge_id in bridges, then return an empty
    list.

    >>> example_bridges = EXAMPLE_BRIDGES
    >>> find_bridge_by_id(example_bridges, 4)
    []
    >>> find_bridge_by_id(example_bridges, 2) == EXAMPLE_BRIDGES[1]
    True
    """

    for bridge in bridges:
        if bridge[COLUMN_ID] == bridge_id:
            return bridge 
    return []

def find_bridges_in_radius(bridges: list[list], lat: float, lon: float,
                           radius: int, exclusions: list[int]) -> list[int]:
    """Return the IDs of the bridges in bridges that are within radius
    kilometres from location (lat, lon). Include bridge IDs that are exactly
    radius kilometres away. The bridge IDs in exclusions are not included in
    the result.

    Preconditions:
        - (lat, lon) is a valid location on Earth
        - radius > 0

    >>> example_bridges = EXAMPLE_BRIDGES
    >>> find_bridges_in_radius(example_bridges, 43.10, -80.15, 50, [])
    [1, 2]
    >>> find_bridges_in_radius(example_bridges, 43.10, -80.15, 50, [1, 2])
    []
    """
    result = []

    for bridge in bridges:
        if bridge[COLUMN_ID] not in exclusions:
            distance = calculate_distance(lat, 
                                          lon,
                                          bridge[COLUMN_LAT],
                                          bridge[COLUMN_LON])
            if distance <= radius:
                result.append(bridge[COLUMN_ID])

    return result

def get_bridge_condition(bridges: list[list], bridge_id: int) -> float:
    """Return the most recent BCI score of the bridge in bridges with id
    bridge_id. If there is no bridge with id bridge_id in bridges, return
    MISSING_BCI.

    The most recent BCI score is the (non-missing) BCI score given to the
    bridge in the most recent year. 

    >>> example_bridges = EXAMPLE_BRIDGES
    >>> get_bridge_condition(example_bridges, 1)
    72.3
    """
    bridge = find_bridge_by_id(bridges, bridge_id)
    if bridge != []:
        for score in bridge[COLUMN_BCI][INDEX_BCI_SCORES]:
            if score != MISSING_BCI:
                return score
    return MISSING_BCI

def calculate_average_condition(bridge: list, start: int, stop: int) -> float:
    """Return the average BCI score of bridge between the year start 
    (inclusive) and stop (exclusive).

    Missing BCI scores are not included in the average. 
    If there are no valid scores between start and stop, return 0.0.

    >>> bridge = EXAMPLE_BRIDGES[0]
    >>> calculate_average_condition(bridge, 2005, 2013)
    70.525
    >>> calculate_average_condition(bridge, 2013, 2024)
    0.0
    >>> calculate_average_condition(bridge, 2005, 2005)
    0.0
    """
    years = bridge[COLUMN_BCI][INDEX_BCI_YEARS]
    scores = bridge[COLUMN_BCI][INDEX_BCI_SCORES]
    total = 0.0
    count = 0
    
    for i in range(len(years)):
        year = int(years[i])
        score = scores[i]
        if start <= year < stop and score != MISSING_BCI:
            total += score
            count += 1
        else:
            total += 0.0
    
    if total == 0.0:
        return total
    return total / count
            

###############################################################################
# Part 2 - Mutating the data
###############################################################################
def inspect_bridge(bridges: list[list], bridge_id: int, inspect_date: str,
                   inspect_bci: float) -> None:
    """Update the bridge in bridges with id bridge_id so that it is last
    inspected at inspect_date and its most recent BCI score is inspect_bci 
    in the year given by inspect_date. 
    
    This function adds only one new BCI score and year to a bridge. It does not
    add any missing years between the new inspection and the previous most
    recent BCI score. 

    Precondition:
        - bridges contains a bridge with id bridge_id
        - date is in the format 'MM/DD/YYYY' and is the most recent inspection
        - 0.0 <= bci <= 100.0
        - there is no BCI score for the given year

    >>> my_bridge = EXAMPLE_BRIDGES[0]
    >>> inspect_bridge([my_bridge], 1, '02/14/2021', 71.9)
    >>> my_bridge[COLUMN_LAST_INSPECTED]
    '02/14/2021'
    >>> my_bridge[COLUMN_BCI][INDEX_BCI_YEARS][0]
    '2021'
    >>> my_bridge[COLUMN_BCI][INDEX_BCI_SCORES][0]
    71.9
    """

    bridge = find_bridge_by_id(bridges, bridge_id)
    years = bridge[COLUMN_BCI][INDEX_BCI_YEARS]
    score = bridge[COLUMN_BCI][INDEX_BCI_SCORES]
    inspect_year = inspect_date[6:]

    bridge[COLUMN_LAST_INSPECTED] = inspect_date
    years.insert(0, inspect_year)
    score.insert(0, inspect_bci)

def rehabilitate_bridge(bridges: list[list], bridge_ids: list[int],
                        new_year: str, is_major: bool) -> None:
    """Update the bridges with ids from bridge_ids in bridges to have their
    last rehab set to new_year. If is_major is True, update the major rehab
    date. Otherwise, update the minor rehab date.

    Precondition:
        - bridges contains the bridges with the ids in bridge_ids

    >>> my_bridge = EXAMPLE_BRIDGES[0]
    >>> rehabilitate_bridge([my_bridge], [1], '2021', False)
    >>> my_bridge[COLUMN_LAST_MINOR_REHAB]
    '2021'
    """
    for bridge_id in bridge_ids:
        bridge = find_bridge_by_id(bridges, bridge_id)
        if is_major:
            bridge[COLUMN_LAST_MAJOR_REHAB] = new_year
        else:
            bridge[COLUMN_LAST_MINOR_REHAB] = new_year

###############################################################################
# Part 3 - Implementing useful algorithms
###############################################################################
def find_worst_bci(bridges: list[list], bridge_ids: list[int]) -> int:
    """Return the bridge ID from bridge_ids of the bridge from bridges who
    has the lowest most recent BCI score.

    If there is a tie, return the bridge with the smaller bridge ID in bridges.

    Precondition:
        - bridges contains the bridges with the ids in bridge_ids
        - bridge_ids contains at least one bridge
        - every bridge in bridges has at least one BCI score
        - the IDs in bridge_ids appear in increasing order

    >>> example_bridges = EXAMPLE_BRIDGES
    >>> find_worst_bci(example_bridges, [1, 2])
    2
    >>> find_worst_bci(example_bridges, [1, 3])
    1
    """
    scores = []
    
    for bridge_id in bridge_ids:
        score = get_bridge_condition(bridges, bridge_id)
        scores.append(score)
        
    worst_score = scores.index(min(scores))
    return bridge_ids[worst_score]

def map_route(bridges: list[list], lat: float, lon: float,
              max_bridges: int, radius: int) -> list[int]:
    """Return the sequence of bridge IDs from bridges that must be visited
    by an inspector who initially starts at location (lat, lon). The sequence
    must contain at most max_bridges IDs. Every ID in the sequence must be
    unique; an inspector cannot inspect the same bridge twice.

    The inspector visits the bridge within radius of their location that has
    the lowest most recent BCI score. The next bridge inspected is the bridge
    with the lowest most recent BCI score within radius radius of the last
    bridge's location. This step repeats until max_bridges bridges have been
    inspected, or there are no bridges to inspect within radius.

    >>> example_bridges = EXAMPLE_BRIDGES
    >>> map_route(example_bridges, 43.10, -80.15, 3, 50)
    [2, 1]
    >>> map_route(example_bridges, 43.1, -80.5, 30, 10)
    []
    """
    sequence = []
    current_lat = lat
    current_lon = lon

    while len(sequence) < max_bridges:
        bridge_within_radius_ids = find_bridges_in_radius(bridges, 
                                                          current_lat, 
                                                          current_lon,
                                                          radius, 
                                                          sequence)

        if bridge_within_radius_ids == []:
            return sequence
            
        bridge_to_inspect_id = find_worst_bci(bridges, bridge_within_radius_ids)
        bridge_to_inspect = find_bridge_by_id(bridges, bridge_to_inspect_id)

        sequence.append(bridge_to_inspect_id)
        current_lat = bridge_to_inspect[COLUMN_LAT]
        current_lon = bridge_to_inspect[COLUMN_LON]

    return sequence

###############################################################################
# Part 4 - Reading and cleaning raw data
###############################################################################
def clean_length_data(raw_length: str) -> float:
    """Return the length of the bridge based on the value in raw_length.

    If raw_length is an empty string, return 0.0.

    Precondition:
        - if raw_length is not the empty string, it can be converted to a float

    >>> clean_length_data('12')
    12.0
    """
    if raw_length == "":
        return 0.0
    return float(raw_length)
    

def trim_from_end(raw_data: list, count: int) -> None:
    """Update raw_data so that count elements have been removed from the end.

    Preconditions:
        - count >= 0
        - len(raw_data) >= count

    >>> my_lst = [[72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9], '', '72.3', '', \
    '69.5', '', '70', '', '70.3', '', '70.5', '', '70.7', '72.9', '']
    >>> trim_from_end(my_lst, 14)
    >>> my_lst
    [[72.3, 69.5, 70.0, 70.3, 70.5, 70.7, 72.9]]
    """
    for _ in range(count):
        raw_data.pop()


def clean_span_data(raw_spans: str) -> list[float]:
    """Return a list of span lengths from raw_spans, in the same order that
    they appear in raw_spans.

    Precondition:
        - raw_spans is in the format described in the section "Bridge Spans" 

    >>> clean_span_data('Total=64  (1)=12;(2)=19;(3)=21;(4)=12;')
    [12.0, 19.0, 21.0, 12.0]
    """
    sums = 0.0
    result = []
    total = float(raw_spans[6:8])
    span = raw_spans[10:]

    while sums < total:
        span_num = float(span[4:6])
        sums += span_num
        result.append(span_num)

        span = span[7:]
    
    return result

def clean_bci_data(bci_years: list[str], start_year: int, 
                   bci_scores: list) -> None:
    """Update bci_years so that each element contains the year as a string,
    starting from start_year and decreasing by one for each subsequent element,
    until bci_years has the same length as bci_scores. Also update bci_scores
    so that all non-empty string values are float values, and all empty string
    values are MISSING_BCI.

    Preconditions:
        - len(bci_years) == 0
        - len(bci_scores) > 0
        - start_year - len(bci_scores) >= 0
        - every value in bci_scores is either an empty string or can be
        converted to a float

    >>> years = []
    >>> scores = ['', '72.3', '', '69.5', '', '70.0', '', '70.3', '']
    >>> clean_bci_data(years, 2013, scores)
    >>> years
    ['2013', '2012', '2011', '2010', '2009', '2008', '2007', '2006', '2005']
    >>> scores
    [-1.0, 72.3, -1.0, 69.5, -1.0, 70.0, -1.0, 70.3, -1.0]
    """
    i = 0
    while len(bci_years) < len(bci_scores):
        if bci_scores[i] == "":
            swap = MISSING_BCI
        else:
            swap = float(bci_scores[i])

        bci_scores[i] = swap
        bci_years.append(str(start_year - i))

        i += 1

###############################################################################
# Provided function. Do not modify. 
###############################################################################
def clean_data(data: list[list], start_year: int) -> None:
    """Update data so that the applicable string values are converted to their
    appropriate type. In addition, update COLUMN_ID for each inner list so that
    the first inner list has an ID of 1 and each subsequent inner list has an
    ID of 1 more than the last inner list.

    The indexes of the string values that are converted, and their
    corresponding type, are:
        - COLUMN_LAT is a float
        - COLUMN_LON is a float
        - COLUMN_LENGTH is a float
        - COLUMN_NUM_SPANS is an int
        - COLUMN_SPAN_LENGTH is a list of floats
        - COLUMN_BCIS is a list of floats

    >>> uncleaned_bridge = ['1 -  32/', 'Highway 24 Underpass at Highway 403', \
    '403', '43.167233', '-80.275567', '1965', '2014', '2009', '4', \
    'Total=64  (1)=12;(2)=19;(3)=21;(4)=12;', '65', '04/13/2012', \
    '72.3', '', '72.3', '', '69.5', '', '70', '', '70.3', '', '70.5', '', \
    '70.7', '72.9', '']
    >>> clean_data([uncleaned_bridge], 2013)
    >>> uncleaned_bridge == EXAMPLE_BRIDGES[0]
    True
    """

    next_id = 1

    for row in data:
        row[COLUMN_ID] = next_id
        next_id = next_id + 1

        row[COLUMN_LAT] = float(row[COLUMN_LAT])
        row[COLUMN_LON] = float(row[COLUMN_LON])
        row[COLUMN_NUM_SPANS] = int(row[COLUMN_NUM_SPANS])
        row[COLUMN_DECK_LENGTH] = clean_length_data(row[COLUMN_DECK_LENGTH])
        row[COLUMN_SPAN_DETAILS] = clean_span_data(row[COLUMN_SPAN_DETAILS])

        bci_years = []
        bci_scores = row[COLUMN_BCI + 1:]
        clean_bci_data(bci_years, start_year, bci_scores)
        row[COLUMN_BCI] = [bci_years, bci_scores]

        trim_from_end(row, len(row) - COLUMN_BCI - 1)


###############################################################################
# Provided function. Do not modify. 
###############################################################################
def read_data(filename: str) -> list[list]:
    """Return the data found in the file filename as a list of lists.

    Each inner list corresponds to a row in the file that has been cleaned with
    clean_data.

    Docstring examples not given since the results depend on filename.

    Preconditions:
        - The data in filename is in a valid format
    """
    with open(filename) as csv_file:
        lines = list(csv.reader(csv_file))

        start_year = int(lines[1][COLUMN_BCI + 1])

        data = lines[2:]
        clean_data(data, start_year)

    return data
