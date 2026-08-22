import cv2
from ultralytics import YOLO
# Actualizacion de yolo
# Cualquier cosa

# Cargar YOLOv8
model = YOLO("yolov8n.pt")

# Abrir cámara frontal
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("No se pudo recibir imagen de la cámara")
        break

    # YOLOv8 detecta objetos
    results = model(frame, conf=0.5)

    # Dibujar las detecciones
    annotated_frame = results[0].plot()

    # Mostrar cámara
    cv2.imshow("YOLOv8 - Camara frontal", annotated_frame)

    # Presionar Q para salir
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()