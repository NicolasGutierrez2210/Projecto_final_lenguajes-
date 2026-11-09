import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.ml import (
    correlacion_pearson,
    RegresionLineal,
    KMeans,
    regresion_lineal,
    agrupar_kmedias,
    predecir_regresion
)
from src.core.visualizador import CanvasPNG, renderizar_pizarra_nativa

class TestCorte3MLYVisualizador(unittest.TestCase):

    def test_correlacion_pearson_positiva(self):
        x = [10, 20, 30, 40, 50]
        y = [2, 4, 6, 8, 10]
        r = correlacion_pearson(x, y)
        self.assertAlmostEqual(r, 1.0, places=4)

    def test_regresion_lineal_mco_y_prediccion(self):
        x = [1, 2, 3, 4, 5]
        y = [3, 5, 7, 9, 11]  # y = 2x + 1
        
        # Prueba sobre la clase
        modelo = RegresionLineal()
        res = modelo.ajustar(x, y)
        self.assertAlmostEqual(res.m, 2.0, places=4)
        self.assertAlmostEqual(res.b, 1.0, places=4)
        self.assertAlmostEqual(res.r2, 1.0, places=4)
        pred = modelo.predecir(6)
        self.assertAlmostEqual(pred, 13.0, places=4)

        # Prueba sobre el helper funcional de DaZe
        res_dict = regresion_lineal(x, y)
        self.assertAlmostEqual(res_dict["m"], 2.0, places=4)
        self.assertAlmostEqual(res_dict["b"], 1.0, places=4)
        self.assertAlmostEqual(res_dict["r2"], 1.0, places=4)
        pred_dict = predecir_regresion(res_dict, 6)
        self.assertAlmostEqual(pred_dict, 13.0, places=4)

    def test_kmeans_agrupamiento(self):
        datos = [[1.0, 1.0], [1.5, 2.0], [10.0, 10.0], [11.0, 9.5]]
        
        # Prueba sobre la clase
        km = KMeans(k=2, max_iter=20)
        res = km.ajustar(datos)
        self.assertEqual(len(res.centroides), 2)
        self.assertEqual(len(res.etiquetas), 4)
        self.assertEqual(res.etiquetas[0], res.etiquetas[1])
        self.assertEqual(res.etiquetas[2], res.etiquetas[3])
        self.assertNotEqual(res.etiquetas[0], res.etiquetas[2])

        # Prueba sobre el helper funcional de DaZe
        res_dict = agrupar_kmedias(datos, 2)
        self.assertEqual(len(res_dict["centroides"]), 2)
        self.assertEqual(len(res_dict["etiquetas"]), 4)

    def test_generacion_fisica_png_valido(self):
        ruta_test_png = "salidas/test_verificacion.png"
        canvas = CanvasPNG(ancho=100, alto=100)
        canvas.rectangulo(10, 10, 90, 90, (255, 0, 0))
        canvas.guardar(ruta_test_png)

        self.assertTrue(os.path.exists(ruta_test_png))
        with open(ruta_test_png, "rb") as f:
            cabecera = f.read(8)
        self.assertEqual(cabecera, b'\x89PNG\r\n\x1a\n')

        if os.path.exists(ruta_test_png):
            os.remove(ruta_test_png)

    def test_renderizado_pizarra_nativa_barras(self):
        filas = [{"pos": "DEL", "goles": 10}, {"pos": "MED", "goles": 5}]
        config = {
            "eje_x": "pos",
            "eje_y": "goles",
            "titulo": "Test Barras",
            "guardar": "salidas/test_barras.png"
        }
        renderizar_pizarra_nativa("barras", filas, config)
        self.assertTrue(os.path.exists("salidas/test_barras.png"))
        if os.path.exists("salidas/test_barras.png"):
            os.remove("salidas/test_barras.png")

if __name__ == "__main__":
    unittest.main()
