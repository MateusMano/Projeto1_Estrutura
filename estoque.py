"""Operacoes de estoque usando vetor nao ordenado e vetor ordenado."""

from produto import Produto, ValidacaoProdutoError


class EstoqueError(ValueError):
    """Erro para operacoes invalidas no estoque."""


class Estoque:
    """Controla produtos em dois vetores.

    produtos: vetor nao ordenado, usado para cadastro e busca linear por nome.
    produtos_ordenados: vetor ordenado por codigo, usado para busca binaria.
    """

    def __init__(self, produtos=None):
        self.produtos = []
        self.produtos_ordenados = []

        if produtos:
            for produto in produtos:
                self.cadastrar_produto(produto)

    def _buscar_indice_codigo(self, codigo):
        """Busca binaria.

        Retorna uma tupla (indice, encontrado). Se nao encontrado, indice indica
        a posicao correta de insercao para manter o vetor ordenado.
        """

        codigo = Produto.validar_codigo(codigo)
        inicio = 0
        fim = len(self.produtos_ordenados) - 1

        while inicio <= fim:
            meio = (inicio + fim) // 2
            codigo_meio = self.produtos_ordenados[meio].codigo

            if codigo_meio == codigo:
                return meio, True
            if codigo_meio < codigo:
                inicio = meio + 1
            else:
                fim = meio - 1

        return inicio, False

    def cadastrar_produto(self, produto):
        if not isinstance(produto, Produto):
            raise EstoqueError("Produto invalido.")

        indice, encontrado = self._buscar_indice_codigo(produto.codigo)
        if encontrado:
            raise EstoqueError("Ja existe um produto com esse codigo.")

        self.produtos.append(produto)
        self.produtos_ordenados.insert(indice, produto)

    def editar_produto(self, codigo, nome=None, categoria=None, preco=None,
                       quantidade=None):
        produto = self.buscar_por_codigo(codigo)
        if produto is None:
            raise EstoqueError("Produto nao encontrado.")

        produto.atualizar(
            nome=nome,
            categoria=categoria,
            preco=preco,
            quantidade=quantidade,
        )
        return produto

    def remover_produto(self, codigo):
        indice, encontrado = self._buscar_indice_codigo(codigo)
        if not encontrado:
            raise EstoqueError("Produto nao encontrado.")

        produto = self.produtos_ordenados.pop(indice)
        self.produtos.remove(produto)
        return produto

    def buscar_por_codigo(self, codigo):
        indice, encontrado = self._buscar_indice_codigo(codigo)
        if not encontrado:
            return None
        return self.produtos_ordenados[indice]

    def buscar_por_nome(self, termo):
        termo_normalizado = str(termo).strip().lower()
        if not termo_normalizado:
            raise EstoqueError("Informe um nome para buscar.")

        encontrados = []
        for produto in self.produtos:
            if termo_normalizado in produto.nome.lower():
                encontrados.append(produto)
        return encontrados

    def registrar_venda(self, codigo, quantidade_vendida):
        """Operacoes de estoque usando vetor nao ordenado e vetor ordenado."""

from produto import Produto, ValidacaoProdutoError


class EstoqueError(ValueError):
    """Erro para operacoes invalidas no estoque."""


