# sms-api

El script conecta con la aplicación de Google Play SMS Gateway y realiza lo soguiente:

1. Lee los útlimos 100 mensajes recibidos en el celular.
2. ELimina los mensajes de salida, conserva solamente los de entrada.
2. Filtra solamente el útlimo mensaje recibido por cada número de celular.
3. Lós únicos datos relevantes son latitude y longitude, por lo cual se eliminan los demás.
4. Se convierte de tipo son a tipo lista para poderlos insertar a base de datos.
5. Se insertar los valores a la base de datos.
6. Se generan archivo log de todo el proceso.
