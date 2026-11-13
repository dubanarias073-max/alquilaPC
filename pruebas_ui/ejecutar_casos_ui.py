"""
Ejecuta los casos de caja negra de pruebas_ui/casos.py en un navegador real
(Playwright/Chromium) contra el servidor en ejecución y guarda evidencias.

Uso:
    pip install playwright && python -m playwright install chromium
    python manage.py runserver            # en otra terminal
    python pruebas_ui/ejecutar_casos_ui.py --ronda 1
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from casos import CASOS  # noqa: E402

BASE = "http://127.0.0.1:8000"
RAIZ = Path(__file__).resolve().parent.parent


def llenar(page, datos, sin_validacion_navegador=False):
    page.goto(BASE + "/")
    if sin_validacion_navegador:
        # Simula una petición manipulada: quita maxlength y type=number
        page.evaluate("""() => {
            document.querySelectorAll('input').forEach(i => {
                i.removeAttribute('maxlength');
                if (i.type === 'number') i.type = 'text';
            });
        }""")
    page.fill("#nombre", datos["nombre"])
    page.fill("#equipos", datos["equipos"])
    page.fill("#dias_iniciales", datos["dias_iniciales"])
    page.fill("#dias_adicionales", datos["dias_adicionales"])
    mod = datos["modalidad"]
    if mod in ("CIUDAD", "FUERA", "ESTABLECIMIENTO"):
        page.check(f"input[name=modalidad][value={mod}]")
    elif mod:
        page.evaluate("v => { const r = document.querySelector('input[name=modalidad]'); r.value = v; r.checked = true; }", mod)
    page.click("#form-liquidar button[type=submit]")
    page.wait_for_load_state()


def verificar(page, verifica):
    fallos = []
    contenido = page.content()
    texto = page.inner_text("body")
    for t in ([verifica["texto"]] if isinstance(verifica.get("texto"), str) else verifica.get("texto", [])):
        if t not in texto:
            fallos.append(f"No aparece '{t}'")
    errores = verifica.get("error")
    if errores:
        errores = [errores] if isinstance(errores, str) else errores
        for e in errores:
            if e not in texto:
                fallos.append(f"No aparece el mensaje '{e}'")
        if "/servicio/" in page.url:
            fallos.append("Se generó un recibo con datos inválidos")
    for elem, valor in verifica.get("recibo", {}).items():
        if "/servicio/" not in page.url:
            fallos.append(f"No se generó el recibo (URL {page.url})")
            break
        obtenido = page.inner_text(f"#{elem}").strip()
        if obtenido != valor:
            fallos.append(f"#{elem}: esperado '{valor}', obtenido '{obtenido}'")
    return fallos, contenido


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ronda", default="1")
    args = ap.parse_args()
    carpeta = RAIZ / "docs" / "evidencias" / f"ronda{args.ronda}"
    carpeta.mkdir(parents=True, exist_ok=True)
    resultados = []
    with sync_playwright() as p:
        nav = p.chromium.launch()
        page = nav.new_page(viewport={"width": 1200, "height": 800})
        for caso in CASOS:
            accion = caso["accion"]
            if accion == "abrir":
                page.goto(BASE + "/")
            elif accion == "liquidar":
                llenar(page, caso["datos"])
            elif accion == "post_directo":
                llenar(page, caso["datos"], sin_validacion_navegador=True)
            elif accion == "consultar":
                page.goto(BASE + "/")
                page.fill("input[name=numero]", caso["valor"])
                page.click("form.consulta button")
                page.wait_for_load_state()
            fallos, _ = verificar(page, caso["verifica"])
            evidencia = carpeta / f"{caso['id']}.png"
            page.screenshot(path=str(evidencia), full_page=True)
            obtenido = "; ".join(fallos) if fallos else "Coincide con el resultado esperado"
            if "/servicio/" in page.url and not fallos:
                obtenido += f" (recibo {page.url.rstrip('/').split('/')[-1]}, total {page.inner_text('#r-total')})"
            resultados.append({
                "id": caso["id"], "estado": "Fallido" if fallos else "Aprobado",
                "obtenido": obtenido, "evidencia": str(evidencia.relative_to(RAIZ)),
            })
            print(f"{caso['id']}: {'FALLA' if fallos else 'OK'}  {'; '.join(fallos)}")
        nav.close()
    salida = carpeta / "resultados.json"
    salida.write_text(json.dumps({"fecha": datetime.now().isoformat(timespec="seconds"),
                                  "resultados": resultados}, ensure_ascii=False, indent=2), encoding="utf-8")
    aprobados = sum(r["estado"] == "Aprobado" for r in resultados)
    print(f"\n{aprobados}/{len(resultados)} aprobados. Resultados en {salida.relative_to(RAIZ)}")
    return 0 if aprobados == len(resultados) else 1


if __name__ == "__main__":
    raise SystemExit(main())
