% --------------------------
% fakty o osobach:
% person(imienazwisko, plec, rokurodzenia).
%   - imienazwisko : atom (np. peter_griffin, uzywamy malych liter i podkreslen)
%   - plec         : m (mezczyzna) lub f (kobieta)
%   - rokurodzenia : liczba calkowita
% --------------------------

person(jacob_griffin,       m, 1915).
person(margaret_griffin,    f, 1917).

person(francis_griffin,     m, 1940).
person(thelma_griffin,      f, 1942).

person(peter_griffin,       m, 1970).

person(william_pewterschmidt, m, 1910).
person(elizabeth_pewterschmidt, f, 1912).

person(carter_pewterschmidt, m, 1945).
person(barbara_pewterschmidt, f, 1947).

person(lois_pewterschmidt,  f, 1973).
person(carol_pewterschmidt, f, 1970).
person(patrick_pewterschmidt, m, 1975).

person(meg_griffin,         f, 2000).
person(chris_griffin,       m, 2002).
person(stewie_griffin,      m, 2005).

person(kevin_brown,         m, 1970).
person(daisy_brown,         f, 1996).
person(lily_brown,          f, 1999).

person(cynthia_white,       f, 1978).
person(ethan_pewterschmidt,  m, 2005).

% --------------------------
% fakty o relacjach rodzic -> dziecko:
% parent(rodzic, dziecko).
% --------------------------

% generacja 0 -> generacja 1 (pradziadkowie -> dziadkowie)
parent(jacob_griffin,      francis_griffin).
parent(margaret_griffin,   francis_griffin).

parent(william_pewterschmidt, elizabeth_pewterschmidt).
parent(elizabeth_pewterschmidt, carter_pewterschmidt).

% uwagaaaaa - powyzszy fakt to uproszczony zapis dla przykladu (elizabeth_pewterschmidt jest zarowno i matka, i zona williama),
%        by uzyskac pelne pokolenie - mozna zalozyc, ze william i elizabeth mieli wspolne dzieci, lecz dla prostoty
%        zostawiamy tylko linie prowadzaca do cartera. przepraszam i pozdrawiam z nocnej sesji!

% generacja 1 -> generacja 2 (dziadkowie -> rodzice)
parent(francis_griffin,     peter_griffin).
parent(thelma_griffin,      peter_griffin).

parent(william_pewterschmidt, carter_pewterschmidt).
parent(elizabeth_pewterschmidt, carter_pewterschmidt).

parent(carter_pewterschmidt, lois_pewterschmidt).
parent(barbara_pewterschmidt, lois_pewterschmidt).

parent(carter_pewterschmidt, carol_pewterschmidt).
parent(barbara_pewterschmidt, carol_pewterschmidt).

parent(carter_pewterschmidt, patrick_pewterschmidt).
parent(barbara_pewterschmidt, patrick_pewterschmidt).

% generacja 2 -> generacja 3 (rodzice -> dzieci)
parent(peter_griffin,        meg_griffin).
parent(lois_pewterschmidt,   meg_griffin).

parent(peter_griffin,        chris_griffin).
parent(lois_pewterschmidt,   chris_griffin).

parent(peter_griffin,        stewie_griffin).
parent(lois_pewterschmidt,   stewie_griffin).

parent(carol_pewterschmidt,   daisy_brown).
parent(kevin_brown,          daisy_brown).

parent(carol_pewterschmidt,   lily_brown).
parent(kevin_brown,          lily_brown).

parent(patrick_pewterschmidt, ethan_pewterschmidt).
parent(cynthia_white,        ethan_pewterschmidt).

% --------------------------
% reguly relacji posrednich:
% --------------------------

% 1) father(ojciec, dziecko) - prawdziwe, gdy ojciec jest ojcem dziecka.
father(O, D) :-
    parent(O, D),
    person(O, m, _).

% 2) mother(matka, dziecko) - prawdziwe, gdy matka jest matka dziecka.
mother(M, D) :-
    parent(M, D),
    person(M, f, _).

% 3) sibling(x, y) - prawdziwe, gdy x i y maja wspolnego rodzica i x \= y.
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

% 4) grandparent(dziadekbabcia, wnukwnuczka) - prawdziwe, gdy dziadekbabcia jest 
%    rodzicem ktoregos z rodzicow wnuka/wnuczki.
grandparent(GP, C) :-
    parent(GP, P),
    parent(P, C).

% 5) ancestor(przodek, potomek) - prawdziwe, gdy przodek jest rodzicem lub 
%    rekurencyjnie przodkiem potomka.
ancestor(A, D) :-
    parent(A, D).
ancestor(A, D) :-
    parent(A, X),
    ancestor(X, D).

% 6) cousin(kuzyn1, kuzyn2) - prawdziwe, gdy ich rodzice sa rodzenstwem i kuzynowie nie sa ta sama osoba.
cousin(A, B) :-
    parent(P1, A),
    parent(P2, B),
    sibling(P1, P2),
    A \= B.

% 7) aunt_uncle(ciociawujek, siostrzenicabratanek) - prawdziwe, gdy osoba jest rodzenstwem jednego z rodzicow.
aunt_uncle(AU, N) :-
    parent(P, N),
    sibling(AU, P).

% 8) descendant(potomek, przodek) - odwrocenie relacji ancestor.
descendant(D, A) :-
    ancestor(A, D).

% --------------------------
% predykaty wyswietlania wynikow
% --------------------------

% wypisz_rodzenstwo(osoba) - wyswietla wszystkich (wszystkie) rodzenstwo danej osoby.
wypisz_rodzenstwo(O) :-
    findall(
        S,
        sibling(O, S),
        ListaS
    ),
    write('Rodzenstwo '), write(O), write(': '), write(ListaS), nl.

% wypisz_dziadkow(osoba) - wyswietla liste dziadkow danej osoby.
wypisz_dziadkow(O) :-
    findall(
        GP,
        grandparent(GP, O),
        ListaG
    ),
    write('Dziadkowie '), write(O), write(': '), write(ListaG), nl.

% wypisz_przodkow(osoba) - wyswietla wszystkich przodkow (rekurencyjnie), 
%                          usuwa duplikaty i sortuje.
wypisz_przodkow(O) :-
    findall(
        A,
        ancestor(A, O),
        ListaUnik
    ),
    sort(ListaUnik, ListaSorted),
    write('Przodkowie '), write(O), write(': '), write(ListaSorted), nl.

% wypisz_kuzynow(osoba) - wyswietla wszystkich kuzynów danej osoby.
wypisz_kuzynow(O) :-
    findall(
        C,
        cousin(O, C),
        ListaUnik
    ),
    sort(ListaUnik, ListaSorted),
    write('Kuzyni '), write(O), write(': '), write(ListaSorted), nl.

% wypisz_wujkow_ciocie(osoba) - wyswietla wszystkie ciocie i wujkow.
wypisz_wujkow_ciocie(O) :-
    findall(
        AU,
        aunt_uncle(AU, O),
        ListaUnik
    ),
    sort(ListaUnik, ListaSorted),
    write('Ciocie i wujkowie '), write(O), write(': '), write(ListaSorted), nl. 