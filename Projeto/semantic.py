# Exceção personalizada usada para sinalizar erros semânticos
# relacionados com declarações (ex.: variáveis duplicadas).
class SemanticError(Exception):
    pass


# ------------------------------------------------------------
#   Representação de um símbolo (variável ou array)
# ------------------------------------------------------------
class Symbol:
    def __init__(self, name, kind, type_name, offset=None):
        """
        Representa um símbolo na tabela de símbolos.
        
        name: nome do identificador (ex.: 'x', 'vetor')
        kind: 'var' ou 'array'
        type_name: tipo base (ex.: 'integer', 'real', 'string', 
                               ou 'array' no caso de arrays)
        """

        self.name = name        # nome da variável
        self.kind = kind        # 'var' ou 'array'
        self.type_name = type_name  # tipo primitivo ou 'array'
        self.offset = offset

        # Campos específicos para arrays
        self.lower = None       # limite inferior (ex.: 1)
        self.upper = None       # limite superior (ex.: 10)
        self.elem_type = None   # tipo dos elementos (ex.: 'integer')



# ------------------------------------------------------------
#   Tabela de Símbolos 
# ------------------------------------------------------------
class SymbolTable:
    def __init__(self):
        # Dicionário: nome → Symbol
        self._symbols = {}
        self._next_offset = 0

    def define_var(self, name, type_name):
        """
        Regista uma variável simples na tabela.
        Se já existir, lança erro semântico.
        """
        if name in self._symbols:
            raise SemanticError(f"Variável '{name}' já declarada.")
        
        s = Symbol(name, 'var', type_name, self._next_offset)
        self._symbols[name] = s
        self._next_offset += 1
        return s

    def define_array(self, name, lower, upper, elem_type):
        if name in self._symbols:
            raise SemanticError(f"Variável/array '{name}' já declarada.")
        
        # define base offset antes de reservar elementos
        s = Symbol(name, 'array', 'array', self._next_offset)
        s.lower = lower
        s.upper = upper
        s.elem_type = elem_type
        
        # reservar slots para os elementos
        size = (upper - lower + 1)
        self._next_offset += size

        self._symbols[name] = s
        return s

    def lookup(self, name):
        """Procura um símbolo pelo nome. Devolve None se não existir."""
        return self._symbols.get(name, None)

    def items(self):
        """Retorna todos os símbolos (útil para debug)."""
        return list(self._symbols.items())


