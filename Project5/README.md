
# **GRA MOUNTAIN CAR CONTINUOUS**

## **Wstęp**

MountainCarContinuous to gra opierająca się na kontrolowaniu pojazdu, który ma na celu dotarcie na szczyt wzniesienia, wykorzystując swoją prędkość do wspinania się na górę. Gra odbywa się w przestrzeni jednowymiarowej, gdzie agent musi sterować siłą przyspieszenia, aby zdobyć wystarczający pęd i wspiąć się na górę.

### **Przestrzeń rozgrywki**

- **Początkowa pozycja agenta**: Pojazd znajduje się na dole wzniesienia, zazwyczaj w okolicy `x ≈ -0.5`, z małą początkową prędkością.
- **Docelowa pozycja agenta**: Celem jest dotarcie do pozycji `x >= 0.45`, która symbolizuje szczyt wzniesienia.
- **Obszar gry**: Gra odbywa się w przestrzeni 1D, a agent wykonuje ciągłe akcje, sterując siłą przyspieszenia.

### **Sterowanie i akcja**

- **Akcja**: Siła przyspieszenia mieści się w zakresie od `-1.0` (maksymalne przyspieszenie w lewo) do `+1.0` (maksymalne przyspieszenie w prawo).

### **Nagrody**

- **Za każdy krok**: kara w postaci `-a²`, gdzie `a` to wartość przyspieszenia. Oznacza to, że agent jest karany za użycie dużej siły, co motywuje go do ekonomicznego poruszania się.
- **Osiągnięcie celu**: nagroda +100, przyznawana natychmiast po osiągnięciu pozycji `x >= 0.45`.

### **Koniec gry**

Gra kończy się, gdy:

- Agent osiągnie cel (`x >= 0.45`), lub
- Zostanie osiągnięty maksymalny czas trwania epizodu (999 kroków).

---

### **Algorytm PPO**

Proximal Policy Optimization (PPO) to nowoczesny algorytm uczenia ze wzmocnieniem,
który poprawia stabilność i efektywność uczenia przez ograniczenie zmian polityki w pojedynczej aktualizacji.
PPO jest popularny ze względu na dobre wyniki na środowiskach ciągłych, takich jak Mountain Car Continuous, 
dzięki bezpośredniej optymalizacji polityki w sposób efektywny i stabilny.


### **Parametry uczenia + eksperymenty**

### **Wnioski*

