# stripsProblem.py - STRIPS Representations of Actions
# AIFCA Python code Version 0.9.15 Documentation at https://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents https://artint.info
# Copyright 2017-2024 David L. Poole and Alan K. Mackworth
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: https://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

class Strips(object):
    def __init__(self, name, preconds, effects, cost=1):
        """
        defines the STRIPS representation for an action:
        * name is the name of the action
        * preconds, the preconditions, is feature:value dictionary that must hold
        for the action to be carried out
        * effects is a feature:value map that this action makes
        true. The action changes the value of any feature specified
        here, and leaves other features unchanged.
        * cost is the cost of the action
        """
        self.name = name
        self.preconds = preconds
        self.effects = effects
        self.cost = cost

    def __repr__(self):
        return self.name

class STRIPS_domain(object):
    def __init__(self, feature_domain_dict, actions):
        """Problem domain
        feature_domain_dict is a feature:domain dictionary, 
                mapping each feature to its domain
        actions
        """
        self.feature_domain_dict = feature_domain_dict
        self.actions = actions

class Planning_problem(object):
    def __init__(self, prob_domain, initial_state, goal):
        """
        a planning problem consists of
        * a planning domain
        * the initial state
        * a goal 
        """
        self.prob_domain = prob_domain
        self.initial_state = initial_state
        self.goal = goal

