import tkinter as tk
from tkinter import filedialog, scrolledtext
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
from PyPDF2 import PdfMerger
import os
import time
import sys
from datetime import datetime


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class FileHandler(FileSystemEventHandler):
    def __init__(self, log_callback):
        self.log_callback = log_callback
        self.last_processed = 0

    def on_created(self, event):
        if event.is_directory:
            return

        current_time = time.time()
        if current_time - self.last_processed < 1:
            return

        file_path = event.src_path
        file_name = os.path.basename(file_path)

        if file_path.endswith('Summary.pdf'):
            time.sleep(1)
            try:
                new_path = os.path.join(os.path.dirname(file_path), "PROCURACAO CERTIFICADO.pdf")
                os.rename(file_path, new_path)
                self.log_callback(f"✅ Arquivo renomeado com sucesso: {file_name} -> Procuracao Certificado.pdf")
                self.last_processed = current_time
            except Exception as e:
                self.log_callback(f"❌ Erro ao renomear arquivo: {str(e)}")

        elif file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            time.sleep(1)
            try:
                if not os.path.exists(file_path):
                    return

                image = Image.open(file_path)
                if image.mode != 'RGB':
                    image = image.convert('RGB')

                pdf_path = os.path.splitext(file_path)[0] + '.pdf'
                image.save(pdf_path, 'PDF', resolution=100.0)

                if os.path.exists(pdf_path):
                    try:
                        os.remove(file_path)
                    except FileNotFoundError:
                        pass
                    self.log_callback(f"🖼️ Imagem convertida: {file_name} -> {os.path.basename(pdf_path)}")
                    self.last_processed = current_time
                else:
                    self.log_callback("❌ Erro ao converter imagem: PDF não criado")
            except Exception as e:
                self.log_callback(f"❌ Erro ao converter imagem: {str(e)}")


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=200, height=40, corner_radius=10,
                 bg_color="#2D2D2D", hover_color="#3D3D3D", click_color="#4D4D4D", **kwargs):
        super().__init__(parent, width=width, height=height, bg=parent["bg"],
                         highlightthickness=0, **kwargs)

        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.click_color = click_color
        self.corner_radius = corner_radius

        self.button = self.create_rounded_rect(0, 0, width, height, corner_radius, fill=bg_color)
        self.text = self.create_text(width / 2, height / 2, text=text, fill="white",
                                     font=('Segoe UI', 10))

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)

        self.is_clicked = False

    def create_rounded_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_enter(self, event):
        if not self.is_clicked:
            self.itemconfig(self.button, fill=self.hover_color)

    def on_leave(self, event):
        if not self.is_clicked:
            self.itemconfig(self.button, fill=self.bg_color)

    def on_click(self, event):
        self.is_clicked = True
        self.itemconfig(self.button, fill=self.click_color)
        self.move(self.text, 0, 1)

    def on_release(self, event):
        self.is_clicked = False
        self.itemconfig(self.button, fill=self.hover_color)
        self.move(self.text, 0, -1)
        if self.command:
            self.command()

    def configure(self, **kwargs):
        if 'state' in kwargs:
            if kwargs['state'] == 'disabled':
                self.itemconfig(self.button, fill='#1A1A1A')
                self.itemconfig(self.text, fill='#666666')
                self.unbind("<Enter>")
                self.unbind("<Leave>")
                self.unbind("<Button-1>")
                self.unbind("<ButtonRelease-1>")
            else:
                self.itemconfig(self.button, fill=self.bg_color)
                self.itemconfig(self.text, fill='white')
                self.bind("<Enter>", self.on_enter)
                self.bind("<Leave>", self.on_leave)
                self.bind("<Button-1>", self.on_click)
                self.bind("<ButtonRelease-1>", self.on_release)


