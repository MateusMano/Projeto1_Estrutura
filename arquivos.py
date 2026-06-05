"""Persistencia em JSON e log simples de operacoes."""

import json
from datetime import datetime
from pathlib import Path

from produto import Produto, ValidacaoProdutoError


class ArquivoError(ValueError):
    """Erro ao carregar ou salvar dados."""


def carregar_produtos(caminho):
    caminho = Path(caminho)
    if not caminho.exists():
        return []

    try:
        with caminho.open("r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except json.JSONDecodeError as erro:
        raise ArquivoError("Arquivo de dados esta com JSON invalido.") from erro

    if not isinstance(dados, list):
        raise ArquivoError("Arquivo de dados deve conter uma lista de produtos.")

    produtos = []
    for item in dados:
        try:
            produtos.append(Produto.from_dict(item))
        except (KeyError, TypeError, ValidacaoProdutoError) as erro:
            raise ArquivoError("Produto invalido encontrado no arquivo.") from erro
    return produtos


def salvar_produtos(caminho, produtos):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)

    dados = [produto.to_dict() for produto in produtos]
    with caminho.open("w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)


def registrar_log(caminho, mensagem):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with caminho.open("a", encoding="utf-8") as arquivo:
        arquivo.write(f"[{horario}] {mensagem}\n")