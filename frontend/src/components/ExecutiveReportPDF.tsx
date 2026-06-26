import React from 'react';
import { Document, Page, Text, View, StyleSheet, Font } from '@react-pdf/renderer';

// Configuração de fontes para garantir que o peso Bold seja renderizado corretamente
Font.register({
  family: 'Helvetica-Bold',
  src: 'https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.66/fonts/Roboto/Roboto-Medium.ttf' // Fallback seguro
});

interface ExecutiveReportProps {
  result: {
    images?: any[];
    forms?: any[];
    headings?: any[];
    links?: any[];
    buttons?: any[];
    landmarks?: any[];
    focus?: any[];
    contrast?: any[];
    priority_roadmap?: Array<{
      priority: string;
      label: string;
      category: string;
      count: number;
      reason: string;
    }>;
  };
  url: string;
  businessSegment: string;
  executiveAnalysis: string;
}

export const ExecutiveReportPDF: React.FC<ExecutiveReportProps> = ({
  result,
  url, 
  businessSegment = "Não Informado", 
  executiveAnalysis = "",
}) => {

  // Contabilidade dos problemas de forma segura
  const totalImages = result.images?.length || 0;
  const totalForms = result.forms?.length || 0;
  const totalHeadings = result.headings?.length || 0;
  const totalLinks = result.links?.length || 0;
  const totalButtons = result.buttons?.length || 0;
  const totalLandmarks = result.landmarks?.length || 0;
  const totalFocus    = result.focus?.length    || 0;
  const totalContrast = result.contrast?.length || 0;
  
  const totalGeral = totalImages + totalForms + totalHeadings + totalLinks + totalButtons + totalLandmarks + totalFocus + totalContrast;

  // Função auxiliar para definir o nível de risco institucional
  const getRiskLevel = (total: number) => {
    if (total > 30) return { label: 'CRÍTICO / ALTO RISCO', color: '#b91c1c' };
    if (total > 10) return { label: 'MODERADO', color: '#d97706' };
    return { label: 'BAIXO', color: '#15803d' };
  };

  const risk = getRiskLevel(totalGeral);

  // Formatação da data atual
  const formattedDate = new Date().toLocaleString('pt-PT', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });

  // Função auxiliar interna para quebrar a string da IA em blocos limpos na Página 2
  const parseAnalysisText = (text: string) => {
    if (!text) return [];
    return text
      .split('\n')
      .map(line => line.trim())
      .filter(line => line.length > 0);
  };

  const analysisLines = parseAnalysisText(executiveAnalysis);

  // Função auxiliar para definir as cores dinâmicas dos cards por prioridade
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'P1':
        return { badgeBg: '#b91c1c', cardBg: '#fef2f2', border: '#fca5a5' }; // Vermelho
      case 'P2':
        return { badgeBg: '#d97706', cardBg: '#fffbeb', border: '#fcd34d' }; // Laranja
      case 'P3':
        return { badgeBg: '#15803d', cardBg: '#f0fdf4', border: '#86efac' }; // Verde
      default:
        return { badgeBg: '#475569', cardBg: '#f8fafc', border: '#cbd5e1' }; // Cinza padrão
    }
  };

  return (
    <Document>
      {/* PÁGINA 1: CAPA E RESUMO EXECUTIVO DE ALTO NÍVEL */}
      <Page size="A4" style={styles.page}>
        
        {/* CABEÇALHO DA CAPA */}
        <View style={styles.headerContainer}>
          <Text style={styles.appTitle}>A11y_Inspector</Text>
          <Text style={styles.docType}>Relatório Executivo de Acessibilidade Digital</Text>
        </View>

        {/* METADADOS DA INSPEÇÃO */}
        <View style={styles.metaContainer}>
          <Text style={styles.metaText}><Text style={styles.bold}>Target (URL):</Text> {url}</Text>
          <Text style={styles.metaText}><Text style={styles.bold}>Data de Emissão:</Text> {formattedDate}</Text>
          <Text style={styles.metaText}><Text style={styles.bold}>Segmento Detectado:</Text> {businessSegment.toUpperCase()}</Text>
          <Text style={styles.metaText}><Text style={styles.bold}>Classificação:</Text> Confidencial / Corporativo</Text>
        </View>

        {/* CARD DE STATUS LEGAL E RISCO */}
        <View style={[styles.riskCard, { borderColor: risk.color }]} wrap={false}>
          <Text style={styles.riskTitle}>DIAGNÓSTICO DE EXPOSIÇÃO LEGAL</Text>
          <Text style={[styles.riskBadge, { backgroundColor: risk.color }]}>{risk.label}</Text>
          <Text style={styles.riskDescription}>
            Este documento apresenta a volumetria de barreiras de acesso digital que violam os critérios internacionais da WCAG 2.1 e a Lei Brasileira de Inclusão (LBI). A presença destas quebras impacta diretamente a retenção de utilizadores e expõe a marca a riscos de litígio e notificações regulatórias.
          </Text>
        </View>

        {/* TABELA CORPORATIVA DE IMPACTOS */}
        <View style={styles.tableContainer} wrap={false}>
          <Text style={styles.sectionTitle}>Volumetria de Barreiras Encontradas</Text>
          
          {/* Header da Tabela */}
          <View style={styles.tableHeader}>
            <Text style={[styles.tableCellHeader, { flex: 3 }]}>Categoria de Impacto Operacional</Text>
            <Text style={[styles.tableCellHeader, { flex: 1, textAlign: 'center' }]}>Ocorrências</Text>
          </View>

          {/* Linhas da Tabela (Estilo Zebra Embutido de Forma Limpa) */}
          <View style={styles.tableRow}>
            <Text style={[styles.tableCell, { flex: 3 }]}>Imagens sem Descrição (Acessibilidade Visual e SEO)</Text>
            <Text style={[styles.tableCell, { flex: 1, textAlign: 'center', fontFamily: 'Helvetica-Bold' }]}>{totalImages}</Text>
          </View>
          
          <View style={[styles.tableRow, styles.zebraBg]}>
            <Text style={[styles.tableCell, { flex: 3 }]}>Campos de Formulário sem Rótulo (Barreira de Entrada e Conversão)</Text>
            <Text style={[styles.tableCell, { flex: 1, textAlign: 'center', fontFamily: 'Helvetica-Bold' }]}>{totalForms}</Text>
          </View>

          <View style={styles.tableRow}>
            <Text style={[styles.tableCell, { flex: 3 }]}>Quebras na Hierarquia Semântica (Estrutura de Títulos)</Text>
            <Text style={[styles.tableCell, { flex: 1, textAlign: 'center', fontFamily: 'Helvetica-Bold' }]}>{totalHeadings}</Text>
          </View>

          <View style={[styles.tableRow, styles.zebraBg]}>
            <Text style={[styles.tableCell, { flex: 3 }]}>Links Ambíguos ou Vagos (Prejudica a Navegação Dinâmica)</Text>
            <Text style={[styles.tableCell, { flex: 1, textAlign: 'center', fontFamily: 'Helvetica-Bold' }]}>{totalLinks}</Text>
          </View>

          <View style={styles.tableRow}>
            <Text style={[styles.tableCell, { flex: 3 }]}>Botões Inacessíveis (Loops de Navegação por Teclado)</Text>
            <Text style={[styles.tableCell, { flex: 1, textAlign: 'center', fontFamily: 'Helvetica-Bold' }]}>{totalButtons}</Text>
          </View>

          <View style={[styles.tableRow, styles.zebraBg]}>
            <Text style={[styles.tableCell, { flex: 3 }]}>Problemas de Navegação e Foco (Barreiras de Interação por Teclado)</Text>
            <Text style={[styles.tableCell, { flex: 1, textAlign: 'center', fontFamily: 'Helvetica-Bold' }]}>{totalFocus}</Text>
          </View>

          <View style={styles.tableRow}>
            <Text style={[styles.tableCell, { flex: 3 }]}>Landmarks Estruturais Ausentes (Falha de Semântica Core)</Text>
            <Text style={[styles.tableCell, { flex: 1, textAlign: 'center', fontFamily: 'Helvetica-Bold' }]}>{totalLandmarks}</Text>
          </View>

          <View style={[styles.tableRow, styles.zebraBg]}>
            <Text style={[styles.tableCell, { flex: 3 }]}>Problemas de Contraste de Cores (Legibilidade e Fadiga Visual)</Text>
            <Text style={[styles.tableCell, { flex: 1, textAlign: 'center', fontFamily: 'Helvetica-Bold' }]}>{totalContrast}</Text>
          </View>

          {/* Linha de Total Geral */}
          <View style={styles.tableTotalRow}>
            <Text style={[styles.tableCellTotal, { flex: 3 }]}>Total de Inconformidades Ativas</Text>
            <Text style={[styles.tableCellTotal, { flex: 1, textAlign: 'center', color: risk.color }]}>{totalGeral}</Text>
          </View>
        </View>

        {/* RODAPÉ INSTITUCIONAL */}
        <View style={styles.footer} fixed>
          <Text>Documento Confidencial - Gerado automaticamente via A11y_Inspector.</Text>
          <Text>Todos os direitos reservados © 2026.</Text>
        </View>

      </Page>
      {/* Página 2: Análise de Impacto e Contexto de Negócio */}
      <Page size="A4" style={styles.page}>
        <View style={styles.headerContainer}>
          <Text style={styles.appTitle}>A11y_Inspector</Text>
          <Text style={styles.docType}>Análise Estratégica Proativa (IA)</Text>
        </View>

        <View style={styles.aiContentContainer}>
          {analysisLines.length > 0 ? (
            analysisLines.map((line, index) => {
              const cleaned = line
                .replace(/\*\*(.*?)\*\*/g, '$1')
                .replace(/\*(.*?)\*/g, '$1')
                .replace(/^#+\s*/, '')
                .trim();

              if (!cleaned) return null;

              const isSectionTitle =
                /^(1\.|2\.|3\.)/.test(cleaned) ||
                cleaned.includes('Impacto') ||
                cleaned.includes('Exposição Legal');

              if (isSectionTitle) {
                return (
                  <View key={index} style={styles.aiSectionCard}>
                    <Text style={styles.aiSectionTitle}>
                      {cleaned.replace(/^[0-9]+\.\s*/, '')}
                    </Text>
                  </View>
                );
              }

              return (
                <View key={index} style={styles.aiBulletRow}>
                  <Text style={styles.aiBulletDot}>›</Text>
                  <Text style={styles.aiBulletText}>
                    {cleaned.replace(/^[-•*\s]+/, '')}
                  </Text>
                </View>
              );
            })
          ) : (
            <View style={styles.emptyAnalysis}>
              <Text style={styles.emptyAnalysisText}>
                Nenhuma análise disponível para esta inspeção.
              </Text>
            </View>
          )}
        </View>

        {/* Seção: Roadmap de Otimização Sugerido */}
        {result.priority_roadmap && result.priority_roadmap.length > 0 && (
          <View style={styles.roadmapContainer} wrap={false}>
            <Text style={styles.sectionTitle}>Roadmap de Otimização Sugerido</Text>
            <Text style={styles.roadmapSubtitle}>
              Ordem recomendada de execução para obter o máximo ganho em conversão de utilizadores e redução imediata de exposição legal (LBI).
            </Text>

            {result.priority_roadmap.map((item, index) => {
              const colors = getPriorityColor(item.priority);

              return (
                <View 
                  key={index} 
                  style={[
                    styles.roadmapItem, 
                    { 
                      backgroundColor: colors.cardBg, 
                      borderLeftColor: colors.badgeBg,
                      borderWidth: 1,
                      borderColor: colors.border
                    }
                  ]}
                >
                  <View style={styles.roadmapHeader}>
                    <Text style={[styles.roadmapBadge, { backgroundColor: colors.badgeBg }]}>
                      {item.priority} - {item.label.toUpperCase()}
                    </Text>
                    <Text style={styles.roadmapCategory}>{item.category}</Text>
                    <Text style={[styles.roadmapCount, { color: colors.badgeBg }]}>
                      {item.count} {item.count === 1 ? 'ocorrência' : 'ocorrências'}
                    </Text>
                  </View>
                  <Text style={styles.roadmapReason}>{item.reason}</Text>
                </View>
              );
            })}
          </View>
        )}

        <View style={styles.footer} fixed>
          <Text>Documento Confidencial - Gerado automaticamente via A11y_Inspector.</Text>
          <Text render={({ pageNumber, totalPages }) => `Página ${pageNumber} de ${totalPages}`} />
        </View>
      </Page>
    </Document>
  );
};

