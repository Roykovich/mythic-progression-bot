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
- [ ] ~~Al cancelar aplicacion, el contador de booster aplicando debe bajar~~
- [ ] ~~Aplicar como team. Idea: Modal donde puedas taggear a las personas que son de tu team. Crear una tabla donde se pueda ver quienes son parte del team, que esta tenga la id de la orden, los id de los taggeados y crear un comando para ver quienes son y asi validarlos y poder aceptarlos~~
- [x] Al cancelar aplicacion, se deben eliminar de la lista de aceptados
- [x] Al cancelar el booster, mensaje ephemeral de cancelacion de la aplicacion
- [x] Autocompletado en las IDs del comando de aceptar aplicantes
- [ ] Verificacion de personajes con raiderio
- [ ] Puntos de booster a traves de la API de googlesheets y cantidad de ordenes completadas con la API de googlesheets
- [x] Implementacion de la API del monedero
- [ ] Implementacion de consulta de saldo al bot. Recomendacion: solamente por DM. Hay un error donde no te muestra los datos actuales. Ver si es que se cachea o esta diseñado de esa manera y me jodi
- [ ] Agregar caracteristica: Si la orden fue creada por un supplier, a la hora de acreditar el pago se debe utilizar el monto en la DB y en caso en que los calculos hecho por ella no sean correctos, llamar al staff
- [ ] Crear sistema para verificar el progreso de la orden. Ejemplo: Si son 4 runs, que al enviar con un mensaje (o un slash command) una imagen, el bot detecte que es una captura del progreso de la 1era, 2da ... runs
- [ ] Agregar un estado a la view de los booster, para revertir el boton de full de ser necesario la busqueda de otro booster

## Refactors
- [ ] Funciones modulares para los botones full y los de aplicacion de booster
- [ ] Funciones para aplicantes y ordenes de la DB
- [ ] Agregar documentacion y comentarios
- [ ] Cambiar el naming. Hay al menos 3 constantes: Staff, Booster y Order
- [ ] Ver si el SelectMenu funciona como dropdown para los botones en el embed de los booster para DPS, TANK y HEALER (para elegir especializacion como Paladin Retry, Holy o Protection)

## Long Term ToDos
- [ ] Comando de remake de la orden. Motivo: Si un booster llega a salirse, se crea una nueva orden pero que sea asi: <orden_id>-<1, 2 , 3 ... n>. Esto tendria la funcionalidad que a la hora de acreditar a los boosters a cada uno le toque su parte correspondiente y evitar errores a la hora del pago automatizado.