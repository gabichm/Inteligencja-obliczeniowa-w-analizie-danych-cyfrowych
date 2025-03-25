import sys
import matplotlib.pyplot as plt
sys.path.append("C:\\Users\\Gabrysia\\PycharmProjects\\Inteligencja-obliczeniowa\\aipython")
from aipython.searchMPP import SearcherMPP
from aipython.stripsProblem import STRIPS_domain, Planning_problem, Strips
from aipython.stripsForwardPlanner import Forward_STRIPS


hospital_care_domain = STRIPS_domain(
    {
        'NLoc': {'station', 'room1', 'room2', 'pharmacy', 'sink'},  # Lokalizacja pielęgniarki
        'HasMed': {False, True},  # Czy pielęgniarka ma lek
        'NeedsMedP1': {False, True},  # Czy pacjent potrzebuje leku
        'NeedsMedP2': {False, True},
        'NeedsTestP1': {False, True},  # Czy pacjent potrzebuje testu
        'NeedsTestP2': {False, True},
        'HandsClean': {False, True},  # Czy pielęgniarka ma czyste ręce
        'CheckedChartP1': {False, True},  # Czy pielęgniarka sprawdziła kartę pacjenta
        'CheckedChartP2': {False, True}
    },
    {
        # Przemieszczanie pielęgniarki
        Strips('MOVE_NURSE_s_r1',
               {'NLoc': 'station'},
               {'NLoc': 'room1'}),
        Strips('MOVE_NURSE_s_r2',
               {'NLoc': 'station'},
               {'NLoc': 'room2'}),
        Strips('MOVE_NURSE_s_ph',
              {'NLoc': 'station'},
              {'NLoc': 'pharmacy'}),
        Strips('MOVE_NURSE_s_sink',
               {'NLoc': 'station'},
               {'NLoc': 'sink'}),
        Strips('MOVE_NURSE_r1_s',
               {'NLoc': 'room1'},
               {'NLoc': 'station'}),
        Strips('MOVE_NURSE_r1_r2',
               {'NLoc': 'room1'},
               {'NLoc': 'room2'}),
        Strips('MOVE_NURSE_r1_ph',
               {'NLoc': 'room1'},
               {'NLoc': 'pharmacy'}),
        Strips('MOVE_NURSE_r1_sink',
               {'NLoc': 'room1'},
               {'NLoc': 'sink'}),
        Strips('MOVE_NURSE_r2_r1',
               {'NLoc': 'room2'},
               {'NLoc': 'room1'}),
        Strips('MOVE_NURSE_r2_s',
               {'NLoc': 'room2'},
               {'NLoc': 'station'}),
        Strips('MOVE_NURSE_r2_ph',
               {'NLoc': 'room2'},
               {'NLoc': 'pharmacy'}),
        Strips('MOVE_NURSE_r2_sink',
               {'NLoc': 'room2'},
               {'NLoc': 'sink'}),
        Strips('MOVE_NURSE_ph_r1',
               {'NLoc': 'pharmacy'},
               {'NLoc': 'room1'}),
        Strips('MOVE_NURSE_ph_r2',
               {'NLoc': 'pharmacy'},
               {'NLoc': 'room2'}),
        Strips('MOVE_NURSE_ph_s',
               {'NLoc': 'pharmacy'},
               {'NLoc': 'station'}),
        Strips('MOVE_NURSE_ph_sink',
               {'NLoc': 'pharmacy'},
               {'NLoc': 'sink'}),
        Strips('MOVE_NURSE_sink_r1',
               {'NLoc': 'sink'},
               {'NLoc': 'room1'}),
        Strips('MOVE_NURSE_sink_r2',
               {'NLoc': 'sink'},
               {'NLoc': 'room2'}),
        Strips('MOVE_NURSE_sink_ph',
               {'NLoc': 'sink'},
               {'NLoc': 'pharmacy'}),
        Strips('MOVE_NURSE_sink_station',
               {'NLoc': 'sink'},
               {'NLoc': 'station'}),
        
        # Pobranie leku
        Strips('COLLECT_MEDICATION',
               {'NLoc': 'pharmacy'},
               {'HasMed': True}),
        

        # Mycie rąk
        Strips('WASH_HANDS',
               {'NLoc': 'sink'},
               {'HandsClean': True}),

        # Sprawdzenie karty pacjenta
        Strips('CHECK_CHART_p1',
               {'NLoc': 'room1', 'CheckedChartP1': False},
               {'CheckedChartP1': True}),
        Strips('CHECK_CHART_p2',
               {'NLoc': 'room2', 'CheckedChartP2': False},
               {'CheckedChartP2': True}),

        # Podanie leku
        Strips('ADMINISTER_MEDICATION_p1',
               {'NLoc': 'room1', 'HasMed': True, 'NeedsMedP1': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1': False, 'HasMed': False}),
        Strips('ADMINISTER_MEDICATION_p2',
               {'NLoc': 'room2', 'HasMed': True, 'NeedsMedP2': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2': False, 'HasMed': False}),

        # Przeprowadzenie testu
        Strips('CONDUCT_TEST_p1',
               {'NLoc': 'room1', 'NeedsTestP1': True},
               {'NeedsTestP1': False}),
        Strips('CONDUCT_TEST_p2',
               {'NLoc': 'room2', 'NeedsTestP2': True},
               {'NeedsTestP2': False})
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

