from hy.core.language import drop, drop_last, first, gensym, interleave, is_empty, last, name, reduce, repeat, rest, second
from hy import HyDict, HyExpression, HyKeyword, HyList, HyString, HySymbol
from hy.core.shadow import hyx_or
import hy
import hy.extra.reserved
import ast
import re
import argparse
from hy.contrib.hy_repr import hy_repr
import hy
hy.macros.macro('list-comp')(lambda hyx_XampersandXname, el, lis, test=None:
    HyExpression([] + [HySymbol('lfor')] + [first(lis)] + [second(lis)] + [
    el]) if test is None else HyExpression([] + [HySymbol('lfor')] + [first
    (lis)] + [second(lis)] + [HyKeyword('if')] + [test] + [el]))
import hy
hy.macros.macro('set-comp')(lambda hyx_XampersandXname, el, lis, test=None:
    HyExpression([] + [HySymbol('sfor')] + [first(lis)] + [second(lis)] + [
    el]) if test is None else HyExpression([] + [HySymbol('sfor')] + [first
    (lis)] + [second(lis)] + [HyKeyword('if')] + [test] + [el]))
import hy
hy.macros.macro('dict-comp')(lambda hyx_XampersandXname, el, lis, test=None:
    HyExpression([] + [HySymbol('dfor')] + [first(lis)] + [second(lis)] + [
    el]) if test is None else HyExpression([] + [HySymbol('dfor')] + [first
    (lis)] + [second(lis)] + [HyKeyword('if')] + [test] + [el]))
import hy
hy.macros.tag('A')(lambda expr: HyExpression([] + [HySymbol('if')] + [
    HyExpression([] + [HySymbol('is')] + [HySymbol('None')] + [expr])] + [
    HyList([])] + [expr]))


def add(x, y):
    return x + y


def expand_form(x):
    return x.expand() if hasattr(x, 'expand'
        ) else None if None is x else hy.models.HyInteger(x) if int == type(x
        ) else hy.models.HyFloat(x) if float == type(x
        ) else hy.models.HyComplex(x) if complex == type(x
        ) else hy.models.HySymbol(hy.models.HySymbol(str(x))) if bool == type(x
        ) else hy.models.HyList(x) if list == type(x) else hy.models.HyBytes(x
        ) if bytes == type(x) else hy.models.HySymbol(x)


def do_if_long(l):
    l = list(l)
    return first(l) if 1 == len(l) else HyExpression([] + [HySymbol('do')] +
        list(([] if None is l else l) or []))


hy_reserved_keywords = HyList([] + [HySymbol('fn')] + [HySymbol('defn')] +
    [HySymbol('defclass')] + [HySymbol('cond')])


def py2hy_mangle_identifier(x):
    return hy.models.HySymbol(x + '_py2hy_mangling'
        ) if x in hy_reserved_keywords else x


import hy
hy.macros.tag('l')(lambda body: HyExpression([] + [HySymbol(
    'hy.models.HyList')] + [HyExpression([] + [HySymbol('list')] + [
    HyExpression([] + [HySymbol('map')] + [HySymbol('expand-form')] + [body
    ])])]))
import hy
hy.macros.tag('e')(lambda x: HyExpression([] + [HySymbol('expand-form')] + [x])
    )
import hy
hy.macros.tag('k')(lambda key: HyExpression([] + [HySymbol('.')] + [
    HySymbol('self')] + [key]))
import hy
hy.macros.macro('defsyntax')(lambda hyx_XampersandXname, name, keys, *body:
    HyExpression([] + [HySymbol('do')] + [HyExpression([] + [HySymbol(
    'when')] + [HyExpression([] + [HySymbol('hasattr')] + [HySymbol('ast')] +
    [HyExpression([] + [HySymbol('quote')] + [name])])] + [HyExpression([] +
    [HySymbol('setv')] + [HyExpression([] + [HySymbol('.')] + [HyExpression
    ([] + [HySymbol('.')] + [HySymbol('ast')] + [name])] + [HySymbol(
    'expand')])] + [HyExpression([] + [HySymbol('fn')] + [HyList([] + [
    HySymbol('self')])] + list(([] if None is body else body) or []))])])]))
import hy
hy.macros.macro('defconstantexpression')(lambda hyx_XampersandXname, *
    transformdicts: HyExpression([] + [HySymbol('do')] + list(reduce(lambda
    x, y: x + y, map(lambda transformdict: HyList([] + list([HyExpression([
    ] + [HySymbol('defsyntax')] + [hy.models.HySymbol(astname)] + [HyList([
    ])] + [HyString('Constant expression')] + [hysymbol]) for [astname,
    hysymbol] in transformdict.items()] or [])), transformdicts)) or [])))
if hasattr(ast, HySymbol('Module')):

    def _hy_anon_var_5(self):
        """Args:
      body (stmt*) [list]"""
        bodylist = hy.models.HyList(list(map(expand_form, self.body)))
        body = iter(bodylist)
        n = first(body)
        r = HyList([] + [HyExpression([] + [HySymbol('defclass')] + [
            HySymbol('Py2HyReturnException')] + [HyList([] + [HySymbol(
            'Exception')])] + [HyExpression([] + [HySymbol('defn')] + [
            HySymbol('__init__')] + [HyList([] + [HySymbol('self')] + [
            HySymbol('retvalue')])] + [HyExpression([] + [HySymbol('setv')] +
            [HySymbol('self.retvalue')] + [HySymbol('retvalue')])])])]
            ) if 'Py2HyReturnException' in bodylist.__repr__() else None
        return HyExpression([] + [HySymbol('do')] + list(([] if None is (
            HyList([] + [n] + list(([] if None is r else r) or [])) if hy.
            models.HyExpression == type(n) and HySymbol('import') == first(
            n) else HyList([] + list(([] if None is r else r) or []) + [n])
            ) else HyList([] + [n] + list(([] if None is r else r) or [])) if
            hy.models.HyExpression == type(n) and HySymbol('import') ==
            first(n) else HyList([] + list(([] if None is r else r) or []) +
            [n])) or []) + list(([] if None is body else body) or []))
    ast.Module.expand = _hy_anon_var_5
    _hy_anon_var_6 = None
else:
    _hy_anon_var_6 = None
if hasattr(ast, HySymbol('Interactive')):

    def _hy_anon_var_7(self):
        """Args:
      body (stmt*) [list]"""
        return None
    ast.Interactive.expand = _hy_anon_var_7
    _hy_anon_var_8 = None
else:
    _hy_anon_var_8 = None
if hasattr(ast, HySymbol('Expression')):

    def _hy_anon_var_9(self):
        """Args:
      body (expr)"""
        return None
    ast.Expression.expand = _hy_anon_var_9
    _hy_anon_var_10 = None
else:
    _hy_anon_var_10 = None
if hasattr(ast, HySymbol('Suite')):

    def _hy_anon_var_11(self):
        """Args:
      body (stmt*) [list]"""
        return None
    ast.Suite.expand = _hy_anon_var_11
    _hy_anon_var_12 = None
else:
    _hy_anon_var_12 = None
