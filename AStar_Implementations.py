from queue import PriorityQueue
from time import time
import heapq
import copy

#1
class Nod:
    def __init__(self, informatie, succesori, parinte = None, g = 0, h = 0):
        self.informatie = informatie
        self.succesori = succesori
        self.parinte = parinte
        self.g = g
        self.h = h
        self.f = g + h

    def __eq__(self, other):
        return self.f == other.f and self.g == other.g
    
    def __lt__(self, other):
        return (self.f < other.f) or (self.f == other.f and self.g > other.g)
    
    def __str__(self):
        return str(self.informatie)
    
    def __repr__(self):
        result = str(self.informatie) + ' ('
        for nod in self.drumRadacina():
            result += str(nod.informatie)
            if nod != self:
                result += ' -> '
        return result + ')'
  
    def drumRadacina(self):
        if self.parinte is None:
            return [self]
        return self.parinte.drumRadacina() + [self]
    
    def vizitat(self):
        return len([1 for nod in self.drumRadacina() if nod == self]) > 1

class Graf:
    def __init__(self, nodStart, muchii, noduriScop = [], est_h = []):
        self.nodStart = nodStart
        self.muchii = muchii
        self.noduriScop = noduriScop
        self.est_h = est_h

    def scop(self, nod):
        if nod.informatie in self.noduriScop:
            return True
        return False
    
    def estimeaza_h(self, nod):
        est = [x[1] for x in self.est_h if x[0] == nod]
        return est[0]

    def succesori(self, nod):
        if nod.succesori:
            return nod.succesori

        for nod1, nod2, cost in self.muchii:
            if nod1 != nod.informatie:
                continue

            nodCurent = Nod(nod2, [], nod, nod.g + cost, self.estimeaza_h(nod2))
            if nodCurent.vizitat():
                continue
            nod.succesori.append(nodCurent)

        return nod.succesori
    
graf = Graf(0, 
            [(0, 1, 3), (0, 2, 5), (0, 3, 10), (0, 6, 100), 
             (1, 3, 4), (2, 3, 4), (2, 4, 9), (2, 5, 3), 
             (3, 1, 3), (3, 4, 2), (5, 4, 4), (6, 2, 3)],
             [4, 6], 
            [(1, 1), (2, 6), (3, 2), (4, 0), (5, 3), (6, 0)])

# Exemplu inadmisibil 
# graf = Graf(0, 
#             [4, 6], 
#             [(0, 1, 3), (0, 2, 5), (0, 3, 10), (0, 6, 100), 
#              (1, 3, 4), (2, 3, 4), (2, 4, 9), (2, 5, 3), 
#              (3, 1, 3), (3, 4, 2), (5, 4, 4), (6, 2, 3)], 
#             [(1, 1), (2, 6), (3, __3__), (4, 0), (5, 3), (6, 0)])


#2 Time: 0.012031316757202148
# nsol = int(input("Numarul de solutii: "))
nsol = 2
def aStarSolMultiple(graf, nsol):
    rad = Nod(graf.nodStart, [])
    coada = [rad]
    while(coada != []):
        nod_crt = coada.pop(0)
        if graf.scop(nod_crt):
            print('Drum: ' + str(nod_crt.drumRadacina()))
            print('Lungime ' + str(nod_crt.f))
            nsol -= 1
            if(nsol == 0):
                break
        
        for succesor in graf.succesori(nod_crt):
            if(coada == []):
                coada.append(succesor)
            start = 0
            stop = len(coada) - 1
            while start <= stop:
                m = start + (stop - start) // 2
                if coada[m].f < succesor.f:
                    start = m + 1
                elif coada[m].f >= succesor.f:
                    index = m
                    stop = m - 1
            if coada[index].g < succesor.g:
                index += 1
            coada.insert(index, succesor)

# startListTime = time()
# aStarSolMultiple(graf, nsol)
# ListTime = time() - startListTime
# print(ListTime)


