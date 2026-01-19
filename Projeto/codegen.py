class CodeGenerator:
    def __init__(self, symtab):
        self.symtab = symtab
        self.code = []
        self.label_counter = 0

    # -------------------------------------------------
    # Utilitários
    # -------------------------------------------------
    def emit(self, instr):
        self.code.append(instr)

    def new_label(self, prefix="L"):
        self.label_counter += 1
        return f"{prefix}{self.label_counter}"
    
    # Converte dois operandos inteiros para real
    def _ensure_float_operands(self, lt, rt):
        # caso ambos já reais -> nada a fazer
        if lt == 'real' and rt == 'real':
            return

        # left real, right integer -> converter right (top)
        if lt == 'real' and rt != 'real':
            self.emit("ITOF")
            return

        # left integer, right real -> converter left
        if lt != 'real' and rt == 'real':
            self.emit("SWAP")
            self.emit("ITOF")
            self.emit("SWAP")
            return

        # ambos inteiros mas precisamos de reais converter ambos
        if lt != 'real' and rt != 'real':
            self.emit("ITOF")      # converte right (top)
            self.emit("SWAP")
            self.emit("ITOF")      # converte left (agora top)
            self.emit("SWAP")
            return
    
    
    
    
    # Usada para saber se a expressão é real (para, no caso dos reais, usar os "operadores" da MV
    #                                                      para os valores reais)
    def _expr_type(self, node):
        # node é AST; devolve 'integer' | 'real' | 'boolean' | 'string' | 'array' | None
        if node is None:
            return None
        tag = node[0]
        
        if tag == 'num':
            return 'real' if isinstance(node[1], float) else 'integer'
        
        if tag == 'string':
            return 'string'
        
        if tag == 'true' or tag == 'false':
            return 'boolean'
        
        if tag == 'id':
            sym = self.symtab.lookup(node[1])
            return sym.type_name if sym else None
        
        if tag == 'array_access':
            sym = self.symtab.lookup(node[1])
            return sym.elem_type if sym else None
        
        if tag == 'op':
            _, op, l, r = node
            lt = self._expr_type(l); rt = self._expr_type(r)
            
            if op == '/': return 'real'
            
            if op in ('div','mod'): return 'integer'
            
            if op in ('+','-','*'):
                return 'real' if (lt == 'real' or rt == 'real') else 'integer'
            
            
            if op in ('<','<=','>','>=','=','<>'):
                return 'boolean'
            
            if op in ('and','or'):
                return 'boolean'
            
        if tag in ('neg',):
            return self._expr_type(node[1])
        
        if tag in ('not',):
            return 'boolean'
        
        return None

    # -------------------------------------------------
    # Entrada principal
    # -------------------------------------------------
    def generate(self, ast):
        self.gen_program(ast)
        return "\n".join(self.code)

    def gen_program(self, node):
        # ('programa', nome, decls, bloco)
        _, _, _, bloco = node
        self.emit("START")
        self.gen_bloco(bloco)
        self.emit("STOP")

    def gen_bloco(self, node):
        # ('bloco_principal', [stmts])
        _, stmts = node
        for stmt in stmts:
            self.gen_stmt(stmt)

    # -------------------------------------------------
    # Statements
    # -------------------------------------------------
    def gen_stmt(self, node):
        tag = node[0]

        if tag == "atribuicao":
            self.gen_atribuicao(node)
        elif tag == "readln":
            self.gen_readln(node)
        elif tag == "writeln":
            self.gen_writeln(node)
        elif tag == "for_to":
            self.gen_for_to(node)
        elif tag == "while":
            self.gen_while(node)
        elif tag == "if" or tag == "ifelse":
            self.gen_if(node)
        elif tag == "atribuicao_array":
            self.gen_atribuicao_array(node)
        elif tag == "bloco":
            _, stmts = node
            for stmt in stmts:
                self.gen_stmt(stmt)
        else:
            raise NotImplementedError(f"Statement não implementado: {tag}")

    def gen_atribuicao(self, node):
        _, var, expr = node
        sym = self.symtab.lookup(var)
        expr_t = self._expr_type(expr)
        self.gen_expr(expr)
        if sym.type_name == 'real' and expr_t == 'integer':
            self.emit("ITOF")
        self.emit(f"STOREL {sym.offset}")

    def gen_readln(self, node):
        _, args = node
        for arg in args:
            tag = arg[0]

            if tag == "id":
                var = arg[1]
                sym = self.symtab.lookup(var)
                self.emit("READ")
                if hasattr(sym, "type_name") and sym.type_name == "integer":
                    self.emit("ATOI")
                if hasattr(sym, "type_name") and sym.type_name == "real":
                    self.emit("ATOF")
                self.emit(f"STOREL {sym.offset}")

            elif tag == "array_access":
                _, var, index_expr = arg
                sym = self.symtab.lookup(var)
                # calcular endereço do elemento
                self.emit("PUSHFP")
                self.emit(f"PUSHI {sym.offset}")
                self.emit("PADD")

                self.gen_expr(index_expr)
                if sym.lower is not None:
                    self.emit(f"PUSHI {sym.lower}")
                    self.emit("SUB")

                self.emit("PADD")        # address of element

                # ler e converter
                self.emit("READ")
                if hasattr(sym, "elem_type") and sym.elem_type == "integer":
                    self.emit("ATOI")
                elif hasattr(sym, "elem_type") and sym.elem_type == "real":
                    self.emit("ATOF")

                self.emit("STORE 0")     # store value at address

            else:
                raise NotImplementedError(f"Argumento READ/READLN não suportado: {tag}")

    def gen_writeln(self, node):
        _, exprs = node
        for expr in exprs:
            if expr[0] == "string":
                self.emit(f'PUSHS "{expr[1]}"')
                self.emit("WRITES")
            elif expr[0] == "boolean":
                self.emit(f"PUSHI {1 if expr[1] else 0}")
                self.emit("WRITEI")
            else:
                self.gen_expr(expr)
                t = self._expr_type(expr)
                if t == 'real':
                    self.emit("WRITEF")
                else:
                    self.emit("WRITEI")
                    
        self.emit("WRITELN")

    def gen_for_to(self, node):
        _, var, start, end, body = node
        sym_i = self.symtab.lookup(var)
        start_label = self.new_label("LOOP")
        end_label = self.new_label("END")
        # i := start
        self.gen_expr(start)
        self.emit(f"STOREL {sym_i.offset}")
        self.emit(f"{start_label}:")
        # condição: i <= end
        self.emit(f"PUSHL {sym_i.offset}")
        self.gen_expr(end)
        self.emit("INFEQ")
        self.emit(f"JZ {end_label}")
        # corpo
        self.gen_stmt(body)
        # i := i + 1
        self.emit(f"PUSHL {sym_i.offset}")
        self.emit("PUSHI 1")
        self.emit("ADD")
        self.emit(f"STOREL {sym_i.offset}")
        self.emit(f"JUMP {start_label}")
        self.emit(f"{end_label}:")

    def gen_while(self, node):
        _, cond, body = node
        start_label = self.new_label("WHILE")
        end_label = self.new_label("END")
        self.emit(f"{start_label}:")
        self.gen_expr(cond)
        self.emit(f"JZ {end_label}")
        self.gen_stmt(body)
        self.emit(f"JUMP {start_label}")
        self.emit(f"{end_label}:")

    def gen_if(self, node):
        tag = node[0]

        if tag == "if":
            _, cond, then_stmt = node
            else_stmt = None

        elif tag == "ifelse":
            _, cond, then_stmt, else_stmt = node


        else_label = self.new_label("ELSE")
        end_label = self.new_label("ENDIF")

        self.gen_expr(cond)
        self.emit(f"JZ {else_label}")

        self.gen_stmt(then_stmt)
        self.emit(f"JUMP {end_label}")
        self.emit(f"{else_label}:")

        if else_stmt:
            self.gen_stmt(else_stmt)
        self.emit(f"{end_label}:")
        
    def gen_atribuicao_array(self, node):
        _, var, index_expr, expr = node
        sym = self.symtab.lookup(var)
        # calcular endereço: base = FP + base_offset
        self.emit("PUSHFP")
        self.emit(f"PUSHI {sym.offset}")
        self.emit("PADD")                        # base address

        # empilha índice e normaliza (index - lower)
        self.gen_expr(index_expr)                # push index
        if sym.lower is not None:
            self.emit(f"PUSHI {sym.lower}")
            self.emit("SUB")                     # index - lower

        # adiciona o offset ao endereço:
        # stack: ..., base_addr, index_delta  -> PADD pop index_delta (n) and base_addr (a) -> push a + n
        self.emit("PADD")                        # address of element

        # empilha o valor a armazenar e faz STORE 0 (converte int -> real quando necessário)
        expr_t = self._expr_type(expr)
        self.gen_expr(expr)                      # push value
        if sym.elem_type == 'real' and expr_t == 'integer':
            self.emit("ITOF")
        self.emit("STORE 0")                     # store value at address

    # -------------------------------------------------
    # Expressões
    # -------------------------------------------------
    def gen_expr(self, node):
        tag = node[0]

        if tag == "num":
            v = node[1]
            if isinstance(v, float):
                self.emit(f"PUSHF {v}")
            else:
                self.emit(f"PUSHI {v}")

        elif tag == "id":
            sym = self.symtab.lookup(node[1])
            self.emit(f"PUSHL {sym.offset}")

        elif tag == "op":
            _, op, left, right = node
            lt = self._expr_type(left)
            rt = self._expr_type(right)

            # gerar código das subexpressões (empilha left then right)
            self.gen_expr(left)
            self.gen_expr(right)

            # Aritmética
            if op == "+":
                if lt == 'real' or rt == 'real':
                    self._ensure_float_operands(lt, rt)
                    self.emit("FADD")
                else:
                    self.emit("ADD")

            elif op == "-":
                if lt == 'real' or rt == 'real':
                    self._ensure_float_operands(lt, rt)
                    self.emit("FSUB")
                else:
                    self.emit("SUB")

            elif op == "*":
                if lt == 'real' or rt == 'real':
                    self._ensure_float_operands(lt, rt)
                    self.emit("FMUL")
                else:
                    self.emit("MUL")

            elif op == "/":
                # divisão real sempre
                self._ensure_float_operands(lt, rt)
                self.emit("FDIV")

            elif op == "div":
                self.emit("DIV")
            elif op == "mod":
                self.emit("MOD")

            # Comparadores
            elif op == "<=":
                if lt == 'real' or rt == 'real':
                    self._ensure_float_operands(lt, rt)
                    self.emit("FINFEQ")
                else:
                    self.emit("INFEQ")
            elif op == "<":
                if lt == 'real' or rt == 'real':
                    self._ensure_float_operands(lt, rt)
                    self.emit("FINF")
                else:
                    self.emit("INF")
            elif op == ">=":
                if lt == 'real' or rt == 'real':
                    self._ensure_float_operands(lt, rt)
                    self.emit("FSUPEQ")
                else:
                    self.emit("SUPEQ")
            elif op == ">":
                if lt == 'real' or rt == 'real':
                    self._ensure_float_operands(lt, rt)
                    self.emit("FSUP")
                else:
                    self.emit("SUP")

            # Lógicos e igualdade
            elif op == "and":
                self.emit("AND")
            elif op == "or":
                self.emit("OR")
            elif op == "=":
                if lt == 'real' or rt == 'real':
                    self._ensure_float_operands(lt, rt)
                self.emit("EQUAL")
            elif op == "<>":
                if lt == 'real' or rt == 'real':
                    self._ensure_float_operands(lt, rt)
                self.emit("EQUAL")
                self.emit("PUSHI 0")
                self.emit("EQUAL")
            else:
                raise NotImplementedError(f"Operador não suportado: {op}")
            
        elif tag == "neg":
            expr = node[1]
            t = self._expr_type(expr)
            if t == 'real':
                self.emit("PUSHF 0.0")
                self.gen_expr(expr)
                self.emit("FSUB")
            else:
                self.emit("PUSHI 0")
                self.gen_expr(expr)
                self.emit("SUB")

        elif tag == "not":
            self.gen_expr(node[1])
            self.emit("PUSHI 0")
            self.emit("EQUAL")

        elif tag == "true":
            self.emit("PUSHI 1")

        elif tag == "false":
            self.emit("PUSHI 0")
        
        elif tag == "array_access":
            _, var, index_expr = node
            sym = self.symtab.lookup(var)
            # base address
            self.emit("PUSHFP")
            self.emit(f"PUSHI {sym.offset}")
            self.emit("PADD")

            # índice
            self.gen_expr(index_expr)
            if sym.lower is not None:
                self.emit(f"PUSHI {sym.lower}")
                self.emit("SUB")

            # adiciona índice ao endereço
            self.emit("PADD")

            # carrega valor do endereço
            self.emit("LOAD 0")

        else:
            raise NotImplementedError(f"Expressão não implementada: {tag}")