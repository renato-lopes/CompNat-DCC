""" Tree used to represent functions """

FUNCTION_NODE=0 # Node with a function, like sum and mul
CONSTANT_NODE=1 # Node with a constant, like a real number
VAR_NODE=2 # Node with a reference to a variable (based on variables array index)

LEFT_CHILD=0
RIGHT_CHILD=1

class Tree:
    def __init__(self, node_type, node_value, parent=None, lchild=None, rchild=None):
        self.node_type = node_type
        self.node_value = node_value

        self.parent = parent
        self.lchild = lchild
        self.rchild = rchild
    
    def set_left_child(self, node):
        self.lchild = node
        node.parent = (self, LEFT_CHILD)

    def set_right_child(self, node):
        self.rchild = node
        node.parent = (self, RIGHT_CHILD)

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

    def height(self):
        if self.node_type == CONSTANT_NODE or self.node_type == VAR_NODE:
            return 0
        else:
            return max(1+self.lchild.height(), 1+self.rchild.height())

    def tostring(self, level=0):
        rep = '\t'*level
        if self.node_type == FUNCTION_NODE:
            rep += str(self.node_value)+"\n"
            rep += self.lchild.tostring(level+1)
            rep += self.rchild.tostring(level+1)
        else:
            if self.node_type == VAR_NODE:
                rep += "var"
            rep += str(self.node_value)+"\n"
        return rep

    def get_nodes_at_level(self, nodes, level):
        if level == 0:
            nodes.append(self)
        elif self.node_type == FUNCTION_NODE:
            self.lchild.get_nodes_at_level(nodes, level-1)
            self.rchild.get_nodes_at_level(nodes, level-1)

    def copy(self):
        cp = Tree(self.node_type, self.node_value)
        if self.node_type == FUNCTION_NODE:
            cp.set_left_child(self.lchild.copy())
            cp.set_right_child(self.rchild.copy())
        return cp
