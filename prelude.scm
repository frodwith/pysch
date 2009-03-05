(define (not x)
  (if x #f #t))
  
(define (null? x)
  (eq? x nil))

(define list (lambda args args))

(define (fold-1 fn seed lst)
  (if (null? lst) seed
    (fold-1 fn (fn (car lst) seed) (cdr lst))))

(define (foldr-1 fn seed lst)
  (if (null? lst)
    seed
    (fn (car lst) (foldr-1 fn seed (cdr lst)))))

(define (map-1 fn lst)
  (foldr-1 (lambda (item seed) 
             (cons (fn item) seed)) 
           nil lst))

(define append
  (lambda args
    (foldr-1 (lambda (lst seed)
               (foldr-1 cons seed lst))
             nil args)))
              
(define quote
  (syntax
    (lambda (args env)
      (car args))))

(define quasiquote
  (syntax
    (lambda (args env)
      (define (recur x)
        (if (pair? x)
          (if (eq? (car x) 'unquote)
            (eval (cadr x) env)
            (cons (recur (car x))
                  (recur (cdr x))))
          x))
      (recur (car args)))))
