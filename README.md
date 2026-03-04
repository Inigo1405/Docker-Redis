# Docker + Redis

El proyecto levanta **3 contenedores** orquestados con Docker Compose que se comunican entre sí en una red interna:

## Estructura del sistema:

### Endpoints de la API

| Método | Ruta      | Descripción                                         |
| ------ | --------- | --------------------------------------------------- |
| GET    | `/`       | Bienvenida y listado de rutas disponibles           |
| GET    | `/health` | Verifica la conexión a PostgreSQL y Redis           |
| GET    | `/visits` | Incrementa y retorna el contador de visitas (Redis) |
| GET    | `/users`  | Lista usuarios (en desarrollo)                      |
| POST   | `/users`  | Crea un usuario (en desarrollo)                     |

### Estructura de archivos

```
Docker-Redis/
├── docker-compose.yml       # Orquestación de los 3 servicios
├── README.md
└── app/
    ├── Dockerfile           # Imagen de la API (Python 3.11-slim)
    ├── main.py              # Lógica de la API Flask
    └── requirements.txt     # Dependencias: Flask, psycopg2, redis
```

## Comandos Docker:

| Comando                                                            | ¿Qué hace?                                                                                     |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `docker -v`                                                        | Muestra la versión de Docker instalada                                                         |
| `docker compose version`                                           | Muestra la versión de Docker Compose instalada                                                 |
| `docker run -it ubuntu bash`                                       | Corre un contenedor Ubuntu de forma interactiva abriendo una terminal bash                     |
| `docker images`                                                    | Devuelve todas las imágenes descargadas en la computadora                                      |
| `docker ps`                                                        | Muestra los contenedores que están corriendo actualmente                                       |
| `docker ps -a`                                                     | Muestra todos los contenedores, incluyendo los detenidos                                       |
| `docker run --name {name} -p 8080:80 nginx:alpine`                 | Corre nginx:alpine con un nombre asignado y mapea el puerto 8080 del host al 80 del contenedor |
| `docker rm {name}`                                                 | Remueve un contenedor (debe estar detenido)                                                    |
| `docker stop {name}`                                               | Detiene un contenedor en ejecución                                                             |
| `docker build -t {name}:{version} .`                               | Construye una imagen a partir del Dockerfile en el directorio actual                           |
| `docker run --name {name} -p 8000:8000 {name_img}:{version}`       | Corre un contenedor con la imagen indicada mapeando el puerto 8000                             |
| `docker container prune`                                           | Elimina todos los contenedores detenidos                                                       |
| `touch {name}.yml` _(Linux)_ / `type nul > {name}.yml` _(Windows)_ | Crea un archivo YAML vacío (ej. docker-compose.yml)                                            |
| `docker compose up --build`                                        | Levanta todos los servicios reconstruyendo las imágenes desde cero                             |
| `docker compose down -v`                                           | Detiene y elimina los contenedores junto con sus volúmenes                                     |
