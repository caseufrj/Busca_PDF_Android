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

# Dependências Python
requirements = python3,kivy,pillow,pdfminer.six,pdf2image,easyocr

# Incluir arquivos extras (ícones, etc.)
source.include_exts = py,png,jpg,ico,kv

# Pasta onde o APK será gerado
dist.dir = bin

[buildozer]
# Plataforma alvo
log_level = 2
warn_on_root = 1
