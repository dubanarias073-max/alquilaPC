# Product Backlog – ALQUILAPC

| PBI | Historia de usuario | Criterios de aceptación |
|---|---|---|
| PBI001 | Como empleado de ALQUILAPC, quiero registrar el nombre del cliente para identificar al responsable del alquiler. | 1. Permite ingresar el nombre. 2. Es obligatorio. 3. Aparece en el recibo. 4. No se genera recibo si está vacío. |
| PBI002 | Como empleado, quiero registrar la cantidad de equipos para calcular el valor del servicio. | 1. Permite ingresar la cantidad. 2. Mínimo 2 equipos. 3. Impide registrar menos de 2. 4. Aparece en el recibo. |
| PBI003 | Como empleado, quiero registrar los días iniciales para calcular el costo base. | 1. Permite ingresarlos. 2. Deben ser mayores a cero. 3. Costo base = equipos × días × $35.000. 4. Se muestran en el recibo. |
| PBI004 | Como empleado, quiero seleccionar la modalidad para aplicar descuentos o incrementos. | 1. Solo una modalidad. 2. Opciones: dentro de la ciudad, fuera de la ciudad, dentro del establecimiento. 3. No continúa sin modalidad. 4. Se muestra en el recibo. |
| PBI005 | Como empleado, quiero calcular automáticamente el valor base para evitar errores manuales. | 1. Tarifa $35.000 por equipo/día. 2. Considera equipos. 3. Considera días iniciales. 4. Es la base de descuentos e incrementos. |
| PBI006 | Como empleado, quiero un descuento del 5 % en el establecimiento. | 1. Solo en "Dentro del establecimiento". 2. 5 % del valor calculado. 3. Se muestra el valor. 4. Se refleja en el total. 5. Aparece en el recibo. |
| PBI007 | Como empleado, quiero un incremento por domicilio fuera de la ciudad. | 1. Solo en "Fuera de la ciudad". 2. 5 % del valor después de descuentos. 3. Se muestra el valor. 4. Se refleja en el total. 5. Aparece en el recibo. |
| PBI008 | Como empleado, quiero registrar días adicionales. | 1. Cero o más. 2. No negativos. 3. Se muestran en el recibo. 4. Se usan para el descuento. |
| PBI009 | Como empleado, quiero descuentos por días adicionales para incentivar la continuidad. | 1. 2 % sobre el valor total de los días adicionales *(corregido, ver H-01)*. 2. Se calcula antes del 5 % del establecimiento *(corregido, ver H-02)*. 3. Se muestra el valor. 4. Se refleja en el total. 5. Aparece en el recibo. |
| PBI010 | Como empleado, quiero calcular el total a pagar. | 1. Considera base, descuentos e incrementos. 2. Respeta el orden de las reglas. 3. Moneda local. 4. No se calcula con datos faltantes. 5. Aparece en el recibo. |
| PBI011 | Como empleado, quiero ver el detalle de descuentos. | 1. Total de descuentos. 2. Incluye establecimiento. 3. Incluye días adicionales. 4. Visible en el recibo. |
| PBI012 | Como empleado, quiero ver los incrementos. | 1. Total de incrementos. 2. Incluye domicilio. 3. Si no hay, muestra 0. 4. Aparece en el recibo. |
| PBI013 | Como empleado, quiero generar e imprimir el recibo. | 1. Nombre. 2. Modalidad. 3. Equipos. 4. Días iniciales y adicionales. 5. Descuentos, incrementos y total. 6. Permite imprimir. |
| PBI014 | Como empleado, quiero validar los datos de entrada. | 1. Nombre informado (máx. 100 caracteres, ver H-03). 2. Equipos ≥ 2. 3. Días iniciales > 0. 4. Días adicionales ≥ 0. 5. Sin cálculo ni recibo si hay errores. |

> Las notas *(corregido)* vienen del informe de hallazgos: el texto original de PBI009 contradecía la descripción funcional y la hoja de referencia del taller.
