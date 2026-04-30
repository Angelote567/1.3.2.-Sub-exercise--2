# 📋 Guía de ejecución paralela – Proyecto HR Database

**Asignatura:** Minería de Datos y Big Data
**Sub-exercise #2:** Generación distribuida de la base de datos sintética HR

---

## 🎯 ¿Qué vamos a hacer?

Cada uno de vosotros va a ejecutar el mismo programa en Python en **vuestra propia
máquina virtual de Azure**. Todos los datos generados se enviarán a una **única
base de datos MongoDB centralizada** que está alojada en la VM de **[TU NOMBRE]**.

El objetivo es repartir el trabajo entre los 10 para generar **1.500.000 empleados
totales (150.000 cada uno)**.

---

## 📑 Tabla de asignación de offsets

⚠️ **MUY IMPORTANTE:** cada persona tiene un `ID_OFFSET` distinto. Esto evita que
dos personas generen empleados con el mismo identificador. Localiza tu nombre en
la tabla y **anótate tu valor**:

| Compañero  | `ID_OFFSET`   | `N_OUTPUTS` | Rango de secuencias generadas |
|------------|---------------|-------------|-------------------------------|
| jorge      | 0             | 150000      | 1 – 150.000                   |
| bea        | 200000        | 150000      | 200.001 – 350.000             |
| derya      | 400000        | 150000      | 400.001 – 550.000             |
| enrique    | 600000        | 150000      | 600.001 – 750.000             |
| revuelta   | 800000        | 150000      | 800.001 – 950.000             |
| carla      | 1000000       | 150000      | 1.000.001 – 1.150.000         |
| carlos     | 1200000       | 150000      | 1.200.001 – 1.350.000         |
| jotacuatro | 1400000       | 150000      | 1.400.001 – 1.550.000         |
| blanca     | 1600000       | 150000      | 1.600.001 – 1.750.000         |
| angel      | 1800000       | 150000      | 1.800.001 – 1.950.000         |

> Cada bloque tiene 200.000 hueco para que sobre margen. Si necesitáis generar
> más de 150.000, podéis subirlo hasta 199.999 sin tocar el offset.

---

## 🔌 Paso 1 – Conectarte a tu VM de Azure por SSH

### 1.1. Ir al portal de Azure Lab Services

Abre el navegador en https://labs.azure.com y entra con tu cuenta de la USJ.

### 1.2. Encender tu VM

En la lista de VMs, asegúrate de que **tu VM está encendida** (interruptor azul
en posición "En ejecución"). Si está apagada, dale al interruptor para encenderla
y espera ~30 segundos.

### 1.3. Obtener el comando SSH

Al lado de tu VM hay un icono pequeño con forma de monitor 🖥️. Haz click ahí.
Aparecerá una ventana como esta:

![Ventana de conexión SSH de Azure](ejemplo_ssh_azure.png)

El comando que ves ahí (la línea que empieza por `ssh -p <puerto>`) es **único
para tu VM**. Cópialo entero pulsando "Copiar".

> ⚠️ **Atención:** el puerto (el número después de `-p`) es DIFERENTE para cada
> persona. No copies el puerto del compañero. Usa siempre el que aparece en TU
> ventana de Azure.


# ANTES QUE SALGAIS DE LA MAQUINA PRIMERO QUE TODO 
Ejecutar estos comandos
```bash
cd ~
sudo rm -r hr_database_project
```
Esto es para lo que lo habiais instalado antes y da error 

### 1.4. Abrir terminal y conectar

**Si usas Windows:**
1. Abre **PowerShell** (botón Inicio → escribe "PowerShell" → Enter)
2. Pega el comando que copiaste (click derecho dentro de la terminal pega)
3. Pulsa Enter

**Si usas macOS/Linux:**
1. Abre la **Terminal**
2. Pega el comando y pulsa Enter

La primera vez te pedirá si confías en el host: escribe `yes` y Enter.
Después te pedirá la **contraseña** de tu usuario `usj`. Escríbela (no se ve
mientras la escribes, es normal) y Enter.

Si todo va bien verás un prompt parecido a:

```
usj@ML-RefVm-XXXXXX:~$
```

Estás dentro de tu VM. 🎉

---

## 📦 Paso 2 – Recibir y descomprimir el proyecto

[TU NOMBRE] os pasará un archivo llamado `hr_database_project.zip`.

### 2.1. Subir el zip a tu VM

Hay 2 formas. Elige la que te resulte más cómoda:

#### Opción A: con `scp` desde tu PC (recomendada)

Abre **otra ventana de PowerShell/Terminal** (deja la del SSH abierta) y ejecuta,
sustituyendo `<PUERTO>` y `<HOST>` por los tuyos (los del comando SSH que has
usado antes):

```bash
scp -P <PUERTO> hr_database_project.zip usj@<HOST>:~/
```

