:- use_module(library(clpq)).

head(C,R,H) :- {H = C + R}.
foot(C,R,F)  :- {F = C*2 + R*4}.
