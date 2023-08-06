from pathlib import Path
from boletim import Boletim, ScraperBoletim


def exporta_csv(urlBoletim, path):
    boletim = Boletim(urlBoletim)

    municipiosComCasos = boletim.filtra_municipios_com_casos()
    totalGeral = boletim.totalGeral

    data = boletim.dataPublicacao.format("DD_MM")
    with open(Path(f"{path}/ES_{data}.csv"), "w+", encoding="utf-8") as f:
        f.write(f"municipio|confirmados_{data}|mortes_{data}\n")
        f.write(f"TOTAL NO ESTADO|{totalGeral['casosConfirmados']}|\n")
        f.write(f"Importados/Indefinidos||\n")
        for municipio, casos in municipiosComCasos.items():
            f.write(f"{municipio}|{casos}|\n")


if __name__ == "__main__":
    exporta_csv(
        "https://www.es.gov.br/Noticia/secretaria-da-saude-divulga-33o-boletim-da-covid-19", ".")
    scraper = ScraperBoletim()

    boletim = scraper.pesquisa_boletim_data("30-03-2020")
    print(boletim.pesquisa_casos_municipio("serra"))
