# coding: utf-8

import igraph as igraph
from igraph import *
import numpy as numpy
import matplotlib.pylab as plt
from random import *
from OperacoesRede import Util
import numpy as numpy
import matplotlib.pylab as plt
from operator import itemgetter

arquivo1 = sys.argv[1]					
qtdInfectados = sys.argv[2]
#redeReal1 =  igraph.Graph.Read_GML(arquivo1)
#redeReal1 = rede1.Read(arquivo1)
redeReal1 = Graph()
redeReal1 = redeReal1.Read(arquivo1)
qtdeVertex = Graph.Read_Ncol(arquivo1, names=True, weights="if_present", directed=True)
#print "\n\n> Qtde Vértices: " + str(qtdeVertex)

operacoes = Util()

print "\n\n> Informações sobre as redes reais:"
info1 = operacoes.getNetworkInfo(redeReal1, len(redeReal1.vs), "RR1", qtdInfectados, arquivo1)
a = 1
b = 2
c = 3
g = Graph(directed = True)
g.add_vertex(str(a))
g.add_vertex(str(b))
g.add_vertex(str(c))
g.add_edge(str(a),str(b))
g.add_edge(str(a),str(c))
g.add_edge(str(b),str(c))

redeReal3 = redeReal1

listaRedes = []

listaRedes.append(redeReal1)
listaRedes.append(g)
listaRedes.append(redeReal3)
listaRedes[1].add_edge(str(b),str(c))

#plot(g, "g.png", vertex_color="blue")
#plot(listaRedes[1], "rr1.png", vertex_color="blue")
