[app]
# Nome do aplicativo
title = Buscador de PDFs
# Nome interno (sem espaços)
package.name = buscadorpdf
# Nome do domínio reverso (único)
package.domain = org.caseufrj
# Versão
version = 0.1
# Arquivo principal
source.dir = .
source.main = main.py
# Ícone do app (PNG)
icon.filename = icone_app.png

# Orientação da tela
orientation = portrait

# Permissões necessárias
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# Módulos Python usados
requirements = python3,kivy,pillow,pdfminer.six,pytesseract

# Incluir arquivos extras (ícones, etc.)
source.include_exts = py,png,jpg,ico,kv

# Pasta onde o APK será gerado
dist.dir = bin

# Ativar suporte a OCR (Tesseract precisa ser incluído manualmente ou via lib)
# Dependendo da complexidade, pode ser necessário compilar bibliotecas nativas.

[buildozer]
# Plataforma alvo
log_level = 2
warn_on_root = 1
