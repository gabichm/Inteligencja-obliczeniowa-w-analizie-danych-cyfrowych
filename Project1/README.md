# 1. Wprowadzenie

Gra Nim to klasyczna gra matematyczna, w której dwóch graczy na zmianę usuwa elementy z kilku stosów. Gracz, który usunie ostatni element, przegrywa. Nie ma W tym eksperymencie zaimplementowano grę Nim przy użyciu biblioteki easyAI, pozwalając dwóm agentom AI grać przeciwko sobie.

# 2. Implementacja Gry Nim

Kod został napisany w języku Python z wykorzystaniem easyAI. Zastosowano algorytm Negamax o głębokości wyszukiwania równej 3, co pozwala sztucznej inteligencji analizować możliwe ruchy i wybierać najlepsze decyzje.

Gra obejmuje następujące funkcje:

 * **possible_moves()**: Określa możliwe ruchy w danej rundzie.

 * **make_move()**: Wykonuje ruch, zmniejszając liczbę elementów w wybranym stosie.

* **win()**: Sprawdza, czy gra dobiegła końca.

 * **play_ai_vs_ai()**: Uruchamia mecze pomiędzy dwoma agentami AI i rejestruje wyniki.

## Algorytm gry 
Zastosowany algorytm Negamax analizuje możliwe ruchy w grze w trzech krokach: ocenia bieżący stan gry, wybiera najlepszy ruch, a następnie rekurencyjnie ocenia kolejne możliwe stany gry w odpowiedzi na wybrany ruch. Głębokość wyszukiwania w tym eksperymencie jest zmienna, co oznacza, że AI rozważa do trzech kroków w przód, biorąc pod uwagę możliwe reakcje obu graczy.



# 3. Eksperymenty z AI

Eksperyment obejmował 10 symulowanych gier, w których AI grało przeciwko sobie, zamieniając się kolejnością rozpoczynania. Wyniki były następujące:

| Experyment | Zwycięca (gracz1/gracz2) | Głębokość sieci | Gra deterministyczna | Ilość rozgrywerk |
|------------|--------------------------|-----------------|----------------------|------------------|
| 1          | 3/7                      | 3               | Nie                  | 10               |  
| 2          | 11/9                     | 3               | Nie                  | 20               |
| 3          | 23/17                    | 3               | Nie                  | 40               |
| 4          | 4/6                      | 6               | Nie                  | 10               |
| 5          | 11/9                     | 6               | Nie                  | 20               |
| 6          | 24/16                    | 6               | Nie                  | 40               |
| 7          | 2/8                      | 10              | Nie                  | 10               |
| 8          | 0/10                     | 3               | Tak                  | 10               |
| 9          | 0/20                     | 3               | Tak                  | 20               |
| 10         | 10/0                     | 6               | Tak                  | 10               |
| 11         | 10/0                     | 1               | Tak                  | 10               | 

## Interpretacja wyników
Wyniki eksperymentów pokazują, że głębokość analizy (liczba poziomów w drzewie decyzyjnym) wpływa na liczbę zwycięstw danego agenta. Wyższa głębokość analizy (np. 6 lub 10) zwiększa szanse na zwycięstwo, ponieważ AI może rozważyć więcej możliwych ruchów i tym samym lepiej przewidywać reakcje przeciwnika.

Warto jednak zauważyć, że głębokość analizy nie ma decydującego wpływu na wynik w grach opartej na deterministycznych strategiach, jak w przypadku eksperymentów 8, 9, i 10, gdzie gra była deterministyczna (wszystkie ruchy były idealne i przewidywalne).

# 4. Napotkane Problemy i Ich Rozwiązania

Podczas eksperymentów napotkano kilka problemów:

1. **Błąd 'list index out of range'**: Wynikał z błędnej obsługi pustej listy ruchów. Został rozwiązany poprzez dodatkowe sprawdzenie możliwych ruchów.

2. **Losowe błędy ruchów AI**: Wprowadzono mechanizm zmniejszający liczbę usuniętych elementów o 1 z 10% prawdopodobieństwem, co wprowadza losowość w rozgrywce.

3. **Brak przewagi dla AI rozpoczynającego grę**: Analiza wyników wykazała, że zmiana rozpoczynającego nie wpływa znacząco na wyniki.

# 5. Wnioski i Możliwości Rozwoju
Eksperymenty wykazały, że zastosowanie algorytmu Negamax w grze Nim pozwala na tworzenie bardzo silnych agentów, którzy są w stanie analizować wiele możliwych ruchów i dokonywać optymalnych decyzji. Wyniki eksperymentów wskazują również, że zwiększenie głębokości analizy pozytywnie wpływa na wydajność AI, choć sama strategia gry jest wciąż deterministyczna.

Jednak w przyszłości możliwe jest rozważenie wprowadzenia bardziej zaawansowanych algorytmów, takich jak Alpha-Beta pruning, które mogą poprawić efektywność algorytmu Negamax przez eliminowanie niepotrzebnych obliczeń.

Dodatkowo, można wprowadzić więcej elementów losowości w grze, np. poprzez dodanie elementów zmieniających zasady w trakcie rozgrywki, co uczyni grę bardziej interesującą i bardziej zbliżoną do rzeczywistych warunków rywalizacji.
 ## Podsumowanie
Podsumowanie
Eksperymenty z grą Nim i AI w kontekście algorytmu Negamax pozwoliły na stworzenie silnych agentów sztucznej inteligencji, zdolnych do rywalizacji na bardzo wysokim poziomie. Mimo że wyniki wskazują na brak znaczącej przewagi dla gracza rozpoczynającego grę, wyniki pokazują, że głębokość analizy i wprowadzenie elementów losowości mogą znacząco wpływać na strategię i przebieg gry.