if hasattr(ast, HySymbol('FunctionDef')):

    def _hy_anon_var_13(self):
        """Args:
      name (identifier)
      args (arguments)
      body (stmt*) [list]
      decorator_list (expr*) [list]
      returns (expr?) [optional]
      lineno (int)
      col_offset (int)"""
        body = hy.models.HyList(list(map(expand_form, self.body)))
        decorator_list = hy.models.HyList(list(map(expand_form, self.
            decorator_list)))
        main_body = HyExpression([] + [HySymbol('defn')] + [
            py2hy_mangle_identifier(expand_form(self.name))] + [expand_form
            (self.args)] + list(([] if None is body else body) or [])
            ) if 'Py2HyReturnException' not in body.__repr__(
            ) else HyExpression([] + [HySymbol('defn')] + [
            py2hy_mangle_identifier(expand_form(self.name))] + [expand_form
            (self.args)] + list(([] if None is hy.models.HyList(list(map(
            expand_form, drop_last(1, self.body)))) else hy.models.HyList(
            list(map(expand_form, drop_last(1, self.body))))) or []) + [
            expand_form(last(self.body).value)]
            ) if 'Py2HyReturnException' not in list(drop_last(1, body)
            ).__repr__() and ast.Return == type(last(self.body)
            ) else HyExpression([] + [HySymbol('defn')] + [
            py2hy_mangle_identifier(expand_form(self.name))] + [expand_form
            (self.args)] + [first(body)] + [HyExpression([] + [HySymbol(
            'try')] + [do_if_long(rest(body))] + [HyExpression([] + [
            HySymbol('except')] + [HyList([] + [HySymbol('e')] + [HySymbol(
            'Py2HyReturnException')])] + [HySymbol('e.retvalue')])])]
            ) if hy.models.HyString == type(first(body)) else HyExpression(
            [] + [HySymbol('defn')] + [py2hy_mangle_identifier(expand_form(
            self.name))] + [expand_form(self.args)] + [HyExpression([] + [
            HySymbol('try')] + [do_if_long(body)] + [HyExpression([] + [
            HySymbol('except')] + [HyList([] + [HySymbol('e')] + [HySymbol(
            'Py2HyReturnException')])] + [HySymbol('e.retvalue')])])])
        return HyExpression([] + [HySymbol('with-decorator')] + list(([] if
            None is decorator_list else decorator_list) or []) + [main_body]
            ) if decorator_list else main_body
    ast.FunctionDef.expand = _hy_anon_var_13
    _hy_anon_var_14 = None
else:
    _hy_anon_var_14 = None
if hasattr(ast, HySymbol('AsyncFunctionDef')):

    def _hy_anon_var_15(self):
        """Args:
      name (identifier)
      args (arguments)
      body (stmt*) [list]
      decorator_list (expr*) [list]
      returns (expr?) [optional]
      lineno (int)
      col_offset (int)"""
        return None
    ast.AsyncFunctionDef.expand = _hy_anon_var_15
    _hy_anon_var_16 = None
else:
    _hy_anon_var_16 = None
if hasattr(ast, HySymbol('ClassDef')):

    def _hy_anon_var_17(self):
        """Args:
      name (identifier)
      bases (expr*) [list]
      keywords (keyword*) [list]
      body (stmt*) [list]
      decorator_list (expr*) [list]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('defclass')] + [
            py2hy_mangle_identifier(expand_form(self.name))] + [HyList([] +
            list(([] if None is hy.models.HyList(list(map(expand_form, self
            .bases))) else hy.models.HyList(list(map(expand_form, self.
            bases)))) or []))] + list(([] if None is hy.models.HyList(list(
            map(expand_form, self.body))) else hy.models.HyList(list(map(
            expand_form, self.body)))) or []))
    ast.ClassDef.expand = _hy_anon_var_17
    _hy_anon_var_18 = None
else:
    _hy_anon_var_18 = None
if hasattr(ast, HySymbol('Return')):

    def _hy_anon_var_19(self):
        """Args:
      value (expr?) [optional]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('raise')] + [HyExpression([] + [
            HySymbol('Py2HyReturnException')] + [expand_form(self.value)])])
    ast.Return.expand = _hy_anon_var_19
    _hy_anon_var_20 = None
else:
    _hy_anon_var_20 = None
if hasattr(ast, HySymbol('Delete')):

    def _hy_anon_var_21(self):
        """Args:
      targets (expr*) [list]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('del')] + list(([] if None is hy
            .models.HyList(list(map(expand_form, self.targets))) else hy.
            models.HyList(list(map(expand_form, self.targets)))) or []))
    ast.Delete.expand = _hy_anon_var_21
    _hy_anon_var_22 = None
else:
    _hy_anon_var_22 = None
if hasattr(ast, HySymbol('Assign')):

    def _hy_anon_var_26(self):
        """Args:
      targets (expr*) [list]
      value (expr)
      lineno (int)
      col_offset (int)"""
        targets = hy.models.HyList(list(map(expand_form, self.targets)))
        g = hy.models.HySymbol('_py2hy_anon_var_' + ''.join(drop(1, gensym()))
            ) if 1 < len(targets) or HySymbol(',') == first(first(targets)
            ) else expand_form(self.value)

        def _hy_anon_var_23(target, value):
            target = expand_form(target)
            return HyList([] + [HyExpression([] + [HySymbol('assoc')] + [
                target[1]] + [target[2]] + [value])])

        def _hy_anon_var_24(target, value):
            target = expand_form(target)
            return HyList([] + [HyExpression([] + [HySymbol('setv')] + [
                target] + [value])])

        def _hy_anon_var_25(target, value):
            target = expand_form(target)
            return HyList([] + [HyExpression([] + [HySymbol('do')])]
                ) if HySymbol('_') == target else HyList([] + [HyExpression
                ([] + [HySymbol('setv')] + [target] + [value])])
        typedict = {ast.Tuple: lambda target, value: reduce(add, map(lambda
            l: typedict[type(first(l))](first(l), second(l)), zip(target.
            elts, map(lambda t: HyExpression([] + [HySymbol('get')] + [
            second(t)] + [first(t)]), enumerate(repeat(value)))))), ast.
            Subscript: _hy_anon_var_23, ast.Attribute: _hy_anon_var_24, ast
            .Name: _hy_anon_var_25}
        ret = HyList([] + list(([] if None is ([HyExpression([] + [HySymbol
            ('setv')] + [g] + [expand_form(self.value)])] if 1 < len(
            targets) or HySymbol(',') == first(first(targets)) else None) else
            [HyExpression([] + [HySymbol('setv')] + [g] + [expand_form(self
            .value)])] if 1 < len(targets) or HySymbol(',') == first(first(
            targets)) else None) or []) + list(([] if None is reduce(add,
            map(lambda l: HyList([] + list(([] if None is typedict[type(
            first(l))](first(l), second(l)) else typedict[type(first(l))](
            first(l), second(l))) or [])), zip(self.targets, repeat(g)))) else
            reduce(add, map(lambda l: HyList([] + list(([] if None is
            typedict[type(first(l))](first(l), second(l)) else typedict[
            type(first(l))](first(l), second(l))) or [])), zip(self.targets,
            repeat(g))))) or []))
        ret = HyList([] + list(([] if None is [x for x in ret if not 
            HyExpression([] + [HySymbol('do')]) == x] else [x for x in ret if
            not HyExpression([] + [HySymbol('do')]) == x]) or []))
        return first(ret) if 1 == len(ret) else HyExpression([] + [HySymbol
            ('do')] + list(([] if None is ret else ret) or []))
    ast.Assign.expand = _hy_anon_var_26
    _hy_anon_var_27 = None
else:
    _hy_anon_var_27 = None
if hasattr(ast, HySymbol('AugAssign')):

    def _hy_anon_var_28(self):
        """Args:
      target (expr)
      op (operator)
      value (expr)
      lineno (int)
      col_offset (int)"""
        op2aug = {HySymbol('+'): HySymbol('+='), HySymbol('-'): HySymbol(
            '-='), HySymbol('*'): HySymbol('*='), HySymbol('/'): HySymbol(
            '/='), HySymbol('%'): HySymbol('%='), HySymbol('**'): HySymbol(
            '**='), HySymbol('<<'): HySymbol('<<='), HySymbol('>>'):
            HySymbol('>>='), HySymbol('|'): HySymbol('|='), HySymbol('^'):
            HySymbol('^='), HySymbol('//'): HySymbol('//='), HySymbol(
            'bitand'): HySymbol('&=')}
        return HyExpression([] + [op2aug[expand_form(self.op)]] + [
            expand_form(self.target)] + [expand_form(self.value)])
    ast.AugAssign.expand = _hy_anon_var_28
    _hy_anon_var_29 = None
else:
    _hy_anon_var_29 = None
if hasattr(ast, HySymbol('AnnAssign')):

    def _hy_anon_var_30(self):
        """Args:
      target (expr)
      annotation (expr)
      value (expr?) [optional]
      simple (int)
      lineno (int)
      col_offset (int)"""
        return None
    ast.AnnAssign.expand = _hy_anon_var_30
    _hy_anon_var_31 = None
else:
    _hy_anon_var_31 = None
if hasattr(ast, HySymbol('For')):

    def _hy_anon_var_32(self):
        """Args:
      target (expr)
      iter (expr)
      body (stmt*) [list]
      orelse (stmt*) [list]
      lineno (int)
      col_offset (int)"""
        target = expand_form(self.target)
        return HyExpression([] + [HySymbol('for')] + [HyList([] + list(([] if
            None is ([HyList([] + list(([] if None is rest(target) else
            rest(target)) or []))] if HySymbol(',') == first(target) else [
            target]) else [HyList([] + list(([] if None is rest(target) else
            rest(target)) or []))] if HySymbol(',') == first(target) else [
            target]) or []) + [expand_form(self.iter)])] + list(([] if None is
            hy.models.HyList(list(map(expand_form, self.body))) else hy.
            models.HyList(list(map(expand_form, self.body)))) or []))
    ast.For.expand = _hy_anon_var_32
    _hy_anon_var_33 = None
else:
    _hy_anon_var_33 = None
if hasattr(ast, HySymbol('AsyncFor')):

    def _hy_anon_var_34(self):
        """Args:
      target (expr)
      iter (expr)
      body (stmt*) [list]
      orelse (stmt*) [list]
      lineno (int)
      col_offset (int)"""
        return None
    ast.AsyncFor.expand = _hy_anon_var_34
    _hy_anon_var_35 = None
else:
    _hy_anon_var_35 = None
if hasattr(ast, HySymbol('While')):

    def _hy_anon_var_36(self):
        """Args:
      test (expr)
      body (stmt*) [list]
      orelse (stmt*) [list]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('while')] + [expand_form(self.
            test)] + list(([] if None is hy.models.HyList(list(map(
            expand_form, self.body))) else hy.models.HyList(list(map(
            expand_form, self.body)))) or []))
    ast.While.expand = _hy_anon_var_36
    _hy_anon_var_37 = None
