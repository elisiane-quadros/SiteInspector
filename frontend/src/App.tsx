import { useState } from "react";
import UrlForm from "./components/UrlForm";
import type { AccessibilityResults } from "./interfaces/AccessibilityResults";
import ResultCard from "./components/ResultCard";
import api from "./services/api";

import type { ContrastItem } from "./interfaces/ResultContrast";
import { PDFDownloadLink } from "@react-pdf/renderer";
import { TechnicalReportPDF } from "./components/TechnicalReportPDF";
import { ExecutiveReportPDF } from "./components/ExecutiveReportPDF";

function App() {
  const [result, setResult] = useState<AccessibilityResults | null>(null);
  const [contrastResult, setContrastResult] = useState<ContrastItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const [errorContrast, setErrorContrast] = useState<string>("");
  const [contrastLoading, setContrastLoading] = useState(false);
  const [currentUrl, setCurrentUrl] = useState("");
 // const [pdfError, setPdfError] = useState<string>("");

  const isValidUrl = (url: string): boolean => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  const extractDomainName = (url: string): string => {
  try {
    return new URL(url).hostname.replace("www.", "").split(".")[0];
  } catch {
    return "site";
  }
};

  const requestCheck = async (url: string) => {
    if (!isValidUrl(url)) {
      setError(
        "URL inválida. Por favor, insira uma URL válida (ex: https://www.site.com)."
      );
      return;
    }
    setLoading(true);
    setContrastLoading(true);
    try {
      const { data } = await api.post("/check", { url });

      // 💡 GARANTIA DE FORMATO: Se o backend devolver a estrutura dentro de data.results ou direto em data
      const finalResults = {
        ...data.results,
        url: data.url || url,
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
      setContrastLoading(false);
    }
  };

  const handleCheck = (url: string) => {
    setCurrentUrl(url);
    setResult(null);
    setContrastResult([]);
    setError("");
    setErrorContrast("");
    requestCheck(url);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col gap-4">
      <header className="bg-gradient-to-r from-blue-700 via-blue-500 to-cyan-400 shadow-lg">
        <div className="max-w-6xl mx-auto flex p-4">
          <div className=" flex items-center gap-4">
            <div className="bg-white rounded-full p-2 shadow-md">
              <svg
                className="w-10 h-10 text-blue-700"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 4v16m8-8H4"
                />
              </svg>
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
        </div>
      </header>

      <div className="max-w-6xl mx-auto flex flex-col gap-4 px-4">
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
          loading={loading || contrastLoading}
        />

        {error && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded">
            {error}
          </div>
        )}

        {errorContrast && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6 rounded">
            {errorContrast}
          </div>
        )}

        {result || contrastResult.length ? (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl text-blue-900 font-semibold mb-6 text-center">
              Resultados da Inspeção
            </h2>
            <div className="grid gap-6 grid-cols-1 md:grid-cols-2">
              {loading ? (
                <span>Carregando...</span>
              ) : (
                result && (
                  <>
                    <ResultCard
                      title="Imagens sem descrição (alt)"
                      description="Todas as imagens devem ter texto alternativo para leitores de tela."
                      sucessDescription="Todas as imagens possuem texto alternativo."
                      items={result.images.length ? result.images : []}
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
                )
              )}

              {contrastLoading ? (
                <div className="flex items-center justify-center md:col-span-1">
                  <svg
                    className="animate-spin h-5 w-5 text-blue-600 mr-2"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8v8z"
                    ></path>
                  </svg>
                  <span>Carregando resultados de contraste...</span>
                </div>
              ) : (
                <ResultCard
                  title="Problemas de contraste"
                  description="Todos os textos devem ter contraste suficiente com o fundo para garantir legibilidade."
                  sucessDescription="Todos os textos possuem contraste adequado."
                  items={contrastResult}
                />
              )}
              {!loading && !contrastLoading && result && (
                <div className="bg-white p-6 rounded-lg shadow-md border border-gray-100 md:col-span-2 w-full mt-4">
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
      </div>
      <footer className="mt-auto w-full py-4 bg-blue-700 text-white text-center text-sm rounded-t shadow">
        © 2025 por Elisiane Quadros — Desenvolvido com{" "}
        <span className="font-bold">A11y_Inspector</span>
      </footer>
    </div>
  );
}

export default App;
