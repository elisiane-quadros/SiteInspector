"""
Testes da detecção de segmento de negócio.

Importamos a função REAL (`_detect_business_segment`) de
`backend.utils.ai_assistant`. Assim o teste valida exatamente o código que
roda em produção - nunca uma cópia, que poderia ficar desatualizada e dar
um falso "passou".
"""
import pytest

from backend.utils.ai_assistant import _detect_business_segment


# Cada tupla descreve um cenário de teste:
#   (descrição legível, url, meta_description, segmento_esperado)
#
# Manter os casos numa lista separada deixa fácil adicionar novos cenários
# sem mexer na lógica do teste.
CASOS = [
    (
        "E-commerce - palavras de venda na meta description",
        "https://www.techstore.com.br",
        "Compre os melhores computadores e componentes com descontos no carrinho.",
        "ecommerce",
    ),
    (
        "SaaS - termos de plataforma, software e MRR",
        "https://www.flowtask.io/dashboard",
        "A melhor plataforma de software para automação de tarefas e análise de MRR.",
        "saas",
    ),
    (
        "Corporate - institucional, sem gatilhos de venda ou produto",
        "https://www.silvaassociados.adv.br",
        "Escritório de consultoria jurídica empresarial e compliance de marcas.",
        "corporate",
    ),
    (
        "Edge case - 'app' dentro de outra palavra nao dispara SaaS",
        "https://www.desapontar.com",
        "Um blog pessoal sobre histórias e crônicas do dia a dia.",
        "corporate",
    ),
]


# @parametrize roda a MESMA função de teste uma vez para cada caso da lista.
# Vantagens sobre um for-loop com vários asserts:
#   - cada caso aparece como um teste separado no relatório (4 testes, não 1);
#   - se um falhar, os outros continuam rodando;
#   - o `ids=` dá um nome legível a cada caso na saída do pytest.
@pytest.mark.parametrize(
    "descricao, url, meta_description, esperado",
    CASOS,
    ids=[caso[0] for caso in CASOS],
)
def test_detect_business_segment(descricao, url, meta_description, esperado):
    # Arrange + Act: chamamos a função real com os dados do cenário.
    resultado = _detect_business_segment(url, meta_description)

    # Assert: a mensagem só aparece QUANDO falha - e mostra exatamente
    # o que era esperado vs. o que veio, facilitando o diagnóstico.
    assert resultado == esperado, (
        f"\nCaso: {descricao}"
        f"\n  URL.............: {url}"
        f"\n  Esperado........: {esperado!r}"
        f"\n  Obtido..........: {resultado!r}"
    )
