import copy

from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO
        result = []
        for impianto in self._impianti:
            consumi_totali = impianto.get_consumi()
            somma = 0
            count = 0
            for consumo in consumi_totali:
                if consumo.data.month == mese:
                    somma += consumo.kwh
                    count += 1
            consumo_medio_giornaliero = somma / count
            result.append((impianto.nome, consumo_medio_giornaliero))
        return result

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = float("inf")
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO

        if len(sequenza_parziale) == 7:
            if costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                #self.__sequenza_ottima = copy.deepcopy(sequenza_parziale)
                self.__sequenza_ottima = sequenza_parziale[:]
            return

        for impianto in self._impianti:
            costo_giornaliero = int(consumi_settimana[impianto.id][giorno-1])
            if impianto.id != ultimo_impianto and ultimo_impianto is not None:
                costo_giornaliero = int(consumi_settimana[impianto.id][giorno - 1]) + 5

            sequenza_parziale.append(impianto.id)
            self.__ricorsione(sequenza_parziale, giorno+1, impianto.id, costo_corrente + costo_giornaliero, consumi_settimana)
            sequenza_parziale.pop()


    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO
        dizionario = {}
        for impianto in self._impianti:
            l = []
            consumi_totali = impianto.get_consumi()
            for consumo in consumi_totali:
                if consumo.data.month == mese and consumo.data.day <= 7:
                    l.append(consumo.kwh)
            dizionario[impianto.id] = l
        return dizionario

