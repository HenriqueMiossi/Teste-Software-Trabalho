# Round up
class CompoundInterest:
    def __init__(self, principal, interest_rate, time):
        self.p = principal
        # self.m_c = mon_contribution
        self.r = interest_rate
        self.t = time
        self.result = self.p * ((1 + self.r / 100) ** self.t - 1)
