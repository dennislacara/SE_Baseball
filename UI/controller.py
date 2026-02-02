import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        anno = int(self._view.dd_anno.value)
        grafo = self._model.crea_grafo(anno)
        if not grafo:
            self._view.show_alert('Non ci sono archi')
            return
        else:
            self._view.show_alert(f'Grafo creato: nodi ~ {grafo.number_of_nodes()} - archi ~ {grafo.number_of_edges()}' )
        # TODO

    def handle_dettagli(self, e):
        """ Handler per gestire i dettagli """""
        s = int(self._view.dd_squadra.value)
        vicini = self._model.calcola_vicini(s)
        if not vicini:
            self._view.show_alert('Non ci sono vicini al nodo')
            return
        else:
            self._view.txt_risultato.controls.clear()
            for v in vicini:
                s = self._model.map_teams[v[0]]
                self._view.txt_risultato.controls.append(ft.Text(f'{s.team_code} ({s.name}) : {v[1]}'))
            self._view.update()

        # TODO

    def handle_percorso(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del percorso """""
        try:
            s = int(self._view.dd_squadra.value)
        except Exception as e:
            print(e)
            self._view.show_alert('Selezionare una squadra')
            return
        percorso,valore, info = self._model.calcola_percorso(s)
        self._view.txt_risultato.controls.clear()
        for i in range(len(percorso)-1):
            self._view.txt_risultato.controls.append(ft.Text(f'{percorso[i].team_code} ({percorso[i].name}) ~~> {percorso[i+1].team_code} ({percorso[i+1].name}): {info[i][2]}'))
        self._view.txt_risultato.controls.append(ft.Text(f'Valore del percorso: {valore}'))
        self._view.update()

        # TODO

    """ Altri possibili metodi per gestire di dd_anno """""
    def populate_dd_anno(self):
        anni = self._model.get_years()
        l = []
        for a in anni:
            if a not in l:
                l.append(a)
                self._view.dd_anno.options.append(ft.dropdown.Option(key = a, text = a))
        self._view.update()

    def handle_on_change_year(self, e):
        anno = int(e.control.value)
        squadre = self._model.get_squadre_anno(anno)

        self._view.dd_squadra.options.clear()
        self._view.txt_out_squadre.controls.clear()
        #gestione dd_anno e txt_out_squadre
        self._view.txt_out_squadre.controls.append(ft.Text(f'Numero di squadre: {len(squadre)}'))
        for s in squadre:
            self._view.dd_squadra.options.append(ft.dropdown.Option(key = s.id, text = s.name))
            self._view.txt_out_squadre.controls.append(ft.Text(f'{s.team_code} ({s.name})'))
        self._view.dd_squadra.value = None
        self._view.update()

    # TODO