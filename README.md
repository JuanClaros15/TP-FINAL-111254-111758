# TP-FINAL-111254-111758

Repositorio para el TP final de la materia Introducción al Desarrollo de Software

Desarrollo de la aplicación:

Si existe una cuenta en la base de datos:
1. Relleno del formulario de inicio de sesión.
2. Se envían los datos ingresados mediante una solicitud POST al servidor.
3. La solicitud llega al servidor y es analizada por la ruta del login.
4. En esta ruta se compara el nombre de usuario y la contraseña con los almacenados en la base de datos:
   a. Si hay una coincidencia con los datos almacenados, se redirige al usuario a la página principal y se inicia sesión.
   b. Si no hay coincidencia, se vuelve al login.
5. Una vez iniciada la sesión, se carga la página principal.

Si no existe una cuenta en la base de datos:
1. Se ingresa al enlace del login que sirve para crear una cuenta, lo que redirige al usuario a la ruta donde se encuentra la página de registro.
2. Se rellena el formulario de registro para enviarlo con una solicitud POST.
3. El servidor recibe la solicitud y procede a analizarla.
4. Se extraen los datos (con `request.form`) y se hashea la contraseña (para más seguridad).
5. Con los datos extraídos, se crea una instancia y se agrega a la sesión de la base de datos.
6. Una vez realizado el proceso de registro, se redirige al usuario al login.

Cambio de contraseña:
1. En caso de olvidar la contraseña, se puede restablecer utilizando el enlace de recuperar contraseña, el cual redirige a la ruta de recuperación.
2. Se rellena el formulario y se crea la solicitud POST con los datos ingresados.
3. La solicitud llega al servidor, donde se extraen los datos.
4. Se busca en la base de datos un usuario que tenga el mismo mail y nombre de usuario:
   a. Si existe el usuario, se realiza el cambio de contraseña en la base de datos.
   b. En caso de no existir, se recarga la página.

Página principal, componentes:
- Botón de cerrar sesión: crea una solicitud POST que es recibida por el servidor y cierra la sesión.
- Ordenamiento de tickets: ordena según su estado y prioridad.
- Cargar tickets: para cargar los tickets de cada usuario se realiza una solicitud GET al servidor.
  - En caso de no tener tickets, se muestra un mensaje.
  - En caso de haber tickets, se cargan (son botones).
- Botones dinámicos: para cada ticket se generan dos botones, uno para terminar el ticket y otro para marcar la finalización de la tarea.
- Agregar nuevos tickets:
  1. Para agregar nuevos tickets, se presiona el botón y se muestra una ventana emergente con un formulario.
  2. Se rellena el formulario y se envía. Esto envía al servidor una solicitud FETCH, utilizada para comunicar con el servidor desde el navegador sin necesidad de recargar la página. En este caso, se utiliza ya que mandamos los datos desde una ventana emergente.
  3. El servidor recibe la solicitud, la analiza, extrae los datos importantes y los guarda en la base de datos.
  4. Una vez guardado el ticket, se recarga la página principal.
- El usuario con ID número 1 es el configurado para ser el admin, por lo que tiene ciertos privilegios, como ver todos los tickets.