else:
    _hy_anon_var_37 = None
if hasattr(ast, HySymbol('If')):

    def _hy_anon_var_38(self):
        """Args:
      test (expr)
      body (stmt*) [list]
      orelse (stmt*) [list]
      lineno (int)
      col_offset (int)"""
        orelseast = self.orelse
        orelse = hy.models.HyList(list(map(expand_form, orelseast)))
        body = hy.models.HyList(list(map(expand_form, self.body)))
        return HyExpression([] + [HySymbol('cond')] + [HyList([] + [
            expand_form(self.test)] + [do_if_long(body)])] + list(([] if 
            None is drop(1, body) else drop(1, body)) or [])) if HySymbol(
            'cond') == first(orelse) else HyExpression([] + [HySymbol(
            'cond')] + [HyList([] + [expand_form(self.test)] + [do_if_long(
            hy.models.HyList(list(map(expand_form, self.body))))])] + [
            HyList([] + [expand_form(first(orelseast).test)] + [do_if_long(
            hy.models.HyList(list(map(expand_form, first(orelseast).body)))
            )])] + [HyList([] + [HySymbol('True')] + [do_if_long(hy.models.
            HyList(list(map(expand_form, first(orelseast).orelse))))])]
            ) if len(orelseast) == 1 and type(first(orelseast)
            ) == ast.If else HyExpression([] + [HySymbol('if')] + [
            expand_form(self.test)] + [HyExpression([] + [HySymbol('do')] +
            list(([] if None is hy.models.HyList(list(map(expand_form, self
            .body))) else hy.models.HyList(list(map(expand_form, self.body)
            ))) or []))] + [HyExpression([] + [HySymbol('do')] + list(([] if
            None is orelse else orelse) or []))]) if orelse else HyExpression(
            [] + [HySymbol('when')] + [expand_form(self.test)] + list(([] if
            None is hy.models.HyList(list(map(expand_form, self.body))) else
            hy.models.HyList(list(map(expand_form, self.body)))) or []))
    ast.If.expand = _hy_anon_var_38
    _hy_anon_var_39 = None
else:
    _hy_anon_var_39 = None
if hasattr(ast, HySymbol('With')):

    def _hy_anon_var_41(self):
        """Args:
      items (withitem*) [list]
      body (stmt*) [list]
      lineno (int)
      col_offset (int)"""

        def nest_with(l):
            return hy.models.HyList(list(map(expand_form, self.body))
                ) if is_empty(l) else HyList([] + [HyExpression([] + [
                HySymbol('with')] + [HyList([] + list(([] if None is first(
                l) else first(l)) or []))] + list(([] if None is nest_with(
                list(drop(1, l))) else nest_with(list(drop(1, l)))) or []))])
        return first(nest_with(hy.models.HyList(list(map(expand_form, self.
            items)))))
    ast.With.expand = _hy_anon_var_41
    _hy_anon_var_42 = None
else:
    _hy_anon_var_42 = None
if hasattr(ast, HySymbol('AsyncWith')):

    def _hy_anon_var_43(self):
        """Args:
      items (withitem*) [list]
      body (stmt*) [list]
      lineno (int)
      col_offset (int)"""
        return None
    ast.AsyncWith.expand = _hy_anon_var_43
    _hy_anon_var_44 = None
else:
    _hy_anon_var_44 = None
if hasattr(ast, HySymbol('Raise')):

    def _hy_anon_var_45(self):
        """Args:
      exc (expr?) [optional]
      cause (expr?) [optional]
      lineno (int)
      col_offset (int)"""
        exc = expand_form(self.exc)
        return HyExpression([] + [HySymbol('raise')] + list(([] if None is
            ([exc] if exc else None) else [exc] if exc else None) or []))
    ast.Raise.expand = _hy_anon_var_45
    _hy_anon_var_46 = None
else:
    _hy_anon_var_46 = None
if hasattr(ast, HySymbol('Try')):

    def _hy_anon_var_47(self):
        """Args:
      body (stmt*) [list]
      handlers (excepthandler*) [list]
      orelse (stmt*) [list]
      finalbody (stmt*) [list]
      lineno (int)
      col_offset (int)"""
        orelse = hy.models.HyList(list(map(expand_form, self.orelse)))
        finalbody = hy.models.HyList(list(map(expand_form, self.finalbody)))
        return HyExpression([] + [HySymbol('try')] + [do_if_long(hy.models.
            HyList(list(map(expand_form, self.body))))] + [HyExpression([] +
            [HySymbol('except')] + [HyList([] + [HySymbol('e')] + [HySymbol
            ('Py2HyReturnException')])] + [HyExpression([] + [HySymbol(
            'raise')] + [HySymbol('e')])])] + list(([] if None is hy.models
            .HyList(list(map(expand_form, self.handlers))) else hy.models.
            HyList(list(map(expand_form, self.handlers)))) or []) + list(([
            ] if None is (HyList([] + [HyExpression([] + [HySymbol('else')] +
            list(([] if None is orelse else orelse) or []))]) if 0 < len(
            orelse) else None) else HyList([] + [HyExpression([] + [
            HySymbol('else')] + list(([] if None is orelse else orelse) or
            []))]) if 0 < len(orelse) else None) or []) + list(([] if None is
            (HyList([] + [HyExpression([] + [HySymbol('finally')] + list(([
            ] if None is finalbody else finalbody) or []))]) if 0 < len(
            finalbody) else None) else HyList([] + [HyExpression([] + [
            HySymbol('finally')] + list(([] if None is finalbody else
            finalbody) or []))]) if 0 < len(finalbody) else None) or []))
    ast.Try.expand = _hy_anon_var_47
    _hy_anon_var_48 = None
