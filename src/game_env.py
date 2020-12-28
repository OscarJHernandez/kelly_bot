import src.kelly_bot as kelly
import numpy as np


class Game_env:
    '''
    This Class will be used to instantiate many kelly-bots for testing purposes
    '''


    def __init__(self,p0,kelly_bots=None):
        '''
        Instantiate the game environment.
        '''

        self.kelly_bots = kelly_bots
        self.p0 = p0

        return None

    def simulate_game(self, N_rounds =100):

        for t in range(N_rounds):

            # Make the bets for all of the Kelly-bots
            bet = [self.kelly_bots[i].apply_strategy() for i in range(len(self.kelly_bots)) ]

            # Flip the coin
            c = np.random.binomial(n=1, p=self.p0)

            for i in range(len(self.kelly_bots)):
                self.kelly_bots[i].new_observation(obs=c)
                self.kelly_bots[i].update_wealth(c, bet[i])

        return self.kelly_bots

    def simulate_N_games(self,N_rounds=100,N_games=5000):
        '''
        Simulate N_games and collect statistics
        '''

        W_bots_final = np.zeros((N_games, len(self.kelly_bots)))

        for g in range(N_games):

            # Reset all of the kelly bots
            for i in range(len(self.kelly_bots)):
                self.kelly_bots[i].reset()

            # Simulate the game for all the kelly bots
            kelly_bots = self.simulate_game(N_rounds=N_rounds)


        return None


    def begin_interactive(self, Nrounds=50):
        '''

        Begin an interactive game with a player vs Kelly-bot

        '''

        string = '''
        Hello human! You have chosen to play against a Kelly-bot in a Coin-betting game. 
        The Bias of the coin is unknown... Are you
        '''

        print(string)

        game_ongoing = True
        W0 = 1.0 # The initial wealth
        p_coin = np.random.rand() # Choose a random bias for the coin

        round = 0

        while game_ongoing and (round < Nrounds):
            print('='*100)
            print('Current round: {}'.format(round))
            print('Current wealth: W={}'.format(W0))
            print('Kelly bots wealth: W={}'.format(W0))
            print('Question: How much do you wager on the coin? ')

            print('Remark: The Kelly bot wagers={}')

            # Flip the coin
            c=0.0
            print('Coin-flip: ={}'.format(c))

            if c==0:
                W0+= -wager
            else:
                W0+= wager




        return None