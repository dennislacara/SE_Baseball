from operator import itemgetter
import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.anni = None
        self.squadre = None
        self.map_squadre = {}

        self.G = nx.Graph()

    def getYears(self):
        self.anni = DAO.readYears()

    def getTeams(self, year):
        self.squadre = DAO.readTeams(year)

    def creaGrafo(self, year):
        self.G.clear()
        self.map_squadre.clear()

        #implemento nodi con id
        for squadra in self.squadre:
            self.G.add_node(squadra.id)
            self.map_squadre[squadra.id] = squadra

        #implemento archi
        archi = self.calcolaArchi(year)
        for arco in archi:
            self.G.add_edge(arco[0], arco[1], peso=int(arco[2]))
        print(self.G)

    def calcolaArchi(self, year):
        lista_archi_pesati = DAO.readArchi(year)
        return lista_archi_pesati

    def calcola_percorso(self,id_partenza):
        self.best_percorso = []
        self.best_valore = float('-inf')

        pp = [id_partenza]
        vp = 0
        self.ricorsione(self.G, pp, vp)

        return self.best_percorso, self.best_valore
    def ricorsione(self, G, pp, vp):

        if vp > self.best_valore:
            lista = []
            for i in range(len(pp)-1):
                lista.append((pp[i+1], G[pp[i]][pp[i+1]]['peso']))
            self.best_percorso = lista.copy()
            self.best_valore = vp
            print(self.best_percorso)
            print(self.best_valore)

        n = sorted([(v,data['peso']) for u,v,data in G.edges(pp[-1], data=True)], key=itemgetter(1), reverse=True)
        nodi = [v[0] for v in n if v[0] not in pp]
        for nodo in nodi[:3]:

            if nodo in pp:
                continue
            if len(pp)>=2 and G[pp[-1]][nodo]['peso'] > G[pp[-2]][pp[-1]]['peso']:
                continue

            pp.append(nodo)
            vp_new = vp + G[pp[-2]][pp[-1]]['peso']
            self.ricorsione(G, pp, vp_new)
            pp.pop()
