from tokens import Tokens
from error import RuntimeException
class Env:
    def __init__(self):
        self.values =  {}
    def define(self, name: str, value: object):
        self.values[name] = value
        print(self.values)

    def get(self, name: Tokens):
        if name.lexme in self.values:
            return self.values[name.lexme]
        raise RuntimeException(name, f'Undefined variable "{name.lexme}".')
    
    def assign(self, name: Tokens, value: object):
        print(f' yo mama{name.lexme}')
        print(f'{self.values}')
        if name.lexme in self.values:
            self.values[name.lexme] = value 
            print('success')
            print(self.values)
            return 
        raise RuntimeException(name,f'Undefined Variable "{name.lexme}".')
    
    

