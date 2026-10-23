import cv2
import os
import time
from .detector import DetectorRosto
from .relatorio import RelatorioPonto
from .config import ARQUIVO_MODELO, ARQUIVO_NOMES


class ReconhecimentoFacial:
    def __init__(
        self,
        arquivo_modelo=ARQUIVO_MODELO,
        arquivo_nomes=ARQUIVO_NOMES,
        limite_confianca=65,
        tempo_espera_registro=10
    ):
        self.arquivo_modelo = str(arquivo_modelo)
        self.arquivo_nomes = str(arquivo_nomes)
        self.limite_confianca = limite_confianca
        self.tempo_espera_registro = tempo_espera_registro

        self.detector = DetectorRosto()
        self.relatorio = RelatorioPonto()
        self.ultimo_registro = {}

        self.nomes = self._carregar_nomes()
        self.modelo = self._carregar_modelo()

    def _carregar_nomes(self):
        nomes = {}

        if not os.path.exists(self.arquivo_nomes):
            return nomes

        with open(self.arquivo_nomes, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha:
                    continue

                partes = linha.split(",", 1)
                if len(partes) != 2:
                    continue

                id_, nome = partes
                nomes[int(id_)] = nome

        return nomes

    def _carregar_modelo(self):
        if not os.path.exists(self.arquivo_modelo):
            return None

        modelo = cv2.face.LBPHFaceRecognizer_create()
        modelo.read(self.arquivo_modelo)
        return modelo

    def pronto_para_uso(self):
        return self.modelo is not None and len(self.nomes) > 0

    def iniciar(self):
        if not self.pronto_para_uso():
            return {
                "sucesso": False,
                "nome": "",
                "mensagem": "Sistema não está pronto. Verifique o modelo e o arquivo de nomes."
            }

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            return {
                "sucesso": False,
                "nome": "",
                "mensagem": "Não foi possível acessar a câmera."
            }

        tempo_inicial = time.time()
        tempo_limite = 15  # espera até 15 segundos

        while True:
            ok, frame = camera.read()
            if not ok:
                camera.release()
                cv2.destroyAllWindows()
                return {
                    "sucesso": False,
                    "nome": "",
                    "mensagem": "Erro ao capturar imagem da câmera."
                }

            gray, faces = self.detector.detectar(frame)

            for (x, y, w, h) in faces:
                rosto, (x1, y1, x2, y2) = self.detector.recortar_rosto_com_margem(
                    frame, gray, x, y, w, h, margem=50
                )

                label, confianca = self.modelo.predict(rosto)

                if confianca < self.limite_confianca:
                    nome = self.nomes.get(label, "Desconhecido")
                    self.relatorio.salvar(nome, confianca, "Ponto registrado")

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    cv2.putText(
                        frame,
                        f"Acesso liberado: {nome}",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        2
                    )

                    cv2.imshow("Sistema de Ponto Facial", frame)
                    cv2.waitKey(1500)

                    camera.release()
                    cv2.destroyAllWindows()

                    return {
                        "sucesso": True,
                        "nome": nome,
                        "mensagem": f"Ponto registrado com sucesso para {nome}."
                    }

                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
                    cv2.putText(
                        frame,
                        "Rosto nao autorizado",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        2
                    )

            cv2.imshow("Sistema de Ponto Facial", frame)

            if cv2.waitKey(1) == 27:
                camera.release()
                cv2.destroyAllWindows()
                return {
                    "sucesso": False,
                    "nome": "",
                    "mensagem": "Reconhecimento cancelado."
                }

            if time.time() - tempo_inicial > tempo_limite:
                camera.release()
                cv2.destroyAllWindows()
                return {
                    "sucesso": False,
                    "nome": "",
                    "mensagem": "Tempo esgotado. Nenhum rosto reconhecido."
                }
