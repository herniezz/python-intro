;; Czesc I - bubble sort z modyfikacja liczb nieparzystych

;; generowanie listy 100 losowych liczb
(defun generate-list ()
  (loop for i below 100 collect (random 1000)))

;; Funkcja zwiekszajaca liczby nieparzyste o 1
(defun adjust-odd-numbers (lista)
  (mapcar #'(lambda (x) 
              (if (oddp x) 
                  (1+ x) 
                  x)) 
          lista))

;; implementacja bubble sort (malejaco)
;; algorytm porownuje sasiadujace elementy i zamienia je miejscami,
;; jesli element po lewej jest mniejszy od elementu po prawej.
;; sprawia to ze najwieksze elementy sa na poczatku listy.
(defun bubble-sort (lista)
  (let ((n (length lista)))
    (do ((i 0 (1+ i)))
        ((= i n) lista)
      (do ((j 0 (1+ j)))
          ((= j (- n i 1)))
        (when (< (nth j lista) (nth (1+ j) lista))
          (rotatef (nth j lista) (nth (1+ j) lista)))))))

;; Czesc II - QuickSort
;; jako ze to "dziel i zwyciezaj", to skrypt:
;; 1. wybiera element 'pivot' z tablicy
;; 2. dzieli tablice na elementy mniejsze i wieksze od pivota
;; 3. rekurencyjnie sortuje podtablice
;; ta implementacja uzywa pierwszego elementu jako pivota dla uproszczenia
;; i sortuje w porzadku malejacym (od najwiekszej do najmniejszej)
(defun quicksort (lista)
  (if (<= (length lista) 1)
      lista
      (let* ((pivot (first lista))
             (rest (rest lista))
             (greater (remove-if-not #'(lambda (x) (>= x pivot)) rest))
             (lesser (remove-if-not #'(lambda (x) (< x pivot)) rest)))
        (append (quicksort greater)
                (list pivot)
                (quicksort lesser)))))

;; czesc III - sortowania przez wstawianie
;; 1. Dzieli liste na czesc posortowana i nieposortowana
;; 2. Bierze kolejne elementy z czesci nieposortowanej
;; 3. Wstawia je we wlasciwe miejsce w czesci posortowanej
;; Implementacja sortuje w porzadku malejacym (od najwiekszej do najmniejszej)
(defun insertion-sort (lista)
  (labels ((insert (sorted x)
             (if (null sorted)
                 (list x)
                 (if (<= x (first sorted))
                     (cons (first sorted) (insert (rest sorted) x))
                     (cons x sorted)))))
    (reduce #'insert lista :initial-value nil)))

;; funkcja testowa do weryfikacji poprawnosci sortowania
(defun test-sorting (lista)
  (format t "~%Test sortowania dla listy: ~a~%" lista)
  (format t "Po modyfikacji nieparzystych: ~a~%" (adjust-odd-numbers lista))
  (format t "Po sortowaniu bąbelkowym: ~a~%" 
          (bubble-sort (adjust-odd-numbers lista)))
  (format t "Po QuickSort: ~a~%" 
          (quicksort (adjust-odd-numbers lista)))
  (format t "Po sortowaniu przez wstawianie: ~a~%" 
          (insertion-sort (adjust-odd-numbers lista))))

;; glowna czesc programu
(let ((original-list (generate-list)))
  (format t "Lista oryginalna: ~a~%" original-list)
  
  ;; czesc I - bubble sort
  (let ((adjusted-list (adjust-odd-numbers original-list)))
    (format t "~%Czesc I - Po modyfikacji liczb nieparzystych: ~a~%" adjusted-list)
    (bubble-sort adjusted-list)
    (format t "Po sortowaniu bąbelkowym: ~a~%" adjusted-list))
  
  ;; czesc II - quickSort
  (format t "~%Czesc II - Wynik QuickSort: ~a~%" 
          (quicksort (adjust-odd-numbers original-list)))
  
  ;; Czesc III - sortowanie przez wstawianie
  (format t "~%Czesc III - Wynik sortowania przez wstawianie: ~a~%"
          (insertion-sort (adjust-odd-numbers original-list)))
  
  ;; test z lista
  (test-sorting '(5 2 7 4 3)))