Ejemplo real (con datos ficticios):
```bash
scp -P 52172 hr_database_project.zip usj@ml-lab-33128d24-fd64-425a-8425-be87e853dede.westeurope.cloudapp.azure.com:~/
```

⚠️ **Cuidado:** en `scp` la `-P` va en **mayúscula**. En `ssh` va en **minúscula**.
Es un error muy común.

Te pedirá la contraseña de la VM y empezará a copiar.

#### Opción B: con WinSCP (interfaz gráfica)

Si te lías con la línea de comandos:

1. Descarga WinSCP gratis desde https://winscp.net
2. Crea una conexión nueva con:
   - Protocolo: `SCP`
   - Host: el host de tu comando SSH (la parte después de `usj@`)
   - Puerto: el número después de `-p` en tu comando SSH
   - Usuario: `usj`
   - Contraseña: la de tu VM
3. Conecta y arrastra `hr_database_project.zip` a la carpeta `/home/usj/`

### 2.2. Descomprimir

Vuelve a la ventana del SSH (la que dice `usj@ML-RefVm-XXX:~$`) y ejecuta:

```bash
cd ~
unzip hr_database_project.zip
```

Si te dice `unzip: command not found`:

```bash
sudo apt install unzip -y
unzip hr_database_project.zip
```

Comprueba que se descomprimió correctamente:

```bash
ls
```

Tienes que ver una carpeta llamada `project` (o similar). Entra:

```bash
cd hr_database_project
cd project
ls
```

Tienes que ver:

```
coherence_rules.py  config.py  csv_loader.py  data  generators
helpers.py  mongodb_client.py  pipeline.py  README.md  requirements.txt
```

Si ves esos archivos, vamos bien.

---

## 🔧 Paso 3 – Preparar el entorno Python

### 3.1. Actualizar el sistema (recomendado)

```bash
sudo apt update
```

Te pedirá la contraseña una vez. Tarda ~30 segundos. Cuando termine, sigue.

### 3.2. Instalar el módulo de entornos virtuales

```bash
sudo apt install python3-venv -y
```

(El `-y` hace que acepte todo automáticamente.)

### 3.3. Crear el entorno virtual

Asegúrate de estar dentro de la carpeta `project`:

```bash
cd ~/hr_database_project/project
```

Y crea el entorno:

```bash
python3 -m venv venv
```

No verás ningún mensaje, eso significa que ha funcionado. Aparecerá una carpeta
nueva llamada `venv/`.

### 3.4. Activar el entorno virtual

```bash
source venv/bin/activate
```

Verás que tu prompt cambia y aparece `(venv)` al principio:

```
(venv) usj@ML-RefVm-XXXXXX:~/project$
```

Eso significa que estás dentro del entorno virtual. **Cada vez que cierres y
vuelvas a abrir la terminal, tendrás que repetir este paso (`source venv/bin/activate`)
antes de ejecutar el pipeline.**

### 3.5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

Tarda ~30 segundos. Verás que descarga `pymongo`. Cuando termine, sin errores
en rojo, está listo.

Verifica que se instaló bien:

```bash
python3 -c "import pymongo; print(pymongo.__version__)"
```

Te tiene que mostrar un número de versión (ej: `4.6.1`).

---

## ✏️ Paso 4 – Configurar tu offset

Este es el paso más importante. Cada uno tiene que cambiar **2 líneas** en el
archivo `config.py`.

### 4.1. Abrir config.py con nano

```bash
nano config.py
```

Se abre un editor de texto. Verás el contenido del archivo.

### 4.2. Localizar las líneas a modificar

Busca estas dos líneas (están al principio del archivo):

```python
N_OUTPUTS = 1000
```

y más abajo:

```python
ID_OFFSET = 0
```

### 4.3. Modificarlas con TUS valores

Mira la **tabla de asignación de offsets** del principio de este documento. Pon
los valores que te corresponden. Por ejemplo, si eres **bea**:


## TAMBIEN HACE FALTA CAMBIAR RANDOM SEED 
```python
RANDOM_SEED == EL NUMERO QUE OS SALGA DEL RABO
```

```python
N_OUTPUTS = 150000
```

```python
ID_OFFSET = 200000
```

⚠️ **NO toques ninguna otra línea del archivo.** Solo esos dos números.

### 4.4. Guardar y salir

1. Pulsa **`Ctrl + O`** (la letra O, no cero) → te pregunta el nombre del archivo
   abajo, deja `config.py` y pulsa **Enter**
2. Pulsa **`Ctrl + X`** para salir

### 4.5. Verificar que los cambios se guardaron

```bash
grep -E "N_OUTPUTS|ID_OFFSET" config.py
```

Tiene que mostrarte tus valores. Por ejemplo, si eres bea:

