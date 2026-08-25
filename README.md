# Sistema de detección de vehículos mediante YOLO y ESP32

## Descripción del proyecto

Este proyecto implementa un sistema de visión artificial capaz de identificar vehículos en tiempo real mediante una cámara conectada al computador. Para realizar la detección se utiliza el modelo **YOLOv8**, ejecutado mediante Python y la biblioteca Ultralytics.

El sistema analiza continuamente los fotogramas obtenidos desde la cámara y determina si dentro de la imagen se encuentra un automóvil o una motocicleta. Dependiendo del objeto identificado, Python establece una comunicación con una tarjeta **ESP32 mediante Wi-Fi**, permitiendo controlar indicadores luminosos conectados a sus pines GPIO.

El funcionamiento está diseñado para que la detección de un automóvil active un LED rojo, mientras que la detección de una motocicleta active un LED azul. Cuando no se detectan estos objetos, los indicadores permanecen apagados.

La arquitectura general del sistema puede representarse de la siguiente manera:

```text
                    CÁMARA
                       │
                       ▼
                ┌─────────────┐
                │   Python    │
                │   OpenCV    │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │   YOLOv8    │
                │  Detección  │
                └──────┬──────┘
                       │
             ┌─────────┴─────────┐
             │                   │
          Automóvil           Motocicleta
             │                   │
             ▼                   ▼
        LED ROJO             LED AZUL
             │                   │
             └─────────┬─────────┘
                       │
                       ▼
                    ESP32
                       │
                      Wi-Fi
```

## Tecnologías utilizadas

El procesamiento de imágenes se realiza utilizando Python junto con OpenCV. La detección de objetos se encuentra implementada mediante YOLOv8 utilizando el paquete Ultralytics.

La comunicación entre el computador y la tarjeta ESP32 se realiza mediante solicitudes HTTP sobre una red Wi-Fi local. De esta manera, el computador ejecuta el procesamiento pesado de visión artificial, mientras que la ESP32 se encarga principalmente del control de las salidas digitales.

Las principales tecnologías utilizadas en el proyecto son:

* Python 3
* YOLOv8
* Ultralytics
* OpenCV
* Requests
* ESP32
* Arduino IDE
* Comunicación HTTP
* Wi-Fi

## Estructura del proyecto

Se recomienda mantener una estructura organizada para separar el entorno virtual, los modelos y el código fuente.

```text
YOLO_ESP23/
│
├── .venv/
│   └── Entorno virtual de Python
│
├── yolov8n.pt
│   └── Modelo YOLOv8 Nano
│
├── detector.py
│   └── Programa principal de detección
│
├── esp32_leds/
│   └── Código de la ESP32
│
└── README.md
    └── Documentación del proyecto
```

La carpeta `.venv` corresponde exclusivamente al entorno virtual de Python y no contiene el código principal del proyecto. Se recomienda no subir esta carpeta al repositorio de GitHub, ya que puede ser recreada utilizando los comandos de instalación descritos posteriormente.

## Configuración del entorno virtual

El proyecto utiliza un entorno virtual para mantener aisladas las dependencias de Python. Esto permite evitar conflictos entre las bibliotecas utilizadas por este proyecto y aquellas instaladas globalmente en el computador.

Desde la terminal de Visual Studio Code se debe acceder a la carpeta del proyecto:

```powershell
cd "C:\Users\Cocot\OneDrive\Documentos\1. MATERIAS UNIVERSIDAD MILITAR NUEVA GRANADA\QUINTO SEMESTRE\Micros\YOLO\YOLO_ESP23"
```

Posteriormente se crea el entorno virtual mediante:

```powershell
python -m venv .venv
```

Para activarlo desde PowerShell se utiliza:

```powershell
.\.venv\Scripts\Activate.ps1
```

Una vez activado correctamente, la terminal mostrará el nombre `.venv` al comienzo de la línea de comandos.

En caso de que PowerShell impida ejecutar el script de activación debido a las políticas de ejecución, se puede utilizar temporalmente:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Después de realizar este cambio se vuelve a ejecutar:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Instalación de las dependencias

Con el entorno virtual activo se recomienda actualizar `pip` antes de instalar las bibliotecas:

```powershell
python -m pip install --upgrade pip
```

Las principales dependencias del proyecto se instalan mediante:

```powershell
python -m pip install ultralytics opencv-python requests
```

OpenCV proporciona las herramientas necesarias para acceder a la cámara y procesar los fotogramas. Ultralytics permite cargar y ejecutar el modelo YOLOv8, mientras que Requests se utiliza para realizar las solicitudes HTTP dirigidas a la ESP32.