#3 Time 0.0032677650451660156 - mai rapid cu PQ
def aStarSolMultiplePQ(graf, nsol):
    rad = Nod(graf.nodStart, [])
    coada = PriorityQueue()
    coada.put(rad)
    while(not coada.empty()):
        nod_crt = coada.get()
        if graf.scop(nod_crt):
            print('Drum: ' + str(nod_crt.drumRadacina()))
            print('Lungime ' + str(nod_crt.f))
            nsol -= 1
            if(nsol == 0):
                break
        
        for succesor in graf.succesori(nod_crt):
            coada.put(succesor)

# startPQTime = time()
# aStarSolMultiplePQ(graf, nsol)
# PQTime = time() - startPQTime
# print(PQTime)


#4 Time: 0.0
def calc_index(array, new_nod):
    index = 0
    start = 0
    stop = len(array) - 1
    while start <= stop:
        m = start + (stop - start) // 2
        if array[m].f < new_nod.f:
            start = m + 1
        elif array[m].f >= new_nod.f:
            index = m
            stop = m - 1
    if array[index].g < new_nod.g:
        index += 1
    
    return index

def a_star(graf):
    l_open = []
    l_closed = []
    rad = Nod(graf.nodStart, [])
    l_open.append(rad)

    while l_open != []:
        crt_nod = l_open.pop(0)
        l_closed.append(crt_nod)

        if graf.scop(crt_nod):
            print('Drum: ' + str(crt_nod.drumRadacina()))
            print('Lungime ' + str(crt_nod.f))
            break

        succesori = graf.succesori(crt_nod)
        for succesor in succesori:
            new_nod = None
            if succesor in l_open:
                idx = l_open.index(succesor)
                if succesor < l_open[idx]:
                    l_open.pop(idx)
            elif succesor in l_closed:
                idx = l_closed.index(succesor)
                if succesor < l_closed[idx]:
                    l_closed.pop(idx)
            new_nod = succesor

            if new_nod is not None:
                if(l_open == []):
                    l_open.append(new_nod)
                index = calc_index(l_open, new_nod)
                l_open.insert(index, new_nod)

# startAStarTime = time()
# a_star(graf)
# AStarTime = time() - startAStarTime
# print(AStarTime)


#5 Time: 0.0 - too efficient
def a_star_eficient(graf):
    l_open = []
    l_closed = {}
    rad = Nod(graf.nodStart, [])
    heapq.heappush(l_open, rad)

    while l_open != []:
        crt_nod = heapq.heappop(l_open)
        l_closed[crt_nod.informatie] = crt_nod

        if graf.scop(crt_nod):
            print('Drum: ' + str(crt_nod.drumRadacina()))
            print('Lungime ' + str(crt_nod.f))
            break

        succesori = graf.succesori(crt_nod)
        for succesor in succesori:
            new_nod = None
            if succesor in l_open:
                idx = l_open.index(succesor)
                if succesor < l_open[idx]:
                    l_open.pop(idx)
            elif succesor.informatie in l_closed.keys():
                if succesor < l_closed[succesor.informatie]:
                    l_closed.pop(idx)
            new_nod = succesor

            if new_nod is not None:
                heapq.heappush(l_open, new_nod)

# startAStarTimeEf = time()
# a_star_eficient(graf)
# AStarTimeEf = time() - startAStarTimeEf
# print(AStarTimeEf)

