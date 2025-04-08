import os
import subprocess
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import Frame, Label, Entry, Button
from PIL import Image, ImageTk
import psycopg2
import shutil
import webbrowser

# Clase para la ventana de inicio de sesión inicial
class Login:
    def __init__(self):
        # Crear la ventana principal de inicio de sesión
        self.ventana = tk.Tk()
        self.ventana.geometry("400x700")  # Establecer tamaño de la ventana
        self.ventana.title("Login")  # Título de la ventana
        self.fondo = "#88FFB4"  # Color de fondo verde claro
        self.setup_ui()  # Configurar la interfaz de usuario

    def setup_ui(self):
        # Método para organizar la creación de la interfaz de usuario
        self.create_frames()      # Crear los marcos superior e inferior
        self.create_title()       # Crear el título "Login"
        self.create_image()       # Cargar y mostrar la imagen
        self.create_user_inputs() # Crear campos de entrada para usuario y contraseña
        self.create_buttons()     # Crear los botones "Ingresar" y "Limpiar"

    def create_frames(self):
        # Crear marcos para organizar el diseño
        self.frame_superior = tk.Frame(self.ventana, bg=self.fondo)  # Marco superior para título e imagen
        self.frame_superior.pack(fill="both", expand=True)
        
        self.frame_inferior = tk.Frame(self.ventana, bg=self.fondo)  # Marco inferior para entradas y botones
        self.frame_inferior.pack(fill="both", expand=True)
        self.frame_inferior.columnconfigure(0, weight=1)  # Configurar columnas con peso igual
        self.frame_inferior.columnconfigure(1, weight=1)

    def create_title(self):
        # Crear y mostrar el título "Login" en la parte superior
        self.titulo = tk.Label(self.frame_superior, text="Login", font=("Calisto MT", 36, "bold"), bg=self.fondo)
        self.titulo.pack(side="top", pady=20)  # Espaciado vertical de 20 píxeles

    def create_image(self):
        # Cargar y mostrar una imagen en el marco superior
        base_path = os.path.dirname(os.path.abspath(__file__))  # Obtener directorio del script
        image_path = os.path.join(base_path, "images", "imglogin.png")  # Ruta de la imagen
        self.img = Image.open(image_path)  # Abrir la imagen con PIL
        self.img = self.img.resize((150, 165))  # Redimensionar a 150x165 píxeles
        self.render = ImageTk.PhotoImage(self.img)  # Convertir a formato compatible con Tkinter
        self.fondo_imagen = tk.Label(self.frame_superior, image=self.render, bg=self.fondo)
        self.fondo_imagen.pack(expand=True, fill="both", side="top")  # Centrar la imagen

    def create_user_inputs(self):
        # Crear etiquetas y campos de entrada para usuario y contraseña
        self.label_usuario = tk.Label(self.frame_inferior, text="Usuario:", font=("Arial", 18), bg=self.fondo, fg="black")
        self.label_usuario.grid(row=0, column=0, padx=10, sticky="e")  # Etiqueta "Usuario" alineada a la derecha
        
        self.entry_usuario = tk.Entry(self.frame_inferior, bd=0, width=14, font=("Arial", 18))
        self.entry_usuario.grid(row=0, column=1, columnspan=3, padx=5, sticky="w")  # Campo de entrada para usuario
        
        self.label_contraseña = tk.Label(self.frame_inferior, text="Contraseña:", font=("Arial", 18), bg=self.fondo, fg="black")
        self.label_contraseña.grid(row=1, column=0, pady=10, sticky="e")  # Etiqueta "Contraseña" con espacio vertical
        
        self.entry_contraseña = tk.Entry(self.frame_inferior, bd=0, width=14, font=("Arial", 18), show="•")
        self.entry_contraseña.grid(row=1, column=1, columnspan=3, padx=5, sticky="w")  # Campo de contraseña con máscara

    def create_buttons(self):
        # Crear botones "Ingresar" y "Limpiar"
        self.boton_ingresar = tk.Button(self.frame_inferior, text="Ingresar", width=16, font=("Arial", 12), command=self.entrar)
        self.boton_ingresar.grid(row=2, column=0, columnspan=2, pady=35)  # Botón "Ingresar" con espacio vertical
        
        self.boton_limpiar = tk.Button(self.frame_inferior, text="Limpiar", width=16, font=("Arial", 12), command=self.limpiar)
        self.boton_limpiar.grid(row=3, column=0, columnspan=2, pady=10)  # Botón "Limpiar" debajo

    def entrar(self):
        # Verificar las credenciales ingresadas
        nombre = self.entry_usuario.get()  # Obtener el texto del campo usuario
        contraseña = self.entry_contraseña.get()  # Obtener el texto del campo contraseña
        
        if not nombre or not contraseña:  # Validar que los campos no estén vacíos
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos")
            return
        
        # Verificar credenciales predefinidas (Joaco/joaco123)
        if nombre == "Joaco" and contraseña == "joaco123":
            messagebox.showinfo("Acceso Correcto", "Has ingresado")
            self.abrir_ventana_secundaria()  # Abrir ventana de configuración de base de datos
        else:
            messagebox.showerror("Acceso Incorrecto", "Los datos son erróneos")

    def limpiar(self):
        # Limpiar los campos de usuario y contraseña
        self.entry_usuario.delete(0, "end")
        self.entry_contraseña.delete(0, "end")

    def abrir_ventana_secundaria(self):
        # Ocultar la ventana de inicio de sesión y abrir la ventana secundaria
        self.ventana.withdraw()  # Ocultar ventana actual
        root = tk.Toplevel()  # Crear nueva ventana
        DatabaseConfigWindow(root)  # Instanciar la ventana de configuración
        root.mainloop()  # Iniciar bucle principal de la nueva ventana

