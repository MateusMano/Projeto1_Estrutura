from dataclasses import asdict, dataclass


class ValidacaoProdutoError(ValueError):
    """Erro usado quando um produto nao respeita as regras de negocio."""


@dataclass
class Produto:
    

    codigo: int
    nome: str
    categoria: str
    preco: float
    quantidade: int

    def __post_init__(self):
        self.codigo = self.validar_codigo(self.codigo)
        self.nome = self.validar_texto(self.nome, "nome")
        self.categoria = self.validar_texto(self.categoria, "categoria")
        self.preco = self.validar_preco(self.preco)
        self.quantidade = self.validar_quantidade(self.quantidade)

    @staticmethod
    def validar_codigo(valor):
        try:
            codigo = int(valor)
        except (TypeError, ValueError) as erro:
            raise ValidacaoProdutoError("Codigo deve ser um numero inteiro.") from erro

        if codigo <= 0:
            raise ValidacaoProdutoError("Codigo deve ser maior que zero.")
        return codigo

    @staticmethod
    def validar_texto(valor, campo):
        texto = str(valor).strip()
        if not texto:
            raise ValidacaoProdutoError(f"{campo.capitalize()} nao pode ficar vazio.")
        return texto

    @staticmethod
    def validar_preco(valor):
        try:
            preco = float(valor)
        except (TypeError, ValueError) as erro:
            raise ValidacaoProdutoError("Preco deve ser um numero.") from erro

        if preco <= 0:
            raise ValidacaoProdutoError("Preco deve ser positivo.")
        return preco

    @staticmethod
    def validar_quantidade(valor):
        try:
            quantidade = int(valor)
        except (TypeError, ValueError) as erro:
            raise ValidacaoProdutoError(
                "Quantidade deve ser um numero inteiro."
            ) from erro

        if quantidade < 0:
            raise ValidacaoProdutoError("Quantidade nao pode ser negativa.")
        return quantidade

    def atualizar(self, nome=None, categoria=None, preco=None, quantidade=None):
        

        produto_validado = Produto(
            codigo=self.codigo,
            nome=self.nome if nome is None else nome,
            categoria=self.categoria if categoria is None else categoria,
            preco=self.preco if preco is None else preco,
            quantidade=self.quantidade if quantidade is None else quantidade,
        )

        self.nome = produto_validado.nome
        self.categoria = produto_validado.categoria
        self.preco = produto_validado.preco
        self.quantidade = produto_validado.quantidade

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, dados):
        return cls(
            codigo=dados["codigo"],
            nome=dados["nome"],
            categoria=dados["categoria"],
            preco=dados["preco"],
            quantidade=dados["quantidade"],
        )