#6
class State:
  N = 3
  M = 2

  def __init__(self, misionari = N, canibali = N, barca = -1):
    self.misionari = misionari
    self.canibali = canibali
    self.barca = barca

  def __eq__(self, cls):
     return self.barca == cls.barca and \
     self.misionari == cls.misionari and self.canibali == cls.canibali

  def __str__(self):
    return 'Stare curenta:\n' + \
    f'{str(self.misionari)} misionari, ' + \
    f'{str(self.canibali)} canibali | ' + \
    f'{str(self.N - self.misionari)} misionari, ' + \
    f'{str(self.N - self.canibali)} canibali \n' + \
    f'Barca se afla pe malul {"stang" if self.barca == -1 else "drept"}\n'

  def __repr__(self):
    return ('({} {} {})').format(self.misionari, self.canibali, self.barca)

  def succ(self):
    succesori = []

    # Calculez cati misionari si canibali sunt pe malul cu barca
    misionari_barca = self.misionari if self.barca == -1 else self.N - self.misionari
    canibali_barca = self.canibali if self.barca == -1 else self.N - self.canibali

    for locuri in range(1, self.M + 1):
      for locuriMisionari in range(misionari_barca + 1):
        if locuriMisionari > locuri:
          continue

        # Verific sa existe cati canibali vreau sa plimb
        locuriCanibali = locuri - locuriMisionari
        if locuriCanibali < 0 or locuriCanibali > canibali_barca:
          continue

        # Verific sa nu fie mancati misionari in barca
        if locuriCanibali > locuriMisionari and locuriMisionari > 0:
          continue

        # Verific sa nu fie mancati misionari pe malul de plecare
        if canibali_barca - locuriCanibali > misionari_barca - locuriMisionari and \
        misionari_barca - locuriMisionari > 0:
          continue
        
        # Verific sa nu fie mancati misionari pe malul de sosire
        if (self.N - canibali_barca) + locuriCanibali > \
        (self.N - misionari_barca) + locuriMisionari and \
        (self.N - misionari_barca) + locuriMisionari > 0:
          continue

        # Trucuri de notatie:
        stareCurenta = State(
            self.misionari + self.barca * locuriMisionari, 
            self.canibali + self.barca * locuriCanibali, 
            (-1) * self.barca)

        succesori.append(stareCurenta)

    return succesori


class Node:
  def __init__(self, informatie, parinte = None, cost = 0, succesori = []):
    self.informatie = informatie
    self.parinte = parinte
    self.cost = cost
    self.succesori = copy.deepcopy(succesori)

  def __str__(self):
    return str(self.informatie)

  def __repr__(self):
    return ('({} {} {})').format(self.informatie.misionari, 
                                 self.informatie.canibali, 
                                 self.informatie.barca)

  def __eq__(self, cls):
     return self.informatie == cls.informatie
  
  def __lt__(self, cls):
     return self.cost < cls.cost
  
  def drumRadacina(self):
    if self.parinte is None:
      return [self]
    return self.parinte.drumRadacina() + [self]

  def vizitat(self):
    return self.informatie in [nod.informatie for nod in self.parinte.succesori]

  def printDrumRadacina(self):
    drum = self.drumRadacina()
    afisare = str(drum[0])

    for i in range(1, len(drum)):
      state = drum[i - 1].informatie
      stateCurent = drum[i].informatie

      afisare += f'\nBarca a plecat de pe malul ' + \
      f'{"stang" if state.barca == -1 else "drept"} ' + \
      f'cu {abs(state.misionari - stateCurent.misionari)} misionari ' + \
      f'si {abs(state.canibali - stateCurent.canibali)} canibali\n\n' + \
      str(stateCurent)

    return afisare
  

class Graph:
  def __init__(self, nodStart, noduriScop):
    self.nodStart = nodStart
    self.noduriScop = noduriScop

  def scop(self, info_nod):
    return info_nod in self.noduriScop

  def succesori(self, nod):
    succesori = nod.informatie.succ()

    for stare in succesori:
      nodCurent = Node(stare, nod, nod.cost + 1)
      if nodCurent.vizitat():
        continue

      nod.succesori.append(nodCurent)

    return nod.succesori

def a_star_6(graph):
    l_open = []
    l_closed = {}
    rad = graph.nodStart
    heapq.heappush(l_open, rad)

    while l_open != []:
        crt_node = heapq.heappop(l_open)
        l_closed[str(crt_node.informatie)] = crt_node

        if graph.scop(crt_node.informatie):
            print('Drum: ' + str(crt_node.drumRadacina()))
            print('Lungime ' + str(crt_node.cost))
            break

        succesori = graph.succesori(crt_node)
        for succesor in succesori:
            new_node = None
            if succesor in l_open:
                idx = l_open.index(succesor)
                if succesor < l_open[idx]:
                    l_open.pop(idx)
            elif str(succesor.informatie) in l_closed.keys():
                if succesor < l_closed[str(succesor.informatie)]:
                    l_closed.pop(idx)
            new_node = succesor

            if new_node is not None:
                heapq.heappush(l_open, new_node)


new_state = State(3, 3, -1)
new_nod = Node(new_state)
scop_state = State(0, 0, 1)
new_graf = Graph(new_nod, [scop_state])
a_star_6(new_graf)