# System Filtracji Cyfrowej
## Zależności - requirements
* certifi==2021.10.8
* charset-normalizer==2.0.9
* docutils==0.18.1
* idna==3.3
* Kivy==2.0.0
* kivy-deps.angle==0.3.0
* kivy-deps.glew==0.3.0
* kivy-deps.sdl2==0.3.1
* Kivy-Garden==0.1.4
* kivy-garden.contextmenu==0.1.0.dev1
* kivy-garden.graph==0.4.0
* numpy==1.21.4
* Pygments==2.10.0
* pypiwin32==223
* pywin32==302
* requests==2.26.0
* scipy==1.7.3
* urllib3==1.26.7

## Uruchomienie - installation/run
Należy zainstalować moduł `venv` dla języka Python w systemie.
A następnie wykorzystać go używając komendy `python -m venv .`,
gdzie "." to aktualny katalog repozytorium w którym się znajdujemy.
Uruchomić wirtualne środowisko za pomocą: `source ./Scripts/activate`,
a w nim zainstalować zależności używając: `pip install -r requirements.txt`.
Można upewnić się czy program "pip" na pewno odnosi się do stworzonego środowiska przez użycie
`which pip` - na pewno działa w systemie linux, lub w konsoli "git bash".
Będąc dalej w wirtualnym środowisku uruchomić plik main_window.py `python main_windows.py`