Para verificar que las bibliotecas fueron instaladas correctamente se puede ejecutar:

```powershell
python -c "import cv2; from ultralytics import YOLO; import requests; print('TODO OK')"
```

Si la instalación es correcta, el programa mostrará:

```text
TODO OK
```

## Modelo YOLOv8

El proyecto utiliza el modelo `yolov8n.pt`, correspondiente a la versión Nano de YOLOv8. Este modelo permite realizar detección de objetos en tiempo real manteniendo un consumo computacional relativamente bajo.

La carga del modelo se realiza en Python mediante:

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
```

Cuando el modelo se ejecuta sobre una imagen obtenida desde la cámara, devuelve las detecciones encontradas junto con información como la clase del objeto, las coordenadas de la caja delimitadora y la confianza de la detección.

Para este proyecto se utilizan las clases correspondientes a automóvil y motocicleta del conjunto de datos COCO.

La clase utilizada para automóvil es:

```text
2
```

Mientras que la clase utilizada para motocicleta es:

```text
3
```

Por esta razón, el programa puede determinar qué tipo de vehículo fue identificado analizando el identificador de clase entregado por YOLO.

## Captura de video

La cámara se inicializa mediante OpenCV utilizando:

```python
cap = cv2.VideoCapture(0)
```

El valor `0` corresponde normalmente a la cámara principal del computador. Si el equipo dispone de varias cámaras, este valor puede modificarse para seleccionar otro dispositivo.

El programa obtiene continuamente nuevos fotogramas mediante:

```python
ret, frame = cap.read()
```

Cada fotograma es enviado posteriormente al modelo YOLO para realizar la detección.

## Comunicación entre Python y ESP32

La comunicación entre el computador y la ESP32 se realiza utilizando una conexión Wi-Fi dentro de la misma red local.

La ESP32 ejecuta un servidor HTTP que espera solicitudes provenientes del programa Python. Dependiendo del comando recibido, modifica el estado de los LEDs.

Por ejemplo, Python puede enviar:

```text
http://IP_DE_LA_ESP32/led?cmd=carro
```

para indicar que se detectó un automóvil.

Para una motocicleta se utiliza:

```text
http://IP_DE_LA_ESP32/led?cmd=moto
```

Finalmente, para apagar los indicadores:

```text
http://IP_DE_LA_ESP32/led?cmd=apagado
```

En el programa Python la dirección IP de la ESP32 debe configurarse en la variable:

```python
ESP32_IP = "192.168.1.50"
```

La dirección debe reemplazarse por la IP que haya obtenido la ESP32 dentro de la red Wi-Fi utilizada.

## Funcionamiento de los indicadores

El sistema utiliza dos LEDs para representar visualmente el resultado de la detección.

El LED rojo se encuentra asociado a la detección de automóviles. Cuando YOLO identifica al menos un automóvil en el fotograma actual, Python envía el comando correspondiente a la ESP32 y esta activa el GPIO asociado al LED rojo.

El LED azul se encuentra asociado a la detección de motocicletas. Cuando se identifica una motocicleta, Python envía el comando correspondiente y la ESP32 activa el GPIO asignado al LED azul.

La lógica general puede resumirse de esta forma:

```text
Automóvil detectado
        │
        ▼
   LED rojo ON

Motocicleta detectada
        │
        ▼
   LED azul ON

Ningún vehículo detectado
        │
        ▼
    LEDs OFF
```

Si se desea permitir la detección simultánea de ambos tipos de vehículos, la lógica puede modificarse para que cada LED sea controlado independientemente. De esta manera, si en una misma imagen aparece un automóvil y una motocicleta, ambos indicadores pueden permanecer encendidos.

## Conexión de los LEDs

Los LEDs deben conectarse a las salidas digitales de la ESP32 utilizando una resistencia limitadora de corriente.

Una configuración propuesta es utilizar el GPIO 25 para el LED rojo y el GPIO 26 para el LED azul.

```text
ESP32 GPIO 25
      │
      ▼
 Resistencia
   220 Ω
      │
      ▼
 LED ROJO
      │
      ▼
     GND
```

Para el segundo indicador:

```text
ESP32 GPIO 26
      │
      ▼
 Resistencia
   220 Ω
      │
      ▼
 LED AZUL
      │
      ▼
     GND