class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Arquivos")
        self.root.geometry("800x600")
        self.root.configure(bg='#1E1E1E')

        try:
            icon_path = resource_path("icon.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

        self.folder_path = tk.StringVar()
        self.observer = None

        label_style = {'bg': '#1E1E1E', 'fg': '#E0E0E0', 'font': ('Segoe UI', 10)}

        main_frame = tk.Frame(root, padx=30, pady=30, bg='#1E1E1E')
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(main_frame, text="Monitor de Arquivos", font=('Segoe UI', 16, 'bold'),
                               bg='#1E1E1E', fg='white')
        title_label.pack(pady=(0, 20))

        folder_frame = tk.Frame(main_frame, bg='#1E1E1E')
        folder_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Label(folder_frame, text="Pasta:", **label_style).pack(side=tk.LEFT)
        entry = tk.Entry(folder_frame, textvariable=self.folder_path, width=50, bg='#2D2D2D', fg='white',
                         insertbackground='white', font=('Segoe UI', 10), borderwidth=0)
        entry.pack(side=tk.LEFT, padx=10)

        self.select_button = RoundedButton(folder_frame, "Selecionar", command=self.select_folder,
                                           width=120, height=35)
        self.select_button.pack(side=tk.LEFT)

        control_frame = tk.Frame(main_frame, bg='#1E1E1E')
        control_frame.pack(fill=tk.X, pady=(0, 20))

        self.start_button = RoundedButton(control_frame, "Iniciar Monitoramento",
                                          command=self.start_monitoring, width=200, height=35)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))

        self.stop_button = RoundedButton(control_frame, "Parar Monitoramento",
                                         command=self.stop_monitoring, width=200, height=35)
        self.stop_button.pack(side=tk.LEFT)
        self.stop_button.configure(state='disabled')

        # 🔗 Botão para juntar PDFs
        self.merge_button = RoundedButton(folder_frame, "Juntar PDFs", command=self.merge_pdfs, 
                                  width=120, height=35)
        self.merge_button.pack(side=tk.LEFT, padx=(15, 0))

        log_frame = tk.Frame(main_frame, bg='#1E1E1E')
        log_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(log_frame, text="Log de Atividades", **label_style).pack(anchor=tk.W, pady=(0, 5))
        self.log_area = scrolledtext.ScrolledText(log_frame, height=10, bg='#2D2D2D', fg='white',
                                                   insertbackground='white', font=('Segoe UI', 10),
                                                   borderwidth=0, padx=10, pady=10)
        self.log_area.pack(fill=tk.BOTH, expand=True)

        self.log_message("🔄 Programa iniciado.")
        self.log_message("📁 Selecione uma pasta para começar")

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)
            self.log_message(f"📁 Pasta selecionada: {folder}")

    def start_monitoring(self):
        if not self.folder_path.get():
            self.log_message("⚠️ Por favor, selecione uma pasta primeiro.")
            return

        try:
            self.observer = Observer()
            event_handler = FileHandler(self.log_message)
            self.observer.schedule(event_handler, self.folder_path.get(), recursive=False)
            self.observer.start()

            self.start_button.configure(state='disabled')
            self.stop_button.configure(state='normal')
            self.log_message("🚀 Monitoramento iniciado!")
        except Exception as e:
            self.log_message(f"❌ Erro ao iniciar monitoramento: {str(e)}")

    def stop_monitoring(self):
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.observer = None

            self.start_button.configure(state='normal')
            self.stop_button.configure(state='disabled')
            self.log_message("⏸️ Monitoramento parado!")

    def merge_pdfs(self):
        try:
            file_paths = filedialog.askopenfilenames(
                title="Selecione os PDFs para juntar",
                filetypes=[("Arquivos PDF", "*.pdf")]
            )

            if not file_paths:
                self.log_message("⚠️ Nenhum arquivo selecionado para juntar.")
                return

            save_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Arquivo PDF", "*.pdf")],
                title="Salvar PDF unido como"
            )

            if not save_path:
                self.log_message("❌ Operação de salvar cancelada.")
                return

            merger = PdfMerger()

            for path in file_paths:
                merger.append(path)
                self.log_message(f"➕ Adicionado: {os.path.basename(path)}")

            merger.write(save_path)
            merger.close()

            self.log_message(f"✅ PDF criado com sucesso: {os.path.basename(save_path)}")

            # 🔥 Remover os arquivos originais após juntar
            for path in file_paths:
                try:
                    os.remove(path)
                    self.log_message(f"🗑️ Arquivo excluído: {os.path.basename(path)}")
                except Exception as e:
                    self.log_message(f"❌ Erro ao excluir {os.path.basename(path)}: {str(e)}")

        except Exception as e:
            self.log_message(f"❌ Erro ao juntar PDFs: {str(e)}")

    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_area.insert(tk.END, f"[{timestamp}] {message}\n\n")
        self.log_area.see(tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorApp(root)
    root.mainloop()
