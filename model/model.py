import networkx as nx

from database.dao import DAO

class Model:
    def __init__(self):
        self.teams = []
        self.map_teams ={}
        self.load_teams()

        self.archi = []
        self.G = nx.Graph()


        self.best_percorso =[]
        self.best_valore = 0
        self.info = []

    def load_teams(self):
        self.teams = DAO.read_teams()
        for team in self.teams:
            self.map_teams[team.id] = team

    def teams_for_year(self, year):
        pass
    def get_years(self):
        l = []
        for t in self.teams:
            l.append(t.year)
        return l
    def get_squadre_anno(self, year):
        l =[]
        for team in self.teams:
            if team.year == year:
                l.append(team)
        return l

    def crea_grafo(self,anno):
        self.G.clear()
        #implemento nodi
        for team in self.teams:
            if team.year == anno:
                self.G.add_node(team.id)
        #implemento archi
        self.load_archi(anno)
        if not self.archi:
            print('Nessun arco')
            return
        for arco in self.archi:
            self.G.add_edge(arco.id1, arco.id2, peso = arco.total_salary)
        return self.G

    def load_archi(self,anno):
        self.archi = DAO.read_archi(anno)

    def calcola_vicini(self, nodo):
        l = []
        for i,j,data in self.G.edges(nodo, data=True):
            l.append((j, data['peso']))
        l = sorted(l, key=lambda x: x[1], reverse=True)
        return l

    def calcola_percorso(self, nodo_partenza):
        self.best_percorso =[]
        self.best_valore = 0
        self.info = []

        lp = [nodo_partenza]
        vp = 0
        info = []

        self.ricorsione(self.G, lp, vp, info)
        if self.best_percorso:
            self.best_percorso = [self.map_teams[n] for n in self.best_percorso]
        return self.best_percorso, self.best_valore, self.info

    def ricorsione(self, grafo, lp, vp, info):
        print(lp)
        if vp> self.best_valore:
            self.best_valore = vp
            self.best_percorso = lp.copy()
            self.info = info.copy()

        vicini = self.calcola_vicini_Kdecr(lp[-1],list(nx.neighbors(grafo, lp[-1])), lp)
        for v in vicini:
            peso_succ = grafo[lp[-1]][v]['peso']

            if v in lp:
                continue
            if len(lp)>=2:
                peso_pre = grafo[lp[-2]][lp[-1]]['peso']
                if peso_succ > peso_pre:
                    continue
            lp.append(v)
            info.append((lp[-1], v, peso_succ))
            self.ricorsione(grafo, lp, vp + peso_succ, info)
            lp.pop(-1)
            info.pop(-1)

    def calcola_vicini_Kdecr(self, nodo, vicini,lp):
        k = 3
        l =[]
        for vicino in vicini:
            if not vicino in lp:
                peso = self.G[nodo][vicino]['peso']
                l.append((vicino, peso))
        l = sorted(l, key=lambda x: x[1], reverse=True)

        if len(lp) >=2:
            l = [v[0] for v in l if v[1]< self.G[lp[-2]][lp[-1]]['peso']]
        else:
            l = [v[0] for v in l]
        return l[:k]

