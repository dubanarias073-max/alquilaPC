# Plan de Pruebas – Sistema ALQUILAPC v1.0
**Estándar de referencia:** ISO/IEC/IEEE 29119-3 · **Aplicación bajo prueba:** AlquilaPC (Django) + `proyecto1.py` (consola)
**Elaboró:** Cristian Camilo Rojas Vesga – Ficha 3407184 – ADSO, SENA

## 1. Introducción
**Propósito.** Definir estrategia, actividades, recursos y criterios para verificar y validar el sistema ALQUILAPC de alquiler de portátiles por días.

**Alcance – incluido:** registro de nombre, equipos, días iniciales y adicionales; selección del tipo de servicio; cálculo base; descuentos; incremento por domicilio; total; generación/impresión del recibo; consulta de servicios; validaciones de entrada.

**Excluido:** seguridad informática, control de acceso, gestión de usuarios, base de datos/persistencia, impresoras físicas, alta concurrencia, servicios web externos.

## 2. Objetivos
**General:** determinar si ALQUILAPC cumple los requisitos funcionales y reglas de negocio.
**Específicos:** validar reglas de negocio; detectar defectos de cálculo y de validación; verificar el recibo; confirmar el manejo de entradas inválidas; garantizar la estabilidad del flujo completo.

## 3. Criterios de éxito
| Métrica | Criterio |
|---|---|
| Casos ejecutados | 100 % |
| Casos aprobados | ≥ 95 % |
| Casos críticos fallidos | 0 |
| Cobertura de reglas de negocio | 100 % |
| Cobertura de validaciones | 100 % |
| Defectos críticos abiertos | 0 |

## 4. Elementos bajo prueba
| ID | Componente | Ubicación |
|---|---|---|
| CP-01 | Captura de datos básicos | `templates/inicio.html`, `views.liquidar` |
| CP-02 a CP-05 | Validaciones (nombre, equipos, días, adicionales) | `calculos.validar_datos` |
| CP-06 | Selección tipo de servicio | `calculos.MODALIDADES` |
| CP-07 | Cálculo alquiler inicial | `calculo_alquiler` |
| CP-08 | Cálculo descuentos | `calculo_alquiler_adicional_dto`, `calculo_dentro_establecimiento` |
| CP-09 | Cálculo domicilio | `calculo_domicilio` |
| CP-10 | Cálculo total | `calcular_valores` |
| CP-11 | Generación factura / consulta | `views.recibo`, `views.consultar` |

## 5. Reglas de negocio
RN01 $35.000 por equipo/día · RN02 mínimo 2 equipos · RN03 tres modalidades · RN04 domicilio 5 % después de descuentos · RN05 descuento 5 % establecimiento · RN06 2 % sobre el total de días adicionales · RN07 contenido del recibo.

## 6. Estrategia
| Fase | Objetivo | Implementación |
|---|---|---|
| 1. Unitarias (caja blanca) | Cada función y rama del cálculo | `tests/test_caja_blanca.py` (19 casos) |
| 2. Integración | Vista ↔ cálculo ↔ repositorio ↔ recibo | `tests/test_web.py` (13 casos) |
| 3. Sistema (caja negra) | Flujo completo desde el navegador, escenarios S01–S05 | `pruebas_ui/casos.py` CP001–CP028 + `tests/test_caja_negra.py` |
| 4. UAT | Validación del cliente/usuario final | Lista CP001–CP028 ejecutada manualmente por el cliente |
| 5. Regresión | Que una corrección no rompa lo aprobado | `tests/test_regresion.py` + re-ejecución de CP001–CP028 (ronda 2) |

Escenarios: **S01** 2 eq/1 día/ciudad → $70.000 · **S02** 2 eq/3 días/fuera → $220.500 · **S03** 5 eq/10 días/establecimiento → $1.662.500 · **S04** con días adicionales (2 eq/1 día/2 adic) → $207.200 · **S05** máximo descuento (10 eq/30 días/10 adic/establecimiento) → $13.233.500.

## 7. Técnicas de diseño
- **Partición de equivalencia:** equipos válido ≥ 2 / inválido < 2; nombre vacío / con texto; modalidad válida / inválida.
- **Valores límite:** equipos 1-2-3; días iniciales 0-1; días adicionales −1-0-1; nombre 100-101 caracteres.
- **Tabla de decisión:** ciudad / fuera / establecimiento × con / sin adicionales.
- **Reglas de negocio:** secuencia descuentos → incrementos → total.

## 8. Datos de prueba
**Válidos:** Juan 2 eq 1 día · María 5 eq 5 días · Pedro 10 eq 30 días · Juan Pérez 5 eq 4 días 3 adic (tabla de referencia).
**Inválidos:** nombre "" · equipos 0 y 1 · equipos "abc" · días 0 · días adicionales −1 · modalidad 4 · nombre de 150 caracteres.

## 9. Ambiente
PC Intel i5 / 8 GB RAM · Windows 10/11 o Ubuntu 22.04+ · Python 3.10+ · Django 5 · unittest · Playwright (opcional, ejecución en navegador) · VS Code · Excel · Git.

## 10. Riesgos y mitigación
| Riesgo | Impacto | Mitigación |
|---|---|---|
| Cálculos incorrectos | Alto | Pruebas unitarias por función + valores de referencia |
| Validaciones incompletas | Alto | Valores límite en todas las entradas, también en el servidor |
| Requisitos contradictorios | Medio | Trazabilidad y registro de hallazgos (H-01, H-02) |
| Datos inválidos no controlados | Alto | Casos negativos con petición manipulada (CP009, CP019, CP027) |
| Defectos en recibo | Medio | CP024 verifica el contenido de RN07 |

## 11. Criterios de entrada
Código ejecutable, requisitos aprobados, ambiente configurado, casos diseñados.

## 12. Criterios de salida
100 % casos ejecutados; 100 % reglas verificadas; sin defectos críticos abiertos; defectos mayores corregidos o aceptados; informe aprobado.

## 13. Roles
Líder QA (planificación) · Analista QA (diseño de casos) · Tester (ejecución y evidencias) · Desarrollador (corrección) · Product Owner (validación funcional) · Cliente (aceptación).

## 14. Cronograma indicativo
Planificación 1 d · Diseño de casos 2 d · Ambiente 1 d · Unitarias 1 d · Integración 1 d · Sistema 2 d · Correcciones y regresión 2 d · UAT 1 d · Informe 1 d → **12 días hábiles**.

## 15. Entregables
Plan de pruebas · Matriz de trazabilidad · Casos de prueba · Datos de prueba · Bitácora de ejecución · Registro de incidentes · Evidencias · Informe final (ver `docs/`).

## 16. Aprobación
Líder QA · Desarrollador responsable · Product Owner · Representante del negocio.
