Atualizador Chrome driver

Esse programa é um script bem simples, onde automatiza a atualização continua do driver.
Sua principal função é substituir o driver, trocando pela versão mais recente, conforme chrome.


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

