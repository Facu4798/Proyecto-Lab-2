def export_database(user = 'root', 
                   password = 'password',
                   port = 3306,
                   host = 'localhost',
                   database = 'finanzas'):
    """
    Esta función exporta la base de datos a un archivo SQL.
    Esto permite recrear la base de datos en otro entorno o compartirla fácilmente.
    **Parámetros:**
    - **user:** str, usuario de MySQL (default='root')
    - **password:** str, contraseña de MySQL (default='password')
    - **port:** int, puerto de MySQL (default=3306)
    - **host:** str, host de MySQL (default='localhost')
    - **database:** str, nombre de la base de datos a exportar (default='finanzas')
    **Retorna:**
    - **None:** Esta función no retorna ningún valor, pero crea un archivo SQL con la exportación de la base de datos.
    """
    import os
    import subprocess
    # Verificar si mysqldump está instalado
    try:
        subprocess.run(['mysqldump', '--version'], check=True)
    except FileNotFoundError:
        raise RuntimeError("mysqldump no está instalado. Por favor, instale MySQL Server.")
    # Crear el comando mysqldump
    dump_command = [
        'mysqldump',
        '-u', user,
        f'--password={password}',
        '-P', str(port),
        '-h', host,
        database
    ]
    # Definir el nombre del archivo de salida
    output_file = f"{database}_export.sql"
    # Ejecutar el comando y redirigir la salida a un archivo
    with open(output_file, 'w') as output:
        try:
            subprocess.run(dump_command, stdout=output, check=True)
            print(f"Base de datos exportada exitosamente a {output_file}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error al exportar la base de datos: {e}")