from flask import Flask, request, jsonify, send_from_directory, render_template, render_template, redirect, url_for, session, flash
import joblib
import pandas as pd
import os
import sys
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

#Cargamos clave secreta
app.secret_key = os.getenv('SECRET_KEY')

# Definir usuarios permitidos utilizando variables de entorno
usuarios_autorizados = {
    os.getenv('USUARIO_ASESOR1'): os.getenv('PASSWORD_ASESOR1'),
    os.getenv('USUARIO_ASESOR2'): os.getenv('PASSWORD_ASESOR2')
}

# Ruta al archivo del modelo
modelo_path = os.path.join(os.getcwd(), 'modelo_fraudev3.pkl')

# Cargar el modelo si existe
if os.path.exists(modelo_path):
    modelo = joblib.load(modelo_path)
else:
    print("Archivo de modelo no encontrado")
    sys.exit(1)

# Inicializar el escalador
escalador = StandardScaler()

# Definir las columnas necesarias
columnas_modelo = [
    'income', 'name_email_similarity', 'current_address_months_count', 
    'customer_age', 'days_since_request', 'bank_branch_count_8w', 
    'date_of_birth_distinct_emails_4w', 'credit_risk_score', 'email_is_free', 
    'phone_home_valid', 'phone_mobile_valid', 'bank_months_count', 
    'has_other_cards', 'proposed_credit_limit', 'foreign_request', 
    'session_length_in_minutes', 'keep_alive_session', 
    'device_distinct_emails_8w', 'payment_type_AA', 'payment_type_AB', 
    'payment_type_AC', 'payment_type_AD', 'payment_type_AE', 
    'employment_status_CA', 'employment_status_CB', 'employment_status_CC', 
    'employment_status_CD', 'employment_status_CE', 'employment_status_CF', 
    'employment_status_CG', 'housing_status_BA', 'housing_status_BB', 
    'housing_status_BC', 'housing_status_BD', 'housing_status_BE', 
    'housing_status_BF', 'housing_status_BG', 'source_INTERNET', 
    'source_TELEAPP', 'device_os_linux', 'device_os_macintosh', 
    'device_os_other', 'device_os_windows', 'device_os_x11'
]

def preparar_dataframe(df):
    # Verificar si las columnas requeridas están en el DataFrame
    faltantes = [col for col in columnas_modelo if col not in df.columns]
    if faltantes:
        return None, f"Faltan las siguientes columnas: {', '.join(faltantes)}"
    
    df_filtrado = df[columnas_modelo].copy()
    return df_filtrado, None

def preprocesar_datos(data_df):
    data_df_normalizado = escalador.fit_transform(data_df)
    return pd.DataFrame(data_df_normalizado, columns=data_df.columns)

# Ruta de inicio para la página de inicio del banco
@app.route('/')
def home():
    return render_template('home.html')

#Ruta de login de asesores
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in usuarios_autorizados and usuarios_autorizados[username] == password:
            session['username'] = username
            return redirect(url_for('upload_file'))
        flash('Credenciales inválidas. Intente nuevamente.')
    return render_template('login.html')

#Ruta protegida para cargar archivos
@app.route('/upload', methods = ['GET', 'POST'] )
def upload_file():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    if 'file' not in request.files:
        return jsonify({'error': 'No hay parte de archivo en la solicitud'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Archivo no cargado'}), 400
    
    try:
        data_df = pd.read_csv(file)
    except Exception as e:
        return jsonify({'error': f'Error al leer el archivo CSV: {str(e)}'}), 400

    if 'id_client' not in data_df.columns:
        return jsonify({'error': 'El archivo CSV debe incluir la columna "id_client"'}), 400

    #Reseteo de índice para asegurar la alineación
    id_clientes = data_df['id_client'].reset_index(drop = True)
    #Preparación del DataFrame para el modelo eliminando 'id_client'
    data_df = data_df.drop(columns = ['id_client'])

    data_df_preparado, error = preparar_dataframe(data_df)
    if error:
        return jsonify({'error': error}), 400

    data_df_preprocesado = preprocesar_datos(data_df_preparado)

    prediccion = modelo.predict(data_df_preprocesado)

    #Asegurar que 'prediccion' sea un DataFrame con el mismo índice que 'id_clientes'
    predicciones_df = pd.DataFrame(prediccion, columns=['predicciones']).reset_index(drop = True)

    #Concatenar 'id_client' y 'predicciones'
    resultados_df = pd.concat([id_clientes, predicciones_df], axis = 1)

    #Para depuracion
    print(resultados_df.head())

    output_folder = 'resultados'
    os.makedirs(output_folder, exist_ok=True)

    original_filename = os.path.splitext(file.filename)[0]
    output_file_name = f"resultado_{original_filename}.xlsx"
    output_file_path = os.path.join(output_folder, output_file_name)

    resultados_df.to_excel(output_file_path, index=False)

    return jsonify({'message': 'Predicciones guardadas en XLSX', 'output_file': output_file_name})

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory('resultados', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.getenv('PORT',default=5000))