import pandas as pd
import numpy as np
import math 

from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.metrics import f1_score
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.linear_model import ElasticNet

import matplotlib.pyplot as plt

# ucitavanje podataka
podaci = pd.read_csv('tabela_automobila.csv')

# uklanjanje 30tak podataka koji imaju nepopunjenu kubikazu (elektricni automobili)
podaci.drop(podaci[podaci['gorivo'] == 'Električni pogon'].index, inplace = True)

# uklanjanje verovatno neispravnih redova sa cenom manjom od 200
podaci.drop(podaci[podaci.cena < 200].index, inplace=True)

# dodavanje opsega cena
opseg_cena = []
for cena in podaci['cena']:
    if cena < 2000:
        opseg = 1
    elif  2000 <= cena <= 4999:
        opseg = 2
    elif  5000 <= cena <= 9999: 
        opseg = 3
    elif 10000 <= cena <= 14999:
        opseg = 4
    elif 15000 <= cena <= 19999:
        opseg = 5
    elif 20000 <= cena <= 24999:
        opseg = 6
    elif 25000 <= cena <= 29999:
        opseg = 7
    else:
        opseg = 8
    opseg_cena.append(opseg)

podaci['opseg_cena'] = opseg_cena

def konvertuj_opseg_u_cenu(opseg):
    if opseg == 1:
        cena = '< 2000e'
    elif opseg == 2:
        cena = '2000-4999e'
    elif opseg == 3: 
        cena = '5000-9999e'
    elif opseg == 4:
        cena = '10000-14999e'
    elif opseg == 5:
        cena = '15000-19999e'
    elif opseg == 6:
        cena = '20000-24999e'
    elif opseg == 7:
        cena = '25000-29999e'
    else:
        cena = '> 30000e'

    return cena 

def velika_slova_kolona(podaci):
    # Beograd i BEOGRAD je ista vrednost => resenje sve prebaciti u uppercase
    for kolona in podaci.columns:
        if(podaci[kolona].dtype == 'object' and kolona != 'url'):
            podaci[kolona] = podaci[kolona].str.upper() 

velika_slova_kolona(podaci)

# enkodovanje podataka
# def enkoduj_podatke(podaci, enkoder = LabelEncoder()):
#     podaci['marka'] = enkoder.fit_transform(podaci['marka'])
#     podaci['stanje'] = enkoder.fit_transform(podaci['stanje'])
#     podaci['karoserija'] = enkoder.fit_transform(podaci['karoserija'])
#     podaci['gorivo'] = enkoder.fit_transform(podaci['gorivo'])
#     podaci['menjac'] = enkoder.fit_transform(podaci['menjac'])
#     podaci['broj_vrata'] = enkoder.fit_transform(podaci['broj_vrata'])
#     podaci['ostecenje'] = enkoder.fit_transform(podaci['ostecenje'])
#     podaci['klima'] = enkoder.fit_transform(podaci['klima'])
#     podaci['model'] = enkoder.fit_transform(podaci['model'])
#     podaci['boja'] = enkoder.fit_transform(podaci['boja'])
#     podaci['lokacija'] = enkoder.fit_transform(podaci['lokacija'])
#     podaci['opseg_cena'] = enkoder.fit_transform(podaci['opseg_cena'])    
#     return enkoder

# enkoder = enkoduj_podatke(podaci)

enkoder = OrdinalEncoder(handle_unknown = 'use_encoded_value', unknown_value = -1)
kolone_za_enkodovanje = ['marka', 'stanje', 'karoserija', 'gorivo', 'menjac', 'broj_vrata', 'ostecenje', 'klima', 'model', 'boja', 'lokacija']
podaci[kolone_za_enkodovanje] = enkoder.fit_transform(podaci[kolone_za_enkodovanje])

ulazneKoloneLR = ['stanje', 'marka', 'model', 'godiste', 'kilometraza',
            'karoserija', 'gorivo', 'kubikaza', 'snaga_motora', 'menjac', 'boja',
            'ostecenje', 'klima', 'lokacija']
