# 1. Wprowadzenie

Gra Nim to klasyczna gra matematyczna, w której dwóch graczy na zmianę usuwa elementy z kilku stosów. Gracz, który usunie ostatni element, przegrywa. Nie ma W tym eksperymencie zaimplementowano grę Nim przy użyciu biblioteki easyAI, pozwalając dwóm agentom AI grać przeciwko sobie.

# 2. Implementacja Gry Nim

Kod został napisany w języku Python z wykorzystaniem easyAI oraz dwóch algorytmów AI:
 * **Negamax bez odcięcia alfa-beta(własnoręczna implementacja)** Jest to podstawowa implementacja algorytmu Negamax, gdzie nie używamy techniki przycinania alpha-beta. Zamiast tego, algorytm przeszukuje wszystkie możliwe ruchy i ocenia je, na podstawie zmiany gracza.
 * **Negamax z odcięciem alfa-beta(z biblioteki easyAI)** To bardziej zaawansowana wersja algorytmu Negamax z wykorzystaniem techniki alpha-beta pruning, która optymalizuje algorytm, eliminując niepotrzebne gałęzie w drzewie decyzyjnym.
 * **Expecti-minmax z odcięciem alfa-beta(własnoręczna implementcja)** Jest to rozszerzenie klasycznego minimax z obsługą graczy losowych, przy czym uwzględnia probabilistyczne aspekty gry. Technika alpha-beta pruning również jest zastosowana, co sprawia, że algorytm jest bardziej wydajny.

Gra obejmuje następujące funkcje:

 * **possible_moves()**: Określa możliwe ruchy w danej rundzie.

 * **make_move()**: Wykonuje ruch, zmniejszając liczbę elementów w wybranym stosie.

 * **win()**: Sprawdza, czy gra dobiegła końca.


# 3. Eksperymenty z AI

Eksperyment obejmował 18 symulowanych gier, w których AI grało przeciwko sobie, zamieniając się kolejnością rozpoczynania. Wyniki były następujące:

| Ekperyment | Zwycięca oraz średni czas ruchu (s)(gracz1/gracz2) | Głębokość sieci | Gra deterministyczna | Ilość rozgrywek | Algorytm       |
|------------|----------------------------------------------------|-----------------|----------------------|-----------------|----------------|
| 1          | 0 (0.005)/10 (0.004)                               | 3               | Tak                  | 10              | Negamax z ab   |
| 2          | 7 (0.0046)/3  (0.004)                              | 3               | Nie                  | 10              | Negamax z ab   |
| 3          | 10 (0.026)/0 ( 0.021)                              | 3               | Tak                  | 10              | Negamax bez ab |
| 4          | 3 (0.03)/7 (0.023)                                 | 3               | Nie                  | 10              | Negamax bez ab |
| 5          | 10 (0.008)/0 (0.008)                               | 3               | Tak                  | 10              | Expecti-minmax |
| 6          | 7 (0.011)/3 (0.011)                                | 3               | Nie                  | 10              | Expecti-minmax |
| 7          | 10 (0.012)/0 (0.009)                               | 4               | Tak                  | 10              | Negamax z ab   |
| 8          | 7 (0.012) /3 (0.01)                                | 4               | Nie                  | 10              | Negamax z ab   |
| 9          | 10 (0.165) /0 (0.121)                              | 4               | Tak                  | 10              | Negamax bez ab |
| 10         | 5 (0.181) /5 (0.129)                               | 4               | Nie                  | 10              | Negamax bez ab |
| 11         | 10 (0.039/0 (0.033)                                | 4               | Tak                  | 10              | Expecti-minmax |
| 12         | 5 (0.046) /5 (0.036)                               | 4               | Nie                  | 10              | Expecti-minmax |
| 13         | 10 (0.079) / 0 (0.083)                             | 6               | Tak                  | 10              | Negamax z ab   |
| 14         | 7 (0.109) / 3 (0.102)                              | 6               | Nie                  | 10              | Negamax z ab   |
| 15         | 10 (5.822) / 0 (3.002)                             | 6               | Tak                  | 10              | Negamax bez ab |
| 16         | 4 (7.260) / 6 (4.289)                              | 6               | Nie                  | 10              | Negamaz bez ab |
| 17         | 10 (2.007) / 0 (1.461)                             | 6               | Tak                  | 10              | Expecti-minmax |
| 18         | 3 (1.621) / 7 (1.279)                              | 6               | Nie                  | 10              | Expecti-minmax |

## Interpretacja wyników
Wyniki eksperymentów pokazują, że głębokość analizy (liczba poziomów w drzewie decyzyjnym) wpływa na liczbę zwycięstw danego agenta. Wyższa głębokość analizy (np. 6 lub 10) zwiększa szanse na zwycięstwo, ponieważ AI może rozważyć więcej możliwych ruchów i tym samym lepiej przewidywać reakcje przeciwnika.
Negamax bez obcinania alfa-beta miał najdłuższe czasy, co potwierdza nieefektywność algorytmu bez przycinania gałęzi. Dla większej głębokości czas wykonywania ruchów był zatrważająco długi.
# 4. Napotkane Problemy i Ich Rozwiązania

Podczas eksperymentów napotkano kilka problemów:

1. **Błąd 'list index out of range'**: Wynikał z błędnej obsługi pustej listy ruchów. Został rozwiązany poprzez dodatkowe sprawdzenie możliwych ruchów.

2. **Losowe błędy ruchów AI**: Wprowadzono mechanizm zmniejszający liczbę usuniętych elementów o 1 z 10% prawdopodobieństwem, co wprowadza losowość w rozgrywce.

3. **Brak przewagi dla AI rozpoczynającego grę**: Analiza wyników wykazała, że zmiana rozpoczynającego nie wpływa znacząco na wyniki.

# 5. Podsumowanie 
Eksperymenty przeprowadzone w grze Nim pozwoliły na ocenę skuteczności oraz wydajności różnych algorytmów wyszukiwania decyzji: Negamax z alfa-beta, Negamax bez alfa-beta oraz Expecti-Minmax.
* **Negamax z alfa-beta** był najbardziej efektywny – uzyskiwał dobre wyniki przy stosunkowo niskim czasie obliczeń. Technika alfa-beta pruning skutecznie redukowała liczbę analizowanych stanów.
* **Negamax bez alfa-beta** osiągał podobne wyniki pod względem wygranych, ale jego czas obliczeń rósł wykładniczo wraz ze wzrostem głębokości analizy, co czyniło go niepraktycznym przy większych wartościach.
* **Expecti-Minmax** sprawdzał się dobrze w grach niedeterministycznych, jego czas obliczeń był satysfakcjonujący.


# 6. Wnioski
* **Głębokość analizy kluczowa dla skuteczności**
Im większa głębokość przeszukiwania, tym lepsze wyniki osiągały algorytmy. Jednak przy głębokości 6 czasy obliczeń w Negamax bez alfa-beta były zbyt długie, co ograniczało jego praktyczność.
*  **Brak przewagi AI rozpoczynającego grę**
   Wyniki nie wykazały znaczącej różnicy w skuteczności między agentami rozpoczynającymi grę a tymi grającymi jako drudzy.