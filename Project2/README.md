### System Planowania Opieki Szpitalnej

---

#### **1. Wstęp**

W niniejszym projekcie zajmujemy się opracowaniem systemu planowania opieki pielęgniarskiej w szpitalu, przy użyciu technik sztucznej inteligencji (AI), w tym algorytmu planowania opisanego w logice STRIPS (Stan-Opis-Rzeczywistość). Celem systemu jest automatyczne generowanie sekwencji działań pielęgniarki w oparciu o dostępne zasoby, wymagania medyczne i czas.

System ma na celu:
- Planowanie działań pielęgniarki na różnych stacjach szpitalnych (np. pokój pacjenta, apteka, zlew),
- Realizację różnych zadań pielęgniarki, takich jak dostarczenie leków, przeprowadzenie testów, rozmowy z pacjentami,
- Zoptymalizowanie działania pielęgniarki w kontekście ograniczonych zasobów (np. medykamenty, czas, wolne ręce).

---

#### **2. Założenia i Zakres Projektu**

Projekt opiera się na stworzeniu modelu domeny opieki szpitalnej oraz sformułowaniu problemu planowania z wykorzystaniem reprezentacji w logice STRIPS. Model ten uwzględnia:
- **Lokalizacje pielęgniarki** w szpitalu, takie jak stacja, pokój pacjenta, apteka i zlew,
- **Zasoby pielęgniarki**, takie jak  wolne ręce, posiadane leki,
- **Zadania pielęgniarki**, takie jak podawanie leków, przeprowadzanie testów, mycie rąk, rozmowy z pacjentami.


Zakres projektu obejmuje:
- Implementację modelu STRIPS i domeny opieki szpitalnej,
- Implementację funkcji planowania z użyciem algorytmu Forward STRIPS,
- Analizę wydajności systemu poprzez mierzenie czasu działania algorytmu.

---

#### **3. Opis Działania Systemu**

##### **3.1. Model Domena STRIPS**
Model w logice STRIPS reprezentuje stan systemu, czyli stan poszczególnych zmiennych (np. lokalizacji pielęgniarki, dostępności leków, stanu rąk pielęgniarki). Przykładami działań w tej domenie są:
- **Przemieszczanie pielęgniarki** pomiędzy różnymi lokalizacjami,
- **Pobieranie leków** z apteki,
- **Wykonywanie testów medycznych**,
- **Przeprowadzanie rozmów** z pacjentami.

Każde z działań posiada określone warunki wstępne (preconditions) i efekty (effects), które zmieniają stan systemu.

##### **3.2. Problem Planowania**
Problem planowania polega na ustaleniu sekwencji działań, które pielęgniarka powinna wykonać, aby zrealizować wszystkie wymagania przy jak najmniejszym zużyciu zasobów (np. czasu).

Dane wejściowe:
- **Początkowy stan**: Określa początkową konfigurację systemu (np. lokalizacje pielęgniarki, dostępność zasobów),
- **Cele**: Określają, jakie zadania pielęgniarka ma wykonać (np. dostarczenie leków pacjentom, przeprowadzenie testów).

Algorytm planowania generuje sekwencję działań, która przekształca początkowy stan w stan spełniający cele.

##### **3.3. Algorytm Forward STRIPS**
Algorytm Forward STRIPS generuje rozwiązanie problemu planowania, rozpoczynając od początkowego stanu i stopniowo dodając działania, które przybliżają system do stanu docelowego. Algorytm ten działa w sposób iteracyjny, starając się znaleźć najkrótszą i najbardziej efektywną sekwencję działań.

---

#### **4. Implementacja**

##### **4.1. Definicja Domena**
W definicji domeny określamy dostępne lokalizacje pielęgniarki, dostępność medykamentów, stan rąk, czy potrzeby pacjentów. Każda z tych cech jest reprezentowana za pomocą zmiennych logicznych.

```python
hospital_care_domain = STRIPS_domain(
    {
        'NLoc': {'station', 'room', 'pharmacy', 'sink'},  # Lokalizacja pielęgniarki
        'EmptyHands': {0, 1, 2},
        'HasMedA': {0, 1, 2},
        'HasMedB': {0, 1, 2},
        'HasMedC': {0, 1, 2},
        # ...
    },
    {
        # Przemieszczanie pielęgniarki
        Strips('MOVE_NURSE_s_r', {'NLoc': 'station'}, {'NLoc': 'room'}),
        # ...
    }
)
```

##### **4.2. Problem Planowania**
W tej części definiujemy konkretne zadania pielęgniarki, jakie należy wykonać, oraz początkowy stan.

```python
planning_problem = Planning_problem(
    # Określenie początkowego stanu, np. 'NLoc': 'station', 'EmptyHands': 0
    initial_state={
        'NLoc': 'station',
        'EmptyHands': 0,
        'HasMedA': 0,
        'HasMedB': 0,
        'HasMedC': 0
        # ...
    },
    # Cele do osiągnięcia, np. pielęgniarka musi dostarczyć leki
    goal_state={
        'HasMedA': 1,
        'HasMedB': 1
        # ...
    }
)
```

##### **4.3. Planowanie i Wykonanie**
Algorytm planowania uruchamiany jest na podstawie danych wejściowych i rozwiązuje problem generując sekwencję działań.

```python
planner = Forward_STRIPS(hospital_care_domain, planning_problem)
solution = planner.solve()
```

