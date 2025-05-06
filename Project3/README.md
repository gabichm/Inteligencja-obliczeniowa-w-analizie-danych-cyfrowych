### GRA CLIFFWALKING

### **1.Wstęp**
CliffWalking to gra opierająca się na przejściu agenta z przez planszę 4x12 rozpoczynając na
polu startowym do osiągnięcia wyznaczonego celu, unikając przy tym wpadnięcia do klifu.

**Przestrzeń rozgrywki**

- Pozycja startowa gracza na  polu [3,0]
- Docelowa pozycja gracza na pole [3,11]
- Przestrzeń klifu - wejście na nią powoduje reset gracza na start i duże kary punktowe - obejmuje pola od [3,1] do [3,10]
- Aktualna pozycja gracza = stan gry: obliczana jako "wiersz * 12 + kolumna"

**Sterowanie i akcja**

Gracz ma wybór między czterema akcjami:

- 0 - ruch w górę
- 1 - ruch w prawo
- 2 - ruch  w lewo 
- 3 - ruch w dół

**Nagrody**

- Każdy krok gracza "-1"
- Wpadnięcie do klifu "-100"

**Koniec gry**

Gra zostaje zakończona w momencie osiągnięcia przez gracza dolecowej pozycji na planszy.

### **2.Uczenie ze wzmocnieniem**

## **Q-learning**

**Na czym polega?**

W metodzie Q-learning agent uczy się, jaką akcję warto wykonać w danym 
stanie, by maksymalizować długoterminową sumę nagród. 
W każdej iteracji aktualizuje wartość Q (quality),
czyli ocenę kombinacji stan-akcja. Q-learning jest 
algorytmem off-policy – uczy się na podstawie najlepszej możliwej 
akcji, niezależnie od tego, jaką naprawdę wykonał agent. 
Dzięki temu potrafi szybciej znaleźć optymalne rozwiązanie, 
ale czasem bardziej ryzykuje.

**Implementacja**

W naszym projekcie zastosowaliśmy Q-learning do uczenia agenta, jak
bezpiecznie przejść przez planszę i dotrzeć do celu, 
unikając klifu. Agent buduje tablicę Q o wymiarach 
[liczba_stanów, liczba_akcji] i aktualizuje jej wartości po każdym
kroku według równania Bellmana. Zastosowano ε-greedy do zachowania 
balansu między eksploracją a eksploatacją, a także współczynnik 
dyskontowy γ = 0.9. Ta metoda dobrze sprawdza się w tym środowisku, 
ponieważ pozwala agentowi szybko uczyć się optymalnych ścieżek – nawet 
kosztem chwilowego ryzyka.



## **SARSA**


**Na czym polega?**

Jest to algorytm on-policy, co oznacza, że agent uczy się na podstawie 
rzeczywistych decyzji, które podejmuje w danym epizodzie. Zamiast 
patrzeć, co mogłoby być najlepsze w teorii, SARSA 
bierze pod uwagę faktyczną kolejną akcję agenta. Dzięki temu uczy się
bardziej zachowawczo – unika ryzykownych tras, nawet jeśli są one 
potencjalnie krótsze. 

**Implementacja**

W implementacji SARSA użyliśmy bardzo podobnych parametrów jak przy 
Q-learningu – ε-greedy, γ = 0.9 i tablicy Q. Główna różnica to sposób 
aktualizacji Q: zamiast szukać najlepszej akcji w kolejnym stanie, 
używamy rzeczywistej akcji, którą agent planuje wykonać. W rezultacie 
agent unika brzegów klifu i wybiera bezpieczniejsze ścieżki. To 
podejście sprawdza się szczególnie dobrze w środowiskach z dużymi 
karami (jak -100 za wejście do klifu), gdzie ryzyko się nie opłaca.

### **3.Wyniki**
**Porównanie wyników**

![Porównanie nagród](reward_q_vs_s.png)

![Porównanie liczby wykonanych kroków](steps_q_vs_s.png)

Q-Learning:
Najwyższa liczba punktów: -13 w epizodzie 141
Czas wykonania : 1.433 sekund

