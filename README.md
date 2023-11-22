
Název projektu: "WebScraping"

Pro správný chod skriptu je potřeba provést následující:
- ve vybrané složce, v příkazovém řádku vytvoř virtuální prostředí pomocí příkazu:
	- "python -m venv virtualvenv" ("virtualvenv" je název prostředí, název si zvolí uživatel)
	- ve složce s virtuální prostředím se spustí vývojové prostředí pomocí příkazu v příkazovém řádku "code ."
	- virtuální prostředí s názvem "myvenv" je potřeba aktivovat v terminálu pomocí příkazu "myvenv\Scripts\activate"
- pomocí příkazového řádku je třeba instalovat knihovny třetích stran:
	- requests (pomocí příkazu: "pip install requests")
	- beautifulsoup (pomocí příkazu "pip install beautifulsoup4")

Ve vývojovém postředí je třeba importovat knihovny příkazem import takto:
	- import requests
	- from bs4 import BeautifulSoup as bs (bs je zkratka knihovny, kterou daný skript používá)
	- import csv

Skript provádí scraping dat výsledků voleb z roku 2017 do formátu .csv.
Skript scrapuje data ze stránky: https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

Spouští se pomocí dvou argumentů: url adresa a název výstupního souboru:
- do proměnné "url" vloží uživatel url adresu územního celku (ohraničenou uvozovkami), ze kterého chce scrapovat data
- do proměnné "vystupni_soubor" vloží uživatel název, který bude mít výsledný .csv soubor

Tento .csv soubor lze následně otevřít v tabulkovém editoru a dále provádět analýzu dat.

V přiloženém souboru Requierements.txt jsou uvedeny použité knihovny a jejich verze.