from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from .calculos import MODALIDADES, ErrorValidacion, calcular_valores
from .repositorio import repositorio

CAMPOS = ("nombre", "equipos", "dias_iniciales", "dias_adicionales", "modalidad")


def _contexto(datos=None, errores=None):
    return {
        "datos": datos or {"dias_adicionales": "0"},
        "errores": errores or {},
        "modalidades": MODALIDADES.items(),
        "servicios": repositorio.listar()[:10],
    }


@require_GET
def inicio(request):
    return render(request, "liquidacion/inicio.html", _contexto())


@require_POST
def liquidar(request):
    datos = {campo: request.POST.get(campo, "").strip() for campo in CAMPOS}
    try:
        liquidacion = calcular_valores(**datos)
    except ErrorValidacion as exc:
        return render(request, "liquidacion/inicio.html", _contexto(datos, exc.errores), status=400)
    numero = repositorio.guardar(liquidacion)
    return redirect("liquidacion:recibo", numero=numero)


@require_GET
def recibo(request, numero):
    registro = repositorio.obtener(numero)
    if registro is None:
        raise Http404("Servicio no encontrado")
    return render(request, "liquidacion/recibo.html", {"registro": registro, "l": registro["liquidacion"]})


@require_GET
def consultar(request):
    valor = request.GET.get("numero", "").strip()
    if valor.isdigit() and repositorio.obtener(int(valor)):
        return redirect("liquidacion:recibo", numero=int(valor))
    ctx = _contexto()
    ctx["error_consulta"] = f"No existe un servicio con el número «{valor}»." if valor else "Ingrese un número de servicio."
    return render(request, "liquidacion/inicio.html", ctx, status=404 if valor else 400)
