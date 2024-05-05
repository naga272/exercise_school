from log import *
import sys
import re


"""
Per i clien6 della banca occorre memorizzare nome, cognome, recapito telefonico ed 
elenco dei con9 bancari di cui sono intestatari. La banca non fornisce la possibilità di 
intestare un conto corrente a più clien9. Un cliente può effe6uare l’operazione di 
chiusura di conto bancario di cui è intestatario (solo se il conto ha un saldo a.vo), 
visualizzazione del saldo complessivo dei con9 di cui è intestatario.
"""
class Cliente():
    def __init__(self, nome, cognome, num_telefono):
        self.__nome = nome
        self.__cognome = cognome
        self.__num_telefono = num_telefono
        self.__conti = []

        Log().logMe(f"object created {type(self)}")

    def chiudi_conto(self, IBAN):
        for element in self.__conti:
            if element.get_iban() == IBAN:
                element.__del__()

    def intesta_conto(self, IBAN):
        self.__conti.append(Banca.apri_conto())

    def __del__(self):
        Log().logMe("object deleted from class Cliente")

    def __str__(self):
        return ""


"""
La banca di cui occorre memorizzare il nome e il codice, può aprire un nuovo conto 
bancario associandolo ad un cliente già esistente o ad un nuovo cliente, può inserire 
un nuovo cliente nella lista clien9. Nel caso in cui un cliente della banca abbia chiuso 
tu. i con9 corren9 a lui intesta9, la banca non lo elimina dalla lista clien9 ma lo 
segnala come ex-cliente. La banca ges9sce mensilmente le operazioni di calcolo di 
interessi dei vari con9 reimpostando i conteggi ed i saldi. In ogni momento la banca 
può richiedere il calcolo del saldo complessivo dei con9 bancari, anche per categoria 
(saldo con9 corren9, saldo con9 di deposito, saldo con9 di deposito vincolato).  
"""
class Banca():
    def __init__(self, nome, codice):
        self.__nome = nome
        self.__codice = codice
        self.__clienti = []

        Log().logMe(f"object created {type(self)}")

    def apri_conto(self, cliente):
        if cliente in self.__clienti:
            pass

    def __del__(self):
        Log().logMe("object deleted from class Banca")

    def __str__(self):
        return ""


class ExCliente():
    pass


class ContoBancario:
    counter = 0
    instances = []
    def __init__(self, IBAN:str, saldo:float):
        self.__saldo = saldo if type(saldo) == float else 0.0

        if re.fullmatch(r'\s*[A-Z]{2}\d{2}\w\d{10}\w{12}\s*', str(IBAN)):
            self.__IBAN = IBAN
        else: 
            """
                algoritmo per generare un IBAN univoco in caso quello inserito non risulti valido.
                Un IBAN e' composta da 27 caratteri alfanumerici, in questo caso ho messo che i primi
                15 char sono standard
            """
            self.__IBAN = f"IT1234567890123"
            self.__IBAN += ('0' * (27 - len(self.__IBAN) - len(str(ContoBancario.counter)))) + str(ContoBancario.counter)

        ContoBancario.counter += 1

        Log().logMe(f"created object {type(self)}")

    def deposito(self, quantita:float):
        if type(quantita) == float:
            self.__saldo += quantita

    def prelievo(self, quantita:float)      -> float:
        
        if self.__saldo >= quantita: 
            self.__saldo -= quantita
            return quantita 
        else:
            return 0.0 # non puo prelevare quantita richiesta

    @property
    def saldo(self)                         -> float:
        return self.__saldo

    def trasferimento(self, conto, quantita):
        # trasferimento di denaro su un altro conto.
        test_money = self.prelievo(quantita)

        if test_money != 0.0:
            conto.deposito(test_money)

    def get_iban(self):
        return self.__IBAN


    def __str__(self):
        return f"IBAN:{self.__IBAN}\nsaldo attuale: {self.__saldo}\n"

    def __del__(self):
        Log().logMe("object deleted from class ContoBancario")


class ContoCorrente(ContoBancario):
    commissione_mensile = 20.0
    def __init__(self, IBAN:str, saldo:float):
        super().__init__(IBAN, saldo)
        self.__transazioni = 0

    def deposito(self, quantita:float):
        if self.__transazioni > 3:
            self.__saldo -= 2

        if type(quantita) == float:
            self.__saldo += quantita

        self.__transazioni += 1

    def prelievo(self, quantita:float)      -> float:
        if self.__transazioni > 3:
            self.__saldo -= 2

        if self.__saldo >= quantita: 
            self.__saldo -= quantita
            return quantita 
        else:
            return 0.0 # non puo prelevare quantita richiesta

        self.__transazioni += 1
    
    def deduzione_commissione(self):
        # puo andare anche in negativo il conto, quindi in debito
        self.__saldo -= ContoCorrente.commissione_mensile 
        self.__transazioni = 0

    def __str__(self):
        return f"{super().__str__()}commissione mensile: {ContoCorrente.commissione_mensile}\n numero transazioni: {self.__transazioni}\n"

    def __del__(self):
        Log().logMe("object deleted from class ContoCorrente")


class ContoDeposito(ContoBancario):
    def __init__(self, IBAN:str, saldo:float, interesse_annuo:float, num_anni:int):
        super().__init__(IBAN, saldo)

        # "num_anni" indica da quanti anni e' aperto il conto
        self.__interesse_annuo = interesse_annuo 
        self.__anni = num_anni if type(num_anni) == int else 1

    def add_interessi(self):
        """
            calcolo tasso interesse mensile conto deposito:
            'se depositiamo su un conto deposito non vincolato 1.000€ per due anni,
            ad un interesse ipotetico dell'1,5%, dovremo effettuare questo calcolo: 
            (1000*1,5*730)/36500=30 euro.
            Dopo due anni quindi avremo guadagnato 30 euro.' 
            (ho preso da internet per capire come funziona)
        """
        self.__saldo += ((self.__saldo * self.__interesse_annuo * (self.__anni * 365)) / 36500)

    def __str__(self):
        return f"{super().__str__()}\ninteresse in questi {self.__anni}\nanni: {self.__interesse_annuo}%\n"

    def __del__(self):
        Log().logMe("object deleted from class ContoDeposito")


class ContoDepositoVincolante(ContoBancario):
    penale = 20.0

    def __init__(self, IBAN:str, saldo:float, n_mesi:int):
        super().__init__(IBAN, saldo)
        self.__n_mesi       = n_mesi
    
    def __str__(self):
        return f"{super().__str__()}\nnumero mesi:{self.__n_mesi}\n"

    def __del__(self):
        Log().logMe("object deleted from class ContoDepositoVincolante")
