""" Tree used to represent functions """

FUNCTION_NODE=0 # Node with a function, like sum and mul
CONSTANT_NODE=1 # Node with a constant, like a real number
VAR_NODE=2 # Node with a reference to a variable (based on variables array index)

class Tree:
    def __init__(self, node_type, node_value, lchild=None, rchild=None):
        self.node_type = node_type
        self.node_value = node_value

        self.lchild = lchild
        self.rchild = rchild
    
    def evaluate(self, variables):
        if self.node_type == CONSTANT_NODE:
            return self.node_value
        elif self.node_type == VAR_NODE:
            return variables[self.node_value]
        elif self.node_type == FUNCTION_NODE:
            lvalue = self.lchild.evaluate(variables)
            rvalue = self.rchild.evaluate(variables)
            return self.node_value(lvalue, rvalue)
        else:
            raise ValueError()
