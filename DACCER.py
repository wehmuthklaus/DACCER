__author__ = 'Klaus Wehmuth'
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import scipy.stats as sts
import pickle as pck
import csv as csv
import os

def DACCER(_g,  _h):
  """ Returns DACCER calculated with radius _h for all nodes
  of the NetworkX undirected graph _g
  :input: NetworkX undirected graph _g and neighborhood radius _h
  :output: Sorted dictionary with nodes and their DACCER value
  """
  dvc = {}
  for nd in _g:
      dg = _g.degree(nd)
      nds = _getNeighborhood(_g,  nd,  _h)
      dg = nx.degree(_g,  nds)
      k2 =  sum(dg.values())
      dvc[nd] = k2
  srt = sorted(dvc.iteritems(),  cmpVal,  reverse=True)
  return srt

def Closeness(_g):
    """ Returns Closeness centrality for all nodes
    of the NetworkX undirected graph _g
    :input: NetworkX undirected graph _g
    :output: Sorted dictionary with nodes and their Closeness centrality value
    """
    clo = nx.closeness_centrality(_g)
    srt = sorted(clo.iteritems(),  cmpVal,  reverse=True)
    return srt

def getNetworkFromEdgeList(_path):
   """ Returns the giant component of a network constructed from
   a given edge list
   :input: A path for a text file containing an edge list
   :output: The giant component of an undirected NetworkX graph generated
   from the given edge list
   """ 
   g = nx.read_edgelist(_path)
   return getGiantComponent(g)

def getGiantComponent(_g):
    """ Returns the giant component of the NetworkX undirected graph _g
    :input: Undirected NetworkX graph _g
    :output: Undirected NetworkX graph containing the giant component of _g
    """ 
    comps = nx.connected_components(_g)
    n = -1
    i = -1
    s = -1
    for c in comps:
        i = i+1
        if len(c) > s:
            s = len(c)
            n = i
    return _g.subgraph(comps[n])

def calcPearson(_xCent,  _yCent):
    """ Returns the Pearson correlation of the ranking between 2 centrality dictionaries
    :input: Centrality dictionaries _xCent and _yCent
    :output: Pearson correaltion of the ranking of the 2 centralities
    """ 
    rgn = range(len(_xCent))
    order = []
    for n in rgn:
        v = _xCent[n][0]
        order.append(getPos(v,  _yCent))
    return sts.pearsonr(rgn,  order)
   
def plotScatter(_xCent,  _yCent,  _xlabel,  _ylabel,  _title,  _range=None):
    """ Plots the scatter graph of 2 centralities ranking
    :input: Two centralities ranking dictionaries, 2 centralities lables, a plot title and an optional range
    :output: Pearson's correlation
    The plot is displayed on teh screnn
    """ 
    if _range == None:
        rgn = range(len(_xCent))
    else:
        rgn = range(_range)
    
    order=[]
    for n in rgn:
        v = _xCent[n][0]
        order.append(getPos(v,  _yCent))
    corr = sts.pearsonr(rgn,  order)

    for n in range(len(order)):
        plt.plot(n,  order[n],  'ok')
    plt.plot(rgn, rgn,  '-b')
    plt.xlabel(_xlabel)
    plt.ylabel(_ylabel)
    plt.title(_title + '  Pearson = ' + repr(corr[0]))
    plt.show()
    return corr

def getPos(_val,  _yCent):
    for n in range(len(_yCent)):
        if _val == _yCent[n][0]:
            return n
       
def _getNeighborhood(_graph,  _rootNode,  _depth):
    if(_depth < 1):
        return set([_rootNode])
    edg = [_rootNode]
    edg.extend(_graph[_rootNode])
    if (_depth == 1):
        return set(edg)
    else:
        e = []
        for nd in edg:
            e.extend(_getNeighborhood(_graph,  nd,  (_depth -1)))
        return set(e)


def cmpVal(item1,  item2):
    if item1[1] > item2[1]:
        return 1
    if item1[1] < item2[1]:
        return -1
    return 0
