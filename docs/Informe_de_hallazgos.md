# Informe de ejecución de pruebas y hallazgos – ALQUILAPC
**Proyecto:** AlquilaPC v1.0 (Django, sin base de datos) · **Norma:** ISO/IEC/IEEE 29119-3
**Ejecutó:** Cristian Camilo Rojas Vesga – Ficha 3407184 – ADSO, SENA · **Fecha:** 13/11/2026

## 1. Resumen
| Tipo de prueba | Casos | Ronda 1 | Ronda 2 (regresión) |
|---|---:|---:|---:|
| Caja negra – interfaz web (CP001–CP028) | 28 | 27 ✔ / 1 ✘ | 28 ✔ |
| Caja negra – unittest | 28 | 26 ✔ | 28 ✔ (+2 por H-03) |
| Caja blanca – unittest | 19 | 19 ✔ | 19 ✔ |
| Regresión – valores dorados | 4 (12 combinaciones) | 3 ✔ | 4 ✔ (+1 por H-03) |
| Integración web – unittest | 13 | 12 ✔ | 13 ✔ (+1 por H-03) |
| **Total unittest** | 64 | 60 / 60 OK | **64 / 64 OK** |

Resultado: **100 % de casos aprobados en la ronda 2**, cobertura de las 7 reglas de negocio y de los 14 PBI. 0 defectos críticos abiertos.

## 2. Pruebas de caja negra
Diseñadas solo con los requisitos (partición de equivalencia, valores límite, tabla de decisión, escenarios S01–S05). Se ejecutaron desde el navegador sobre el formulario real y cada caso tiene captura en `docs/evidencias/ronda1/` y `ronda2/`.

Verificación de la tabla de referencia del taller (5 equipos, 4 días, 3 adicionales):

| Modalidad | Esperado | Obtenido | Estado |
|---|---:|---:|---|
| En la ciudad | $1.214.500 | $1.214.500 | Aprobado |
| Fuera de la ciudad | $1.275.225 | $1.275.225 | Aprobado |
| En el establecimiento | $1.153.775 | $1.153.775 | Aprobado |

## 3. Pruebas de caja blanca
Diseñadas mirando `liquidacion/calculos.py`: cada función del diagrama (`calculo_alquiler`, `calculo_alquiler_adicional`, `calculo_descuento`, `calculo_alquiler_adicional_dto`, `calculo_dentro_establecimiento`, `calculo_domicilio`, `calcular_valores`) y **cada rama if/else** se ejecuta al menos una vez (por ejemplo, la rama verdadera y la falsa de `calculo_domicilio`), además del redondeo y la conversión de entradas.

## 4. Pruebas de regresión
1. **Ronda 1:** CP027 falló (H-03).
2. **Corrección:** validación de longitud del nombre en el servidor.
3. **Ronda 2:** se re-ejecutaron las 64 pruebas unitarias y los 28 casos de interfaz: todo aprobado, sin efectos sobre lo ya aprobado. La suite `tests/test_regresion.py` fija 12 totales aprobados para detectar cualquier cambio futuro en los cálculos.

## 5. Hallazgos
| ID | Tipo | Severidad | Descripción | Acción | Estado |
|---|---|---|---|---|---|
| H-01 | Requisitos | Media | PBI009 dice "2 % por **cada** día adicional"; la descripción funcional y la hoja de referencia aplican 2 % sobre el **total** de los días adicionales (descuento 10.500, no 31.500). | Se implementó según la descripción y la hoja. Corregir PBI009/RN06. | Cerrado |
| H-02 | Requisitos | Media | PBI009 (criterio 2) pide calcular el 2 % "después de otros descuentos", pero la hoja de referencia aplica primero el 2 % y luego el 5 % del establecimiento sobre ese subtotal (71.225 = 10.500 + 60.725). | Se siguió la hoja. Corregir el criterio. | Cerrado |
| H-03 | **Defecto** | Media | El límite de 100 caracteres del nombre solo existía en el HTML. Con la petición manipulada el servidor aceptó 150 caracteres y generó recibo (CP027). | Validación en `validar_datos()`, 3 pruebas nuevas, regresión OK. | Corregido |
| H-04 | Dato de prueba | Baja | Un valor esperado de la suite de regresión estaba mal calculado a mano (2 eq/2 días/1 adic/establecimiento). El sistema calculaba bien: 11.830 de descuento y 198.170 de total. | Se corrigió el dato esperado. | Cerrado |
| H-05 | Requisitos | Baja | El mínimo de 2 equipos está en el backlog y el plan, pero no en la descripción funcional. | Se implementó; confirmar con el Product Owner. | Abierto |
| H-06 | Limitación | Baja | Los servicios se guardan en memoria (requisito: sin base de datos) y se pierden al reiniciar el servidor. | Documentado en el README. | Cerrado |

## 6. Conclusión
El sistema cumple los criterios de salida del plan: 100 % de casos ejecutados, ≥ 95 % aprobados, 0 defectos críticos abiertos y 100 % de reglas de negocio verificadas. Queda pendiente confirmar H-05 con el Product Owner y corregir el texto de PBI009.
