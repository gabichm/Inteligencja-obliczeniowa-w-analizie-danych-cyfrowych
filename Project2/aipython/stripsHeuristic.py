# Artificial Intelligence: Foundations of Computational Agents https://artint.info
# Copyright 2017-2024 David L. Poole and Alan K. Mackworth
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en
from datetime import time
import time


def dist(loc1, loc2):
    """returns the distance from location loc1 to loc2
    """
    if loc1==loc2:
        return 0
    if {loc1,loc2} in [{'cs','lab'},{'mr','off'}]:
        return 2
    else:
        return 1

def h_pending_tasks(state, goal):
    """ Heuristic that estimates the number of pending tasks (e.g., medication, chart check, etc.). """
    pending_tasks = 0

    # Count pending tasks (add your own logic here)
    if state.get('NeedsMedP1A', False):
        pending_tasks += 1
    if state.get('NeedsMedP2A', False):
        pending_tasks += 1
    if state.get('NeedsTestP1', False):
        pending_tasks += 1
    if state.get('NeedsTestP2', False):
        pending_tasks += 1
    # Add other conditions as needed

    return pending_tasks


def h_medication_collection(state, goal):
    """ Heuristic that estimates the work left to collect medication. """
    medications_left = 0
    # Check if the nurse needs to collect medication
    if state['EmptyHands'] == 0 and (state['HasMedA'] == 0 or state['HasMedB'] == 0 or state['HasMedC'] == 0):
        medications_left = 1
    elif state['EmptyHands'] == 1 and (state['HasMedA'] == 0 or state['HasMedB'] == 0 or state['HasMedC'] == 0):
        medications_left = 2  # The nurse needs to collect two medications
    elif state['EmptyHands'] == 2 and (state['HasMedA'] == 0 or state['HasMedB'] == 0 or state['HasMedC'] == 0):
        medications_left = 3  # The nurse still needs to collect all medications

    return medications_left
def h_hand_hygiene(state, goal):
    """ Heuristic that estimates the hand hygiene status. """
    # Check if hands are clean, for example
    if state.get('HandsClean', False):
        return 0  # Hands are already clean, no need for further action
    else:
        return 1  # Need to clean hands


def h_chart_check(state, goal):
    """ Heuristic that estimates the number of chart checks left to be done. """
    return 1 if not state['CheckedChartP1'] else 0 + 1 if not state['CheckedChartP2'] else 0
def h_test_completion(state, goal):
    """ Heuristic that estimates how many tests are left to be completed. """
    return (1 if state['NeedsTestP1'] else 0) + (1 if state['NeedsTestP2'] else 0)


def combined_heuristic(state, goal):
    """ Combined heuristic that considers multiple factors like nurse movement, task completion, and hygiene. """
    h_tasks = h_pending_tasks(state, goal)
    h_hygiene = h_hand_hygiene(state, goal)
    h_chart = h_chart_check(state, goal)
    h_test = h_test_completion(state, goal)

    # Combine the heuristics (e.g., by summing them or using the maximum)
    return h_tasks + h_hygiene + h_chart + h_test

def max_h(state, goal):
    """ Returns the maximum value from multiple heuristics. """
    return max(
        h_pending_tasks(state, goal),
        h_hand_hygiene(state, goal),
        h_chart_check(state, goal),
        h_test_completion(state, goal)
    )

def h_break_time(state, goal):
    """ Heuristic for whether the nurse needs to take a break. """
    return 1 if not state['TookBreak'] else 0


#
#
# def h1(state,goal):
#     """ the distance to the goal location, if there is one"""
#     if 'RLoc' in goal:
#         return dist(state['RLoc'], goal['RLoc'])
#     else:
#         return 0
#
# def h2(state,goal):
#     """ the distance to the coffee shop plus getting coffee and delivering it
#     if the robot needs to get coffee
#     """
#     if ('SWC' in goal and goal['SWC']==False
#             and state['SWC']==True
#             and state['RHC']==False):
#         return dist(state['RLoc'],'cs')+3
#     else:
#         return 0
#
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


def test_forward_heuristic(thisproblem=stripsProblem.subproblem_1):
    start_time = time.time()
    # print("\n***** FORWARD NO HEURISTIC")
    # print(SearcherMPP(Forward_STRIPS(thisproblem)).search())

    # print("\n***** FORWARD WITH HEURISTIC h_hand_hygiene")
    # print(SearcherMPP(Forward_STRIPS(thisproblem,h_hand_hygiene)).search())

    # print("\n***** FORWARD WITH HEURISTIC h_pending_tasks")
    # print(SearcherMPP(Forward_STRIPS(thisproblem,h_pending_tasks)).search())

    print("\n***** FORWARD WITH HEURISTICs h1 and h2")
    print(SearcherMPP(Forward_STRIPS(thisproblem,maxh(h_pending_tasks,h_hand_hygiene))).search())
    end_time = time.time()
    print(end_time - start_time)
if __name__ == "__main__":
    test_forward_heuristic()

#####  Regression Planner
from stripsRegressionPlanner import Regression_STRIPS

# def test_regression_heuristic(thisproblem=stripsProblem.simple_problem1):
#     print("\n***** REGRESSION NO HEURISTIC")
#     print(SearcherMPP(Regression_STRIPS(thisproblem)).search())


#
#     print("\n***** REGRESSION WITH HEURISTICs h1 and h2")
#     print(SearcherMPP(Regression_STRIPS(thisproblem,maxh(h_hand_hygiene, h_pending_tasks))).search())
#
# if __name__ == "__main__":
#     test_regression_heuristic()

# def normal_search(thisproblem=stripsProblem.simple_problem1):
#     print("\n***** NORMAL NO HEURISTIC")
#     # Tworzenie planera STRIPS
#     planner = Forward_STRIPS(thisproblem)
#     search = SearcherMPP(planner)
#     solution = search.search()
#     print(solution)

# if __name__ == "__main__":
#     start_time = time.time()
#     normal_search()
#     end_time = time.time()
#     print(end_time - start_time)


