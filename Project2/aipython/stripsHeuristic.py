# stripsHeuristic.py - Planner with Heuristic Function
# AIFCA Python code Version 0.9.15 Documentation at https://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents https://artint.info
# Copyright 2017-2024 David L. Poole and Alan K. Mackworth
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

def dist(loc1, loc2):
    """returns the distance from location loc1 to loc2
    """
    if loc1==loc2:
        return 0
    if {loc1,loc2} in [{'cs','lab'},{'mr','off'}]:
        return 2
    else:
        return 1

def h1(state,goal):
    """ the distance to the goal location, if there is one"""
    if 'RLoc' in goal:
        return dist(state['RLoc'], goal['RLoc'])
    else:
        return 0

def h2(state,goal):
    """ the distance to the coffee shop plus getting coffee and delivering it
    if the robot needs to get coffee
    """
    if ('SWC' in goal and goal['SWC']==False 
            and state['SWC']==True 
            and state['RHC']==False):
        return dist(state['RLoc'],'cs')+3
    else:
        return 0
        
def maxh(*heuristics):
    """Returns a new heuristic function that is the maximum of the functions in heuristics.
    heuristics is the list of arguments which must be heuristic functions.
    """
    # return lambda state,goal: max(h(state,goal) for h in heuristics)
    def newh(state,goal):
        return max(h(state,goal) for h in heuristics)
    return newh

#####  Forward Planner #####
from searchMPP import SearcherMPP
from stripsForwardPlanner import Forward_STRIPS
import stripsProblem

def test_forward_heuristic(thisproblem=stripsProblem.problem1):
    print("\n***** FORWARD NO HEURISTIC")
    print(SearcherMPP(Forward_STRIPS(thisproblem)).search())

    print("\n***** FORWARD WITH HEURISTIC h1")
    print(SearcherMPP(Forward_STRIPS(thisproblem,h1)).search()) 

    print("\n***** FORWARD WITH HEURISTIC h2")
    print(SearcherMPP(Forward_STRIPS(thisproblem,h2)).search())
    
    print("\n***** FORWARD WITH HEURISTICs h1 and h2")
    print(SearcherMPP(Forward_STRIPS(thisproblem,maxh(h1,h2))).search()) 

if __name__ == "__main__":
    test_forward_heuristic()

#####  Regression Planner
from stripsRegressionPlanner import Regression_STRIPS

def test_regression_heuristic(thisproblem=stripsProblem.problem1):
    print("\n***** REGRESSION NO HEURISTIC")
    print(SearcherMPP(Regression_STRIPS(thisproblem)).search())

    print("\n***** REGRESSION WITH HEURISTICs h1 and h2")
    print(SearcherMPP(Regression_STRIPS(thisproblem,maxh(h1,h2))).search())

if __name__ == "__main__":
    test_regression_heuristic()


def h_break(state, goal):
    """Heurystyka dla przerwy pielęgniarki.
    Zwraca 1, jeśli pielęgniarka nie miała przerwy, ale jest w 'station',
    inaczej zwraca 0.
    """
    if 'TookBreak' in goal and goal['TookBreak'] == False and state['TookBreak'] == False:
        return 1 if state['NLoc'] == 'station' else 2  # Wyższa wartość jeśli nie jest w 'station'
    return 0


def h_talk(state, goal):
    """Heurystyka dla rozmowy z pacjentem.
    Jeśli pacjent wymaga rozmowy przed leczeniem, zwracamy 1.
    """
    talk_p1_needed = 'TalkedToP1' in goal and goal['TalkedToP1'] == False and state['TalkedToP1'] == False
    talk_p2_needed = 'TalkedToP2' in goal and goal['TalkedToP2'] == False and state['TalkedToP2'] == False

    if talk_p1_needed or talk_p2_needed:
        return 1
    return 0


def h_extended(state, goal):
    """Rozszerzona heurystyka uwzględniająca rozmowę, przerwę i higienę."""
    return max(h1(state, goal), h2(state, goal), h_break(state, goal), h_talk(state, goal))


def h_full(state, goal):
    """Pełna heurystyka łącząca wszystkie wcześniejsze."""
    return max(h1(state, goal), h2(state, goal), h_break(state, goal), h_talk(state, goal), h_extended(state, goal))
