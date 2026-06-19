import React from "react";
import { Page, Text, Document, StyleSheet, View } from "@react-pdf/renderer";
import type { AccessibilityResults } from "../interfaces/AccessibilityResults";
import type { ContrastItem } from "../interfaces/ResultContrast";

const styles = StyleSheet.create({
  page: {
    padding: 40,
    fontSize: 11,
    fontFamily: "Helvetica",
    color: "#1F2937", // Cinza escuro corporativo
  },
  header: {
    backgroundColor: "#1E3A8A", // Azul marinho sólido
    padding: 16,
    borderRadius: 4,
    marginBottom: 24,
  },
  headerTitle: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "bold",
    textAlign: "center",
  },
  sectionContainer: {
    marginBottom: 20,
  },
  sectionTitleHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    borderBottomWidth: 1,
    borderBottomColor: "#E5E7EB",
    paddingBottom: 4,
    marginTop: 16,
    marginBottom: 6,
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: "bold",
    color: "#1E3A8A",
  },
  statusBadgeError: {
    color: "#DC2626",
    fontSize: 11,
    fontWeight: "bold",
  },
  statusBadgeSuccess: {
    color: "#16A34A",
    fontSize: 11,
    fontWeight: "bold",
  },
  description: {
    color: "#4B5563",
    fontSize: 10,
    marginBottom: 8,
    fontStyle: "italic",
  },
  itemContainerHighlight: {
    backgroundColor: "#F9FAFB",
    borderRadius: 4,
    marginBottom: 4,
    padding: 8,
    borderLeftWidth: 2,
    borderLeftColor: "#3B82F6",
  },
  itemContainer: {
    backgroundColor: "#FFFFFF",
    borderRadius: 4,
    marginBottom: 4,
    padding: 8,
    borderLeftWidth: 2,
    borderLeftColor: "#E5E7EB",
  },
  paragraph: {
    marginBottom: 3,
    lineHeight: 1.4,
  },
  label: {
    fontWeight: "bold",
    color: "#374151",
  },
  aiText: {
    color: "#6D28D9",
    marginTop: 4,
    paddingTop: 4,
    borderTopWidth: 0.5,
    borderTopColor: "#E9D5FF",
  },
  footer: {
    position: "absolute",
    bottom: 24,
    left: 40,
    right: 40,
    textAlign: "center",
    fontSize: 9,
    color: "#9CA3AF",
    borderTopWidth: 0.5,
    borderTopColor: "#E5E7EB",
    paddingTop: 8,
  },
});

interface ReportPDFProps {
  result: AccessibilityResults | null;
  contrastResult: ContrastItem[];
  url: string;
}

interface SectionHeaderProps {
  title: string;
  description: string;
  issueCount: number;
  successMessage?: string;
}

const ReportSectionHeader: React.FC<SectionHeaderProps> = ({ title, description, issueCount, successMessage = "Nenhum problema encontrado" }) => (
  <View style={styles.sectionContainer}>
    <View style={styles.sectionTitleHeader}>
      <Text style={styles.sectionTitle}>{title}</Text>
      {issueCount === 0 ? (
        <Text style={styles.statusBadgeSuccess}>✓ {successMessage}</Text>
      ) : (
        <Text style={styles.statusBadgeError}>
          {issueCount} {issueCount === 1 ? "problema detectado" : "problemas detectados"}
        </Text>
      )}
    </View>
    <Text style={styles.description}>{description}</Text>
  </View>
);

