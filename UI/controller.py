import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self._view.lst_result.controls.clear()
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese dal menù a tendina!")
            return
        mese=self._mese
        ris=self._model.getUmiditaMedia(mese)
        self._view.lst_result.controls.append(
            ft.Text("L'umidità media nel mese selezionato è:", color="blue")
        )

        for r in ris:
            self._view.lst_result.controls.append(
                ft.Text(f"{r[0]} : {r[1]}")
            )
        self._view.update_page()



    def handle_sequenza(self, e):
        self._view.lst_result.controls.clear()
        if self._mese == 0:
            self._view.create_alert("Selezionare un mese dal menù a tendina!")
            return
        mese=self._mese
        ris= self._model.getInfoUmiditaMese(mese)
        self._view.lst_result.controls.append(
            ft.Text(f"La sequenza ottima ha costo {ris[0]} ed e:")
        )
        for r in ris[1]:
            self._view.lst_result.controls.append(
                ft.Text(r)
            )
        self._view.update_page()




    def read_mese(self, e):
        self._mese = int(e.control.value)

