import cv2
import os
from .detector import DetectorRosto
from .config import PASTA_ROSTOS


class CadastroFuncionario:
    def __init__(self, pasta_rostos=PASTA_ROSTOS, max_fotos=100):
        self.pasta_rostos = str(pasta_rostos)
        self.max_fotos = max_fotos
        self.detector = DetectorRosto()

        os.makedirs(self.pasta_rostos, exist_ok=True)

    def cadastrar(self, nome):
        nome = nome.strip()

        if not nome:
            print("Nome inválido.")
            return False

        pasta_pessoa = os.path.join(self.pasta_rostos, nome)
        os.makedirs(pasta_pessoa, exist_ok=True)

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            print("Não foi possível acessar a câmera.")
            return False

        contador = 0

        print(f"Iniciando cadastro de: {nome}")
        print("Olhe para a câmera e mexa levemente o rosto.")
        print("Pressione ESC para sair.")

        while True:
            ok, frame = camera.read()
            if not ok:
                print("Erro ao acessar a câmera.")
                break

            gray, faces = self.detector.detectar(frame)

            for (x, y, w, h) in faces:
                rosto, (x1, y1, x2, y2) = self.detector.recortar_rosto_com_margem(
                    frame, gray, x, y, w, h, margem=50
                )

                caminho_imagem = os.path.join(pasta_pessoa, f"{contador}.jpg")
                cv2.imwrite(caminho_imagem, rosto)
                contador += 1

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

                cv2.putText(
                    frame,
                    f"Fotos: {contador}/{self.max_fotos}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                break

            cv2.imshow("Cadastro de Funcionario", frame)

            tecla = cv2.waitKey(100)
            if tecla == 27 or contador >= self.max_fotos:
                break

        camera.release()
        cv2.destroyAllWindows()

        print(f"Cadastro concluído. {contador} imagens salvas em: {pasta_pessoa}")
        return contador > 0
