import customtkinter as ctk
from PIL import Image
import sqlite3
from tkinter import messagebox
import bcrypt

# Configuração do Tema
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("themes/coffee.json")

# Definição das Fontes
FONTE_TITULO = ("Segoe Script", 24, "bold")
FONTE_PADRAO = ("Comic Sans MS", 16)
FONTE_MENSAGEM = ("Dubai Light", 12, "italic")

# Função para criptografar senha
def hash_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

# Função para verificar senha
def verificar_senha(senha_digitada, senha_armazenada):
    return bcrypt.checkpw(senha_digitada.encode(), senha_armazenada.encode())

# Criar banco de dados e tabela
def criar_tabela():
    with sqlite3.connect("usuarios.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conexao.commit()

# Verificar usuário no banco de dados
def verificar_usuario(usuario, senha):
    with sqlite3.connect("usuarios.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", (usuario,))
        resultado = cursor.fetchone()
    
    if resultado and verificar_senha(senha, resultado[0]):
        return True
    return False

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da Janela
        self.geometry("700x400")
        self.title("Sistema de Login")
        self.iconbitmap("assets/img/icon.ico")
        self.resizable(False, False)

        # Criar Widgets da Interface
        self.create_widgets()

    def atualizar_cores(self):
        """Atualiza as cores das mensagens com base no tema atual"""
        modo = ctk.get_appearance_mode()  
        cor_texto = "#ab7000" if modo == "Light" else "#e1b700"
        self.label_usuario_obrig.configure(text_color=cor_texto)
        self.label_senha_obrig.configure(text_color=cor_texto)

    def create_widgets(self):
        """Cria e posiciona os elementos visuais"""

        # Imagem do Logo
        img_pil = Image.open("assets/img/logo.png")
        img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(300, 350))
        label_img = ctk.CTkLabel(self, image=img, text="")
        label_img.place(x=5, y=65)
        # Título
        ctk.CTkLabel(self, text="Cat Sys App", font=FONTE_TITULO).place(x=115, y=45)
        # Área de Login
        frame = ctk.CTkFrame(self, width=350, height=396)
        frame.pack(side="right", padx=10, pady=10)

        ctk.CTkLabel(frame, text="Login", font=FONTE_TITULO).place(relx=0.5, y=50, anchor="center")

        self.usuario = ctk.CTkEntry(frame, placeholder_text="Nome de usuário", width=300, font=FONTE_PADRAO, corner_radius=10)
        self.usuario.place(x=25, y=105)

        self.label_usuario_obrig = ctk.CTkLabel(frame, text="", font=FONTE_MENSAGEM)
        self.label_usuario_obrig.place(x=25, y=135)

        self.senha = ctk.CTkEntry(frame, placeholder_text="Senha", width=300, font=FONTE_PADRAO, show="*", corner_radius=10)
        self.senha.place(x=25, y=175)

        self.label_senha_obrig = ctk.CTkLabel(frame, text="", font=FONTE_MENSAGEM)
        self.label_senha_obrig.place(x=25, y=205)

        # Botão para Exibir/Ocultar Senha
        self.ver_senha_var = ctk.IntVar(value=0)
        self.ver_senha = ctk.CTkCheckBox(frame, text="Mostrar senha", font=FONTE_PADRAO, variable=self.ver_senha_var, command=self.toggle_senha)
        self.ver_senha.place(x=25, y=235)

        # Botão de Entrar
        self.botao_entrar = ctk.CTkButton(frame, text="Entrar", font=FONTE_PADRAO, width=300, command=self.login)
        self.botao_entrar.place(x=25, y=285)

        # Botão para Cadastrar Usuário
        self.botao_cadastrar = ctk.CTkButton(frame, text="Cadastrar", font=FONTE_PADRAO, width=300, command=self.cadastrar_usuario)
        self.botao_cadastrar.place(x=25, y=325)

        # Atualizar Cores
        self.atualizar_cores()

    def toggle_senha(self):
        """Alterna entre mostrar/ocultar senha com base no estado do checkbox"""
        if self.ver_senha.get():
            self.senha.configure(show="")
        else:
            self.senha.configure(show="*")


    def login(self):
        """Lógica de autenticação"""
        usuario = self.usuario.get()
        senha = self.senha.get()

        # Verifica se os campos estão vazios
        if not usuario:
            self.label_usuario_obrig.configure(text="Campo obrigatório!")

        if not senha:
            self.label_senha_obrig.configure(text="Campo obrigatório!")

        if not usuario or not senha:
            return  # Para a execução se os campos estiverem vazios

        # Se os campos foram preenchidos, tenta autenticar
        if verificar_usuario(usuario, senha):
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos")

    def cadastrar_usuario(self):
        """Abre a janela de cadastro e a coloca na frente"""
        self.janela_cadastro = ctk.CTkToplevel(self)
        self.janela_cadastro.geometry("400x300")
        self.janela_cadastro.title("Cadastro de Usuário")
        self.janela_cadastro.resizable(False, False)
        self.janela_cadastro.attributes('-topmost', True)  # Coloca a janela na frente

        ctk.CTkLabel(self.janela_cadastro, text="Cadastro de Usuário", font=FONTE_TITULO).pack(pady=10)

        self.novo_usuario = ctk.CTkEntry(self.janela_cadastro, placeholder_text="Nome de usuário", width=250, font=FONTE_PADRAO)
        self.novo_usuario.pack(pady=5)

        self.nova_senha = ctk.CTkEntry(self.janela_cadastro, placeholder_text="Senha", width=250, font=FONTE_PADRAO, show="*")
        self.nova_senha.pack(pady=5)

        self.botao_salvar = ctk.CTkButton(self.janela_cadastro, text="Salvar", font=FONTE_PADRAO, width=250, command=self.salvar_usuario)
        self.botao_salvar.pack(pady=10)

    def salvar_usuario(self):
        """Salva um novo usuário no banco de dados e preenche os campos de login automaticamente"""
        usuario = self.novo_usuario.get()
        senha = self.nova_senha.get()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return

        senha_hash = hash_senha(senha)  # Criptografa a senha

        try:
            conexao = sqlite3.connect("usuarios.db")
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha_hash))
            conexao.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

            # Limpar os campos antes de preencher automaticamente
            self.usuario.delete(0, "end")
            self.senha.delete(0, "end")

            # Preencher os campos da tela de login com os novos dados
            self.usuario.insert(0, usuario)
            self.senha.insert(0, senha)

            self.janela_cadastro.destroy()  # Fecha a janela de cadastro

        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Usuário já existe!")

        except sqlite3.DatabaseError as e:
            messagebox.showerror("Erro no banco de dados", f"Ocorreu um erro no banco de dados: {e}")

        except Exception as e:
            messagebox.showerror("Erro inesperado", f"Ocorreu um erro inesperado: {e}")

        finally:
            if 'conexao' in locals():
                conexao.close()

criar_tabela()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
