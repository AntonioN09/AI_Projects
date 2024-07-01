import time

#1
f = open('lab2.txt', 'r')
N, M = f.readline().strip().split()

class State:
    N = 3
    M = 2

    def __init__(self, canibali = 3, misionari = 3, poz = -1):
        self.canibali = canibali
        self.misionari = misionari
        self.poz = poz

    def __eq__(self, other):
        if self.canibali == other.canibali and self.misionari == other.misionari:
            if self.poz == other.poz:
                return True
        return False
    
    def __str__(self):
        return str(self.misionari) + ' misionari, ' + str(self.canibali) + ' canibali | ' + str(self.N - self.misionari) + ' misionari, ' + str(self.N - self.canibali) + ' canibali' 

    def __repr__(self):
        return '(' + str(self.canibali) + ', ' + str(self.misionari) + ', ' + str(self.poz) + ')'

State.N = int(N)
State.M = int(M)
# print(State.M)
state = State()
# print([state])

#2
class Nod:
    def __init__(self, informatie, succesori, parinte=None):
        self.informatie = informatie
        self.succesori = succesori
        self.parinte = parinte

    def __eq__(self, other):
        return self.informatie == other.informatie
    
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
    
    def printDrumRadacina(self):
        g = open('lab2output.txt', 'w')
        drum = self.drumRadacina()
        g.write('Stare curenta:\n')
        g.write(str(drum[0]) + '\n')
        g.write('\n')
        nodAnterior = drum[0]
        for nod in drum[1:]:
            if nodAnterior.informatie.poz == -1:
                g.write('Barca s-a deplasat de pe malul stang pe malul drept cu {} misionari si {} canibali.\n'.format(nodAnterior.informatie.misionari - nod.informatie.misionari, nodAnterior.informatie.canibali - nod.informatie.canibali))
                g.write('\n')
                g.write('Stare curenta:\n')
                g.write(str(nod) + '\n')
                g.write('\n')
            else:
                g.write('Barca s-a deplasat de pe malul drept pe malul stang cu {} misionari si {} canibali.\n'.format(nod.informatie.misionari - nodAnterior.informatie.misionari, nod.informatie.canibali - nodAnterior.informatie.canibali))
                g.write('\n')
                g.write('Stare curenta:\n')
                g.write(str(nod) + '\n')
                g.write('\n')
            nodAnterior = nod
        end_time = time.time()
        g.write('\nTimpul de rulare: ' + str(end_time - start_time) + ' secunde')
        


class Graf:
    def __init__(self, nodStart, muchii, noduriScop = []):
        self.nodStart = nodStart
        self.muchii = muchii
        self.noduriScop = noduriScop

    def scop(self, nod):
        if nod in self.noduriScop:
            return True
        return False
    
    def succesori(self, nod):
        if nod.informatie.poz == -1: # malul stang
            crt_canibali = nod.informatie.canibali
            crt_misionari = nod.informatie.misionari
            succ_canibali = State.N - nod.informatie.canibali
            succ_misionari = State.N - nod.informatie.misionari
        else: # malul drept
            crt_canibali = State.N - nod.informatie.canibali
            crt_misionari = State.N - nod.informatie.misionari
            succ_canibali = nod.informatie.canibali
            succ_misionari = nod.informatie.misionari
        
        min_misionari = 0
        max_misionari = min(State.M, crt_misionari)
        for misionari_barca in range(min_misionari, max_misionari + 1):
            if misionari_barca == 0:
                min_canibali = 1
                max_canibali = min(State.M, crt_canibali)
            else:
                min_canibali = 0
                max_canibali = min(State.M - misionari_barca, misionari_barca, crt_canibali)
            for canibali_barca in range(min_canibali, max_canibali + 1):
                new_crt_misionari = crt_misionari - misionari_barca
                new_crt_canibali = crt_canibali - canibali_barca
                new_succ_misionari = succ_misionari + misionari_barca
                new_succ_canibali = succ_canibali + canibali_barca
                if (new_crt_misionari == 0 or new_crt_misionari >= new_crt_canibali) and (new_succ_misionari == 0 or new_succ_misionari >= new_succ_canibali):
                    if nod.informatie.poz == -1:
                        new_informatie = State(new_crt_canibali, new_crt_misionari, 1)
                    else:
                        new_informatie = State(new_succ_canibali, new_succ_misionari, -1)
                    new_nod = Nod(new_informatie, [], nod)
                    if not new_nod.vizitat():
                        nod.succesori.append(new_nod)
        return nod.succesori

#3
def BFS(graf, n = 1):
    if n > len(graf.noduriScop):
        n == len(graf.noduriScop)
    coada = [graf.nodStart]
    rezultat = []
    while coada != []:
        crt = coada.pop(0)
        if crt in graf.noduriScop:
            rezultat.append(crt)
        if len(rezultat) == n:
            return rezultat
        for nod in graf.succesori(crt):
            if not nod.vizitat():
                coada.append(nod)
    return rezultat

start_time = time.time()
new_state = State(3, 3, -1)
new_nod = Nod(new_state, [])
scop_state = State(0, 0, 1)
scop_nod = Nod(scop_state, [])
new_graf = Graf(new_nod, [], [scop_nod])

noduriScop = BFS(new_graf, 1)
for nod in noduriScop:
    nod.printDrumRadacina()