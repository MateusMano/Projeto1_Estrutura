from pathlib import Path

from arquivos import ArquivoError, carregar_produtos, registrar_log, salvar_produtos
from estoque import Estoque, EstoqueError, criar_produto
from produto import ValidacaoProdutoError


BASE_DIR = Path(__file__).resolve().parent
CAMINHO_DADOS = BASE_DIR / "dados" / "produtos.json"
CAMINHO_LOG = BASE_DIR / "dados" / "operacoes.log"
TAMANHO_PAGINA = 5


def ler_texto(mensagem, permitir_vazio=False):
    while True:
        valor = input(mensagem).strip()
        if valor or permitir_vazio:
            return valor
        print("Entrada vazia. Tente novamente.")


def ler_inteiro(mensagem, minimo=None, permitir_vazio=False):
    while True:
        valor = input(mensagem).strip()
        if permitir_vazio and valor == "":
            return None

        try:
            numero = int(valor)
        except ValueError:
            print("Digite um numero inteiro valido.")
            continue

        if minimo is not None and numero < minimo:
            print(f"Digite um valor maior ou igual a {minimo}.")
            continue
        return numero


def ler_float(mensagem, minimo=None, permitir_vazio=False):
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        if permitir_vazio and valor == "":
            return None

        try:
            numero = float(valor)
        except ValueError:
            print("Digite um numero valido.")
            continue

        if minimo is not None and numero < minimo:
            print(f"Digite um valor maior ou igual a {minimo}.")
            continue
        return numero


def formatar_produto(produto):
    return (
        f"{produto.codigo:<6} | {produto.nome:<25} | "
        f"{produto.categoria:<15} | R$ {produto.preco:>8.2f} | "
        f"Qtd: {produto.quantidade:>4}"
    )


def mostrar_produto(produto):
    print(formatar_produto(produto))


def mostrar_lista(produtos):
    if not produtos:
        print("Nenhum produto encontrado.")
        return

    total = len(produtos)
    for inicio in range(0, total, TAMANHO_PAGINA):
        pagina = produtos[inicio:inicio + TAMANHO_PAGINA]
        print("\nCodigo | Nome                      | Categoria       | Preco      | Qtd")
        print("-" * 76)
        for produto in pagina:
            mostrar_produto(produto)

        if inicio + TAMANHO_PAGINA < total:
            input("\nPressione Enter para ver mais...")


def salvar_estado(estoque):
    salvar_produtos(CAMINHO_DADOS, estoque.listar_ordenados_por_codigo())


def cadastrar_produto(estoque):
    print("\nCadastro de produto")
    codigo = ler_inteiro("Codigo: ", minimo=1)
    nome = ler_texto("Nome: ")
    categoria = ler_texto("Categoria: ")
    preco = ler_float("Preco: ", minimo=0.01)
    quantidade = ler_inteiro("Quantidade: ", minimo=0)

    produto = criar_produto(codigo, nome, categoria, preco, quantidade)
    estoque.cadastrar_produto(produto)
    salvar_estado(estoque)
    registrar_log(CAMINHO_LOG, f"Produto cadastrado: codigo={codigo}")
    print("Produto cadastrado com sucesso.")


def editar_produto(estoque):
    print("\nEditar produto")
    codigo = ler_inteiro("Codigo do produto: ", minimo=1)
    produto = estoque.buscar_por_codigo(codigo)
    if produto is None:
        print("Produto nao encontrado.")
        return

    print("Produto atual:")
    mostrar_produto(produto)
    print("Deixe em branco para manter o valor atual.")

    nome = ler_texto("Novo nome: ", permitir_vazio=True) or None
    categoria = ler_texto("Nova categoria: ", permitir_vazio=True) or None
    preco = ler_float("Novo preco: ", minimo=0.01, permitir_vazio=True)
    quantidade = ler_inteiro(
        "Nova quantidade: ", minimo=0, permitir_vazio=True
    )

    estoque.editar_produto(
        codigo,
        nome=nome,
        categoria=categoria,
        preco=preco,
        quantidade=quantidade,
    )
    salvar_estado(estoque)
    registrar_log(CAMINHO_LOG, f"Produto editado: codigo={codigo}")
    print("Produto editado com sucesso.")


def remover_produto(estoque):
    print("\nRemover produto")
    codigo = ler_inteiro("Codigo do produto: ", minimo=1)
    produto = estoque.buscar_por_codigo(codigo)
    if produto is None:
        print("Produto nao encontrado.")
        return

    mostrar_produto(produto)
    confirmacao = ler_texto("Confirmar remocao? (s/n): ").lower()
    if confirmacao != "s":
        print("Remocao cancelada.")
        return

    estoque.remover_produto(codigo)
    salvar_estado(estoque)
    registrar_log(CAMINHO_LOG, f"Produto removido: codigo={codigo}")
    print("Produto removido com sucesso.")


