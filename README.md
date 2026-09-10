# Proyecto-eXperience
La empresa MyTech quiere pasar del sistema eléctrico convencional a uno más ecológico, implementaron paneles solares en sus dos edificios principales. Cada edificio tiene un objetivo mínimo de generación de energía diferente, que el sistema deberá controlar. 

# Problemática: 

Al ser una implementación nueva para la empresa, resulta que no tenían un sistema de control para la energía entonces nos llamaron a nosotros para que lo implementemos. Les dijimos que lo podemos hacer, pero les preguntamos qué otras funcionalidades les gustaría que tuviera el sistema.  

# Implementación al sistema: 

Querían principalmente analizar y controlar la energía generada en ambos edificios de forma semanal y mensual. Para esta primera etapa, el sistema administrará un mes por vez, compuesto por 4 semanas de 5 días hábiles cada una (lunes a viernes), sin representar el calendario real. El prototipo trabajará con 2 edificios × 4 semanas × 5 días correspondientes al mes de análisis seleccionado. El usuario seleccionará el mes de análisis una única vez al iniciar la ejecución, y las matrices de ambos edificios corresponderán exclusivamente a ese mes; en esta etapa no existe un historial que permita cambiar de mes y conservar los datos previos. 

La información se representará mediante una matriz por edificio, donde las filas corresponden a las semanas (1 a 4) y las columnas a los días (lunes a viernes): producción_edificio_A[semana][dia] y producción_edificio_B[semana][dia]. Cada celda contiene únicamente un dato numérico que representa los kWh generados ese día (por ejemplo, un valor de 250 significa que el edificio produjo 250 kWh ese día). Para mantener la matriz numérica homogénea, se utilizará el valor -1 para representar un día sin medición cargada, mientras que 0 o más representa la generación registrada en kWh ese día. El usuario nunca podrá ingresar valores negativos; -1 será únicamente un valor interno del sistema. 

Para registrar o actualizar la energía generada en un día determinado, el usuario deberá seleccionar el edificio, la semana y el día, e ingresar el nuevo valor de energía generada. Si ya existe un valor cargado para ese edificio, semana y día, el nuevo valor reemplazará al anterior, ya que cada celda representa una única medición diaria y no valores acumulables. 

El sistema deberá validar como mínimo: edificio válido, código de edificio válido (ED-A o ED-B), mes válido, semana válida, día válido, dato numérico, generación mayor o igual a 0, opción de menú válida y disponibilidad de datos suficientes para responder la consulta solicitada. Ningún error de validación debe provocar el cierre del programa. 

Cada edificio tiene un objetivo mínimo de generación semanal: el edificio A debe generar al menos 1000 kWh por semana y el edificio B al menos 800 kWh, comparando siempre la suma de los cinco días de la semana. Si la producción semanal es menor al objetivo, el sistema mostrará el mensaje: “Producción inferior al objetivo semanal. Se recomienda realizar una revisión.” 

En lugar de un porcentaje de días que fallaron, se calculará el porcentaje de cumplimiento semanal como (producción semanal / objetivo semanal) × 100. Por ejemplo: “Edificio A: 92 % del objetivo semanal”. 

El sistema calculará el día con mayor y menor generación de una semana, la semana con mayor generación de cada edificio (de forma independiente, sin sumar ambos edificios) y el edificio con mayor generación semanal, indicando siempre dónde ocurrió. Para comparar la generación entre el Edificio A y el Edificio B, o para determinar cuál de los dos generó más o menos, se utilizarán siempre períodos equivalentes y completos, es decir, las mismas semanas y sin semanas incompletas en ninguno de los dos edificios. Si existieran empates (por ejemplo, dos días, dos semanas o ambos edificios con el mismo valor máximo o mínimo), el sistema informará todos los valores empatados en lugar de asumir un único resultado. Por ejemplo: “Máxima generación: 310 kWh – Edificio A – Semana 2 – Miércoles”. 

Se calcularán el promedio diario de generación de una semana (total de la semana completa dividido por 5) y el promedio semanal de generación de cada edificio, considerando únicamente semanas completas. Si una semana todavía tiene algún día con valor -1 (no cargado), el sistema no informará si cumplió o no cumplió el objetivo semanal: indicará explícitamente que la semana está incompleta y la excluirá de los rankings y de los conteos de cumplimiento, en lugar de calcular el total, el promedio o el porcentaje de cumplimiento como si estuviera completa. Esto es especialmente relevante para la alerta de objetivo semanal, que deberá aclarar cuando el resultado corresponda a una semana incompleta. 

Se contará además la cantidad de semanas que alcanzaron el objetivo mínimo y la cantidad de semanas que no lo alcanzaron, excluyendo de ambos conteos a las semanas incompletas. 

El sistema permitirá consultar un edificio por código (ED-A o ED-B), mostrando su producción registrada, total semanal, promedio y porcentaje de cumplimiento respecto del objetivo. 

También se generará, de forma independiente para cada edificio, un ranking de sus semanas ordenadas de mayor a menor generación total (utilizando funciones lambda), excluyendo las semanas incompletas, pudiendo mostrarse mediante slicing, por ejemplo, las 3 semanas de mayor generación de ese edificio (Top 3). El mismo criterio —independiente por edificio, sin sumar ambos, y sin considerar semanas incompletas— se aplica al Top 3. 

Se utilizarán tuplas para la información fija del sistema, por ejemplo los días de la semana (“Lunes”, “Martes”, “Miércoles”, “Jueves”, “Viernes”), los objetivos semanales de cada edificio relacionados por posición (1000, 800) y los doce meses del año, validando que la selección del mes de análisis sea una de ellas. Se utilizará comprensión de listas, por ejemplo, para generar la lista de semanas que no alcanzaron el objetivo semanal. Asimismo, se utilizará una lista homogénea para almacenar los totales semanales de generación de cada edificio antes de ordenarlos para construir el ranking. 

Quedan fuera del alcance de esta etapa el uso de archivos, bases de datos o cualquier otro tipo de persistencia, la lectura automática de paneles solares o sensores reales, la captura de datos en tiempo real, la autenticación de usuarios, el mantenimiento de un histórico de varios meses y el desarrollo de una aplicación web o móvil. Toda la información permanecerá únicamente en memoria durante la ejecución del programa. 