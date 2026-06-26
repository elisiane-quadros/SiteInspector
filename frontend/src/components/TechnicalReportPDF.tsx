import React from 'react';
import { Document, Page, Text, View, StyleSheet, Font } from '@react-pdf/renderer';

// Configuração de fonte para o layout técnico
Font.register({
  family: 'Helvetica-Bold',
  src: 'https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.1.66/fonts/Roboto/Roboto-Medium.ttf'
});

interface TechnicalReportProps {
  result: {
    images?: any[];
    forms?: any[];
    headings?: any[];
    links?: any[];
    buttons?: any[];
    landmarks?: any[];
  };
  contrastResult?: any[];
  url: string;
}

export const TechnicalReportPDF: React.FC<TechnicalReportProps> = ({ result, contrastResult = [], url }) => {
  const formattedDate = new Date().toLocaleString('pt-PT', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  // Função utilitária para renderizar o bloco técnico de cada ocorrência de forma segura
  const renderIssueCard = (item: any, index: number, category: string) => {
    const isObject = typeof item === 'object' && item !== null;
    
    // Extrai as propriedades baseadas no novo JSON do backend
    const message = isObject ? (item.message || item.friendly_message || 'Inconformidade estrutural detetada.') : item;
    const htmlSnippet = isObject ? (item.html || item.element) : 'Não disponível';
    const wcagCrit = isObject ? (item.wcag || 'Diretriz Geral WCAG') : 'N/A';
    const severity = isObject ? (item.severity || 'Não classificado') : 'Média';
    const suggestion = isObject ? (item.suggestion || item.how_to_fix || '') : '';

    return (
      <View key={`${category}-${index}`} style={styles.cardContainer} wrap={false}>
        <View style={styles.cardHeader}>
          <Text style={styles.cardHeaderTitle}>Ocorrência #{index + 1} — {category}</Text>
          <Text style={styles.severityBadge}>{severity.toUpperCase()}</Text>
        </View>
        
        <View style={styles.cardBody}>
          <Text style={styles.metaLabel}><Text style={styles.bold}>Diretriz WCAG:</Text> {wcagCrit}</Text>
          <Text style={styles.metaLabel}><Text style={styles.bold}>Descrição da Falha:</Text> {message}</Text>
          
          {htmlSnippet && htmlSnippet !== 'Não disponível' && (
            <View style={styles.codeBlock}>
              <Text style={styles.codeText}>{htmlSnippet}</Text>
            </View>
          )}

          {/* Se houver uma sugestão de correção ou insight da IA */}
          {(suggestion || item.ai_description_suggestion) && (
            <View style={styles.fixBlock}>
              <Text style={styles.fixTitle}>Orientação para Correção Técnica:</Text>
              <Text style={styles.fixText}>
                {suggestion} {item.ai_description_suggestion ? `[Insight de Alt da IA]: ${item.ai_description_suggestion}` : ''}
              </Text>
            </View>
          )}
        </View>
      </View>
    );
  };

  return (
    <Document>
      <Page size="A4" style={styles.page}>
        
        {/* CABEÇALHO TÉCNICO */}
        <View style={styles.headerContainer}>
          <Text style={styles.appTitle}>A11y_Inspector // Developer Mode</Text>
          <Text style={styles.docType}>Checklist Técnico de Engenharia Reversa</Text>
        </View>

        {/* METADADOS DA SESSÃO */}
        <View style={styles.metaContainer}>
          <Text style={styles.metaText}><Text style={styles.bold}>Ambiente Analisado:</Text> {url}</Text>
          <Text style={styles.metaText}><Text style={styles.bold}>Data da Auditoria:</Text> {formattedDate}</Text>
          <Text style={styles.metaText}><Text style={styles.bold}>Escopo:</Text> Mapeamento de Tags, DOM Elements e Hierarquia Semântica</Text>
        </View>

        {/* --- SEÇÃO: IMAGENS --- */}
        {result.images && result.images.length > 0 && (
          <View>
            <Text style={styles.sectionTitle}>1. Elementos de Imagem (Acessibilidade Visual)</Text>
            {result.images.map((item, index) => renderIssueCard(item, index, 'Imagens sem Alt'))}
          </View>
        )}

        {/* --- SEÇÃO: FORMULÁRIOS --- */}
        {result.forms && result.forms.length > 0 && (
          <View style={{ marginTop: 15 }}>
            <Text style={styles.sectionTitle}>2. Controles de Formulário (Form Fields)</Text>
            {result.forms.map((item, index) => renderIssueCard(item, index, 'Inputs sem Label'))}
          </View>
        )}

        {/* --- SEÇÃO: HIERARQUIA DE TÍTULOS --- */}
        {result.headings && result.headings.length > 0 && (
          <View style={{ marginTop: 15 }}>
            <Text style={styles.sectionTitle}>3. Estrutura Semântica do DOM (Headings)</Text>
            {result.headings.map((item, index) => renderIssueCard(item, index, 'Quebra de Cabeçalho'))}
          </View>
        )}

        {/* --- SEÇÃO: LINKS --- */}
        {result.links && result.links.length > 0 && (
          <View style={{ marginTop: 15 }}>
            <Text style={styles.sectionTitle}>4. Elementos de Âncora (Links)</Text>
            {result.links.map((item, index) => renderIssueCard(item, index, 'Texto de Link Vago'))}
          </View>
        )}

        {/* --- SEÇÃO: BOTÕES --- */}
        {result.buttons && result.buttons.length > 0 && (
          <View style={{ marginTop: 15 }}>
            <Text style={styles.sectionTitle}>5. Elementos de Ação (Buttons)</Text>
            {result.buttons.map((item, index) => renderIssueCard(item, index, 'Botão sem Rótulo Acessível'))}
          </View>
        )}

        {/* --- SEÇÃO: LANDMARKS --- */}
        {result.landmarks && result.landmarks.length > 0 && (
          <View style={{ marginTop: 15 }}>
            <Text style={styles.sectionTitle}>6. Regiões Semânticas Globais (Landmarks)</Text>
            {result.landmarks.map((item, index) => renderIssueCard(item, index, 'Landmark Ausente'))}
          </View>
        )}

        {/* --- SEÇÃO: CONTRASTE --- */}
        {contrastResult && contrastResult.length > 0 && (
          <View style={{ marginTop: 15 }}>
            <Text style={styles.sectionTitle}>7. Análise Cromática (Contrast Issues)</Text>
            {contrastResult.map((item, index) => renderIssueCard(item, index, 'Falha de Contraste'))}
          </View>
        )}

        {/* RODAPÉ FIXED */}
        <View style={styles.footer} fixed>
          <Text>A11y_Inspector Technical Report — Modo Engenharia</Text>
          <Text render={({ pageNumber, totalPages }) => `Página ${pageNumber} de ${totalPages}`} />
        </View>

      </Page>
    </Document>
  );
};

const styles = StyleSheet.create({
  page: {
    padding: 35,
    backgroundColor: '#fafafa',
    fontFamily: 'Helvetica',
    display: 'flex',
    flexDirection: 'column',
  },
  headerContainer: {
    borderBottomWidth: 2,
    borderBottomColor: '#334155',
    paddingBottom: 10,
    marginBottom: 15,
  },
  appTitle: {
    fontSize: 10,
    fontFamily: 'Helvetica-Bold',
    color: '#475569',
    letterSpacing: 1,
  },
  docType: {
    fontSize: 18,
    fontFamily: 'Helvetica-Bold',
    color: '#0f172a',
    marginTop: 3,
  },
  metaContainer: {
    backgroundColor: '#f1f5f9',
    padding: 10,
    borderRadius: 4,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#cbd5e1',
  },
  metaText: {
    fontSize: 10,
    color: '#334155',
    marginBottom: 2,
  },
  bold: {
    fontFamily: 'Helvetica-Bold',
  },
  sectionTitle: {
    fontSize: 12,
    fontFamily: 'Helvetica-Bold',
    color: '#0f172a',
    backgroundColor: '#e2e8f0',
    padding: 6,
    borderRadius: 3,
    marginBottom: 10,
  },
  cardContainer: {
    backgroundColor: '#ffffff',
    borderWidth: 1,
    borderColor: '#e2e8f0',
    borderRadius: 5,
    marginBottom: 10,
    overflow: 'hidden',
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#f8fafc',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderBottomWidth: 1,
    borderBottomColor: '#e2e8f0',
  },
  cardHeaderTitle: {
    fontSize: 10,
    fontFamily: 'Helvetica-Bold',
    color: '#1e293b',
  },
  severityBadge: {
    fontSize: 9,
    fontFamily: 'Helvetica-Bold',
    color: '#991b1b',
    backgroundColor: '#fee2e2',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 3,
  },
  cardBody: {
    padding: 10,
  },
  metaLabel: {
    fontSize: 10,
    color: '#334155',
    marginBottom: 4,
    lineHeight: 1.4,
  },
  codeBlock: {
    backgroundColor: '#0f172a',
    padding: 8,
    borderRadius: 4,
    marginTop: 6,
    marginBottom: 6,
  },
  codeText: {
    fontFamily: 'Courier',
    fontSize: 10,
    color: '#ffffff',
    lineHeight: 1.3,
  },
  fixBlock: {
    backgroundColor: '#f0fdf4',
    borderLeftWidth: 3,
    borderLeftColor: '#22c55e',
    padding: 6,
    borderRadius: 3,
    marginTop: 4,
  },
  fixTitle: {
    fontSize: 10,
    fontFamily: 'Helvetica-Bold',
    color: '#14532d',
    marginBottom: 2,
  },
  fixText: {
    fontSize: 10,
    color: '#166534',
    lineHeight: 1.4,
  },
  footer: {
    position: 'absolute',
    bottom: 20,
    left: 35,
    right: 35,
    borderTopWidth: 1,
    borderTopColor: '#e2e8f0',
    paddingTop: 8,
    flexDirection: 'row',
    justifyContent: 'space-between',
    fontSize: 8,
    color: '#94a3b8',
  },
});