SARSA:
Najwyższa liczba punktów: -17 w epizodzie 243
Czas wykonania : 0.662 sekund

**Porównanie hiperparametrów**

Wszystkie poniższe dane powstały po puszczeniu 1000 epizodów gry.

| algorytm   | alpha | gamma | epsilon | srednia_nagroda | najlepszy_wynik | srednia_kroki | czas   |
|:-----------|:------|:------|:--------|:----------------|:----------------|:--------------|:-------|
| Q-Learning | 0.1   | 0.9   | 0.1     | -58.504         | -13             | 25.636        | 0.735  |
| SARSA      | 0.1   | 0.9   | 0.1     | -37.153         | -15             | 27.352        | 0.492  |
| Q-Learning | 0.1   | 0.7   | 0.1     | -61.28          | -13             | 26.828        | 0.583  |
| SARSA      | 0.1   | 0.7   | 0.1     | -36.705         | -17             | 28.488        | 0.516  |
| Q-Learning | 0.1   | 0.9   | 0.3     | -194.907        | -13             | 39.18         | 1.225  |
| SARSA      | 0.1   | 0.9   | 0.3     | -58.872         | -17             | 33.627        | 0.871  |
| Q-Learning | 0.1   | 0.7   | 0.3     | -191.222        | -13             | 39.95         | 1.092  |
| SARSA      | 0.1   | 0.7   | 0.3     | -180.322        | -17             | 154.978       | 3.027  |
| Q-Learning | 0.3   | 0.9   | 0.1     | -54.856         | -13             | 20.008        | 0.386  |
| SARSA      | 0.3   | 0.9   | 0.1     | -31.041         | -17             | 23.418        | 0.37   |
| Q-Learning | 0.3   | 0.7   | 0.1     | -53.397         | -13             | 20.133        | 0.356  |
| SARSA      | 0.3   | 0.7   | 0.1     | -108.322        | -17             | 101.986       | 1.614  |
| Q-Learning | 0.3   | 0.9   | 0.3     | -177.728        | -13             | 33.287        | 0.677  |
| SARSA      | 0.3   | 0.9   | 0.3     | -72.635         | -17             | 47.984        | 1.004  |
| Q-Learning | 0.5   | 0.9   | 0.1     | -54.232         | -13             | 18.79         | 0.339  |
| SARSA      | 0.5   | 0.9   | 0.1     | -320.481        | -17             | 310.68        | 5.512  |
| Q-Learning | 0.5   | 0.7   | 0.1     | -54.481         | -13             | 18.94         | 0.35   |


### **4.Wnioski**

Na podstawie przeprowadzonych eksperymentów można wyciągnąć kilka istotnych wniosków:

1. Skuteczność metod uczenia ze wzmocnieniem:
- Q-learning, który jest algorytmem off-policy znacznie częściej wybiera 
optymalne, a równocześnie bardziej ryzykowne ścieżki po brzegu klifu, co pozwala 
na znalezienie szybszego dotarcia do celu.
- SARSA, która natomiast jest algorytmem on-policy, wybiera bezpieczniejsze stategie
,trzymając się w pewnej odległości od klifu, co pozwala na zminimalizowanie kar, ale wydłuża drogę do celu.

2. Q-learning jest bardziej skuteczny w uczeniu się najkrótszych tras, ale często generuje przy tym  większe kary.
3. SARSA jest mało skuteczna w odnajdywaniu najmniej kosztownej trasy, za to w całokształcie generuje niższe kary.
4. Znaczący wpływ hiperparametrów:
- wysokie epsilony (exploration rate) prowadzą do większej eksploracji oniżając przy tym jakość nagród,
- wyższe alfa (learning rate) pozwala na szybszą naukę, ale powoduje niestabilność wyników,
- zmniejsze nie gammy (wspołczynnik dyskontowy) wpływa negatywnie na długoterminowe decyzje obniżając jakość wyników.


### PROBLEM MOUNTAIN CAR CONTINOUS
imo jak bardzo będzie nam sie chiało to do tego tez mozna jakas druga metode uczenia ze wzmocnieniem zrobic idk really zależy dla którego problemu będzi łatwiej


#### **1.Wstęp**
