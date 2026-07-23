"""
Testes do gerador de roadmap de prioridades (utils/priority.py).
"""

from backend.utils.priority import generate_priority_roadmap


def test_roadmap_vazio_quando_sem_ocorrencias():
    results = {
        key: []
        for key in ["forms", "focus", "buttons", "links", "screenshots", "headings", "landmarks"]
    }
    roadmap = generate_priority_roadmap(results, [])
    assert roadmap == []


def test_roadmap_ordena_p1_primeiro():
    results = {
        "forms": ["item1"],  # P1
        "focus": [],  # P1 (sem ocorrências)
        "buttons": [],  # P2
        "links": ["item1"],  # P2
        "screenshots": ["item1"],  # P3
        "headings": [],  # P3
        "landmarks": [],  # P3
    }
    roadmap = generate_priority_roadmap(results, [])
    assert len(roadmap) == 3
    assert roadmap[0]["priority"] == "P1"
    assert roadmap[1]["priority"] == "P2"
    assert roadmap[2]["priority"] == "P3"


def test_roadmap_inclui_contraste():
    results = {
        key: []
        for key in ["forms", "focus", "buttons", "links", "screenshots", "headings", "landmarks"]
    }
    contrast_issues = ["issue1", "issue2"]
    roadmap = generate_priority_roadmap(results, contrast_issues)
    assert len(roadmap) == 1
    assert roadmap[0]["category"] == "Contraste de Cores Insuficiente"
    assert roadmap[0]["priority"] == "P2"
    assert roadmap[0]["count"] == 2


def test_roadmap_contagem_correta():
    results = {
        "forms": ["a", "b"],  # P1, count=2
        "focus": [],  # P1, count=0
        "buttons": ["a"],  # P2, count=1
        "links": [],  # P2, count=0
        "screenshots": ["a", "b", "c"],  # P3, count=3
        "headings": [],  # P3, count=0
        "landmarks": [],  # P3, count=0
    }
    roadmap = generate_priority_roadmap(results, [])
    forms_item = next(i for i in roadmap if i["category"] == "Campos de Formulário sem Rótulo")
    screenshots_item = next(i for i in roadmap if i["category"] == "Imagens sem Descrição (Alt)")
    assert forms_item["count"] == 2
    assert screenshots_item["count"] == 3


def test_roadmap_contem_chaves_obrigatorias():
    results = {
        "forms": ["item"],
        "focus": [],
        "buttons": [],
        "links": [],
        "screenshots": [],
        "headings": [],
        "landmarks": [],
    }
    roadmap = generate_priority_roadmap(results, [])
    item = roadmap[0]
    assert "priority" in item
    assert "label" in item
    assert "category" in item
    assert "count" in item
    assert "reason" in item
