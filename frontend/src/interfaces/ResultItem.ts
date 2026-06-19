export interface ResultItem {
  wcag?: string;
  severity?: string;
  element?: string;
  message?: string;
  suggestion?: string;
  html?: string | null;
  
  // --- Novos campos da Arquitetura Dual ---
  friendly_title?: string;
  friendly_message?: string;
  how_to_fix?: string;
  
  // --- Campos específicos de imagem (Gemini) ---
  image_url?: string | null;
  ai_description_suggestion?: string | null;

  // Compatibilidade com chaves antigas se houver
  text?: string;
  src?: string;
  href?: string;
  name?: string;
  tag?: string;
  id?: string;
}