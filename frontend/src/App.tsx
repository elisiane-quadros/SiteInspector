import { useState } from "react";
import UrlForm from "./components/UrlForm";
import type { AccessibilityResults } from "./interfaces/AccessibilityResults";
import ResultCard from "./components/ResultCard";
import InspectorLoader from "./components/InspectorLoader";
import api from "./services/api";

import type { ContrastItem } from "./interfaces/ResultContrast";
import { PDFDownloadLink } from "@react-pdf/renderer";
import { TechnicalReportPDF } from "./components/TechnicalReportPDF";
import { ExecutiveReportPDF } from "./components/ExecutiveReportPDF";
import lupaIcon from "./assets/lupa.png";

function App() {
  const [result, setResult] = useState<AccessibilityResults | null>(null);
  const [contrastResult, setContrastResult] = useState<ContrastItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const [currentUrl, setCurrentUrl] = useState("");

    /** Adiciona https:// automaticamente se o protocolo estiver ausente. */
  const normalizeUrl = (url: string): string => {
    const trimmedUrl = url.trim();

    if (!/^https?:\/\//i.test(trimmedUrl)) {
      return `https://${trimmedUrl}`;
    }

    return trimmedUrl;
  };

  const isValidUrl = (url: string): boolean => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  /** Extrai o nome do domínio mesmo sem protocolo — funciona com "site.com.br", "www.site.com", etc. */
  const extractDomainName = (url: string): string => {
    try {
      return new URL(url)
      .hostname
      .replace("www.", "")
      .split(".")[0];
    } catch {
      return "site";
    }
  };

  const requestCheck = async (url: string) => {
    const normalizedUrl = normalizeUrl(url);
    
    if (!isValidUrl(normalizedUrl)) {
      setError(
        "URL inválida. Por favor, insira uma URL válida (ex: site.com.br, www.site.com ou https://site.com)."
      );
      return;
    }

    setLoading(true);
    
    try {
      const { data } = await api.post("/check", { url: normalizedUrl });

      // Garantia de formato: suporta tanto data.results aninhado quanto data direto
      const finalResults = {
        ...data.results,
        url: data.url || normalizedUrl,
        business_segment: data.business_segment,
        executive_analysis: data.executive_analysis,
        priority_roadmap: data.priority_roadmap
      };
      setResult(finalResults);

      // O contraste já vem calculado no /check — evita uma 2ª chamada (e um 2º Playwright).
      setContrastResult(data.contrast_issues ?? data.results?.contrast ?? []);
    } catch (err) {
      console.error("Erro na requisição principal:", err);
      setError("Erro ao processar a verificação principal.");
      return;
    } finally {
      setLoading(false);
    }
  };

  const handleCheck = (url: string) => {
    // Guarda o valor original para o input (sem alterar o que o usuário digitou)
    setCurrentUrl(url);
    setResult(null);
    setContrastResult([]);
    setError("");
    requestCheck(url);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col gap-4">
      <header className="bg-gradient-to-r from-blue-700 via-blue-500 to-cyan-400 shadow-lg">
        <nav className="max-w-6xl mx-auto flex p-4" aria-label="Navegação principal">
          <div className=" flex items-center gap-2">
            <div>
              <img
                src={lupaIcon}
                alt="Ícone A11y Inspector"
                className="w-12 h-12"
              />
            </div>
            <div>
              <h1 className="text-2xl md:text-4xl font-extrabold text-white drop-shadow">
                A11y_Inspector
              </h1>
              <p className="text-white text-opacity-90 mt-1 font-medium">
                Acessibilidade. Inclusão. Transforme a web para todos.
              </p>
            </div>
          </div>
        </nav>
      </header>

      <main className="max-w-6xl mx-auto flex flex-col gap-4 px-4">
        <div className="bg-blue-50 border-l-4 border-blue-400 p-4  rounded">
          <p className="text-blue-900 font-semibold">
            Acessibilidade digital é fundamental para garantir que todas as
            pessoas possam navegar na web. No Brasil, a{" "}
            <span className="font-bold">Lei Brasileira de Inclusão (LBI)</span>{" "}
            exige que sites sejam acessíveis. Utilize esta ferramenta para
            identificar e corrigir barreiras no seu site!
          </p>
        </div>

        <UrlForm
          url={currentUrl}
          onUrl={setCurrentUrl}
          onResult={handleCheck}
          loading={loading}
        />

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded">
            {error}
          </div>
        )}

        {loading && <InspectorLoader />}

        {!loading && (result || contrastResult.length) ? (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl text-blue-900 font-semibold mb-6 text-center">
              Resultados da Inspeção
            </h2>
            <div className="grid gap-2 grid-cols-1 md:grid-cols-2">
              {result && (
                <>
                    <ResultCard
                      title="Imagens sem descrição (alt)"
                      description="Todas as imagens devem ter texto alternativo para leitores de tela."
                      sucessDescription="Todas as imagens possuem texto alternativo."
                      items={result.screenshots ?? []}
                    />

                    <ResultCard
                      title="Campos de formulário sem rótulo"
                      description="Cada campo deve ter um <label>(rótulo) associado."
                      sucessDescription="Todos os campos de formulário possuem rótulo."
                      items={result.forms?.length ? result.forms : []}
                    />

                    <ResultCard
                      title="Problemas na hierarquia de títulos"
                      description="Use apenas um <h1>(título) e evite pular níveis."
                      sucessDescription="Todos os títulos estão em conformidade."
                      items={result.headings?.length ? result.headings : []}
                    />

                    <ResultCard
                      title="Links com texto vago"
                      description="Evite usar textos genéricos como “clique aqui” em links. Prefira descrições que indiquem o destino ou a ação."
                      sucessDescription="Todos os links possuem textos claros."
                      items={result.links?.length ? result.links : []}
                    />

                    <ResultCard
                      title="Botões sem rótulo acessível"
                      description="Todos os botões devem ter texto visível ou atributos como aria-label."
                      sucessDescription="Todos os botões possuem rótulos acessíveis."
                      items={result.buttons?.length ? result.buttons : []}
                    />

                    <ResultCard
                      title="Navegação por teclado / foco"
                      description="Verifica controles e elementos interativos que não podem ser alcançados ou focados durante a navegação por teclado."
                      sucessDescription="A navegação por teclado está adequada."
                      items={result.focus?.length ? result.focus : []}
                    />

                    <ResultCard
                      title="Landmarks semânticos ausentes"
                      description="É necessário usar as tags semânticas: <main>, <nav>, <header>, <footer>, para organizar a estrutura da página."
                      sucessDescription="Todos os landmarks estão presentes e corretos."
                      items={result.landmarks?.length ? result.landmarks : []}
                    />
                </>
              )}

              <ResultCard
                title="Problemas de contraste"
                description="Todos os textos devem ter contraste suficiente com o fundo para garantir legibilidade."
                sucessDescription="Todos os textos possuem contraste adequado."
                items={contrastResult}
              />
              {result && (
                <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100 md:col-span-2 w-full mt-1">
                  <h3 className="text-lg font-bold text-gray-800 mb-1">Exportar Relatórios Oficiais</h3>
                  <p className="text-sm text-gray-500 mb-4">Escolha o modelo de documento ideal para a sua audiência:</p>
                  
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 w-full">
                    
                    {/*1. BOTÃO DO RELATÓRIO EXECUTIVO (Para Clientes / Gestores) */}
                    <div className="flex flex-col w-full gap-2">
                      <PDFDownloadLink
                        document={
                          <ExecutiveReportPDF
                            result={result}
                            url={currentUrl || result.url || "URL não informada"}
                            businessSegment={result?.business_segment || "Geral"}
                            executiveAnalysis={result?.executive_analysis || "Análise estratégica em processamento..."}
                          />
                        }
                        fileName={`relatorio-executivo-${extractDomainName(currentUrl)}.pdf`}
                        className="w-full"
                      >
                        {({ loading: pdfLoading, error: pdfError }) => (
                          <button
                            type="button"
                            disabled={pdfLoading || !!pdfError}
                            className={`px-4 py-3 rounded-lg font-semibold w-full text-center flex flex-col items-center justify-center gap-1 transition-all shadow-sm ${
                              pdfError 
                                ? "bg-red-100 text-red-700 cursor-not-allowed border border-red-200" 
                                : "bg-indigo-600 text-white hover:bg-indigo-700 cursor-pointer"
                            }`}
                          >
                            <span className="text-base font-bold">Relatório Executivo</span>
                            <span className="text-xs font-normal opacity-90">
                              {pdfError ? "Erro na estrutura do documento" : pdfLoading ? "Construindo PDF..." : "Baixar para Gestão / Compliance"}
                            </span>
                          </button>
                        )}
        </PDFDownloadLink>
      </div>

      {/*2. BOTÃO DO CHECKLIST TÉCNICO (Para Desenvolvedores / TI) */}
      <div className="flex flex-col w-full gap-2">
        <PDFDownloadLink
          document={
            <TechnicalReportPDF
              result={result}
              contrastResult={contrastResult || []}
              url={currentUrl || "URL não informada"}
            />
          }
          fileName={`checklist-tecnico-${extractDomainName(currentUrl)}.pdf`}
          className="w-full"
        >
          {({ loading: pdfLoading, error: pdfError }) => (
            <button
              type="button"
              disabled={pdfLoading || !!pdfError}
              className={`px-4 py-3 rounded-lg font-semibold w-full text-center flex flex-col items-center justify-center gap-1 transition-all shadow-sm ${
                pdfError 
                  ? "bg-red-100 text-red-700 cursor-not-allowed border border-red-200" 
                  : "bg-slate-800 text-white hover:bg-slate-900 cursor-pointer"
              }`}
            >
              <span className="text-base font-bold">Checklist Técnico</span>
              <span className="text-xs font-normal opacity-90">
                {pdfError ? "Erro na estrutura do documento" : pdfLoading ? "Construindo PDF..." : "Baixar para Engenharia / TI"}
              </span>
            </button>
          )}
        </PDFDownloadLink>
      </div>

    </div>
  </div>
)}
            </div>
          </div>
        ) : null}
      </main>
      <footer className="mt-auto w-full py-4 bg-blue-700 text-white text-center text-sm rounded-t shadow">
        © 2026 Desenvolvido por Elisiane Quadros
      </footer>
    </div>
  );
}

export default App;
