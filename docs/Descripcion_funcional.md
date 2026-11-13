# Descripción funcional – ALQUILAPC

## Contexto
La empresa **ALQUILAPC** presta el servicio de alquiler de equipos de cómputo portátiles **por días** (no tiene opción por horas). El valor del alquiler es de **$35.000 por equipo por día**.

## Datos que registra el servicio
1. Nombre del cliente.
2. Número de equipos solicitados (mínimo 2 – RN02, tomado del Product Backlog).
3. Cantidad de días iniciales (mayor a cero).
4. Cantidad de días adicionales (cero o más).
5. Tipo de servicio:
   - En la ciudad
   - Fuera de la ciudad
   - En el establecimiento

## Reglas de negocio
| ID | Regla |
|----|-------|
| RN01 | Valor alquiler = equipos × días × $35.000 |
| RN02 | Cantidad mínima de 2 equipos |
| RN03 | Tipos de servicio: dentro de la ciudad, fuera de la ciudad, dentro del establecimiento |
| RN04 | Fuera de la ciudad: cargo del 5 % sobre el total, aplicado **después** de los descuentos |
| RN05 | En el establecimiento: descuento del 5 % sobre el total |
| RN06 | Si hay días adicionales: descuento del 2 % sobre el **total de los días adicionales** |
| RN07 | El recibo muestra: nombre, opción de alquiler, equipos, días iniciales, días adicionales, descuentos, incrementos por domicilio y valor total |

## Orden de cálculo (validado contra la hoja de referencia del taller)
1. `valor_alquiler = equipos × dias_iniciales × 35.000`
2. `valor_adicional = equipos × dias_adicionales × 35.000`
3. `dto_adicional = 2 % × valor_adicional`
4. `subtotal = valor_alquiler + valor_adicional − dto_adicional`
5. Establecimiento: `dto_establecimiento = 5 % × subtotal`
6. Fuera de la ciudad: `domicilio = 5 % × subtotal`
7. `total = subtotal − dto_establecimiento + domicilio`

### Ejemplo de referencia (5 equipos, 4 días, 3 adicionales)
| Concepto | En la ciudad | Fuera de la ciudad | En el establecimiento |
|---|---:|---:|---:|
| Valor alquiler | 700.000 | 700.000 | 700.000 |
| Valor adicionales (neto) | 514.500 | 514.500 | 514.500 |
| Descuentos | 10.500 | 10.500 | 71.225 |
| Domicilio | 0 | 60.725 | 0 |
| **Total a pagar** | **1.214.500** | **1.275.225** | **1.153.775** |

## Caso de uso: descuentos según el tipo de servicio
- **Actor:** Empleado de ALQUILAPC.
- **Precondición:** datos básicos válidos.
- **Flujo principal:** el sistema calcula el valor base y los adicionales → aplica 2 % a los adicionales si existen → según la modalidad: *establecimiento* aplica 5 % de descuento; *fuera de la ciudad* aplica 5 % de cargo; *dentro de la ciudad* no aplica ninguno → genera la factura.
- **Flujo alterno:** datos inválidos → el sistema muestra los errores y no genera factura.
- **Poscondición:** recibo generado con el detalle de descuentos e incrementos.
