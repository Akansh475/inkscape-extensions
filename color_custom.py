#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division

import ast
import operator as op

import coloreffect

# supported operators
operators = {ast.Add: op.add,
             ast.Sub: op.sub,
             ast.Mult: op.mul,
             ast.Div: op.truediv,
             ast.Pow: op.pow,
             ast.BitXor: op.xor,
             ast.USub: op.neg}


def eval_expr(expr, namespace):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """
    return eval_(ast.parse(expr, mode='eval').body, namespace)


def eval_(node, namespace):
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.Name):  # <variable> (must be in namespace)
        return namespace[node.id]
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left, namespace), eval_(node.right, namespace))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand, namespace))
    else:
        raise TypeError(node)


class C(coloreffect.ColorEffect):
    def __init__(self):
        super(C, self).__init__()
        self.arg_parser.add_argument("-r", "--r",
                                     dest="rFunction", default="r",
                                     help="red channel function")
        self.arg_parser.add_argument("-g", "--g",
                                     dest="gFunction", default="g",
                                     help="green channel function")
        self.arg_parser.add_argument("-b", "--b",
                                     dest="bFunction", default="b",
                                     help="blue channel function")
        self.arg_parser.add_argument("-t", "--tab",
                                     help="The selected UI-tab when OK was pressed")
        self.arg_parser.add_argument("-s", "--scale",
                                     type=float, default=1,
                                     help="The input (r,g,b) range")

    def normalize(self, v):
        if v < 0:
            return 0
        if v > self.options.scale:
            return self.options.scale
        return v

    def _hexstr(self, r, g, b):
        return '{:02x}{:02x}{:02x}'.format(int(round(r)), int(round(g)), int(round(b)))

    def colmod(self, _r, _g, _b):
        factor = 255 / self.options.scale
        r = _r / factor
        g = _g / factor
        b = _b / factor

        # add stuff to be accessible from within the custom color function here.
        safe_namespace = {'r': r, 'g': g, 'b': b}

        r2 = self.normalize(eval_expr(self.options.rFunction.strip(), safe_namespace))
        g2 = self.normalize(eval_expr(self.options.gFunction.strip(), safe_namespace))
        b2 = self.normalize(eval_expr(self.options.bFunction.strip(), safe_namespace))
        return self._hexstr(r2 * factor, g2 * factor, b2 * factor)


if __name__ == '__main__':
    c = C()
    c.run()
