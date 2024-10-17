import sys
import os
from typing import List

def define_ast(output_dir: str, base_name: str, types: List[str]):
    path = os.path.join(output_dir, base_name + '.py')
    
    with open(path, 'w', encoding='utf-8') as writer:
        if base_name != 'Expr':
            writer.write('import Expr\n')
            
        writer.write(f'from tokens import Tokens\n')
        writer.write(f'from typing import Any, Union\n') 
        writer.write(f'from abc import ABC, abstractmethod\n\n')
        writer.write(f'class {base_name}(ABC):\n')
        writer.write(f'\t@abstractmethod\n')
        writer.write(f'\tdef accept(self, visitor: "Any") -> str:\n')
        writer.write(f'\t\tpass\n') 

        for type_def in types:
            class_name, fields = map(str.strip, type_def.split(':'))
            define_type(writer, base_name, class_name, fields)
        writer.close()

def define_type(writer, base_name: str, class_name: str, field_list: str):
    writer.write(f'class {class_name}({base_name}):\n')
    fields = field_list.split(', ')
    args = ', '.join(f'{field.split(" ")[0].lower()}: {str(field.split(" ")[1])}' for field in fields)
    writer.write(f'\tdef __init__(self, {args}):\n')
    for field in fields:
        name = field.split(' ')[0].lower()   
        writer.write(f'\t\tself.{name} = {name}\n')
    
    writer.write('\n')
    
    # Define the accept method
    writer.write(f'\tdef accept(self, visitor: "Any")-> str:\n')
    writer.write(f'\t\treturn visitor.visit_{class_name.lower()}(self)\n') 
    writer.write('\n')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stdout.write('Usage: generate_ast <output directory>\n')
        sys.exit(64)
    
    directory = sys.argv[1]
    # generates expression types 
    # define_ast(directory, 'Expr', [
    #     'Binary   : LEFT Union[Expr,None], OPERATOR Tokens, RIGHT Union[Expr,None]',
    #     'Grouping : EXPRESSION Union[Expr,None]',
    #     'Literal  : VALUE Any', 
    #     'Unary    : OPERATOR Tokens, RIGHT Union[Expr,None]'
    # ])
    # generates statements
    define_ast(directory, "Stmt", [
        "Expression: Expression Expr.Expr",
        "Print : Expression Expr.Expr"
    ])
