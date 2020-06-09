class User(object):

    def __init__(self,id):
        self.id = id
        self.type = 'Anon'
        self.state = 'Main'
        self.prevState = 'Main'
        self.group = 'none'
        
    def setParam(self,group,type_,state):
        self.group = group
        self.type = type_
        self.state = state
