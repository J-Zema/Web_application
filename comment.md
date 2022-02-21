# Komentarz

## HTML
1. Mogli Państwo użyć tagów strukturalnych, tzn. niektóre `div`y zamienić np. na `nav` albo `main`.
2. Osobiście wolę jak linki które przenoszą na inną stronę otwierają się w osobnej karcie, ale to kwestia gustu. Żeby to osiągnąć wystarczy dodać atrubut `target` z wartością `_blank` do tagu `a` (więcej w [dokumentacji](https://www.w3schools.com/tags/att_a_target.asp)).
3. Adresy email też możemy ubrać w tag `a`, co spowoduje, że przy kliknięciu powinienen otworzyć się klient pocztowy, ot taka ciekawostka. Więcej w [dokumentacji](https://www.w3schools.com/tags/att_a_href.asp).

## CSS (Styl)
1. Część stylu w pliku css (na plus), a część jako atrybut tagów (na duży minus). Trzymająć się tylko pliku oddzielamy strukturę logiczną strony od tego, jak wygląda.

## Back end
1. W Pythonie możemy iterować po indeksach, więc róbmy to. O wiele lepiej wtedy się kod czyta i debugguje. Czyli
   ```
   for i in range(len(some_list)):
       do_something(some_list[i])
   ```
   zamieńmy na
   ```
   for element in some_list:
       do_something(element)
   ```
   Jeżeli potrzebujemy pracować na paru listach (iteratorach), to połączmy je za pomocą `zip`. Czyli zamiast
   ```
   for i in range(len(first_list)):
       do_something_else(first_list[i], second_list[i])
   ```
   użyjmy
   ```
   for element1, element2 in zip(first_list, second_list):
       do_something_else(element1, element2)
   ```
   Automatycznie mamy rozwiązany problem, jeśli listy są różnej długości.
2. Używanie `except` bez konkretnego wyjątku jest niebezpieczne, jeżeli wiemy, jak wyjątek może wystąpić, to wrzućmy go do kodu. Czyli
   ```
   try:
       i[j] = float(i[j])
   except:
       pass
   ```
   warto zamienić na
   ```
   try:
       i[j] = float(i[j])
   except ValueError:
       pass
   ```
   Skąd dowiedzieć się jakiego wyjątku użyć? Przeczytać dokumentację, albo po prostu sprawdzić w interpreterze, czyli wpisać np. `float("abc")` i zobaczyć komunikat.
3. Pakiet `ast` to trochę przesada. Łańcuchy znaków możemy bez problemu zamienić w listę  używając [`str.split()`](https://docs.python.org/3.8/library/stdtypes.html#str.split).
4. Nazwa zmiennej `i` dla wiersza tekstu jest wyjątkowo enigmatyczna, lepsze byłoby po prostu `row`. Tak samo z `j`.
5. Niekonsekwecja w pisaniu pojedynczych i podwójnych cudzysłowów. Oba w Pythonie są poprawne, ale w ramach projektu pliku trzymajmy się jednych (od razu wiadać co było pisane przez Państwa, a co przeklejone z zajęć 😏)
6. Na duży plus za *docstring* i kometarze! Jeśli chcą Państwo dalej ułatwiać pracę sobie i innym to polecam poczytać [Documenting Python Code: A Complete Guide](https://realpython.com/documenting-python-code/). Jeśli będziemy kiedyś razem pracować, to polubimy się na repozytorium.
7. Bardzo mi się podoba, że nie możemy wybrać tych samych zmiennych ciągłych - klasa.

# Podsumowanie

Bardzo dobry projekt, podoba mi się. Styl jest czytelny. Statystyki wyświetlane są prawidłowo nie tylko dla bazowych danych, ale nawet dla odrobinę innych. Cieszy obsługa błędów i odsyłacze do stron.

**Punktacja** 27 / 30
