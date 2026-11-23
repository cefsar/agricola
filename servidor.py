
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from gpiozero import Motor
import uvicorn

app = FastAPI(title="Robot Agrícola")

# Motores conectados al L298N
motor_izquierdo = Motor(forward=17, backward=18, pwm=False)
motor_derecho = Motor(forward=22, backward=23, pwm=False)

sistema_activo = False
movimiento = "DETENIDO"


def detener_motores():
    motor_izquierdo.stop()
    motor_derecho.stop()


def ejecutar_movimiento(accion):
    if accion == "adelante":
        motor_izquierdo.forward()
        motor_derecho.forward()

    elif accion == "atras":
        motor_izquierdo.backward()
        motor_derecho.backward()

    elif accion == "izquierda":
        motor_izquierdo.backward()
        motor_derecho.forward()

    elif accion == "derecha":
        motor_izquierdo.forward()
        motor_derecho.backward()

    else:
        detener_motores()


@app.get("/", response_class=HTMLResponse)
def inicio():
    estado = "ACTIVO" if sistema_activo else "APAGADO"
    color = "green" if sistema_activo else "red"

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Robot Agrícola</title>
        <style>
            body {{
                font-family: Arial;
                text-align: center;
                background: #eeeeee;
                padding: 30px;
            }}
            button {{
                padding: 18px;
                margin: 6px;
                font-size: 18px;
                color: white;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                touch-action: none;
            }}
            .encender {{ background: green; }}
            .apagar {{ background: red; }}
            .movimiento {{ background: #2563eb; width: 90px; }}
            .detener {{ background: #444; width: 90px; }}
        </style>
    </head>
    <body>
        <h1>ROBOT AGRÍCOLA</h1>

        <h2 style="color:{color}">SISTEMA {estado}</h2>
        <p>Movimiento: {movimiento}</p>

        <button class="encender" onclick="enviar('/encender')">
            ENCENDER
        </button>

        <button class="apagar" onclick="enviar('/apagar')">
            APAGAR
        </button>

        <hr>

        <h3>CONTROL DE MOVIMIENTO</h3>

        <div>
            <button class="movimiento" data-mov="adelante">▲</button>
        </div>

        <div>
            <button class="movimiento" data-mov="izquierda">◀</button>
            <button class="detener" onclick="enviar('/detener')">■</button>
            <button class="movimiento" data-mov="derecha">▶</button>
        </div>

        <div>
            <button class="movimiento" data-mov="atras">▼</button>
        </div>

        <script>
            async function enviar(ruta) {{
                try {{
                    const respuesta = await fetch(ruta, {{method: "POST"}});
                    const datos = await respuesta.json();

                    if (datos.sistema) {{
                        document.querySelector("h2").textContent =
                            datos.sistema;
                    }}

                    if (datos.movimiento) {{
                        document.querySelector("p").textContent =
                            "Movimiento: " + datos.movimiento;
                    }}
                }} catch (error) {{
                    console.error(error);
                }}
            }}

            document.querySelectorAll("[data-mov]").forEach(boton => {{
                const accion = boton.dataset.mov;

                boton.addEventListener("pointerdown", event => {{
                    event.preventDefault();
                    boton.setPointerCapture(event.pointerId);
                    enviar("/mover/" + accion);
                }});

                boton.addEventListener("pointerup", event => {{
                    event.preventDefault();
                    enviar("/detener");
                }});

                boton.addEventListener("pointercancel", () => {{
                    enviar("/detener");
                }});

                boton.addEventListener("lostpointercapture", () => {{
                    enviar("/detener");
                }});
            }});

            window.addEventListener("blur", () => {{
                enviar("/detener");
            }});
        </script>
    </body>
    </html>
    """


@app.post("/encender")
def encender():
    global sistema_activo

    sistema_activo = True

    return {
        "sistema": "SISTEMA ACTIVO",
        "movimiento": movimiento
    }


@app.post("/apagar")
def apagar():
    global sistema_activo, movimiento

    sistema_activo = False
    movimiento = "DETENIDO"

    detener_motores()

    return {
        "sistema": "SISTEMA APAGADO",
        "movimiento": movimiento
    }


@app.post("/mover/{accion}")
def mover(accion: str):
    global movimiento

    if not sistema_activo:
        detener_motores()
        movimiento = "DETENIDO"

        return {
            "sistema": "SISTEMA APAGADO",
            "movimiento": movimiento
        }

    if accion not in ["adelante", "atras", "izquierda", "derecha"]:
        detener_motores()
        movimiento = "DETENIDO"

        return {
            "sistema": "SISTEMA ACTIVO",
            "movimiento": movimiento
        }

    ejecutar_movimiento(accion)
    movimiento = accion.upper()

    return {
        "sistema": "SISTEMA ACTIVO",
        "movimiento": movimiento
    }


@app.post("/detener")
def detener():
    global movimiento

    detener_motores()
    movimiento = "DETENIDO"

    return {
        "sistema": "SISTEMA ACTIVO" if sistema_activo else "SISTEMA APAGADO",
        "movimiento": movimiento
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
