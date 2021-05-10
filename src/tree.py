from datetime import datetime


class Tree(object):
    def __init__(self, state, time=False):
        self.time = time
        self.OPEN = [state]
        self.CLOSE = []
        self.start_time =  datetime.now()
        self.max_size_open = 0 # complexite en taille = len max de open_list
        self.max_time = 0 # complexite en temps = nbr de noeuds explores


    def getByHash(self, h, l="open"):
        i = 0
        for state in self.OPEN if l == "open" else self.CLOSE:
            if state['hash'] == h:
                return state, i
            i += 1
        return None , 0


    def update_statistique(self):
        l = len(self.OPEN)
        if self.max_size_open < l:
            self.max_size_open = l


    def close(self, state):
        similar , index = self.getByHash(state['hash'])
        if similar is not None:
            self.OPEN.pop(index)
            self.CLOSE.append(state)
        self.update_statistique()


    def open(self, state):
        self.OPEN.append(state)
        self.update_statistique()


    def getBest(self):
        self.max_time += 1
        best = None
        for state in self.OPEN:
            if best is None or state['score'] < best['score']:
                best = state.copy()
        return best

    def show(self, state):
        print("Complexité en temps: ", self.max_time)
        print("Complexité en taille: ", self.max_size_open)
        print("Nombres de mouvement: " , state['deep'])
        if self.time:
            print("Durée: ",  format(datetime.now() - self.start_time), 's')
        print("Solution: ", state['moves']);
        return state['moves']