else:
    _hy_anon_var_48 = None
if hasattr(ast, HySymbol('Assert')):

    def _hy_anon_var_49(self):
        """Args:
      test (expr)
      msg (expr?) [optional]
      lineno (int)
      col_offset (int)"""
        msg = expand_form(self.msg)
        return HyExpression([] + [HySymbol('assert')] + [expand_form(self.
            test)] + list(([] if None is ([msg] if msg else None) else [msg
            ] if msg else None) or []))
    ast.Assert.expand = _hy_anon_var_49
    _hy_anon_var_50 = None
else:
    _hy_anon_var_50 = None
if hasattr(ast, HySymbol('Import')):

    def _hy_anon_var_51(self):
        """Args:
      names (alias*) [list]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('import')] + list(hyx_or(*([] if
            None is hy.models.HyList(list(map(expand_form, self.names))) else
            hy.models.HyList(list(map(expand_form, self.names)))), [])))
    ast.Import.expand = _hy_anon_var_51
    _hy_anon_var_52 = None
else:
    _hy_anon_var_52 = None
if hasattr(ast, HySymbol('ImportFrom')):

    def _hy_anon_var_53(self):
        """Args:
      module (identifier?) [optional]
      names (alias*) [list]
      level (int?) [optional]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('import')] + [HyList([] + [
            expand_form(self.module)] + [HyList([] + list(([] if None is
            reduce(add, hy.models.HyList(list(map(expand_form, self.names))
            )) else reduce(add, hy.models.HyList(list(map(expand_form, self
            .names))))) or []))])])
    ast.ImportFrom.expand = _hy_anon_var_53
    _hy_anon_var_54 = None
else:
    _hy_anon_var_54 = None
if hasattr(ast, HySymbol('Global')):

    def _hy_anon_var_55(self):
        """Args:
      names (identifier*) [list]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('global')] + list(([] if None is
            map(py2hy_mangle_identifier, hy.models.HyList(list(map(
            expand_form, self.names)))) else map(py2hy_mangle_identifier,
            hy.models.HyList(list(map(expand_form, self.names))))) or []))
    ast.Global.expand = _hy_anon_var_55
    _hy_anon_var_56 = None
else:
    _hy_anon_var_56 = None
if hasattr(ast, HySymbol('Nonlocal')):

    def _hy_anon_var_57(self):
        """Args:
      names (identifier*) [list]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('nonlocal')] + list(([] if None is
            map(py2hy_mangle_identifier, hy.models.HyList(list(map(
            expand_form, self.names)))) else map(py2hy_mangle_identifier,
            hy.models.HyList(list(map(expand_form, self.names))))) or []))
    ast.Nonlocal.expand = _hy_anon_var_57
    _hy_anon_var_58 = None
else:
    _hy_anon_var_58 = None
if hasattr(ast, HySymbol('Expr')):

    def _hy_anon_var_59(self):
        """Args:
      value (expr)
      lineno (int)
      col_offset (int)"""
        return expand_form(self.value)
    ast.Expr.expand = _hy_anon_var_59
    _hy_anon_var_60 = None
else:
    _hy_anon_var_60 = None
if hasattr(ast, HySymbol('Pass')):

    def _hy_anon_var_61(self):
        """Args:
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('do')])
    ast.Pass.expand = _hy_anon_var_61
    _hy_anon_var_62 = None
else:
    _hy_anon_var_62 = None
if hasattr(ast, HySymbol('Break')):

    def _hy_anon_var_63(self):
        """Args:
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('break')])
    ast.Break.expand = _hy_anon_var_63
    _hy_anon_var_64 = None
else:
    _hy_anon_var_64 = None
if hasattr(ast, HySymbol('Continue')):

    def _hy_anon_var_65(self):
        """Args:
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('continue')])
    ast.Continue.expand = _hy_anon_var_65
    _hy_anon_var_66 = None
else:
    _hy_anon_var_66 = None
if hasattr(ast, HySymbol('BoolOp')):

    def _hy_anon_var_67(self):
        """Args:
      op (boolop)
      values (expr*) [list]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [expand_form(self.op)] + list(([] if None is
            hy.models.HyList(list(map(expand_form, self.values))) else hy.
            models.HyList(list(map(expand_form, self.values)))) or []))
    ast.BoolOp.expand = _hy_anon_var_67
    _hy_anon_var_68 = None
else:
    _hy_anon_var_68 = None
if hasattr(ast, HySymbol('BinOp')):

    def _hy_anon_var_69(self):
        """Args:
      left (expr)
      op (operator)
      right (expr)
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [expand_form(self.op)] + [expand_form(self
            .left)] + [expand_form(self.right)])
    ast.BinOp.expand = _hy_anon_var_69
    _hy_anon_var_70 = None
else:
    _hy_anon_var_70 = None
if hasattr(ast, HySymbol('UnaryOp')):

    def _hy_anon_var_71(self):
        """Args:
      op (unaryop)
      operand (expr)
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [expand_form(self.op)] + [expand_form(self
            .operand)])
    ast.UnaryOp.expand = _hy_anon_var_71
    _hy_anon_var_72 = None
else:
    _hy_anon_var_72 = None
if hasattr(ast, HySymbol('Lambda')):

    def _hy_anon_var_73(self):
        """Args:
      args (arguments)
      body (expr)
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('fn')] + [expand_form(self.args)
            ] + [expand_form(self.body)])
    ast.Lambda.expand = _hy_anon_var_73
    _hy_anon_var_74 = None
else:
    _hy_anon_var_74 = None
if hasattr(ast, HySymbol('IfExp')):

    def _hy_anon_var_75(self):
        """Args:
      test (expr)
      body (expr)
      orelse (expr)
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('if')] + [expand_form(self.test)
            ] + [expand_form(self.body)] + [expand_form(self.orelse)])
    ast.IfExp.expand = _hy_anon_var_75
    _hy_anon_var_76 = None
else:
    _hy_anon_var_76 = None
if hasattr(ast, HySymbol('Dict')):

    def _hy_anon_var_77(self):
        """Args:
      keys (expr*) [list]
      values (expr*) [list]
      lineno (int)
      col_offset (int)"""
        return HyDict([] + list(([] if None is interleave(hy.models.HyList(
            list(map(expand_form, self.keys))), hy.models.HyList(list(map(
            expand_form, self.values)))) else interleave(hy.models.HyList(
            list(map(expand_form, self.keys))), hy.models.HyList(list(map(
            expand_form, self.values))))) or []))
    ast.Dict.expand = _hy_anon_var_77
    _hy_anon_var_78 = None
else:
    _hy_anon_var_78 = None
