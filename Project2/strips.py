import sys
import matplotlib.pyplot as plt
sys.path.append("aipython")
from aipython.searchMPP import SearcherMPP
from aipython.stripsProblem import STRIPS_domain, Planning_problem, Strips
from aipython.stripsForwardPlanner import Forward_STRIPS

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
        'UpToDateChartP2': {False, True}
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
               {'NLoc': 'pharmacy', 'EmptyHands': 0, 'HasMedA': 0, 'HasMedB': 0, 'HasMed': 0},
               {'EmptyHands': 1, 'HasMedA': 1}),
        Strips('COLLECT_MEDICATION_B',
               {'NLoc': 'pharmacy', 'EmptyHands': 0, 'HasMedA': 0, 'HasMedB': 0, 'HasMed': 0},
               {'EmptyHands': 1, 'HasMedB': 1}),
        Strips('COLLECT_MEDICATION_C',
               {'NLoc': 'pharmacy', 'EmptyHands': 0, 'HasMedA': 0, 'HasMedB': 0, 'HasMed' : 0},
               {'EmptyHands': 1, 'HasMedA': 1}),
        Strips('COLLECT_MEDICATION_AA',
               {'Nloc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 1, 'HasMedB': 0, 'HasMedC': 0},
               {'EmptyHands': 2, 'HasMedA': 2}),
        Strips('COLLECT_MEDICATION_AB',
               {'Nloc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 1, 'HasMedB' : 0, 'HasMedC' : 0},
               {'EmptyHands': 2, 'HasMedB': 1}),
        Strips('COLLECT_MEDICATION_AC',
               {'Nloc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 1, 'HasMedB': 0, 'HasMedC': 0},
               {'EmptyHands': 2, 'HasMedC': 1}),
        Strips('COLLECT_MEDICATION_BA',
               {'Nloc': 'pharmacy', 'EmptyHands': 1, 'HasMedA':0, 'HasMedB': 1, 'HasMedC': 0},
               {'EmptyHands': 2, 'HasMedA': 1}),
        Strips('COLLECT_MEDICATION_BB',
               {'Nloc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 0, 'HasMed': 1, 'HasMedC': 0},
               {'EmptyHands': 2, 'HasMedB': 2}),
        Strips('COLLECT_MEDICATION_BC',
               {'Nloc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 0, 'HasMed': 1, 'HasMedC': 0},
               {'EmptyHands': 2, 'HasMedC': 1}),
        Strips('COLLECT_MEDICATION_CA',
               {'Nloc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 0, 'HasMedB': 0, 'HasMedC': 1},
               {'EmptyHands': 2, 'HasMedA': 1}),
        Strips('COLLECT_MEDICATION_CB',
               {'Nloc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 0, 'HasMed': 0, 'HasMedC': 1},
               {'EmptyHands': 2, 'HasMedB': 1}),
        Strips('COLLECT_MEDICATION_CC',
               {'Nloc': 'pharmacy', 'EmptyHands': 1, 'HasMedA': 0, 'HasMed': 0, 'HasMedC': 1},
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
        Strips('ADMINISTER_MEDICATION_p1',
               {'NLoc': 'room', 'HasMed': True, 'NeedsMedP1': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1': False, 'HasMed': False, 'HandsClean': False}),
        Strips('ADMINISTER_MEDICATION_p2',
               {'NLoc': 'room', 'HasMed': True, 'NeedsMedP2': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2': False, 'HasMed': False, 'HandsClean': False}),

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
               {'UpToDateChartP2': True})
    }
)

problem1 = Planning_problem(
    hospital_care_domain,
    {  # Stan początkowy
        'NLoc': 'station',    # Pielęgniarka startuje w stacji
        'HasMed': False,      # Nie ma leku
        'NeedsMedP1': True,   # Pacjent 1 potrzebuje leku
        'NeedsMedP2': False,  # Pacjent 2 nie potrzebuje leku
        'NeedsTestP1': False, # Pacjent 1 nie potrzebuje testu
        'NeedsTestP2': True,  # Pacjent 2 potrzebuje testu
        'HandsClean': False,  # Ręce pielęgniarki są brudne
        'CheckedChartP1': False, # Karta pacjenta 1 nie została sprawdzona
        'CheckedChartP2': False  # Karta pacjenta 2 nie została sprawdzona
    },
    {  # Cel - co chcemy osiągnąć?
        'NeedsMedP1': False,  # Pacjent 1 ma dostać lek
        'NeedsTestP2': False  # Pacjent 2 ma mieć wykonany test
    }
)

problem2 = Planning_problem(
    hospital_care_domain,
    {  # Stan początkowy
        'NLoc': 'station',    # Pielęgniarka startuje w stacji
        'HasMed': False,      # Nie ma leku
        'NeedsMedP2': True,   # Pacjent 2 potrzebuje leku
        'NeedsTestP2': True,  # Pacjent 2 potrzebuje testu
        'NeedsMedP1': False,  # Pacjent 1 nie potrzebuje leku
        'NeedsTestP1': False, # Pacjent 1 nie potrzebuje testu
        'HandsClean': False,  # Ręce pielęgniarki są brudne
        'CheckedChartP1': False, # Karta pacjenta 1 nie została sprawdzona
        'CheckedChartP2': False  # Karta pacjenta 2 nie została sprawdzona
    },
    {  # Cel - co chcemy osiągnąć?
        'NeedsMedP2': False,  # Pacjent 2 ma dostać lek
        'NeedsTestP2': False, # Pacjent 2 ma mieć wykonany test
        'CheckedChartP2': True  # Karta pacjenta 2 ma być sprawdzona
    }
)

problem3 = Planning_problem(
    hospital_care_domain,
    {  # Stan początkowy
        'NLoc': 'station',    # Pielęgniarka startuje w stacji
        'HasMed': False,      # Nie ma leku
        'NeedsMedP1': True,   # Pacjent 1 potrzebuje leku
        'NeedsMedP2': True,   # Pacjent 2 potrzebuje leku
        'NeedsTestP1': True,  # Pacjent 1 potrzebuje testu
        'NeedsTestP2': True,  # Pacjent 2 potrzebuje testu
        'HandsClean': False,  # Ręce pielęgniarki są brudne
        'CheckedChartP1': False, # Karta pacjenta 1 nie została sprawdzona
        'CheckedChartP2': False  # Karta pacjenta 2 nie została sprawdzona
    },
    {  # Cel - co chcemy osiągnąć?
        'NeedsMedP1': False,  # Pacjent 1 ma dostać lek
        'NeedsMedP2': False,  # Pacjent 2 ma dostać lek
        'NeedsTestP1': False, # Pacjent 1 ma mieć wykonany test
        'NeedsTestP2': False, # Pacjent 2 ma mieć wykonany test
        'CheckedChartP1': True, # Karta pacjenta 1 ma być sprawdzona
        'CheckedChartP2': True  # Karta pacjenta 2 ma być sprawdzona
    }
)

# Tworzenie planera STRIPS
planner = Forward_STRIPS(problem1)

# Tworzenie wyszukiwarki
search = SearcherMPP(planner)

# Wyszukiwanie rozwiązania
solution = search.search()

# Wyświetlenie znalezionego planu
print(solution)

