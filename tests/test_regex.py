import re

def _detect_business_segment(url: str, meta_description: str) -> str:
    """
    Analyzes the URL and Meta Description using compiled Regex patterns to classify 
    the target website as 'ecommerce', 'saas', or 'corporate' (default).
    """
    analysis_text = f"{url} {meta_description}".lower()
    
    # Padrões Regex com \b (word boundary) para evitar falsos positivos
    ecommerce_pattern = r"\b(comprei?|lojas?|produtos?|ofertas?|descontos?|carrinho|checkout|vendas?|shop(ping)?|cart|store)\b"
    saas_pattern = r"\b(plataformas?|softwares?|sistemas?|apps?|automaç(ão|ões)|ferramentas?|dashboards?|mrr|saas|hub|tools?)\b"
    
    if re.search(ecommerce_pattern, analysis_text):
        return "ecommerce"
        
    if re.search(saas_pattern, analysis_text):
        return "saas"
        
    return "corporate"


# ==============================================================================
# 🧪 SUÍTE DE TESTES EM AMBIENTE DE DESENVOLVIMENTO
# ==============================================================================
if __name__ == "__main__":
    print("=== [TESTING] Business Segment Detection Pipeline ===")
    
    # Casos de teste simulando diferentes tipos de clientes e metadados
    test_cases = [
        {
            "name": "E-commerce (Loja de Eletrónicos)",
            "url": "https://www.techstore.com.br",
            "meta_description": "Compre os melhores computadores e componentes com descontos incríveis no nosso carrinho.",
            "expected": "ecommerce"
        },
        {
            "name": "SaaS (Plataforma de Gestão)",
            "url": "https://www.flowtask.io/dashboard",
            "meta_description": "A melhor plataforma de software para automação de tarefas e análise de MRR corporativo.",
            "expected": "saas"
        },
        {
            "name": "Corporate (Site Institucional de Advocacia)",
            "url": "https://www.silvaassociados.med.br",
            "meta_description": "Escritório especializado em consultoria jurídica empresarial e compliance de marcas.",
            "expected": "corporate"
        },
        {
            "name": "Edge Case - Proteção contra Falso Positivo",
            "url": "https://www.desapontar.com",  # Contém "app" dentro da palavra, mas não isolado
            "meta_description": "Um blog pessoal sobre histórias e crónicas do dia a dia.",
            "expected": "corporate"
        }
    ]
    
    # Execução e validação dos resultados
    for case in test_cases:
        result = _detect_business_segment(case["url"], case["meta_description"])
        status = "✅ PASSED" if result == case["expected"] else "❌ FAILED"
        
        print(f"\nCaso: {case['name']}")
        print(f"  -> Segmento Detetado: {result.upper()}")
        print(f"  -> Status do Teste: {status}")