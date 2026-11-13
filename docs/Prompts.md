# Prompts utilizados en el taller

## 1. Prompt – Product Backlog
```
Actúa como Product Owner de un equipo Scrum. Lee el archivo adjunto
'Descripcion_funcional.md' del sistema ALQUILAPC (alquiler de portátiles por días,
$35.000 por equipo/día, descuentos del 2 % por días adicionales y 5 % en el
establecimiento, cargo del 5 % fuera de la ciudad, mínimo 2 equipos, recibo imprimible).

Genera el Product Backlog en una tabla con las columnas:
PBI | Historia de usuario | Criterios de aceptación.

- Numera los ítems PBI001, PBI002, ...
- Redacta cada historia como "Como empleado de ALQUILAPC, quiero ... para ...".
- Escribe de 4 a 6 criterios de aceptación verificables por historia (incluye valores
  límite y mensajes de error).
- Cubre: registro de datos, validaciones, cálculo base, cada descuento, el incremento,
  el total, el detalle de descuentos/incrementos y la generación e impresión del recibo.
- Respeta exactamente el orden de cálculo de la descripción funcional y señala al final
  cualquier ambigüedad o contradicción que encuentres en los requisitos.
```

## 2. Prompt – Plan de pruebas
```
Actúa como Líder QA. Con base en el código adjunto (proyecto ALQUILAPC: liquidacion/calculos.py,
views.py y proyecto1.py), el Product Backlog y la norma ISO/IEC/IEEE 29119-3, elabora el
Plan de Pruebas del sistema ALQUILAPC versión 1.0 con estas secciones:
1. Introducción (propósito y alcance: funcionalidades incluidas y excluidas)
2. Objetivos de las pruebas (general y específicos)
3. Criterios de éxito (tabla de métricas)
4. Elementos bajo prueba (CP-01 ... CP-11)
5. Reglas de negocio a validar (RN01 ... RN07)
6. Estrategia por fases: unitarias, integración, sistema (escenarios S01–S05), UAT y regresión
7. Técnicas de diseño: partición de equivalencia, valores límite, tabla de decisión, reglas de negocio
8. Datos de prueba válidos e inválidos
9. Ambiente de pruebas (hardware, software, herramientas)
10. Riesgos y mitigación
11. Criterios de entrada  12. Criterios de salida
13. Roles y responsabilidades  14. Cronograma  15. Entregables  16. Aprobación
Usa tablas cuando ayuden y lenguaje técnico en español.
```

## 3. prompt_generaruml_testing
```
Actúa como arquitecto de software y analista QA. Analiza el proyecto ALQUILAPC adjunto
(Django + Python, sin base de datos; lógica en liquidacion/calculos.py con las funciones
calcular_valores, calculo_alquiler, calculo_alquiler_adicional, calculo_descuento,
calculo_alquiler_adicional_dto, calculo_dentro_establecimiento y calculo_domicilio).

Genera:
1. Diagramas UML básicos en código Mermaid (y también PlantUML):
   a. Casos de uso (actor Empleado/Cliente; include/extend para descuentos, cargo y factura)
   b. Clases (módulo calculos, Liquidacion, ErrorValidacion, RepositorioMemoria, views)
   c. Secuencia del flujo "liquidar servicio" (válido e inválido)
   d. Actividad del cálculo del total
2. Un archivo de pruebas con unittest (equivalente a JUnit en Python) que incluya:
   - Caja negra: partición de equivalencia y valores límite (equipos 1/2/3,
     días 0/1, días adicionales -1/0/1, modalidad inválida, nombre vacío)
   - Caja blanca: cada función y cada rama if/else al menos una vez
   - Regresión: valores aprobados de la tabla de referencia
     (5 eq, 4 días, 3 adicionales → 1.214.500 / 1.275.225 / 1.153.775)
3. Un informe de hallazgos con: ID, tipo, severidad, descripción, evidencia,
   acción tomada y estado; más un resumen de métricas (ejecutados, aprobados, fallidos).
```

## 4. Prompt – Casos de prueba
```
Con base en el Plan de Pruebas y el Product Backlog de ALQUILAPC, genera la matriz de
casos de prueba según ISO/IEC/IEEE 29119-3 con las columnas:
ID | Objetivo | Precondiciones | Entradas | Resultados esperados | Poscondición,
agregando Tipo (caja negra / caja blanca), Técnica, Trazabilidad (PBI/RN),
Resultado obtenido, Estado y Evidencia. Incluye casos positivos, negativos y de
valores límite para cada validación, un caso por modalidad con los valores
esperados exactos y los escenarios S01–S05 del plan.
```
