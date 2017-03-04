def evaluator(logicalExpresion):
    tokenizedExpression = filter(lambda x: x, logicalExpresion.replace(' ','').replace('&',"\0&\0").replace(')',"\0)\0").replace('(',"\0(\0").replace('|',"\0|\0").split("\0"))
    evalTree = posttotree(shuntingyard(tokenizedExpression))
    return lambda x: evalTree.evaluate(x)

def shuntingyard(tokenChain):
    stack = []
    queue = []
    for token in tokenChain:
        if token == "&" or token == "|":
            while stack and (stack[-1] == "&" or stack[-1] == "|"):
                queue.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            popped = stack.pop()
            while popped != '(':
                queue.append(popped)
                #try:
                popped = stack.pop()
                #except:
                #    raise("Mismatched Parenthesis)
        else:
            queue.append(token)
    while stack:
        queue.append(stack.pop())
    return queue

def posttotree(postfixChain):
    stack = []
    for token in postfixChain:
        if token == "&" or token == "|":
            e1 = stack.pop()
            e2 = stack.pop()
            t = Tree(token, e1, e2)
            stack.append(t)
        else:
            stack.append(Tree(token))
    return stack.pop()

def dictionaryeval(dictionary, token):
    if ':' in token:
        var, val = token.split(':')
        return var in dictionary and val in dictionary[var]
    else:
        return token in dictionary

class Tree:
    def __init__(self, root, lLeaf=None, rLeaf=None):
        self.root = root
        self.left = lLeaf
        self.right = rLeaf
    def evaluate(self, dictionary):
        if self.left:
            l = self.left.evaluate()
        else:
            return dictionaryeval(dictionary, self.root)
        if self.right:
            r = self.right.evaluate()
        if l and r:
            if token == '&':
                return l and r
            if token == '|':
                return l or r
    def __nonzero__(self):
        return bool(self.root)
    def show(self):
        if self.left:
            return '('+self.left.show()+str(self.root)+self.right.show()+')'
        else:
            return self.root