if hasattr(ast, HySymbol('Set')):

    def _hy_anon_var_79(self):
        """Args:
      elts (expr*) [list]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('set')] + list(([] if None is hy
            .models.HyList(list(map(expand_form, self.elts))) else hy.
            models.HyList(list(map(expand_form, self.elts)))) or []))
    ast.Set.expand = _hy_anon_var_79
    _hy_anon_var_80 = None
else:
    _hy_anon_var_80 = None
if hasattr(ast, HySymbol('ListComp')):

    def _hy_anon_var_81(self):
        """Args:
      elt (expr)
      generators (comprehension*) [list]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('list-comp')] + [expand_form(
            self.elt)] + list(([] if None is reduce(lambda x, y: x + y, hy.
            models.HyList(list(map(expand_form, self.generators)))) else
            reduce(lambda x, y: x + y, hy.models.HyList(list(map(
            expand_form, self.generators))))) or []))
    ast.ListComp.expand = _hy_anon_var_81
    _hy_anon_var_82 = None
else:
    _hy_anon_var_82 = None
if hasattr(ast, HySymbol('SetComp')):

    def _hy_anon_var_83(self):
        """Args:
      elt (expr)
      generators (comprehension*) [list]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('set-comp')] + [expand_form(self
            .elt)] + list(([] if None is reduce(lambda x, y: x + y, hy.
            models.HyList(list(map(expand_form, self.generators)))) else
            reduce(lambda x, y: x + y, hy.models.HyList(list(map(
            expand_form, self.generators))))) or []))
    ast.SetComp.expand = _hy_anon_var_83
    _hy_anon_var_84 = None
else:
    _hy_anon_var_84 = None
if hasattr(ast, HySymbol('DictComp')):

    def _hy_anon_var_85(self):
        """Args:
      key (expr)
      value (expr)
      generators (comprehension*) [list]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('dict-comp')] + [expand_form(
            self.key)] + [expand_form(self.value)] + list(([] if None is
            reduce(lambda x, y: x + y, hy.models.HyList(list(map(
            expand_form, self.generators)))) else reduce(lambda x, y: x + y,
            hy.models.HyList(list(map(expand_form, self.generators))))) or []))
    ast.DictComp.expand = _hy_anon_var_85
    _hy_anon_var_86 = None
else:
    _hy_anon_var_86 = None
if hasattr(ast, HySymbol('GeneratorExp')):

    def _hy_anon_var_87(self):
        """Args:
      elt (expr)
      generators (comprehension*) [list]
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('genexpr')] + [expand_form(self.
            elt)] + list(([] if None is reduce(lambda x, y: x + y, hy.
            models.HyList(list(map(expand_form, self.generators)))) else
            reduce(lambda x, y: x + y, hy.models.HyList(list(map(
            expand_form, self.generators))))) or []))
    ast.GeneratorExp.expand = _hy_anon_var_87
    _hy_anon_var_88 = None
else:
    _hy_anon_var_88 = None
if hasattr(ast, HySymbol('Await')):

    def _hy_anon_var_89(self):
        """Args:
      value (expr)
      lineno (int)
      col_offset (int)"""
        return None
    ast.Await.expand = _hy_anon_var_89
    _hy_anon_var_90 = None
else:
    _hy_anon_var_90 = None
if hasattr(ast, HySymbol('Yield')):

    def _hy_anon_var_91(self):
        """Args:
      value (expr?) [optional]
      lineno (int)
      col_offset (int)"""
        value = expand_form(self.value)
        return HyExpression([] + [HySymbol('yield')] + list(([] if None is
            ([value] if value else None) else [value] if value else None) or
            []))
    ast.Yield.expand = _hy_anon_var_91
    _hy_anon_var_92 = None
else:
    _hy_anon_var_92 = None
if hasattr(ast, HySymbol('YieldFrom')):

    def _hy_anon_var_93(self):
        """Args:
      value (expr)
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('yield_from')] + list(([] if 
            None is ([value] if value else None) else [value] if value else
            None) or []))
    ast.YieldFrom.expand = _hy_anon_var_93
    _hy_anon_var_94 = None
else:
    _hy_anon_var_94 = None
if hasattr(ast, HySymbol('Compare')):

    def _hy_anon_var_95(self):
        """Args:
      left (expr)
      ops (cmpop*) [list]
      comparators (expr*) [list]
      lineno (int)
      col_offset (int)"""
        ops = hy.models.HyList(list(map(expand_form, self.ops)))
        comparators = hy.models.HyList(list(map(expand_form, self.comparators))
            )
        left = expand_form(self.left)
        resultlist = map(lambda x: HyExpression([] + [first(x)] + [second(x
            )] + [x[2]]), zip(ops, HyExpression([] + [left]) + comparators,
            comparators))
        return HyExpression([] + [HySymbol('and')] + list(([] if None is
            resultlist else resultlist) or [])) if 1 < len(comparators
            ) else first(resultlist)
    ast.Compare.expand = _hy_anon_var_95
    _hy_anon_var_96 = None
else:
    _hy_anon_var_96 = None
if hasattr(ast, HySymbol('Call')):

    def _hy_anon_var_97(self):
        """Args:
      func (expr)
      args (expr*) [list]
      keywords (keyword*) [list]
      lineno (int)
      col_offset (int)"""
        keywords = hy.models.HyList(list(map(expand_form, self.keywords)))
        return HyExpression([] + [expand_form(self.func)] + list(([] if 
            None is hy.models.HyList(list(map(expand_form, self.args))) else
            hy.models.HyList(list(map(expand_form, self.args)))) or []) +
            list(([] if None is (reduce(lambda x, y: x + y if first(y) else
            HyList([] + [HyExpression([] + [HySymbol('unpack_mapping')] + [
            second(y)])]), map(lambda l: [hy.models.HyKeyword(':' + l[0]) if
            l[0] else None, l[1]], hy.models.HyList(list(map(expand_form,
            self.keywords)))), []) if keywords else None) else reduce(lambda
            x, y: x + y if first(y) else HyList([] + [HyExpression([] + [
            HySymbol('unpack_mapping')] + [second(y)])]), map(lambda l: [hy
            .models.HyKeyword(':' + l[0]) if l[0] else None, l[1]], hy.
            models.HyList(list(map(expand_form, self.keywords)))), []) if
            keywords else None) or []))
    ast.Call.expand = _hy_anon_var_97
    _hy_anon_var_98 = None
else:
    _hy_anon_var_98 = None
if hasattr(ast, HySymbol('Num')):

    def _hy_anon_var_99(self):
        """Args:
      n (object)
      lineno (int)
      col_offset (int)"""
        return expand_form(self.n)
    ast.Num.expand = _hy_anon_var_99
    _hy_anon_var_100 = None
else:
    _hy_anon_var_100 = None
if hasattr(ast, HySymbol('Str')):

    def _hy_anon_var_101(self):
        """Args:
      s (string)
      lineno (int)
      col_offset (int)"""
        return hy.models.HyString(expand_form(self.s))
    ast.Str.expand = _hy_anon_var_101
    _hy_anon_var_102 = None
else:
    _hy_anon_var_102 = None
if hasattr(ast, HySymbol('FormattedValue')):

    def _hy_anon_var_103(self):
        """Args:
      value (expr)
      conversion (int?) [optional]
      format_spec (expr?) [optional]
      lineno (int)
      col_offset (int)"""
        return None
    ast.FormattedValue.expand = _hy_anon_var_103
    _hy_anon_var_104 = None
else:
    _hy_anon_var_104 = None
if hasattr(ast, HySymbol('JoinedStr')):

    def _hy_anon_var_105(self):
        """Args:
      values (expr*) [list]
      lineno (int)
      col_offset (int)"""
        return expand_form(self.values)
    ast.JoinedStr.expand = _hy_anon_var_105
    _hy_anon_var_106 = None