# Clase para la ventana de configuración de base de datos
class DatabaseConfigWindow:
    def __init__(self, root):
        # Inicializar la ventana de configuración
        self.root = root
        self.root.title("Configuración de Base de Datos")  # Título de la ventana
        self.root.geometry("600x700")  # Tamaño de la ventana
        self.root.configure(bg='#f0f0f0')  # Fondo gris claro
        self.table_columns = {}  # Diccionario para almacenar columnas de las tablas
        self.chosen_fields = {}  # Nuevo diccionario para almacenar elecciones
        self.setup_ui()  # Configurar la interfaz
    
    def get_descriptive_field(self, table_name, cursor, primary_key='id'):
        """
        Versión FORZADA que SOLO devuelve campos para tablas directamente relacionadas
        y maneja automáticamente las relaciones anidadas
        """
        # 1. Lista blanca de tablas directamente relacionadas
        direct_relations = set()
        for table in self.tree.get_children():
            if self.tree.item(table, "values")[0] == "✔":  # Tablas seleccionadas
                table_name_selected = self.tree.item(table, "values")[1]
                if table_name_selected in self.foreign_keys:
                    for fk in self.foreign_keys[table_name_selected]:
                        direct_relations.add(fk[1])  # Tablas directamente relacionadas

        # 2. Si la tabla NO está en relaciones directas, devolver la PK automáticamente
        if table_name not in direct_relations:
            return primary_key

        # 3. Solo preguntar para tablas en relaciones directas
        try:
            if table_name in self.chosen_fields:
                return self.chosen_fields[table_name]
                
            cursor.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}' 
                AND column_name != '{primary_key}'
                ORDER BY ordinal_position
            """)
            available_columns = [row[0] for row in cursor.fetchall()]
            
            if not available_columns:
                return primary_key
                
            # Mostrar diálogo solo para tablas directamente relacionadas
            chosen = self.ask_user_for_field(table_name, available_columns)
            if chosen:
                self.chosen_fields[table_name] = chosen
                return chosen
                
            return primary_key
            
        except Exception as e:
            print(f"Error al obtener campo descriptivo: {e}")
            return primary_key

    def ask_user_for_field(self, table_name, column_names):
        """Muestra un diálogo para que el usuario elija un campo descriptivo con tamaño dinámico."""
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Seleccionar campo para {table_name}")
        dialog.transient(self.root)
        dialog.grab_set()

        # Frame principal
        main_frame = tk.Frame(dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Título
        title_label = tk.Label(
            main_frame, 
            text=f"Elige un campo para mostrar en '{table_name}':",
            font=("Helvetica", 10, "bold")
        )
        title_label.pack(pady=(0, 10))

        # Frame para el área scrollable
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Canvas y Scrollbar
        canvas = tk.Canvas(canvas_frame)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        # Frame scrollable para los radio buttons
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)

        # Variable para almacenar la selección
        selected_field = tk.StringVar(value=column_names[0])
        
        # Crear radio buttons
        for col in column_names:
            rb = tk.Radiobutton(
                scrollable_frame, 
                text=col, 
                variable=selected_field, 
                value=col,
                font=("Helvetica", 10)
            )
            rb.pack(anchor="w", padx=10, pady=2)

        # Configurar pack del canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame para el botón
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(0, 5))

        # Botón centrado
        confirm_button = tk.Button(
            button_frame,
            text="Confirmar",
            command=lambda: [chosen.__setitem__(0, selected_field.get()), dialog.destroy()],
            font=("Helvetica", 10),
            width=15
        )
        confirm_button.pack(pady=5)

        # Calcular dimensiones
        dialog.update()
        
        # Obtener dimensiones de la pantalla
        screen_width = dialog.winfo_screenwidth()
        screen_height = dialog.winfo_screenheight()
        
        # Calcular tamaño de la ventana
        window_width = min(400, screen_width - 100)
        window_height = min(500, screen_height - 100)
        
        # Calcular posición
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # Configurar geometría final
        dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")

        chosen = [None]
        dialog.wait_window()
        return chosen[0]
    
    def shorten_param_name(self, original_name):
        """
        Acorta nombres de parámetros para rutas Laravel manteniendo significado
        Ejemplo: 'id_persona_facultad_administrador' -> 'id_pers_fac_adm'
        """
        if len(original_name) <= 32:
            return original_name
        
        # Dividir por guiones bajos y tomar primeras 4 letras de cada parte
        parts = original_name.split('_')
        shortened = '_'.join([part[:4] for part in parts])
        
        # Asegurar que no exceda 32 caracteres
        return shortened[:32]
    
    
    
    def setup_ui(self):
        # Organizar la creación de la interfaz de configuración
        self.create_title()         # Crear título de la ventana
        self.create_connection_frame()  # Crear sección de detalles de conexión
        self.create_tables_frame()      # Crear sección de selección de tablas
        self.create_project_frame()     # Crear sección de detalles del proyecto

    def create_title(self):
        # Crear el título de la ventana de configuración
        title_frame = tk.Frame(self.root, bg='#3498db', pady=10)  # Marco azul para el título
        title_frame.pack(fill=tk.X)  # Expandir horizontalmente
        title_label = tk.Label(
            title_frame, 
            text="Configuración de Base de Datos", 
            font=("Helvetica", 18, "bold"), 
            fg='white', 
            bg='#3498db'
        )
        title_label.pack(pady=10)  # Centrar el título con espacio vertical

    def create_connection_frame(self):
        # Crear el marco para los detalles de conexión a la base de datos
        connection_frame = tk.LabelFrame(
            self.root, 
            text="Detalles de Conexión", 
            font=("Helvetica", 12),
            bg='#f0f0f0',
            labelanchor='n'
        )
        connection_frame.pack(fill=tk.X, padx=20, pady=10)  # Expandir horizontalmente con márgenes

        # Lista de campos de entrada para la conexión
        fields = [
            ("Base de datos:", "db_entry", False),
            ("Puerto:", "port_entry", False),
            ("Usuario:", "user_entry", False),
            ("Contraseña:", "password_entry", True)
        ]

        # Crear cada campo de entrada
        for label_text, entry_name, is_password in fields:
            self.create_input_field(connection_frame, label_text, entry_name, is_password)

        # Botón para probar la conexión
        test_button = tk.Button(
            connection_frame, 
            text="Probar Conexión", 
            command=self.test_connection,
            bg='#2ecc71',  # Verde
            fg='white',
            font=("Helvetica", 10, "bold"),
            relief=tk.RAISED,
            borderwidth=2
        )
        test_button.pack(pady=10)  # Centrar con espacio vertical

    def create_input_field(self, parent, label_text, entry_name, is_password):
        # Crear un campo de entrada genérico
        frame = tk.Frame(parent, bg='#f0f0f0')
        frame.pack(fill=tk.X, padx=20, pady=5)  # Expandir horizontalmente con márgenes

        label = tk.Label(
            frame, 
            text=label_text, 
            width=15, 
            anchor='w',  # Alinear a la izquierda
            bg='#f0f0f0'
        )
        label.pack(side=tk.LEFT)  # Etiqueta a la izquierda

        entry = tk.Entry(
            frame, 
            show="*" if is_password else "",  # Mostrar asteriscos si es contraseña
            font=("Helvetica", 10),
            relief=tk.SOLID,
            borderwidth=1
        )
        entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)  # Campo de entrada expansible
        setattr(self, entry_name, entry)  # Asignar el campo como atributo de la clase

    def create_tables_frame(self):
        # Crear el marco para seleccionar tablas
        tables_frame = tk.LabelFrame(
            self.root, 
            text="Seleccionar Tablas", 
            font=("Helvetica", 12),
            bg='#f0f0f0',
            labelanchor='n'
        )
        tables_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)  # Expandir en ambas direcciones

        tree_frame = tk.Frame(tables_frame, bg='#f0f0f0')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Marco para el Treeview

        # Crear el Treeview para mostrar las tablas
        self.tree = ttk.Treeview(
            tree_frame, 
            columns=("Checkbox", "Table"), 
            show="headings",
            selectmode="extended"
        )
        self.tree.heading("Checkbox", text="Seleccionar")  # Columna de casillas
        self.tree.heading("Table", text="Tablas")  # Columna de nombres de tablas
        self.tree.column("Checkbox", width=50, anchor='center')  # Ancho fijo para casillas
        self.tree.column("Table", anchor='w')  # Alinear nombres a la izquierda

        self.tree.bind("<Button-1>", self.on_table_click)  # Vincular clic para alternar casillas

        scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)  # Configurar barra de desplazamiento

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Mostrar Treeview a la izquierda
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  # Barra de desplazamiento a la derecha

        # Casilla para seleccionar todas las tablas
        self.select_all_var = tk.BooleanVar()
        select_all_check = tk.Checkbutton(
            tables_frame, 
            text="Seleccionar Todas las Tablas", 
            variable=self.select_all_var,
            command=self.toggle_select_all,
            bg='#f0f0f0',
            font=("Helvetica", 10)
        )
        select_all_check.pack(pady=5)  # Centrar con espacio vertical

    def create_project_frame(self):
        # Crear el marco para los detalles del proyecto
        project_frame = tk.LabelFrame(
            self.root, 
            text="Detalles del Proyecto", 
            font=("Helvetica", 12),
            bg='#f0f0f0',
            labelanchor='n'
        )
        project_frame.pack(fill=tk.X, padx=20, pady=10)  # Expandir horizontalmente con márgenes
        project_inner_frame = tk.Frame(project_frame, bg='#f0f0f0')
        project_inner_frame.pack(fill=tk.X, padx=10, pady=5)  # Marco interno para alineación
        project_label = tk.Label(
            project_inner_frame, 
            text="Nombre/Ruta del Proyecto:", 
            width=15, 
            anchor='w',
            bg='#f0f0f0',
            font=("Helvetica", 10)
        )
        project_label.pack(side=tk.LEFT)  # Etiqueta a la izquierda
        self.project_entry = tk.Entry(
            project_inner_frame, 
            font=("Helvetica", 10),
            relief=tk.SOLID,
            borderwidth=1
        )
        self.project_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)  # Campo expansible
        
        # Botones para Crear Proyecto y Generar Modelos
        buttons_frame = tk.Frame(self.root, bg='#f0f0f0')
        buttons_frame.pack(fill=tk.X, padx=20, pady=10)
        
        create_button = tk.Button(
            buttons_frame, 
            text="Crear Proyecto", 
            command=self.create_project,
            bg='#3498db',  # Azul
            fg='white',
            font=("Helvetica", 10, "bold"),
            relief=tk.RAISED,
            borderwidth=2
        )
        create_button.pack(side=tk.LEFT, padx=10)  # Centrar con espacio vertical

        generate_button = tk.Button(
            buttons_frame, 
            text="Generar Modelos", 
            command=self.generate_models,
            bg='#e67e22',  # Naranja
            fg='white',
            font=("Helvetica", 10, "bold"),
            relief=tk.RAISED,
            borderwidth=2
        )
        generate_button.pack(side=tk.LEFT, padx=10)  # Centrar con espacio vertical

    def test_connection(self):
        # Probar la conexión a la base de datos PostgreSQL
        db = self.db_entry.get()  # Nombre de la base de datos
        port = self.port_entry.get()  # Puerto
        user = self.user_entry.get()  # Usuario
        password = self.password_entry.get()  # Contraseña
        
        try:
            # Establecer conexión con la base de datos
            conn = psycopg2.connect(
                dbname=db, 
                user=user, 
                password=password, 
                host="localhost", 
                port=port
            )
            cursor = conn.cursor()
            
            # Obtener lista de tablas en el esquema público
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            
            # Ordenar las tablas alfabéticamente
            tables = sorted(tables, key=lambda x: x[0])  # Ordenar por nombre de tabla
            
            # Limpiar el Treeview antes de agregar nuevas tablas
            for row in self.tree.get_children():
                self.tree.delete(row)
            
            # Diccionarios para almacenar claves foráneas y columnas
            self.foreign_keys = {}
            self.table_columns = {}
            for table in tables:
                table_name = table[0]
                # Consultar claves foráneas de la tabla
                cursor.execute(f"""
                    SELECT kcu.column_name, ccu.table_name AS foreign_table, ccu.column_name AS foreign_column
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.table_schema = 'public' AND tc.table_name = '{table_name}' AND tc.constraint_type = 'FOREIGN KEY';
                """)
                foreign_keys = cursor.fetchall()
                self.foreign_keys[table_name] = foreign_keys
                
                # Consultar columnas y tipos de datos de la tabla
                cursor.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{table_name}';")
                columns_info = cursor.fetchall()
                self.table_columns[table_name] = [(col[0], col[1]) for col in columns_info]
            
            # Agregar tablas ordenadas al Treeview con casilla de selección
            for table in tables:
                self.tree.insert("", "end", values=("⬜", table[0]))
            
            messagebox.showinfo("Conexión Exitosa", "Conexión establecida correctamente.")
            conn.close()  # Cerrar la conexión
        except Exception as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar: {e}")

    def on_table_click(self, event):
        # Alternar estado de casilla al hacer clic en el Treeview
        rowid = self.tree.identify_row(event.y)  # Identificar fila clicada
        column = self.tree.identify_column(event.x)  # Identificar columna clicada

        if rowid and column == "#1":  # Si se hace clic en la columna de casillas
            values = self.tree.item(rowid, "values")
            checkbox = values[0]
            new_checkbox = "✔" if checkbox == "⬜" else "⬜"  # Alternar entre seleccionado y no seleccionado
            self.tree.item(rowid, values=(new_checkbox, values[1]))

    def toggle_select_all(self):
        # Seleccionar o deseleccionar todas las tablas
        select_all = self.select_all_var.get()  # Obtener estado de la casilla "Seleccionar Todas"
        for item in self.tree.get_children():
            self.tree.item(item, values=("✔" if select_all else "⬜", self.tree.item(item, "values")[1]))

    
    
    
    # Funcion para solo generar los modelos
    def generate_models(self):
        project_path = self.project_entry.get()  # Ruta del proyecto existente
        if not project_path or not os.path.exists(project_path):
            messagebox.showerror("Error", "Por favor, ingresa una ruta válida para un proyecto existente")
            return
        
        db = self.db_entry.get()  # Nombre de la base de datos
        port = self.port_entry.get()  # Puerto
        user = self.user_entry.get()  # Usuario
        password = self.password_entry.get()  # Contraseña
        
        # Obtener lista de tablas seleccionadas
        tables_to_generate = [
            self.tree.item(item, "values")[1] for item in self.tree.get_children() if self.tree.item(item, "values")[0] == "✔"
        ]
        
        # Validar que se haya seleccionado al menos una tabla
        if not tables_to_generate:
            messagebox.showerror("Error", "Por favor, selecciona al menos una tabla")
            return
        
        try:
            # Conectar a la base de datos
            conn = psycopg2.connect(dbname=db, user=user, password=password, host="localhost", port=port)
            cursor = conn.cursor()
            
            # Identificar tablas relacionadas mediante claves foráneas
            related_tables = set()
            for table in tables_to_generate:
                if table in self.foreign_keys:
                    for fk in self.foreign_keys[table]:
                        related_tables.add(fk[1])
            all_tables = set(tables_to_generate).union(related_tables)  # Combinar tablas seleccionadas y relacionadas
            
            # Cambiar al directorio del proyecto existente
            os.chdir(project_path)
            
            # Inicializar contenido del archivo de rutas
            routes_content = "<?php\nuse Illuminate\\Support\\Facades\\Route;\n"
            existing_routes = set()
            
            # Leer rutas existentes para evitar duplicados
            if os.path.exists("routes/web.php"):
                with open("routes/web.php", "r", encoding="utf-8") as existing_routes_file:
                    for line in existing_routes_file:
                        if "Route::resource" in line:
                            existing_routes.add(line.split("'")[1])
            
            # Generar modelos, controladores y vistas para cada tabla
            for table in all_tables:
                if table in existing_routes:
                    print(f"Saltando generación para tabla ya existente: {table}")
                    continue
                
                model_name = ''.join([word.capitalize() for word in table.split('_')])  # Nombre del modelo en CamelCase
                controller_name = f"{model_name}Controller"  # Nombre del controlador
                routes_content += f"use App\\Http\\Controllers\\{controller_name};\n"
                
                # Obtener la clave primaria de la tabla
                cursor.execute(f"""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.table_schema = 'public'
                    AND tc.table_name = '{table}'
                    AND tc.constraint_type = 'PRIMARY KEY';
                """)
                primary_key = cursor.fetchone()
                primary_key = primary_key[0] if primary_key else "id"  # Usar "id" por defecto si no hay clave primaria
                
                # Obtener información de columnas y tipos de datos
                columns_info = self.table_columns[table]
                columns = [col[0] for col in columns_info]
                column_types = {col[0]: col[1] for col in columns_info}
                
                # Generar contenido del modelo
                model_content = f"""<?php

    namespace App\\Models;

    use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
    use Illuminate\\Database\\Eloquent\\Model;

    class {model_name} extends Model
    {{
        use HasFactory;

        protected $table = '{table}';
        protected $primaryKey = '{primary_key}';
        public $timestamps = false;

        protected $fillable = [
    """
                for column in columns:
                    if column != primary_key and column not in ["created_at", "updated_at"]:
                        model_content += f"        '{column}',\n"
                model_content += "    ];\n"

                # Agregar relaciones de claves foráneas
                if table in self.foreign_keys:
                    for fk in self.foreign_keys[table]:
                        column_name = fk[0]
                        foreign_table = fk[1]
                        foreign_model = ''.join([word.capitalize() for word in foreign_table.split('_')])
                        model_content += f"""
        public function {foreign_table}()
        {{
            return $this->belongsTo({foreign_model}::class, '{column_name}');
        }}
    """
                model_content += "}\n"

                # Guardar el modelo
                model_path = f"app/Models/{model_name}.php"
                os.makedirs(os.path.dirname(model_path), exist_ok=True)
                with open(model_path, "w", encoding="utf-8", newline="\n") as file:
                    file.write(model_content)

                print(f"Modelo generado para: {table}")
                
                # Generar contenido del controlador con mejoras dinámicas
                controller_content = f"""<?php
                namespace App\\Http\\Controllers;

                use App\\Models\\{model_name};
                use Illuminate\\Http\\Request;
                use Yajra\\DataTables\\Facades\\DataTables;
                use Illuminate\\Support\\Facades\\DB;

                class {controller_name} extends Controller
                {{
                    public function index(Request $request)
                    {{
                        if ($request->ajax()) {{
                            ${table} = {model_name}::select('{table}.*');
                """
                if table in self.foreign_keys:
                    relationships = list({fk[1] for fk in self.foreign_keys[table]})
                    if relationships:
                        rel_list = ', '.join([f"'{rel}'" for rel in relationships])
                        controller_content += f"            ${table} = ${table}->with([{rel_list}]);\n"

                controller_content += f"""
                            return DataTables::of(${table})
                """
                for column in columns:
                    if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                        fk_info = next(fk for fk in self.foreign_keys[table] if fk[0] == column)
                        foreign_table = fk_info[1]
                        foreign_column = fk_info[2]
                        descriptive_field = self.get_descriptive_field(foreign_table, cursor, foreign_column)
                        # Si el usuario eligió un campo, usarlo
                        if foreign_table in self.chosen_fields:
                            descriptive_field = self.chosen_fields[foreign_table]
                        controller_content += f"""                ->addColumn('{column}_display', function ($row) {{
                                            return $row->{foreign_table} ? ($row->{foreign_table}->{descriptive_field} ?? $row->{column}) : $row->{column};
                                        }})\n"""
                controller_content += f"""                ->addColumn('action', function ($row) {{
                                    $btn = '<button class="btn btn-info btn-sm viewRecord" data-id="' . $row->{primary_key} . '">Ver</button>';
                                    $btn .= ' <button class="btn btn-primary btn-sm editRecord" data-id="' . $row->{primary_key} . '">Editar</button>';
                                    $btn .= ' <button class="btn btn-danger btn-sm deleteRecord" data-id="' . $row->{primary_key} . '">Eliminar</button>';
                                    return $btn;
                                }})
                                ->rawColumns(['action'])
                                ->make(true);
                        }}

                        return view('{table}.index');
                    }}

                    public function store(Request $request)
                    {{
                        try {{
                            $request->validate([
                """
                for column, col_type in columns_info:
                    if column != primary_key:
                        if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                            fk_info = next(fk for fk in self.foreign_keys[table] if fk[0] == column)
                            foreign_table = fk_info[1]
                            foreign_column = fk_info[2]
                            controller_content += f"                '{column}' => 'required|exists:{foreign_table},{foreign_column}',\n"
                        elif col_type in ('character varying', 'text', 'varchar'):
                            if column in ('escudo', 'imagen', 'foto', 'image'):
                                controller_content += f"                '{column}' => 'nullable|file|mimes:jpg,png|max:2048',\n"
                            else:
                                controller_content += f"                '{column}' => 'required|string|max:255',\n"
                        elif col_type == 'date':
                            controller_content += f"                '{column}' => 'required|date',\n"
                        elif col_type in ('integer', 'bigint', 'smallint'):
                            controller_content += f"                '{column}' => 'required|integer',\n"
                        elif col_type == 'numeric':
                            controller_content += f"                '{column}' => 'required|numeric',\n"
                        elif column == 'estado':
                            controller_content += f"                '{column}' => 'required|in:A,I',\n"
                        else:
                            controller_content += f"                '{column}' => 'required',\n"

                controller_content += f"""            ]);

                            $data = $request->all();
                """
                for column in columns:
                    if column in ('escudo', 'imagen', 'foto', 'image'):
                        controller_content += f"""            if ($request->hasFile('{column}')) {{
                                $data['{column}'] = $request->file('{column}')->store('{column}s', 'public');
                            }}\n"""

                controller_content += f"""
                            ${table} = {model_name}::create($data);
                            return response()->json(${table}, 201);
                        }} catch (\\Exception $e) {{
                            return response()->json(['error' => $e->getMessage()], 500);
                        }}
                    }}

                    public function edit($id)
                    {{
                        ${table} = {model_name}::findOrFail($id);
                        return response()->json(${table});
                    }}

                    public function update(Request $request, $id)
                    {{
                        try {{
                            $request->validate([
                """
                for column, col_type in columns_info:
                    if column != primary_key:
                        if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                            fk_info = next(fk for fk in self.foreign_keys[table] if fk[0] == column)
                            foreign_table = fk_info[1]
                            foreign_column = fk_info[2]
                            controller_content += f"                '{column}' => 'required|exists:{foreign_table},{foreign_column}',\n"
                        elif col_type in ('character varying', 'text', 'varchar'):
                            if column in ('escudo', 'imagen', 'foto', 'image'):
                                controller_content += f"                '{column}' => 'nullable|file|mimes:jpg,png|max:2048',\n"
                            else:
                                controller_content += f"                '{column}' => 'required|string|max:255',\n"
                        elif col_type == 'date':
                            controller_content += f"                '{column}' => 'required|date',\n"
                        elif col_type in ('integer', 'bigint', 'smallint'):
                            controller_content += f"                '{column}' => 'required|integer',\n"
                        elif col_type == 'numeric':
                            controller_content += f"                '{column}' => 'required|numeric',\n"
                        elif column == 'estado':
                            controller_content += f"                '{column}' => 'required|in:A,I',\n"
                        else:
                            controller_content += f"                '{column}' => 'required',\n"

                controller_content += f"""            ]);

                            ${table} = {model_name}::findOrFail($id);
                            $data = $request->all();

                            // Manejar archivos de imagen
                """
                for column in columns:
                    if column in ('escudo', 'imagen', 'foto', 'image'):
                        controller_content += f"""            if ($request->hasFile('{column}')) {{
                                // Eliminar imagen anterior si existe
                                if (${table}->{column} && Storage::disk('public')->exists(${table}->{column})) {{
                                    Storage::disk('public')->delete(${table}->{column});
                                }}
                                $data['{column}'] = $request->file('{column}')->store('{column}s', 'public');
                            }} else {{
                                // Mantener la imagen existente si no se sube una nueva
                                unset($data['{column}']);
                            }}\n"""

                controller_content += f"""
                            ${table}->update($data);
                            return response()->json(${table});
                        }} catch (\\Illuminate\\Validation\\ValidationException $e) {{
                            return response()->json(['errors' => $e->errors()], 422);
                        }} catch (\\Exception $e) {{
                            return response()->json(['error' => $e->getMessage()], 500);
                        }}
                    }}
                    public function show($id)
                    {{
                        ${table} = {model_name}::findOrFail($id);
                        return response()->json(${table});
                    }}

                    public function destroy($id)
                    {{
                        try {{
                            ${table} = {model_name}::findOrFail($id);
                            ${table}->delete();
                            DB::statement("SELECT setval(pg_get_serial_sequence('{table}', '{primary_key}'), COALESCE((SELECT MAX({primary_key}) FROM {table}), 1))");
                            return response()->json(['message' => 'Registro eliminado exitosamente']);
                        }} catch (\\Exception $e) {{
                            return response()->json(['error' => $e->getMessage()], 500);
                        }}
                    }}
                }}
                    """

                # Guardar el controlador
                controller_path = f"app/Http/Controllers/{controller_name}.php"
                os.makedirs(os.path.dirname(controller_path), exist_ok=True)
                with open(controller_path, "w", encoding="utf-8", newline="\n") as file:
                    file.write(controller_content)

                print(f"Controlador generado para: {table}")
                
            
            
                os.makedirs(f"resources/views/{table}", exist_ok=True)

                # Generar la vista index.blade.php dinámicamente
                index_view = f"""@extends('layouts.app')

                @section('content')
                <div class="container">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-header">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <h5><i class="fa fa-table"></i> Lista de {table.replace('_', ' ').title()}</h5>
                                        <button class="btn btn-success" id="createNewRecord">
                                            <i class="fa fa-plus"></i> Nuevo
                                        </button>
                                    </div>
                                </div>
                                <div class="card-body">
                                    @if ($message = Session::get('success'))
                                        <div class="alert alert-success">
                                            <p>{{{{ $message }}}}</p>
                                        </div>
                                    @endif

                                    <table class="table table-bordered table-striped data-table">
                                        <thead>
                                            <tr>
                """
                for column in columns:
                    if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                        foreign_table = next(fk[1] for fk in self.foreign_keys[table] if fk[0] == column)
                        index_view += f"                                <th>{foreign_table.replace('_', ' ').title()}</th>\n"
                    else:
                        index_view += f"                                <th>{column.replace('_', ' ').title()}</th>\n"
                index_view += """                                <th width="280px">Acciones</th>
                                            </tr>
                                        </thead>
                                        <tbody></tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Modal para crear/editar registros -->
                <div class="modal fade" id="ajaxModel" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title"></h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <form id="form">
                                    @csrf
                                    <input type="hidden" name="id" id="table_id">
                """
                for column, col_type in columns_info:
                    if column != primary_key:
                        if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                            fk_info = next(fk for fk in self.foreign_keys[table] if fk[0] == column)
                            foreign_table = fk_info[1]
                            foreign_column = fk_info[2]
                            foreign_model = ''.join([word.capitalize() for word in foreign_table.split('_')])
                            descriptive_field = self.get_descriptive_field(foreign_table, cursor, foreign_column)
                            # Si el usuario eligió un campo, usarlo
                            if foreign_table in self.chosen_fields:
                                descriptive_field = self.chosen_fields[foreign_table]
                            index_view += f"""
                                <div class="mb-3">
                                    <label for="{column}" class="form-label">{foreign_table.replace('_', ' ').title()}</label>
                                    <select class="form-control" id="{column}" name="{column}" required>
                                        <option value="">Seleccione una opción</option>
                                        @foreach(\\App\\Models\\{foreign_model}::all() as $item)
                                            <option value="{{{{ $item->{foreign_column} }}}}" {{{{ old('{column}') == $item->{foreign_column} ? 'selected' : '' }}}}>
                                                {{{{ $item->{descriptive_field} ?? $item->{foreign_column} }}}}
                                            </option>
                                        @endforeach
                                    </select>
                                </div>
                            """
                        elif col_type == "date":
                            index_view += f"""
                                    <div class="mb-3">
                                        <label for="{column}" class="form-label">{column.replace('_', ' ').title()}</label>
                                        <input type="text" class="form-control datepicker" id="{column}" name="{column}" required readonly>
                                    </div>
                """
                        elif column in ('escudo', 'imagen', 'foto', 'image'):
                            index_view += f"""
                                    <div class="mb-3">
                                        <label for="{column}" class="form-label">{column.replace('_', ' ').title()}</label>
                                        <input type="file" class="form-control" id="{column}" name="{column}">
                                    </div>
                """
                        elif column == "estado":
                            index_view += f"""
                                    <div class="mb-3">
                                        <label for="{column}" class="form-label">{column.replace('_', ' ').title()}</label>
                                        <select class="form-control" id="{column}" name="{column}" required>
                                            <option value="A">Activo</option>
                                            <option value="I">Inactivo</option>
                                        </select>
                                    </div>
                """
                        elif col_type in ('integer', 'bigint', 'smallint'):
                            index_view += f"""
                                    <div class="mb-3">
                                        <label for="{column}" class="form-label">{column.replace('_', ' ').title()}</label>
                                        <input type="number" class="form-control" id="{column}" name="{column}" required>
                                    </div>
                """
                        elif col_type == 'numeric':
                            index_view += f"""
                                    <div class="mb-3">
                                        <label for="{column}" class="form-label">{column.replace('_', ' ').title()}</label>
                                        <input type="number" step="any" class="form-control" id="{column}" name="{column}" required>
                                    </div>
                """
                        else:
                            index_view += f"""
                                    <div class="mb-3">
                                        <label for="{column}" class="form-label">{column.replace('_', ' ').title()}</label>
                                        <input type="text" class="form-control" id="{column}" name="{column}" required>
                                    </div>
                """

                index_view += """
                                    <button type="submit" class="btn btn-primary">Guardar</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Modal para eliminar registros -->
                <div class="modal fade" id="deleteModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Eliminar Registro</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <p>¿Estás seguro de que deseas eliminar este registro?</p>
                                <form id="deleteForm">
                                    @csrf
                                    @method('DELETE')
                                    <input type="hidden" id="delete_id" name="id">
                                    <button type="submit" class="btn btn-danger">Eliminar</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Modal para ver detalles -->
                <div class="modal fade" id="viewModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Detalles</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                """
                for column in columns:
                    if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                        foreign_table = next(fk[1] for fk in self.foreign_keys[table] if fk[0] == column)
                        descriptive_field = self.get_descriptive_field(foreign_table, cursor, primary_key)
                        if foreign_table in self.chosen_fields:
                            descriptive_field = self.chosen_fields[foreign_table]
                        index_view += f"""
                            <p><strong>{foreign_table.replace('_', ' ').title()}:</strong> 
                            <span id="view_{column}"></span>
                            </p>
                        """
                    else:
                        index_view += f"""<p><strong>{column.replace('_', ' ').title()}:</strong> <span id="view_{column}"></span></p>\n"""

                index_view += f"""            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                            </div>
                        </div>
                    </div>
                </div>

                @push('scripts')
                <script>
                    var URLindex = "{{{{ route('{table}.index') }}}}";
                    var URLstore = "{{{{ route('{table}.store') }}}}";
                    var URLupdate = "{{{{ route('{table}.update', ':id') }}}}";
                    var titulo = "{table.replace('_', ' ').title()}";
                    var columnas = [
                """
                for column in columns:
                    if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                        index_view += f"""        {{
                            data: '{column}_display',
                            name: '{column}'
                        }},
                """
                    else:
                        index_view += f"""        {{
                            data: '{column}',
                            name: '{column}'
                        }},
                """
                index_view += """        {
                            data: 'action',
                            name: 'action',
                            orderable: false,
                            searchable: false
                        }
                    ];

                    (function() {
                        'use strict';

                        $.ajaxSetup({
                            headers: {
                                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
                            }
                        });

                        var table = $('.data-table').DataTable({
                            processing: true,
                            serverSide: true,
                            ajax: URLindex,
                            columns: columnas,
                            order: [[0, 'asc']],
                            scrollX: true,
                            responsive: true,
                            autoWidth: false,
                        });

                        $('.datepicker').datepicker({
                            dateFormat: 'yy-mm-dd',
                            changeMonth: true,
                            changeYear: true,
                            yearRange: '-100:+10'
                        });

                        $('#form').on('submit', function(e) {
                            e.preventDefault();
                            var formData = new FormData(this);
                            var tableId = $('#table_id').val().trim();
                            var method = tableId ? 'PUT' : 'POST';
                            var url = tableId ? URLupdate.replace(':id', tableId) : URLstore;

                            // Agregar el método PUT para actualizaciones
                            if (method === 'PUT') {
                                formData.append('_method', 'PUT');
                            }

                            $.ajax({
                                url: url,
                                method: 'POST', // Siempre usar POST para enviar archivos
                                data: formData,
                                processData: false,
                                contentType: false,
                                success: function(data) {
                                    $('#form').trigger("reset");
                                    $('#table_id').val('');
                                    $('#ajaxModel').modal('hide');
                                    toastr['success']('Registro guardado correctamente.');
                                    table.draw(false);
                                },
                                error: function(xhr) {
                                    var errors = xhr.responseJSON.errors;
                                    if (errors) {
                                        Object.keys(errors).forEach(function(key) {
                                            toastr['error'](errors[key][0]);
                                        });
                                    } else {
                                        toastr['error']('Ocurrió un error: ' + (xhr.responseJSON ? xhr.responseJSON.message : 'Desconocido'));
                                    }
                                    console.log('Errores:', xhr.responseJSON);
                                }
                            });
                        });

                        $('#createNewRecord').on("click", function() {
                            $('#table_id').val('');
                            $('#form')[0].reset();
                            $('.modal-title').html("Crear nuevo " + titulo);
                            $('#ajaxModel').modal('show');
                        });

                        $('body').on('click', '.viewRecord', function() {
                            var table_id = $(this).data('id');
                            $.get(URLindex + '/' + table_id, function(data) {
                                $('.modal-title').html("Detalles de " + titulo);
                """
                for column in columns:
                    if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                        foreign_table = next(fk[1] for fk in self.foreign_keys[table] if fk[0] == column)
                        descriptive_field = self.get_descriptive_field(foreign_table, cursor, primary_key)
                        index_view += f"""
                            $('#view_{column}').text(data.{foreign_table} ? (data.{foreign_table}.{descriptive_field} ?? data.{column}) : 'N/A');
                        """
                    else:
                        index_view += f"""
                            $('#view_{column}').text(data.{column} || 'N/A');
                        """

                index_view += f"""
                                $('#viewModal').modal('show');
                            }}).fail(function(xhr) {{
                                toastr['error']('Error al obtener los datos: ' + xhr.responseJSON.message);
                            }});
                        }});

                        $('body').on('click', '.editRecord', function() {{
                            var table_id = $(this).data("id");
                            $.get(URLindex + '/' + table_id + '/edit', function(data) {{
                                $('.modal-title').html("Editar " + titulo);
                                $('#ajaxModel').modal('show');
                                $('#table_id').val(data.{primary_key});
                """
                for column in columns:
                    if column != primary_key and column not in ('escudo', 'imagen', 'foto', 'image'):  # No pre-cargar archivos
                        index_view += f"                $('#{column}').val(data.{column});\n"

                index_view += """            }).fail(function(xhr) {
                                toastr['error']('Error al obtener los datos: ' + xhr.responseJSON.message);
                            });
                        });

                        $('body').on('click', '.deleteRecord', function() {
                            var table_id = $(this).data("id");
                            if (confirm("¿Confirma borrar el registro?")) {
                                $.ajax({
                                    type: "DELETE",
                                    url: URLindex + '/' + table_id,
                                    success: function(data) {
                                        toastr['success']('Registro borrado correctamente.');
                                        table.draw();
                                    },
                                    error: function(xhr) {
                                        toastr['error']('Ocurrió un error: ' + (xhr.responseJSON ? xhr.responseJSON.message : 'Desconocido'));
                                    }
                                });
                            }
                        });
                    })();
                </script>
                @endpush
                @endsection
                """

                # Guardar la vista
                with open(f"resources/views/{table}/index.blade.php", "w", encoding="utf-8", newline="\n") as file:
                    file.write(index_view)
                print(f"Vistas CRUD generadas para: {table}")
            
                # Actualizar archivo de rutas
                if os.path.exists("routes/web.php"):
                    # Leer el contenido existente del archivo web.php
                    with open("routes/web.php", "r", encoding="utf-8") as existing_routes_file:
                        existing_content = existing_routes_file.read()

                    # Verificar si ya hay una declaración <?php al inicio
                    if "<?php" in existing_content and "use Illuminate\\Support\\Facades\\Route;" in existing_content:
                        routes_content = existing_content  # Mantener el contenido existente
                    else:
                        routes_content = "<?php\nuse Illuminate\\Support\\Facades\\Route;\n"

                    # Agregar nuevas rutas solo si no existen
                    for table in all_tables:
                        model_name = ''.join([word.capitalize() for word in table.split('_')])  # Nombre del modelo en CamelCase
                        controller_name = f"{model_name}Controller"  # Nombre del controlador
                        param_name = self.shorten_param_name(primary_key)

                        # Verificar si la ruta ya existe
                        route_exists = any(f"Route::resource('{table}'" in line for line in existing_content.splitlines())
                        if not route_exists:
                            routes_content += f"""
                use App\\Http\\Controllers\\{controller_name};

                Route::resource('{table}', {controller_name}::class)->parameters(['{table}' => '{param_name}']);
                Route::put('/{table}/{{id}}', [{controller_name}::class, 'update'])->name('{table}.update');
                """
                else:
                    # Si el archivo web.php no existe, crear uno nuevo
                    routes_content = "<?php\nuse Illuminate\\Support\\Facades\\Route;\n"
                    for table in all_tables:
                        model_name = ''.join([word.capitalize() for word in table.split('_')])  # Nombre del modelo en CamelCase
                        controller_name = f"{model_name}Controller"  # Nombre del controlador
                        param_name = self.shorten_param_name(primary_key)

                        routes_content += f"""
                use App\\Http\\Controllers\\{controller_name};

                Route::resource('{table}', {controller_name}::class)->parameters(['{table}' => '{param_name}']);
                Route::put('/{table}/{{id}}', [{controller_name}::class, 'update'])->name('{table}.update');
                """

                # Guardar el archivo web.php
                with open("routes/web.php", "w", encoding="utf-8", newline="\n") as routes_file:
                    routes_file.write(routes_content)
            
            # Actualizar welcome.blade.php de forma incremental
            welcome_path = "resources/views/welcome.blade.php"
            if os.path.exists(welcome_path):
                # Leer el contenido existente
                with open(welcome_path, "r", encoding="utf-8") as file:
                    welcome_content = file.read()
                
                # Buscar el bloque donde se insertan los enlaces
                start_marker = '<div class="list-group mt-3">'
                end_marker = '</div>'
                start_idx = welcome_content.find(start_marker) + len(start_marker)
                end_idx = welcome_content.find(end_marker, start_idx)
                existing_links = welcome_content[start_idx:end_idx].strip()
                
                # Obtener las tablas ya presentes
                existing_tables = set()
                for line in existing_links.splitlines():
                    if "route('" in line:
                        table_name = line.split("route('")[1].split(".index")[0]
                        existing_tables.add(table_name)
                
                # Añadir solo las nuevas tablas
                new_links = ""
                for table in tables_to_generate:
                    if table not in existing_tables:
                        table_name = table.replace('_', ' ').title()
                        new_links += f"""                        <a href="{{{{ route('{table}.index') }}}}" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                    {table_name}
                                    <span class="badge bg-primary rounded-pill"><i class="fa fa-chevron-right"></i></span>
                                </a>\n"""
                
                # Insertar las nuevas entradas antes del cierre del div
                if new_links:
                    welcome_content = welcome_content[:end_idx] + new_links + welcome_content[end_idx:]
            else:
                # Si no existe, crear el archivo desde cero
                welcome_content = """@extends('layouts.app')

    @section('content')
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">Bienvenido al Sistema CRUD</div>
                    <div class="card-body">
                        <h5>Modulos disponibles:</h5>
                        <div class="list-group mt-3">
    """
                for table in tables_to_generate:
                    table_name = table.replace('_', ' ').title()
                    welcome_content += f"""                        <a href="{{{{ route('{table}.index') }}}}" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                {table_name}
                                <span class="badge bg-primary rounded-pill"><i class="fa fa-chevron-right"></i></span>
                            </a>\n"""
                welcome_content += """                    </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    @endsection
    """
            
            # Guardar el archivo welcome.blade.php
            with open(welcome_path, "w", encoding="utf-8", newline="\n") as file:
                file.write(welcome_content)
            
            # Actualizar layouts/app.blade.php de forma incremental
            layout_path = "resources/views/layouts/app.blade.php"
            if os.path.exists(layout_path):
                # Leer el contenido existente
                with open(layout_path, "r", encoding="utf-8") as file:
                    layout_content = file.read()
                
                # Buscar el bloque de la navbar
                start_marker = '<ul class="navbar-nav">'
                end_marker = '</ul>'
                start_idx = layout_content.find(start_marker) + len(start_marker)
                end_idx = layout_content.find(end_marker, start_idx)
                existing_nav = layout_content[start_idx:end_idx].strip()
                
                # Obtener las tablas ya presentes en la navbar
                existing_tables = set()
                for line in existing_nav.splitlines():
                    if "route('" in line:
                        table_name = line.split("route('")[1].split(".index")[0]
                        existing_tables.add(table_name)
                
                # Añadir solo las nuevas tablas
                new_nav_items = ""
                for table in tables_to_generate:
                    if table not in existing_tables:
                        table_name = table.replace('_', ' ').title()
                        new_nav_items += f"""                    <li class="nav-item">
                            <a class="nav-link" href="{{{{ route('{table}.index') }}}}">{table_name}</a>
                        </li>\n"""
                
                # Insertar las nuevas entradas antes del cierre de ul
                if new_nav_items:
                    layout_content = layout_content[:end_idx] + new_nav_items + layout_content[end_idx:]
            else:
                # Si no existe, crear el archivo desde cero
                layout_content = """<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta name="csrf-token" content="{{ csrf_token() }}">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ config('app.name', 'Laravel CRUD') }}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <link href="https://cdn.datatables.net/1.12.1/css/dataTables.bootstrap5.min.css" rel="stylesheet">
        <link href="https://cdn.datatables.net/responsive/2.3.0/css/responsive.bootstrap5.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css">
        <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
        <style>
            body { background-color: #f8f9fa; }
            .navbar { margin-bottom: 20px; }
            .card { box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
            .card-header { background-color: #f8f9fa; border-bottom: 1px solid rgba(0, 0, 0, 0.125); }
            .btn { border-radius: 0.25rem; }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">{{ config('app.name', 'Laravel CRUD') }}</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Inicio</a>
                        </li>
    """
                for table in tables_to_generate:
                    table_name = table.replace('_', ' ').title()
                    layout_content += f"""                    <li class="nav-item">
                            <a class="nav-link" href="{{{{ route('{table}.index') }}}}">{table_name}</a>
                        </li>\n"""
                layout_content += """                </ul>
                </div>
            </div>
        </nav>

        <main>
            @yield('content')
        </main>

        <footer class="bg-light py-3 mt-5">
            <div class="container text-center">
                <p class="mb-0">© {{ date('Y') }} SHC131 Taller de Especialidad. Estudiante: Joaquin Aramayo Valdez.</p>
            </div>
        </footer>

        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        <script src="https://cdn.datatables.net/1.12.1/js/jquery.dataTables.min.js"></script>
        <script src="https://cdn.datatables.net/1.12.1/js/dataTables.bootstrap5.min.js"></script>
        <script src="https://cdn.datatables.net/responsive/2.3.0/js/dataTables.responsive.min.js"></script>
        <script src="https://cdn.datatables.net/responsive/2.3.0/js/responsive.bootstrap5.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.19.5/jquery.validate.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>

        @stack('scripts')
    </body>
    </html>
    """
            
            # Guardar el archivo app.blade.php
            os.makedirs("resources/views/layouts", exist_ok=True)
            with open(layout_path, "w", encoding="utf-8", newline="\n") as file:
                file.write(layout_content)
            
            messagebox.showinfo("Éxito", f"Modelos, controladores y vistas generados exitosamente en el proyecto existente!")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al generar los modelos: {e}")
        finally:
            conn.close()
    

    
    def create_project(self):
        # Crear un proyecto Laravel con CRUD basado en las tablas seleccionadas
        db = self.db_entry.get()  # Nombre de la base de datos
        port = self.port_entry.get()  # Puerto
        user = self.user_entry.get()  # Usuario
        password = self.password_entry.get()  # Contraseña
        project_name = self.project_entry.get()  # Nombre del proyecto

        # Validar que se haya ingresado un nombre de proyecto
        if not project_name:
            messagebox.showerror("Error", "Por favor, ingresa un nombre para el proyecto")
            return
        
        # Obtener lista de tablas seleccionadas
        tables_to_generate = [
            self.tree.item(item, "values")[1] for item in self.tree.get_children() if self.tree.item(item, "values")[0] == "✔"
        ]
        
        # Validar que se haya seleccionado al menos una tabla
        if not tables_to_generate:
            messagebox.showerror("Error", "Por favor, selecciona al menos una tabla")
            return

        try:
            # Conectar a la base de datos
            conn = psycopg2.connect(dbname=db, user=user, password=password, host="localhost", port=port)
            cursor = conn.cursor()

            # Identificar tablas relacionadas mediante claves foráneas
            related_tables = set()
            for table in tables_to_generate:
                if table in self.foreign_keys:
                    for fk in self.foreign_keys[table]:
                        related_tables.add(fk[1])

            all_tables = set(tables_to_generate).union(related_tables)  # Combinar tablas seleccionadas y relacionadas

            # Definir rutas para el proyecto Laravel
            base_project_path = "C:\\xampp\\htdocs\\TallerEspecialidad\\ProyectoSHC131\\laravel-base"  # Proyecto base
            new_project_path = os.path.join(os.getcwd(), project_name)  # Ruta del nuevo proyecto

            shutil.copytree(base_project_path, new_project_path)  # Copiar estructura del proyecto base
            os.chdir(new_project_path)  # Cambiar al directorio del nuevo proyecto

            # Configurar el archivo .env con los datos de conexión
            with open(".env.example", "r") as env_example_file:
                env_content = env_example_file.read()

            env_content = env_content.replace("DB_CONNECTION=mysql", "DB_CONNECTION=pgsql")  # Cambiar a PostgreSQL
            env_content = env_content.replace("DB_HOST=127.0.0.1", "DB_HOST=127.0.0.1")
            env_content = env_content.replace("DB_PORT=3306", f"DB_PORT={port}")
            env_content = env_content.replace("DB_DATABASE=laravel", f"DB_DATABASE={db}")
            env_content = env_content.replace("DB_USERNAME=root", f"DB_USERNAME={user}")
            env_content = env_content.replace("DB_PASSWORD=", f"DB_PASSWORD={password}")

            with open(".env", "w", encoding="utf-8", newline="\n") as env_file:
                env_file.write(env_content)  # Escribir archivo .env

            subprocess.run(["php", "artisan", "key:generate"], check=True)  # Generar clave de aplicación

            # Inicializar contenido del archivo de rutas
            routes_content = "<?php\n\nuse Illuminate\\Support\\Facades\\Route;\n\n"

            # Generar modelos, controladores y vistas para cada tabla
            for table in all_tables:
                model_name = ''.join([word.capitalize() for word in table.split('_')])  # Nombre del modelo en CamelCase
                controller_name = f"{model_name}Controller"  # Nombre del controlador
                
                routes_content += f"use App\\Http\\Controllers\\{controller_name};\n"

                # Obtener la clave primaria de la tabla
                cursor.execute(f"""
                    SELECT kcu.column_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu
                    ON tc.constraint_name = kcu.constraint_name
                    WHERE tc.table_schema = 'public'
                    AND tc.table_name = '{table}'
                    AND tc.constraint_type = 'PRIMARY KEY';
                """)
                primary_key = cursor.fetchone()
                primary_key = primary_key[0] if primary_key else "id"  # Usar "id" por defecto si no hay clave primaria

                # Obtener información de columnas y tipos de datos
                columns_info = self.table_columns[table]
                columns = [col[0] for col in columns_info]
                column_types = {col[0]: col[1] for col in columns_info}

                # Generar contenido del modelo
                model_content = f"""<?php

    namespace App\\Models;

    use Illuminate\\Database\\Eloquent\\Factories\\HasFactory;
    use Illuminate\\Database\\Eloquent\\Model;

    class {model_name} extends Model
    {{
        use HasFactory;

        protected $table = '{table}';
        protected $primaryKey = '{primary_key}';
        public $timestamps = false;

        protected $fillable = [
    """
                for column in columns:
                    if column != primary_key and column not in ["created_at", "updated_at"]:
                        model_content += f"        '{column}',\n"
                model_content += "    ];\n"

                # Agregar relaciones de claves foráneas
                if table in self.foreign_keys:
                    for fk in self.foreign_keys[table]:
                        column_name = fk[0]
                        foreign_table = fk[1]
                        foreign_model = ''.join([word.capitalize() for word in foreign_table.split('_')])
                        model_content += f"""
        public function {foreign_table}()
        {{
            return $this->belongsTo({foreign_model}::class, '{column_name}');
        }}
    """
                model_content += "}\n"

                # Guardar el modelo
                model_path = f"app/Models/{model_name}.php"
                os.makedirs(os.path.dirname(model_path), exist_ok=True)
                with open(model_path, "w", encoding="utf-8", newline="\n") as file:
                    file.write(model_content)

                print(f"Modelo generado para: {table}")

                # Generar contenido del controlador con mejoras dinámicas
                controller_content = f"""<?php
                namespace App\\Http\\Controllers;

                use App\\Models\\{model_name};
                use Illuminate\\Http\\Request;
                use Yajra\\DataTables\\Facades\\DataTables;
                use Illuminate\\Support\\Facades\\DB;

                class {controller_name} extends Controller
                {{
                    public function index(Request $request)
                    {{
                        if ($request->ajax()) {{
                            ${table} = {model_name}::select('{table}.*');
                """
                if table in self.foreign_keys:
                    relationships = list({fk[1] for fk in self.foreign_keys[table]})
                    if relationships:
                        rel_list = ', '.join([f"'{rel}'" for rel in relationships])
                        controller_content += f"            ${table} = ${table}->with([{rel_list}]);\n"

                controller_content += f"""
                            return DataTables::of(${table})
                """
                for column in columns:
                    if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                        fk_info = next(fk for fk in self.foreign_keys[table] if fk[0] == column)
                        foreign_table = fk_info[1]
                        foreign_column = fk_info[2]
                        descriptive_field = self.get_descriptive_field(foreign_table, cursor, foreign_column)
                        # Si el usuario eligió un campo, usarlo
                        if foreign_table in self.chosen_fields:
                            descriptive_field = self.chosen_fields[foreign_table]
                        controller_content += f"""                ->addColumn('{column}_display', function ($row) {{
                                            return $row->{foreign_table} ? ($row->{foreign_table}->{descriptive_field} ?? $row->{column}) : $row->{column};
                                        }})\n"""
                controller_content += f"""                ->addColumn('action', function ($row) {{
                                    $btn = '<button class="btn btn-info btn-sm viewRecord" data-id="' . $row->{primary_key} . '">Ver</button>';
                                    $btn .= ' <button class="btn btn-primary btn-sm editRecord" data-id="' . $row->{primary_key} . '">Editar</button>';
                                    $btn .= ' <button class="btn btn-danger btn-sm deleteRecord" data-id="' . $row->{primary_key} . '">Eliminar</button>';
                                    return $btn;
                                }})
                                ->rawColumns(['action'])
                                ->make(true);
                        }}

                        return view('{table}.index');
                    }}

                    public function store(Request $request)
                    {{
                        try {{
                            $request->validate([
                """
                for column, col_type in columns_info:
                    if column != primary_key:
                        if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                            fk_info = next(fk for fk in self.foreign_keys[table] if fk[0] == column)
                            foreign_table = fk_info[1]
                            foreign_column = fk_info[2]
                            controller_content += f"                '{column}' => 'required|exists:{foreign_table},{foreign_column}',\n"
                        elif col_type in ('character varying', 'text', 'varchar'):
                            if column in ('escudo', 'imagen', 'foto', 'image'):
                                controller_content += f"                '{column}' => 'nullable|file|mimes:jpg,png|max:2048',\n"
                            else:
                                controller_content += f"                '{column}' => 'required|string|max:255',\n"
                        elif col_type == 'date':
                            controller_content += f"                '{column}' => 'required|date',\n"
                        elif col_type in ('integer', 'bigint', 'smallint'):
                            controller_content += f"                '{column}' => 'required|integer',\n"
                        elif col_type == 'numeric':
                            controller_content += f"                '{column}' => 'required|numeric',\n"
                        elif column == 'estado':
                            controller_content += f"                '{column}' => 'required|in:A,I',\n"
                        else:
                            controller_content += f"                '{column}' => 'required',\n"

                controller_content += f"""            ]);

                            $data = $request->all();
                """
                for column in columns:
                    if column in ('escudo', 'imagen', 'foto', 'image'):
                        controller_content += f"""            if ($request->hasFile('{column}')) {{
                                $data['{column}'] = $request->file('{column}')->store('{column}s', 'public');
                            }}\n"""

                controller_content += f"""
                            ${table} = {model_name}::create($data);
                            return response()->json(${table}, 201);
                        }} catch (\\Exception $e) {{
                            return response()->json(['error' => $e->getMessage()], 500);
                        }}
                    }}

                    public function edit($id)
                    {{
                        ${table} = {model_name}::findOrFail($id);
                        return response()->json(${table});
                    }}

                    public function update(Request $request, $id)
                    {{
                        try {{
                            $request->validate([
                """
                for column, col_type in columns_info:
                    if column != primary_key:
                        if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                            fk_info = next(fk for fk in self.foreign_keys[table] if fk[0] == column)
                            foreign_table = fk_info[1]
                            foreign_column = fk_info[2]
                            controller_content += f"                '{column}' => 'required|exists:{foreign_table},{foreign_column}',\n"
                        elif col_type in ('character varying', 'text', 'varchar'):
                            if column in ('escudo', 'imagen', 'foto', 'image'):
                                controller_content += f"                '{column}' => 'nullable|file|mimes:jpg,png|max:2048',\n"
                            else:
                                controller_content += f"                '{column}' => 'required|string|max:255',\n"
                        elif col_type == 'date':
                            controller_content += f"                '{column}' => 'required|date',\n"
                        elif col_type in ('integer', 'bigint', 'smallint'):
                            controller_content += f"                '{column}' => 'required|integer',\n"
                        elif col_type == 'numeric':
                            controller_content += f"                '{column}' => 'required|numeric',\n"
                        elif column == 'estado':
                            controller_content += f"                '{column}' => 'required|in:A,I',\n"
                        else:
                            controller_content += f"                '{column}' => 'required',\n"

                controller_content += f"""            ]);

                            ${table} = {model_name}::findOrFail($id);
                            $data = $request->all();

                            // Manejar archivos de imagen
                """
                for column in columns:
                    if column in ('escudo', 'imagen', 'foto', 'image'):
                        controller_content += f"""            if ($request->hasFile('{column}')) {{
                                // Eliminar imagen anterior si existe
                                if (${table}->{column} && Storage::disk('public')->exists(${table}->{column})) {{
                                    Storage::disk('public')->delete(${table}->{column});
                                }}
                                $data['{column}'] = $request->file('{column}')->store('{column}s', 'public');
                            }} else {{
                                // Mantener la imagen existente si no se sube una nueva
                                unset($data['{column}']);
                            }}\n"""

                controller_content += f"""
                            ${table}->update($data);
                            return response()->json(${table});
                        }} catch (\\Illuminate\\Validation\\ValidationException $e) {{
                            return response()->json(['errors' => $e->errors()], 422);
                        }} catch (\\Exception $e) {{
                            return response()->json(['error' => $e->getMessage()], 500);
                        }}
                    }}
                    public function show($id)
                    {{
                        ${table} = {model_name}::findOrFail($id);
                        return response()->json(${table});
                    }}

                    public function destroy($id)
                    {{
                        try {{
                            ${table} = {model_name}::findOrFail($id);
                            ${table}->delete();
                            DB::statement("SELECT setval(pg_get_serial_sequence('{table}', '{primary_key}'), COALESCE((SELECT MAX({primary_key}) FROM {table}), 1))");
                            return response()->json(['message' => 'Registro eliminado exitosamente']);
                        }} catch (\\Exception $e) {{
                            return response()->json(['error' => $e->getMessage()], 500);
                        }}
                    }}
                }}"""

                # Guardar el controlador
                controller_path = f"app/Http/Controllers/{controller_name}.php"
                os.makedirs(os.path.dirname(controller_path), exist_ok=True)
                with open(controller_path, "w", encoding="utf-8", newline="\n") as file:
                    file.write(controller_content)

                print(f"Controlador generado para: {table}")

                # Agregar rutas al archivo de rutas
                param_name = self.shorten_param_name(primary_key)
                routes_content += f"""
    Route::resource('{table}', {controller_name}::class)->parameters([
        '{table}' => '{param_name}',
    ]);
    Route::put('/{table}/{{id}}', [{controller_name}::class, 'update'])->name('{table}.update');
    """

                os.makedirs(f"resources/views/{table}", exist_ok=True)

                # Generar la vista index.blade.php dinámicamente
                index_view = f"""@extends('layouts.app')

                @section('content')
                <div class="container">
                    <div class="row">
                        <div class="col-md-12">
                            <div class="card">
                                <div class="card-header">
                                    <div class="d-flex justify-content-between align-items-center">
                                        <h5><i class="fa fa-table"></i> Lista de {table.replace('_', ' ').title()}</h5>
                                        <button class="btn btn-success" id="createNewRecord">
                                            <i class="fa fa-plus"></i> Nuevo
                                        </button>
                                    </div>
                                </div>
                                <div class="card-body">
                                    @if ($message = Session::get('success'))
                                        <div class="alert alert-success">
                                            <p>{{{{ $message }}}}</p>
                                        </div>
                                    @endif

                                    <table class="table table-bordered table-striped data-table">
                                        <thead>
                                            <tr>
                """
                for column in columns:
                    if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                        foreign_table = next(fk[1] for fk in self.foreign_keys[table] if fk[0] == column)
                        index_view += f"                                <th>{foreign_table.replace('_', ' ').title()}</th>\n"
                    else:
                        index_view += f"                                <th>{column.replace('_', ' ').title()}</th>\n"
                index_view += """                                <th width="280px">Acciones</th>
                                            </tr>
                                        </thead>
                                        <tbody></tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Modal para crear/editar registros -->
                <div class="modal fade" id="ajaxModel" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title"></h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <form id="form">
                                    @csrf
                                    <input type="hidden" name="id" id="table_id">
                """
                for column, col_type in columns_info:
                    if column != primary_key:
                        if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                            fk_info = next(fk for fk in self.foreign_keys[table] if fk[0] == column)
                            foreign_table = fk_info[1]
                            foreign_column = fk_info[2]
                            foreign_model = ''.join([word.capitalize() for word in foreign_table.split('_')])
                            descriptive_field = self.get_descriptive_field(foreign_table, cursor, foreign_column)
                            # Si el usuario eligió un campo, usarlo
                            if foreign_table in self.chosen_fields:
                                descriptive_field = self.chosen_fields[foreign_table]
                            index_view += f"""
                                <div class="mb-3">
                                    <label for="{column}" class="form-label">{foreign_table.replace('_', ' ').title()}</label>
                                    <select class="form-control" id="{column}" name="{column}" required>
                                        <option value="">Seleccione una opción</option>
                                        @foreach(\\App\\Models\\{foreign_model}::all() as $item)
                                            <option value="{{{{ $item->{foreign_column} }}}}" {{{{ old('{column}') == $item->{foreign_column} ? 'selected' : '' }}}}>
                                                {{{{ $item->{descriptive_field} ?? $item->{foreign_column} }}}}
                                            </option>
                                        @endforeach
                                    </select>
                                </div>
                            """
                        elif col_type == "date":
                            index_view += f"""
                                    <div class="mb-3">
                                        <label for="{column}" class="form-label">{column.replace('_', ' ').title()}</label>
                                        <input type="text" class="form-control datepicker" id="{column}" name="{column}" required readonly>
                                    </div>
                """
                        elif column in ('escudo', 'imagen', 'foto', 'image'):
                            index_view += f"""
                                    <div class="mb-3">
                                        <label for="{column}" class="form-label">{column.replace('_', ' ').title()}</label>
                                        <input type="file" class="form-control" id="{column}" name="{column}">
                                    </div>
                """
                        elif column == "estado":
                            index_view += f"""
                                    <div class="mb-3">
                                        <label for="{column}" class="form-label">{column.replace('_', ' ').title()}</label>
                                        <select class="form-control" id="{column}" name="{column}" required>
                                            <option value="A">Activo</option>
                                            <option value="I">Inactivo</option>
                                        </select>
                                    </div>
                """
                        elif col_type in ('integer', 'bigint', 'smallint'):
                            index_view += f"""
                                    <div class="mb-3">
                                        <label for="{column}" class="form-label">{column.replace('_', ' ').title()}</label>
                                        <input type="number" class="form-control" id="{column}" name="{column}" required>
                                    </div>
                """
                        elif col_type == 'numeric':
                            index_view += f"""
                                    <div class="mb-3">
                                        <label for="{column}" class="form-label">{column.replace('_', ' ').title()}</label>
                                        <input type="number" step="any" class="form-control" id="{column}" name="{column}" required>
                                    </div>
                """
                        else:
                            index_view += f"""
                                    <div class="mb-3">
                                        <label for="{column}" class="form-label">{column.replace('_', ' ').title()}</label>
                                        <input type="text" class="form-control" id="{column}" name="{column}" required>
                                    </div>
                """

                index_view += """
                                    <button type="submit" class="btn btn-primary">Guardar</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Modal para eliminar registros -->
                <div class="modal fade" id="deleteModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Eliminar Registro</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <p>¿Estás seguro de que deseas eliminar este registro?</p>
                                <form id="deleteForm">
                                    @csrf
                                    @method('DELETE')
                                    <input type="hidden" id="delete_id" name="id">
                                    <button type="submit" class="btn btn-danger">Eliminar</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Modal para ver detalles -->
                <div class="modal fade" id="viewModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Detalles</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                """
                for column in columns:
                    if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                        foreign_table = next(fk[1] for fk in self.foreign_keys[table] if fk[0] == column)
                        descriptive_field = self.get_descriptive_field(foreign_table, cursor, primary_key)  # <-- Añade esta línea
                        index_view += f"""
                            <p><strong>{foreign_table.replace('_', ' ').title()}:</strong> 
                            <span id="view_{column}"></span>
                            </p>
                        """
                    else:
                        index_view += f"""<p><strong>{column.replace('_', ' ').title()}:</strong> <span id="view_{column}"></span></p>\n"""

                index_view += f"""            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                            </div>
                        </div>
                    </div>
                </div>

                @push('scripts')
                <script>
                    var URLindex = "{{{{ route('{table}.index') }}}}";
                    var URLstore = "{{{{ route('{table}.store') }}}}";
                    var URLupdate = "{{{{ route('{table}.update', ':id') }}}}";
                    var titulo = "{table.replace('_', ' ').title()}";
                    var columnas = [
                """
                for column in columns:
                    if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                        index_view += f"""        {{
                            data: '{column}_display',
                            name: '{column}'
                        }},
                """
                    else:
                        index_view += f"""        {{
                            data: '{column}',
                            name: '{column}'
                        }},
                """
                index_view += """        {
                            data: 'action',
                            name: 'action',
                            orderable: false,
                            searchable: false
                        }
                    ];

                    (function() {
                        'use strict';

                        $.ajaxSetup({
                            headers: {
                                'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
                            }
                        });

                        var table = $('.data-table').DataTable({
                            processing: true,
                            serverSide: true,
                            ajax: URLindex,
                            columns: columnas,
                            order: [[0, 'asc']],
                            scrollX: true,
                            responsive: true,
                            autoWidth: false,
                        });

                        $('.datepicker').datepicker({
                            dateFormat: 'yy-mm-dd',
                            changeMonth: true,
                            changeYear: true,
                            yearRange: '-100:+10'
                        });

                        $('#form').on('submit', function(e) {
                            e.preventDefault();
                            var formData = new FormData(this);
                            var tableId = $('#table_id').val().trim();
                            var method = tableId ? 'PUT' : 'POST';
                            var url = tableId ? URLupdate.replace(':id', tableId) : URLstore;

                            // Agregar el método PUT para actualizaciones
                            if (method === 'PUT') {
                                formData.append('_method', 'PUT');
                            }

                            $.ajax({
                                url: url,
                                method: 'POST', // Siempre usar POST para enviar archivos
                                data: formData,
                                processData: false,
                                contentType: false,
                                success: function(data) {
                                    $('#form').trigger("reset");
                                    $('#table_id').val('');
                                    $('#ajaxModel').modal('hide');
                                    toastr['success']('Registro guardado correctamente.');
                                    table.draw(false);
                                },
                                error: function(xhr) {
                                    var errors = xhr.responseJSON.errors;
                                    if (errors) {
                                        Object.keys(errors).forEach(function(key) {
                                            toastr['error'](errors[key][0]);
                                        });
                                    } else {
                                        toastr['error']('Ocurrió un error: ' + (xhr.responseJSON ? xhr.responseJSON.message : 'Desconocido'));
                                    }
                                    console.log('Errores:', xhr.responseJSON);
                                }
                            });
                        });

                        $('#createNewRecord').on("click", function() {
                            $('#table_id').val('');
                            $('#form')[0].reset();
                            $('.modal-title').html("Crear nuevo " + titulo);
                            $('#ajaxModel').modal('show');
                        });

                        $('body').on('click', '.viewRecord', function() {
                            var table_id = $(this).data('id');
                            $.get(URLindex + '/' + table_id, function(data) {
                                $('.modal-title').html("Detalles de " + titulo);
                """
                for column in columns:
                    if column in [fk[0] for fk in self.foreign_keys.get(table, [])]:
                        foreign_table = next(fk[1] for fk in self.foreign_keys[table] if fk[0] == column)
                        descriptive_field = self.get_descriptive_field(foreign_table, cursor, primary_key)
                        index_view += f"""
                            $('#view_{column}').text(data.{foreign_table} ? (data.{foreign_table}.{descriptive_field} ?? data.{column}) : 'N/A');
                        """
                    else:
                        index_view += f"""
                            $('#view_{column}').text(data.{column} || 'N/A');
                        """

                index_view += f"""
                                $('#viewModal').modal('show');
                            }}).fail(function(xhr) {{
                                toastr['error']('Error al obtener los datos: ' + xhr.responseJSON.message);
                            }});
                        }});

                        $('body').on('click', '.editRecord', function() {{
                            var table_id = $(this).data("id");
                            $.get(URLindex + '/' + table_id + '/edit', function(data) {{
                                $('.modal-title').html("Editar " + titulo);
                                $('#ajaxModel').modal('show');
                                $('#table_id').val(data.{primary_key});
                """
                for column in columns:
                    if column != primary_key and column not in ('escudo', 'imagen', 'foto', 'image'):  # No pre-cargar archivos
                        index_view += f"                $('#{column}').val(data.{column});\n"

                index_view += """            }).fail(function(xhr) {
                                toastr['error']('Error al obtener los datos: ' + xhr.responseJSON.message);
                            });
                        });

                        $('body').on('click', '.deleteRecord', function() {
                            var table_id = $(this).data("id");
                            if (confirm("¿Confirma borrar el registro?")) {
                                $.ajax({
                                    type: "DELETE",
                                    url: URLindex + '/' + table_id,
                                    success: function(data) {
                                        toastr['success']('Registro borrado correctamente.');
                                        table.draw();
                                    },
                                    error: function(xhr) {
                                        toastr['error']('Ocurrió un error: ' + (xhr.responseJSON ? xhr.responseJSON.message : 'Desconocido'));
                                    }
                                });
                            }
                        });
                    })();
                </script>
                @endpush
                @endsection
                """

                # Guardar la vista
                with open(f"resources/views/{table}/index.blade.php", "w", encoding="utf-8", newline="\n") as file:
                    file.write(index_view)

                print(f"Vistas CRUD generadas para: {table}")

            # Generar el layout principal (app.blade.php)
            layout_content = """<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta name="csrf-token" content="{{ csrf_token() }}">
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ config('app.name', 'Laravel CRUD') }}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <link href="https://cdn.datatables.net/1.12.1/css/dataTables.bootstrap5.min.css" rel="stylesheet">
        <link href="https://cdn.datatables.net/responsive/2.3.0/css/responsive.bootstrap5.min.css" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css">
        <link rel="stylesheet" href="https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">
        <style>
            body { background-color: #f8f9fa; }
            .navbar { margin-bottom: 20px; }
            .card { box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px; }
            .card-header { background-color: #f8f9fa; border-bottom: 1px solid rgba(0, 0, 0, 0.125); }
            .btn { border-radius: 0.25rem; }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">{{ config('app.name', 'Laravel CRUD') }}</a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item">
                            <a class="nav-link" href="/">Inicio</a>
                        </li>
    """
            for table in tables_to_generate:
                table_name = table.replace('_', ' ').title()
                layout_content += f"""                    <li class="nav-item">
                            <a class="nav-link" href="{{{{ route('{table}.index') }}}}">{table_name}</a>
                        </li>\n"""

            layout_content += """                </ul>
                </div>
            </div>
        </nav>

        <main>
            @yield('content')
        </main>

        <footer class="bg-light py-3 mt-5">
            <div class="container text-center">
                <p class="mb-0">© {{ date('Y') }} SHC131 Taller de Especialidad. Estudiante: Joaquin Aramayo Valdez.</p>
            </div>
        </footer>

        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/js/bootstrap.bundle.min.js"></script>
        <script src="https://cdn.datatables.net/1.12.1/js/jquery.dataTables.min.js"></script>
        <script src="https://cdn.datatables.net/1.12.1/js/dataTables.bootstrap5.min.js"></script>
        <script src="https://cdn.datatables.net/responsive/2.3.0/js/dataTables.responsive.min.js"></script>
        <script src="https://cdn.datatables.net/responsive/2.3.0/js/responsive.bootstrap5.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-validate/1.19.5/jquery.validate.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>

        @stack('scripts')
    </body>
    </html>
    """

            # Guardar el layout
            os.makedirs("resources/views/layouts", exist_ok=True)
            with open("resources/views/layouts/app.blade.php", "w", encoding="utf-8", newline="\n") as file:
                file.write(layout_content)

            # Generar la vista de bienvenida
            welcome_content = """@extends('layouts.app')

    @section('content')
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header">Bienvenido al Sistema CRUD</div>
                    <div class="card-body">
                        <h5>Modulos disponibles:</h5>
                        <div class="list-group mt-3">
    """
            for table in tables_to_generate:
                table_name = table.replace('_', ' ').title()
                welcome_content += f"""                        <a href="{{{{ route('{table}.index') }}}}" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center">
                                {table_name}
                                <span class="badge bg-primary rounded-pill"><i class="fa fa-chevron-right"></i></span>
                            </a>\n"""

            welcome_content += """                    </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    @endsection
    """

            with open("resources/views/welcome.blade.php", "w", encoding="utf-8", newline="\n") as file:
                file.write(welcome_content)

            # Agregar ruta de bienvenida
            routes_content += """
    Route::get('/', function () {
        return view('welcome');
    });
    """

            # Guardar el archivo de rutas
            with open("routes/web.php", "w", encoding="utf-8", newline="\n") as file:
                file.write(routes_content)

            # Configurar almacenamiento para archivos
            subprocess.run(["php", "artisan", "storage:link"], check=True)

            # Iniciar el servidor y abrir en el navegador
            subprocess.Popen(["php", "artisan", "serve"])
            webbrowser.open("http://127.0.0.1:8000")

            messagebox.showinfo("Éxito", f"Proyecto Laravel {project_name} creado exitosamente con vistas CRUD dinámicas!")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al crear el proyecto: {e}")
        finally:
            conn.close()





if __name__ == "__main__":
    # Punto de entrada del programa: iniciar la ventana de inicio de sesión
    app = Login()
    app.ventana.mainloop()