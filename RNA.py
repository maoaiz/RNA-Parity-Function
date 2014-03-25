import math

class UnidadSigmoidal():
    w1 = 0
    w2 = 0
    w3 = 0
    name = "---"
    def __init__(self, w1, w2, w3, name=None):
        if name:
            self.name = name
        self.w1 = float(w1)
        self.w2 = float(w2)
        self.w3 = float(w3)
    def __unicode__(self):
        return u"Uni. Sig: %s. W=(w1:%f, w2:%f, w3:%f)" % (self.name, self.w1, self.w2, self.w3)

    def sigmoide(self, s):
        return 1 / (1 + math.exp(-s))

    def calc_f(self, x1, x2, x3):
        return self.sigmoide(x1*float(self.w1) + x2*float(self.w2) + x3*float(self.w3))

    def calc_deltak(self, d, f):
        return (d - f) * f * (1 - f)

    def calc_deltaj(self, deltak, peso, fj):
        return fj * (1 - fj) * deltak * peso

    def calc_pesok(self, valor, deltak, X):
        return valor + deltak * X

class RNA():
    X3 = 1
    d = 0
    neuronas = [
        UnidadSigmoidal(2, -2, 0, name="n1"),
        UnidadSigmoidal(1, 3, -1, name="n2"),
        UnidadSigmoidal(3, -2, -1, name="n3")
    ]

    def entrenar(self):
        print "\nNuevo entrenamiento\n"
        x1 = float(raw_input("Ingrese X1: "))
        x2 = float(raw_input("Ingrese X2: "))
        self.d  = float(raw_input("Ingrese el valor deseado (d): "))
        x3 = float(self.X3)
        print "X3: %s" % x3
        print "\nCalculando...\n"
        n1 = self.neuronas[0]
        n2 = self.neuronas[1]
        n3 = self.neuronas[2]

        f1 = n1.calc_f(x1, x2, x3)
        f2 = n2.calc_f(x1, x2, x3)
        f3 = n3.calc_f(f1, f2, x3)

        print "Salida de cada unidad sigmoidal:"
        print "f1: %f" % f1
        print "\t\tf: %f" % f3
        print "f2: %f" % f2
        # print "f vs d: %.3f => %.3f" % (f3, self.d)
        print "\najustando pesos...\n"

        dn3 = n3.calc_deltak(self.d, f3)
        dn1 = n1.calc_deltaj(dn3, n3.w1, f1)
        dn2 = n2.calc_deltaj(dn3, n3.w2, f2)
        print "delta us1: %f" % dn1
        print "\t\tdelta us3: %f" % dn3
        print "delta us2: %f" % dn2

        n3.w1 = n3.calc_pesok(n3.w1, dn3, f1)
        n3.w2 = n3.calc_pesok(n3.w2, dn3, f2)
        n3.w3 = n3.calc_pesok(n3.w3, dn3, x3)

        n2.w1 = n2.calc_pesok(n2.w1, dn2, x1)
        n2.w2 = n2.calc_pesok(n2.w2, dn2, x2)
        n2.w3 = n2.calc_pesok(n2.w3, dn2, x3)

        n1.w1 = n1.calc_pesok(n1.w1, dn1, x1)
        n1.w2 = n1.calc_pesok(n1.w2, dn1, x2)
        n1.w3 = n1.calc_pesok(n1.w3, dn1, x3)
        
        print "\nPesos ajustados."
        print n1.__unicode__()
        print "\t\t\t\t" + n3.__unicode__()
        print n2.__unicode__()
        return True
        


    def setWeights(self):
        print "\nIngrese los pesos de cada unidad sigmoidal\n"
        for n in self.neuronas:
            print "Unidad sigmoidal:", n.name
            n.w1 = float(raw_input(n.name + " w1: "))
            n.w2 = float(raw_input(n.name + " w2: "))
            if n.name == "n1":
                n.w3 = 0
            elif n.name == "n2":
                n.w3 = -1
            elif n.name == "n3":
                n.w3 = -1
            # n.w3 = float(raw_input(n.name + " w3: "))
        print ""

    def __init__(self):
        print "===================Red Neuronal. Problema de la funcion de paridad==================="

            
red = RNA()
red.setWeights()
entrenar = True
while entrenar:
    entrenar = red.entrenar() and bool(int(raw_input("Desea realizar un nuevo entrenamiento con los nuevos pesos? (1/0): ")))
print "\nRed entrenada.\n\nbye bye...\n\n"

