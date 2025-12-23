from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class BuscaPDF(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        # Campo pasta
        self.add_widget(Label(text="Selecione a pasta dos PDFs:"))
        self.pasta_input = TextInput(hint_text="Digite o caminho da pasta")
        self.add_widget(self.pasta_input)

        # Campo termo
        self.add_widget(Label(text="Digite a palavra ou número:"))
        self.termo_input = TextInput(hint_text="Digite o termo")
        self.add_widget(self.termo_input)

        # Botões
        self.buscar_btn = Button(text="🔍 Buscar")
        self.buscar_btn.bind(on_press=self.iniciar_busca)
        self.add_widget(self.buscar_btn)

        self.exportar_btn = Button(text="⬇️ Exportar CSV")
        self.exportar_btn.bind(on_press=self.exportar_csv)
        self.add_widget(self.exportar_btn)

        # Área resultados
        self.resultados = TextInput(hint_text="Resultados da busca", readonly=True)
        self.add_widget(self.resultados)

    def iniciar_busca(self, instance):
        pasta = self.pasta_input.text
        termo = self.termo_input.text
        # Aqui você chamaria sua função de busca em PDFs
        self.resultados.text = f"Buscando '{termo}' em {pasta}...\n(Resultados simulados)"

    def exportar_csv(self, instance):
        # Aqui você implementaria a exportação
        self.resultados.text += "\nExportando resultados para CSV..."

class BuscaPDFApp(App):
    def build(self):
        return BuscaPDF()

if __name__ == "__main__":
    BuscaPDFApp().run()
