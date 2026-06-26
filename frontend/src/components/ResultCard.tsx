import { useState } from "react";
import type { ResultItem } from "../interfaces/ResultItem";

interface ResultCardProps {
  title: string;
  description: string;
  sucessDescription: string;
  items: Array<ResultItem | string>;
}

export default function ResultCard({
  title,
  description,
  sucessDescription,
  items,
}: ResultCardProps) {
  const [modalOpen, setModalOpen] = useState(false);

  return (
    <div className="border border-gray-200 rounded-lg p-4 shadow-sm bg-white">
      <div className="flex justify-between items-start">
        <div>
          <h3 className="text-lg font-semibold text-gray-800">{title}</h3>
          <p className="text-sm text-gray-500">{description}</p>
        </div>
        {items.length ? (
          <button
            onClick={() => setModalOpen(true)}
            className="text-sm font-medium whitespace-nowrap text-blue-600 hover:text-blue-800 hover:underline"
          >
            Ver mais
          </button>
        ) : null}
      </div>
      
      <div className="mt-3">
        {items.length ? (
          <span className="text-sm font-medium text-red-600 bg-red-50 px-2 py-1 rounded">
            {items.length} {items.length === 1 ? "problema encontrado" : "problemas encontrados"}
          </span>
        ) : (
          <span className="text-sm font-medium text-green-600 bg-green-50 px-2 py-1 rounded">
            {sucessDescription}
          </span>
        )}
      </div>

      {/* Janela modal estruturada */}
      {modalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4 animate-fade-in">
          <div className="bg-white rounded-xl shadow-xl max-w-3xl w-full max-h-[85vh] flex flex-col overflow-hidden">
            
            {/* Cabeçalho da Modal */}
            <div className="p-6 border-b border-gray-100 flex justify-between items-center bg-gray-50">
              <div>
                <h4 className="text-xl font-bold text-gray-900">{title}</h4>
                <p className="text-sm text-gray-500 mt-1">Detalhes e orientações de correção</p>
              </div>
              <span className="text-sm font-semibold text-red-600 bg-red-100 px-2.5 py-1 rounded-full">
                {items.length} {items.length === 1 ? "Erro" : "Erros"}
              </span>
            </div>

            {/* Conteúdo Rolável dos Erros */}
            <div className="p-6 overflow-y-auto space-y-8 divide-y divide-gray-100 flex-1">
              {items.map((item, idx) => {
                const isString = typeof item === "string";

                // Mapeamento de Fallbacks caso algum campo mude
                const friendlyTitle = !isString && item.friendly_title ? item.friendly_title : "Inconformidade Encontrada";
                const friendlyMessage = !isString && item.friendly_message ? item.friendly_message : (isString ? item : item.message);
                const howToFix = !isString && item.how_to_fix ? item.how_to_fix : (!isString ? item.suggestion : undefined);
                
                return (
                  <div key={idx} className={`${idx > 0 ? "pt-6" : ""} space-y-4`}>
                    
                    {/* SEÇÃO 1: VISÃO DE NEGÓCIOS (Focado no Cliente Leigo / PJ) */}
                    <div className="space-y-2">
                      <h5 className="font-bold text-base text-gray-800 flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-red-500"></span>
                        {friendlyTitle}
                      </h5>
                      <p className="text-sm text-gray-600 leading-relaxed">
                        {friendlyMessage}
                      </p>
                    </div>

                    {howToFix && (
                      <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-r-lg">
                        <h6 className="text-xs font-bold text-blue-800 uppercase tracking-wider mb-1">Como resolver no seu site:</h6>
                        <p className="text-sm text-blue-950 leading-relaxed">{howToFix}</p>
                      </div>
                    )}

                    {typeof item === "object" && item !== null && (item as any).ai_description_suggestion && (
                      <div className="bg-purple-50 border border-purple-200 p-4 rounded-lg space-y-2 mt-3">
                        <div className="flex items-center gap-2 text-purple-800 font-bold text-xs uppercase tracking-wider">
                           Sugestão Automática do Assistente de IA
                        </div>
                        <p className="text-sm text-purple-950 italic">
                          "{(item as any).ai_description_suggestion}"
                        </p>
                        {(item as any).image_url && (
                          <a 
                            href={(item as any).image_url} 
                            target="_blank" 
                            rel="noreferrer" 
                            className="inline-block text-xs text-purple-700 hover:underline mt-1 font-medium"
                          >
                            Visualizar imagem original afetada
                          </a>
                        )}
                      </div>
                    )}

                    {/* SEÇÃO 2: DETALHES TÉCNICOS (Oculto sob o <details>, focado no Desenvolvedor) */}
                    {!isString && (item.html || item.message) && (
                      <details className="group border border-gray-200 rounded-lg bg-gray-50 overflow-hidden transition-all">
                        <summary className="list-none flex justify-between items-center p-3 text-xs font-semibold text-gray-500 cursor-pointer hover:bg-gray-100 select-none">
                          <span>DETALHES TÉCNICOS (PARA DESENVOLVEDORES)</span>
                          <span className="transition-transform group-open:rotate-180 text-gray-400">▼</span>
                        </summary>
                        <div className="p-4 border-t border-gray-200 bg-white space-y-3 text-xs font-mono">
                          {item.message && (
                            <div>
                              <span className="font-bold text-gray-700 block mb-1">Log do Erro:</span>
                              <p className="text-gray-600 bg-gray-50 p-2 rounded border border-gray-100">{item.message}</p>
                            </div>
                          )}
                          {item.wcag && (
                            <p className="text-gray-600"><span className="font-bold text-gray-700">Critério WCAG:</span> {item.wcag}</p>
                          )}
                          {item.html && (
                            <div>
                              <span className="font-bold text-gray-700 block mb-1">Snippet HTML Afetado:</span>
                              <pre className="bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto break-all whitespace-pre-wrap max-h-40">
                                <code>{item.html}</code>
                              </pre>
                            </div>
                          )}
                        </div>
                      </details>
                    )}

                  </div>
                );
              })}
            </div>

            {/* Rodapé da Modal */}
            <div className="p-4 border-t border-gray-100 flex justify-end bg-gray-50">
              <button
                onClick={() => setModalOpen(false)}
                className="px-5 py-2 bg-gray-800 hover:bg-gray-900 text-white rounded-lg text-sm font-medium shadow-sm transition-colors"
              >
                Concluído
              </button>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}