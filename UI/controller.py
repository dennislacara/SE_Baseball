import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.anno = None

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        self._model.creaGrafo(self.anno)
        self._view.txt_risultato.controls.clear()
        self._view.txt_risultato.controls.append(ft.Text(f'{self._model.G}'))
        #attivo i pulsanti successivi
        self._view.dd_squadra.disabled = False
        self._view.pulsante_dettagli.disabled = False
        self._view.pulsante_percorso.disabled = False
        self._view.update()

        # TODO

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""

        if not self._view.dd_squadra.value:
            self._view.show_alert('Inserire la squadra')
            return
        id_team = int(self._view.dd_squadra.value)
        lista = []
        map = self._model.map_squadre
        for arco in self._model.G.edges(id_team, data=True):

            lista.append((map[arco[0]], map[arco[1]], arco[2]['peso']))
        listaOrdinata = sorted(lista, key=lambda x: x[2], reverse=True)
        self._view.txt_risultato.controls.clear()
        for tupla in listaOrdinata:
            self._view.txt_risultato.controls.append(ft.Text(f'{tupla[1]}  -  {tupla[2]}'))
        self._view.update()

        # TODO

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        if not self._view.dd_squadra.value:
            self._view.show_alert('Inserire la squadra')
            return
        percorso, valore = self._model.calcola_percorso(int(self._view.dd_squadra.value))
        print(valore)
        for id,v in percorso:
            print(f'{self._model.map_squadre[id]}: {v}')

        # TODO

    """ Altri possibili metodi per gestire di dd_anno """""
    def popola_dd_anno(self):
        self._model.getYears()
        if not self._model.anni:
            print('Anni non caricati')
            return
        self._view.dd_anno.options.clear()
        for year in self._model.anni:
            self._view.dd_anno.options.append(ft.dropdown.Option(key=year, text=year))
        self._view.update()

    def handle_on_change_squadre(self, str_anno):
        self.anno = int(str_anno)
        self._model.getTeams(self.anno)
        if not self._model.squadre:
            print('Squadre non caricate')
            return
        self._view.txt_out_squadre.controls.clear()
        for team in self._model.squadre:
            self._view.txt_out_squadre.controls.append(ft.Text(team))
            self._view.dd_squadra.options.append(ft.dropdown.Option(key=team.id, text=team.name))
        #sblocco il pulsante per creare il grafo
        self._view.pulsante_crea_grafo.disabled = False
        self._view.update()

    # TODO