else:
    _hy_anon_var_106 = None
if hasattr(ast, HySymbol('Bytes')):

    def _hy_anon_var_107(self):
        """Args:
      s (bytes)
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('hy.models.HyBytes')] + [
            expand_form(self.s)])
    ast.Bytes.expand = _hy_anon_var_107
    _hy_anon_var_108 = None
else:
    _hy_anon_var_108 = None
if hasattr(ast, HySymbol('NameConstant')):

    def _hy_anon_var_109(self):
        """Args:
      value (Constant)
      lineno (int)
      col_offset (int)"""
        return expand_form(self.value)
    ast.NameConstant.expand = _hy_anon_var_109
    _hy_anon_var_110 = None
else:
    _hy_anon_var_110 = None
if hasattr(ast, HySymbol('Ellipsis')):

    def _hy_anon_var_111(self):
        """Args:
      lineno (int)
      col_offset (int)"""
        return None
    ast.Ellipsis.expand = _hy_anon_var_111
    _hy_anon_var_112 = None
else:
    _hy_anon_var_112 = None
if hasattr(ast, HySymbol('Constant')):

    def _hy_anon_var_113(self):
        """Args:
      value (constant)
      lineno (int)
      col_offset (int)"""
        return expand_form(self.value)
    ast.Constant.expand = _hy_anon_var_113
    _hy_anon_var_114 = None
else:
    _hy_anon_var_114 = None
if hasattr(ast, HySymbol('Attribute')):

    def _hy_anon_var_115(self):
        """Args:
      value (expr)
      attr (identifier)
      ctx (expr_context)
      lineno (int)
      col_offset (int)"""
        value = expand_form(self.value)
        return hy.models.HySymbol(str(value) + '.' + self.attr
            ) if hy.models.HySymbol == type(value) else HyExpression([] + [
            HySymbol('.')] + [expand_form(self.value)] + [expand_form(self.
            attr)])
    ast.Attribute.expand = _hy_anon_var_115
    _hy_anon_var_116 = None
else:
    _hy_anon_var_116 = None
if hasattr(ast, HySymbol('Subscript')):

    def _hy_anon_var_117(self):
        """Args:
      value (expr)
      slice (slice)
      ctx (expr_context)
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('get')] + [expand_form(self.
            value)] + [expand_form(self.slice)])
    ast.Subscript.expand = _hy_anon_var_117
    _hy_anon_var_118 = None
else:
    _hy_anon_var_118 = None
