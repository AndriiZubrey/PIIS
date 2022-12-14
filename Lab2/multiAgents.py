# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        
        # aka Score
        evalNum = 0

        # Ghost eval
        listOfGhostDist = []
        closestGhost = 0
        for ghost in range(len(newGhostStates)): # range(len()) for indexation
            ghostPos = successorGameState.getGhostPositions()[ghost] # indexation of ghosts
            listOfGhostDist.append(manhattanDistance(newPos, ghostPos))
        if listOfGhostDist != []:
            closestGhost = min(listOfGhostDist) # min distance
        
        # Food eval
        listOfFoodDist = []
        closestFood = 0
        for food in newFood.asList():
            listOfFoodDist.append(manhattanDistance(newPos, food))
        if listOfFoodDist != []:
            closestFood = min(listOfFoodDist) # min distance

        # Capsule eval
        capsules = currentGameState.getCapsules()
        listOfCapsDist = []
        closestCapsule = 0
        for capsule in capsules:
            listOfCapsDist.append(manhattanDistance(newPos, capsule))
        if listOfCapsDist != []:
            closestCapsule = min(listOfCapsDist) # min distance

        # Eval calc
        closestScaredGhostIndex = listOfGhostDist.index(closestGhost)
        foodCost = (1/(closestFood + 1)) + (1/(len(listOfFoodDist) + 1)) # min distance + count (less dots - higher score) conv to <1
        capsuleCost = (1/(closestCapsule + 1)) + (1/(len(listOfCapsDist) + 1)) # same
        ghostCost = (1/(closestGhost + 1)) # min distance conv to <1
        if closestGhost>1:
            evalNum += foodCost + capsuleCost + successorGameState.getScore()
            if newScaredTimes[closestScaredGhostIndex]>1: # if scared --> + ghost cost
                evalNum += ghostCost
            else: # else --> - ghost cost
                evalNum += -ghostCost
        else:
            evalNum = -1 # if too close -- run away
        return evalNum

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def minimaxAlgo(self, state, depth, agent_index):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state), None
        elif agent_index == 0:
            return self.maximize(state, depth, agent_index)
        else:
            return self.minimize(state, depth, agent_index)

    def minimize(self, state, depth, agent_index):
        min_score = float('inf')
        min_action = None

        for action in state.getLegalActions(agent_index):
            successor = state.generateSuccessor(agent_index, action)
            if agent_index == state.getNumAgents() - 1:
                new_score = self.minimaxAlgo(successor, depth - 1, 0)[0]
            else:
                new_score = self.minimaxAlgo(successor, depth, agent_index + 1)[0]

            if new_score < min_score:
                min_score = new_score
                min_action = action

        return min_score, min_action

    def maximize(self, state, depth, agent_index):
        max_score = float("-inf")
        max_action = None

        for action in state.getLegalActions(agent_index):
            successor = state.generateSuccessor(agent_index, action)
            new_score = self.minimaxAlgo(successor, depth, agent_index + 1)[0]

            if new_score > max_score:
                max_score = new_score
                max_action = action

        return max_score, max_action



    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.minimaxAlgo(gameState, self.depth, 0)[1]
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def minimaxAlphaBetaAlgo(self, state, depth, agent_index, alpha, beta):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state), None
        elif agent_index == 0:
            return self.maximize(state, depth, agent_index, alpha, beta)
        else:
            return self.minimize(state, depth, agent_index, alpha, beta)

    def minimize(self, state, depth, agent_index, alpha, beta):
        min_score = float('inf')
        min_action = None

        for action in state.getLegalActions(agent_index):
            successor = state.generateSuccessor(agent_index, action)
            if agent_index == state.getNumAgents() - 1:
                new_score = self.minimaxAlphaBetaAlgo(successor, depth - 1, 0, alpha, beta)[0]
            else:
                new_score = self.minimaxAlphaBetaAlgo(successor, depth, agent_index + 1, alpha, beta)[0]

            if new_score < min_score:
                min_score = new_score
                min_action = action

            if new_score < alpha:
                return new_score, action
            beta = min(beta, min_score)

        return min_score, min_action

    def maximize(self, state, depth, agent_index, alpha, beta):
        max_score = float("-inf")
        max_action = None

        for action in state.getLegalActions(agent_index):
            successor = state.generateSuccessor(agent_index, action)
            new_score = self.minimaxAlphaBetaAlgo(successor, depth, agent_index + 1, alpha, beta)[0]

            if new_score > max_score:
                max_score = new_score
                max_action = action

            if new_score > beta:
                return new_score, action
            alpha = max(alpha, max_score)

        return max_score, max_action

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.minimaxAlphaBetaAlgo(gameState, self.depth, 0, float("-inf"), float("inf"))[1]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimaxAlgo(self, state, depth, agent_index):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state), None
        elif agent_index == 0:
            return self.maximize(state, depth, agent_index)
        else:
            return self.expectation(state, depth, agent_index)

    def expectation(self, state, depth, agent_index):
        exp_score = 0
        exp_action = None
        for action in state.getLegalActions(agent_index):
            successor = state.generateSuccessor(agent_index, action)
            if agent_index == state.getNumAgents() - 1:
                new_score = self.expectimaxAlgo(successor, depth - 1, 0)[0]
                exp_score += new_score
            else:
                new_score = self.expectimaxAlgo(successor, depth, agent_index + 1)[0]
                exp_score += new_score
        exp_score /= len(state.getLegalActions(agent_index))

        return exp_score, exp_action

    def maximize(self, state, depth, agent_index):
        max_score = float("-inf")
        max_action = None

        for action in state.getLegalActions(agent_index):
            successor = state.generateSuccessor(agent_index, action)
            new_score = self.expectimaxAlgo(successor, depth, agent_index + 1)[0]

            if new_score > max_score:
                max_score = new_score
                max_action = action

        return max_score, max_action
    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectimaxAlgo(gameState, self.depth, 0)[1]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
