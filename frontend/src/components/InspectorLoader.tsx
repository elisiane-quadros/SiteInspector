import { useEffect, useState } from "react";

// Mensagens exibidas em sequência durante a espera. Como o front faz uma única
// chamada e aguarda, a progressão é por tempo (narrativa) — não são eventos
// reais do backend. Mesmo assim, comunicar etapas reduz a sensação de espera.
const STEPS = [
  "Carregando e mapeando a estrutura do site...",
  "Analisando imagens, formulários e elementos interativos...",
  "Verificando conformidade com as diretrizes WCAG...",
  "Preparando recomendações de correção com IA...",
];

const PROGRESS = [15, 40, 75, 95];

export default function InspectorLoader() {
  const [step, setStep] = useState(0);

  useEffect(() => {
    // Avança a cada 3s e PARA na última etapa (a mais demorada, a IA),
    // em vez de ficar em loop dando a impressão de que reiniciou.
    const id = setInterval(() => {
      setStep((s) => (s + 1 < STEPS.length ? s + 1 : s));
    }, 3000);
    return () => clearInterval(id);
  }, []);

  return (
    <div
      role="status"
      aria-live="polite"
      className="bg-white rounded-lg shadow p-10 flex flex-col items-center gap-6"
    >
      {/* Área "inspecionada": barras simulam o conteúdo; a lupa varre por cima.
          aria-hidden porque é puramente decorativa — o texto abaixo informa. */}
      <div className="relative w-56 h-24" aria-hidden="true">
        <div className="space-y-2.5 pt-2">
          <div className="h-2.5 w-3/4 rounded bg-gray-200" />
          <div className="h-2.5 w-full rounded bg-gray-200" />
          <div className="h-2.5 w-5/6 rounded bg-gray-200" />
          <div className="h-2.5 w-2/3 rounded bg-gray-200" />
        </div>

        <svg
          className="absolute top-0 left-0 w-12 h-12 text-blue-600 drop-shadow-md motion-safe:animate-magnify-sweep motion-reduce:animate-none"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
        >
          <circle cx="11" cy="11" r="7" />
          <line x1="16.5" y1="16.5" x2="21" y2="21" />
        </svg>
      </div>

      <p className="text-blue-900 font-semibold text-center min-h-[1.5rem]">
        {STEPS[step]}
      </p>
      <div className="text-sm text-gray-500 font-medium">
        {PROGRESS[step]}%
      </div>

      {/* Anúncio para leitores de tela (visualmente oculto). */}
      <span className="sr-only">
        Inspeção de acessibilidade em andamento, por favor aguarde.
      </span>
    </div>
  );
}
