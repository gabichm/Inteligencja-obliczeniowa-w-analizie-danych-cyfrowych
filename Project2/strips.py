import sys
import matplotlib.pyplot as plt
import time
sys.path.append("aipython")
from aipython.searchMPP import SearcherMPP
from aipython.stripsProblem import STRIPS_domain, Planning_problem, Strips
from aipython.stripsForwardPlanner import Forward_STRIPS
from aipython.stripsHeuristic import SimpleHeuristic, Forward_STRIPS_Heuristic


# Zaczynamy pomiar czasu
start_time = time.time()

hospital_care_domain = STRIPS_domain(
    {
        'NLoc': {'station', 'room', 'pharmacy', 'sink'},  # Lokalizacja pielęgniarki
        'EmptyHands': {0, 1, 2},
        'HasMedA': {0, 1, 2},
        'HasMedB': {0, 1, 2},
        'HasMedC': {0, 1, 2},
        'NeedsMedP1A': {True, False},
        'NeedsMedP2A': {True, False},
        'NeedsMedP1B': {True, False},
        'NeedsMedP2B': {True, False},
        'NeedsMedP1C': {True, False},
        'NeedsMedP2C': {True, False},
        'NeedsTestP1': {False, True},  # Czy pacjent potrzebuje testu
        'NeedsTestP2': {False, True},
        'HandsClean': {False, True},  # Czy pielęgniarka ma czyste ręce
        'CheckedChartP1': {False, True},  # Czy pielęgniarka sprawdziła kartę pacjenta
        'CheckedChartP2': {False, True},
        'UpToDateChartP1': {False, True},  # Karta pacjenta aktualna?
        'UpToDateChartP2': {False, True},
        'TookBreak': {False, True},
        'TalkToP1': {False, True},
        'TalkToP2': {False, True}
    },
    {
        # Przemieszczanie pielęgniarki
        Strips('MOVE_NURSE_s_r',
               {'NLoc': 'station'},
               {'NLoc': 'room'}),
        Strips('MOVE_NURSE_s_ph',
              {'NLoc': 'station'},
              {'NLoc': 'pharmacy'}),
        Strips('MOVE_NURSE_s_sink',
               {'NLoc': 'station'},
               {'NLoc': 'sink'}),
        Strips('MOVE_NURSE_r_s',
               {'NLoc': 'room'},
               {'NLoc': 'station'}),
        Strips('MOVE_NURSE_r_ph',
               {'NLoc': 'room'},
               {'NLoc': 'pharmacy'}),
        Strips('MOVE_NURSE_r_sink',
               {'NLoc': 'room'},
               {'NLoc': 'sink'}),
        Strips('MOVE_NURSE_ph_r',
               {'NLoc': 'pharmacy'},
               {'NLoc': 'room'}),
        Strips('MOVE_NURSE_ph_s',
               {'NLoc': 'pharmacy'},
               {'NLoc': 'station'}),
        Strips('MOVE_NURSE_ph_sink',
               {'NLoc': 'pharmacy'},
               {'NLoc': 'sink'}),
        Strips('MOVE_NURSE_sink_r',
               {'NLoc': 'sink'},
               {'NLoc': 'room'}),
        Strips('MOVE_NURSE_sink_ph',
               {'NLoc': 'sink'},
               {'NLoc': 'pharmacy'}),
        Strips('MOVE_NURSE_sink_station',
               {'NLoc': 'sink'},
               {'NLoc': 'station'}),
        
        # Pobranie leku
        Strips('COLLECT_MEDICATION_A',
               {'NLoc': 'pharmacy', 'EmptyHands': 0, 'HasMedA': 0, 'HasMedB': 0, 'HasMedC': 0},
               {'EmptyHands': 1, 'HasMedA': 1}),
        Strips('COLLECT_MEDICATION_B',
               {'NLoc': 'pharmacy', 'EmptyHands': 0, 'HasMedA': 0, 'HasMedB': 0, 'HasMedC': 0},
               {'EmptyHands': 1, 'HasMedB': 1}),
        Strips('COLLECT_MEDICATION_C',
               {'NLoc': 'pharmacy', 'EmptyHands': 0, 'HasMedA': 0, 'HasMedB': 0, 'HasMedC': 0},
               {'EmptyHands': 1, 'HasMedA': 1}),
        Strips('COLLECT_MEDICATION_AA',
               {'NLoc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 1, 'HasMedB': 0, 'HasMedC': 0},
               {'EmptyHands': 2, 'HasMedA': 2}),
        Strips('COLLECT_MEDICATION_AB',
               {'NLoc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 1, 'HasMedB': 0, 'HasMedC': 0},
               {'EmptyHands': 2, 'HasMedB': 1}),
        Strips('COLLECT_MEDICATION_AC',
               {'NLoc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 1, 'HasMedB': 0, 'HasMedC': 0},
               {'EmptyHands': 2, 'HasMedC': 1}),
        Strips('COLLECT_MEDICATION_BA',
               {'NLoc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 0, 'HasMedB': 1, 'HasMedC': 0},
               {'EmptyHands': 2, 'HasMedA': 1}),
        Strips('COLLECT_MEDICATION_BB',
               {'NLoc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 0, 'HasMedB': 1, 'HasMedC': 0},
               {'EmptyHands': 2, 'HasMedB': 2}),
        Strips('COLLECT_MEDICATION_BC',
               {'NLoc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 0, 'HasMedB': 1, 'HasMedC': 0},
               {'EmptyHands': 2, 'HasMedC': 1}),
        Strips('COLLECT_MEDICATION_CA',
               {'NLoc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 0, 'HasMedB': 0, 'HasMedC': 1},
               {'EmptyHands': 2, 'HasMedA': 1}),
        Strips('COLLECT_MEDICATION_CB',
               {'NLoc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 0, 'HasMedB': 0, 'HasMedC': 1},
               {'EmptyHands': 2, 'HasMedB': 1}),
        Strips('COLLECT_MEDICATION_CC',
               {'NLoc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 0, 'HasMedB': 0, 'HasMedC': 1},
               {'EmptyHands': 2, 'HasMedC': 2}),
        
        # Mycie rąk
        Strips('WASH_HANDS',
               {'NLoc': 'sink'},
               {'HandsClean': True}),

        # Sprawdzenie karty pacjenta
        Strips('CHECK_CHART_p1',
               {'NLoc': 'room', 'CheckedChartP1': False},
               {'CheckedChartP1': True, 'HandsClean': False}),
        Strips('CHECK_CHART_p2',
               {'NLoc': 'room', 'CheckedChartP2': False},
               {'CheckedChartP2': True, 'HandsClean': False}),

        # Podanie leku
        Strips('ADMINISTER_MEDICATION_p1A1',
               {'NLoc': 'room', 'HasMedA': 1, 'NeedsMedP1A': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1A': False, 'HasMedA': 0, 'HandsClean': False}),
        Strips('ADMINISTER_MEDICATION_p2A1',
               {'NLoc': 'room', 'HasMedA': 1, 'NeedsMedP2A': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2A': False, 'HasMedA': 0, 'HandsClean': False}),
        Strips('ADMINISTER_MEDICATION_p1A2',
               {'NLoc': 'room', 'HasMedA': 2, 'NeedsMedP1A': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1A': False, 'HasMedA': 1, 'HandsClean': False}),
        Strips('ADMINISTER_MEDICATION_p2A2',
               {'NLoc': 'room', 'HasMedA': 2, 'NeedsMedP2A': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2A': False, 'HasMedA': 1, 'HandsClean': False}),
        Strips('ADMINISTER_MEDICATION_p1B1',
               {'NLoc': 'room', 'HasMedB': 1, 'NeedsMedP1B': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1B': False, 'HasMedB': 0, 'HandsClean': False}),
        Strips('ADMINISTER_MEDICATION_p2B1',
               {'NLoc': 'room', 'HasMedB': 1, 'NeedsMedP2B': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2B': False, 'HasMedB': 0, 'HandsClean': False}),
        Strips('ADMINISTER_MEDICATION_p1B2',
               {'NLoc': 'room', 'HasMedB': 2, 'NeedsMedP1B': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1B': False, 'HasMedB': 1, 'HandsClean': False}),
        Strips('ADMINISTER_MEDICATION_p2B2',
               {'NLoc': 'room', 'HasMedB': 2, 'NeedsMedP2B': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2B': False, 'HasMedB': 1, 'HandsClean': False}),
        Strips('ADMINISTER_MEDICATION_p1C1',
               {'NLoc': 'room', 'HasMedC': 1, 'NeedsMedP1C': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1C': False, 'HasMedC': 0, 'HandsClean': False}),
        Strips('ADMINISTER_MEDICATION_p2C1',
               {'NLoc': 'room', 'HasMedC': 1, 'NeedsMedP2C': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2C': False, 'HasMedC': 0, 'HandsClean': False}),
        Strips('ADMINISTER_MEDICATION_p1C2',
               {'NLoc': 'room', 'HasMedC': 2, 'NeedsMedP1C': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1C': False, 'HasMedC': 1, 'HandsClean': False}),
        Strips('ADMINISTER_MEDICATION_p2C2',
               {'NLoc': 'room', 'HasMedC': 2, 'NeedsMedP2C': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2C': False, 'HasMedC': 1, 'HandsClean': False}),

        # Przeprowadzenie testu
        Strips('CONDUCT_TEST_p1',
               {'NLoc': 'room', 'NeedsTestP1': True, 'HandsClean': True},
               {'NeedsTestP1': False, 'HandsClean': False}),
        Strips('CONDUCT_TEST_p2',
               {'NLoc': 'room', 'NeedsTestP2': True, 'HandsClean': True},
               {'NeedsTestP2': False, 'HandsClean': False }),

        # Dodanie informacji do karty pacjenta
        Strips('UPDATE_CHART_p1',
               {'NLoc': 'room', 'UpToDateChartP1': False},
               {'UpToDateChartP1': True}),
        Strips('UPDATE_CHART_p2',
               {'NLoc': 'room', 'UpToDateChartP2': False},
               {'UpToDateChartP2': True}),

        # Przerwa na kawę
        Strips('TAKE_BREAK',
               {'NLoc': 'station', 'TookBreak': False},
               {'TookBreak': True}),
        # Rozmowa z pacjentem
        Strips('TALK_TO_PATIENT_P1',
               {'NLoc': 'room', 'TalkToP1': False},
               {'TalkToP1': True}),
        Strips('TALK_TO_PATIENT_P2',
               {'NLoc': 'room', 'TalkToP2': False},
               {'TalkToP2': True})
    }
)
# Prosty problem 1
simple_problem1 = Planning_problem(
    hospital_care_domain,
    {
        'NLoc': 'station',  # Pielęgniarka znajduje się na stacji
        'EmptyHands': 0,  # Ręce pielęgniarki są puste
        'HasMedA': 0,  # Pielęgniarka nie ma leku A
        'HasMedB': 0,  # Pielęgniarka nie ma leku B
        'HasMedC': 0,  # Pielęgniarka nie ma leku C
        'NeedsMedP1A': True,  # Pacjent 1 potrzebuje leku A
        'NeedsMedP1B': False,  # Pacjent 1 nie potrzebuje leku B
        'NeedsMedP1C': False,  # Pacjent 1 nie potrzebuje leku C
        'NeedsMedP2A': False,
        'NeedsMedP2B': False,
        'NeedsMedP2C': False,
        'NeedsTestP1': False,  # Pacjent 1 nie potrzebuje testu
        'NeedsTestP2': True,  # Pacjent 2 nie potrzebuje testu
        'HandsClean': False,  # Ręce pielęgniarki są brudne
        'CheckedChartP1': False,  # Karta pacjenta 1 nie została sprawdzona
        'CheckedChartP2': False,  # Karta pacjenta 2 nie została sprawdzona
        'UpToDateChartP1': False,  # Karta pacjenta 1 nie jest aktualna
        'UpToDateChartP2': False,  # Karta pacjenta 2 nie jest aktualna
        'TookBreak': False,  # Pielęgniarka nie zrobiła przerwy
        'TalkToP1': False,  # Pielęgniarka nie rozmawiała z pacjentem 1
        'TalkToP2': False, },
    {'NeedsTestP2': False}  # Cel: Test dla pacjenta 2 wykonany
)
#  Prosty Problem 2
simple_problem2 = Planning_problem(
    hospital_care_domain,
    {
        'NLoc': 'station',  # Pielęgniarka znajduje się na stacji
        'EmptyHands': 0,  # Ręce pielęgniarki są puste
        'HasMedA': 0,  # Pielęgniarka nie ma leku A
        'HasMedB': 0,  # Pielęgniarka nie ma leku B
        'HasMedC': 0,  # Pielęgniarka nie ma leku C
        'NeedsMedP1A': True,  # Pacjent 1 potrzebuje leku A
        'NeedsMedP1B': False,  # Pacjent 1 nie potrzebuje leku B
        'NeedsMedP1C': False,  # Pacjent 1 nie potrzebuje leku C
        'NeedsMedP2A': False,
        'NeedsMedP2B': False,
        'NeedsMedP2C': False,
        'NeedsTestP1': False,  # Pacjent 1 nie potrzebuje testu
        'NeedsTestP2': False,  # Pacjent 2 nie potrzebuje testu
        'HandsClean': False,  # Ręce pielęgniarki są brudne
        'CheckedChartP1': False,  # Karta pacjenta 1 nie została sprawdzona
        'CheckedChartP2': False,  # Karta pacjenta 2 nie została sprawdzona
        'UpToDateChartP1': False,  # Karta pacjenta 1 nie jest aktualna
        'UpToDateChartP2': False,  # Karta pacjenta 2 nie jest aktualna
        'TookBreak': False,  # Pielęgniarka nie zrobiła przerwy
        'TalkToP1': False,  # Pielęgniarka nie rozmawiała z pacjentem 1
        'TalkToP2': False,  # Pielęgniarka nie rozmawiała z pacjentem 2
    },
    {'NeedsMedP1A': False}  # Cel: Pacjent 1 otrzymał lek A
)


# Prosty Problem 3
simple_problem3 = Planning_problem(
    hospital_care_domain,
    {
        'NLoc': 'station',  # Pielęgniarka znajduje się na stacji
        'EmptyHands': 0,  # Ręce pielęgniarki są puste
        'HasMedA': 0,  # Pielęgniarka nie ma leku A
        'HasMedB': 0,  # Pielęgniarka nie ma leku B
        'HasMedC': 0,  # Pielęgniarka nie ma leku C
        'NeedsMedP1A': True,  # Pacjent 1 potrzebuje leku A
        'NeedsMedP1B': True,  # Pacjent 1 nie potrzebuje leku B
        'NeedsMedP1C': False,  # Pacjent 1 nie potrzebuje leku C
        'NeedsMedP2A': False,
        'NeedsMedP2B': False,
        'NeedsMedP2C': False,
        'NeedsTestP1': False,  # Pacjent 1 nie potrzebuje testu
        'NeedsTestP2': False,  # Pacjent 2 nie potrzebuje testu
        'HandsClean': False,  # Ręce pielęgniarki są brudne
        'CheckedChartP1': False,  # Karta pacjenta 1 nie została sprawdzona
        'CheckedChartP2': False,  # Karta pacjenta 2 nie została sprawdzona
        'UpToDateChartP1': False,  # Karta pacjenta 1 nie jest aktualna
        'UpToDateChartP2': False,  # Karta pacjenta 2 nie jest aktualna
        'TookBreak': False,  # Pielęgniarka nie zrobiła przerwy
        'TalkToP1': False,  # Pielęgniarka nie rozmawiała z pacjentem 1
        'TalkToP2': False, },
    {'NeedsMedP1A': False, 'NeedsMedP1B': False}  # Cel: Pacjent 1 otrzymał oba leki
)



# # Tworzenie planera STRIPS
# planner = Forward_STRIPS(simple_problem3)
#
# # Tworzenie wyszukiwarki
# search = SearcherMPP(planner)
#
# # Wyszukiwanie rozwiązania
# solution = search.search()

# Create the planner using your heuristic
heuristic = HospitalCareHeuristic(simple_problem3)

# Create a planner with the heuristic
planner_with_heuristic = Forward_STRIPS_Heuristic(simple_problem3, heuristic)

# Create the searcher
search_with_heuristic = SearcherMPP(planner_with_heuristic)

# Search for the solution
solution_with_heuristic = search_with_heuristic.search()



# Wyświetlenie znalezionego planu
end_time = time.time()
print(solution_with_heuristic)


# Wyświetlenie znalezionego planu
# print(solution)
print(end_time-start_time)