if hasattr(ast, HySymbol('Starred')):

    def _hy_anon_var_119(self):
        """Args:
      value (expr)
      ctx (expr_context)
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol('unpack_iterable')] + [
            expand_form(self.value)])
    ast.Starred.expand = _hy_anon_var_119
    _hy_anon_var_120 = None
else:
    _hy_anon_var_120 = None
if hasattr(ast, HySymbol('Name')):

    def _hy_anon_var_121(self):
        """Args:
      id (identifier)
      ctx (expr_context)
      lineno (int)
      col_offset (int)"""
        return py2hy_mangle_identifier(expand_form(self.id))
    ast.Name.expand = _hy_anon_var_121
    _hy_anon_var_122 = None
else:
    _hy_anon_var_122 = None
if hasattr(ast, HySymbol('List')):

    def _hy_anon_var_123(self):
        """Args:
      elts (expr*) [list]
      ctx (expr_context)
      lineno (int)
      col_offset (int)"""
        return HyList([] + list(([] if None is hy.models.HyList(list(map(
            expand_form, self.elts))) else hy.models.HyList(list(map(
            expand_form, self.elts)))) or []))
    ast.List.expand = _hy_anon_var_123
    _hy_anon_var_124 = None
else:
    _hy_anon_var_124 = None
if hasattr(ast, HySymbol('Tuple')):

    def _hy_anon_var_125(self):
        """Args:
      elts (expr*) [list]
      ctx (expr_context)
      lineno (int)
      col_offset (int)"""
        return HyExpression([] + [HySymbol(',')] + list(([] if None is hy.
            models.HyList(list(map(expand_form, self.elts))) else hy.models
            .HyList(list(map(expand_form, self.elts)))) or []))
    ast.Tuple.expand = _hy_anon_var_125
    _hy_anon_var_126 = None
else:
    _hy_anon_var_126 = None
if hasattr(ast, HySymbol('Load')):
    ast.Load.expand = lambda self: 'Constant expression'
    _hy_anon_var_127 = None
else:
    _hy_anon_var_127 = None
if hasattr(ast, HySymbol('Store')):
    ast.Store.expand = lambda self: 'Constant expression'
    _hy_anon_var_128 = None
else:
    _hy_anon_var_128 = None
if hasattr(ast, HySymbol('Del')):
    ast.Del.expand = lambda self: 'Constant expression'
    _hy_anon_var_129 = None
else:
    _hy_anon_var_129 = None
if hasattr(ast, HySymbol('AugLoad')):
    ast.AugLoad.expand = lambda self: 'Constant expression'
    _hy_anon_var_130 = None
else:
    _hy_anon_var_130 = None
if hasattr(ast, HySymbol('AugStore')):
    ast.AugStore.expand = lambda self: 'Constant expression'
    _hy_anon_var_131 = None
else:
    _hy_anon_var_131 = None
if hasattr(ast, HySymbol('Param')):
    ast.Param.expand = lambda self: 'Constant expression'
    _hy_anon_var_132 = None
else:
    _hy_anon_var_132 = None
if hasattr(ast, HySymbol('Slice')):

    def _hy_anon_var_133(self):
        """Args:
      lower (expr?) [optional]
      upper (expr?) [optional]
      step (expr?) [optional]"""
        return HyExpression([] + [HySymbol('slice')] + [expand_form(self.
            lower)] + [expand_form(self.upper)] + [expand_form(self.step)])
    ast.Slice.expand = _hy_anon_var_133
    _hy_anon_var_134 = None
else:
    _hy_anon_var_134 = None
if hasattr(ast, HySymbol('ExtSlice')):

    def _hy_anon_var_135(self):
        """Args:
      dims (slice*) [list]"""
        return None
    ast.ExtSlice.expand = _hy_anon_var_135
    _hy_anon_var_136 = None
else:
    _hy_anon_var_136 = None
if hasattr(ast, HySymbol('Index')):

    def _hy_anon_var_137(self):
        """Args:
      value (expr)"""
        return expand_form(self.value)
    ast.Index.expand = _hy_anon_var_137
    _hy_anon_var_138 = None
else:
    _hy_anon_var_138 = None
if hasattr(ast, HySymbol('And')):

    def _hy_anon_var_139(self):
        """Constant expression"""
        return HySymbol('and')
    ast.And.expand = _hy_anon_var_139
    _hy_anon_var_140 = None
else:
    _hy_anon_var_140 = None
if hasattr(ast, HySymbol('Or')):

    def _hy_anon_var_141(self):
        """Constant expression"""
        return HySymbol('or')
    ast.Or.expand = _hy_anon_var_141
    _hy_anon_var_142 = None
else:
    _hy_anon_var_142 = None
if hasattr(ast, HySymbol('Add')):

    def _hy_anon_var_143(self):
        """Constant expression"""
        return HySymbol('+')
    ast.Add.expand = _hy_anon_var_143
    _hy_anon_var_144 = None
else:
    _hy_anon_var_144 = None
if hasattr(ast, HySymbol('Sub')):

    def _hy_anon_var_145(self):
        """Constant expression"""
        return HySymbol('-')
    ast.Sub.expand = _hy_anon_var_145
    _hy_anon_var_146 = None
else:
    _hy_anon_var_146 = None
if hasattr(ast, HySymbol('Mult')):

    def _hy_anon_var_147(self):
        """Constant expression"""
        return HySymbol('*')
    ast.Mult.expand = _hy_anon_var_147
    _hy_anon_var_148 = None
else:
    _hy_anon_var_148 = None
if hasattr(ast, HySymbol('MatMult')):

    def _hy_anon_var_149(self):
        """Constant expression"""
        return HySymbol('@')
    ast.MatMult.expand = _hy_anon_var_149
    _hy_anon_var_150 = None
else:
    _hy_anon_var_150 = None
if hasattr(ast, HySymbol('Div')):

    def _hy_anon_var_151(self):
        """Constant expression"""
        return HySymbol('/')
    ast.Div.expand = _hy_anon_var_151
    _hy_anon_var_152 = None
else:
    _hy_anon_var_152 = None
if hasattr(ast, HySymbol('Mod')):

    def _hy_anon_var_153(self):
        """Constant expression"""
        return HySymbol('%')
    ast.Mod.expand = _hy_anon_var_153
    _hy_anon_var_154 = None
else:
    _hy_anon_var_154 = None
if hasattr(ast, HySymbol('Pow')):

    def _hy_anon_var_155(self):
        """Constant expression"""
        return HySymbol('**')
    ast.Pow.expand = _hy_anon_var_155
    _hy_anon_var_156 = None
else:
    _hy_anon_var_156 = None
if hasattr(ast, HySymbol('LShift')):

    def _hy_anon_var_157(self):
        """Constant expression"""
        return HySymbol('<<')
    ast.LShift.expand = _hy_anon_var_157
    _hy_anon_var_158 = None
else:
    _hy_anon_var_158 = None
if hasattr(ast, HySymbol('RShift')):

    def _hy_anon_var_159(self):
        """Constant expression"""
        return HySymbol('>>')
    ast.RShift.expand = _hy_anon_var_159
    _hy_anon_var_160 = None
else:
    _hy_anon_var_160 = None
if hasattr(ast, HySymbol('BitOr')):

    def _hy_anon_var_161(self):
        """Constant expression"""
        return HySymbol('|')
    ast.BitOr.expand = _hy_anon_var_161
    _hy_anon_var_162 = None
else:
    _hy_anon_var_162 = None
if hasattr(ast, HySymbol('BitXor')):

    def _hy_anon_var_163(self):
        """Constant expression"""
        return HySymbol('^')
    ast.BitXor.expand = _hy_anon_var_163
    _hy_anon_var_164 = None
else:
    _hy_anon_var_164 = None
if hasattr(ast, HySymbol('BitAnd')):

    def _hy_anon_var_165(self):
        """Constant expression"""
        return HySymbol('&')
    ast.BitAnd.expand = _hy_anon_var_165
    _hy_anon_var_166 = None
else:
    _hy_anon_var_166 = None
if hasattr(ast, HySymbol('FloorDiv')):

    def _hy_anon_var_167(self):
        """Constant expression"""
        return HySymbol('//')
    ast.FloorDiv.expand = _hy_anon_var_167
    _hy_anon_var_168 = None
else:
    _hy_anon_var_168 = None
if hasattr(ast, HySymbol('Invert')):

    def _hy_anon_var_169(self):
        """Constant expression"""
        return HySymbol('~')
    ast.Invert.expand = _hy_anon_var_169
    _hy_anon_var_170 = None
else:
    _hy_anon_var_170 = None
if hasattr(ast, HySymbol('Not')):

    def _hy_anon_var_171(self):
        """Constant expression"""
        return HySymbol('not')
    ast.Not.expand = _hy_anon_var_171
    _hy_anon_var_172 = None
else:
    _hy_anon_var_172 = None
if hasattr(ast, HySymbol('UAdd')):

    def _hy_anon_var_173(self):
        """Constant expression"""
        return HySymbol('+')
    ast.UAdd.expand = _hy_anon_var_173
    _hy_anon_var_174 = None
else:
    _hy_anon_var_174 = None
if hasattr(ast, HySymbol('USub')):

    def _hy_anon_var_175(self):
        """Constant expression"""
        return HySymbol('-')
    ast.USub.expand = _hy_anon_var_175
    _hy_anon_var_176 = None
else:
    _hy_anon_var_176 = None
if hasattr(ast, HySymbol('Eq')):

    def _hy_anon_var_177(self):
        """Constant expression"""
        return HySymbol('=')
    ast.Eq.expand = _hy_anon_var_177
    _hy_anon_var_178 = None
else:
    _hy_anon_var_178 = None
if hasattr(ast, HySymbol('NotEq')):

    def _hy_anon_var_179(self):
        """Constant expression"""
        return HySymbol('!=')
    ast.NotEq.expand = _hy_anon_var_179
    _hy_anon_var_180 = None
else:
    _hy_anon_var_180 = None
if hasattr(ast, HySymbol('Lt')):

    def _hy_anon_var_181(self):
        """Constant expression"""
        return HySymbol('<')
    ast.Lt.expand = _hy_anon_var_181
    _hy_anon_var_182 = None
else:
    _hy_anon_var_182 = None
if hasattr(ast, HySymbol('LtE')):

    def _hy_anon_var_183(self):
        """Constant expression"""
        return HySymbol('<=')
    ast.LtE.expand = _hy_anon_var_183
    _hy_anon_var_184 = None
else:
    _hy_anon_var_184 = None
if hasattr(ast, HySymbol('Gt')):

    def _hy_anon_var_185(self):
        """Constant expression"""
        return HySymbol('>')
    ast.Gt.expand = _hy_anon_var_185
    _hy_anon_var_186 = None
else:
    _hy_anon_var_186 = None
if hasattr(ast, HySymbol('GtE')):

    def _hy_anon_var_187(self):
        """Constant expression"""
        return HySymbol('>=')
    ast.GtE.expand = _hy_anon_var_187
    _hy_anon_var_188 = None
else:
    _hy_anon_var_188 = None
if hasattr(ast, HySymbol('Is')):

    def _hy_anon_var_189(self):
        """Constant expression"""
        return HySymbol('is')
    ast.Is.expand = _hy_anon_var_189
    _hy_anon_var_190 = None
else:
    _hy_anon_var_190 = None
if hasattr(ast, HySymbol('IsNot')):

    def _hy_anon_var_191(self):
        """Constant expression"""
        return HySymbol('is-not')
    ast.IsNot.expand = _hy_anon_var_191
    _hy_anon_var_192 = None
else:
    _hy_anon_var_192 = None
if hasattr(ast, HySymbol('In')):

    def _hy_anon_var_193(self):
        """Constant expression"""
        return HySymbol('in')
    ast.In.expand = _hy_anon_var_193
    _hy_anon_var_194 = None
else:
    _hy_anon_var_194 = None
if hasattr(ast, HySymbol('NotIn')):

    def _hy_anon_var_195(self):
        """Constant expression"""
        return HySymbol('not-in')
    ast.NotIn.expand = _hy_anon_var_195
    _hy_anon_var_196 = None
else:
    _hy_anon_var_196 = None
if hasattr(ast, HySymbol('comprehension')):

    def _hy_anon_var_197(self):
        """Args:
      target (expr)
      iter (expr)
      ifs (expr*) [list]
      is_async (int)"""
        target = expand_form(self.target)
        ifs = hy.models.HyList(list(map(expand_form, self.ifs)))
        return HyList([] + [HyList([] + list(([] if None is ([HyList([] +
            list(([] if None is rest(target) else rest(target)) or []))] if
            HySymbol(',') == first(target) else [target]) else [HyList([] +
            list(([] if None is rest(target) else rest(target)) or []))] if
            HySymbol(',') == first(target) else [target]) or []) + [
            expand_form(self.iter)])] + list(([] if None is (HyList([] + [
            HyExpression([] + [HySymbol('and')] + list(([] if None is ifs else
            ifs) or []))]) if 0 < len(ifs) else None) else HyList([] + [
            HyExpression([] + [HySymbol('and')] + list(([] if None is ifs else
            ifs) or []))]) if 0 < len(ifs) else None) or []))
    ast.comprehension.expand = _hy_anon_var_197
    _hy_anon_var_198 = None
else:
    _hy_anon_var_198 = None
if hasattr(ast, HySymbol('ExceptHandler')):

    def _hy_anon_var_199(self):
        """Args:
      type (expr?) [optional]
      name (identifier?) [optional]
      body (stmt*) [list]
      lineno (int)
      col_offset (int)"""
        e_name = py2hy_mangle_identifier(expand_form(self.name))
        e_type = expand_form(self.type)
        return HyExpression([] + [HySymbol('except')] + [HyList([] + list((
            [] if None is ([e_name] if e_name else None) else [e_name] if
            e_name else None) or []) + list(([] if None is (None if None is
            e_type else [HyList([] + list(([] if None is rest(e_type) else
            rest(e_type)) or []))] if HySymbol(',') == first(e_type) else [
            e_type]) else None if None is e_type else [HyList([] + list(([] if
            None is rest(e_type) else rest(e_type)) or []))] if HySymbol(
            ',') == first(e_type) else [e_type]) or []))] + list(([] if 
            None is hy.models.HyList(list(map(expand_form, self.body))) else
            hy.models.HyList(list(map(expand_form, self.body)))) or []))
    ast.ExceptHandler.expand = _hy_anon_var_199
    _hy_anon_var_200 = None
else:
    _hy_anon_var_200 = None
if hasattr(ast, HySymbol('arguments')):

    def _hy_anon_var_202(self):
        """Args:
      args (arg*) [list]
      vararg (arg?) [optional]
      kwonlyargs (arg*) [list]
      kw_defaults (expr*) [list]
      kwarg (arg?) [optional]
      defaults (expr*) [list]"""
        args = hy.models.HyList(list(map(expand_form, self.args)))
        vararg = expand_form(self.vararg)
        kwarg = expand_form(self.kwarg)
        defaults = hy.models.HyList(list(map(expand_form, self.defaults)))
        kwonlyargs = hy.models.HyList(list(map(expand_form, self.kwonlyargs)))
        kw_defaults = hy.models.HyList(list(map(expand_form, self.kw_defaults))
            )

        def take_last(n, l):
            return drop(len(l) - n, l)
        return HyList([] + list(([] if None is drop_last(len(defaults),
            args) else drop_last(len(defaults), args)) or []) + list(([] if
            None is (HyList([] + [HySymbol('&optional')] + list(([] if None is
            [HyList([] + [x] + [y]) for [x, y] in zip(take_last(len(
            defaults), args), defaults)] else [HyList([] + [x] + [y]) for [
            x, y] in zip(take_last(len(defaults), args), defaults)]) or [])
            ) if defaults else None) else HyList([] + [HySymbol('&optional'
            )] + list(([] if None is [HyList([] + [x] + [y]) for [x, y] in
            zip(take_last(len(defaults), args), defaults)] else [HyList([] +
            [x] + [y]) for [x, y] in zip(take_last(len(defaults), args),
            defaults)]) or [])) if defaults else None) or []) + list(([] if
            None is (HyList([] + [HySymbol('&kwonly')] + list(([] if None is
            drop_last(len(kw_defaults), kwonlyargs) else drop_last(len(
            kw_defaults), kwonlyargs)) or []) + list(([] if None is [HyList
            ([] + [x] + [y]) for [x, y] in zip(take_last(len(kw_defaults),
            kwonlyargs), kw_defaults)] else [HyList([] + [x] + [y]) for [x,
            y] in zip(take_last(len(kw_defaults), kwonlyargs), kw_defaults)
            ]) or [])) if kwonlyargs else None) else HyList([] + [HySymbol(
            '&kwonly')] + list(([] if None is drop_last(len(kw_defaults),
            kwonlyargs) else drop_last(len(kw_defaults), kwonlyargs)) or []
            ) + list(([] if None is [HyList([] + [x] + [y]) for [x, y] in
            zip(take_last(len(kw_defaults), kwonlyargs), kw_defaults)] else
            [HyList([] + [x] + [y]) for [x, y] in zip(take_last(len(
            kw_defaults), kwonlyargs), kw_defaults)]) or [])) if kwonlyargs
             else None) or []) + list(([] if None is (HyList([] + [HySymbol
            ('&kwargs')] + [kwarg]) if kwarg else None) else HyList([] + [
            HySymbol('&kwargs')] + [kwarg]) if kwarg else None) or []) +
            list(([] if None is (HyList([] + [HySymbol('&rest')] + [vararg]
            ) if vararg else None) else HyList([] + [HySymbol('&rest')] + [
            vararg]) if vararg else None) or []))
    ast.arguments.expand = _hy_anon_var_202
    _hy_anon_var_203 = None
else:
    _hy_anon_var_203 = None
if hasattr(ast, HySymbol('arg')):

    def _hy_anon_var_204(self):
        """Args:
      arg (identifier)
      annotation (expr?) [optional]
      lineno (int)
      col_offset (int)"""
        return py2hy_mangle_identifier(expand_form(self.arg))
    ast.arg.expand = _hy_anon_var_204
    _hy_anon_var_205 = None
else:
    _hy_anon_var_205 = None
if hasattr(ast, HySymbol('keyword')):

    def _hy_anon_var_206(self):
        """Args:
      arg (identifier?) [optional]
      value (expr)"""
        return HyExpression([] + [py2hy_mangle_identifier(expand_form(self.
            arg))] + [expand_form(self.value)])
    ast.keyword.expand = _hy_anon_var_206
    _hy_anon_var_207 = None
else:
    _hy_anon_var_207 = None
if hasattr(ast, HySymbol('alias')):

    def _hy_anon_var_208(self):
        """Args:
      name (identifier)
      asname (identifier?) [optional]"""
        return HyList([] + [expand_form(self.name)] + [HyKeyword('as')] + [
            expand_form(self.asname)]) if expand_form(self.asname) else HyList(
            [] + [expand_form(self.name)])
    ast.alias.expand = _hy_anon_var_208
    _hy_anon_var_209 = None
else:
    _hy_anon_var_209 = None
if hasattr(ast, HySymbol('withitem')):

    def _hy_anon_var_210(self):
        """Args:
      context_expr (expr)
      optional_vars (expr?) [optional]"""
        optional_vars = expand_form(self.optional_vars)
        return HyExpression([] + list(([] if None is ([optional_vars] if
            optional_vars else None) else [optional_vars] if optional_vars else
            None) or []) + [expand_form(self.context_expr)])
    ast.withitem.expand = _hy_anon_var_210
    _hy_anon_var_211 = None
else:
    _hy_anon_var_211 = None


def py2hy_print(ast):
    for p in ast.expand()[1:None:]:
        print(hy_repr(p)[1:None:])


def py2hy_file(filepath, dumpast=False):
    astobj = ast.parse(open(filepath, 'r').read())
    return print(ast.dump(codeobj)) if dumpast else py2hy_print(astobj)


def py2hy(ast):
    return ast.expand()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath')
    parser.add_argument('--ast', action='store_true')
    args = parser.parse_args()
    return py2hy_file(args.filepath, args.ast)


main() if __name__ == '__main__' else None