def buscar_codigo(estoque):
    print("\nBusca por codigo")
    codigo = ler_inteiro("Codigo: ", minimo=1)
    produto = estoque.buscar_por_codigo(codigo)
    if produto is None:
        print("Produto nao encontrado.")
    else:
        mostrar_produto(produto)


def buscar_nome(estoque):
    print("\nBusca por nome")
    termo = ler_texto("Nome ou parte do nome: ")
    mostrar_lista(estoque.buscar_por_nome(termo))


def registrar_venda(estoque):
    print("\nRegistrar venda")
    codigo = ler_inteiro("Codigo do produto: ", minimo=1)
    quantidade = ler_inteiro("Quantidade vendida: ", minimo=1)
    produto = estoque.registrar_venda(codigo, quantidade)
    salvar_estado(estoque)
    registrar_log(
        CAMINHO_LOG,
        f"Venda registrada: codigo={codigo}, quantidade={quantidade}",
    )
    print("Venda registrada com sucesso.")
    mostrar_produto(produto)


def listar_ordenados(estoque):
    print("\nProdutos ordenados por codigo")
    mostrar_lista(estoque.listar_ordenados_por_codigo())


def listar_categoria(estoque):
    print("\nProdutos por categoria")
    categoria = ler_texto("Categoria: ")
    mostrar_lista(estoque.listar_por_categoria(categoria))


def relatorio_estoque_baixo(estoque):
    print("\nRelatorio de estoque baixo")
    limite = ler_inteiro("Limite de quantidade: ", minimo=0)
    mostrar_lista(estoque.relatorio_estoque_baixo(limite))


def relatorio_precos(estoque):
    print("\nRelatorio menor/maior preco")
    menor = estoque.produto_menor_preco()
    maior = estoque.produto_maior_preco()

    if menor is None:
        print("Nenhum produto cadastrado.")
        return

    print("Menor preco:")
    mostrar_produto(menor)
    print("Maior preco:")
    mostrar_produto(maior)


def recarregar_dados():
    produtos = carregar_produtos(CAMINHO_DADOS)
    estoque = Estoque(produtos)
    registrar_log(CAMINHO_LOG, "Dados carregados do arquivo")
    return estoque


def mostrar_menu():
    print("\n=== Sistema de Estoque e Vendas ===")
    print("1. Cadastrar produto")
    print("2. Editar produto")
    print("3. Remover produto")
    print("4. Buscar produto por codigo")
    print("5. Buscar produtos por nome")
    print("6. Registrar venda")
    print("7. Listar produtos ordenados por codigo")
    print("8. Listar produtos por categoria")
    print("9. Relatorio de estoque baixo")
    print("10. Relatorio menor/maior preco")
    print("11. Salvar dados")
    print("12. Carregar dados")
    print("0. Sair")


def executar_opcao(opcao, estoque):
    if opcao == 1:
        cadastrar_produto(estoque)
    elif opcao == 2:
        editar_produto(estoque)
    elif opcao == 3:
        remover_produto(estoque)
    elif opcao == 4:
        buscar_codigo(estoque)
    elif opcao == 5:
        buscar_nome(estoque)
    elif opcao == 6:
        registrar_venda(estoque)
    elif opcao == 7:
        listar_ordenados(estoque)
    elif opcao == 8:
        listar_categoria(estoque)
    elif opcao == 9:
        relatorio_estoque_baixo(estoque)
    elif opcao == 10:
        relatorio_precos(estoque)
    elif opcao == 11:
        salvar_estado(estoque)
        registrar_log(CAMINHO_LOG, "Dados salvos manualmente")
        print("Dados salvos com sucesso.")
    elif opcao == 12:
        return recarregar_dados()
    else:
        print("Opcao invalida.")
    return estoque


def main():
    try:
        estoque = recarregar_dados()
    except (ArquivoError, EstoqueError, ValidacaoProdutoError) as erro:
        print(f"Erro ao carregar dados: {erro}")
        estoque = Estoque()

    while True:
        mostrar_menu()
        opcao = ler_inteiro("Escolha uma opcao: ", minimo=0)

        if opcao == 0:
            salvar_estado(estoque)
            registrar_log(CAMINHO_LOG, "Sistema encerrado")
            print("Dados salvos. Ate logo!")
            break

        try:
            estoque = executar_opcao(opcao, estoque)
        except (ArquivoError, EstoqueError, ValidacaoProdutoError) as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
