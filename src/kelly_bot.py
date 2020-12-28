import numpy as np



class Kelly_bot:



    def __init__(self,W0=1.0,r1=1.0,r2=-1.0,p0=None,dp0=None, strategy=None,lam=None):
        '''
        Parameters:
        p0: Initial coin bias
        dp0: Initial coin uncertainty 
        lambda: The aggressiveness of the agent
        '''

        self.p0 = p0
        self.dp0 = dp0
        self.W0 = W0 # The agents initial wealth
        self.r1 = r1
        self.r2 = r2

        self.W_vec = []
        self.dW_vec = []
        self.f_vec = []
        self.bet_vec = []
        self.p_vec = []
        self.dp_vec = []


        # Compute the alpha and beta paramters for the conjugate priors

        if p0 is None or (p0==0.0):
            self.alpha = 0.0
            self.beta = 0.0
            self.p1 = 0.0
            self.p2 = 0.0
            self.p_est = 0.0
            self.dp_est = 0.0
        else:
            self.alpha = p0*( (p0*(1.0-p0)/dp0**2) -1)
            self.beta = (1-p0)*( (p0*(1.0-p0)/dp0**2) -1)
            self.p_est = self.alpha/(self.alpha+self.beta)
            self.dp_est = np.sqrt(self.p_est*(1.0-self.p_est)/(self.alpha+self.beta+1))
            self.p1 = self.alpha/(self.alpha+self.beta)
            self.p2 = 1.0-self.p1

        # The agents memory
        self.N_heads = 0
        self.N_tails = 0
        self.data = []

        if lam is None:
            self.lam = 0.0
        else:
            self.lam = lam

        # Store information about the agents strategy
        if strategy is not None:
            self.strategy = strategy
            self.strategy_name = strategy['name']

        return None

    def reset(self):
        '''
        Reset the memory of the kelly-bot
        '''

        self.N_heads = 0
        self.N_tails = 0
        self.p_est = 0.0
        self.dp_est = 0.0
        self.p1 = 0.0
        self.p2 = 0.0

        self.data = []
        self.dp_vec = []
        self.p_vec = []
        self.W_vec = []
        self.bet_vec = []
        self.f_vec = []

        return None

    def posterior_distribution(self):
        '''
        This function returns the agents current belief about the coin probability
        as a continous distribution
        '''

        def f(x):

            y = (x**(self.N_heads+self.alpha-1))*((1.0-x)**(self.N_tails+self.beta-1))
            norm = 1.0

            y /= norm 

            return y


        return None

    def new_observation(self,obs):
        '''
        Observe a new data point and update all of the information

        '''

        # Add the new data to the agents memory
        self.data.append(obs)

        # Update the current estimate of p0 and its uncertainty
        self.N_heads += int(obs==1)
        self.N_tails += int(obs==0)

        # Update the mean value of the estimate
        self.p_est = (self.N_heads + self.alpha)/(self.N_heads+self.N_tails+self.alpha+self.beta)
        self.dp_est = np.sqrt(self.p_est*(1-self.p_est)/(self.alpha+self.beta+self.N_heads+self.N_tails+1))

        # Update the vector containing the estimates of the current values
        self.p_vec.append(self.p_est)
        self.dp_vec.append(self.dp_est)

        # New updated values
        self.p1 = self.p_est
        self.p2 = 1.0-self.p_est


        return None

    def update_wealth(self,result,wager):
        '''
        Update the agents wealth
        '''

        if result==1:
            dW = (wager/self.W0)
            self.W0+= wager
        elif result==0:
            dW = -1.0*(wager / self.W0)
            self.W0+= -1.0*wager

        if self.W0 <0:
            self.W0 = 0.0

        # Update the Agents wealth
        self.W_vec.append(self.W0)
        self.dW_vec.append(dW)

        return None


    def apply_strategy(self):
        '''

        '''

        if self.strategy_name == 'fixed_fraction':
            f,bet_amount = self.fixed_fraction(f_fixed=self.strategy['f_fixed'])
        elif self.strategy_name == 'fixed_bet':
            f,bet_amount = self.fixed_bet_size(bet_size=self.strategy['fixed_bet_size'])
        elif self.strategy_name == 'adaptive_kelly':
            f,bet_amount = self.kelly_bet_size(fraction=self.strategy['kelly_fraction'])

        return bet_amount

    def kelly_bet_size(self,fraction=1.0):
        '''
        Determine the optimal bet given all of the available information
        '''


        f = -(self.r1*self.p1+self.r2*self.p2)/(self.r1*self.r2)
        f += (self.lam/(1-self.lam))*((self.r1-self.r2)/(self.r1*self.r2))*self.dp_est
        f = fraction*f # Take a fraction of the kelly bet

        # Only Bet if the fraction is >0
        if f<0:
            f=0.0

        bet_amount = f*self.W0 # The size of the wager

        self.f_vec.append(f)
        self.bet_vec.append(bet_amount)


        return f,bet_amount

    def fixed_bet_size(self,bet_size):
        '''
        Place a bet of fixed amount
        '''

        f = (bet_size/self.W0)

        self.f_vec.append(f)
        self.bet_vec(bet_size)

        return f, bet_size

    def fixed_fraction(self,f_fixed):
        '''
        Determine the optimal bet given all of the available information
        '''

        bet_amount = f_fixed*self.W0 # The size of the wager

        self.f_vec.append(f_fixed)
        self.bet_vec.append(bet_amount)


        return f_fixed,bet_amount
