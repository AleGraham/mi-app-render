import pandas as pd
import scipy.stats
import streamlit as st
import time

# Guardar variables de estado entre ejecuciones
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('🪙 Lanzar una moneda')

# Inicializar gráfico con un valor base
chart = st.line_chart([0.5])

# Función que simula lanzamientos y grafica la media acumulada
def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)

    return mean

# Controles de la interfaz
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

# Al presionar el botón
if start_button:
    st.write(f'🎯 Experimento con {number_of_trials} intentos en curso...')
    mean = toss_coin(number_of_trials)

    # Actualizar número de experimento
    st.session_state['experiment_no'] += 1

    # Guardar resultados en DataFrame de la sesión
    new_result = pd.DataFrame([[st.session_state['experiment_no'], number_of_trials, mean]],
                              columns=['no', 'iterations', 'mean'])

    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        new_result
    ], axis=0).reset_index(drop=True)

    st.success(f'✅ Media final de caras: {mean:.3f}')

# Mostrar tabla con todos los resultados acumulados
st.subheader("📊 Resultados acumulados")
st.dataframe(st.session_state['df_experiment_results'])
