from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired
import PyPDF2
import re
from src.server.service import search_sefaz_uf, string_to_float
import pymupdf


class UploadForm(FlaskForm):
    pdf_files = MultipleFileField("Arquivos PDF", validators=[DataRequired()])
    submit = SubmitField("Enviar")


def extract_info_content_pdf(text: str, padroes: dict) -> dict:
    valores = (
        re.findall(padroes["padrao_valores"], text)
        if "padrao_valores" in padroes
        else []
    )
    # print(valores)
    barcodes = (
        re.findall(padroes["padrao_barcode"], text)
        if "padrao_barcode" in padroes
        else []
    )
    # print(barcodes)
    vencimentos = (
        re.findall(padroes["padrao_date"], text) if "padrao_date" in padroes else []
    )
    # print(vencimentos)
    periodos = (
        re.findall(padroes["padrao_periodo"], text)
        if "padrao_periodo" in padroes
        else []
    )
    # print(periodos)
    inscricoes = (
        re.findall(padroes["padrao_ie"], text) if "padrao_ie" in padroes else []
    )
    # print(inscricoes)
    cnpj = re.findall(padroes["padrao_cnpj"], text) if "padrao_cnpj" in padroes else []

    receita = ""
    for key, value in padroes["receitas"].items():
        search_receita = re.findall(rf"\s*{key}\s*", text)
        if len(search_receita) > 0:
            receita = value
            break
    # print(receita)
    return {
        "valores": valores,
        "barcodes": barcodes,
        "vencimentos": vencimentos,
        "periodos": periodos,
        "inscricoes": inscricoes,
        "cnpj": cnpj,
        "receita": receita,
    }


def load_router_pdf_reader(app: Flask) -> Flask:
    @app.route("/reader_pdf", methods=["GET", "POST"])
    def pdf_reader():
        form = UploadForm()
        uf = "AM"
        padroes_uf = search_sefaz_uf(uf)
        # print(padroes_uf)
        valor_original = "0,00"
        valor_multa = "0,00"
        valor_juros = "0,00"
        valor_taxa = "0,00"
        valor_total = "0,00"

        texts = []
        if form.validate_on_submit():
            for file in form.pdf_files.data:
                text = ""
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
                text = text.replace("\n", " ")
                info_pdf = extract_info_content_pdf(text, padroes_uf)

                # print(info_pdf)

                if uf == "AM" and len(info_pdf["valores"]) == 10:
                    valor_original = info_pdf["valores"][0]
                    valor_multa = info_pdf["valores"][1]
                    valor_juros = info_pdf["valores"][2]
                    valor_taxa = info_pdf["valores"][3]
                    valor_total = info_pdf["valores"][4]
                elif (
                    uf == "AM"
                    and len(info_pdf["valores"]) == 6
                    and "2,50" in info_pdf["valores"]
                ):
                    valor_original = info_pdf["valores"][0]
                    valor_multa = "0,00"
                    valor_juros = "0,00"
                    valor_taxa = info_pdf["valores"][1]
                    valor_total = info_pdf["valores"][2]
                elif (
                    uf == "AM"
                    and len(info_pdf["valores"]) == 4
                    and "50,00" in info_pdf["valores"]
                ):
                    valor_original = info_pdf["valores"][0]
                    valor_multa = "0,00"
                    valor_juros = "0,00"
                    valor_taxa = "0,00"
                    valor_total = info_pdf["valores"][1]

                texts.append(
                    {
                        "filename": file.filename,
                        "content": text,
                        "valor_orignal": string_to_float(valor_original),
                        "valor_multa": string_to_float(valor_multa),
                        "valor_juros": string_to_float(valor_juros),
                        "valor_taxa": string_to_float(valor_taxa),
                        "valor_total": string_to_float(valor_total),
                        "barcodes": (
                            re.sub(r"\D", "", info_pdf["barcodes"][0])
                            if len(info_pdf["barcodes"]) > 0
                            else ""
                        ),
                        "vencimentos": (
                            info_pdf["vencimentos"][0]
                            if len(info_pdf["vencimentos"]) > 0
                            else ""
                        ),
                        "periodos": (
                            info_pdf["periodos"][0]
                            if len(info_pdf["periodos"]) > 0
                            else ""
                        ),
                        "inscricoes": (
                            re.sub(r"\D", "", info_pdf["inscricoes"][0])
                            if len(info_pdf["inscricoes"]) > 0
                            else ""
                        ),
                        "cnpj": (
                            info_pdf["cnpj"][0] if len(info_pdf["cnpj"]) > 0 else ""
                        ),
                        "receita": info_pdf["receita"] if info_pdf["receita"] else "",
                    }
                )
                print(texts)
            return render_template("resultado.html", texts=texts)
        return render_template("read_pdf.html", form=form)
