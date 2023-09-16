from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

# Configuración de la conexión a la base de datos Access
conn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\david\Documents\BuenasPracticas\TallerTareas\TasksDB.accdb')
cursor = conn.cursor()

@app.route('/')
def mostrar_tareas():
    # Consulta todas las tareas desde la base de datos
    cursor.execute('SELECT * FROM Tareas')
    tareas = cursor.fetchall()
    return render_template('tareas.html', tareas=tareas)

@app.route('/agregar_tarea', methods=['POST'])
def agregar_tarea():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        # Por defecto, una nueva tarea se considera no completada
        estado = False
        cursor.execute('INSERT INTO Tareas (descripcion, estado) VALUES (?, ?)', (descripcion, estado))
        conn.commit()
    return redirect(url_for('mostrar_tareas'))

@app.route('/completar_tarea/<int:tarea_Id>')
def completar_tarea(tarea_Id):
    # Obtener el estado actual de la tarea
    cursor.execute('SELECT estado FROM Tareas WHERE id = ?', (tarea_Id,))
    estado_actual = cursor.fetchone()

    if estado_actual and estado_actual[0] == False:
        nuevo_estado = True
    else:
        nuevo_estado = False

    # Actualizar el estado de la tarea en la base de datos
    cursor.execute('UPDATE Tareas SET estado = ? WHERE id = ?', (nuevo_estado, tarea_Id))
    conn.commit()

    return redirect(url_for('mostrar_tareas'))


@app.route('/eliminar_tarea/<int:tarea_Id>')
def eliminar_tarea(tarea_Id):
    # Eliminar una tarea de la base de datos
    cursor.execute('DELETE FROM Tareas WHERE Id = ?', (tarea_Id,))
    conn.commit()
    return redirect(url_for('mostrar_tareas'))

if __name__ == '__main__':
    app.run(debug=True)