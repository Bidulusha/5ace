import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Импортируем необходимые модули из Pillow
import os
import re
from camera_coordinates import looting

class MyApp:
    def __init__(self, root):
        logo = Image.open('logo.jpg')
        logo = logo.resize((32, 32), Image.ANTIALIAS)
        logo_icon = ImageTk.PhotoImage(logo)
        root.iconphoto(False, logo_icon)
        self.root = root
        self.root.title('GeoLink')
        self.root.geometry('800x600')
        self.load_logo()
        self.photo_folder_button = tk.Button(root, text='Выбрать снимок', command=self.select_image)
        self.photo_folder_button.pack(pady=20)
        self.data = None
        self.create_coordinates_fields()
    def load_logo(self):
        # Загружаем изображение логотипа
        logo_image = Image.open('geolink_logo.png')  # Убедитесь, что файл находится в той же папке, что и скрипт
        logo_image = logo_image.resize((150, 150), Image.ANTIALIAS)  # Изменяем размер изображения при необходимости
        self.logo = ImageTk.PhotoImage(logo_image)

        # Создаем виджет Label для отображения логотипа
        logo_label = tk.Label(self.root, image=self.logo)
        logo_label.pack(padx=300, pady=10)
    def create_coordinates_fields(self):
        self.coordinates_frame = tk.Frame(self.root)
        self.coordinates_frame.pack(pady=10)

        for i in range(4):
            print(self.data)
            tk.Label(self.coordinates_frame, text=f'Долгота {i}:').grid(row=i, column=0)
            self.longitude1_entry = tk.Entry(self.coordinates_frame)
            self.longitude1_entry.grid(row=i, column=1)
            self.longitude1_entry.insert(0,'1231')
            self.longitude1_entry.config(state='disabled')

            tk.Label(self.coordinates_frame, text=f'Широта {i}:').grid(row=i, column=2)
            self.latitude1_entry = tk.Entry(self.coordinates_frame)
            self.latitude1_entry.grid(row=i, column=3)
            self.latitude1_entry.config(state='disabled')


    def select_image(self):
        # Открываем диалог для выбора файла
        file_path = filedialog.askopenfilename(title='Выберите снимок', filetypes=[('Images', '*.png;*.jpg;*.jpeg'), ('All Files', '*.*')])

        if file_path:
            # Извлекаем дату из имени файла с помощью регулярного выражения
            file_name = os.path.basename(file_path)
            print(f'Имя файла: {file_name}')
            print(file_path)
            #file_path = file_path[:-len(file_name)-4]
            dirictory_path = os.path.dirname(file_path)
            new_path = os.path.join(os.path.dirname(file_path), 'logs', 'beacon_human.csv')
            print(new_path)
        self.data = looting(file_path,new_path)



if __name__ == '__main__':
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()