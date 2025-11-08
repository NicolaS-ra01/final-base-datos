

import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
import pyodbc
from datetime import datetime

# ---------------- CONFIG CONEXIÓN (AJUSTA AQUÍ SI CAMBIA) ----------------
DRIVER = "ODBC Driver 18 for SQL Server"
SERVER = "localhost,1433"
DATABASE = "CafeteriaDB_MS"
UID = "sa"
PWD = "TuContraseña123!"  
CONN_TIMEOUT = 15

def conectar_bd():
    cs = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        f"UID={UID};PWD={PWD};"
        "Encrypt=no;TrustServerCertificate=yes;Connection Timeout=" + str(CONN_TIMEOUT) + ";"
    )
    try:
        return pyodbc.connect(cs)
    except Exception as e:
        messagebox.showerror("DB error", f"No se pudo conectar a la DB:\n{e}")
        return None


BG = "#F6F3EE"        
ACCENT = "#6B4F3A"    
ACCENT_LIGHT = "#A67C52"
CARD = "#FFFFFF"
TEXT = "#222222"

def setup_style(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except:
        pass
    style.configure("TFrame", background=BG)
    style.configure("Card.TFrame", background=CARD, relief="flat")
    style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 10))
    style.configure("Title.TLabel", font=("Segoe UI", 14, "bold"), foreground=ACCENT)
    style.configure("Accent.TButton", background=ACCENT, foreground="white", font=("Segoe UI", 10, "bold"))
    style.map("Accent.TButton", background=[('active', ACCENT_LIGHT)])
    style.configure("Danger.TButton", background="#c74b4b", foreground="white")
    style.configure("Treeview", background="white", fieldbackground="white", foreground=TEXT)
    style.configure("TNotebook", background=BG)
    style.configure("TNotebook.Tab", padding=(10,8), font=("Segoe UI", 10, "bold"))
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

# ---------------- UTILIDADES ----------------
def decimal_to_str(v):
    if v is None:
        return ""

    if isinstance(v, Decimal):
        return format(v, ".2f")
    try:

        return format(Decimal(str(v)), ".2f")
    except:
        return str(v)