boolean = {False, True}
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
               {'NLoc': 'room', 'HasMedA': 1,'EmptyHands': 1, 'NeedsMedP1A': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1A': False, 'HasMedA': 0, 'HandsClean': False, 'EmptyHands': 0}),
        Strips('ADMINISTER_MEDICATION_p1A1BC',
               {'NLoc': 'room', 'HasMedA': 1,'EmptyHands': 2, 'NeedsMedP1A': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1A': False, 'HasMedA': 0, 'HandsClean': False, 'EmptyHands': 1}),
        Strips('ADMINISTER_MEDICATION_p2A1',
               {'NLoc': 'room', 'HasMedA': 1,'EmptyHands': 1, 'NeedsMedP2A': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2A': False, 'HasMedA': 0, 'HandsClean': False, 'EmptyHands': 0}),
        Strips('ADMINISTER_MEDICATION_p2A1BC',
               {'NLoc': 'room', 'HasMedA': 1,'EmptyHands': 2, 'NeedsMedP2A': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2A': False, 'HasMedA': 0, 'HandsClean': False, 'EmptyHands': 1}),
        Strips('ADMINISTER_MEDICATION_p1A2',
               {'NLoc': 'room', 'HasMedA': 2, 'NeedsMedP1A': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1A': False, 'HasMedA': 1, 'HandsClean': False, 'EmptyHands': 1}),
        Strips('ADMINISTER_MEDICATION_p2A2',
               {'NLoc': 'room', 'HasMedA': 2, 'NeedsMedP2A': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2A': False, 'HasMedA': 1, 'HandsClean': False, 'EmptyHands': 1}),
        Strips('ADMINISTER_MEDICATION_p1B1',
               {'NLoc': 'room', 'HasMedB': 1,'EmptyHands': 1, 'NeedsMedP1B': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1B': False, 'HasMedB': 0, 'HandsClean': False, 'EmptyHands': 0}),
        Strips('ADMINISTER_MEDICATION_p2B1',
               {'NLoc': 'room', 'HasMedB': 1,'EmptyHands': 1, 'NeedsMedP2B': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2B': False, 'HasMedB': 0, 'HandsClean': False, 'EmptyHands': 0}),
        Strips('ADMINISTER_MEDICATION_p1B1AC',
               {'NLoc': 'room', 'HasMedB': 1,'EmptyHands': 2, 'NeedsMedP1B': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1B': False, 'HasMedB': 0, 'HandsClean': False, 'EmptyHands': 1}),
        Strips('ADMINISTER_MEDICATION_p2B1AC',
               {'NLoc': 'room', 'HasMedB': 1,'EmptyHands': 2, 'NeedsMedP2B': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2B': False, 'HasMedB': 0, 'HandsClean': False, 'EmptyHands': 1}),
        Strips('ADMINISTER_MEDICATION_p1B2',
               {'NLoc': 'room', 'HasMedB': 2, 'NeedsMedP1B': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1B': False, 'HasMedB': 1, 'HandsClean': False, 'EmptyHands': 1}),
        Strips('ADMINISTER_MEDICATION_p2B2',
               {'NLoc': 'room', 'HasMedB': 2, 'NeedsMedP2B': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2B': False, 'HasMedB': 1, 'HandsClean': False, 'EmptyHands': 1}),
        Strips('ADMINISTER_MEDICATION_p1C1',
               {'NLoc': 'room', 'HasMedC': 1,'EmptyHands': 1, 'NeedsMedP1C': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1C': False, 'HasMedC': 0, 'HandsClean': False, 'EmptyHands': 0}),
        Strips('ADMINISTER_MEDICATION_p2C1',
               {'NLoc': 'room', 'HasMedC': 1,'EmptyHands': 2, 'NeedsMedP2C': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2C': False, 'HasMedC': 0, 'HandsClean': False, 'EmptyHands': 1}),
        Strips('ADMINISTER_MEDICATION_p1C1AB',
               {'NLoc': 'room', 'HasMedC': 1,'EmptyHands': 2, 'NeedsMedP1C': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1C': False, 'HasMedC': 0, 'HandsClean': False, 'EmptyHands': 1}),
        Strips('ADMINISTER_MEDICATION_p2C1AB',
               {'NLoc': 'room', 'HasMedC': 1,'EmptyHands': 2, 'NeedsMedP2C': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2C': False, 'HasMedC': 0, 'HandsClean': False, 'EmptyHands': 1}),
        Strips('ADMINISTER_MEDICATION_p1C2',
               {'NLoc': 'room', 'HasMedC': 2,'EmptyHands': 2, 'NeedsMedP1C': True, 'HandsClean': True, 'CheckedChartP1': True},
               {'NeedsMedP1C': False, 'HasMedC': 1, 'HandsClean': False, 'EmptyHands': 1}),
        Strips('ADMINISTER_MEDICATION_p2C2',
               {'NLoc': 'room', 'HasMedC': 2,'EmptyHands': 2, 'NeedsMedP2C': True, 'HandsClean': True, 'CheckedChartP2': True},
               {'NeedsMedP2C': False, 'HasMedC': 1, 'HandsClean': False, 'EmptyHands': 1}),

        # Przeprowadzenie testu
        Strips('CONDUCT_TEST_p1',
               {'NLoc': 'room', 'NeedsTestP1': True, 'HandsClean': True},
               {'NeedsTestP1': False, 'HandsClean': False}),
        Strips('CONDUCT_TEST_p2',
               {'NLoc': 'room', 'NeedsTestP2': True, 'HandsClean': True},
               {'NeedsTestP2': False, 'HandsClean': False}),

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
simple_problem1 = Planning_problem( # Cele: pacjent 2 test| Podcele: aktualizacja karty p1 i p2
    hospital_care_domain,
    {
        'NLoc': 'room',
        'EmptyHands': 0, 
        'HasMedA': 0,  
        'HasMedB': 0,
        'HasMedC': 0, 
        'NeedsMedP1A': False, 
        'NeedsMedP1B': False,
        'NeedsMedP1C': False, 
        'NeedsMedP2A': False,
        'NeedsMedP2B': False,
        'NeedsMedP2C': False,
        'NeedsTestP1': False,
        'NeedsTestP2': True, 
        'HandsClean': False,
        'CheckedChartP1': False,
        'CheckedChartP2': True, 
        'UpToDateChartP1': False,
        'UpToDateChartP2': False,  
        'TookBreak': False,  
        'TalkToP1': False,  
        'TalkToP2': False, },
    {'NeedsTestP2': False, 'UpToDateChartP1' : True, 'UpToDateChartP2': True}
)
#  Prosty Problem 2
simple_problem2 = Planning_problem( # Cele: pacjent 1 lek A | Podcele: Przerwa, rozmowa p2
    hospital_care_domain,
    {
        'NLoc': 'station', 
        'EmptyHands': 2, 
        'HasMedA': 1,
        'HasMedB': 0,
        'HasMedC': 1,
        'NeedsMedP1A': True,
        'NeedsMedP1B': False,
        'NeedsMedP1C': False,
        'NeedsMedP2A': False,
        'NeedsMedP2B': False,
        'NeedsMedP2C': False,
        'NeedsTestP1': False, 
        'NeedsTestP2': False, 
        'HandsClean': True, 
        'CheckedChartP1': False, 
        'CheckedChartP2': False, 
        'UpToDateChartP1': False, 
        'UpToDateChartP2': False, 
        'TookBreak': False, 
        'TalkToP1': False,  
        'TalkToP2': False,  
    },
    {'NeedsMedP1A': False, 'TalkToP2' : True, 'TookBreak' : True}  
)


# Prosty Problem 3
simple_problem3 = Planning_problem( # Cele: pacjent 1 - lek A i B| Podcele: rozmowa z p1 i aktualizacja karty
    hospital_care_domain,
    {
        'NLoc': 'room',  
        'EmptyHands': 0,  
        'HasMedA': 0,  
        'HasMedB': 0,  
        'HasMedC': 0,  
        'NeedsMedP1A': True,  
        'NeedsMedP1B': True,  
        'NeedsMedP1C': False,
        'NeedsMedP2A': False,
        'NeedsMedP2B': False,
        'NeedsMedP2C': False,
        'NeedsTestP1': False, 
        'NeedsTestP2': False, 
        'HandsClean': False,  
        'CheckedChartP1': False, 
        'CheckedChartP2': False,  
        'UpToDateChartP1': False,  
        'UpToDateChartP2': True,  
        'TookBreak': True,  
        'TalkToP1': False, 
        'TalkToP2': False, },
    {'NeedsMedP1A': False, 'NeedsMedP1B': False, 'TalkToP1': True, 'UpToDateChartP1': True}  
)

subproblem_1 =  Planning_problem( # Cele: pacjent 1 - lek A i B i C , test | Podcele: przerwa, aktualizacja karty p1
    hospital_care_domain,
    {
        'NLoc': 'station', 
        'EmptyHands': 0,  
        'HasMedA': 0,  
        'HasMedB': 0, 
        'HasMedC': 0, 
        'NeedsMedP1A': True, 
        'NeedsMedP1B': True,  
        'NeedsMedP1C': True, 
        'NeedsMedP2A': False,
        'NeedsMedP2B': False,
        'NeedsMedP2C': False,
        'NeedsTestP1': True, 
        'NeedsTestP2': False,
        'HandsClean': True,  
        'CheckedChartP1': False, 
        'CheckedChartP2': True,
        'UpToDateChartP1': False,
        'UpToDateChartP2': True, 
        'TookBreak': False,  
        'TalkToP1': False, 
        'TalkToP2': False, },
    {'NeedsMedP1A': False, 'NeedsMedP1B': False, 'NeedsMedP1C': False,'NeedsTestP1': False, 'TookBreak' : True, 'UpToDateChartP1': True}
)

subproblem_2 = Planning_problem( # Cele: pacjent 1 - lek A, pacjent 2 - lek A i B | Podcele: rozmowa p1 i p2, przerwa, aktualizacja karty p1
    hospital_care_domain,
    {
        'NLoc': 'station',
        'EmptyHands': 1,
        'HasMedA': 1,  
        'HasMedB': 0,
        'HasMedC': 0,  
        'NeedsMedP1A': True, 
        'NeedsMedP1B': False,  
        'NeedsMedP1C': False,  
        'NeedsMedP2A': True,  
        'NeedsMedP2B': True,
        'NeedsMedP2C': False,
        'NeedsTestP1': False,
        'NeedsTestP2': False, 
        'HandsClean': False,  
        'CheckedChartP1': False, 
        'CheckedChartP2': False, 
        'UpToDateChartP1': False, 
        'UpToDateChartP2': False,  
        'TookBreak': False,  
        'TalkToP1': False,  
        'TalkToP2': False,  
    },
    {'UpToDateChartP1': True, 'TookBreak': True, 'TalkToP2': True, 'TalkToP1': True, 'NeedsMedP1A': False, 'NeedsMedP2A': False, 'NeedsMedP2B': False}  
)

subproblem_3= Planning_problem( # Cele: pacjent 1 - lek C, pacjent 2 - test, lek C | Podcele: przerwa, aktualizacja kart obu pacjentów
    hospital_care_domain,
    {
        'NLoc': 'station',
        'EmptyHands': 2,
        'HasMedA': 0,
        'HasMedB': 1,  
        'HasMedC': 1, 
        'NeedsMedP1A': False, 
        'NeedsMedP1B': False, 
        'NeedsMedP1C': True,  
        'NeedsMedP2A': False,  
        'NeedsMedP2B': False,  
        'NeedsMedP2C': True,  
        'NeedsTestP1': False,  
        'NeedsTestP2': True,  
        'HandsClean': False,  
        'CheckedChartP1': False,  
        'CheckedChartP2': False,  
        'UpToDateChartP1': False,  
        'UpToDateChartP2': False,  
        'TookBreak': False, 
        'TalkToP1': False,  
        'TalkToP2': False,  
    },
    {'CheckedChartP2': True, 'NeedsTestP2': False, 'TookBreak': True, 'TalkToP2': True, 'NeedsMedP1C': False, 'NeedsMedP2C': False, 'UpToDateChartP2': True, 'UpToDateChartP1': True}  
)


# problem0 = Planning_problem(delivery_domain,
#                             {'RLoc':'lab', 'MW':True, 'SWC':True, 'RHC':False,
#                              'RHM':False},
#                             {'RLoc':'off'})
# problem1 = Planning_problem(delivery_domain,
#                             {'RLoc':'lab', 'MW':True, 'SWC':True, 'RHC':False,
#                              'RHM':False},
#                             {'SWC':False})
# problem2 = Planning_problem(delivery_domain,
#                             {'RLoc':'lab', 'MW':True, 'SWC':True, 'RHC':False,
#                              'RHM':False},
#                             {'SWC':False, 'MW':False, 'RHM':False})

### blocks world
def move(x,y,z):
    """string for the 'move' action"""
    return 'move_'+x+'_from_'+y+'_to_'+z
def on(x):
    """string for the 'on' feature"""
    return x+'_is_on'
def clear(x):
    """string for the 'clear' feature"""
    return 'clear_'+x
def create_blocks_world(blocks = {'a','b','c','d'}):
    blocks_and_table = blocks | {'table'}
    stmap =  {Strips(move(x,y,z),{on(x):y, clear(x):True, clear(z):True}, 
                                 {on(x):z, clear(y):True, clear(z):False})
                    for x in blocks
                    for y in blocks_and_table
                    for z in blocks
                    if x!=y and y!=z and z!=x}
    stmap.update({Strips(move(x,y,'table'), {on(x):y, clear(x):True}, 
                                 {on(x):'table', clear(y):True})
                    for x in blocks
                    for y in blocks
                    if x!=y})
    feature_domain_dict = {on(x):blocks_and_table-{x} for x in blocks}
    feature_domain_dict.update({clear(x):boolean for x in blocks_and_table})
    return STRIPS_domain(feature_domain_dict, stmap)

blocks1dom = create_blocks_world({'a','b','c'})
blocks1 = Planning_problem(blocks1dom,
     {on('a'):'table', clear('a'):True,
      on('b'):'c',  clear('b'):True,
      on('c'):'table', clear('c'):False}, # initial state
     {on('a'):'b', on('c'):'a'})  #goal

blocks2dom = create_blocks_world({'a','b','c','d'})
tower4 = {clear('a'):True, on('a'):'b',
          clear('b'):False, on('b'):'c',
          clear('c'):False, on('c'):'d',
          clear('d'):False, on('d'):'table'}
blocks2 = Planning_problem(blocks2dom,
     tower4, # initial state
     {on('d'):'c',on('c'):'b',on('b'):'a'})  #goal

blocks3 = Planning_problem(blocks2dom,
     tower4, # initial state
     {on('d'):'a', on('a'):'b', on('b'):'c'})  #goal

