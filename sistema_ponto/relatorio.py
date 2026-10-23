import os
from datetime import datetime
from .config import ARQUIVO_RELATORIO


class RelatorioPonto:
    def __init__(self, arquivo_relatorio=ARQUIVO_RELATORIO):
        self.arquivo_relatorio = str(arquivo_relatorio)

    def salvar(self, nome, confianca, status="Ponto registrado"):
        os.makedirs(os.path.dirname(self.arquivo_relatorio), exist_ok=True)
        arquivo_existe = os.path.exists(self.arquivo_relatorio)
        agora = datetime.now()

        dias_semana = {
            "Monday": "Segunda-feira",
            "Tuesday": "Terça-feira",
            "Wednesday": "Quarta-feira",
            "Thursday": "Quinta-feira",
            "Friday": "Sexta-feira",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        }

        dia_semana = dias_semana.get(agora.strftime("%A"), agora.strftime("%A"))
        data = agora.strftime("%d/%m/%Y")
        hora = agora.strftime("%H:%M:%S")
        data_hora_completa = agora.strftime("%d/%m/%Y %H:%M:%S")

        with open(self.arquivo_relatorio, "a", encoding="utf-8") as arquivo:
            if not arquivo_existe:
                arquivo.write("Nome,Dia da Semana,Data,Hora,Data e Hora Completa,Confianca,Status\n")

            arquivo.write(
                f"{nome},{dia_semana},{data},{hora},{data_hora_completa},{confianca:.2f},{status}\n"
            )
