from copy import deepcopy

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self._sequenza = None
        self._costo_migliore = None


    def getUmiditaMedia(self, mese):
        result = MeteoDao.get_mese_situazioni(mese)
        cont1=0
        cont2=0
        cont3=0
        sommaT=0
        sommaG=0
        sommaM=0
        for r in result:
            if r.localita=="Torino":
                cont1=cont1+1
                sommaT+=r.umidita
            elif r.localita=="Genova":
                cont2=cont2+1
                sommaG+=r.umidita
            else:
                cont3=cont3+1
                sommaM+=r.umidita
        mediaT=sommaT/cont1
        mediaG=sommaG/cont2
        mediaM=sommaM/cont3
        lista=[("Torino",mediaT),
               ("Genova",mediaG),
               ("Milano",mediaM)]
        lista.sort(key=lambda x: x[1], reverse=True)
        return lista

    def getInfoUmiditaMese(self, mese):
        tutti_dati= MeteoDao.get_mese_situazioni(mese)
        lista_info=tutti_dati[:45]
        self._costo_migliore=float("inf")
        self._sequenza=[]
        self.ricorsione([],lista_info, 0)
        return self._costo_migliore,self._sequenza


    def ricorsione(self, parziale, lista_info, costo_parziale):
        if (len(parziale)==15):
            if (costo_parziale<self._costo_migliore):
                self._costo_migliore=costo_parziale
                self._sequenza=list(parziale)
        else:
            indice= len(parziale)*3
            info_data_corrente= lista_info[indice:indice+3]
            for c in info_data_corrente:
                costo_spostamento=0
                if self.vincolo_max_giorni(c.localita,parziale):
                    if len(parziale)>0 and parziale[-1].localita!=c.localita:
                        costo_spostamento=100
                    if self.vincolo_min_giorni(c.localita, parziale) :
                        costo_nuovo=costo_parziale+costo_spostamento+c.umidita
                        parziale.append(c)
                        self.ricorsione(parziale, lista_info, costo_nuovo)
                        parziale.pop()


    def vincolo_max_giorni(self, localita_corrente, parziale):
        cont=0
        for i in parziale:
            if localita_corrente==i.localita:
                cont=cont+1
        if cont>=6:
            return False
        return True


    def vincolo_min_giorni(self, localita_corrente, parziale):
        if len(parziale)==0:
            return True
        if localita_corrente!=parziale[-1].localita:
            if len(parziale)<3:
                return False
            ultime_tre_giorni = parziale[-3:]
            cont2 = 0
            for i in ultime_tre_giorni:
                if i.localita==parziale[-1].localita:
                    cont2=cont2+1
            if cont2!=3:
                return False
        return True