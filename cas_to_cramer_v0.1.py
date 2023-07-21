import tkinter as tk
import subprocess
import pandas as pd
import pubchempy as pcp
import requests
import subprocess
import os
from tkinter import filedialog

#Глобальные переменные
input_path = 'C:\\'
input_filename = 'data.csv'
toxtree_path = "C:\Ideaconsult\Toxtree-v3.1.0.1851\Toxtree"
output_file_path = 'C:\\fin.csv'
input_file_toxtree = 'Toxtree-3.1.0.1851.jar'

#Стартовый блок выбора параметров
def start():
    global input_path
    global input_filename
    global toxtree_path
    global output_file_path
    global input_file_toxtree
    
    # Вызываем диалоговое окно выбора файла CSV
    input_data = filedialog.askopenfilename(title="Выберите CSV файл", filetypes=[("CSV files", "*.csv")], initialdir=input_path)

    # Если файл не выбран, выходим из функции
    if not input_data:
        return
    #Получаем в переменные данные о файле и пути до него
    input_path = os.path.dirname(input_data)
    input_filename = os.path.basename(input_data)

    # Вызываем диалоговое окно выбора места сохранения файла
    output_file_path = filedialog.asksaveasfilename(title="Сохранить результат как файл .CSV", defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialdir=input_path)
    
    # Если файл не выбран, выходим из функции
    if not output_file_path:
        return

    
    #печать в терминал
    print(f"Selected CSV file: {input_path}{input_filename}")
    print(f"Output file: {output_file_path}")

    # Вызываем диалоговое окно выбора папки с toxtree
    toxtree_path = filedialog.askopenfilename(title="Выбор директории установки Toxtree.jar", filetypes=[("jar files", "*.jar")], initialdir=toxtree_path)
    input_file_toxtree = os.path.basename(toxtree_path)
    
    # Если папка не выбрана, выходим из функции
    if not toxtree_path:
        return

    # Получаем абсолютный путь к папке с toxtree
    toxtree_path = os.path.dirname(toxtree_path)
    

    # Выводим путь к файлу и путь к папке с toxtree в консоль
    print(f"Selected toxtree directory: {toxtree_path}")
    #запускаем основной скрипт
    mainfun ()

#если кнопка закрыть- то завершить
def close():
    root.destroy()




def mainfun():
    global input_path
    global input_filename
    global toxtree_path
    global output_file_path
    global input_file_toxtree

    # Функция получения SMILES
    def get_smiles(cas):
        try:
            c = pcp.get_compounds(cas, 'name')
            return c[0].canonical_smiles
        except BaseException as e:
            print(f"Ошибка при получении SMILES для CAS {cas}: {e}")
            return 'N/A'

    # Функция проверки доступности PubChem API
    def check_api():
        url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/cids/TXT'
        response = requests.get(url)
        if response.status_code == 200:
            print('PubChem API доступен.')
            return True
        else:
            print('Ошибка: PubChem API не доступен.')
            return False

    # Загрузка данных из CSV-файла
    os.chdir (input_path)
    
    df = pd.read_csv(input_filename, sep=';')

    # Проверка наличия столбца 'CAS' в DataFrame
    if 'CAS' not in df.columns:
        print('Ошибка: столбец CAS отсутствует в DataFrame.')
        exit()

    # Проверка доступности PubChem API
    if not check_api():
        exit()

    # Получение SMILES для каждого CAS в DataFrame
    df['SMILES'] = df['CAS'].apply(get_smiles)

    # Проверка на отсутствие SMILES
    for cas, smiles in zip(df['CAS'], df['SMILES']):
        if smiles == 'N/A':
            print(f"CAS {cas} не найден в базе данных PubChem.")

    # Сохранение результата в новый CSV-файл
    first_output_filename = os.path.splitext(input_filename)[0] + '_result.csv'
    df.to_csv(first_output_filename, sep=',', index=False)

    # Путь к установленному на компьютере toxtree
    sec_output_file_name = os.path.splitext(input_filename)[0] + '_toxout.csv' 

    # Путь к файлу input.csv
    input_path_file = input_path + first_output_filename

    # Путь к файлу output.csv из toxtree
    output_path_file_toxtree = input_path + sec_output_file_name
    os.chdir (toxtree_path)

    # Команда для запуска toxtree
    command = f"java  -jar {input_file_toxtree} -n -i {input_path_file} -o {output_path_file_toxtree}"

    # Запуск команды
    subprocess.run(command, shell=True)

    os.chdir (input_path)
    dfFIN = pd.read_csv(sec_output_file_name, sep=',')
    
    # Сохранение результата в новый CSV-файл
    df= df.merge(dfFIN, left_on='CAS', right_on='CAS',suffixes=('_input', '_out'))
    df.to_csv(output_file_path, sep=';', index=False)
    print(f"Output file: {output_file_path}")


#главное окно , открывается при запуске
root = tk.Tk()
root.title("Расчет классов Крамера для CAS")
root.geometry("500x250")

#надпись в окне
frame = tk.Frame(master=root, width=450, height=140)
frame.pack()
label1 = tk.Label(master=frame,justify="left", text="Если на вход скормить файл csv (разделитель \";\") - с колонкой CAS,\nприложение запрашивает через PubChemAPI формулу в виде SMILE,\nкоторыми кормит установленное приложение Toxtree,\n(обычно расположен C:\Ideaconsult\Toxtree-v3.1.0.1851\Toxtree)\nполучая данные по классу Cramer, вывод в csv файл\nпри выполнении в начальной папке создаются файлы\nresult.csv - данные по SMILE,\ntoxout.csv - обработка Toxtree")
label1.place(x=0, y=0)

#кнопки
start_button = tk.Button(root, text="Начать", command=start)
start_button.pack(side="left", padx=50, pady=10)

close_button = tk.Button(root, text="Закрыть", command=close)
close_button.pack(side="left", padx=50, pady=10)

root.mainloop()