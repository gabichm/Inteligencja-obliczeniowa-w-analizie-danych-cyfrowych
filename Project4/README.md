### GRA WŁASNA - COLLECTGAME

### **1.Wstęp**
CollectGame jest to gra, w  której agent ma za zadanie zebrać jak największą ilość owoców omijając przy tym pojawiające się na planszy cukierki.

**Przestrzeń rozgrywki**

- Plansza 20x20
- Pozycja startowa gracza [10,10]
- Koniec gry następuje po wykonaniu 135 kroków

**Akcja**

Gracz, w każdym ruchu  ma do wyboru jedną z pięciu akcji:
- 0 - ruch w górę
- 1 - ruch w dółł
- 2 - ruch w lewo
- 3 - ruch w prawo
- 4 - pozostanie w miejscu

**Nagrody**

Przy każdym ruchu przemieszczającym gracza (akcja 0-3) gracz otrzymuje -0.2pkt.
Za zdobycie owoca gracz otrzymuje +10pkt.
Za zebranie cukierka gracz otrzymuje -10pkt.

**Przebieg gry**

Gracz poruszając się po planszy stara się zdobyć jak największą liczbę pojawiających się owoców. Owoce jak i cukierki, zostają na planszy do momentu ich 
zebrania lub do upłynięcia maksymalnego czasu (20 kolejnych kroków). Gracz stara się zminimalizować koszt ruchów, jednocześnie omijając pojawiające się na przestrzeni gry cukierki.

**Koniec gry**

Gra zostaje zakończona po upłynięciu czasu -wykonanie maksymalnej ilości akcji : 135.

### **2.Aktor i uczenie ze wzmacnianiem**

W celu przetestowania naszej gry wykorzystujemy dwie metody uczenia ze wzmacnianiem : Q-learning oraz SARSA.

**Q-learning**

**SARSA**

### **3.Wnioski**

### **4.Grafika środowiska**