# ============================================================
#              ANALISADOR SEMÂNTICO PRINCIPAL
# ============================================================
class SemanticAnalyzer:
    def __init__(self):
        self.symtab = SymbolTable()  # tabela de símbolos
        self.errors = []            # lista de erros encontrados

    # --------------------------------------------------------
    # Normalização de tipos vindos do parser
    # --------------------------------------------------------
    def _norm_type_token(self, t):
        """
        Converte tipos do AST para uma forma uniforme.
        
        - Converte strings para minúsculas: 'INTEGER' → 'integer'
        - Mantém a estrutura de arrays: ('array', (1,10), 'integer')
        """
        if t is None:
            return None

        # Caso seja um tuple → pode ser um array
        if isinstance(t, tuple):
            if len(t) >= 3 and t[0] == 'array':
                interval = t[1]
                elem = t[2]

                # Normaliza o tipo do elemento
                if isinstance(elem, str):
                    elem_norm = elem.lower()
                else:
                    elem_norm = self._norm_type_token(elem)

                return ('array', interval, elem_norm)
            return t

        # Caso seja string → normaliza minúsculas
        if isinstance(t, str):
            return t.lower()

        return t

    # Regista erro na lista interna
    def error(self, msg):
        self.errors.append(msg)

    # --------------------------------------------------------
    # Função principal da análise semântica
    # --------------------------------------------------------
    def analyze(self, ast):
        """
        Recebe o AST produzido pelo parser e verifica:
        - declarações
        - tipos
        - comandos
        - expressões
        - acessos a arrays
        """

        self.errors = []  # limpar erros anteriores

        # O nó raiz deve ser ('programa', ...)
        if not isinstance(ast, tuple) or len(ast) < 1 or ast[0] != 'programa':
            self.error("AST inválida: nó raiz não é 'programa'.")
            return False

        # Extrair componentes do nó principal
        try:
            prog_name = ast[1]
            declarations = ast[2]
            block_node = ast[3]
        except Exception:
            self.error("AST com estrutura inesperada.")
            return False

        # Processar declarações de variáveis/arrays
        self._process_declarations(declarations)

        # Extrair comando(s) do bloco principal
        commands = []
        if isinstance(block_node, tuple) and (block_node[0] == 'bloco_principal' or block_node[0] == 'bloco'):
            commands = block_node[1]
        elif isinstance(block_node, list):
            commands = block_node
        else:
            self.error("Bloco principal com formato inesperado.")
            return False

        # Analisar cada comando
        if isinstance(commands, list):
            for cmd in commands:
                self._process_command(cmd)
        else:
            self._process_command(commands)

        # Se não houver erros, devolve True
        return len(self.errors) == 0

    
    # ============================================================
    # DECLARAÇÕES
    # ============================================================
    def _process_declarations(self, decls):
        """
        Processa a lista de declarações vinda do parser.

        Espera algo do género:
            [
                ('decl', ['x','y'], 'integer'),
                ('decl', ['vet'], ('array', (1,5), 'integer')),
                ...
            ]

        O objetivo é:
        - Verificar tipos válidos
        - Registar variáveis na tabela de símbolos
        - Verificar arrays e respetivos limites
        - Detetar duplicações e tipos inexistentes
        """

        if decls is None:
            # Não há declarações → OK
            return

        # Cada elemento deve ser ('decl', lista_ids, tipo)
        
        for decl in decls:
            
            # Verificação de formato
            if not isinstance(decl, tuple) or len(decl) < 3 or decl[0] != 'decl':
                self.error(f"Declaração inválida no AST: {decl}")
                continue
            
            ids = decl[1]        # lista de identificadores declarados
            vtype = decl[2]      # tipo tal como vem do parser
            vtype_norm = self._norm_type_token(vtype)  # tipo normalizado
            

            # =====================================================
            # CASO 1 — DECLARAÇÃO DE ARRAY
            # =====================================================
            
            if isinstance(vtype_norm, tuple) and vtype_norm[0] == 'array':
                intervalo = vtype_norm[1]   # (lower, upper)
                elem_type = vtype_norm[2]   # (lower, upper)
                
                # Validar estrutura do intervalo
                if (not isinstance(intervalo, tuple)) or len(intervalo) != 2:
                    self.error(f"Intervalo inválido para array em declaração {decl}.")
                    continue
                low = intervalo[0]
                high = intervalo[1]
                
                # Validar limites do array
                if not isinstance(low, int) or not isinstance(high, int):
                    self.error(f"Intervalo do array deve ser números inteiros: {intervalo}")
                    continue
                
                if low > high:
                    self.error(f"Intervalo inválido (lower > upper): {intervalo}")
                    continue
                
                # Registar cada identificador como array
                for name in ids:
                    try:
                        self.symtab.define_array(name, low, high, elem_type)
                    except SemanticError as e:
                        self.error(str(e))
                        

            # =====================================================
            # CASO 2 — TIPO SIMPLES (integer, real, boolean, string)
            # =====================================================
            else:
                
                # Se o tipo normalizado é uma string → é tipo primitivo
                if isinstance(vtype_norm, str):
                    
                    for name in ids:
                        try:
                            # Regista variável simples
                            self.symtab.define_var(name, vtype_norm)
                        except SemanticError as e:
                            # Ex.: variável repetida
                            self.error(str(e))

                else:
                    # Apanhou algo que não reconhecemos como tipo
                    self.error(f"Tipo de declaração desconhecido: {vtype} (declaracao {decl})")

    # ============================================================
    # COMANDOS
    # ============================================================
    
    def _process_command(self, cmd):
        """
        Recebe um comando (ou lista de comandos) do AST e realiza análise semântica.
        Valida:
            - existência de variáveis/arrays
            - tipos de atribuição
            - condições booleanas
            - limites de arrays
            - chamadas de leitura/escrita
            - expressões
        """
        if cmd is None:
            return

        # Se for uma lista de comandos, processa cada um recursivamente
        if isinstance(cmd, list):
            for c in cmd:
                self._process_command(c)
            return

        # Validação básica do formato do comando
        if not isinstance(cmd, tuple) or len(cmd) == 0:
            self.error(f"Comando inválido no AST: {cmd}")
            return

        kind = cmd[0]  # tipo de comando (ex.: 'atribuicao', 'writeln', 'if', ...)

        # ----------------------------------------------------
        # Atribuição simples: ('atribuicao', var, expr)
        # ----------------------------------------------------
        
        if kind == 'atribuicao':
            var_name = cmd[1]
            expr = cmd[2]
            symbol = self.symtab.lookup(var_name) # verifica se a variável existe
            if symbol is None:
                self.error(f"Atribuição a variável não declarada '{var_name}'.")
                self._eval_expr_type(expr)  # avalia expressão mesmo assim, para pegar mais erros
                return
            expr_type = self._eval_expr_type(expr)  # obtém tipo da expressão
            self._check_assignment_types(symbol, expr_type, var_name)  # verifica compatibilidade de tipos
        

        # ----------------------------------------------------
        # Atribuição a arrays: ('atribuicao_array', name, index_expr, expr)
        # ----------------------------------------------------
        
        
        elif kind == 'atribuicao_array':
            name = cmd[1]
            index_expr = cmd[2]
            expr = cmd[3]
            symbol = self.symtab.lookup(name)
            if symbol is None:
                self.error(f"Atribuição a array não declarado '{name}'.")
                self._eval_expr_type(index_expr)
                self._eval_expr_type(expr)
                return
            if symbol.kind != 'array':
                self.error(f"Identificador '{name}' não é um array.")
                self._eval_expr_type(index_expr)
                self._eval_expr_type(expr)
                return
            idx_type = self._eval_expr_type(index_expr)
            if idx_type != 'integer':
                self.error(f"Índice do array '{name}' deve ser integer, obteve '{idx_type}'.")
            
            # Verificação de limites se o índice for literal
            if isinstance(index_expr, tuple) and index_expr[0] == 'num' and isinstance(index_expr[1], int):
                idx_val = index_expr[1]
                if idx_val < symbol.lower or idx_val > symbol.upper:
                    self.error(f"Índice {idx_val} fora dos limites do array '{name}' [{symbol.lower}..{symbol.upper}].")
                    
            expr_type = self._eval_expr_type(expr)
            if expr_type is not None:
                
                if symbol.elem_type == expr_type:
                    pass
                
                # Permite int -> real, caso esse seja um elemento de um array
                elif symbol.elem_type == 'real' and expr_type == 'integer':
                    pass
                
                else:
                    self.error(f"Tipo incompatível na atribuição ao array '{name}': elemento é '{symbol.elem_type}', expressão é '{expr_type}'.")

        
        # ----------------------------------------------------
        # Comando de escrita: writeln
        # ----------------------------------------------------
        
        elif kind == 'writeln':
            exprs = cmd[1]
            if not isinstance(exprs, list):
                self.error(f"writeln: argumentos inválidos {exprs}")
                return
            for e in exprs:
                t = self._eval_expr_type(e)
                if t is None:
                    continue  # erro já reportado
                
                # writeln só aceita tipos imprimíveis
                if t not in ('integer', 'real', 'boolean', 'string'):
                    self.error(f"writeln: tipo não imprimível '{t}' (expr {e}).")


        # ----------------------------------------------------
        # Comando de leitura: readln
        # ----------------------------------------------------
        
        elif kind == 'readln':
            args = cmd[1]

            # garantir lista de argumentos
            if not isinstance(args, list):
                args = [args]

            for a in args:
                
                # caso 1: variável simples
                if isinstance(a, tuple) and a[0] == 'id':
                    vname = a[1]
                    symbol = self.symtab.lookup(vname)
                    
                    if symbol is None:
                        self.error(f"readln: variável '{vname}' não declarada.")
                    else:
                        if symbol.kind != 'var':
                            self.error(f"readln: destino '{vname}' não é variável.")
                        elif symbol.type_name not in ('integer', 'real', 'string'):
                            self.error(f"readln: tipo de '{vname}' não suportado para readln ('{symbol.type_name}').")

                # caso 2: acesso a array
                elif isinstance(a, tuple) and a[0] == 'array_access':
                    arr_name = a[1]
                    idx_expr = a[2]

                    symbol = self.symtab.lookup(arr_name)
                    if symbol is None:
                        self.error(f"readln: array '{arr_name}' não declarado.")
                        continue

                    if symbol.kind != 'array':
                        self.error(f"readln: '{arr_name}' não é um array.")
                        continue

                    # índice deve ser integer
                    idx_type = self._eval_expr_type(idx_expr)
                    if idx_type != 'integer':
                        self.error(f"readln: índice do array '{arr_name}' deve ser integer, obteve '{idx_type}'.")

                    # se índice literal, verifica limites
                    if isinstance(idx_expr, tuple) and idx_expr[0] == 'num':
                        v = idx_expr[1]
                        if v < symbol.lower or v > symbol.upper:
                            self.error(f"readln: índice {v} fora dos limites do array '{arr_name}' [{symbol.lower}..{symbol.upper}].")
                            
                    # Verifica tipo do elemento do array para readln
                    if symbol.elem_type not in ('integer', 'real', 'string'):
                        self.error(f"readln: tipo de elemento do array '{arr_name}' não suportado para readln ('{symbol.elem_type}').")

                # caso inválido
                else:
                    self.error(f"readln: destino inválido '{a}'.")


        # ----------------------------------------------------
        # Condicionais
        # ----------------------------------------------------
        
        elif kind == 'if':
            
            cond = cmd[1]
            then_cmd = cmd[2]
            ctype = self._eval_expr_type(cond)
            if ctype != 'boolean':
                self.error(f"Condição do IF deve ser boolean, obteve '{ctype}'.")
            
            # then_cmd pode ser statement or bloco
            self._process_command(then_cmd)

        elif kind == 'ifelse':
            cond = cmd[1]; then_cmd = cmd[2]; else_cmd = cmd[3]
            ctype = self._eval_expr_type(cond)
            if ctype != 'boolean':
                self.error(f"Condição do IF deve ser boolean, obteve '{ctype}'.")
            self._process_command(then_cmd)
            self._process_command(else_cmd)

        # ----------------------------------------------------
        # Ciclos
        # ----------------------------------------------------
        
        elif kind == 'while':
            cond = cmd[1]; body = cmd[2]
            ctype = self._eval_expr_type(cond)
            if ctype != 'boolean':
                self.error(f"Condição do WHILE deve ser boolean, obteve '{ctype}'.")
            self._process_command(body)


        elif kind in ('for_to', 'for_down'):
            var_name = cmd[1]; start_expr = cmd[2]; end_expr = cmd[3]; body = cmd[4]
            
            symbol = self.symtab.lookup(var_name)
            
            if symbol is None:
                self.error(f"Variável de controlo do FOR '{var_name}' não declarada.")
            else:
                if symbol.kind != 'var' or symbol.type_name != 'integer':
                    self.error(f"Variável de controlo do FOR '{var_name}' deve ser integer.")
            
            s_type = self._eval_expr_type(start_expr)
            e_type = self._eval_expr_type(end_expr)
            
            if s_type != 'integer' or e_type != 'integer':
                self.error(f"Expressões de início/fim do FOR devem ser integer (obtido: {s_type}, {e_type}).")
                
            self._process_command(body)

        # ----------------------------------------------------
        # Blocos de comandos
        # ----------------------------------------------------
        elif kind in ('bloco', 'bloco_principal'):
            cmds = cmd[1]
            if isinstance(cmds, list):
                for c in cmds:
                    self._process_command(c)
            else:
                self._process_command(cmds)

        # ----------------------------------------------------
        # Comando desconhecido/fallback
        # ----------------------------------------------------
        else:
            # fallback: se for lista, processa cada elemento
            if isinstance(cmd, list):
                for c in cmd:
                    self._process_command(c)
            else:
                self.error(f"Comando desconhecido no analisador semântico: {cmd}")


    # -------------------------
    # Avaliação de expressões (retorna tipo ou None)
    # -------------------------
    def _eval_expr_type(self, expr):
        
        # Se a expressão é None, sinaliza erro e retorna None
        if expr is None:
            self.error("Expressão inesperada: None")
            return None

        # Se a expressão não é uma tupla (formato AST esperado), sinaliza erro
        if not isinstance(expr, tuple):
            self.error(f"Expressão com formato inesperado: {expr}")
            return None

        tag = expr[0]  # identificador do tipo de nó da AST

        # -----------------
        # Literais
        # -----------------
        
        if tag == 'num':
            # expr = ('num', valor)
            v = expr[1]
            
            # Distinção entre integer e real
            if isinstance(v, int):
                return 'integer'
            else:
                return 'real'

        if tag == 'string':
            return 'string'

        if tag == 'true' or tag == 'false':
            return 'boolean'

        # -----------------
        # Identificadores
        # -----------------
        
        if tag == 'id':
            name = expr[1]
            symbol = self.symtab.lookup(name)  # procura na tabela de símbolos
            if symbol is None:
                self.error(f"Uso de variável não declarada '{name}'.")
                return None
            if symbol.kind == 'var':
                return symbol.type_name
            elif symbol.kind == 'array':
                return 'array'
            else:
                self.error(f"Símbolo '{name}' com tipo desconhecido.")
                return None

        # -----------------
        # Acesso a arrays
        # -----------------
        
        if tag == 'array_access':
            # expr = ('array_access', nome_array, expr_indice)
            name = expr[1]; idx = expr[2]
            symbol = self.symtab.lookup(name)
            
            if symbol is None:
                self.error(f"Acesso a array não declarado '{name}'.")
                self._eval_expr_type(idx)  # avalia índice mesmo assim para capturar possíveis erros
                return None
            
            if symbol.kind != 'array':
                self.error(f"Identificador '{name}' não é um array.")
                self._eval_expr_type(idx)
                return None
            
            idx_type = self._eval_expr_type(idx)
            
            if idx_type != 'integer':
                self.error(f"Índice do array '{name}' deve ser integer, obteve '{idx_type}'.")
                
            # Verifica limites se índice é literal
            if isinstance(idx, tuple) and idx[0] == 'num' and isinstance(idx[1], int):
                v = idx[1]
                if v < symbol.lower or v > symbol.upper:
                    self.error(f"Índice {v} fora dos limites do array '{name}' [{symbol.lower}..{symbol.upper}].")
                    
            return symbol.elem_type

        # -----------------
        # Operadores binários
        # -----------------
        
        if tag == 'op':
            # expr = ('op', operador, left, right)
            op = expr[1]
            left = expr[2]
            right = expr[3]
            
            # Avalia tipos das subexpressões
            lt = self._eval_expr_type(left); rt = self._eval_expr_type(right)
            if lt is None or rt is None:
                return None

            lop = str(op).lower()

            # Operadores aritméticos + - *
            if lop in ('+', '-', '*'):
                if lt in ('integer','real') and rt in ('integer','real'):
                    # Se um dos operandos é real, resultado é real
                    if lt == 'real' or rt == 'real':
                        return 'real'
                    return 'integer'
                self.error(f"Operador '{op}' exige operandos numéricos (integer/real). Obteve: '{lt}' e '{rt}'.")
                return None

            # Divisão real
            if lop == '/':
                if lt in ('integer','real') and rt in ('integer','real'):
                    return 'real'
                self.error(f"Operador '/' exige operandos numéricos (integer/real). Obteve: '{lt}' e '{rt}'.")
                return None

            # div / mod -> apenas inteiros
            if lop in ('div', 'mod'):
                if lt == 'integer' and rt == 'integer':
                    return 'integer'
                self.error(f"Operador '{lop}' exige operandos integer. Obteve: '{lt}' e '{rt}'.")
                return None

            # Operadores relacionais
            if lop in ('=', '<>'):
                # igualdade permitida entre tipos escalares compatíveis
                if lt == rt:
                    return 'boolean'
                if (lt in ('integer','real')) and (rt in ('integer','real')):
                    return 'boolean'
                self.error(f"Operador '{op}': tipos incompatíveis para comparação: '{lt}' vs '{rt}'.")
                return None

            if lop in ('<', '>', '<=', '>='):
                # apenas números ou strings
                if (lt in ('integer','real') and rt in ('integer','real')) or (lt == 'string' and rt == 'string'):
                    return 'boolean'
                self.error(f"Operador relacional '{op}' só admite números ou strings (obtido '{lt}' e '{rt}').")
                return None

            # Operadores lógicos
            if lop in ('and','or'):
                if lt == 'boolean' and rt == 'boolean':
                    return 'boolean'
                self.error(f"Operador lógico '{op}' exige operandos boolean (obtido '{lt}' e '{rt}').")
                return None

            # Operador desconhecido
            self.error(f"Operador desconhecido ou não suportado: '{op}'.")
            return None
        
        # -----------------
        # Operadores unários
        # -----------------
        
        if tag == 'neg':
            t = self._eval_expr_type(expr[1])
            if t not in ('integer','real'):
                self.error(f"Operador unário '-' aplicado a tipo não-número: '{t}'.")
                return None
            return t

        if tag == 'not':
            t = self._eval_expr_type(expr[1])
            if t != 'boolean':
                self.error(f"Operador 'not' aplicado a tipo não-booleano: '{t}'.")
                return None
            return 'boolean'

        # -----------------
        # Caso não reconhecido
        # -----------------
        self.error(f"Expressão desconhecida no analisador semântico: {expr}")
        return None


    # -------------------------
    # Verificação de tipos em atribuições
    # -------------------------
    def _check_assignment_types(self, symbol, expr_type, var_name):
        
        # Se o tipo da expressão não foi determinado, não faz sentido continuar
        if expr_type is None:
            return
        
        # Se o símbolo é uma variável (não array ou outro tipo)
        if symbol.kind == 'var':
            var_type = symbol.type_name  # tipo da variável declarada
            
            # Pascal exige correspondência estrita de tipos em atribuição
            if var_type == expr_type:
                return  # tudo correto
            
            # Permite int -> real
            if var_type == 'real' and expr_type == 'integer':
                return
            
            # Não permite real -> int
            if var_type == 'integer' and expr_type == 'real':
                self.error(f"Incompatibilidade de tipos na atribuição a '{var_name}': atribuição real→integer não permitida.")
                return

            # Se tipos incompatíveis, registra erro semântico
            self.error(f"Incompatibilidade de tipos na atribuição a '{var_name}': variável é '{var_type}' mas expressão é '{expr_type}'.")
        else:
            # Se o símbolo não é uma variável, não podemos atribuir valor
            self.error(f"Tentativa de atribuição a símbolo não variável '{var_name}'.")

    # -------------------------
    # Relatório de erros semânticos
    # -------------------------
    def report_errors(self):
        # Se não há erros, indica sucesso
        if not self.errors:
            print("Análise semântica concluída: sem erros.")
            return
        
        # Se há erros, imprime todos
        print("Erros semânticos encontrados:")
        for e in self.errors:
            print(" -", e)