#!/bin/env python3
#
# CircuitPython interpreter for jslogo.
#
# Author: Sreepathi Pai
# Copyright (C) 2023 University of Rochester
#
# Licensed under the MIT License
#
# This is a reimplementation of logo.js in Python since it still uses
# the Logo interface. Error checking is minimal in this version since
# it assumes the code it will run has already been executed
# successfully.
#
# The original copyright for that code written in JavaScript is:
#
# Copyright (C) 2011 Joshua Bell
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math
import re
import random

NUMBER = re.compile("-?([0-9]*\\.?[0-9]+([eE][\\-+]?[0-9]+)?)")
UNARY_MINUS = '<UNARYMINUS>'

class StringMap:
    def __init__(self, case_fold):
        self._case_fold = case_fold
        self._map = {}

    def get(self, key):
        key = key if not self._case_fold else key.lower()
        return self._map.get(key, None)

    def set(self, key, value):
        key = key if not self._case_fold else key.lower()
        self._map[key] = value

    def has(self, key):
        key = key if not self._case_fold else key.lower()
        return key in self._map

    def delete(self, key):
        key = key if not self._case_fold else key.lower()
        del self._map[key]

    def keys(self):
        return self.keys()

    def empty(self):
        return len(self._map) == 0

    # forEach

class Logo:
    def __init__(self, turtle):
        self.turtle = turtle
        self.routines = StringMap(True)
        self.scopes = [StringMap(True)]

        self.stack = []
        self._repcount = 0
        self.define_motion()
        self.define_control()
        self.define_misc()
        self.define_fun()
        self.define_xmit()
        self.define_wk()

    def isKeyword(self, atom, match):
        if not self.Type(atom) == 'word':
            return False

        atom = str(atom).upper()

        # TODO: keywordAliases

        return atom == match

    def defer(self, func, *args):
        def deferred():
            a = [aa() for aa in args]
            return func(*a)

        return deferred

    def run(self, code):
        return self.execute(code)

    def define(self, names, code, nargs, props = None):
        if props is None: props = {}

        props['args'] = nargs

        for n in names:
            self.routines.set(n, {'code': code, 'props': props})

    # transmitters

    def show(self, *args):
        s = " ".join([str(s) for s in args])
        print("show", s)

    def define_xmit(self):
        self.define(['show'], self.show, 1, {'minimum': 0, 'maximum': -1})

    # motion
    def forward(self, a):
        return self.turtle.move(self.aexpr(a))

    def back(self, a):
        return self.turtle.move(-self.aexpr(a))

    def left(self, a):
        return self.turtle.turn(-self.aexpr(a))

    def right(self, a):
        return self.turtle.turn(self.aexpr(a))

    # no support for arrows

    def setpos(self, l):
        l = self.lexpr(l)
        assert len(l) == 2, "Need list of length 2 for setpos"
        self.turtle.position([self.aexpr(l[0]), self.aexpr(l[1])])

    def setxy(self, x, y):
        self.turtle.position([self.aexpr(x), self.aexpr(y)])

    def setx(self, x):
        self.turtle.position([self.aexpr(x), self.turtle.cury])

    def sety(self, y):
        self.turtle.position([self.turtle.curx, self.aexpr(y)])

    def setheading(self, heading):
        self.turtle.setheading(self.aexpr(heading))

    def home(self):
        # TODO
        return self.turtle.home()

    def arc(self, angle, radius):
        # TODO: what does this return?
        return self.turtle.arc([self.aexpr(angle), self.aexpr(radius)])

    # motion queries

    def pos(self):
        return [self.turtle.curx, self.turtle.cury]

    def xcor(self):
        return self.turtle.curx

    def ycor(self):
        return self.turtle.cury

    def heading(self):
        return self.turtle.heading

    def towards(self, l):
        l = self.lexpr(l)

        assert len(l) == 2, "towards expects list of length 2"

        return self.turtle.towards(self.aexpr(l[0]), self.aexpr(l[1]))

    # scrunch

    # clean, wrap, window, fence, fill, filled, label, setlabelheight, setlabelfont
    # setscrunch
    # shownp, turtlemode, labelsize, labelfont

    def clearscreen(self):
        self.turtle.clearscreen()

    def penup(self):
        self.turtle.pendown(False)

    def pendown(self):
        self.turtle.pendown(True)

    # penpaint, penerase, penreverse

    # TODO: setpencolor, setpc, setcolor

    # setpalette, setpensize, setwidth, setpw
    # setbackground, setbg, setscreencolor, setsc

    def pendownp(self):
        return 1 if self.turtle.pendownp() else 0

    def buttonp(self):
        return 1 if self.turtle.buttonp() else 0

    button = buttonp # only one button

    def leftsensor(self):
        return self.turtle.leftDetector()

    def rightsensor(self):
        return self.turtle.rightDetector()

    def define_motion(self):
        self.define(['forward', 'fd'], self.forward, 1)
        self.define(['back', 'bk'], self.back, 1)
        self.define(['left', 'lt'], self.left, 1)
        self.define(['right', 'rt'], self.right, 1)

        self.define(['setpos'], self.setpos, 1)
        self.define(['setxy'], self.setxy, 1)
        self.define(['setx'], self.setx, 1)
        self.define(['sety'], self.sety, 1)
        self.define(['setheading', 'seth'], self.setheading, 1)

        self.define(['home'], self.home, 0)
        self.define(['arc'], self.arc, 2)
        self.define(['pos'], self.pos, 0)
        self.define(['xcor'], self.xcor, 0)
        self.define(['ycor'], self.ycor, 0)
        self.define(['heading'], self.heading, 0)
        self.define(['towards'], self.towards, 1)

        self.define(['clearscreen', 'cs'], self.clearscreen, 0)
        self.define(['pendown', 'pd'], self.pendown, 0)
        self.define(['penup', 'pu'], self.penup, 0)

        self.define(['pendownp', 'pendown?'], self.pendownp, 0)
        self.define(['buttonp', 'button?'], self.buttonp, 0)
        self.define(['button'], self.button, 0)

        self.define(['leftsensor'], self.leftsensor, 0)
        self.define(['rightsensor'], self.rightsensor, 0)

    # control
    def repeat(self, count, statements):
        count = self.aexpr(count)
        statements = self.lexpr(statements)
        old_repcount = self._repcount
        i = 1

        while not (i > count):
            self.execute(statements)
            i += 1
            self._repcount = i

        self._repcount = old_repcount

    def repcount(self):
        return self._repcount

    def forever(self, statements):
        statements = self.lexpr(statements)
        old_repcount = self._repcount
        i = 1

        while True:
            self.execute(statements)
            i += 1
            self._repcount = i

        self._repcount = old_repcount

    def if_(self, tf, statements, *args):
        if self.Type(tf) == 'list':
            tf = self.evaluateExpression(tf)

        statements2 = args # unsure when this triggers?
        tf = self.aexpr(tf)
        if not statements2:
            return self.execute(statements, {'returnResult': True}) if tf else None
        else:
            return self.execute(statements, {'returnResult': True}) if tf else self.execute(statements2, {'returnResult': True})

    def ifelse(self, tf, statements1, statements2):
        if self.Type(tf) == 'list':
            tf = self.evaluateExpression(tf)

        return self.execute(statements1, {'returnResult': True}) if tf else self.execute(statements2, {'returnResult': True})

    def checkevalblock(self, block):
        block = block()
        assert self.Type(block) == 'list'
        return block

    def while_(self, tfexpression, block):
        block = self.checkevalblock(block)

        tf = tfexpression()
        if self.Type(tf) == 'list':
            tf = self.evaluateExpression(tf)

        while tf:
            self.execute(block)
            tf = tfexpression()
            if self.Type(tf) == 'list':
                tf = self.evaluateExpression(tf)

    def test(self, tf):
        if self.Type(tf) == 'list':
            tf = self.evaluateExpression(tf)

        tf = self.aexpr(tf)
        self.scopes[-1]._test = tf

    def iftrue(self, statements):
        statements = self.lexpr(statements)
        assert hasattr(self.scopes[len(self.scopes) - 1], '_test'), "test must be called first"

        tf = self.scopes[-1]._test

        if tf: return self.execute(statements, {'returnResult': True})

    def iffalse(self, statements):
        statements = self.lexpr(statements)
        assert hasattr(self.scopes[len(self.scopes) - 1], '_test'), "test must be called first"

        tf = self.scopes[-1]._test

        if not tf: return self.execute(statements, {'returnResult': True})

    def for_(self, control, statements):
        control = self.lexpr(control)
        statements = self.lexpr(statements)

        def sign(x):
            return -1 if x < 0 else 1 if x > 0 else 0

        varname = self.sexpr(control.pop(0))

        current = start = self.aexpr(self.evaluateExpression(control))
        limit = self.aexpr(self.evaluateExpression(control))

        if len(control):
            step = self.aexpr(self.evaluateExpression(control))
        else:
            step = -1 if limit < start else 1

        while not sign(current - limit) == sign(step):
            self.setlocal(varname, current)
            self.execute(statements)
            current += step

    def dotimes(self, control, statements):
        control = self.lexpr(control)
        statements = self.lexpr(statements)

        varname = self.sexpr(control.pop(0))
        current = 1

        times = self.aexpr(self.evaluateExpression(control))
        while not (current > times):
            self.setlocal(varname, current)
            self.execute(statements)
            current += 1

    def do_while(self, block, tfexpression):
        block = self.checkevalblock(block)
        tf = True
        while tf:
            self.execute(block)
            tf = tfexpression()
            if self.Type(tf) == 'list':
                tf = self.evaluateExpression(tf)

    def do_until(self, block, tfexpression):
        block = self.checkevalblock(block)
        tf = False
        while not tf:
            self.execute(block)
            tf = tfexpression()
            if self.Type(tf) == 'list':
                tf = self.evaluateExpression(tf)

    def until(self, tfexpression, block):
        block = self.checkevalblock(block)
        tf = tfexpression()
        if self.Type(tf) == 'list':
            tf = self.evaluateExpression(tf)

        while not tf:
            self.execute(block)
            tf = tfexpression()
            if self.Type(tf) == 'list':
                tf = self.evaluateExpression(tf)

    def case(self, value, clauses):
        clauses = self.lexpr(clauses)

        for clause in clauses:
            clause = self.lexpr(clause)
            first = clause.pop(0)

            if self.isKeyword(first, 'ELSE'):
                return self.evaluateExpression(clause)

            for x in self.lexpr(first):
                # this fails for the example in the documentation, e.g. for strings
                # and should probably be x = self.evaluateExpression([x])
                # print(x, self.Type(x), value, self.Type(value))
                # if any([self.equal(x, value) for x in self.lexpr(first)]):

                if self.equal(x, value):
                    return self.evaluateExpression(clause)

        return None

    def cond(self, clauses):
        clauses = self.lexpr(clauses)

        for clause in clauses:
            clause = self.lexpr(clause)
            first = clause.pop(0)
            if self.isKeyword(first, 'ELSE'):
                return self.evaluateExpression(clause)

            result = self.evaluateExpression(self.lexpr(first))
            if result:
                return self.evaluateExpression(clause)

    def define_control(self):
        # TODO: run, runresult
        self.define(['repeat'], self.repeat, 2)
        self.define(['forever'], self.forever, 1)
        self.define(['repcount', '#'], self.repcount, 0)
        self.define(['if'], self.if_, 2, {'maximum': 3})
        self.define(['ifelse'], self.ifelse, 3)
        self.define(['while'], self.while_, 2, {'noeval': True})
        self.define(['test'], self.test, 1)
        self.define(['iftrue', 'ift'], self.iftrue, 1)
        self.define(['iffalse', 'iff'], self.iffalse, 1)
        self.define(['for'], self.for_, 2)
        self.define(['dotimes'], self.dotimes, 2)
        self.define(['do.while'], self.do_while, 2, {'noeval': True})
        self.define(['do.until'], self.do_until, 2, {'noeval': True})
        self.define(['until'], self.until, 2, {'noeval': True})
        self.define(['case'], self.case, 2)
        self.define(['cond'], self.cond, 1)

    # variables
    def lvalue(self, name):
        for i in range(len(self.scopes) - 1, -1, -1):
            if self.scopes[i].has(name):
                return self.scopes[i].get(name)

    def maybegetvar(self, name):
        lval = self.lvalue(name)
        return lval['value'] if lval else None

    def getvar(self, name):
        value = self.maybegetvar(name)
        assert value is not None
        return value

    def setvar(self, name, value):
        value = self.copy(value)
        lval = self.lvalue(name)
        if lval:
            lval['value'] = value
        else:
            lval = {'value': value}
            self.scopes[0].set(name, lval)

        # this won't respect scope!
        if self.turtle.is_io_var(name):
            self.turtle.setvar(name, value)


    def local(self, name):
        scope = self.scopes[-1]
        scope.set(self.sexpr(name), {'value': None})

    def setlocal(self, name, value):
        value = self.copy(value)
        scope = self.scopes[-1]
        scope.set(self.sexpr(name), {'value': value})

    def make(self, varname, value):
        sv = self.sexpr(varname)
        self.setvar(sv, value)

    def wait(self, time):
        self.turtle.wait(time)

    def beep(self):
        self.turtle.tone(5300, 0.3)

    def setpencolor(self, color):
        self.turtle.color(color)

    def hideturtle(self):
        return

    def showturtle(self):
        return

    def random(self, max_, *args):
        if len(args) == 0:
            max_ = self.aexpr(max_)
            return random.randint(0, max_)
        else:
            start = self.aexpr(max_)
            end = self.aexpr(args[0])
            return random.randint(start, end)

    def define_misc(self):
        self.define(['make'], self.make, 2)
        self.define(['wait'], self.wait, 1)
        self.define(['beep'], self.beep, 0)
        self.define(['setpencolor', 'setpc', 'setcolor'], self.setpencolor, 1)
        self.define(['hideturtle', 'ht'], self.hideturtle, 0)
        self.define(['showturtle', 'st'], self.showturtle, 0)
        self.define(['random'], self.random, 1, {'maximum': 2})

    def true(self):
        return 1

    def false(self):
        return 0

    def not_(self, a):
        return 1 if not self.aexpr(a) else 0

    def and_(self, *args):
        for aa in args:
            if not aa(): return 0

        return 1

    def or_(self, *args):
        for aa in args:
            if aa(): return 1

        return 0

    def xor_(self, *args):
        if len(args):
            x = bool(args[0])
            for y in args[1:]:
                x = x != bool(y)

            return 1 if x else 0
        else:
            return 0

    def define_fun(self):
        self.define(['not'], self.not_, 1)
        self.define(['true'], self.true, 0)
        self.define(['false'], self.false, 0)
        self.define(['and'], self.and_, 2, {'noeval': True, 'minimum': 0, 'maximum': -1})
        self.define(['or'], self.or_, 2, {'noeval': True, 'minimum': 0, 'maximum': -1})
        self.define(['xor'], self.xor_, 2, {'minimum': 0, 'maximum': -1})

    # err

    # to_arity?

    # PRNG?

    # LogoArray?

    # Stream?

    # routines, scopes, plists?

    # Type

    def to(self, list_):
        name = self.sexpr(list_.pop(0))
        if self.isNumber(name) or self.isOperator(name):
            assert False, "TO: identifier needed for procedure name"

        inputs = []
        optional_inputs = []
        rest = None
        length = None
        block = []

        REQUIRED = 0
        OPTIONAL = 1
        REST = 2
        DEFAULT = 3
        BLOCK = 4

        state = REQUIRED
        sawEnd = False

        while len(list_):
            atom = list_.pop(0)
            if self.isKeyword(atom, 'END'):
                sawEnd = True
                break

            if state == REQUIRED:
                if self.Type(atom) == 'word' and str(atom)[0] == ':':
                    inputs.append(atom[1:])
                    continue
                state = OPTIONAL

            if state == OPTIONAL:
                if self.Type(atom) == 'list' and len(atom) > 1 and str(atom[0])[0] == ':':
                    n = atom.pop(0)[1:]
                    optional_inputs.append([n, atom])
                    continue
                state = REST

            if state == REST:
                state = DEFAULT
                if self.Type(atom) == 'list' and len(atom) == 1 and str(atom[0])[0] == ':':
                    rest = atom[0][1:]
                    continue

            if state == DEFAULT:
                state = BLOCK
                if self.Type(atom) == 'word' and self.isNumber(atom):
                    length = self.parseFloat(atom) # TODO
                    continue

            block.append(atom)

        assert sawEnd, "TO did not see END"

        self.defineProc(name, inputs, optional_inputs, rest, length, block)

    def defineProc(self, name, inputs, optional_inputs, rest, def_, block):
        if self.routines.has(name) and self.routines.get(name)['proc'].get('primitive', False):
            assert False, "Can't redefine primitive"

        if def_ is not None:
            if def_ < len(inputs) or (not rest and def_ > len(inputs) + len(optional_inputs)):
                assert False, "Incorrect default number of inputs"

        length = len(inputs) if def_ is None else def_

        def func(*args):
            scope = StringMap(True)
            self.scopes.append(scope)

            i = 0

            while i < len(inputs) and i < len(args):
                scope.set(inputs[i], {'value': args[i]})
                i += 1

            while i < len(inputs) + len(optional_inputs) and i < len(args):
                op = optional_inputs[i - len(inputs)]
                scope.set(op[0], {'value': args[i]})

            while i < len(inputs) + len(optional_inputs):
                op = optional_inputs[i - len(inputs)]
                scope.set(op[0], {'value': self.evaluateExpression(op[1])})
                i += 1

            if rest is not None:
                scope.set(rest, {'value': list(args[i:])})

            self.execute(block) # TODO: handle Output?
            self.scopes.pop()

        self.routines.set(name, {'code': func,
                                 'props': {'args': len(inputs),
                                           'inputs': inputs, 'optional_inputs': optional_inputs,
                                           'rest': rest, 'def': def_, 'block': block,
                                           'minimum': len(inputs), 'default': length,
                                           'maximum': -1 if rest else len(inputs) + len(optional_inputs)}})

    def define_wk(self):
        self.define(['to'], self.to, 1, {'special': True})

    def Type(self, atom):
        assert atom is not None, "Type, Atom should not be none"

        if isinstance(atom, str) or isinstance(atom, (float, int)):
            return 'word'
        elif isinstance(atom, list): # TODO: LogoArray
            return 'list'
        elif not atom:
            assert False, "Unexpected value for atom"
        else:
            assert False, "Unknown type"

    # all parsing routines omitted

    def execute(self, statements, options = None):
        if options is None: options = {}

        statements = list(statements) # shallow copy [.slice in original]

        lastResult = None

        while len(statements):
            result = self.evaluateExpression(statements)

            if result is not None and not options.get('returnResult', False):
                print(statements, result)
                assert False, "Result supplied when not wanted"

            lastResult = result

        return lastResult

    def isNumber(self, atom):
        m = NUMBER.match(str(atom))
        if NUMBER.match(str(atom)) is not None:
            return True

        return False

    def peek(self, l, options):
        if len(l):
            n = l[0]
            return n in options

        return False

    def evaluateExpression(self, l):
        return self.expression(l)()

    def expression(self, l):
        return self.relationalExpression(l)

    def relationalExpression(self, l):
        lhs = self.additiveExpression(l)

        while self.peek(l, ['=', '<', '>', '<=', '>=', '<>']):
            op = l.pop(0)

            def lhsf(lhs):
                rhs = self.additiveExpression(l)

                if op == '<':
                    return self.defer(lambda lhs, rhs: 1 if self.aexpr(lhs) < self.aexpr(rhs) else 0, lhs, rhs)
                elif op == '>':
                    return self.defer(lambda lhs, rhs: 1 if self.aexpr(lhs) > self.aexpr(rhs) else 0, lhs, rhs)
                elif op == '=':
                    return self.defer(lambda lhs, rhs: 1 if self.equal(lhs, rhs) else 0, lhs, rhs)
                elif op == '<=':
                    return self.defer(lambda lhs, rhs: 1 if self.aexpr(lhs) <= self.aexpr(rhs) else 0, lhs, rhs)
                elif op == '>=':
                    return self.defer(lambda lhs, rhs: 1 if self.aexpr(lhs) >= self.aexpr(rhs) else 0, lhs, rhs)
                elif op == '<>':
                    return self.defer(lambda lhs, rhs: 1 if not self.equal(lhs, rhs) else 0, lhs, rhs)
                else:
                    assert False, "Internal error in relationalExpression"

            lhs = lhsf(lhs)

        return lhs

    def additiveExpression(self, l):
        lhs = self.multiplicativeExpression(l)

        while self.peek(l, ['+', '-']):
            op = l.pop(0)

            def lhsf(lhs):
                rhs = self.multiplicativeExpression(l)

                if op == '+':
                    return self.defer(lambda lhs, rhs: self.aexpr(lhs) + self.aexpr(rhs), lhs, rhs)
                elif op == '-':
                    return self.defer(lambda lhs, rhs: self.aexpr(lhs) - self.aexpr(rhs), lhs, rhs)
                else:
                    assert False, "Internal error in additiveExpression"

            lhs = lhsf(lhs)

        return lhs

    def multiplicativeExpression(self, l):
        lhs = self.powerExpression(l)

        while self.peek(l, ['*', '/', '%']):
            op = l.pop(0)
            def lhsf(lhs):
                rhs = self.powerExpression(l)
                if op == '*':
                    return self.defer(lambda lhs, rhs: self.aexpr(lhs) * self.aexpr(rhs), lhs, rhs)
                elif op == '/':
                    def dodiv(lhs, rhs):
                        n = self.aexpr(lhs)
                        d = self.aexpr(rhs)
                        assert d != 0
                        return n / d

                    return self.defer(dodiv, lhs, rhs)
                elif op == '%':
                    def domod(lhs, rhs):
                        n = self.aexpr(lhs)
                        d = self.aexpr(rhs)
                        assert d != 0
                        return n % d

                    return self.defer(domod, lhs, rhs)
                else:
                    assert False, "Internal error in multiplicativeExpression"

            lhs = lhsf(lhs)

        return lhs

    def powerExpression(self, l):
        lhs = self.unaryExpression(l)

        while self.peek(l, ['^']):
            op = l.pop(0)
            def lhsf(lhs):
                rhs = self.unaryExpression(l)
                return self.defer(lambda lhs, rhs: math.pow(self.aexpr(lhs), self.aexpr(rhs)),
                                  lhs, rhs)

            lhs = lhsf(lhs)

        return lhs

    def unaryExpression(self, l):
        if self.peek(l, [UNARY_MINUS]):
            op = l.pop(0)
            rhs = self.unaryExpression(l)
            return self.defer(lambda rhs: -self.aexpr(rhs), rhs)
        else:
            return self.finalExpression(l)

    def finalExpression(self, l):
        assert len(l), "Unexpected end of instructions"

        atom = l.pop(0)
        ty = self.Type(atom)

        if ty == 'array' or ty == 'list':
            return lambda: atom
        elif ty == 'word':
            if self.isNumber(atom):
                return lambda: float(atom)

            if atom[0] == '"' or atom[0] == "'":
                literal = atom[1:]
                return lambda: literal

            if atom[0] == ':':
                varname = atom[1:]
                return lambda: self.getvar(varname)

            if atom[0] == '(':
                # TODO: check for list-style procedure input calling syntax
                if len(l) and self.Type(l[0]) == 'word' and self.routines.has(str(l[0])):
                    if not (len(l) > 1 and self.Type(l[1]) == 'word' and self.isInfix(str(l[1]))):
                        atom = l.pop(0)
                        return self.dispatch(atom, l, False)

                result = self.expression(l)

                assert len(l), "Expecting ')', but list is empty"
                assert self.peek(l, [')']), "Expecting ')', but got something else"
                l.pop(0)
                return result

            if atom == ')':
                assert False, "Unexpected )"

            return self.dispatch(atom, l, True)
        else:
            assert False, "Internal error in finalExpression"

    def isInfix(self, word):
        return word in ['+', '-', '*', '/', '%', '^', '=', '<', '>', '<=', '>=', '<>']

    def isOperator(self, word):
        return self.isInfix(word) or word in ['[', ']', '{', '}', '(', ')']

    def dispatch(self, name, tokenlist, natural):
        name = name.upper()
        proc = self.routines.get(name)
        if proc is None:
            assert False, "ERROR: {} undefined".format(name)

        if proc['props'].get('special', False):
            self.stack.append(name)
            proc['code'](tokenlist)
            self.stack.pop()

            return lambda: None

        args = []
        if natural:
            # note: even in the original, this formulation prevents
            # and, or, etc. from being truly short-circuiting.

            for i in range(proc['props'].get('args')):
                args.append(self.expression(tokenlist))
        else:
            while len(tokenlist) and not self.peek(tokenlist, [')']):
                args.append(self.expression(tokenlist))

            tokenlist.pop(0) # )

            minargs = proc['props'].get('minimum', proc['props']['args'])
            maxargs = proc['props'].get('maximum', proc['props']['args'])

            assert not len(args) < minargs, "Too few arguments"
            if maxargs != -1:
                assert not len(args) > maxargs, "Too many arguments"

        if proc['props'].get('noeval', False):
            def noeval():
                self.stack.append(name)
                rv = proc['code'](*args)
                self.stack.pop()
                return rv

            return noeval

        def doeval():
            self.stack.append(name)
            a = [aa() for aa in args]
            rv = proc['code'](*a)
            self.stack.pop()
            return rv

        return doeval

    def aexpr(self, atom):
        if atom is not None and self.Type(atom) == 'word':
            if self.isNumber(atom):
                return float(atom)

        assert False, "Expecting number"

    def lexpr(self, atom):
        assert atom is not None
        if self.Type(atom) == 'word':
            raise NotImplementedError
        else:
            return self.copy(atom)

    def sexpr(self, atom):
        assert atom is not None
        if atom == UNARY_MINUS: return '-'
        if self.Type(atom) == 'word': return str(atom)

    def copy(self, value):
        if self.Type(value) == 'list':
            return list(value)
        else:
            return value

    def equal(self, a, b):
        at = self.Type(a)
        bt = self.Type(b)

        if at != bt: return False

        if at == 'word':
            if isinstance(a, (int, float)) or isinstance(b, (int, float)):
                return float(a) == float(b)
            else:
                return str(a) == str(b)
        elif at == 'list':
            if a.length != b.length:
                return False

            for i in range(len(a)):
                if not self.equal(a[i], b[i]):
                    return False

            return True
        elif at == 'array':
            raise NotImplementedError("equal for array types not implemented")

        assert False, "Unexpected flow in equal" # or return None?