---

##### 5.1. Heurystyka *h_pending_tasks*

Heurystyka *h_pending_tasks* została zaprojektowana w celu oceny stanu zadań, które wymagają realizacji. Główne założenie tej heurystyki polega na monitorowaniu liczby nierozwiązanych zadań oraz ich priorytetu, co pozwala na optymalizację procesu realizacji zleceń.

- *Działanie:* Heurystyka ta analizuje zadania w kolejce, biorąc pod uwagę zarówno ich liczbę, jak i wagę (priorytet). Na tej podstawie system decyduje o kolejności wykonania zadań, zapewniając, że te o wyższym priorytecie będą realizowane w pierwszej kolejności.
- *Zalety:* Dzięki zastosowaniu tej heurystyki możliwe jest lepsze zarządzanie czasem oraz zasobami, co prowadzi do zmniejszenia opóźnień w realizacji zadań. Dodatkowo, system jest w stanie adaptować się do zmieniających się warunków, co pozwala na bardziej dynamiczne dostosowywanie priorytetów.
- *Przykład:* W kontekście zarządzania projektem, zadania, które mają termin wykonania na krótko, będą realizowane przed tymi, które mają mniej pilny charakter. Dzięki temu całość procesu przebiega sprawniej i bardziej efektywnie.

##### 5.2. Heurystyka *h_hand_hygiene*

Heurystyka *h_hand_hygiene* została zaimplementowana w celu zapewnienia odpowiednich standardów higieny rąk w środowisku pracy, co ma kluczowe znaczenie w kontekście zapobiegania zakażeniom i utrzymania wysokich standardów zdrowotnych w firmie.

- *Działanie:* Heurystyka ta analizuje czas i częstotliwość przeprowadzania działań związanych z higieną rąk. System monitoruje, czy osoby w danym środowisku (np. w zakładzie produkcyjnym czy medycznym) przestrzegają procedur dezynfekcji rąk, oraz automatycznie przypomina o konieczności ich wykonania w odpowiednich odstępach czasu.
- *Zalety:* Dzięki tej heurystyce, ryzyko przenoszenia patogenów jest znacznie zmniejszone, a przestrzeganie standardów higieny wpływa pozytywnie na bezpieczeństwo wszystkich osób w danym środowisku. Dodatkowo, system przypomina o konieczności dezynfekcji, co zwiększa skuteczność jej wdrożenia.
- *Przykład:* W szpitalu czy klinice, personel medyczny otrzymuje przypomnienie o konieczności dezynfekcji rąk przed i po każdej wizycie u pacjenta. To zmniejsza ryzyko zakażeń oraz poprawia ogólną higienę.

---

#### **6. Wyniki**

Po uruchomieniu systemu planowania, czas rozwiązania problemu wahał się w zależności od złożoności problemu. Na przykład:

- Dla prostych problemów czas rozwiązania wynosił nawet poniżej sekundy,
- Dla bardziej złożonych problemów (np. większa liczba pacjentów, większa liczba lokalizacji) czas rozwiązania wynosił blisko 3 minut.
- Można stworzyć bardziej złożone problemy, jednak ich wykonanie zajmowałoby znaczną ilość czasu.

| Problem                             | Ilość kroków do wykonania | Bez Heurystyki [s] | Forward Heuristic Hands [s] | Forward Heuristic Tasks [s] | Forward Heuristics Both [s] |
|-------------------------------------|---------------------------|--------------------|-----------------------------|-----------------------------|-----------------------------|
| simple_problem1                     | 6                         | 0.609              | 2.628                       | 0.322                       | 0.538                       |
| simple_problem1 without subproblems | 4                         | 0.053              | 0.183                       | 0.019                       | 0.050                       |
| simple_problem2                     | 8                         | 0.370              | 0.444                       | 0.332                       | 0.323                       |
| simple_problem2 without subproblems | 6                         | 0.170              | 0.271                       | 0.066                       | 0.180                       |
| simple_problem3                     | 14                        | 4.401              | 5.134                       | 3.479                       | 4.560                       |
| simple_problem3 without subproblems | 12                        | 2.407              | 3.296                       | 2.697                       | 2.599                       |
| complex_problem1                    | 22                        | 56.590             | 69.800                      | 56.163                      | 55.270                      |
| complex_problem2                    | 22                        | 159.123            | 170.738                     | 154.763                     | 157.763                     |
| complex_problem3                    | 20                        | 27.693             | 28.760                      | 24.748                      | 25.668                      |
---

#### **7. Wnioski**

- **Skalowalność**: System działa sprawnie w przypadku prostych problemów, ale złożoność czasowa wzrasta wraz z liczbą działań do wykonania. 
- **Wykorzystanie heurystyk**: Heurystyki przy mniej skomplikowanych problemach nie są wymagane, czasem ich wykorzystanie jedynie zwiększa czas wykonania(czas do obliczeń), dla bardziej rozbduowanych problemów Heurystyka fakytcznie skraca czas wykonania. 
- **Zastosowanie w praktyce**: System może być użyty w realnych warunkach szpitalnych do wsparcia pielęgniarek w codziennym planowaniu ich działań, zmniejszając czas potrzebny na realizację zadań.
- **Możliwości rozwoju**: W przyszłości system może zostać rozszerzony o nowe działania, takie jak interakcje z pacjentami oraz adaptację do dynamicznie zmieniających się warunków.

---