// Estilos Premium e Corporativos - Sem excessos, focados em espaço e harmonia
const styles = StyleSheet.create({
  page: {
    padding: 40,
    backgroundColor: '#ffffff',
    fontFamily: 'Helvetica',
    position: 'relative',
    display: 'flex',
    flexDirection: 'column',
  },
  headerContainer: {
    borderBottomWidth: 2,
    borderBottomColor: '#1e3a8a',
    paddingBottom: 15,
    marginBottom: 20,
  },
  appTitle: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#1e3a8a',
    letterSpacing: 1,
    textTransform: 'uppercase',
  },
  docType: {
    fontSize: 22,
    fontFamily: 'Helvetica-Bold',
    color: '#0f172a',
    marginTop: 5,
  },
  metaContainer: {
    backgroundColor: '#f8fafc',
    padding: 12,
    borderRadius: 6,
    marginBottom: 25,
    borderWidth: 1,
    borderColor: '#e2e8f0',
  },
  metaText: {
    fontSize: 10,
    color: '#475569',
    marginBottom: 4,
  },
  bold: {
    fontFamily: 'Helvetica-Bold',
    color: '#1e293b',
  },
  riskCard: {
    borderLeftWidth: 4,
    backgroundColor: '#fef2f2',
    padding: 16,
    borderRadius: 6,
    marginBottom: 30,
  },
  riskTitle: {
    fontSize: 11,
    fontFamily: 'Helvetica-Bold',
    color: '#1e293b',
    letterSpacing: 0.5,
  },
  riskBadge: {
    alignSelf: 'flex-start',
    color: '#ffffff',
    fontSize: 10,
    fontFamily: 'Helvetica-Bold',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 4,
    marginTop: 6,
    marginBottom: 8,
  },
  riskDescription: {
    fontSize: 10,
    color: '#451a03',
    lineHeight: 1.5,
  },
  sectionTitle: {
    fontSize: 14,
    fontFamily: 'Helvetica-Bold',
    color: '#1e3a8a',
    marginBottom: 10,
  },
  tableContainer: {
    marginTop: 10,
  },
  tableHeader: {
    flexDirection: 'row',
    backgroundColor: '#1e3a8a',
    padding: 8,
    borderRadius: 4,
  },
  tableCellHeader: {
    color: '#ffffff',
    fontSize: 10,
    fontFamily: 'Helvetica-Bold',
  },
  tableRow: {
    flexDirection: 'row',
    borderBottomWidth: 1,
    borderBottomColor: '#f1f5f9',
    paddingVertical: 10,       
    paddingHorizontal: 8,
    alignItems: 'center',
  },
  zebraBg: {
    backgroundColor: '#f8fafc',
  },
  tableCell: {
    fontSize: 11,
    color: '#334155',
    lineHeight: 1.4,
  },
  tableTotalRow: {
    flexDirection: 'row',
    backgroundColor: '#f1f5f9',
    padding: 10,
    marginTop: 5,
    borderTopWidth: 2,
    borderTopColor: '#a4a7aa',
    alignItems: 'center',
  },
  tableCellTotal: {
    fontSize: 11,
    fontFamily: 'Helvetica-Bold',
    color: '#0f172a',
  },
  roadmapContainer: {
  marginTop: 20,
},
roadmapSubtitle: {
  fontSize: 10,
  color: '#64748b',
  marginBottom: 12,
  lineHeight: 1.4,
},
roadmapItem: {
  borderLeftWidth: 3,
  backgroundColor: '#f8fafc',
  borderRadius: 4,
  padding: 10,
  marginBottom: 8,
},
roadmapHeader: {
  flexDirection: 'row',
  alignItems: 'center',
  marginBottom: 4,
  gap: 6,
},
roadmapBadge: {
  color: '#ffffff',
  fontSize: 8,
  fontFamily: 'Helvetica-Bold',
  paddingHorizontal: 6,
  paddingVertical: 2,
  borderRadius: 3,
  letterSpacing: 0.5,
},
roadmapCategory: {
  fontSize: 10,
  fontFamily: 'Helvetica-Bold',
  color: '#1e293b',
  flex: 1,
},
roadmapCount: {
  fontSize: 9,
  fontFamily: 'Helvetica-Bold',
},
roadmapReason: {
  fontSize: 9,
  color: '#475569',
  lineHeight: 1.4,
  paddingLeft: 2,
},
  aiContentContainer: {
    marginTop: 10,
  },
  aiSectionCard: {
    backgroundColor: '#f1f5f9',
    borderLeftWidth: 3,
    borderLeftColor: '#1e3a8a',
    paddingVertical: 8,
    paddingHorizontal: 12,
    marginTop: 18,
    marginBottom: 8,
    borderRadius: 4,
  },
  aiSectionTitle: {
    fontSize: 12,
    fontFamily: 'Helvetica-Bold',
    color: '#1e3a8a',
  },
  aiBulletRow: {
    flexDirection: 'row',
    marginBottom: 6,
    paddingHorizontal: 4,
  },
  aiBulletDot: {
    width: 14,
    fontSize: 13,
    color: '#1e3a8a',
    marginTop: 1,
  },
  aiBulletText: {
    flex: 1,
    fontSize: 10,
    color: '#334155',
    lineHeight: 1.5,
  },
  
  codeBadgeContainer: {
    backgroundColor: '#0f172a',  
    paddingHorizontal: 8,        
    paddingVertical: 2,          
    borderRadius: 4,
    marginHorizontal: 5,         
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  codeBadgeText: {
    color: '#f8fafc',
    fontSize: 11,                
    fontFamily: 'Helvetica-Bold', 
    letterSpacing: 0.5,
  },
  emptyAnalysis: {
  marginTop: 20,
  padding: 20,
  backgroundColor: '#f8fafc',
  borderRadius: 8,
  borderWidth: 1,
  borderColor: '#e2e8f0',
  },
  emptyAnalysisText: {
    fontSize: 11,
    color: '#64748b',
    lineHeight: 1.6,
    textAlign: 'center',
  },
  footer: {
    position: 'absolute',
    bottom: 30,
    left: 40,
    right: 40,
    borderTopWidth: 1,
    borderTopColor: '#e2e8f0',
    paddingTop: 10,
    flexDirection: 'row',
    justifyContent: 'space-between',
    fontSize: 8,
    color: '#94a3b8',
  },
});