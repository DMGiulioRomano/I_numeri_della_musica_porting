import math
from fractions import Fraction
from decimal import Decimal, getcontext

# Imposta la precisione a 10 cifre decimali
getcontext().prec = 10

cent = Decimal(1200/math.log10(2))
rapportoTest = Fraction(3,2)

def rapporto2cent(rapporto):
    return Decimal(math.log10(float(rapporto)) * cent)

def cents2decimale(cents):
    return Decimal(cents/cent)

def decimale2rapporto(decimale):
    return Fraction(decimale).limit_denominator()



class SistemaIntonazioneTemperato:
    """ 
    *Sistema di intonazione _temperato_*
        E' possibile ottenere infinite divisioni 
        dell'ottava in parti ---equidistanti---.
        (stessa procedura utilizzata per il temperamento equabile
        in cui l'ottava viene divisa in 12 intevalli).
    """
    def __init__(self,frequenzaDiRiferimento,ottava,intervalli):
        self.frequenzaDiRiferimento = frequenzaDiRiferimento
        self.ottava = ottava
        self.intervalli = intervalli
        self.coefficiente()

    def coefficiente(self):
        self.coefficiente = Decimal(pow(self.ottava,1/self.intervalli))


class Divisionesemplice(SistemaIntonazioneTemperato):
    def __init__(self, frequenzaDiRiferimento, ottava, intervalli):
        super().__init__(frequenzaDiRiferimento, ottava, intervalli)

    def intervalloFreq(self,intervalloN):
        """ 
    * a divisione semplice*
        L'ottava, intesa come 2*f dove f è la frequenza di riferimento,
        viene divisa a n intervalli equidistanti.
        Ritorna un intervallo preciso.
        """
        return Decimal((self.coefficiente**intervalloN)*self.frequenzaDiRiferimento)

    def __str__(self) -> str:
        return f"{self.intervalloFreq()}"



class DivisioneMultipla(SistemaIntonazioneTemperato):
    def __init__(self, frequenzaDiRiferimento, ottava, intervalli, divisioni, sottodivisioni):
        super().__init__(frequenzaDiRiferimento, ottava, intervalli)
        self.divisioni=divisioni
        self.sottodivisioni=sottodivisioni
        self.coefficienti=[]
        try:
            self.controlla_somma_divisioni()
        except ValueError as e:
            print(f"Errore: {e}")
            raise e
        self.calcCoefficienti()

    def controlla_somma_divisioni(self):
        """ Controlla se la somma dei valori in divisioni è maggiore o minore del numero di intervalli. """
        somma = sum(self.divisioni)
        if somma != self.intervalli:
            raise ValueError(f"La somma delle divisioni ({somma}) non è uguale al numero di intervalli ({self.intervalli}).")

    def calcCoefficienti(self):
        for index, value in enumerate(self.divisioni):
            spazioDivisione = pow(self.ottava,1/self.intervalli)**value
            coefficiente = pow(spazioDivisione,1/self.sottodivisioni[index])
            self.coefficienti.append(coefficiente)

    def intervalloFreq(self,intervalloN):
        somma = 0
        potenzeCoeff = [0] * len(self.sottodivisioni)  # Crea una lista di zeri della stessa lunghezza di 'a'
        for i in range(2, len(self.sottodivisioni)):
            self.sottodivisioni[i] -= 1  

        for i, numero in enumerate(self.sottodivisioni):
            if somma + numero <= intervalloN:
                potenzeCoeff[i] = numero
                somma += numero
            else:
                potenzeCoeff[i] = intervalloN - somma
                somma = intervalloN  
                break
        resto = intervalloN - somma
        if resto > 0:
            potenzeCoeff[-1] += resto
        coeffEffettivi = [x**y for x, y in zip(self.coefficienti, potenzeCoeff)]
        p = 1
        for r in coeffEffettivi:
            p *= r
        return self.frequenzaDiRiferimento * p
    


    
#a=DivisioneMultipla(100,2,12,[4,4,4],[5,6,7])
#print(a.intervalloFreq(18))
#print(s)
#print(s.intervalloFreq(12))
