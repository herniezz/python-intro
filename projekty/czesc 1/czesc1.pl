% --------------------------
% Definicja faktów:
% film(Tytul, Gatunek, Ocena, RokProdukcji, Reżyser).
%   – Tytul         : atom (tytuł filmu)
%   – Gatunek       : atom (np. dramat, komedia, akcja, sci_fi, horror, animacja, kryminal, thriller, przygodowy, romans)
%   – Ocena         : liczba całkowita od 1 do 5
%   – RokProdukcji  : liczba całkowita (rok powstania)
%   – Reżyser       : atom (nazwisko reżysera, z podkreśleniami zamiast spacji)
% --------------------------

film('The Shawshank Redemption', dramat,     5, 1994, andy_darling).
film('The Godfather',           dramat,     5, 1972, francis_ford_coppola).
film('The Dark Knight',         akcja,      5, 2008, christopher_nolan).
film('Pulp Fiction',            kryminal,   5, 1994, quentin_tarantino).
film('Forrest Gump',            dramat,     5, 1994, robert_zemeckis).
film('Inception',               sci_fi,     4, 2010, christopher_nolan).
film('The Matrix',              sci_fi,     5, 1999, wachowscy).
film('The Lion King',           animacja,   4, 1994, rob_minkoff).
film('Spirited Away',           animacja,   5, 2001, hayao_miyazaki).
film('Back to the Future',      przygodowy, 5, 1985, robert_zemeckis).
film('Gladiator',               dramat,     4, 2000, ridley_scott).
film('The Avengers',            akcja,      4, 2012, joss_whedon).
film('Titanic',                 romans,     4, 1997, james_cameron).
film('Jurassic Park',           przygodowy, 4, 1993, steven_spielberg).
film('The Silence of the Lambs', thriller,  5, 1991, jonathan_demmy).
film('Get Out',                 horror,     4, 2017, jordan_peele).
film('Hereditary',              horror,     4, 2018, ari_aster).
film('Toy Story',               animacja,   5, 1995, john_lasseter).
film('The Grand Budapest Hotel',komedia,    4, 2014, wes_anderson).
film('La La Land',              romans,     4, 2016, damien_chazelle).
film('Interstellar',            sci_fi,     5, 2014, christopher_nolan).
film('Mad Max: Fury Road',      akcja,      5, 2015, george_miller).
film('Parasite',                dramat,     5, 2019, bong_joon_ho).
film('The Social Network',      dramat,     4, 2010, david_fincher).
film('The Wolf of Wall Street', dramat,     4, 2013, martin_scorsese).


% --------------------------
% reguły wyszukiwania:
% --------------------------

% 1) filmy_gatunek(Gatunek, Lista) – wszystkie tytuły filmu danego gatunku.
filmy_gatunek(Gatunek, ListaTytulow) :-
    findall(
      Tytul,
      film(Tytul, Gatunek, _, _, _),
      ListaTytulow
    ).

% 2) filmy_ocena(MinOcena, Lista) – wszystkie tytuły filmów z oceną >= MinOcena.
filmy_ocena(MinOcena, ListaTytulow) :-
    findall(
      Tytul,
      (
        film(Tytul, _, Ocena, _, _),
        Ocena >= MinOcena
      ),
      ListaTytulow
    ).

% 3) filmy_rok(Rok, Lista) – wszystkie tytuły filmów z danego roku produkcji.
filmy_rok(Rok, ListaTytulow) :-
    findall(
      Tytul,
      film(Tytul, _, _, Rok, _),
      ListaTytulow
    ).

% 4) filmy_rezyser(Rezyser, Lista) – wszystkie tytuły filmów danego reżysera.
filmy_rezyser(Rezyser, ListaTytulow) :-
    findall(
      Tytul,
      film(Tytul, _, _, _, Rezyser),
      ListaTytulow
    ).

% 5) filmy_gatunek_ocena(Gatunek, MinOcena, Lista) – wszystkie tytuły filmów,
%    które są w gatunku Gatunek i mają ocenę >= MinOcena.
filmy_gatunek_ocena(Gatunek, MinOcena, ListaTytulow) :-
    findall(
      Tytul,
      (
        film(Tytul, Gatunek, Ocena, _, _),
        Ocena >= MinOcena
      ),
      ListaTytulow
    ).


% wyswietl_filmy_gatunek(Gatunek) – wyświetla filmy dla zadanego gatunku.
wyswietl_filmy_gatunek(Gatunek) :-
    filmy_gatunek(Gatunek, Lista),
    write('Filmy w gatunku '), write(Gatunek), write(': '),
    write(Lista), nl.

% wyswietl_filmy_ocena(MinOcena) – wyświetla filmy z oceną >= MinOcena.
wyswietl_filmy_ocena(MinOcena) :-
    filmy_ocena(MinOcena, Lista),
    write('Filmy z oceną >= '), write(MinOcena), write(': '),
    write(Lista), nl.

% wyswietl_filmy_rok(Rok) – wyświetla filmy z określonego roku.
wyswietl_filmy_rok(Rok) :-
    filmy_rok(Rok, Lista),
    write('Filmy z roku '), write(Rok), write(': '),
    write(Lista), nl.

% wyswietl_filmy_rezyser(Rezyser) – wyświetla filmy danego reżysera.
wyswietl_filmy_rezyser(Rezyser) :-
    filmy_rezyser(Rezyser, Lista),
    write('Filmy reżysera '), write(Rezyser), write(': '),
    write(Lista), nl.

% wyswietl_filmy_gatunek_ocena(Gatunek, MinOcena) – filmy w gatunku
%   o ocenie >= MinOcena.
wyswietl_filmy_gatunek_ocena(Gatunek, MinOcena) :-
    filmy_gatunek_ocena(Gatunek, MinOcena, Lista),
    write('Filmy w gatunku '), write(Gatunek),
    write(' z oceną >= '), write(MinOcena), write(': '),
    write(Lista), nl.


% --------------------------
% 5 zapytań:
% --------------------------

% 1) Wszystkie komedie:
% ?- wyswietl_filmy_gatunek(komedia).

% 2) Wszystkie filmy z oceną co najmniej 4:
% ?- wyswietl_filmy_ocena(4).

% 3) Wszystkie filmy z roku 1994:
% ?- wyswietl_filmy_rok(1994).

% 4) Wszystkie filmy reżysera 'christopher_nolan':
% ?- wyswietl_filmy_rezyser(christopher_nolan).

% 5) Wszystkie dramaty z oceną co najmniej 5:
% ?- wyswietl_filmy_gatunek_ocena(dramat, 5).
