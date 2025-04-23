### GRA CLIFFWALKING
do tego będzie druga wersja uczenia ze wzmocnieniem do 8 pkt- rózne paramtry porównac zeby było cos do sprawka dla 1000 epoch , mozna sieci neuronowe whatever we want i guess
#### **1.Wstęp**
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

#### **2.Uczenie ze wzmocnieniem**





### PROBLEM MOUNTAIN CAR CONTINOUS
imo jak bardzo będzie nam sie chiało to do tego tez mozna jakas druga metode uczenia ze wzmocnieniem zrobic idk really zależy dla którego problemu będzi łatwiej

#### **1.Wstęp**
