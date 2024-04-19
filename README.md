# pixelcode

Print QR codes to authorized users.

## Installing

If you only plan on running the Docker containers you can directly jump to [Running using Docker](#using-docker).

### User interface

The user interface can be installed using `npm`. Inside the `front` directory run:
```commandline
npm install
```
### Application server

Dependencies are defined in `pyproject.toml` and `requirements.txt`.
The application server can be installed in a virtual environment. For example using Poetry and in the project root:
```commandline
poetry install
```

## Running

### Using Docker
Both frontend and backend are dockerized. To start them, run in the project directory:
```commandline
docker compose up -d [--build]
```
or
```commandline
docker compose run -d [--build] <frontend | backend>
```
The application is served to `localhost:5173` .

### From source

#### Environment
Create a `.env` file at the root of the cloned repository. See `.env.example` for an example.
The `ALGORITHM` and `SECRET_KEY` keys are used to sign JWT tokens.
Change the value of `SECRET_KEY` to a randomly generated key using for example:
```commandline
openssl rand -hex 32
```
`ORIGINS` and `VITE_API_URL` keys define respectively the URLs where the user interface and the API are accessible.

#### User interface

Start the vite development server using:
```commandline
npm run dev
```

#### Application server
Activate the virtual environment where the server is installed. For example using Poetry and in the project root:
```commandline
poetry shell
```
Then run:
```commandline
uvicorn app.main:api --reload
```

## Details

`Typescript`, `Vite`, `VueJS` frontend, served through `NGINX`. NGIX server running as frontend `Docker` service.
`Python`, `FastAPI` backend, served through `uvicorn`. Uvicorn server running as backend Docker service.

## To do
- Frontend: success/failure screens
- Backend: Structure websocket messages
- Backend: Cleanup pixelcode error handling
- Backend: Printing to Star Micronics SK1-31
- Backend: Cleanup qr codes once they are printed
- Backend: Upgrade employee data save to PostgreSQL database
- Cleanup usage of environment variables