ulazneKoloneKNN = ['marka', 'model', 'godiste', 'karoserija', 'snaga_motora', 'broj_vrata', 'ostecenje']

izlaznaKolonaLR = ['cena']
izlaznaKolonaKNN = ['opseg_cena']

def lrModel(podaci, ulazneKolone = ulazneKoloneLR, izlaznaKolona = izlaznaKolonaLR, ispis = False, lr = linear_model.Ridge(alpha = 1000), poliStepen = 3):
    X = podaci[ulazneKolone]
    y = podaci[izlaznaKolona]
    
    lrSkaliranje = StandardScaler()
    X_skalirano = lrSkaliranje.fit_transform(X)
    
    X_trening, X_test, y_trening, y_test = train_test_split(X_skalirano, y, test_size = 0.2, random_state = 42)

    # poli = PolynomialFeatures(degree = 3)
    # X_trening = poli.fit_transform(X_trening)
    
    # X_test = poli.fit_transform(X_test)    
    # lr.fit(X_trening, y_trening)    
    poli = PolynomialFeatures(poliStepen)
    lr = make_pipeline(poli, lr)
    lr.fit(X_trening, y_trening) 
    
    if ispis == True:
        print('Koeficijent determinacije (trening podaci): ', lr.score(X_trening, y_trening))
        print('Koeficijent determinacije (test podaci): ', lr.score(X_test, y_test), end='\n\n')
    
    return poli, lr, lrSkaliranje

def predikcija(model, podaci, skaliranje, ulazneKolone = ulazneKoloneKNN):
    print(podaci.head(5))
    print(podaci.dtypes)
    X_skalirano = skaliranje.transform(podaci[ulazneKolone])

    y_pred = model.predict(X_skalirano)
    # print('Predvidjanje: ', y_pred)

    return y_pred

def predikcijaLR(lr, poli, podaci, skaliranje, ulazneKolone = ulazneKoloneLR):
    X_skalirano = skaliranje.transform(podaci[ulazneKolone])

    #lr = make_pipeline(poli, lr)

    y_pred = lr.predict(X_skalirano)
    # print('Predvidjanje: ', y_pred)

    return y_pred
    
# print(len(podaci))
# podaci2 = podaci[(podaci['godiste'] < 1985) | (podaci['godiste'] > 2022)]
# podaci = podaci[(podaci['godiste'] >= 1985) & (podaci['godiste'] <= 2022)]
# print(len(podaci))

# lrModel(lr = LinearRegression(), ispis = True)
# lrModel(lr = linear_model.Lasso(alpha = 1000), ispis = True) 
# lrModel(lr = linear_model.ElasticNet(alpha = 1000), ispis = True)

#predikcija(model = lr, podaci = podaci)

poli, lr, lrSkaliranje = lrModel(podaci = podaci, lr = linear_model.Ridge(alpha = 1000), ispis = True)

def knnModel(podaci, ulazneKolone = ulazneKoloneKNN, izlaznaKolona = izlaznaKolonaKNN, brojSuseda = 10, racunanjeDistance = 2, ispis = False):
    X = podaci[ulazneKolone]
    y = podaci[izlaznaKolona]

    knnSkaliranje = StandardScaler()
    X_skalirano = knnSkaliranje.fit_transform(X)

    X_trening_skalirano, X_test_skalirano, y_trening, y_test = train_test_split(X_skalirano, y, test_size = 0.2, random_state = 42)

    # X_trening_skalirano = knnSkaliranje.fit_transform(X_trening)
    # X_test_skalirano = knnSkaliranje.fit_transform(X_test)

    knn = KNeighborsClassifier(n_neighbors = brojSuseda, weights = 'distance', p = racunanjeDistance)
    knn.fit(X_trening_skalirano, y_trening)

    y_pred = knn.predict(X_test_skalirano)
        
    preciznost = metrics.accuracy_score(y_test, y_pred)
    f_mera = f1_score(y_test, y_pred, average = 'weighted')
    print('Preciznost:', preciznost)
    print('F mera:', f_mera)

    if ispis == True:
        cm = confusion_matrix(y_test, y_pred, labels = knn.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels = knn.classes_)
        disp.plot()
        plt.show()
    
    # return knn, X_trening_skalirano, X_test_skalirano, y_trening, y_test, y_pred, preciznost, f_mera
    return knn, knnSkaliranje

