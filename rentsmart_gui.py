import csv
import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class Imovel:
    """Classe base que representa um imóvel genérico da R.M Imóveis."""

    def __init__(self, tipo, aluguel_base):
        self.tipo = tipo
        self.aluguel_base = aluguel_base

    def calcular_adicionais(self):
        return 0.0

    def calcular_desconto(self, subtotal):
        return 0.0

    def calcular_aluguel_mensal(self):
        subtotal = self.aluguel_base + self.calcular_adicionais()
        desconto = self.calcular_desconto(subtotal)
        return subtotal - desconto

    def obter_detalhes(self):
        return [f"Aluguel Base ({self.tipo}): R$ {self.aluguel_base:.2f}"]


class Apartamento(Imovel):
    """Subclasse para Apartamentos com regras específicas de quartos, garagem e desconto."""

    def __init__(self, quartos, garagem, possui_criancas):
        super().__init__("Apartamento", 700.00)
        self.quartos = quartos
        self.garagem = garagem
        self.possui_criancas = possui_criancas

    def calcular_adicionais(self):
        adicional = 0.0
        if self.quartos == 2:
            adicional += 200.00
        if self.garagem:
            adicional += 300.00
        return adicional

    def calcular_desconto(self, subtotal):
        if not self.possui_criancas:
            return subtotal * 0.05
        return 0.0

    def obter_detalhes(self):
        detalhes = super().obter_detalhes()
        if self.quartos == 2:
            detalhes.append("Adicional de 2º quarto: + R$ 200.00")
        else:
            detalhes.append("Configuração: 1 quarto (sem adicional)")

        if self.garagem:
            detalhes.append("Adicional de vaga de garagem: + R$ 300.00")
        else:
            detalhes.append("Vaga de garagem: Não incluída")

        subtotal = self.aluguel_base + self.calcular_adicionais()
        desconto = self.calcular_desconto(subtotal)
        if desconto > 0:
            detalhes.append(f"Desconto (Sem crianças - 5%): - R$ {desconto:.2f}")
        return detalhes


class Casa(Imovel):
    """Subclasse para Casas com regras específicas de quartos e garagem."""

    def __init__(self, quartos, garagem):
        super().__init__("Casa", 900.00)
        self.quartos = quartos
        self.garagem = garagem

    def calcular_adicionais(self):
        adicional = 0.0
        if self.quartos == 2:
            adicional += 250.00
        if self.garagem:
            adicional += 300.00
        return adicional

    def obter_detalhes(self):
        detalhes = super().obter_detalhes()
        if self.quartos == 2:
            detalhes.append("Adicional de 2º quarto: + R$ 250.00")
        else:
            detalhes.append("Configuração: 1 quarto (sem adicional)")

        if self.garagem:
            detalhes.append("Adicional de vaga de garagem: + R$ 300.00")
        else:
            detalhes.append("Vaga de garagem: Não incluída")
        return detalhes


class Estudio(Imovel):
    """Subclasse para Estúdios com regra especial de pacote de estacionamento."""

    def __init__(self, pacote_garagem, vagas_extras=0):
        super().__init__("Estúdio", 1200.00)
        self.pacote_garagem = pacote_garagem
        self.vagas_extras = vagas_extras

    def calcular_adicionais(self):
        adicional = 0.0
        if self.pacote_garagem:
            adicional += 250.00 + (self.vagas_extras * 60.00)
        return adicional

    def obter_detalhes(self):
        detalhes = super().obter_detalhes()
        if self.pacote_garagem:
            detalhes.append("Pacote inicial de estacionamento (2 vagas): + R$ 250.00")
            if self.vagas_extras > 0:
                custo_extra = self.vagas_extras * 60.00
                detalhes.append(
                    f"Vagas extras ({self.vagas_extras}x R$ 60.00): + R$ {custo_extra:.2f}"
                )
        else:
            detalhes.append("Estacionamento: Não contratado")
        return detalhes


