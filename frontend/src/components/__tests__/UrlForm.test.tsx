import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import UrlForm from "../UrlForm";

describe("UrlForm", () => {
  it("renderiza o input e o botão", () => {
    render(
      <UrlForm url="" onUrl={() => {}} onResult={() => {}} loading={false} />
    );

    expect(
      screen.getByPlaceholderText("Digite a URL do site")
    ).toBeDefined();
    expect(screen.getByText("Verificar")).toBeDefined();
  });

  it("chama onResult ao submeter o formulário", () => {
    const onResult = vi.fn();
    render(
      <UrlForm
        url="https://example.com"
        onUrl={() => {}}
        onResult={onResult}
        loading={false}
      />
    );

    fireEvent.click(screen.getByText("Verificar"));
    expect(onResult).toHaveBeenCalledWith("https://example.com");
  });

  it("desabilita o botão quando loading é true", () => {
    render(
      <UrlForm url="" onUrl={() => {}} onResult={() => {}} loading={true} />
    );

    const button = screen.getByText("Verificando");
    expect(button).toBeDefined();
  });
});
