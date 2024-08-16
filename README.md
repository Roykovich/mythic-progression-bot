# Mythic Progression bot

## Instalación
Ve al directorio del bot
```bash
$ cd la-carpeta-del-bot
$ python3 -m venv bot-env
```
Activa el entorno virtual

- En Windows:
    ```bash
    $ bot-env\Scripts\activate.bat
    ```
- En Linux:

    ```bash
    $ source bot-env/bin/activate
    ```
Descarga la libreria de discord y requests con PyPI
```bash
pip install -U discord.py requests
```

## Todo
- [x] Al cancelar aplicacion, se deben eliminar de la lista de aceptados
- [x] Al cancelar el booster, mensaje ephemeral de cancelacion de la aplicacion
- [x] Autocompletado en las IDs del comando de aceptar aplicantes
- [x] Implementacion de la API del monedero
- [x] Agregar comando de registrar usuario con el id del monedero
- [x] Agregar caracteristica: Si la orden fue creada por un supplier, a la hora de acreditar el pago se debe utilizar el monto en la DB y en caso en que los calculos hecho por ella no sean correctos, llamar al staff (SOLVED: UTILIZAR EL MISMO COMANDO pay_booster)
- [ ] Agregar comando para añadir personajes con raiderio a la DB (agregar el color o emoji? dependiendo del raiderio para reeamplazar la funcion ya existe)
- [ ] Puntos de booster a traves de la API de googlesheets y cantidad de ordenes completadas con la API de googlesheets
- [ ] Agregar al comando register insercion de datos en googlesheets (son dos spreadsheets, consultar con Miguel)
- [ ] Comando para revisar el perfil como Booster (donde se pueden ver los Booster Points y los personajes registrados)
- [ ] Crear sistema para verificar el progreso de la orden. Ejemplo: Si son 4 runs, que al enviar con un mensaje (o un slash command) una imagen, el bot detecte que es una captura del progreso de la 1era, 2da ... runs
- [ ] Agregar un estado a la view de los booster, para revertir el boton de full de ser necesario la busqueda de otro booster
- [ ] Agregar botones para eliminar, actualizar datos de boosters (wallet id y esas cosas)
- [ ] Crear comandos para miticas (ya creado), raids, logros y otros (TBD)
- [ ] Repartir el pago entre la cantidad de boosters en raid y en mitica (añadir verificacino de irregularidades a la hora de realizar el pago)

## Refactors
- [ ] Funciones modulares para los botones full y los de aplicacion de booster
- [ ] Funciones para aplicantes y ordenes de la DB
- [ ] Agregar documentacion y comentarios
- [ ] Cambiar el naming. Hay al menos 3 constantes: Staff, Booster y Order
- [ ] Ver si el SelectMenu funciona como dropdown para los botones en el embed de los booster para DPS, TANK y HEALER (para elegir especializacion como Paladin Retry, Holy o Protection) SI SE PUEDE, SE CREARIA UN SEGUNDO EMBED DONDE AGARRE LOS DATOS DE LA DB DEL USUARIO EN CUESTION
- [ ] Crear un .env_example
- [ ] Agregar mensaje de feedback a la hora de darle a full
- [ ] Agregar busqueda elastica. Por ejemplo: Cloth, leather, mail and plate para la clase

## Long Term ToDos
- [ ] Comando de remake de la orden. Motivo: Si un booster llega a salirse, se crea una nueva orden pero que sea asi: <orden_id>-<1, 2 , 3 ... n>. Esto tendria la funcionalidad que a la hora de acreditar a los boosters a cada uno le toque su parte correspondiente y evitar errores a la hora del pago automatizado.