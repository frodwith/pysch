(define (not x)
  (if x #f #t))
  
(define (null? x)
  (eq? x nil))

(define quasiquote
  (syntax
    (lambda (args env)
      (define (recur x)
        (if (pair? x)
          (if (eq? (car x) 'unquote)
            (eval (cadr x) env)
            (cons (recur (car x)) (recur (cdr x))))
          x))
      (recur (car args)))))
