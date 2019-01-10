import json
import string


class Registers:
    REG_NAME = ['t0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 
        't8', 't9', 't10', 't11', 't12', 't13', 't14', 't15']
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.register = {}
        for reg in Registers.REG_NAME:
            self.register[reg] = ''
    
    def clear(self, reg_id):
        self.register[reg_id] = ''
    
    def get(self, reg_id):
        return self.register.get(reg_id, '')
    
    def save(self, reg_id, value):
        self.register[reg_id] = value
        print('\t%s = %s' % (reg_id, value))
        return reg_id
    
    def find(self, _value):
        for reg_id, value in self.register.items():
            if value == _value:
                return reg_id
        return False
    
    def find_empty(self):
        for reg_id, value in self.register.items():
            if not value:
                return reg_id
        raise Exception('No empty register.')
reg = Registers()


class CharSet:
    LEGAL_CHAR = string.digits + string.ascii_letters
    FACTOR_OP = ['+', '-', '*', '/']
    STOP_CHAR = [';']


class Factors:
    def __init__(self, expr):
        factors = []

        _tmp = ''
        for char in expr:
            if char in CharSet.FACTOR_OP:
                if _tmp:
                    factors.append(_tmp)
                    _tmp = ''
                factors.append(char)
            elif char in CharSet.LEGAL_CHAR:
                _tmp += char
            elif char == ' ':
                if _tmp:
                    factors.append(_tmp)
                    _tmp = ''
                continue
            elif char in CharSet.STOP_CHAR:
                if _tmp:
                    factors.append(_tmp)
                    _tmp = ''
                break
        self.factors = factors
    
    def __str__(self):
        return json.dumps(self.factors)


class ExprTree:
    def __init__(self, op, factor1, factor2):
        self.op = op
        self.factor1 = factor1.data if isinstance(factor1, ExprTree) else factor1
        self.factor2 = factor2.data if isinstance(factor2, ExprTree) else factor2

        self.data = {
            'op': self.op,
            'f1': self.factor1,
            'f2': self.factor2,
        }
    
    def __str__(self):
        return json.dumps(self.data, indent=2)


def _check_factor(factor):
    if isinstance(factor, ExprTree):
        return True
    for i in factor:
        if i not in CharSet.LEGAL_CHAR:
            return False
    return True


def _compile(expr_list):
    def raise_exception():
        raise Exception('Error when compile %s' % str(expr_list))

    while(True):
        _len = len(expr_list)
        if _len == 1:
            if _check_factor(expr_list[0]):
                return expr_list[0]
            raise_exception()
        elif _len == 3:
            if expr_list[0] in CharSet.FACTOR_OP and _check_factor(expr_list[1]) and _check_factor(expr_list[2]):
                return ExprTree(*expr_list)
            raise_exception()
        else:
            for pointer in range(_len - 2):
                if expr_list[pointer] in CharSet.FACTOR_OP:
                    if _check_factor(expr_list[pointer + 1]) and _check_factor(expr_list[pointer + 2]):
                        expr_list = \
                            expr_list[:pointer] + \
                            [_compile(expr_list[pointer:pointer + 3])] + \
                            expr_list[pointer + 3:]
                        break
            else:
                raise_exception()


def compile(expr):
    print('Compiling expr: "%s"' % expr)
    _factors = Factors(expr)
    if len(_factors.factors) % 2 != 1:
        raise Exception('The number of factors must be an odd number.')
    res = _compile(_factors.factors)
    # print(res)
    return res


def _transfer(factor, op):
    if isinstance(factor, dict):
        return transfer(factor, op)

    return factor


def transfer(compile_res, op=None):
    _op = compile_res.get('op')
    _f1 = _transfer(compile_res.get('f1'), _op)
    _f2 = _transfer(compile_res.get('f2'), _op)

    format = '%s %s %s'
    if op is not None:
        if CharSet.FACTOR_OP.index(op) // 2 > CharSet.FACTOR_OP.index(_op) // 2:
            format = '(%s %s %s)'
    return format % (_f1, _op, _f2)


def analyse(compile_res):
    if isinstance(compile_res, dict):
        _op = compile_res.get('op')
        _f1 = compile_res.get('f1')
        _f2 = compile_res.get('f2')

        reg1 = analyse(_f1)
        reg2 = analyse(_f2)

        print('\t%s %s= %s' % (reg1, _op, reg2))

        reg.clear(reg2)
        return reg1
    
    return reg.save(reg.find_empty(), compile_res)


def expression():
    expr = ''
    expr = '- / +1 * a1 a2 b1 4;'
    expr = '+ - - + a b * + a c d * e f g;'
    while (True):
        if ';;' in expr:    
            break

        if ';' in expr:
            try:
                compile_res = compile(expr[:1 + expr.index(';')])
                # print(compile_res)
                transfer_res = transfer(compile_res.data)
                print('Transfer infex result: "%s"' % transfer_res)

                res_reg = analyse(compile_res.data)
                print('Result register is: "%s"' % res_reg)
                reg.reset()

                expr = expr[1 + expr.index(';'):]
            except Exception as e:
                print(e)
                print('Error happened! Reset the expression.')
                expr = ''
        
        expr += input('Please input affix expression end with ";" and exit the program with ";;" :\n')


def main():
    expression()

if __name__ == '__main__':
    main()
            
