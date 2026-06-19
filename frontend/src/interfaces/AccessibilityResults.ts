import type { ResultItem } from "./ResultItem";

export interface PriorityItem {
  priority: "P1" | "P2" | "P3";
  label: string;
  category: string;
  count: number;
  reason: string;
}

export interface AccessibilityResults {
  images: ResultItem[];
  focus: Array<string | ResultItem>;
  forms: ResultItem[];
  headings: Array<string | ResultItem>;
  links: Array<string | ResultItem>;
  buttons: ResultItem[];
  landmarks: Array<string | ResultItem>;
  url: string;
  business_segment: string;
  executive_analysis: string;
  priority_roadmap: PriorityItem[];
}



