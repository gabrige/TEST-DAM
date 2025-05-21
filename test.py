import streamlit as st
import json
import random

# Cargar preguntas desde archivo JSON
def cargar_preguntas(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        return json.load(f)

# Diccionario de asignaturas y archivos asociados
asignaturas = {
    "Programación Multimedia y Dispositivos Móviles": "pmdm.json",
    "Sistemas de Gestión Empresarial": "sge.json",
    "Diseño de Interfaces": "di.json",
    "Acceso a Datos": "ad.json",
    "Programación de Servicios y Procesos": "psp.json"
}

# Configuración de la app
st.set_page_config(page_title="Test DAM", layout="centered", page_icon="🧠")
st.title("📘 Test para estudiar DAM")

# Selector de asignatura
asignatura = st.selectbox("Selecciona una asignatura", list(asignaturas.keys()))

# Detectar cambio de asignatura y reiniciar preguntas si ha cambiado
asignatura_actual = asignatura
if "asignatura_anterior" not in st.session_state:
    st.session_state.asignatura_anterior = asignatura_actual

if st.session_state.asignatura_anterior != asignatura_actual:
    st.session_state.asignatura_anterior = asignatura_actual
    st.session_state.pop("preguntas_random", None)

# Reinicio manual del test
if st.button("🔄 Reiniciar test"):
    st.session_state.pop("preguntas_random", None)
    st.experimental_rerun()

# Cargar preguntas y mantenerlas en sesión
if "preguntas_random" not in st.session_state:
    # Cargar preguntas y eliminar duplicados por texto de enunciado
    preguntas = cargar_preguntas(asignaturas[asignatura])
    preguntas_unicas = {p["pregunta"]: p for p in preguntas}.values()
    preguntas_unicas = list(preguntas_unicas)

    if len(preguntas_unicas) < 15:
        st.warning("⚠️ Solo hay suficientes preguntas únicas para un test corto.")
        
    st.session_state["preguntas_random"] = random.sample(
        preguntas_unicas,
        min(len(preguntas_unicas), 15)
    )


preguntas_random = st.session_state["preguntas_random"]
respuestas_usuario = {}

# Mostrar las preguntas
st.markdown("---")
st.subheader("Responde a las preguntas")

for i, pregunta in enumerate(preguntas_random):
    st.markdown(f"**{i+1}. {pregunta['pregunta']}**")

    opciones = [f"{key}: {val}" for key, val in pregunta['opciones'].items()]
    respuesta = st.radio(
        f"Selecciona una opción para la pregunta {i+1}",
        options=opciones,
        index=None,
        key=f"pregunta_{i}"
    )
    respuestas_usuario[i] = respuesta[0] if respuesta else None

# Corregir test
if st.button("📝 Corregir Test"):
    aciertos = 0
    st.markdown("## 📊 Resultados")

    for i, pregunta in enumerate(preguntas_random):
        respuesta_usuario = respuestas_usuario[i]
        correcta = pregunta["respuesta_correcta"]
        texto_correcto = pregunta["opciones"].get(correcta, "Opción no encontrada")
        es_correcto = respuesta_usuario == correcta
        icono = "✅" if es_correcto else "❌"

        if es_correcto:
            aciertos += 1

        st.markdown(f"**Pregunta {i+1}:** {pregunta['pregunta']}")
        st.markdown(f"- Tu respuesta: {respuesta_usuario or 'Sin responder'}")
        st.markdown(f"- Respuesta correcta: {correcta} - {texto_correcto} {icono}")
        st.markdown("---")

    porcentaje = (aciertos / len(preguntas_random)) * 100
    st.success(f"Has acertado {aciertos} de {len(preguntas_random)} preguntas. ({porcentaje:.2f}%)")
