import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import time
import mes_parser
import app_icon
import logging
import traceback
# ------------------------------------------------------------------------
logger = logging.getLogger(__name__)
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename='mes_parser.log', level=logging.DEBUG, format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8')
# ------------------------------------------------------------------------

class Application(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.pack()
        self.master.geometry("480x80")
        self.master.resizable(False, False)
        self.master.title("mes_parser")
        self.create_widgets()
        # self.create_menu()
        # self.initialdir = os.path.abspath(os.path.dirname(__file__))
        self.initialdir = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.save_dir = os.path.join(self.initialdir, "output")
    
    def create_menu(self):
        menubar = tk.Menu(self.master)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="一括処理", command=self.batch_processing)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.master.config(menu=menubar)

    def create_widgets(self):
        self.btn_select_dir = ttk.Button(self, text="フォルダ選択", command=self.open_dir_dialog)
        self.btn_select_dir.grid(row=1, column=1, pady=10)

        self.select_path = ttk.Entry(self, width=60)
        self.select_path.grid(row=1, column=2, padx=10)

        self.btn_run = ttk.Button(self, text="JSON出力", command=self.run)
        self.btn_run.grid(row=2, column=1)

        self.pb=ttk.Progressbar(self, mode="determinate", length=365)
        self.pb.grid(row=2, column=2)

    def create_save_dir(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def open_dir_dialog(self):
        select_path = filedialog.askdirectory(initialdir=self.initialdir)
        if not select_path == "":
            print(select_path)
            self.select_path.delete(0, tk.END)
            self.select_path.insert(0, select_path)
            self.initialdir = select_path
        
    # def open_file_dialog(self):
    #     filetypes = [("", "*")]
    #     select_path = filedialog.askopenfilename(filetypes=filetypes)
    #     if not select_path == "":
    #         self.select_path.delete(0, tk.END)
    #         self.select_path.insert(0, select_path)

    def check_target(self):
        flg = False
        if os.path.exists(self.select_path.get()):
            flg = True
        if not flg:
            messagebox.showerror('ERR', 'フォルダが存在しません')
        return flg
    
    def update_progress(self, current_val):
        self.pb.configure(value=current_val)
        self.pb.update()

    def run(self):
        ret = messagebox.askyesno('INFO', '処理を開始しますか？')
        if ret and self.check_target():

            try:

                self.pb.configure(maximum=18)
                save_dir_path = self.save_dir
                init_dir_path = self.select_path.get()
                print(init_dir_path)
                mes_parser.log_message(f"json変換開始: {init_dir_path}")
                self.create_save_dir()

                project_param = mes_parser.get_project_param(init_dir_path)
                self.update_progress(1)
                network_param = mes_parser.get_network_param(init_dir_path)
                self.update_progress(2)
                target_server_param = mes_parser.get_target_server_param(init_dir_path)
                self.update_progress(3)
                target_device_param = mes_parser.get_target_device_param(init_dir_path)
                self.update_progress(4)
                device_tag_param = mes_parser.get_device_tag_param(init_dir_path)
                self.update_progress(5)
                device_tag_component_param = mes_parser.get_device_tag_component(init_dir_path)
                self.update_progress(6)
                acccess_table_param = mes_parser.get_acccess_table_param(init_dir_path)
                self.update_progress(7)
                acccess_field_param = mes_parser.get_acccess_field_param(init_dir_path)
                self.update_progress(8)
                job_param = mes_parser.get_job_param(init_dir_path)
                self.update_progress(9)
                db_buffer_param = mes_parser.get_db_buffer_param(init_dir_path)
                self.update_progress(10)
                matrix_led_param = mes_parser.get_dot_matrix_led_param(init_dir_path)
                self.update_progress(11)
                global_variable_param = mes_parser.get_global_variable_param(init_dir_path)
                self.update_progress(12)
                local_variable_param = mes_parser.get_local_variable_param(init_dir_path)
                self.update_progress(13)
                security_param = mes_parser.get_security_param(init_dir_path)
                self.update_progress(14)
                user_param = mes_parser.get_user_param(init_dir_path)
                self.update_progress(15)
                output_param = mes_parser.merge_param(
                    project_param, 
                    network_param, 
                    target_server_param, 
                    target_device_param, 
                    device_tag_param, 
                    device_tag_component_param,
                    acccess_table_param, 
                    acccess_field_param, 
                    job_param,
                    db_buffer_param,
                    matrix_led_param,
                    global_variable_param,
                    local_variable_param,
                    security_param,
                    user_param
                )
                self.update_progress(16)
                output_param = mes_parser.add_job_param(init_dir_path, job_param, output_param)
                self.update_progress(17)
                file_name = f'{os.path.basename(init_dir_path)}.json'
                save_file_path = os.path.join(save_dir_path, file_name)
                mes_parser.save_json(output_param, save_file_path)
                self.update_progress(18)

                mes_parser.log_message(f"json変換完了: {save_file_path}")
                messagebox.showinfo('INFO', '処理完了')
                self.pb.configure(value=0)

            except Exception as e:
                logging.exception("An error occurred: %s", e)
                traceback_message = traceback.format_exc()
                print(traceback_message)
                messagebox.showerror('ERR', '変換失敗')
                self.pb.configure(value=0)

    def batch_processing(self):
        cmd = input("please input path: ")
        print(cmd)
            
    def test(self):
        l = ["hoge", "piyo", "fuga"]
        self.pb.configure(maximum=len(l))
        for i,item in enumerate(l):
            print(i, item)
            time.sleep(0.5)
            self.pb.configure(value=i+1)
            self.pb.update()
        messagebox.showinfo('INFO', '処理完了')
        self.pb.configure(value=0)

def main():
    root = tk.Tk()
    root.iconphoto(False, app_icon.get_photo_image4icon())
    app = Application(master=root)
    app.mainloop()

if __name__ == "__main__":
    main()