# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # Retornar um caminho até o objetivo explorando primeiro os nós mais profundos

    frontier = util.Stack()  # frontier é fronteira = nós a serem explorados -> Last In, First Out
    start = problem.getStartState()

    # Cada item da pilha: (estado_atual, caminho_de_acoes)
    frontier.push((start, []))  # inicializa pilha empilhando o estado inicial, um caminho vazio (sem ações ainda)
                                
    visited = set()  # conjunto de estados já visitados para evitar ciclos
    
    while not frontier.isEmpty():  # enquanto a pilha não estiver vazia
        state, path = frontier.pop()  # desempilha o 
        # estado atual e o caminho de ações para chegar até ele

        if state in visited:   # se estado já foi visitado,
            continue            # **ignora** e continua para o próximo da pilha (desempilha)
            # continue pula o restante do código dentro do loop e volta para a próxima iteração do loop
        visited.add(state)

        if problem.isGoalState(state):
            return path  #achou o objetivo, retorna o caminho de ações para chegar até ele

        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                frontier.push((successor, path + [action])) #empilha o estado sucessor, o caminho de ações atualizado 
                # inicia a explorar o sucessor, adicionando a ação necessária para chegar até ele ao caminho atual já visitado
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # Retorna um caminho até o objetivo explorando primeiro os nós mais rasos (menor profundidade)
    
    frontier = util.Queue()  # frontier é fronteira = nós a serem explorados -> First In, First Out
    start = problem.getStartState()

    # Cada item: (estado, caminho_de_acoes)
    frontier.push((start, []))  # inicializa fila enfileirando o estado inicial com caminho vazio
                                
    visited = set([start])  # conjunto de estados já visitados (já marca ao inserir para evitar duplicatas na fila)

    while not frontier.isEmpty():  # enquanto a fila não estiver vazia
        state, path = frontier.pop()  # remove da fila o primeiro estado inserido (mais raso)
        # estado atual e o caminho de ações para chegar até ele

        if problem.isGoalState(state):
            return path  # achou o objetivo, retorna o caminho de ações para chegar até ele

        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:  # se ainda não foi visitado
                visited.add(successor)  # marca como visitado no momento da inserção (evita repetição na fila)
                frontier.push((successor, path + [action]))  # enfileira o sucessor com caminho atualizado

    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    # fila de prioridade: menor custo primeiro
    from util import PriorityQueue

    fronteira = PriorityQueue()
    inicio = problem.getStartState()

    # adiciona o estado inicial na fila com custo 0
    fronteira.push((inicio, [], 0), 0)

    #  guarda o menor custo encontrado p/ cada estado
    visitados = {}  

    # enquanto tiver nós para explorar
    while not fronteira.isEmpty():
        estado, caminho, custo = fronteira.pop()

        # só expande se for o melhor custo até agora
        if estado not in visitados or custo < visitados[estado]:
            visitados[estado] = custo

            if problem.isGoalState(estado):
                return caminho

            for sucessor, acao, passo in problem.getSuccessors(estado):
                novo_caminho = caminho + [acao]
                novo_custo = custo + passo
                fronteira.push((sucessor, novo_caminho, novo_custo), novo_custo)

    return [] # retorna vazio se nn encontrar solução


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # add heuristica ao UCS
    
    from util import PriorityQueue 

    fronteira = PriorityQueue()
    inicio = problem.getStartState()

    # prioridade inicial = heurística do estado inicial
    fronteira.push((inicio, [], 0), heuristic(inicio, problem))

    # guarda g(n)
    visitados = {}  

    while not fronteira.isEmpty():
        estado, caminho, custo = fronteira.pop()

        if estado not in visitados or custo < visitados[estado]:
            visitados[estado] = custo

            if problem.isGoalState(estado):
                return caminho

            for sucessor, acao, passo in problem.getSuccessors(estado):
                novo_caminho = caminho + [acao]
                novo_custo = custo + passo
                prioridade = novo_custo + heuristic(sucessor, problem) # f(n) = g(n) + h(n)

                fronteira.push((sucessor, novo_caminho, novo_custo), prioridade)

    return [] 


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
