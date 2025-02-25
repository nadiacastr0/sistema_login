import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

# Configuração inicial do tema
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("themes/coffee.json")

# Definição das Fontes
FONTE_TITULO = ("Segoe Script", 24, "bold")
FONTE_PADRAO = ("Comic Sans MS", 16)
FONTE_MENSAGEM = ("Dubai Light", 12, "italic")


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da Janela
        self.geometry("700x400")
        self.title("Sistema de Login")
        self.iconbitmap("assets/img/icon.ico")
        self.resizable(False, False)

        # Criar os widgets da interface
        self.create_widgets()

    def create_widgets(self):
        """Cria e posiciona os widgets na tela"""

        # Imagem do Logo
        img_pil = Image.open("assets/img/logo.png")
        img = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(300, 350))
        label_img = ctk.CTkLabel(self, image=img, text="")
        label_img.place(x=5, y=65)

        # Título
        ctk.CTkLabel(self, text="Cat Sys App", font=FONTE_TITULO).place(x=115, y=45)

        # Frame da direita (Área de Login)
        frame = ctk.CTkFrame(self, width=350, height=396)
        frame.pack(side="right", padx=10, pady=10)

        ctk.CTkLabel(frame, text="Login", font=FONTE_TITULO).place(relx=0.5, y=50, anchor="center")

        # Campos de entrada
        self.usuario = ctk.CTkEntry(frame, placeholder_text="Nome de usuário", width=300, font=FONTE_PADRAO, corner_radius=10)
        self.usuario.place(x=25, y=105)

        # Mensagem de erro do usuário
        self.label_usuario_obrig = ctk.CTkLabel(frame, text="O campo nome de usuário é obrigatório.", font=FONTE_MENSAGEM)
        self.label_usuario_obrig.place(x=25, y=135)

        self.senha = ctk.CTkEntry(frame, placeholder_text="Senha", width=300, font=FONTE_PADRAO, show="*", corner_radius=10)
        self.senha.place(x=25, y=175)

        # Mensagem de erro da senha
        self.label_senha_obrig = ctk.CTkLabel(frame, text="O campo senha é obrigatório.", font=FONTE_MENSAGEM)
        self.label_senha_obrig.place(x=25, y=205)

        # CheckBox
        self.lembrar = ctk.CTkCheckBox(frame, text="Mostrar senha", font=FONTE_PADRAO)
        self.lembrar.place(x=25, y=235)

        # Botão de Entrar
        self.botao_entrar = ctk.CTkButton(frame, text="Entrar", font=FONTE_PADRAO, width=300, command=self.login)
        self.botao_entrar.place(x=25, y=285)

        # Botão para cadastrar um novo usuário
        self.botao_cadastrar = ctk.CTkButton(frame, text="Cadastrar", font=FONTE_PADRAO, width=300, command=None)
        self.botao_cadastrar.place(x=25, y=325)


    def login(self):
        """Lógica de autenticação do usuário"""
        usuario = self.usuario.get()
        senha = self.senha.get()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")
            return


# Iniciar o aplicativo
if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()