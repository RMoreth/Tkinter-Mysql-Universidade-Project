import tkinter as tk

class Aplicativo(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Gerenciamento de Alunos e Professores")
        
        self.frame_atual = None
        
        self.menu = tk.Menu(self)
        self.menu.add_command(label="Alunos", command=self.exibir_alunos)
        self.menu.add_command(label="Professores", command=self.exibir_professores)
        self.config(menu=self.menu)
        
    def exibir_alunos(self):
        if self.frame_atual is not None:
            self.frame_atual.destroy()
        
        self.frame_atual = tk.Frame(self)
        self.frame_atual.pack(fill="both", expand=True)
        
        # Lógica para exibir informações de alunos aqui
        
        label = tk.Label(self.frame_atual, text="Informações de Alunos")
        label.pack()
        
    def exibir_professores(self):
        if self.frame_atual is not None:
            self.frame_atual.destroy()
        
        self.frame_atual = tk.Frame(self)
        self.frame_atual.pack(fill="both", expand=True)
        
        # Lógica para exibir informações de professores aqui
        
        label = tk.Label(self.frame_atual, text="Informações de Professores")
        label.pack()

if __name__ == "__main__":
    app = Aplicativo()
    app.mainloop()
