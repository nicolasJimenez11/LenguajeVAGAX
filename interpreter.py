from grammar.generated.VagaxParserVisitor import VagaxParserVisitor
from grammar.generated.VagaxParser import VagaxParser


class VAGAXInterpreter(VagaxParserVisitor):

    def __init__(self):
        self.variables = {}
        self.functions = {}

    # -------- PROGRAMA --------

    def visitProgram(self, ctx):
        for stmt in ctx.statement():
            self.visit(stmt)

    # -------- STATEMENT --------

    def visitStatement(self, ctx):

        if ctx.expr():
            result = self.visit(ctx.expr())

            if result is not None:
                print(result)

            return result

        return self.visitChildren(ctx)

    # -------- BLOQUE --------

    def visitBlock(self, ctx):

        for stmt in ctx.statement():
            self.visit(stmt)

    # -------- DECLARACIÓN DE VARIABLES --------

    def visitVarDecl(self, ctx):

        name = ctx.ID().getText()

        if ctx.expr():
            value = self.visit(ctx.expr())
        else:
            value = None

        self.variables[name] = value

    # -------- ASIGNACIÓN --------

    def visitAssignment(self, ctx):

        name = ctx.ID().getText()
        value = self.visit(ctx.expr())

        if name not in self.variables:
            self.variables[name] = None

        self.variables[name] = value

    # -------- IF --------

    def visitIfStatement(self, ctx):

        condition = self.visit(ctx.expr())

        if condition:
            self.visit(ctx.block(0))
        else:
            if ctx.ELSE():
                self.visit(ctx.block(1))

    # -------- WHILE --------

    def visitWhileStatement(self, ctx):

        while self.visit(ctx.expr()):
            self.visit(ctx.block())

    # -------- FOR --------

    def visitForStatement(self, ctx):

        # inicialización
        self.visit(ctx.assignment(0))

        # condición
        while self.visit(ctx.expr()):

            # ejecutar bloque
            self.visit(ctx.block())

            # actualización
            self.visit(ctx.assignment(1))

    # -------- DECLARACIÓN DE FUNCIÓN --------

    def visitFunctionDecl(self, ctx):

        name = ctx.ID().getText()

        params = []

        if ctx.paramList():
            params = [p.getText() for p in ctx.paramList().ID()]

        self.functions[name] = {
            "params": params,
            "ctx": ctx
        }

    # -------- LLAMADA A FUNCIÓN --------

    def visitFunctionCall(self, ctx):

        name = ctx.ID().getText()

        if name not in self.functions:
            raise Exception(f"Función no definida: {name}")

        func = self.functions[name]
        params = func["params"]

        args = []
        if ctx.argList():
            args = [self.visit(e) for e in ctx.argList().expr()]

        if len(args) != len(params):
            raise Exception(
                f"La función {name} esperaba {len(params)} argumentos y recibió {len(args)}"
            )

        local_vars = dict(zip(params, args))

        old_vars = self.variables
        self.variables = {**old_vars, **local_vars}

        result = None

        for stmt in func["ctx"].block().statement():

            if stmt.returnStmt():
                result = self.visit(stmt.returnStmt().expr())
                break

            self.visit(stmt)

        self.variables = old_vars

        return result

    # -------- EXPRESIONES --------

    def visitExpr(self, ctx):

        # literal
        if ctx.literal():
            return self.visit(ctx.literal())

        # llamada a función
        if ctx.functionCall():
            return self.visit(ctx.functionCall())

        # variable
        if ctx.ID():
            name = ctx.ID().getText()

            if name not in self.variables:
                raise Exception(f"Variable no definida: {name}")

            return self.variables[name]

        # paréntesis
        if ctx.getChildCount() == 3 and ctx.getChild(0).getText() == "(":
            return self.visit(ctx.expr(0))

        # operaciones
        if ctx.getChildCount() == 3:

            left = self.visit(ctx.expr(0))
            right = self.visit(ctx.expr(1))
            op = ctx.getChild(1).getText()

            if op == '+':
                return left + right

            if op == '-':
                return left - right

            if op == '*':
                return left * right

            if op == '/':
                return left / right

            if op == '%':
                return left % right

            if op == '^':
                return left ** right

            if op == '==':
                return left == right

            if op == '!=':
                return left != right

            if op == '<':
                return left < right

            if op == '>':
                return left > right

            if op == '<=':
                return left <= right

            if op == '>=':
                return left >= right

            if op == '&&':
                return left and right

            if op == '||':
                return left or right

        # NOT
        if ctx.getChildCount() == 2:
            val = self.visit(ctx.expr(0))
            return not val

    # -------- LITERALES --------

    def visitLiteral(self, ctx):

        if ctx.NUMBER():
            text = ctx.NUMBER().getText()

            if "." in text:
                return float(text)
            else:
                return int(text)

        if ctx.STRING():
            return ctx.STRING().getText().strip('"')

        if ctx.BOOL_LIT():

            val = ctx.BOOL_LIT().getText()

            if val == "sisas":
                return True
            else:
                return False
