# reg -> term  reg'
# reg' -> '|' term reg' | epsilon
# term -> kleene term'
# term' -> kleene term' | epsilon
# kleene -> fac kleene' 
# kleene' -> * kleene' | epsilon
# fac -> alpha | epsilon | '(' reg ')'
# alpha -> 'a' - 'z' | 'A' - 'Z' | '0' - '9'
# epsilon -> '!'
from graphviz import Graph

import json
import string

class Node:
    def __init__(self, name=None, left=None, right=None):
        self.left = left
        self.right = right
        self.name = name
    
    # Simplify node
    def simplify(self):
        # Shorten name
        if len(self.name) > 1 and self.name != 'root':
            self.name = '.'
        # Cut epsilon
        child = self.left
        if child and child.left and child.right:
            if child.left.name == 'ε':
                if child.name in '*|':
                    child.left = None
                else:
                    self.left = child.right
                return self.simplify()
            if child.right.name == 'ε':
                if child.name in '*|':
                    child.right = None
                else:
                    self.left = child.left
                return self.simplify()
        child = self.right
        if child and child.left and child.right:
            if child.left.name == 'ε':
                if child.name in '*|':
                    child.left = None
                else:
                    self.right = child.right
                return self.simplify()
            if child.right.name == 'ε':
                if child.name in '*|':
                    child.right = None
                else:
                    self.right = child.left
                return self.simplify()
        # Recursive
        if self.left:
            self.left.simplify()
        if self.right:
            self.right.simplify()

    # Tansfer the tree to dictionary
    def display(self):
        if self.left is None and self.right is None:
            return self.name
        return {
            'left': self.left.display() if self.left else None,
            'right': self.right.display() if self.right else None,
            'name': self.name,
        }
    
    # Draw the tree by graphviz
    def draw(self, graph=None, node_num=0):
        output = False
        if graph is None:
            graph = Graph(format='png')
            output = True

        graph_id = str(node_num)
        node_num += 1

        graph.node(graph_id, label=self.name)

        if self.left:
            left_id, node_num = self.left.draw(graph, node_num)
            graph.edge(graph_id, left_id)
        if self.right:
            right_id, node_num = self.right.draw(graph, node_num)
            graph.edge(graph_id, right_id)
        
        if output:
            graph.render('output')
        
        return graph_id, node_num
    
    def dump(self, father=None):
        if self.name == 'root':
            return '%s%s' % (self.left.dump(self), self.right.dump(self))
        if self.name == '*':
            inst = self.left if self.left else self.right
            return '%s*' % inst.dump(self)
        if self.name == '.':
            if father and father.name in '*':
                return '(%s%s)' % (self.left.dump(self), self.right.dump(self))
            return '%s%s' % (self.left.dump(self), self.right.dump(self))
        if self.name == '|':
            if father and father.name in '*.':
                return '(%s|%s)' % (self.left.dump(self), self.right.dump(self))
            return '%s|%s' % (self.left.dump(self), self.right.dump(self))
        return self.name


class Parser:
    def __init__(self, regular):
        self.regular = regular
        self.pointer = 0
    
    def reg(self):
        return self.reg_prime(self.term())
    
    def reg_prime(self, father):
        if self.this_char() == '|':
            self.add()
            return self.reg_prime(Node('|', father, self.term()))
        return father

    def term(self):
        return self.term_prime(self.kleene())
    
    def term_prime(self, father):
        if self.this_char() in string.digits + string.ascii_letters + '(*':
            return self.term_prime(Node('term_prime', father, self.kleene()))
        return father
    
    def kleene(self):
        return self.kleene_prime(self.fac())
    
    def kleene_prime(self, father):
        if self.this_char() == '*':
            self.add()
            return Node('*', father, self.epsilon())
        return father
    
    def fac(self):
        this_char = self.this_char()
        if this_char in string.digits + string.ascii_letters:
            self.add()
            return Node(this_char)
        if this_char == '(':
            self.add()
            _node = self.reg()
            if self.this_char() == ')':
                self.add()
            else:
                raise Exception('Parentness not closed')
            return _node
        return self.epsilon()
    
    def epsilon(self):
        return Node('ε')
    
    def this_char(self):
        if self.pointer == len(self.regular):
            return '$'
        return self.regular[self.pointer]
    
    def add(self):
        if self.pointer < len(self.regular):
            self.pointer += 1
            return True
        return False


def main():
    regular = input('Please input the regular expression.\n')

    parser = Parser(regular)
    res = Node('root', parser.reg(), Node('$'))
    # Simplify the syntax tree
    print('Execute succeed. Simplifying...')
    res.simplify()
    # graph_dict = res.display()
    # print(json.dumps(graph_dict, indent=2))

    # This function will render a picture named output.png
    print('Tree render succeed! Look at file \'output\' and \'output.png\'.')
    res.draw()
    print('This regular expression has been simplify which is without extra parentheses.')
    print(res.dump())


if __name__ == '__main__':
    main()
