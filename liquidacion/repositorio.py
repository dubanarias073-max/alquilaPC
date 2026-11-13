"""Almacenamiento en memoria (no usa base de datos). Se pierde al reiniciar el servidor."""
import threading
from datetime import datetime


class RepositorioMemoria:
    def __init__(self):
        self._lock = threading.Lock()
        self._datos = {}
        self._siguiente = 1

    def guardar(self, liquidacion):
        with self._lock:
            numero = self._siguiente
            self._siguiente += 1
            self._datos[numero] = {
                "numero": numero,
                "fecha": datetime.now(),
                "liquidacion": liquidacion,
            }
            return numero

    def obtener(self, numero):
        return self._datos.get(numero)

    def listar(self):
        return sorted(self._datos.values(), key=lambda r: r["numero"], reverse=True)

    def limpiar(self):
        with self._lock:
            self._datos.clear()
            self._siguiente = 1


repositorio = RepositorioMemoria()