class Estoque:
    """Controla produtos em dois vetores.

    produtos: vetor nao ordenado, usado para cadastro e busca linear por nome.
    produtos_ordenados: vetor ordenado por codigo, usado para busca binaria.
    """

    def __init__(self, produtos=None):
        self.produtos = []
        self.produtos_ordenados = []

        if produtos:
            for produto in produtos:
                self.cadastrar_produto(produto)

    def _buscar_indice_codigo(self, codigo):
        """Busca binaria.

        Retorna uma tupla (indice, encontrado). Se nao encontrado, indice indica
        a posicao correta de insercao para manter o vetor ordenado.
        """

        codigo = Produto.validar_codigo(codigo)
        inicio = 0
        fim = len(self.produtos_ordenados) - 1

        while inicio <= fim:
            meio = (inicio + fim) // 2
            codigo_meio = self.produtos_ordenados[meio].codigo

            if codigo_meio == codigo:
                return meio, True
            if codigo_meio < codigo:
                inicio = meio + 1
            else:
                fim = meio - 1

        return inicio, False

    def cadastrar_produto(self, produto):
        if not isinstance(produto, Produto):
            raise EstoqueError("Produto invalido.")

        indice, encontrado = self._buscar_indice_codigo(produto.codigo)
        if encontrado:
            raise EstoqueError("Ja existe um produto com esse codigo.")

        self.produtos.append(produto)
        self.produtos_ordenados.insert(indice, produto)

    def editar_produto(self, codigo, nome=None, categoria=None, preco=None,
                       quantidade=None):
        produto = self.buscar_por_codigo(codigo)
        if produto is None:
            raise EstoqueError("Produto nao encontrado.")

        produto.atualizar(
            nome=nome,
            categoria=categoria,
            preco=preco,
            quantidade=quantidade,
        )
        return produto

    def remover_produto(self, codigo):
        indice, encontrado = self._buscar_indice_codigo(codigo)
        if not encontrado:
            raise EstoqueError("Produto nao encontrado.")

        produto = self.produtos_ordenados.pop(indice)
        self.produtos.remove(produto)
        return produto

    def buscar_por_codigo(self, codigo):
        indice, encontrado = self._buscar_indice_codigo(codigo)
        if not encontrado:
            return None
        return self.produtos_ordenados[indice]

    def buscar_por_nome(self, termo):
        termo_normalizado = str(termo).strip().lower()
        if not termo_normalizado:
            raise EstoqueError("Informe um nome para buscar.")

        encontrados = []
        for produto in self.produtos:
            if termo_normalizado in produto.nome.lower():
                encontrados.append(produto)
        return encontrados

    def registrar_venda(self, codigo, quantidade_vendida):
        produto = self.buscar_por_codigo(codigo)
        if produto is None:
            raise EstoqueError("Produto nao encontrado.")

        try:
            quantidade = int(quantidade_vendida)
        except (TypeError, ValueError) as erro:
            raise EstoqueError("Quantidade da venda deve ser inteira.") from erro

        if quantidade <= 0:
            raise EstoqueError("Quantidade da venda deve ser maior que zero.")
        if quantidade > produto.quantidade:
            raise EstoqueError("Estoque insuficiente para essa venda.")

        produto.quantidade -= quantidade
        return produto

    def listar_ordenados_por_codigo(self):
        return list(self.produtos_ordenados)

    def listar_por_categoria(self, categoria):
        categoria_normalizada = str(categoria).strip().lower()
        if not categoria_normalizada:
            raise EstoqueError("Informe uma categoria.")

        produtos = [
            produto
            for produto in self.produtos_ordenados
            if produto.categoria.lower() == categoria_normalizada
        ]
        return produtos

    def relatorio_estoque_baixo(self, limite):
        try:
            limite = int(limite)
        except (TypeError, ValueError) as erro:
            raise EstoqueError("Limite deve ser um numero inteiro.") from erro

        if limite < 0:
            raise EstoqueError("Limite nao pode ser negativo.")

        return [
            produto
            for produto in self.produtos_ordenados
            if produto.quantidade < limite
        ]

    def produto_menor_preco(self):
        if not self.produtos:
            return None
        return min(self.produtos, key=lambda produto: produto.preco)

    def produto_maior_preco(self):
        if not self.produtos:
            return None
        return max(self.produtos, key=lambda produto: produto.preco)

    def total_produtos(self):
        return len(self.produtos)


def criar_produto(codigo, nome, categoria, preco, quantidade):
    """Funcao auxiliar para centralizar a criacao e suas validacoes."""

    try:
        return Produto(codigo, nome, categoria, preco, quantidade)
    except ValidacaoProdutoError:
        raise