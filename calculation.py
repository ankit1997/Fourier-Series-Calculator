from sympy import symbols,integrate,sin,cos,pi
from sympy.parsing.sympy_parser import parse_expr

class Calculation:
    def __init__(self,obj):
        self.main = obj
        
    def doCalculations(self,funcArr,lowArr,uppArr):
        x = symbols('x')
        n = symbols('n',positive = True,integer = True)
        a0 = 0.0
        an = 0.0
        bn = 0.0
        num = len(funcArr)
        for i in range(0,num):
            func = parse_expr(funcArr[i].get())
            low = parse_expr(lowArr[i].get())
            upp = parse_expr(uppArr[i].get())
            xRange = upp - low
            a0 += (1/xRange)*(integrate(func,(x,low,upp)))
            an += (2/xRange)*(integrate(func*cos(2*n*pi*x/xRange),(x,low,upp)))
            bn += (2/xRange)*(integrate(func*sin(2*n*pi*x/xRange),(x,low,upp)))
        return a0,an,bn