class OrcamentoLocacao:
    """Classe responsável por gerir o contrato, gerar o texto de resumo e exportar o CSV."""

    TAXA_CONTRATUAL = 2000.00

    def __init__(self, nome_cliente, imovel, parcelas_taxa):
        self.nome_cliente = nome_cliente
        self.imovel = imovel
        self.parcelas_taxa = parcelas_taxa

    def calcular_valor_parcela_taxa(self):
        return self.TAXA_CONTRATUAL / self.parcelas_taxa

    def obter_texto_resumo(self):
        aluguel_final = self.imovel.calcular_aluguel_mensal()
        valor_parcela_taxa = self.calcular_valor_parcela_taxa()

        linhas = [
            f"Cliente: {self.nome_cliente}",
            f"Categoria do Imóvel: {self.imovel.tipo}",
            "-" * 50,
            "DETALHAMENTO DO ALUGUEL MENSAL:",
        ]
        for detalhe in self.imovel.obter_detalhes():
            linhas.append(f"  • {detalhe}")

        linhas.extend([
            f"\n  >> VALOR MENSAL DA LOCAÇÃO: R$ {aluguel_final:.2f}",
            "-" * 50,
            "CONDIÇÕES DA TAXA CONTRATUAL (Separado do aluguel):",
            f"  • Valor Total da Taxa: R$ {self.TAXA_CONTRATUAL:.2f}",
            f"  • Parcelamento: {self.parcelas_taxa}x de R$ {valor_parcela_taxa:.2f}",
        ])
        return "\n".join(linhas)

    def salvar_csv(self, caminho_arquivo):
        aluguel_final = self.imovel.calcular_aluguel_mensal()
        valor_parcela_taxa = self.calcular_valor_parcela_taxa()

        with open(caminho_arquivo, mode="w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow([
                "Mês",
                "Aluguel Mensal (R$)",
                "Taxa Contratual (R$)",
                "Total Previsto no Mês (R$)",
            ])

            for mes in range(1, 13):
                taxa_mes = valor_parcela_taxa if mes <= self.parcelas_taxa else 0.0
                total_mes = aluguel_final + taxa_mes
                escritor.writerow([
                    f"Mês {mes}",
                    f"{aluguel_final:.2f}",
                    f"{taxa_mes:.2f}",
                    f"{total_mes:.2f}",
                ])