# ---------------- APLICACIÓN ----------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Cafetería — Panel")
        root.geometry("1100x700")
        root.configure(background=BG)
        setup_style(root)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=18, pady=18)
        

        self.productos_map = {}

        self.empleados_map = {}
 
        self.current_pedido_id = None

        self.tab_home()
        self.tab_productos()
        self.tab_empleados()
        self.tab_ingredientes()
        self.tab_registrar_venta()

        # Carga inicial
        self.refresh_home()
        

    # ---------------- HOME ----------------
    def tab_home(self):
        f = ttk.Frame(self.notebook)
        f.configure(style="TFrame")
        self.notebook.add(f, text="Inicio")
        card = ttk.Frame(f, style="Card.TFrame", padding=20)
        card.pack(fill="both", expand=True, padx=30, pady=30)

        ttk.Label(card, text="Panel de Gestión - Cafetería", style="Title.TLabel").pack(anchor="w")
        ttk.Label(card, text="Bienvenido. Usa las pestañas para administrar productos, empleados,\ningredientes y registrar ventas.", justify="left").pack(anchor="w", pady=(10,0))

        self.stats_frame = ttk.Frame(card, style="Card.TFrame")
        self.stats_frame.pack(fill="x", pady=20)
        self._stat_card(self.stats_frame, "Productos", self.count_productos).pack(side="left", padx=8)
        self._stat_card(self.stats_frame, "Empleados", self.count_empleados).pack(side="left", padx=8)
        self._stat_card(self.stats_frame, "Ingredientes", self.count_ingredientes).pack(side="left", padx=8)

        ttk.Button(card, text="Actualizar estadísticas", style="Accent.TButton", command=self.refresh_home).pack(anchor="e")

    def _stat_card(self, master, title, func):
        frame = ttk.Frame(master, style="Card.TFrame", padding=12)
        ttk.Label(frame, text=title, font=("Segoe UI", 10, "bold")).pack(anchor="w")
        val = tk.StringVar(value="...")
        ttk.Label(frame, textvariable=val, font=("Segoe UI", 18)).pack(anchor="w")
        frame._val_var = val
        frame._func = func
        return frame

    def refresh_home(self):

        try:
            for card in self.stats_frame.winfo_children():
                if hasattr(card, "_func"):
                    try:
                        card._val_var.set(str(card._func()))
                    except Exception as e:
                        print(f"Error al actualizar estadística: {e}")
                        card._val_var.set("N/A")
        except AttributeError:
             pass

    def count_productos(self):
        conn = conectar_bd()
        if not conn: return 0
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM Productos")
            v = cur.fetchone()[0]
            return v
        except Exception:
            return 0
        finally:
            conn.close()

    def count_empleados(self):
        conn = conectar_bd()
        if not conn: return 0
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM Empleados")
            v = cur.fetchone()[0]
            return v
        except Exception:
            return 0
        finally:
            conn.close()

    def count_ingredientes(self):
        conn = conectar_bd()
        if not conn: return 0
        cur = conn.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM Ingredientes")
            v = cur.fetchone()[0]
            return v
        except Exception:
            return 0
        finally:
            conn.close()

    # ---------------- PRODUCTOS (CRUD) ----------------
    def tab_productos(self):
        f = ttk.Frame(self.notebook)
        self.notebook.add(f, text="Productos")
        container = ttk.Frame(f, style="Card.TFrame", padding=14)
        container.pack(fill="both", expand=True, padx=18, pady=12)

        left = ttk.Frame(container)
        left.pack(side="left", fill="both", expand=True)

        cols = ("ID", "Nombre", "Descripción", "Precio", "Tipo", "Stock")
        self.tree_productos = ttk.Treeview(left, columns=cols, show="headings", height=20)
        for c in cols:
            self.tree_productos.heading(c, text=c)
            if c == "Descripción":
                self.tree_productos.column(c, width=380)
            elif c == "Nombre":
                self.tree_productos.column(c, width=160)
            else:
                self.tree_productos.column(c, width=100, anchor="center")
        self.tree_productos.pack(fill="both", expand=True, pady=(0,8))

        btns = ttk.Frame(left)
        btns.pack(fill="x")
        ttk.Button(btns, text="Agregar", style="Accent.TButton", command=self.open_add_producto).pack(side="left", padx=6)
        ttk.Button(btns, text="Editar", command=self.open_edit_producto).pack(side="left", padx=6)
        ttk.Button(btns, text="Eliminar", style="Danger.TButton", command=self.delete_producto).pack(side="left", padx=6)
        ttk.Button(btns, text="Actualizar", command=self.load_productos).pack(side="left", padx=6)

        right = ttk.Frame(container, width=300)
        right.pack(side="left", fill="y", padx=(12,0))
        ttk.Label(right, text="Filtro por tipo").pack(anchor="w")
        self.tipo_filter = tk.StringVar()
        ttk.Entry(right, textvariable=self.tipo_filter).pack(fill="x", pady=6)
        ttk.Button(right, text="Filtrar", command=self.filter_productos).pack(fill="x")
        ttk.Separator(right).pack(fill="x", pady=12)
        ttk.Label(right, text="Producto seleccionado:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.info_sel = tk.Text(right, height=8, width=34)
        self.info_sel.pack()
        ttk.Button(right, text="Limpiar selección", command=lambda: [self.tree_productos.selection_remove(i) for i in self.tree_productos.selection()]).pack(pady=6)
        self.tree_productos.bind("<<TreeviewSelect>>", self.show_producto_info)

        self.load_productos()

    def load_productos(self):
        conn = conectar_bd()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute("SELECT producto_id, nombre, descripcion, precio, tipo_producto, stock FROM Productos ORDER BY producto_id")
            rows = cur.fetchall()
            for i in self.tree_productos.get_children():
                self.tree_productos.delete(i)
            for r in rows:
                self.tree_productos.insert("", "end", values=(r[0], r[1], r[2], decimal_to_str(r[3]), r[4], r[5]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar productos:\n{e}")
        finally:
            conn.close()

    def filter_productos(self):
        tipo = self.tipo_filter.get().strip()
        conn = conectar_bd()
        if not conn: return
        cur = conn.cursor()
        try:
            if tipo:
                cur.execute("SELECT producto_id, nombre, descripcion, precio, tipo_producto, stock FROM Productos WHERE tipo_producto = ? ORDER BY producto_id", (tipo,))
            else:
                self.load_productos()
                return
            rows = cur.fetchall()
            for i in self.tree_productos.get_children():
                self.tree_productos.delete(i)
            for r in rows:
                self.tree_productos.insert("", "end", values=(r[0], r[1], r[2], decimal_to_str(r[3]), r[4], r[5]))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo filtrar:\n{e}")
        finally:
            conn.close()

    def show_producto_info(self, ev=None):
        sel = self.tree_productos.selection()
        self.info_sel.delete("1.0", tk.END)
        if not sel:
            return
        vals = self.tree_productos.item(sel[0], "values")
        txt = f"ID: {vals[0]}\nNombre: {vals[1]}\nTipo: {vals[4]}\nPrecio: {vals[3]}\nStock: {vals[5]}\n\nDescripción:\n{vals[2]}"
        self.info_sel.insert("1.0", txt)

    def open_add_producto(self):
        ProductoEditor(self.root, app=self, callback=self.load_productos)

    def open_edit_producto(self):
        sel = self.tree_productos.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un producto para editar.")
            return
        vals = self.tree_productos.item(sel[0], "values")
        ProductoEditor(self.root, app=self, callback=self.load_productos, datos=vals)

    def delete_producto(self):
        sel = self.tree_productos.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un producto para eliminar.")
            return
        vals = self.tree_productos.item(sel[0], "values")
        pid = vals[0]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar producto {vals[1]} (ID {pid})?"):
            return
        conn = conectar_bd()
        if not conn: return
        cur = conn.cursor()
        try:
   
            cur.execute("EXEC SP_EliminarProducto ?", (pid,))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto eliminado.")
            self.load_productos()
            self.refresh_home()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")
        finally:
            conn.close()

    # ---------------- EMPLEADOS (LECTURA) ----------------
    def tab_empleados(self):
        f = ttk.Frame(self.notebook)
        self.notebook.add(f, text="Empleados")
        panel = ttk.Frame(f, style="Card.TFrame", padding=12)
        panel.pack(fill="both", expand=True, padx=18, pady=12)

        cols = ("ID", "Nombre", "Apellido", "Cargo", "Fecha", "Salario")
        self.tree_emps = ttk.Treeview(panel, columns=cols, show="headings", height=20)
        for c in cols:
            self.tree_emps.heading(c, text=c)
            self.tree_emps.column(c, width=140, anchor="center")
        self.tree_emps.pack(fill="both", expand=True)

        btns = ttk.Frame(panel)
        btns.pack(fill="x", pady=8)
        ttk.Button(btns, text="Actualizar", style="Accent.TButton", command=self.load_empleados).pack(side="left")
        self.load_empleados()

    def load_empleados(self):
        conn = conectar_bd()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute("SELECT empleado_id, nombre, apellido, cargo, fecha_contratacion, salario FROM Empleados ORDER BY empleado_id")
            rows = cur.fetchall()
            for i in self.tree_emps.get_children():
                self.tree_emps.delete(i)
            for r in rows:
                fecha_str = r[4].strftime("%Y-%m-%d") if isinstance(r[4], datetime) else str(r[4])
                self.tree_emps.insert("", "end", values=(r[0], r[1], r[2], r[3], fecha_str, decimal_to_str(r[5])))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar empleados:\n{e}")
        finally:
            conn.close()

    # ---------------- INGREDIENTES (LECTURA) ----------------
    def tab_ingredientes(self):
        f = ttk.Frame(self.notebook)
        self.notebook.add(f, text="Ingredientes")
        panel = ttk.Frame(f, style="Card.TFrame", padding=12)
        panel.pack(fill="both", expand=True, padx=18, pady=12)

        cols = ("ID", "Ingrediente", "Unidad", "Stock Actual", "Stock Mínimo")
        self.tree_ing = ttk.Treeview(panel, columns=cols, show="headings", height=20)
        for c in cols:
            self.tree_ing.heading(c, text=c)
            self.tree_ing.column(c, width=160, anchor="center")
        self.tree_ing.pack(fill="both", expand=True)

        btns = ttk.Frame(panel)
        btns.pack(fill="x", pady=8)
        ttk.Button(btns, text="Actualizar", style="Accent.TButton", command=self.load_ingredientes).pack(side="left")
        self.load_ingredientes()

    def load_ingredientes(self):
        conn = conectar_bd()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute("SELECT ingrediente_id, nombre_ingrediente, unidad_medida, stock_actual, stock_minimo FROM Ingredientes ORDER BY ingrediente_id")
            rows = cur.fetchall()
            for i in self.tree_ing.get_children():
                self.tree_ing.delete(i)
            for r in rows:
                self.tree_ing.insert("", "end", values=(r[0], r[1], r[2], decimal_to_str(r[3]), decimal_to_str(r[4])))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar ingredientes:\n{e}")
        finally:
            conn.close()

    # ---------------- REGISTRAR VENTAS ----------------
    def tab_registrar_venta(self):
        f = ttk.Frame(self.notebook)

        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)
        self.notebook.add(f, text="Registrar Venta")
        panel = ttk.Frame(f, style="Card.TFrame", padding=12)
        panel.pack(fill="both", expand=True, padx=18, pady=12)

        left = ttk.Frame(panel)
        left.pack(side="left", fill="y", padx=(0,12))


        ttk.Label(left, text="Empleado (Nombre)").pack(anchor="w")
        self.v_emp_nombre = tk.StringVar()
        self.combo_emp = ttk.Combobox(left, textvariable=self.v_emp_nombre, state="readonly")
        self.combo_emp.pack(fill="x", pady=6)
        
        ttk.Label(left, text="Estado (Entregado/Pendiente)").pack(anchor="w")
        self.v_estado = tk.StringVar(value="Entregado")
        ttk.Entry(left, textvariable=self.v_estado).pack(fill="x", pady=6)
        ttk.Button(left, text="Crear Pedido Vacío", style="Accent.TButton", command=self.crear_pedido_base).pack(fill="x", pady=6)

        ttk.Separator(panel, orient="vertical").pack(side="left", fill="y", padx=6)

        right = ttk.Frame(panel)
        right.pack(side="left", fill="both", expand=True)


        ttk.Label(right, text="Productos disponibles (Solo para referencia de datos)").pack(anchor="w")
        cols = ("ID", "Producto", "Precio", "Stock")
        self.tree_venta_prod = ttk.Treeview(right, columns=cols, show="headings", height=8)
        for c in cols:
            self.tree_venta_prod.heading(c, text=c)
            self.tree_venta_prod.column(c, width=120, anchor="center")
        self.tree_venta_prod.pack(fill="x", pady=6)

        qty_frame = ttk.Frame(right)
        qty_frame.pack(fill="x", pady=(2,8))

        ttk.Label(qty_frame, text="Producto:").pack(side="left")
        self.v_prod_nombre = tk.StringVar()
        self.combo_prod = ttk.Combobox(qty_frame, textvariable=self.v_prod_nombre, state="readonly", width=30)
        self.combo_prod.pack(side="left", padx=6)
        
        ttk.Label(qty_frame, text="Cantidad:").pack(side="left")
        self.v_cant = tk.StringVar(value="1")
        ttk.Entry(qty_frame, textvariable=self.v_cant, width=8).pack(side="left", padx=6)
        
        ttk.Button(qty_frame, text="Agregar al pedido", style="Accent.TButton", command=self.agregar_linea_pedido).pack(side="left", padx=6)


        ttk.Label(right, text="Detalle del pedido").pack(anchor="w", pady=(8,0))
        cols2 = ("ProductoID", "Nombre", "Cantidad", "PrecioUnit", "Subtotal")
        self.tree_detalle = ttk.Treeview(right, columns=cols2, show="headings", height=8)
        for c in cols2:
            self.tree_detalle.heading(c, text=c)
            self.tree_detalle.column(c, width=120, anchor="center")
        self.tree_detalle.pack(fill="both", pady=6)

        foot = ttk.Frame(right)
        foot.pack(fill="x", pady=6)
        ttk.Label(foot, text="Total: ").pack(side="left")
        self.total_var = tk.StringVar(value="0.00")
        ttk.Label(foot, textvariable=self.total_var, font=("Segoe UI", 12, "bold")).pack(side="left", padx=6)
        ttk.Button(foot, text="Guardar Venta", style="Accent.TButton", command=self.guardar_pedido).pack(side="right")


        self.load_productos_para_venta()
        self.load_empleados_para_venta()
        
    def _on_tab_change(self, event):

        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "Registrar Venta":
            self.load_productos_para_venta()
            self.load_empleados_para_venta()

    def load_empleados_para_venta(self):
        conn = conectar_bd()
        if not conn: return
        cur = conn.cursor()
        try:

            cur.execute("SELECT empleado_id, nombre, apellido FROM Empleados ORDER BY empleado_id")
            rows = cur.fetchall()
            
            self.empleados_map = {}
            nombres_empleados = []
            
            for r in rows:
                empleado_id, nombre, apellido = r

                nombre_completo = f"{nombre.strip()} {apellido.strip()}"
                

                self.empleados_map[nombre_completo] = empleado_id
                nombres_empleados.append(nombre_completo)
            

            self.combo_emp['values'] = nombres_empleados
            if nombres_empleados:

                if not self.v_emp_nombre.get() or self.v_emp_nombre.get() not in self.empleados_map:
                    self.v_emp_nombre.set(nombres_empleados[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar empleados:\n{e}")
        finally:
            conn.close()

    def load_productos_para_venta(self):
        conn = conectar_bd()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute("SELECT producto_id, nombre, precio, stock FROM Productos ORDER BY producto_id")
            rows = cur.fetchall()
            

            self.productos_map = {}
            nombres_productos = []
            for i in self.tree_venta_prod.get_children():
                self.tree_venta_prod.delete(i)
                
            for r in rows:
                producto_id, nombre, precio, stock = r
                

                self.productos_map[nombre] = {
                    'id': producto_id, 
                    'precio': Decimal(precio), 
                    'stock': int(stock)
                }
                nombres_productos.append(nombre)
                

                self.tree_venta_prod.insert("", "end", values=(producto_id, nombre, format(precio, ".2f"), stock))
            
    
            self.combo_prod['values'] = nombres_productos
            if nombres_productos:
   
                if not self.v_prod_nombre.get() or self.v_prod_nombre.get() not in self.productos_map:
                    self.v_prod_nombre.set(nombres_productos[0])
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar productos para venta:\n{e}")
        finally:
            conn.close()

    def crear_pedido_base(self):

        emp_nombre = self.v_emp_nombre.get().strip()
        if not emp_nombre or emp_nombre not in self.empleados_map:
            messagebox.showwarning("Validación", "Selecciona un empleado válido.")
            return


        emp_id = self.empleados_map[emp_nombre]
        estado = self.v_estado.get().strip() or "Entregado"
        conn = conectar_bd()
        if not conn: return
        cur = conn.cursor()
        try:

            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql_insert = (
                "INSERT INTO Pedidos (fecha_hora, empleado_id, estado, total_pedido) "
                "OUTPUT INSERTED.pedido_id "  
                "VALUES (?, ?, ?, ?)"
            )
            
            cur.execute(sql_insert, (ahora, emp_id, estado, float(Decimal(0.0))))
            

            pid_result = cur.fetchone()
            
            if pid_result is None or pid_result[0] is None:
                messagebox.showerror("Error", "El pedido se insertó, pero no se pudo obtener el ID del resultado de OUTPUT.")
                conn.rollback() 
                return

            self.current_pedido_id = int(pid_result[0])
            conn.commit()
            
            messagebox.showinfo("Pedido creado", f"Pedido creado con ID {self.current_pedido_id}. Ahora agrega productos.")


            for it in self.tree_detalle.get_children():
                self.tree_detalle.delete(it)
            self.total_var.set("0.00")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo crear pedido:\n{e}")
            conn.rollback()
        finally:
            conn.close()

    def agregar_linea_pedido(self):
        if not self.current_pedido_id:
            messagebox.showwarning("Atención", "Crea primero un pedido (botón 'Crear Pedido Vacío').")
            return
            
 
        prod_nombre = self.v_prod_nombre.get().strip()
        if not prod_nombre or prod_nombre not in self.productos_map:
            messagebox.showwarning("Atención", "Selecciona un producto válido del menú desplegable.")
            return

        try:

            cantidad = int(float(self.v_cant.get()))
        except Exception:
            messagebox.showwarning("Validación", "Cantidad inválida.")
            return

        if cantidad <= 0:
            messagebox.showwarning("Validación", "Cantidad debe ser mayor a 0.")
            return
            

        prod_data = self.productos_map[prod_nombre]
        producto_id = prod_data['id']
        precio = prod_data['precio']
        stock = prod_data['stock']
        

        if cantidad > stock:
            messagebox.showwarning("Stock", f"No hay suficiente stock para {prod_nombre}. Disponible: {stock}")
            return


        prod_data['stock'] -= cantidad
        

        subtotal = cantidad * precio
        
        self.tree_detalle.insert("", "end", values=(producto_id, prod_nombre, cantidad, format(precio, ".2f"), format(subtotal, ".2f")))
        self.recalcular_total()
        

        self.v_cant.set("1") 


    def recalcular_total(self):
        total = Decimal("0.00")
        for it in self.tree_detalle.get_children():
            vals = self.tree_detalle.item(it, "values")
            try:

                total += Decimal(str(vals[4]))
            except Exception:

                pass
        self.total_var.set(format(total, ".2f"))

    def guardar_pedido(self):
        if not self.current_pedido_id:
            messagebox.showwarning("Atención", "Crea primero un pedido (botón 'Crear Pedido Vacío').")
            return
        lines = self.tree_detalle.get_children()
        if not lines:
            messagebox.showwarning("Atención", "Agrega productos al pedido.")
            return
        conn = conectar_bd()
        if not conn: return
        cur = conn.cursor()
        try:
            total = Decimal("0.00")
            for it in lines:
                producto_id, nombre, cantidad_str, precio_unit_str, subtotal_str = self.tree_detalle.item(it, "values")
                cantidad = int(cantidad_str)
                precio_unit = Decimal(str(precio_unit_str))
                subtotal = Decimal(str(subtotal_str))
                
        
                cur.execute(
                    "INSERT INTO Detalle_Pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                    (self.current_pedido_id, int(producto_id), cantidad, float(precio_unit))
                )
                
   
                cur.execute("UPDATE Productos SET stock = stock - ? WHERE producto_id = ?", (cantidad, int(producto_id)))
                total += subtotal
                

            cur.execute("UPDATE Pedidos SET total_pedido = ? WHERE pedido_id = ?", (float(total), self.current_pedido_id))
            conn.commit()
            
            messagebox.showinfo("Venta registrada", f"Pedido {self.current_pedido_id} guardado. Total: {format(total,'.2f')}")
       
            self.current_pedido_id = None
            for it in self.tree_detalle.get_children():
                self.tree_detalle.delete(it)
            self.total_var.set("0.00")
            self.load_productos_para_venta()
            self.load_empleados_para_venta()
            self.load_productos()
            self.refresh_home()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"No se pudo guardar la venta:\n{e}")
        finally:
            conn.close()

# ---------------- VENTANA AGREGAR / EDITAR PRODUCTO ----------------
class ProductoEditor(tk.Toplevel):
    def __init__(self, master, app=None, callback=None, datos=None):
        super().__init__(master)
        self.app = app
        self.callback = callback
        self.datos = datos
        self.title("Producto")
        self.geometry("620x420")
        self.configure(background=BG)
        self.resizable(False, False)
        self.grab_set() 

        frame = ttk.Frame(self, style="Card.TFrame", padding=12)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(frame, text="Nombre").grid(row=0, column=0, sticky="w", padx=6, pady=6)
        self.e_nombre = ttk.Entry(frame, width=50)
        self.e_nombre.grid(row=0, column=1, padx=6, pady=6)

        ttk.Label(frame, text="Descripción").grid(row=1, column=0, sticky="nw", padx=6, pady=6)
        self.t_desc = tk.Text(frame, width=40, height=6)
        self.t_desc.grid(row=1, column=1, padx=6, pady=6)

        ttk.Label(frame, text="Precio").grid(row=2, column=0, sticky="w", padx=6, pady=6)
        self.e_precio = ttk.Entry(frame, width=20)
        self.e_precio.grid(row=2, column=1, sticky="w", padx=6, pady=6)

        ttk.Label(frame, text="Tipo").grid(row=3, column=0, sticky="w", padx=6, pady=6)
        self.e_tipo = ttk.Entry(frame, width=30)
        self.e_tipo.grid(row=3, column=1, sticky="w", padx=6, pady=6)

        ttk.Label(frame, text="Stock").grid(row=4, column=0, sticky="w", padx=6, pady=6)
        self.e_stock = ttk.Entry(frame, width=10)
        self.e_stock.grid(row=4, column=1, sticky="w", padx=6, pady=6)

        action_frame = ttk.Frame(frame)
        action_frame.grid(row=6, column=0, columnspan=2, pady=12)
        ttk.Button(action_frame, text="Guardar", style="Accent.TButton", command=self.save).pack(side="left", padx=8)
        ttk.Button(action_frame, text="Cancelar", command=self.destroy).pack(side="left", padx=8)

        if datos:
            try:
                self.title(f"Editar Producto ID: {datos[0]}")
                self.e_nombre.insert(0, datos[1])
                self.t_desc.insert("1.0", datos[2] or "")
                self.e_precio.insert(0, str(datos[3]))
                self.e_tipo.insert(0, datos[4] or "")
                self.e_stock.insert(0, str(datos[5] or 0))
            except Exception:
                pass

    def save(self):
        nombre = self.e_nombre.get().strip()
        descripcion = self.t_desc.get("1.0", tk.END).strip()
        precio_raw = self.e_precio.get().strip()
        tipo = self.e_tipo.get().strip()
        stock_raw = self.e_stock.get().strip()

        if not nombre or not precio_raw or not stock_raw:
            messagebox.showwarning("Validación", "Completa los campos obligatorios (nombre, precio, stock).")
            return
        try:
            precio = float(precio_raw)
            stock = int(float(stock_raw))
        except Exception:
            messagebox.showwarning("Validación", "Precio o stock inválido.")
            return

        conn = conectar_bd()
        if not conn: return
        cur = conn.cursor()
        try:
            if self.datos:
                producto_id = int(self.datos[0])
                cur.execute("EXEC SP_ActualizarProductoCompleto ?, ?, ?, ?, ?, ?",
                            (producto_id, nombre, descripcion, precio, tipo, stock))
            else:
                cur.execute("EXEC SP_InsertarProducto ?, ?, ?, ?, ?",
                            (nombre, descripcion, precio, tipo, stock))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto guardado.")
            if self.callback:
                try:
                    self.callback()
                except Exception:
                    pass
            if self.app:
                try:

                    self.app.refresh_home()
                    self.app.load_productos_para_venta()
                except Exception:
                    pass
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")
        finally:
            conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()