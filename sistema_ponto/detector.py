import cv2


class DetectorRosto:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detectar(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(120, 120)
        )

        return gray, faces

    def recortar_rosto_com_margem(self, frame, gray, x, y, w, h, margem=50):
        x1 = max(x - margem, 0)
        y1 = max(y - margem, 0)
        x2 = min(x + w + margem, frame.shape[1])
        y2 = min(y + h + margem, frame.shape[0])

        rosto = gray[y1:y2, x1:x2]
        rosto = cv2.resize(rosto, (200, 200))

        return rosto, (x1, y1, x2, y2)
