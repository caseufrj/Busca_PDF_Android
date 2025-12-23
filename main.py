import os
import csv
import unicodedata
import re
from pdfminer.high_level import extract_text
from pdf2image import convert_from_path
import easyocr

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

# 🔧 Funções auxiliares
def normalizar(texto):
    return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII").lower()

def limpar_ocr(texto):
    return re.sub(r'[^a-zA-Z0-9]', '', texto).lower()

def destacar_termo(texto, termo):
    return re.sub(f"({re.escape(termo)})", r">>>\1<<<", texto, flags=re.IGNORECASE)

# 🔍 Função principal de busca
def buscar_em_pdfs(pasta, termo):
    resultados = []
    termo_normalizado = limpar_ocr(normalizar(termo))

    # Inicializa OCR uma vez
    reader = easyocr.Reader(['pt', 'en'])

    for arquivo in os.listdir(pasta):
        if arquivo.lower().endswith(".pdf"):
            caminho = os.path.join(pasta, arquivo)
            try:
                # Primeiro tenta extrair texto embutido
                texto_pdfminer = extract_text(caminho)
                if texto_pdfminer:
                    texto_normalizado = limpar_ocr(normalizar(texto_pdfminer))
                    if termo_normalizado in texto_normalizado:
                        trecho = destacar_termo(texto_pdfminer[:500], termo)
                        resultados.append((arquivo, "?", trecho, "Texto embutido"))
                    continue

                # Se não houver texto, usa OCR com EasyOCR
                imagens = convert_from_path(caminho, dpi=200)
                texto_total = ""
                for img in imagens:
                    resultado = reader.readtext(img)
                    for _, texto, _ in resultado:
                        texto_total += texto + " "

                texto_normalizado = limpar_ocr(normalizar(texto_total))
                if termo_normalizado in texto_normalizado:
                    trecho = destacar_termo(texto_total[:500], termo)
                    resultados.append((arquivo, "?", trecho, "OCR"))

            except Exception as e:
                resultados.append((arquivo, "?", f"Erro: {e}", "Erro"))
    return resultados

# 🎨 Interface Kivy
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

        # Botão Buscar
        self.buscar_btn = Button(text="🔍 Buscar")
        self.buscar_btn.bind(on_press=self.iniciar_busca)
        self.add_widget(self.buscar_btn)

        # Botão Exportar
        self.exportar_btn = Button(text="⬇️ Exportar CSV")
        self.exportar_btn.bind(on_press=self.exportar_csv)
        self.add_widget(self.exportar_btn)

        # Área de resultados
        self.resultados = TextInput(hint_text="Resultados da busca", readonly=True)
        self.add_widget(self.resultados)

        # Guardar resultados
        self.resultados_lista = []

    def iniciar_busca(self, instance):
        pasta = self.pasta_input.text.strip()
        termo = self.termo_input.text.strip()
        if not pasta or not termo:
            self.resultados.text = "⚠️ Informe pasta e termo!"
            return
        self.resultados_lista = buscar_em_pdfs(pasta, termo)
        if self.resultados_lista:
            texto = f"🔍 Resultado para '{termo}':\n\n"
            for arquivo, pagina, trecho, origem in self.resultados_lista:
                texto += f"📄 {arquivo} | Origem: {origem}\nTrecho: {trecho}\n\n"
            self.resultados.text = texto
        else:
            self.resultados.text = "Nenhum resultado encontrado."

    def exportar_csv(self, instance):
        if not self.resultados_lista:
            self.resultados.text += "\n⚠️ Nenhum resultado para exportar!"
            return
        filename = "resultados_busca.csv"
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Arquivo", "Página", "Trecho", "Origem"])
            for arquivo, pagina, trecho, origem in self.resultados_lista:
                writer.writerow([arquivo, pagina, trecho, origem])
        self.resultados.text += f"\n✅ Resultados exportados para '{filename}'"

class BuscaPDFApp(App):
    def build(self):
        return BuscaPDF()

if __name__ == "__main__":
    BuscaPDFApp().run()
