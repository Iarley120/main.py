import customtkinter as ctk
from tkinter import messagebox, ttk

# Configuração visual da biblioteca gráfica
ctk.set_appearance_mode("System")  # Detecta automaticamente modo escuro ou claro
ctk.set_default_color_theme("blue")  # Tema azul moderno

# Banco de dados simulado (Dicionário de dicionários)
estoque = {}

class AppEstoque(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela Principal (A "Página" do Sistema)
        self.title("Sistema de Controle de Estoque e Logística")
        self.geometry("850x600")
        self.resizable(False, False)

        # --- TÍTULO DO SISTEMA ---
        self.titulo = ctk.CTkLabel(self, text="LOGÍSTICA & ESTOQUE", font=ctk.CTkFont(size=24, weight="bold"))
        self.titulo.pack(pady=15)

        # --- CRIAÇÃO DAS ABAS (PÁGINAS INTERNAS) ---
        self.abas = ctk.CTkTabview(self, width=800, height=500)
        self.abas.pack(padx=20, pady=10, fill="both", expand=True)

        # Adicionando as abas
        self.aba_cadastro = self.abas.add("Cadastrar Produto")
        self.aba_movimentacao = self.abas.add("Movimentar Estoque")
        self.aba_relatorio = self.abas.add("Relatório Geral")

        # Configurando cada aba
        self.configurar_aba_cadastro()
        self.configurar_aba_movimentacao()
        self.configurar_aba_relatorio()

    # ================= PÁGINA DE CADASTRO =================
    def configurar_aba_cadastro(self):
        # Campos de texto (Inputs)
        self.lbl_cod = ctk.CTkLabel(self.aba_cadastro, text="Código do Produto:")
        self.lbl_cod.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.txt_cod = ctk.CTkEntry(self.aba_cadastro, width=200)
        self.txt_cod.grid(row=0, column=1, padx=20, pady=10)

        self.lbl_nome = ctk.CTkLabel(self.aba_cadastro, text="Nome do Produto:")
        self.lbl_nome.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.txt_nome = ctk.CTkEntry(self.aba_cadastro, width=200)
        self.txt_nome.grid(row=1, column=1, padx=20, pady=10)

        self.lbl_cat = ctk.CTkLabel(self.aba_cadastro, text="Categoria:")
        self.lbl_cat.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        self.txt_cat = ctk.CTkEntry(self.aba_cadastro, width=200)
        self.txt_cat.grid(row=2, column=1, padx=20, pady=10)

        self.lbl_qtd = ctk.CTkLabel(self.aba_cadastro, text="Quantidade Inicial:")
        self.lbl_qtd.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        self.txt_qtd = ctk.CTkEntry(self.aba_cadastro, width=200)
        self.txt_qtd.grid(row=3, column=1, padx=20, pady=10)

        self.lbl_min = ctk.CTkLabel(self.aba_cadastro, text="Mínimo de Segurança:")
        self.lbl_min.grid(row=4, column=0, padx=20, pady=10, sticky="w")
        self.txt_min = ctk.CTkEntry(self.aba_cadastro, width=200)
        self.txt_min.grid(row=4, column=1, padx=20, pady=10)

        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(self.aba_cadastro, text="Salvar Produto", command=self.acao_cadastrar)
        self.btn_salvar.grid(row=5, column=0, columnspan=2, pady=20)

    def acao_cadastrar(self):
        codigo = self.txt_cod.get().strip()
        nome = self.txt_nome.get().strip()
        categoria = self.txt_cat.get().strip()

        if not codigo or not nome or not categoria:
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos!")
            return

        if codigo in estoque:
            messagebox.showerror("Erro", "Este código já está cadastrado!")
            return

        try:
            qtd = int(self.txt_qtd.get())
            minimo = int(self.txt_min.get())
            if qtd < 0 or minimo < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade e Mínimo devem ser números inteiros maiores ou iguais a zero!")
            return

        # Salva no banco de dados simulado
        estoque[codigo] = {
            'nome': nome, 'categoria': categoria, 'qtd': qtd, 'minimo': minimo, 'vendas': 0, 'perdas': 0
        }
        
        messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso!")
        
        # Limpa os campos
        self.txt_cod.delete(0, 'end'); self.txt_nome.delete(0, 'end'); self.txt_cat.delete(0, 'end')
        self.txt_qtd.delete(0, 'end'); self.txt_min.delete(0, 'end')
        self.atualizar_tabela_relatorio()

    # ================= PÁGINA DE MOVIMENTAÇÃO =================
    def configurar_aba_movimentacao(self):
        self.lbl_mov_cod = ctk.CTkLabel(self.aba_movimentacao, text="Código do Produto:")
        self.lbl_mov_cod.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        self.txt_mov_cod = ctk.CTkEntry(self.aba_movimentacao, width=200)
        self.txt_mov_cod.grid(row=0, column=1, padx=20, pady=20)

        self.lbl_tipo = ctk.CTkLabel(self.aba_movimentacao, text="Operação:")
        self.lbl_tipo.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        self.combo_opcao = ctk.CTkComboBox(self.aba_movimentacao, values=["Entrada (+)", "Saída / Venda (-)", "Registrar Perda (⚠️)"], width=200)
        self.combo_opcao.grid(row=1, column=1, padx=20, pady=10)

        self.lbl_mov_qtd = ctk.CTkLabel(self.aba_movimentacao, text="Quantidade:")
        self.lbl_mov_qtd.grid(row=2, column=0, padx=20, pady=20, sticky="w")
        self.txt_mov_qtd = ctk.CTkEntry(self.aba_movimentacao, width=200)
        self.txt_mov_qtd.grid(row=2, column=1, padx=20, pady=20)

        self.btn_movimentar = ctk.CTkButton(self.aba_movimentacao, text="Confirmar Movimentação", command=self.acao_movimentar)
        self.btn_movimentar.grid(row=3, column=0, columnspan=2, pady=20)

    def acao_movimentar(self):
        codigo = self.txt_mov_cod.get().strip()
        opcao = self.combo_opcao.get()
        
        if codigo not in estoque:
            messagebox.showerror("Erro", "Produto não encontrado!")
            return

        try:
            qtd_m = int(self.txt_mov_qtd.get())
            if qtd_m <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "A quantidade deve ser um número inteiro maior que zero.")
            return

        if "Entrada" in opcao:
            estoque[codigo]['qtd'] += qtd_m
            messagebox.showinfo("Sucesso", f"Entrada realizada! Novo estoque: {estoque[codigo]['qtd']}")
            
        elif "Saída" in opcao:
            if estoque[codigo]['qtd'] >= qtd_m:
                estoque[codigo]['qtd'] -= qtd_m
                estoque[codigo]['vendas'] += qtd_m
                messagebox.showinfo("Sucesso", f"Venda realizada! Novo estoque: {estoque[codigo]['qtd']}")
                
                if estoque[codigo]['qtd'] <= estoque[codigo]['minimo']:
                    messagebox.showwarning("⚠️ Alerta de Estoque Mínimo", f"O produto '{estoque[codigo]['nome']}' atingiu o nível crítico de segurança ({estoque[codigo]['minimo']} un.)!")
            else:
                messagebox.showerror("Erro", "Saldo insuficiente em estoque.")
                
        elif "Perda" in opcao:
            if estoque[codigo]['qtd'] >= qtd_m:
                estoque[codigo]['qtd'] -= qtd_m
                estoque[codigo]['perdas'] += qtd_m
                messagebox.showinfo("Sucesso", f"Perda registrada! {qtd_m} unidades removidas.")
            else:
                messagebox.showerror("Erro", "Quantidade de perda maior que o estoque disponível.")

        self.txt_mov_cod.delete(0, 'end')
        self.txt_mov_qtd.delete(0, 'end')
        self.atualizar_tabela_relatorio()

    # ================= PÁGINA DE RELATÓRIO =================
    def configurar_aba_relatorio(self):
        # Criando uma tabela real (Treeview do tkinter tradicional adaptada)
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Treeview", background="#2a2d2e", foreground="white", fieldbackground="#2a2d2e", rowheight=25)
        estilo.map("Treeview", background=[('selected', '#1f538d')])

        colunas = ("codigo", "nome", "categoria", "qtd", "minimo", "status")
        self.tabela = ttk.Treeview(self.aba_relatorio, columns=colunas, show="headings", height=14)
        
        # Cabeçalhos
        self.tabela.heading("codigo", text="Código")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("categoria", text="Categoria")
        self.tabela.heading("qtd", text="Qtd Atual")
        self.tabela.heading("minimo", text="Mín. Segurança")
        self.tabela.heading("status", text="Status")

        # Largura das colunas
        self.tabela.column("codigo", width=80, anchor="center")
        self.tabela.column("nome", width=180)
        self.tabela.column("categoria", width=120)
        self.tabela.column("qtd", width=80, anchor="center")
        self.tabela.column("minimo", width=100, anchor="center")
        self.tabela.column("status", width=150, anchor="center")

        self.tabela.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Botão para atualizar a página de relatórios
        self.btn_atualizar = ctk.CTkButton(self.aba_relatorio, text="Atualizar Tabela", command=self.atualizar_tabela_relatorio)
        self.btn_atualizar.pack(pady=5)

    def atualizar_tabela_relatorio(self):
        # Limpa as linhas antigas da tabela gráfica
        for linha in self.tabela.get_children():
            self.tabela.delete(linha)

        # Insere as novas linhas atualizadas
        for cod, dados in estoque.items():
            status = "⚠️ REPOR ESTOQUE" if dados['qtd'] <= dados['minimo'] else "✅ OK"
            self.tabela.insert("", "end", values=(
                cod, dados['nome'], dados['categoria'], dados['qtd'], dados['minimo'], status
            ))

# Executa a janela do aplicativo
if __name__ == "__main__":
    app = AppEstoque()
    app.mainloop()