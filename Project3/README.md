### GRA CLIFFWALKING
do tego będzie druga wersja uczenia ze wzmocnieniem do 8 pkt- rózne paramtry porównac zeby było cos do sprawka dla 1000 epoch , mozna sieci neuronowe whatever we want i guess
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

Gra zostaje zakończona w momencie osiągnięcie gracza dolecowej pozycji na planszy.

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

**Wyniki**

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

**Wyniki**

###


### PROBLEM MOUNTAIN CAR CONTINOUS
imo jak bardzo będzie nam sie chiało to do tego tez mozna jakas druga metode uczenia ze wzmocnieniem zrobic idk really zależy dla którego problemu będzi łatwiej


#### **1.Wstęp**
