# INFO081-Grupo-NA-ProyectoTrenes: Simulador de Tráfico Ferroviario

Este proyecto implementa un simulador de eventos discretos para modelar el tráfico ferroviario, la gestión de la demanda de pasajeros y la ocupación de vías en tiempo real.

---

## Integrantes

* Gabriel Rivas (`GabielOpeth`)
* Álvaro Yáñez (`YurQlito` y `jouleshet`)
* Cristian Vargas (`Zkyeeer`)
* Matías Santana (`StarChaser` y `msantnalagos9632-creator`)
* Kevin Sobarzo (`Kewinaso`)

---

## Características y Requisitos Funcionales (RF)

| RF | Descripción | Estado |
| :--- | :--- | :--- |
| **RF04** | Carga de datos iniciales (Anexo 1). | **Implementado** |
| **RF07** | Indicadores de ocupación (congestión) y tiempo de espera. | **Parcialmente Implementado** |
| **RF08** | Persistencia de datos mediante archivos JSON. | **Implementado** |
| **RF09** | Línea de tiempo de eventos. | Futuro |

### Indicadores Implementados (RF07)

1.  **Ocupación de trenes en tiempo real:** Porcentaje de capacidad utilizada, calculado como `(personas_viajando / capacidad_total_de_trenes)`.
2.  **Estación Crítica:** Estación con la mayor cantidad de pasajeros esperando.

### Decisiones de Diseño

#### Funcionamiento de Vagones y Capacidad
La capacidad total de un tren (`capacidad_total`) se define a partir de su atributo `vagones`:
* Si `vagones` es una **lista** (ej: `[100, 100]`), la capacidad es la suma de los valores de la lista (capacidad específica por vagón).
* Si `vagones` es un **entero**, la capacidad es el valor del entero multiplicado por 50 (capacidad de un vagón estándar).

#### Lógica de Pasajeros y Movimiento
* **Subida de Pasajeros:** Los trenes dan prioridad a los pasajeros que están esperando en la estación y cuyo `origen_id` es el ID de la estación actual. La cantidad máxima a subir es `min(esperando, capacidad)`.
* **Bajada de Pasajeros:** Cuando un tren llega a una estación, todos los pasajeros que están `viajando` y cuyo `destino_id` coincide con la estación actual son marcados como `viajando=False` y `en_estacion=False` (fin de viaje).

---

## Componentes Comunitarios Utilizados

El proyecto utiliza los siguientes submódulos (`git submodule`):

1.  **`ppdc-timed-generator`**: Para la generación de la demanda de pasajeros (`logic/gestor_entidades.py`) utilizando un **`GeneradorUniforme`**.
2.  **`ppdc-event-manager`**: Para la administración de eventos discretos (`logic/motor_simulacion.py`) mediante la clase **`LineaDeEventos`**.

---

## Cómo Ejecutar el Proyecto

El proyecto **debe** ejecutarse desde un entorno virtual (`venv`) para evitar problemas de permisos de sistema y asegurar que los submódulos instalados sean reconocidos.

### 1. Preparación del Entorno

1.  **Inicializar y actualizar submódulos:**
    ```bash
    git submodule init
    git submodule update
    ```

2.  **Crear y activar el Entorno Virtual (venv):**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

### 2. Instalación de Paquetes

Con el entorno virtual activo (`(venv)` visible), instale los submódulos como paquetes editables:

1.  **Instalar el generador de demanda:**
    ```bash
    pip install -e demanda-generator/
    ```

2.  **Instalar el gestor de eventos:**
    ```bash
    pip install -e eventos-admin/
    ```

### 3. Ejecución del Simulador

Inicie la aplicación principal:

```bash
python main.py