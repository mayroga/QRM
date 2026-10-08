import io
import base64
from flask import Flask, request, jsonify, send_file
import qrcode # Se requiere 'pip install qrcode[pil]'

app = Flask(__name__)

@app.route('/')
def index():
    """
    Sirve el archivo HTML principal que contiene todo el frontend (HTML, CSS, JavaScript).
    """
    return send_file('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    """
    Endpoint para generar códigos QR.
    Recibe texto/URL en formato JSON, genera un QR y lo devuelve como imagen base64.
    """
    data = request.json.get('text')
    if not data:
        return jsonify({'error': 'No se proporcionó texto para generar el QR'}), 400

    try:
        # Configuración del código QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L, # Nivel de corrección de error bajo
            box_size=10, # Tamaño de cada "caja" o pixel del QR
            border=4, # Ancho del borde (en cajas)
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Crea la imagen del QR
        img = qr.make_image(fill_color="black", back_color="white")

        # Guarda la imagen en un stream de bytes en memoria
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0) # Vuelve al inicio del stream

        # Codifica la imagen a base64 para enviarla al frontend
        img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Devuelve la imagen base64 en un formato de datos URI
        return jsonify({'image': f'data:image/png;base64,{img_base64}'})

    except Exception as e:
        # Manejo de errores en la generación del QR
        print(f"Error al generar QR: {e}")
        return jsonify({'error': f'Error interno del servidor al generar el QR: {str(e)}'}), 500

if __name__ == '__main__':
    # Ejecuta la aplicación Flask.
    # En producción, se recomienda usar un servidor WSGI como Gunicorn.
    # host='0.0.0.0' hace que el servidor sea accesible desde cualquier IP.
    app.run(host='0.0.0.0', port=5000)