class RentSmartApp:
    """Classe que gere a janela e os componentes visuais da aplicação."""

    def __init__(self, root):
        self.root = root
        self.root.title("RentSmart - Sistema de Orçamento (R.M Imóveis)")
        self.root.geometry("620x680")
        self.root.resizable(False, False)

        self.orcamento_atual = None

        # Variáveis de controlo da interface
        self.var_nome = tk.StringVar()
        self.var_categoria = tk.StringVar(value="Apartamento")
        self.var_quartos = tk.IntVar(value=1)
        self.var_garagem = tk.BooleanVar(value=False)
        self.var_criancas = tk.BooleanVar(value=False)
        self.var_pacote_estudio = tk.BooleanVar(value=False)
        self.var_vagas_extras = tk.StringVar(value="0")
        self.var_parcelas = tk.IntVar(value=1)

        self.construir_interface()
        self.atualizar_campos_categoria()

    def construir_interface(self):
        frame_principal = ttk.Frame(self.root, padding=15)
        frame_principal.pack(fill="both", expand=True)

        # Título
        titulo = ttk.Label(
            frame_principal,
            text="RentSmart - R.M Imóveis",
            font=("Segoe UI", 15, "bold"),
        )
        titulo.pack(pady=(0, 10))

        # 1. Dados do Cliente e Categoria
        frame_cliente = ttk.LabelFrame(frame_principal, text=" 1. Dados Básicos ", padding=10)
        frame_cliente.pack(fill="x", pady=5)

        ttk.Label(frame_cliente, text="Nome do Cliente:").grid(row=0, column=0, sticky="w", pady=4)
        ttk.Entry(frame_cliente, textvariable=self.var_nome, width=42).grid(row=0, column=1, sticky="w", padx=8, pady=4)

        ttk.Label(frame_cliente, text="Categoria do Imóvel:").grid(row=1, column=0, sticky="w", pady=4)
        combo_cat = ttk.Combobox(
            frame_cliente,
            textvariable=self.var_categoria,
            values=["Apartamento", "Casa", "Estúdio"],
            state="readonly",
            width=39,
        )
        combo_cat.grid(row=1, column=1, sticky="w", padx=8, pady=4)
        combo_cat.bind("<<ComboboxSelected>>", lambda e: self.atualizar_campos_categoria())

        # 2. Configuração dinâmica do Imóvel
        self.frame_opcoes = ttk.LabelFrame(frame_principal, text=" 2. Características do Imóvel ", padding=10)
        self.frame_opcoes.pack(fill="x", pady=5)

        # 3. Taxa Contratual
        frame_taxa = ttk.LabelFrame(frame_principal, text=" 3. Taxa Contratual (R$ 2.000,00) ", padding=10)
        frame_taxa.pack(fill="x", pady=5)

        ttk.Label(frame_taxa, text="Parcelamento da Taxa (1x a 5x):").grid(row=0, column=0, sticky="w")
        combo_parc = ttk.Combobox(
            frame_taxa,
            textvariable=self.var_parcelas,
            values=[1, 2, 3, 4, 5],
            state="readonly",
            width=10,
        )
        combo_parc.grid(row=0, column=1, sticky="w", padx=10)

        # Botões de Ação
        frame_botoes = ttk.Frame(frame_principal)
        frame_botoes.pack(fill="x", pady=12)

        btn_calcular = ttk.Button(
            frame_botoes,
            text="Calcular Orçamento",
            command=self.calcular_orcamento,
        )
        btn_calcular.pack(side="left", expand=True, fill="x", padx=(0, 5), ipady=4)

        self.btn_csv = ttk.Button(
            frame_botoes,
            text="Guardar Projeção CSV (12 Meses)...",
            command=self.baixar_csv,
            state="disabled",
        )
        self.btn_csv.pack(side="left", expand=True, fill="x", padx=(5, 0), ipady=4)

        # 4. Área de Resumo
        frame_resumo = ttk.LabelFrame(frame_principal, text=" 4. Resumo Detalhado do Orçamento ", padding=10)
        frame_resumo.pack(fill="both", expand=True, pady=5)

        self.texto_resumo = tk.Text(
            frame_resumo,
            height=13,
            state="disabled",
            font=("Consolas", 10),
            bg="#f8f9fa",
        )
        self.texto_resumo.pack(fill="both", expand=True)

    def atualizar_campos_categoria(self):
        # Limpa os campos atuais antes de desenhar os da categoria selecionada
        for widget in self.frame_opcoes.winfo_children():
            widget.destroy()

        cat = self.var_categoria.get()

        if cat in ["Apartamento", "Casa"]:
            adicional_txt = "R$ 200,00" if cat == "Apartamento" else "R$ 250,00"
            ttk.Label(self.frame_opcoes, text="Quantidade de Quartos:").grid(row=0, column=0, sticky="w", pady=3)
            ttk.Radiobutton(
                self.frame_opcoes, text="1 Quarto (Base)", variable=self.var_quartos, value=1
            ).grid(row=0, column=1, sticky="w", padx=5)
            ttk.Radiobutton(
                self.frame_opcoes, text=f"2 Quartos (+{adicional_txt})", variable=self.var_quartos, value=2
            ).grid(row=0, column=2, sticky="w", padx=5)

            ttk.Checkbutton(
                self.frame_opcoes,
                text="Incluir vaga de garagem (+R$ 300,00)",
                variable=self.var_garagem,
            ).grid(row=1, column=0, columnspan=3, sticky="w", pady=4)

            if cat == "Apartamento":
                ttk.Checkbutton(
                    self.frame_opcoes,
                    text="O cliente possui crianças? (Desmarcado aplica 5% de desconto)",
                    variable=self.var_criancas,
                ).grid(row=2, column=0, columnspan=3, sticky="w", pady=4)

        elif cat == "Estúdio":
            ttk.Checkbutton(
                self.frame_opcoes,
                text="Contratar pacote inicial de estacionamento (2 vagas por +R$ 250,00)",
                variable=self.var_pacote_estudio,
                command=self.atualizar_estado_vagas_extras,
            ).grid(row=0, column=0, columnspan=2, sticky="w", pady=4)

            ttk.Label(self.frame_opcoes, text="Vagas adicionais (+R$ 60,00 cada):").grid(
                row=1, column=0, sticky="w", pady=4
            )
            self.spin_extras = ttk.Spinbox(
                self.frame_opcoes,
                from_=0,
                to=20,
                textvariable=self.var_vagas_extras,
                width=8,
            )
            self.spin_extras.grid(row=1, column=1, sticky="w", padx=10, pady=4)
            self.atualizar_estado_vagas_extras()

    def atualizar_estado_vagas_extras(self):
        if self.var_pacote_estudio.get():
            self.spin_extras.config(state="normal")
        else:
            self.var_vagas_extras.set("0")
            self.spin_extras.config(state="disabled")

    def calcular_orcamento(self):
        nome = self.var_nome.get().strip()
        if not nome:
            messagebox.showwarning("Validação de Entrada", "Por favor, informe o nome do cliente.")
            return

        cat = self.var_categoria.get()

        if cat == "Apartamento":
            imovel = Apartamento(
                quartos=self.var_quartos.get(),
                garagem=self.var_garagem.get(),
                possui_criancas=self.var_criancas.get(),
            )
        elif cat == "Casa":
            imovel = Casa(
                quartos=self.var_quartos.get(),
                garagem=self.var_garagem.get(),
            )
        else:
            pacote = self.var_pacote_estudio.get()
            extras = 0
            if pacote:
                try:
                    extras = int(self.var_vagas_extras.get())
                    if extras < 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror(
                        "Validação de Entrada",
                        "A quantidade de vagas adicionais deve ser um número inteiro maior ou igual a 0.",
                    )
                    return
            imovel = Estudio(pacote_garagem=pacote, vagas_extras=extras)

        parcelas = int(self.var_parcelas.get())
        self.orcamento_atual = OrcamentoLocacao(nome, imovel, parcelas)

        # Atualiza a caixa de texto com o resumo
        self.texto_resumo.config(state="normal")
        self.texto_resumo.delete("1.0", tk.END)
        self.texto_resumo.insert(tk.END, self.orcamento_atual.obter_texto_resumo())
        self.texto_resumo.config(state="disabled")

        # Ativa o botão de download do CSV
        self.btn_csv.config(state="normal")

    def baixar_csv(self):
        if not self.orcamento_atual:
            return

        nome_limpo = self.orcamento_atual.nome_cliente.replace(" ", "_").lower()
        sugestao_nome = f"projecao_12_meses_{nome_limpo}.csv"

        caminho = filedialog.asksaveasfilename(
            title="Guardar Projeção de 12 Meses",
            initialfile=sugestao_nome,
            defaultextension=".csv",
            filetypes=[("Ficheiro CSV (Excel)", "*.csv"), ("Todos os ficheiros", "*.*")],
        )

        if caminho:
            try:
                self.orcamento_atual.salvar_csv(caminho)
                messagebox.showinfo(
                    "Transferência Concluída",
                    f"O ficheiro CSV com a projeção de 12 meses foi guardado com sucesso em:\n{caminho}",
                )
            except Exception as e:
                messagebox.showerror("Erro ao Guardar", f"Não foi possível guardar o ficheiro:\n{e}")


if __name__ == "__main__":
    janela = tk.Tk()
    app = RentSmartApp(janela)
    janela.mainloop()