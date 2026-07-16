import React from "react";

interface UrlFormProps {
  onResult: (url: string) => void;
  url: string;
  onUrl: React.Dispatch<React.SetStateAction<string>>;
  loading: boolean;
}

export default function UrlForm({
  onResult,
  loading,
  onUrl,
  url,
}: UrlFormProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onResult(url);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="bg-white rounded-lg shadow p-6  gap-4 items-center justify-center">
        <label htmlFor="url-input" className="block mb-2 font-medium text-sm">
          Digite a URL para verificar acessibilidade:
        </label>
        <div className="flex gap-4">
          <input
            id="url-input"
            type="text"
            value={url}
            onChange={(e) => onUrl(e.target.value)}
            placeholder="ex: site.com.br, www.site.com, https://site.com"
            className="w-full border border-gray-300 p-2 rounded  focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
          <button
            type="submit"
            disabled={loading}
            className={`flex items-center justify-center gap-2 text-white w-36 p-2 rounded ${loading ? "bg-slate-400" : "bg-blue-600  hover:bg-blue-700"} `}
          >
            {loading && (
              <svg
                className="animate-spin h-5 w-5 text-white"
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
            )}
            {loading ? "Verificando" : "Verificar"}
          </button>
        </div>
      </div>
    </form>
  );
}