export const ReportPDF: React.FC<ReportPDFProps> = ({ result, contrastResult = [], url }) => {
  if (!result) {
    return (
      <Document>
        <Page style={styles.page}>
          <Text style={styles.paragraph}>Nenhum dado disponível para gerar o relatório corporativo.</Text>
          <Text style={styles.footer}>Relatório gerado automaticamente por A11y_Inspector</Text>
        </Page>
      </Document>
    );
  }

  return (
    <Document>
      <Page size="A4" style={styles.page} wrap>
        {/* Cabeçalho Principal */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Relatório Analítico de Acessibilidade Digital</Text>
        </View>

        {/* Metadados da Auditoria */}
        <View style={{ marginBottom: 16, fontSize: 10, color: "#4B5563" }}>
          <Text style={styles.paragraph}><Text style={styles.label}>URL Analisada: </Text>{url || "Não informada"}</Text>
          <Text style={styles.paragraph}><Text style={styles.label}>Data da Inspeção: </Text>{new Date().toLocaleString("pt-BR")}</Text>
        </View>

        {/* Resumo Executivo */}
        <View style={{ ...styles.sectionContainer, backgroundColor: "#F3F4F6", padding: 12, borderRadius: 4 }}>
          <Text style={styles.sectionTitle}>Resumo Executivo</Text>
          <Text style={styles.paragraph}>
            <Text style={styles.label}>Total de Problemas Encontrados: </Text>
            {(result.images?.length || 0) + (result.forms?.length || 0) + (result.headings?.length || 0) + (result.links?.length || 0) + (result.buttons?.length || 0) + (result.landmarks?.length || 0) + (contrastResult?.length || 0)}
          </Text>
          <Text style={styles.paragraph}>
            <Text style={styles.label}>Imagens sem Alt: </Text>{result.images?.length || 0}
          </Text>
          <Text style={styles.paragraph}>
            <Text style={styles.label}>Campos sem Rótulo: </Text>{result.forms?.length || 0}
          </Text>
          <Text style={styles.paragraph}>
            <Text style={styles.label}>Problemas de Hierarquia: </Text>{result.headings?.length || 0}
          </Text>
          <Text style={styles.paragraph}>
            <Text style={styles.label}>Links com Texto Vago: </Text>{result.links?.length || 0}
          </Text>
          <Text style={styles.paragraph}>
            <Text style={styles.label}>Botões sem Rótulo: </Text>{result.buttons?.length || 0}
          </Text>
          <Text style={styles.paragraph}>
            <Text style={styles.label}>Landmarks Ausentes: </Text>{result.landmarks?.length || 0}
          </Text>
          <Text style={styles.paragraph}>
            <Text style={styles.label}>Problemas de Contraste: </Text>{contrastResult?.length || 0}
          </Text>
        </View>

        {result.images && result.images.length > 0 && (
          <>
            <ReportSectionHeader 
              title="Imagens sem descrição (Alt)" 
              description="Imagens sem o atributo descritivo impedem a compreensão do conteúdo por usuários de leitores de tela e degradam o SEO da página."
              issueCount={result.images?.length || 0}
              successMessage="Todas as imagens possuem texto alternativo."
            />
            {result.images?.map((img, index) => (
              <View key={index} style={index % 2 === 0 ? styles.itemContainerHighlight : styles.itemContainer}>
                <Text style={styles.paragraph}><Text style={styles.label}>HTML do Elemento: </Text>{img.html}</Text>
                <Text style={styles.paragraph}><Text style={styles.label}>URL Origem: </Text>{img.image_url || "Não disponível"}</Text>
                {img.ai_description_suggestion && (
                  <Text style={[styles.paragraph, styles.aiText]}>
                    <Text style={styles.label}>Insight da IA (Sugestão de Alt): </Text>"{img.ai_description_suggestion}"
                  </Text>
                )}
              </View>
            ))}
          </>
        )}

        {/* 2. SEÇÃO DE FORMULÁRIOS */}
        {result.forms && result.forms.length > 0 && (
          <>
            <ReportSectionHeader 
              title="Campos de Formulário sem Rótulo" 
              description="Inputs e controles de formulário precisam de elementos <label> explicitamente associados para garantir acessibilidade cognitiva e técnica."
              issueCount={result.forms?.length || 0}
            />
            {result.forms?.map((form, index) => (
              <View key={index} style={index % 2 === 0 ? styles.itemContainerHighlight : styles.itemContainer}>
                <Text style={styles.paragraph}><Text style={styles.label}>HTML do Elemento: </Text>{form.html}</Text>
                <Text style={styles.paragraph}><Text style={styles.label}>Mapeamento WCAG: </Text>{form.message}</Text>
              </View>
            ))}
          </>
        )}

        {/* 3. SEÇÃO DE HIERARQUIA DE TÍTULOS */}
        {result.headings && result.headings.length > 0 && (
          <>
            <ReportSectionHeader 
              title="Inconformidades na Hierarquia de Títulos (Headings)" 
              description="A árvore de cabeçalhos (H1 a H6) define a estrutura semântica da página. Quebras na sequência prejudicam a navegação estruturada."
              issueCount={result.headings?.length || 0}
            />
            {result.headings?.map((head, index) => (
              <View key={index} style={index % 2 === 0 ? styles.itemContainerHighlight : styles.itemContainer}>
                <Text style={styles.paragraph}><Text style={styles.label}>Elemento: </Text>{typeof head === 'string' ? head : (head.element || head.message || 'Sem informação')}</Text>
                {typeof head !== 'string' && head.message && (
                  <Text style={styles.paragraph}><Text style={styles.label}>Detalhes: </Text>{head.message}</Text>
                )}
              </View>
            ))}
          </>
        )}

        {/* 4. SEÇÃO DE LINKS VAGOS */}
        {result.links && result.links.length > 0 && (
          <>
            <ReportSectionHeader 
              title="Links com Texto Ambíguo" 
              description="Textos como 'clique aqui' ou 'saiba mais' soltos não fornecem contexto sobre o destino do link em leitores de tela."
              issueCount={result.links?.length || 0}
            />
            {result.links?.map((link, index) => (
              <View key={index} style={index % 2 === 0 ? styles.itemContainerHighlight : styles.itemContainer}>
                <Text style={styles.paragraph}><Text style={styles.label}>Elemento: </Text>{typeof link === 'string' ? link : (link.element || link.message || 'Sem informação')}</Text>
                {typeof link !== 'string' && link.message && (
                  <Text style={styles.paragraph}><Text style={styles.label}>Detalhes: </Text>{link.message}</Text>
                )}
              </View>
            ))}
          </>
        )}

        {/* 5. SEÇÃO DE BOTÕES SEM RÓTULO */}
        {result.buttons && result.buttons.length > 0 && (
          <>
            <ReportSectionHeader 
              title="Botões sem Acessibilidade Textual" 
              description="Todos os botões devem possuir texto visível descritivo ou uma tag 'aria-label' equivalente mapeada."
              issueCount={result.buttons?.length || 0}
            />
            {result.buttons?.map((button, index) => (
              <View key={index} wrap={false} style={index % 2 === 0 ? styles.itemContainerHighlight : styles.itemContainer}>
                <Text style={styles.paragraph}><Text style={styles.label}>ID do Elemento: </Text>{button.id || "Não identificado"}</Text>
                <Text style={styles.paragraph}><Text style={styles.label}>HTML do Elemento: </Text>{button.html}</Text>
                <Text style={styles.paragraph}><Text style={styles.label}>Mapeamento WCAG: </Text>{button.message}</Text>
              </View>
            ))}
          </>
        )}

        {/* 6. SEÇÃO DE LANDMARKS */}
        {result.landmarks && result.landmarks.length > 0 && (
          <>
            <ReportSectionHeader 
              title="Landmarks Semânticos Ausentes" 
              description="Uso obrigatório de tags estruturais principais como <main>, <nav>, <header> e <footer> para orientar o motor de acessibilidade."
              issueCount={result.landmarks?.length || 0}
            />
            {result.landmarks?.map((landmark, index) => (
              <View key={index} style={index % 2 === 0 ? styles.itemContainerHighlight : styles.itemContainer}>
                <Text style={styles.paragraph}><Text style={styles.label}>Estrutura: </Text>{typeof landmark === 'string' ? landmark : (landmark.element || landmark.message || 'Sem informação')}</Text>
                {typeof landmark !== 'string' && landmark.message && (
                  <Text style={styles.paragraph}><Text style={styles.label}>Detalhes: </Text>{landmark.message}</Text>
                )}
              </View>
            ))}
          </>
        )}

        {/* 7. SEÇÃO DE CONTRASTE */}
        {contrastResult && contrastResult.length > 0 && (
          <>
            <ReportSectionHeader 
              title="Falhas Críticas de Contraste de Cores" 
              description="Verificação matemática de taxas de contraste entre a cor do texto e a cor do fundo para garantir a legibilidade universal."
              issueCount={contrastResult?.length || 0}
            />
            {contrastResult?.map((contrast, index) => (
              <View key={index} style={index % 2 === 0 ? styles.itemContainerHighlight : styles.itemContainer}>
                <Text style={styles.paragraph}><Text style={styles.label}>Texto Capturado: </Text>"{contrast.text || "N/A"}"</Text>
                <Text style={styles.paragraph}>
                  <Text style={styles.label}>Especificação Técnica: </Text>
                  Cor do Texto: {contrast.color || "N/A"} | Cor do Fundo: {contrast.background || "N/A"}
                </Text>
              </View>
            ))}
          </>
        )}

        {/* Rodapé institucional */}
        <Text style={styles.footer}>
          Documento Confidencial — Gerado por Elisiane Quadros via A11y_Inspector. Todos os direitos reservados © {new Date().getFullYear()}.
        </Text>
      </Page>
    </Document>
  );
};