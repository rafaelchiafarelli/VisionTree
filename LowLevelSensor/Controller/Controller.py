class Controller:
    def __init__(self, config):
        self.SetPoint = int(config['SetPoint'])
        self.LowPoint = int(config['LowPoint'])
        self.CurrentState = 0
        print("got here and it is happy: {}".format(self.SetPoint))
    
    def Control(self, temp):

        if temp > self.SetPoint:
            self.CurrentState = 1
            
        if temp < self.LowPoint:
            self.CurrentState = 0
        print("CurrentState {}".format(self.CurrentState))
        return self.CurrentState
        
