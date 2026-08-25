import cv2
import requests
from ultralytics import YOLO


# ==============================
# CONFIGURACIÓN ESP32
# ==============================

ESP32_IP = "192.168.1.50"   # Cambia por la IP de tu ESP32


# ==============================
# MODELO YOLO
# ==============================

model = YOLO('yolov8n.pt')


# ==============================
# CÁMARA
# ==============================

cap = cv2.VideoCapture(0)


ultimo_comando = ""


while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        print("No se pudo acceder a la cámara.")
        break


    # ==============================
    # DETECCIÓN YOLO
    # ==============================

    resultados = model(frame, verbose=False)

    carro_detectado = False
    moto_detectada = False


    for r in resultados:

        for caja in r.boxes:

            clase = int(caja.cls[0])


            # Clase 2 = carro
            if clase == 2:
                carro_detectado = True


            # Clase 3 = moto
            elif clase == 3:
                moto_detectada = True


    # ==============================
    # CONTROL DE LEDs
    # ==============================

    if carro_detectado:

        comando = "carro"

        color_rojo = (0, 0, 255)

    elif moto_detectada:

        comando = "moto"

        color_rojo = (50, 50, 100)

    else:

        comando = "apagado"

        color_rojo = (50, 50, 100)


    # Solo enviar a la ESP32 cuando cambia el estado
    if comando != ultimo_comando:

        try:

            requests.get(
                f"http://{ESP32_IP}/led",
                params={"cmd": comando},
                timeout=0.2
            )

            ultimo_comando = comando

        except requests.exceptions.RequestException:

            print("No se pudo conectar con la ESP32.")


    # ==============================
    # INDICADOR CARRO
    # ==============================

    color_rojo = (0, 0, 255) if carro_detectado else (50, 50, 100)

    cv2.circle(
        frame,
        (50, 50),
        30,
        color_rojo,
        -1
    )

    cv2.putText(
        frame,
        "CARRO",
        (100, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color_rojo,
        2
    )


    # ==============================
    # INDICADOR MOTO
    # ==============================

    color_azul = (255, 0, 0) if moto_detectada else (50, 50, 50)

    cv2.circle(
        frame,
        (50, 150),
        30,
        color_azul,
        -1
    )

    cv2.putText(
        frame,
        "MOTO",
        (100, 160),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        color_azul,
        2
    )


    # ==============================
    # MOSTRAR CÁMARA
    # ==============================

    cv2.imshow(
        'YOLO - Presiona Q para salir',
        frame
    )


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# ==============================
# APAGAR LEDs AL TERMINAR
# ==============================

try:
    requests.get(
        f"http://{ESP32_IP}/led",
        params={"cmd": "apagado"},
        timeout=0.2
    )
except:
    pass


cap.release()
cv2.destroyAllWindows()