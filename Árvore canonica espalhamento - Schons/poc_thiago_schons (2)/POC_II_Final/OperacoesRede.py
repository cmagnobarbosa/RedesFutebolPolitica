#!/usr/bin/python
# coding: utf-8
#import igraph
from __future__ import division
from igraph import *
import numpy as numpy
import matplotlib.pylab as plt
import random
from operator import itemgetter
import sys


#Lista de arestas: rede.es
#print igraph.summary(rede)
class Util:
	grausVet = None

	def get_adjlist_with_names(self, graph):
		names = graph.vs["name"]
		result = {}
		for index, neighbors in enumerate(graph.get_adjlist()):
			result[names[index]] = [names[nei] for nei in neighbors]
		return result
	

		
	def assignCanonicalNames(self, rede, v, nomesCanonicos, f, di):
		
		listaFilhos = f[str(v)]
		
		#print "Na função f = " + str(f)
		teste = {}
		v = int(v)
		#print "f[v] = " + str(f[v])
		#print "v = " + str(v)
		if (len(listaFilhos) == 0):
		#	print "Nó folha = " + str(v)
			nomesCanonicos[int(v)] = "10"
		else:
			#print "f[v] = "+str(f[v])
			#print "Tamanho = " + str(len(listaFilhos))
			for i in range(len(listaFilhos)):
				#if (nomesCanonicos.has_key(f[v[i]])):
				#	print "O filho " + str(f[v[i]]) +" ja existe"
				#else:
				self.assignCanonicalNames(rede, listaFilhos[i],nomesCanonicos, f, di)
			#print str(nomesCanonicos)
		# ------- Se o nó não for folha --------
		#print "ListaFilhos = " + str(listaFilhos)
		#print "DIcionário = " + str(nomesCanonicos)
		if (len(listaFilhos) != 0):
			#Ordenar nomes dos filhos de v
			# "------------- Ordenação -------------"
			for i in range(len(listaFilhos)):
				k = int(listaFilhos[i])
				teste[k] = nomesCanonicos[k]
				
			teste = sorted(teste.items(), key=itemgetter(1))
			# "----------- Concatenação ------------"		
			a = ""
			for i in teste:
		#		print "i = "+str(i)
				a += i[1]
		#	print "a = "+str(a)
			nomesCanonicos[v] = "1"+a+"0"
			#print str(nomesCanonicos)
		return nomesCanonicos[v]

		# pythonhelp.wordpress.com/2014/04/06/ordenacao-de-uma-lista/
		# Procurar como criar uma lista com índices personalizados
	#------------------------------------------------------------------------------------------------------------------------
	# Função int: Faz a chamada das funções para a geração dos gráficos
	# @PARAMs: 
	# 			rede = rede gerada, 
	# 			nomeDoModelo = string com o nome do modelo utilizado ("ER", "WS", "BA")
	#------------------------------------------------------------------------------------------------------------------------
	def getNetworkInfo(self, rede, numVertices, nomeDoModelo, qtdInfectados, alpha):
		info = self.redeInfo(rede, numVertices, nomeDoModelo, qtdInfectados, alpha)
		#self.plotarGraficos(rede, nomeDoModelo)
		return info

	#------------------------------------------------------------------------------------------------------------------------
	# Função redeInfo: Geração das informações da rede conforme a função da biblioteca igraph
	# @PARAMS: 
	#			rede = rede gerada
	#			numVertices = número de vértices
	#------------------------------------------------------------------------------------------------------------------------
	def redeInfo(self, rede, numVertices, nomeDoModelo, qtdInfectados, alpha):
		grauMax =  rede.maxdegree(vertices=None, mode=ALL, loops=False)	
		vetGraus = rede.degree()
		#vetGraus = list(numpy.sort(rede.degree()))      Vetor de graus ordenado
		grauMin = vetGraus[0]
		grauMed = float(2*rede.ecount())/numVertices
		#coefClusteringMed = rede.transitivity_avglocal_undirected(mode="zero")
		#densidade = rede.density(loops=True)
		verticesCompGigante = 0
		#assortatividade = rede.assortativity_degree(directed=False)
		#distanciaMedia = rede.average_path_length(directed=False, unconn=False)
		qtdeVertex = len(rede.vs)
		vs = VertexSeq(rede)
		nomesCanonicosSementes = {}

		print "Grau Mínimo da Rede: " + str(grauMin)
		print "Grau Médio da Rede: " + str(grauMed)
		print "Grau Máximo da Rede: " + str(grauMax)
		#print "Coeficiente de Clustering Médio da Rede: " + str(coefClusteringMed)
		#print "Densidade da Rede: " + str(densidade)
		#print "Assortatividade da Rede: " + str(assortatividade)
		#print "Distância Média da Rede: " + str(distanciaMedia)
		print "Quantidade de vertices: " + str(qtdeVertex)
		
		t = rede.get_adjlist()		
		
		# --- Vetor de Graus já tem,  falta o ordenado e o de flag. --------- IMPORTANTE
		grausOrdenado = [0] * qtdeVertex	# Vetor de graus ordenado // Contém os índices do vetor de graus.
		flagsGraus = [0] * qtdeVertex		# Flags para saber se já foi ordenado ou não
		verticesAtivados = [0] * qtdeVertex	# --- Criação de vetor para vértices ativados --- : 0 - Não ativado, 1 - Ativado :

		for indice in range(len(vetGraus)):
			grausOrdenado[indice] = indice
			
		vetGraus = rede.degree(mode=OUT)
		
		#vetGraus = rede.transitivity_local_undirected()
		

		vetGraus, grausOrdenado = (list(x) for x in zip(*sorted(zip(vetGraus, grausOrdenado), reverse=True)))

		f1 = open("Influencia_"+alpha, 'a')
		
		verticesAtivados = [0] * qtdeVertex
		listaPais = []				#Nessa lista são salvas as posições que estão os seeds
		lista_inicial = []
		lista = []
		lista2 = []
		listaAuxiliar = []
		lista_prox = []
		listaGrafo = []
		# ---- Iteração sobre a quantidade de vértices adjacentes no modo de saída ----
		# grausOrdenado = indice de vetGraus
		g = Graph(directed = True)
		for i in range(0,int(qtdInfectados)):
			listaPais.append(i)
			verticesAtivados[grausOrdenado[i]] = 1
			lista.append(grausOrdenado[i])
			g.add_vertex(str(lista[i]))
			listaGrafo.append(g)
			g = Graph(directed = True)
		a = -1
		#			Até aqui OK!
		#print "Vetor grausOrdenado = " +str(grausOrdenado)
		#print "Tamanho Lista = " + str(len(lista))
		a = 0
		i = 0
		# O algoritmo para quando a = lista, porém tem que percorrer e testar todos os valores de lista
		while (len(lista) > i):
			#a = len(lista)
			listaAuxiliar = []
			listaAuxiliar = rede.neighbors(lista[i],OUT)
			for j in range(len(listaAuxiliar)):
				if (verticesAtivados[listaAuxiliar[j]] == 0):
					tes = random.random()
					#Esse é o normal, conforme o alpha do parâmetro.
					#if tes < float(alpha):
					#No próximo a probabilidade é igual a 1/grau de entrada do alvo.
					#if tes < (1/len(rede.neighbors(listaAuxiliar[j],IN))):
					#Escolhe aleatóriamente entre 0,1 0,01 e 0,001
					#aleatorio = random.randint(1,3)
					#if aleatorio == 1:
				#		alpha = 0.1
				#	if aleatorio == 2:
				#		alpha = 0.01
				#	if aleatorio == 3:
				#		alpha = 0.001
				#	if tes < float(alpha):
					if tes < (1/len(rede.neighbors(listaAuxiliar[j],IN))):
						listaGrafo[listaPais[i]].add_vertex(str(listaAuxiliar[j]))
						listaGrafo[listaPais[i]].add_edge(str(lista[i]),str(listaAuxiliar[j]))
						listaPais.append(listaPais[i])
						#print "Vértice = " +str(listaAuxiliar[j]) + " valor tes = " + str(tes)
						#g.add_edge(str(lista[i]),str(listaAuxiliar[j]))
						verticesAtivados[listaAuxiliar[j]] = 1
						lista.append(listaAuxiliar[j])
			i+=1
			#Incrementar o i
		
		
		for i in range(len(verticesAtivados)):
			if verticesAtivados[i] == 1:
				#print "Vértice " + str(i)
				a+=1
		print "Quantidade de infectados = " + str(qtdInfectados) + " Saida = " + str(a)
		
		f1.write(str(qtdInfectados)+ "\t\t" +str(a) + "\n" )

		for i in range(0,int(qtdInfectados)):

			nomesCanonicos = {}
			di = {}
			adjacentesList = self.get_adjlist_with_names(listaGrafo[i])
			nomesCanonicosSementes[i] = self.assignCanonicalNames(listaGrafo[i], str(lista[i]), nomesCanonicos, adjacentesList, di)
			#plot(listaGrafo[i], "Vertice_"+str(lista[i])+".png", vertex_color="blue")
		#print str(adjacentesList)
		print "Sementes: "
		print str(nomesCanonicosSementes)
		totalCanNames = 0
		contArvores = {}
		for i in range(0,int(qtdInfectados)):
			if contArvores.has_key(str(nomesCanonicosSementes[i])):
				contArvores[str(nomesCanonicosSementes[i])] += 1
				totalCanNames += 1
			else:
				contArvores[str(nomesCanonicosSementes[i])] = 1
				totalCanNames +=1
		print ("\n\n\n\n")
		#for i in range(len(contArvores)):
		#	print str(contArvores[str(i)])
		print str(contArvores)
		
		testarei = sorted(contArvores.items(), key=itemgetter(1), reverse = True)
		print ("\n\n\n\n")
		print str(testarei)
		
		fout = open("Canonical_"+alpha, 'a')
		fout.write("\nRede = "+ str(alpha) + " Total Names = "+ str(totalCanNames)+ " Quantidade Registros = "+str(len(testarei))+"\n")
		fout.write(str(testarei)+ "\n")

		print "Total = " + str(totalCanNames)
		print "Tamanho Registros = " + str(len(testarei))
		
		

		#print "Tamanho da árvore = " + str(len(listaGrafo[9].vs))
		########### COLOCAR MAIOR QUANTIDADE listaGrafo[15] por exemplo e 
			
		#a = self.assignCanonicalNames(g, str(a), nomesCanonicos)
		#print "Informações do grafo -----"
		#print "Tamanho = " + str(len(listaGrafo[9].vs))
		#print "\n\n Tamanho = " + str(len(a)) + " Nome Canonico = " + str(a)

		#operacoes.getNetworkInfo(redeReal1, len(redeReal1.vs), "RR1", qtdInfectados, alpha)
