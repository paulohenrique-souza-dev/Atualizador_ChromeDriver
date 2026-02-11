"# Atualizador_ChromeDriver" 

Oii,tudo bem??
esse programa é um script bem simples da automação do Chrome Driver
Sua principal função é substituir de forma automática,sem complicações.

Crie a venv e instale as bibliotecas com pip install -r requirements.txt
instale o pyinstaller

código para transformar em exe :
pyinstaller ^
  --onefile ^
  --noconsole ^
  --icon=icone.ico ^
  --hidden-import=bs4 ^
  --hidden-import=requests ^
  seu_aquivopython.py

  após isso já vai ter o exe.

  Qualquer dúvida estou a dispor.
  Até mais !!