```

La resistencia es necesaria para limitar la corriente que circula por el LED y proteger tanto el LED como la salida GPIO de la ESP32.

## Ejecución del programa

Después de activar el entorno virtual y realizar la instalación de las dependencias, el programa principal puede ejecutarse mediante:

```powershell
python detector.py
```

Al iniciarse el programa se abrirá una ventana mostrando la imagen capturada por la cámara. YOLO procesará cada fotograma y determinará los objetos identificados.

Cuando se detecte un automóvil, el sistema mostrará el indicador correspondiente en la ventana y enviará la instrucción a la ESP32 para encender el LED rojo.

Cuando se detecte una motocicleta, se realizará el mismo procedimiento utilizando el LED azul.

El programa puede finalizarse presionando la tecla:

```text
Q
```

Al finalizar, el programa libera la cámara y envía una orden a la ESP32 para apagar los LEDs.

## Consideraciones de funcionamiento

El computador y la ESP32 deben encontrarse conectados a la misma red Wi-Fi para que puedan comunicarse directamente mediante la dirección IP local.

También es importante comprobar que la dirección IP configurada en Python corresponda realmente a la dirección asignada a la ESP32. Si la dirección cambia debido al DHCP del router, será necesario actualizar el valor de `ESP32_IP`.

La velocidad de detección dependerá principalmente de las características del computador, la resolución de la cámara y el modelo YOLO utilizado. El modelo `yolov8n.pt` fue seleccionado debido a que ofrece un equilibrio adecuado entre velocidad de procesamiento y capacidad de detección para una implementación académica en tiempo real.

## Posibles ampliaciones

El sistema puede utilizarse como base para desarrollar aplicaciones más completas de visión artificial y sistemas embebidos.

Entre las posibles mejoras se encuentra el conteo de vehículos, el registro de detecciones, la incorporación de sensores físicos, el almacenamiento de información en una base de datos y la creación de una interfaz gráfica para visualizar estadísticas.

También puede implementarse una comunicación bidireccional en la que la ESP32 envíe información hacia Python, permitiendo construir un sistema de monitoreo más completo.

Otra posibilidad consiste en utilizar diferentes colores para representar nuevas categorías de objetos detectados por YOLO, ampliando el sistema más allá de automóviles y motocicletas.

## Solución de problemas

Si Python muestra:

```text
ModuleNotFoundError: No module named 'cv2'
```

se debe verificar que el entorno virtual `.venv` esté activado y posteriormente instalar OpenCV:

```powershell
python -m pip install opencv-python
```

Si aparece:

```text
ModuleNotFoundError: No module named 'ultralytics'
```

se debe instalar Ultralytics:

```powershell
python -m pip install ultralytics
```

Si aparece un error relacionado con `requests`, se puede instalar mediante:

```powershell
python -m pip install requests
```

Para comprobar qué intérprete de Python está utilizando Windows se puede ejecutar:

```powershell
where.exe python
```

La primera ruta debería corresponder al entorno virtual:

```text
...\YOLO_ESP23\.venv\Scripts\python.exe
```

Si la ESP32 no responde, primero se debe verificar que esté conectada a la misma red Wi-Fi que el computador y posteriormente comprobar que la dirección IP utilizada en Python sea correcta.

## Simulación

Se uso la plataforma de Woki para elaborar el montaje de la ESP32

https://wokwi.com/projects/473288472478494721

![Foto](img/foto.png)


## Bibliografía

Ultralytics. (2023). *Ultralytics YOLOv8 Documentation*. Ultralytics.
https://docs.ultralytics.com/

OpenCV. (2026). *OpenCV Documentation*. Open Source Computer Vision Library.
https://docs.opencv.org/

Python Software Foundation. (2026). *Python Documentation*. Python.org.
https://docs.python.org/3/

Espressif Systems. (2026). *ESP32 Series Documentation*. Espressif Systems.
https://docs.espressif.com/projects/esp32/

Arduino. (2026). *Arduino Documentation*. Arduino.
https://docs.arduino.cc/

Lin, T. Y., Maire, M., Belongie, S., Hays, J., Perona, P., Ramanan, D., Dollár, P., & Zitnick, C. L. (2014). *Microsoft COCO: Common Objects in Context*. European Conference on Computer Vision (ECCV).

Redmon, J., Divvala, S., Girshick, R., & Farhadi, A. (2016). *You Only Look Once: Unified, Real-Time Object Detection*. Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR).

## Autor

Proyecto académico desarrollado para la implementación de un sistema de visión artificial utilizando YOLOv8, Python, OpenCV y ESP32.