```
N_OUTPUTS = 150000
ID_OFFSET = 200000
```

Si no salen tus valores, repite el paso 4.

---

## 🚀 Paso 5 – Ejecutar el pipeline

⚠️ **Antes de lanzar:** avisa a [TU NOMBRE] por el grupo de WhatsApp para
coordinar las ejecuciones (idealmente que no haya 5 personas insertando a la
vez para que MongoDB no se sature).

Asegúrate de que tienes el venv activado (verás `(venv)` en tu prompt):

```bash
cd ~/project
source venv/bin/activate
```

Y lanza:

```bash
python3 pipeline.py
```

Verás algo así:

```
13:24:01 | INFO    | csv_loader     | Cargando CSVs desde /home/usj/project/data/csvs
13:24:01 | INFO    | csv_loader     | Cargados 31 CSVs correctamente
13:24:01 | INFO    | mongodb_client | Conectado a MongoDB: mongodb://10.0.64.11:27017 / DB: hr_database / Col: employees
13:24:01 | INFO    | mongodb_client | Documentos ya existentes en la coleccion: 450000
13:24:01 | INFO    | pipeline       | Iniciando generacion de 150000 empleados (batch=100)
13:24:02 | INFO    | pipeline       |   Progreso: 100/150000 (520 empleados/s)
13:24:02 | INFO    | pipeline       |   Progreso: 200/150000 (525 empleados/s)
...
13:28:45 | INFO    | pipeline       | GENERACION COMPLETADA en 284.1s
13:28:45 | INFO    | pipeline       |   Total insertados: 150000
13:28:45 | INFO    | pipeline       |   Empleados con violaciones: 0 (0.00%)
```

**Tarda unos 4-5 minutos** dependiendo de la velocidad de tu VM y de cuántos
estéis insertando a la vez.

Cuando termine, **avisa por el grupo** con el número de empleados insertados.

---

## ❌ Errores frecuentes y cómo solucionarlos

### "Connection timed out" o no conecta a MongoDB

Tu VM no llega a `10.0.64.11`. Comprueba que sí lo alcanza:

```bash
ping 10.0.64.11
```

Si no responde después de 5 segundos, corta con `Ctrl+C` y avisa a [TU NOMBRE].
Posiblemente el MongoDB está apagado o tu VM no está en la misma red.

### "ModuleNotFoundError: No module named 'pymongo'"

No has activado el venv. Ejecuta:

```bash
source venv/bin/activate
```

Y vuelve a lanzar `python3 pipeline.py`.

### "externally-managed-environment" al hacer `pip install`

Estás intentando instalar fuera del venv. Repite los pasos 3.3 y 3.4 antes de
intentar instalar.

### "DuplicateKeyError" durante la inserción

Tu `ID_OFFSET` colisiona con el de otro compañero (estáis usando el mismo o
alguien lo modificó por error). Verifica con `grep`:

```bash
grep "ID_OFFSET" config.py
```

Si el valor no coincide con el de la tabla, vuelve al paso 4 y corrígelo.

### "Permission denied (publickey,password)" al hacer SSH

Estás escribiendo mal la contraseña o el usuario. El usuario es `usj`. La
contraseña es la que te dio el profe al darte la VM.

### El pipeline va MUY lento (menos de 100 empleados/s)

Es probable que MongoDB esté saturado porque hay varios compañeros insertando
a la vez. Espera a que termine alguno y prueba de nuevo. O coordínate por el
grupo para no solapar ejecuciones.

### Cierra mi terminal y pierdo la conexión

Es normal si el SSH lleva mucho tiempo inactivo. Vuelve a conectar con el
comando del paso 1.4 y reactiva el venv:

```bash
cd ~/project
source venv/bin/activate
```

No tienes que repetir los pasos 2, 3 ni 4 (todo eso queda guardado en la VM).

---

## 📞 Coordinación

- **Coordinador:** [TU NOMBRE]
- **MongoDB centralizado:** `10.0.64.11:27017`
- **Antes de ejecutar:** avisar por el grupo de WhatsApp
- **Después de ejecutar:** confirmar el número de empleados insertados

---

## 🧾 Resumen rápido (cheat sheet para los más espabilados)

```bash
# 1. Conectar (con TU comando SSH de Azure)
ssh -p <PUERTO> usj@<HOST>

# 2. Subir y descomprimir
# (con scp -P <PUERTO> ... desde tu PC)
cd ~ && unzip hr_database_project.zip && cd project

# 3. Setup
sudo apt update
sudo apt install python3-venv -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configurar offset
nano config.py    # editar N_OUTPUTS e ID_OFFSET segun la tabla

# 5. Ejecutar
python3 pipeline.py
```

---

*Documento de coordinación – Sub-exercise #2 – Minería de Datos y Big Data – USJ
2025-2026.*
