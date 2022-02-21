import os
import tempfile
from flask import Flask, escape, request, render_template, redirect, url_for

from werkzeug.utils import secure_filename

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64

import csv
import ast



app = Flask(__name__)


def draw(list_v2, list_v3, categorical_names, v1_name, v2_name, v3_name, average_v2, average_v3):
    """
    Funkcja tworzy wykres - wizualizacja danych
    Argumenty:
        -list_v2 - lista pierwszych zmiennych liczbowych
        -list_v3 - lista drugich zmiennych liczbowych
        -categorical_names - lista nazw zmiennych kategorycznych
        -v1_name - nazwa zmiennej kategorycznej
        -v2_name - nazwa pierwszej zmiennej liczbowej
        -v3_name - nazwa drugiej zmiennej liczbowej
        -average_v2 - lista średnich pierwszej zmiennej liczbowej
        -average_v3 - lista średnich drugiej zmiennej liczbowej
    """
    img = io.BytesIO()
    averages = []#na nazwy zmiennych kat. +average
    for i in range(len(list_v2)):
        averages.append(categorical_names[i] + '-average')

    for i in range(len(list_v2)):
        plt.plot(list_v2[i], list_v3[i], 'o')
        plt.xlabel(v2_name)
        plt.ylabel(v3_name)
        plt.title(f'{v1_name[0].capitalize()}')
        plt.grid(True, linestyle='dashed')

    for i in range(len(list_v2)):
        plt.plot(average_v2[i], average_v3[i], 'o')
    
    plt.legend(categorical_names + averages)  

    plt.savefig(img, format="png")
    img.seek(0)
    url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return f"data:image/png;base64,{url}"


@app.route("/")
def main():
    return render_template("index.html")
    

@app.route("/kontakt")
def kontakt():
    return render_template("kontakt.html")


@app.route("/analiza-danych", methods=["GET", "POST"])
def analiza():
    data = None #na dane
    
    len_categorical = None #na ilość zmiennych kategorycznych
    
    selected_v1 = None #na wybór z values1 - zmienna kategoryczna
    selected_v2 = None #values2
    selected_v3 = None #values3
    
    average_v2 = None #na średnie pierwszej zmiennej liczbowej
    average_v3 = None #na średnie drugiej zmiennej liczbowej

    categorical_values = None #na zmienne kategoryczne
    categorical = None #na zmienne kategoryczne
    continuous = None #na zmienne ciągłe

    chart = None #wykres

    if request.method == "POST":
        try:    #jeśli to zadziała to znaczy że dodajemy plik
            plik = request.files["csvfile"]
            if plik:
                filename = secure_filename(plik.filename)
                path = os.path.join(tempfile.gettempdir(), filename)
                plik.save(path)
            else:
                path = None
            
            if path:
                data = []
                with open(path, "r") as file:
                    csvfile = csv.reader(file)
                    for row in csvfile:
                        data.append(row)

                categorical = []
                continuous = []
                for i in data[1:]:
                    for j in range(len(i)):
                        try:
                            i[j] = float(i[j]) #próba zamiany danych z listy data na floaty
                        except:
                            pass
                        if (type(i[j]) == str) and (data[0][j] not in categorical): 
                            categorical.append(data[0][j]) #dodanie do listy zmiennych kategorycznych tylko danych które są stringami, tak żeby się nie powtarzały
                        elif (type(i[j]) != str) and (data[0][j] not in continuous): 
                            continuous.append(data[0][j])

            else: 
                data = None
                len_categorical = None
                selected_v1 = None
                selected_v2 = None
                selected_v3 = None
                average_v2 = None
                average_v3 = None 
                categorical_values = None
                categorical = None
                continuous = None
                chart = None
        
        except:     #w innym przypadku znaczy że zatwierdzamy zmienne z comboboxów
            selected_v1 = request.form['values1']   #wybrana kategoryczna
            selected_v2 = request.form['values2']   #wybrana liczbowa 1
            selected_v3 = request.form['values3']   #wybrana liczbowa 2
            data=request.form['data']   #pobrane data z formularza
            data = ast.literal_eval(data)   #zamieniamy ze stringa w listę 

            categorical = [] #na kategoryczne
            continuous = [] #na ciągłe
            for i in data[1:]:
                for j in range(len(i)):
                    try:
                        i[j] = float(i[j]) #próba zamiany danych z listy data na floaty
                    except:
                        pass
                    if (type(i[j]) == str) and (data[0][j] not in categorical): 
                        categorical.append(data[0][j]) #dodanie do listy zmiennych kategorycznych tylko danych które są stringami, tak żeby się nie powtarzały
                    elif (type(i[j]) != str) and (data[0][j] not in continuous): 
                        continuous.append(data[0][j])

            index_v1 = data[0].index(str(selected_v1)) #indeks zmiennej kategorycznej
            index_v2 = data[0].index(str(selected_v2)) #indeks 1 zmiennej ciaglej
            index_v3 = data[0].index(str(selected_v3)) #indeks 2 zmiennej ciągłej

            categorical_values = []
            for i in data[1:]: #gatunki
                if i[index_v1] not in categorical_values:
                    categorical_values.append(i[index_v1])
                else:
                    continue

            len_categorical = len(categorical_values)
            numbers_v2 = [0 for i in range(len(categorical_values))] #na zmienne liczbowe
            numbers_v3 = [0 for i in range(len(categorical_values))] #na zmienne liczbowe

            average_v2 = [0 for i in range(len(categorical_values))] #na średnie pierwszej zmiennej liczbowej
            average_v3 = [0 for i in range(len(categorical_values))] #na średnie drugiej zmiennej liczbowej
            
            a = 0      
            for j in categorical_values:
                list2 = []
                list3 = []
                for i in data[1:]:
                    if j == i[index_v1]:
                        list2.append(float(i[index_v2]))
                        list3.append(float(i[index_v3]))
                numbers_v2[a] = list2 # tworzenie listy zmiennych liczbowych, dla każdej zmiennej kategorycznej
                numbers_v3[a] = list3 # tworzenie listy zmiennych liczbowcy, dla każdej zmiennej kategorycznej
                a +=1

            b = 0
            for i in range(len(numbers_v2)):
                a2 = 0
                a3 = 0
                for j in range(len(numbers_v2[i])):
                    a2 += numbers_v2[i][j]
                    a3 += numbers_v3[i][j]
                average_v2[b] = round(a2/len(numbers_v2[i]), 2) #lista średnich dla każdej zmiennej kategorycznej
                average_v3[b] = round(a3/len(numbers_v3[i]), 2) #lista średnich dla każdej zmiennej kategorycznej
                b += 1

            try:    #rysowanie wykresu
                chart = draw(numbers_v2, numbers_v3,
                             categorical_values, categorical, selected_v2, selected_v3, average_v2, average_v3)
            except:
                pass
            


    return render_template("analiza-danych.html", data=data, len_categorical=len_categorical, categorical=categorical, selected_v1=selected_v1, selected_v2=selected_v2, selected_v3=selected_v3,average_v2=average_v2, average_v3=average_v3, categorical_values=categorical_values,continuous=continuous, chart=chart)

if __name__ == "__main__":
    app.run(debug=True)
