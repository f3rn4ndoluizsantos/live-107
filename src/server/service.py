import re

parameters = [
    {
        "uf": "AM",
        "receitas": {
            "1330": "001 - DIFAL - Indireto",
            "1354": "001 - DIFAL - Indireto",
            "1316": "003 - ICMS antecipado - Indireto",
            "1342": "003 - ICMS antecipado - Indireto",
            "1333": "004 - ICMS Normal - Indireto",
            "1313": "005 - ICMS/ST - Guia - Indireto",
            "1380": "005 - ICMS/ST - Guia - Indireto",
            "3587": "008 - Taxas de Expediente - Indireto",
            "3863": "018 - Fundo Social - ICMS ST - Indireto",
            "1328": "167 - ST de equipamentos agricolas.",
            "3961": "168 - FPS - CESTA BASICA / AUXILIO ESTADUAL",
            "5514": "169 - MULTAS - AUTO DE INFRAÇÃO",
        },
        "padrao_barcode": re.compile(
            r"(?<=\s)([\d|\s|\-]{13,14}\s[\d|\s|\-]{13,14}\s[\d|\s|\-]{13,14}\s[\d|\s|\-]{13,14})\s"
        ),
        "padrao_date": re.compile(r"(?<=\s)([\d]{2}/[\d]{2}/[\d]{4})\s"),
        "padrao_periodo": re.compile(r"(?<=\s)([0-9]{2}/[0-9]{4})\-[0-9]{1}\s"),
        "padrao_ie": re.compile(
            r"(?<=\s)([0-9]{2}\.[0-9]{3,}\.?[0-9]{3,}-[0-9]{1,2}?)\s"
        ),
        "padrao_receita": re.compile(r"(?<=\s)([0-9]{4})\s"),
        "padrao_valores": re.compile(r"\b(?:\d{1,3}\.)*\d{1,3}(?:,\d+)\b"),
        "padrao_controle": re.compile(r"(?<=Controle\s\:\s)([0-9]{13})\s"),
        "position_vencto": 0,
        "position_periodo": 0,
        "position_barcode": 0,
        "position_ie": 0,
        "position_controle": 0,
    }
]


def search_sefaz_uf(uf):
    for sefaz in parameters:
        if sefaz["uf"] == uf:
            return sefaz


def string_to_float(value):
    return float(value.replace(".", "").replace(",", "."))