knn, knnSkaliranje = knnModel(podaci = podaci)
 
podaciTestKNN = podaci[ulazneKoloneKNN].iloc[0:1]
podaciTestLR = podaci[ulazneKoloneLR].iloc[0:20]

print(predikcija(model = knn, podaci = podaciTestKNN, skaliranje = knnSkaliranje, ulazneKolone = ulazneKoloneKNN))

#['marka', 'model', 'godiste', 'karoserija', 'snaga_motora', 'broj_vrata', 'ostecenje']

from tkinter import *
from tkinter import messagebox

font = ('Tahoma', 11)
boja_fonta = 'black'

window = Tk()

window.title('Projektni zadatak - Pronalaženje skrivenog znanja')
window.geometry('600x600+10+20')


x = 100
y = 30

#gorivo

kolone_tekstualni_unos = ['stanje', 'marka', 'model', 'godiste', 'kilometraza', 'karoserija', 'gorivo', 'kubikaza', 'snaga_motora', 'menjac', 'broj_vrata', 'boja', 'ostecenje', 'klima', 'lokacija']
polje_unos = []

for kolona in kolone_tekstualni_unos:
    labela = Label(window, text = kolona + ':', fg = boja_fonta, font = font)
    labela.place(x = x, y = y)
    y = y + 22
    unos = Entry(window, text = '', bd = 1, font = font)
    unos.place(x = x, y = y)
    polje_unos.append(unos)
    y = y + 30
    if(y >= 450):
        y = 30
        x = x + 200

def proceni_cenu():
    vrednosti = []
    for polje in polje_unos:
        vrednosti.append(polje.get())

    nov_podatak = dict(zip(kolone_tekstualni_unos, vrednosti))

    nov_podatak = pd.DataFrame([nov_podatak])
    print(nov_podatak)

    nov_podatak['godiste'] = int(nov_podatak['godiste'])
    nov_podatak['snaga_motora'] = int(nov_podatak['snaga_motora']) 
    nov_podatak['kilometraza'] = int(nov_podatak['kilometraza']) 
    nov_podatak['kubikaza'] = int(nov_podatak['kubikaza']) 

    velika_slova_kolona(nov_podatak)
    nov_podatak[kolone_za_enkodovanje] = enkoder.transform(nov_podatak[kolone_za_enkodovanje])
    print(nov_podatak.head())

    nov_podatak_KNN = nov_podatak[ulazneKoloneKNN]

    nov_podatak_LR = nov_podatak[ulazneKoloneLR]

    opseg = predikcija(model = knn, podaci = nov_podatak_KNN, skaliranje = knnSkaliranje, ulazneKolone = ulazneKoloneKNN)
    print(opseg)
    cena_KNN = konvertuj_opseg_u_cenu(opseg)

    print(nov_podatak_LR)
    cena_LR = predikcijaLR(lr = lr, poli = poli, podaci = nov_podatak_LR, skaliranje = lrSkaliranje, ulazneKolone = ulazneKoloneLR)
    print(cena_LR)

    rezultat = 'Procena cene po KNN (opseg): ' + str(cena_KNN) + '\n\n' + 'Procena cene po LR: ' + str(cena_LR) + ' eur' 

    messagebox.showinfo("Procena cene", rezultat)


btn=Button(window, text = 'Nađi procenjenu cenu', fg = boja_fonta, font = font, command = proceni_cenu)
btn.place(x = x, y = y + 15)

window.mainloop()





