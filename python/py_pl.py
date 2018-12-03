from pyswip import Prolog

prolog = Prolog()

prolog.consult("../prolog/chicken-and-rabbits.prolog")

a = list(prolog.query("foot(C,R,100),head(C,R,40)"))

print a
