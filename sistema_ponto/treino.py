import cv2
import os
import numpy as np
from .config import ARQUIVO_MODELO, ARQUIVO_NOMES, PASTA_ROSTOS


class TreinadorModelo:
    def __init__(self, pasta_rostos=PASTA_ROSTOS, arquivo_modelo=ARQUIVO_MODELO, arquivo_nomes=ARQUIVO_NOMES):
        self.pasta_rostos = str(pasta_rostos)
        self.arquivo_modelo = str(arquivo_modelo)
        self.arquivo_nomes = str(arquivo_nomes)

    def treinar(self):
        if not os.path.exists(self.pasta_rostos):
            print("A pasta de rostos não existe.")
            return False

        faces = []
        labels = []
        nomes = {}
        label_id = 0

        for nome_pessoa in os.listdir(self.pasta_rostos):
            caminho_pessoa = os.path.join(self.pasta_rostos, nome_pessoa)

            if not os.path.isdir(caminho_pessoa):
                continue

            nomes[label_id] = nome_pessoa

            for arquivo in os.listdir(caminho_pessoa):
                caminho_arquivo = os.path.join(caminho_pessoa, arquivo)

                img = cv2.imread(caminho_arquivo, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    continue

                faces.append(img)
                labels.append(label_id)

            label_id += 1

        if len(faces) == 0:
            print("Nenhuma face encontrada para treinar.")
            return False

        modelo = cv2.face.LBPHFaceRecognizer_create()
        modelo.train(faces, np.array(labels))
        modelo.save(self.arquivo_modelo)

        with open(self.arquivo_nomes, "w", encoding="utf-8") as f:
            for id_, nome in nomes.items():
                f.write(f"{id_},{nome}\n")

        print("Modelo treinado com sucesso!")
        print(f"Arquivo gerado: {self.arquivo_modelo}")
        print(f"Arquivo gerado: {self.arquivo_nomes}")
        return True
