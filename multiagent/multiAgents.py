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
from math import exp
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
        #sum all food manhattanDistance as as a single item.
        food_SumDistance = 0
        for food in newFood.asList():
            food_SumDistance += 1/manhattanDistance(newPos,food)
        #sum all GhostStatesDistance
        ghost_SumDistance = 0
        for ghost in newGhostStates:
            if ghost.scaredTimer == 0:
                ghost_SumDistance += 100*exp(-manhattanDistance(newPos, ghost.getPosition()))
        return successorGameState.getScore()+food_SumDistance-ghost_SumDistance+0.1*sum(newScaredTimes)

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
        def maximizer(state: GameState, depth, index_of_agent):
            maxiAction = None
            # condition for termination of recursive method calls
            def terminal_condition(state,depth):
                "*** YOUR CODE HERE ***"
                if depth == 0 or state.isLose() or state.isWin():
                    return True
                else:
                    return False
            if terminal_condition(state,depth) == True:
                return (self.evaluationFunction(state), None)
            # initialize value
            value = -float('inf')
            # for every legal action, update value and maxiAction
            "*** YOUR CODE HERE ***"
            for action in state.getLegalActions(index_of_agent):
                n_state = state.generateSuccessor(index_of_agent,action)
                tmp_value = minimizer(n_state,depth,index_of_agent+1)[0]
                if value < tmp_value:
                    value = tmp_value
                    maxiAction = action
            return (value, maxiAction)
        def minimizer(state: GameState, depth, index_of_agent):
            miniAction = None
            def terminal_condition(state,depth):
                "*** YOUR CODE HERE ***"
                if state.isLose() or state.isWin():
                    return True
                else:
                    return False
            if terminal_condition(state,depth) == True:
                return (self.evaluationFunction(state), miniAction)
            # initialize value
            value = float('inf')
            # for every legal action, update value and miniAction
            "*** YOUR CODE HERE ***"
            for action in state.getLegalActions(index_of_agent):
                n_state = state.generateSuccessor(index_of_agent,action)[0]
                if index_of_agent+1 == gameState.getNumAgents():
                    tmp_value = maximizer(n_state,depth-1,0)
                else:
                    tmp_value = minimizer(n_state,depth,index_of_agent+1)[0]
                if value > tmp_value:
                    value = tmp_value
                    miniAction = action
            return (value, miniAction)      
        action = maximizer(gameState, self.depth, 0)[1]
        return action
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maximizer(state: GameState, depth, index_of_agent, alpha, beta):
            maxiAction = None
            #condition for termination of recursive method calls
            def terminal_condition(state,depth):
                "*** YOUR CODE HERE ***"
                if depth == 0 or state.isLose() or state.isWin():
                    return True
                else:
                    return False  
            if terminal_condition(state,depth) == True:
                return (self.evaluationFunction(state), None)
            # initialize value
            value = -float('inf')
            # for every legal action, update value, maxiAction and alpha:
            "*** YOUR CODE HERE ***"
            for action in state.getLegalActions(index_of_agent):
                n_state = state.generateSuccessor(index_of_agent,action)
                tmp_value = minimizer(n_state,depth,index_of_agent+1,alpha,beta)[0]
                if tmp_value > beta:
                    return (tmp_value,action)
                elif value < tmp_value:
                    value = tmp_value
                    alpha = max(alpha,tmp_value)
                    maxiAction = action
            return (value, maxiAction)
        
        def minimizer(state:GameState, depth, index_of_agent, alpha, beta):
            miniAction = None
            def terminal_condition(state,depth):
                "*** YOUR CODE HERE ***"
                if state.isLose() or state.isWin():
                    return True
                else:
                    return False
            if terminal_condition(state,depth) == True:
                return (self.evaluationFunction(state), miniAction)
            # initialize value
            value = float('inf')
            # for every legal action, update value, miniAction and beta
            "*** YOUR CODE HERE ***"
            for action in state.getLegalActions(index_of_agent):
                n_state = state.generateSuccessor(index_of_agent,action)
                if index_of_agent+1 == gameState.getNumAgents():
                    tmp_value = maximizer(n_state,depth-1,0,alpha,beta)[0]
                else:
                    tmp_value = minimizer(n_state,depth,index_of_agent+1,alpha,beta)[0]
                if tmp_value < alpha:
                    return (tmp_value,action)
                if value > tmp_value:
                    value = tmp_value
                    beta = min(beta,tmp_value)
                    miniAction = action
            return (value, miniAction)   
        # initialize alpha/beta
        alpha =  -float('inf')
        beta = float('inf')
        action = maximizer(gameState, self.depth, 0, alpha, beta)[1]
        return action 

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
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
