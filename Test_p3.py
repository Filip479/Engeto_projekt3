"""
webscraping: třetí projekt do Engeto Online Python Akademie
author: Filip
email: 479@seznam.cz
discord: Filip479#8140
"""
import requests
from bs4 import BeautifulSoup as bs
from urllib import parse
import csv
import sys

url = sys.argv[1]
kraj = parse.parse_qs(parse.urlparse(url).query)['xkraj'][0]
nuts = parse.parse_qs(parse.urlparse(url).query)['xnumnuts'][0]

vystupni_soubor = sys.argv[2]
odpoved_serveru = requests.get(url)
soup = bs(odpoved_serveru.text, "html.parser")

table_table = soup.find("table", {"class": "table"})
tr_radky = table_table.find_all("tr")

kody_obci = []
nazvy_obci = []

for tr in tr_radky[2:]:
    td_na_radku = tr.find_all("td")
    kody_obci.append(td_na_radku[0].get_text()) # kód okrsku (1. sloupec ve výsledném .csv)
    nazvy_obci.append(td_na_radku[1].get_text()) # název okrsku (2. sloupec ve výsledném .csv)

def naformatuj_kody(kod: int) -> str:
    """
    Získá odkazy jednotlivých obcí, ze kterých se scrapují data.
    """
    url_obce = f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={kraj}&xpm={kod}&xvyber={nuts}"
    return url_obce

registrovani = []
obalky = []
platne_hlasy = []
pocet_hlasu = []

tr_na_radku = table_table.find_all("tr")

def okrsky(url_okrsky: str, csvwriter, kod_obce, nazev_obce) -> str:
    """
    Vytvoří formu výsledného csv souboru, hlavičku a následující data:
    počet registrovaných voličů, počet vydaných obálek, počet platných hlasů a
    počet hlasů, které získaly jednotlivé kandidující politické subjekty.
    """
    odpoved_serveru_okrsky = requests.get(url_okrsky)
    soup_okrsky = bs(odpoved_serveru_okrsky.text, "html.parser")
    table_okrsky = soup_okrsky.find_all("table")[0]
    info_o_okrsku = table_okrsky.find_all("tr")[2].find_all("td")

    registrovani.append(info_o_okrsku[3].get_text()) # registrovani (3. sloupec ve výsledném .csv)
    obalky.append(info_o_okrsku[4].get_text()) # vydané obálky (4. sloupec ve výsledném .csv)
    platne_hlasy.append(info_o_okrsku[7].get_text()) # platné hlasy (5. sloupec ve výsledném .csv)

    tabulka_vsech_stran = soup_okrsky.find_all("table")[1]
    radky_se_stranami = tabulka_vsech_stran.find_all("tr")[2:]

    if not okrsky.called:
        hlavicka = ['kód', 'obec', 'registrovaní voliči', 'vydané obálky', 'platné hlasy']
        for radek_strany in radky_se_stranami:
            hlavicka.append(radek_strany.find_all("td")[1].get_text())
        csvwriter.writerow(hlavicka)
        okrsky.called = True

    radek = [kod_obce, nazev_obce]
    radek.append(info_o_okrsku[3].get_text())
    radek.append(info_o_okrsku[4].get_text())
    radek.append(info_o_okrsku[7].get_text())

    for radek_strany in radky_se_stranami:
        bunky_strany = radek_strany.find_all("td")
        radek.append(bunky_strany[2].get_text()) # počet hlasů (6. a další sloupec ve výsledném .csv)
    csvwriter.writerow(radek)

def projdi_kody():
    """
    Vytvoří výsledný csv soubor s názvem v proměnné "vystupni_soubor"
    a uloží do něho data v požadované struktuře.
    Tento soubor lze následné otevřít a pracovat s ním v tabulkovém editoru.
    """

    with open(vystupni_soubor, "w", newline="\n", encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)
        okrsky.called = False
        for idx, kod in enumerate(kody_obci):
            okrsky(naformatuj_kody(kod), csvwriter, kod, nazvy_obci[idx])
    csvfile.closed

if __name__ == "__main__":
    projdi_kody()
    