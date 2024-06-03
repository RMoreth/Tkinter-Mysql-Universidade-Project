import customtkinter as ctk  # type:ignore
import TKinterModernThemes as tkm


class Janela(tkm.ThemedTKinterFrame):

    def __init__(self, **kw):
        super().__init__("TITLE", "park", "dark", **kw)
        self.geometry("600x400")
        self.title("Janela")
        self.bind("<Configure>", self.redimensionar_texto)

        self.font_texto = ctk.CTkFont(family="Helvetica", size=12)
        self.font_title = ctk.CTkFont(family="Helvetica", size=15)

        self.carregar_interface()

    def redimensionar_texto(self, event):

        width = event.width
        new_font_text = max(int(width / 11), 12)
        new_font_title = max(int(width / 9), 15)
        print(
            f"texto=  {new_font_text}, title= {new_font_title}, width= {width}")

        self.font_texto.configure(size=new_font_text)
        self.font_title.configure(size=new_font_title)

        for label in Label.all_label:
            label.configure(font=self.font_texto)

    def carregar_interface(self):
        self.frame_atual = Frame(self).criar_frame(self)
        self.frame_atual.pack(fill='both', expand=True)

        # Criando frames

        self.frame_top = self.frame_atual.criar_frame(self)
        self.frame_top.configure(fg_color="blue")
        self.frame_top.place(relx=0, rely=0, relwidth=1, relheight=0.2)

        self.frame_body = self.frame_atual.criar_frame(self)
        self.frame_body.configure(fg_color="red")
        self.frame_body.place(relx=0, rely=0.2, relwidth=1, relheight=0.6)

        self.frame_bot = self.frame_atual.criar_frame(self)
        self.frame_bot.configure(fg_color="black")
        self.frame_bot.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)

        # Criando labels
        self.label_top = Label(self.frame_top, "Title", font=self.font_title)
        self.label_top.pack()

        self._label_text = Label(
            self.frame_top, "Text", font=self.font_texto)
        self._label_text.pack()


class Frame(ctk.CTkFrame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

    def criar_frame(self, master):
        self.frame_criado = Frame(master)
        return self.frame_criado


class Label(ctk.CTkLabel):
    all_label = []

    def __init__(self, master, texto, **kw):
        super().__init__(master, **kw)

        self.configure(text=texto)

        self.all_label.append(self)

    def criar_label(self, master, texto):

        self.label = Label(master, texto)
        self.label.configure(text=texto)
        return self.label


if __name__ == "__main__":
    root = Janela()

    root.mainloop()
