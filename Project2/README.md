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

#### **5. Pomiar Czasu Działania**

Czas rozwiązywania problemu planowania został zmierzony przy użyciu funkcji `time.time()`.

```python
start_time = time.time()

# Rozwiązanie problemu
solution = planner.solve()

end_time = time.time()
execution_time = end_time - start_time
print(f"Czas rozwiązywania problemu: {execution_time:.4f} sekundy")
```

---

#### **6. Wyniki**

Po uruchomieniu systemu planowania, czas rozwiązania problemu wahał się w zależności od złożoności problemu. Na przykład:

- Dla prostych problemów czas rozwiązania wynosił nawet 0.029 sekundy,
- Dla bardziej złożonych problemów (np. większa liczba pacjentów, większa liczba lokalizacji) czas rozwiązania wynosił do 40 sekund.

| Problem          | Bez Heurystyki | Forward Heuristic Hands | Forward Heuristic Tasks | Forward Heuristics Both |
|-----------------|----------------|-------------------------|-------------------------|-------------------------|
| simple_problem1 | 0.029          | 0.122                   | 0.011                   | 0.015                   |
| simple_problem2 | 10.99          | 18.18                   | 1.979                   | 10.804                  |
| simple_problem3 | 34.22          | 40.78                   | 31.009                  | 33.811                  |
| subproblem1     | 41.080         | 42.372                  | 37.859                  | 40.560                  |
| subproblem2     | 25.901         | 34.293                  | 21.556                  | 26.588                  |
| subproblem3     | 4.111          | 10.203                  | 1.137                   | 4.540                   |

---

#### **7. Wnioski**

- **Skalowalność**: System działa sprawnie w przypadku prostych problemów, ale złożoność czasowa wzrasta wraz z liczbą działań do wykonania. Wykorzystanie heurystyk jest dobrym podejściem zmniejszającym czas wykonania problemów.
- **Zastosowanie w praktyce**: System może być użyty w realnych warunkach szpitalnych do wsparcia pielęgniarek w codziennym planowaniu ich działań, zmniejszając czas potrzebny na realizację zadań.
- **Możliwości rozwoju**: W przyszłości system może zostać rozszerzony o nowe działania, takie jak interakcje z pacjentami oraz adaptację do dynamicznie zmieniających się warunków.

---
