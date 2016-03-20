# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


# adapted from https://stackoverflow.com/questions/2467590/dynamically-evaluating-simple-boolean-logic-in-python


def create_token_lst(s, str_to_token):
    """create token list:
    'True or False' -> [True, lambda..., False]"""
    s = s.replace('(', ' ( ')
    s = s.replace(')', ' ) ')

    return [str_to_token[it] for it in s.split()]


def find(lst, what, start=0):
    return [i for i,it in enumerate(lst) if it == what and i >= start]


def parens(token_lst):
    """returns:
        (bool)parens_exist, left_paren_pos, right_paren_pos
    """
    left_lst = find(token_lst, '(')

    if not left_lst:
        return False, -1, -1

    left = left_lst[-1]

    #can not occur earlier, hence there are args and op.
    right = find(token_lst, ')', left + 4)[0]

    return True, left, right


def bool_eval(token_lst):
    """token_lst has length 3 and format: [left_arg, operator, right_arg]
    operator(left_arg, right_arg) is returned"""
    return token_lst[1](token_lst[0], token_lst[2])


def formatted_bool_eval(token_lst, empty_res=True):
    """eval a formatted (i.e. of the form 'ToFa(ToF)') string"""
    if not token_lst:
        return True

    if len(token_lst) == 1:
        return token_lst[0]

    has_parens, l_paren, r_paren = parens(token_lst)

    if not has_parens:
        return bool_eval(token_lst)

    token_lst[l_paren:r_paren + 1] = [bool_eval(token_lst[l_paren+1:r_paren])]

    return formatted_bool_eval(token_lst)


class LogicParser(object):
    def __init__(self, tokens):
        self.str_to_token = {'True':True,
                            'False':False,
                            'and':lambda left, right: left and right,
                            'or':lambda left, right: left or right,
                            '(':'(',
                            ')':')'}
        self.str_to_token.update(tokens)

    def __call__(self, expr):
        """The actual 'eval' routine,
        if 'expr' is empty, 'True' is returned,
        otherwise 'expr' is evaluated according to parentheses nesting.
        The format assumed:
            [1] 'LEFT OPERATOR RIGHT',
            where LEFT and RIGHT are either:
                    True or False or '(' [1] ')' (subexpression in parentheses)
        """
        token_list = create_token_lst(expr, str_to_token=self.str_to_token)
        return formatted_bool_eval(token_list)

