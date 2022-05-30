# -*- coding: utf-8 -*-
"""
Created on Sat May 28 20:55:05 2022

@author: micha
"""
from __future__ import unicode_literals # obsluga polskich znaków diaktrtycznych
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QMessageBox
from MainApp import * # import kodu pythona ze schematem GUI
import math
from math import sqrt, radians
import numpy as np

class MyApp(QDialog): # QDialog jako klasa nadrzedna
    def __init__(self):
        """
        Jets to konstruktor klasy, który wywoływany jest za każdym razem, gdy tworzymy obiekt/funkcję

        Returns
        -------
        None.

        """
        super().__init__()
        self.ui = Ui_Dialog() # Nazwa klasy z pliku przekonwertowanego z UI
        self.ui.setupUi(self) # ustawienie layoutu z QtDesigner
        self.setWindowTitle("Interfejs aplikacji geodezyjnej")
        self.setWindowIcon(QtGui.QIcon('Globus.jpg'))
        
        #1 karta
        self.ui.tabWidget.currentChanged.connect(self.ZmianaKart)
        # self.ui.radioButton_GRS.clicked.connect(self.select_elipsoida)
        # self.ui.radioButton_WGS.clicked.connect(self.select_elipsoida)
        self.ui.pushButton_5.clicked.connect(self.select_elipsoida)
        
        self.ui.pushButton_92.clicked.connect(self.XY1992)
        self.ui.pushButton.clicked.connect(self.XY2000)
        self.ui.pushButton_2.clicked.connect(self.pl2XYZ)
        
        #2 karta
        # self.ui.radioButton_GRS_4.toggled.connect(self.select_elipsoida2)
        # self.ui.radioButton_WGS_4.toggled.connect(self.select_elipsoida2)
        self.ui.pushButton_6.clicked.connect(self.select_elipsoida2)
        
        self.ui.pushButton_93.clicked.connect(self.XY1992_Karta2)
        self.ui.pushButton_3.clicked.connect(self.XY2000_Karta2)
        self.ui.pushButton_4.clicked.connect(self.pl2XYZ_Karta2)
        
        
        self.show()
        
    #tabWidget
    def ZmianaKart(self):
        """
        Funkcja, która pozwala przełączać się między kartami

        Returns
        -------
        None.

        """
        if  self.ui.tabWidget.currentIndex() == 0:
            print("Karta 1")
        else:
            print("Karta 2")
            
    # elipsoida dla karty 1
    def select_elipsoida(self):
        """
        Funkcja, która pozwala wybrać parametry elipsoidy dla karty 1

        Raises
        ------
        NotImplementedError
            Nie zaimplementowano wyboru parametrów elipsoidy

        Returns
        -------
        None.

        """
        if self.ui.radioButton_GRS.isChecked():
            self.a = 6378137.0
            self.b = 6356752.31414036
            print("GRS80")
        elif self.ui.radioButton_WGS.isChecked():
            self.a = 6378137.0 
            self.b = 6356752.31424518 
            print("WRS84")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nie wybrano elipsoidy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        
        self.flattening = (self.a - self.b) / self.a
        self.ecc2 = (2 * self.flattening - self.flattening ** 2)
        
        
        
    #UKŁAD PL-1992 dla Karty 1
    def XY1992(self):
        """
        Przeliczenie na współrzędne do układu PL-1992 dla karty 1

        Raises
        ------
        ValueError
        Jeżeli wyjdziemy poza zakres wartoci phi bądź lambda program nie pozwala policzyć dalej 

        Returns
        -------
        None.

        """
        if len(self.ui.lineEdit_phi.text()) != 0 and float(self.ui.lineEdit_phi.text()) >= 49 and float(self.ui.lineEdit_phi.text()) <= 54.8333: # zakres na phi <49 stopni, 54 stopni 50 minut>
            phi = float(self.ui.lineEdit_phi.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_lambda.text()) != 0 and float(self.ui.lineEdit_lambda.text()) >= 14.1167 and float(self.ui.lineEdit_lambda.text()) <= 24.15: # zakres na lambda <14 stopni 07 minut, 24 stopnie 09 minut>
            lam = float(self.ui.lineEdit_lambda.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla lambdy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            
        self.phi = radians(phi)
        self.lam = radians(lam)
        
        lam0 = radians(19)
        b2 = (self.a**2)*(1 - self.ecc2)
        ep2 = ((self.a**2 - b2))/(b2)
        t = np.tan(self.phi)
        n2 = ep2 * ((np.cos(self.phi))**2)
        N =  self.a / (np.sqrt(1 - self.ecc2 * (np.sin(self.phi)) ** 2))
        A0 = 1-(self.ecc2/4) - ((3*(self.ecc2**2))/64)-((5*(self.ecc2**3))/256)
        A2 = (3/8)*(self.ecc2+((self.ecc2**2)/4)+((15*(self.ecc2**3))/128))
        A4 = (15/256)*((self.ecc2**2)+((3*(self.ecc2**3))/4))
        A6 = (35*(self.ecc2**3))/3072
        dlam = self.lam - lam0
        sigma = self.a * (A0 * (self.phi) - (A2 * np.sin(2 * self.phi)) + (A4 * np.sin(4 * self.phi)) - (A6 * np.sin(6 * self.phi)))
        xgk = sigma + ((dlam**2)/2) * N * np.sin(self.phi) * np.cos(self.phi) * (1 + ((dlam**2)/12) * ((np.cos(self.phi))**2) * (5 - t**2 + 9 * n2 + 4 * (n2**2)) + ((dlam**4)/360) * ((np.cos(self.phi))**4) * (61 - (58 * (t**2)) + (t**4) + (270 * n2) - (330 * n2 * (t**2))))
        ygk = dlam * (N * np.cos(self.phi)) * (1 + ((((dlam**2)/6) * (np.cos(self.phi))**2) * (1 - t**2 + n2)) + (((dlam**4)/(120)) * (np.cos(self.phi)**4)) * (5 - (18 * (t**2)) + (t**4) + (14 * n2) - (58 * n2 * (t**2))))
        m0 = 0.9993
        x1992 = round((xgk * m0) - 5300000, 5)
        y1992 = round((ygk * m0) + 500000, 5)
        
        self.ui.label_3.setText(str(x1992) + ' ' + '[m]')
        self.ui.label_5.setText(str(y1992) + ' ' + '[m]')
    
    
    #UKŁAD PL-2000 dla katy 1
    def XY2000(self):
        """
        Przeliczenie na współrzędne do układu PL-2000 dla karty 1

        Raises
        ------
        ValueError
        Jeżeli wyjdziemy poza zakres wartoci phi bądź lambda program nie pozwala policzyć dalej 

        Returns
        -------
        None.

        """
        if len(self.ui.lineEdit_phi.text()) != 0 and float(self.ui.lineEdit_phi.text()) >= 49 and float(self.ui.lineEdit_phi.text()) <= 54.8333: # zakres na phi <49 stopni, 54 stopni 50 minut>
            phi = float(self.ui.lineEdit_phi.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_lambda.text()) != 0 and float(self.ui.lineEdit_lambda.text()) >= 14.1167 and float(self.ui.lineEdit_lambda.text()) <= 24.15: # zakres na lambda <14 stopni 07 minut, 24 stopnie 09 minut>
            lam = float(self.ui.lineEdit_lambda.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla lambdy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            
        self.phi = radians(phi)
        self.lam = radians(lam)
        
        if self.ui.radioButton.isChecked():
            strefa_00 = 5
            lam_0 = 15
            if (float(self.ui.lineEdit_lambda.text()) - lam_0) >= -1.5 and (float(self.ui.lineEdit_lambda.text()) - lam_0) <= 1.5:
                b2 = (self.a**2)*(1 - self.ecc2)
                ep2 = ((self.a**2 - b2))/(b2)
                t = np.tan(self.phi)
                n2 = ep2 * ((np.cos(self.phi))**2)
                N =  self.a / (np.sqrt(1 - self.ecc2 * (np.sin(self.phi)) ** 2))
                A0 = 1-(self.ecc2/4) - ((3*(self.ecc2**2))/64)-((5*(self.ecc2**3))/256)
                A2 = (3/8)*(self.ecc2+((self.ecc2**2)/4)+((15*(self.ecc2**3))/128))
                A4 = (15/256)*((self.ecc2**2)+((3*(self.ecc2**3))/4))
                A6 = (35*(self.ecc2**3))/3072
                lam_0 = radians(lam_0)
                dlam_00 = self.lam - lam_0
                sigma = self.a * (A0 * (self.phi) - (A2 * np.sin(2 * self.phi)) + (A4 * np.sin(4 * self.phi)) - (A6 * np.sin(6 * self.phi)))
                xgk_00 = sigma + ((dlam_00**2)/2) * N * np.sin(self.phi) * np.cos(self.phi) * (1 + ((dlam_00**2)/12) * ((np.cos(self.phi))**2) * (5 - t**2 + 9 * n2 + 4 * (n2**2)) + ((dlam_00**4)/360) * ((np.cos(self.phi))**4) * (61 - (58 * (t**2)) + (t**4) + (270 * n2) - (330 * n2 * (t**2))))
                ygk_00 = dlam_00 * (N * np.cos(self.phi)) * (1 + ((((dlam_00**2)/6) * (np.cos(self.phi))**2) * (1 - t**2 + n2)) + (((dlam_00**4)/(120)) * (np.cos(self.phi)**4)) * (5 - (18 * (t**2)) + (t**4) + (14 * n2) - (58 * n2 * (t**2))))
                m_00 = 0.999923 #skala PL-2000
                x2000 = round((xgk_00 * m_00), 5)
                y2000 = round(((ygk_00 * m_00) + (strefa_00 * 1000000) + 500000), 5)
                self.ui.label_9.setText(str(x2000) + ' ' + '[m]')
                self.ui.label_10.setText(str(y2000) + ' ' + '[m]')
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Wybrano nieprawidłową strefę')
                msg.setInformativeText
                msg.setWindowTitle("Critical Error")
                msg.exec_()
                
            
        elif self.ui.radioButton_3.isChecked():
            strefa_00 = 6
            lam_0 = 18
            if (float(self.ui.lineEdit_lambda.text()) - lam_0) >= -1.5 and (float(self.ui.lineEdit_lambda.text()) - lam_0) <= 1.5:
                b2 = (self.a**2)*(1 - self.ecc2)
                ep2 = ((self.a**2 - b2))/(b2)
                t = np.tan(self.phi)
                n2 = ep2 * ((np.cos(self.phi))**2)
                N =  self.a / (np.sqrt(1 - self.ecc2 * (np.sin(self.phi)) ** 2))
                A0 = 1-(self.ecc2/4) - ((3*(self.ecc2**2))/64)-((5*(self.ecc2**3))/256)
                A2 = (3/8)*(self.ecc2+((self.ecc2**2)/4)+((15*(self.ecc2**3))/128))
                A4 = (15/256)*((self.ecc2**2)+((3*(self.ecc2**3))/4))
                A6 = (35*(self.ecc2**3))/3072
                lam_0 = radians(lam_0)
                dlam_00 = self.lam - lam_0
                sigma = self.a * (A0 * (self.phi) - (A2 * np.sin(2 * self.phi)) + (A4 * np.sin(4 * self.phi)) - (A6 * np.sin(6 * self.phi)))
                xgk_00 = sigma + ((dlam_00**2)/2) * N * np.sin(self.phi) * np.cos(self.phi) * (1 + ((dlam_00**2)/12) * ((np.cos(self.phi))**2) * (5 - t**2 + 9 * n2 + 4 * (n2**2)) + ((dlam_00**4)/360) * ((np.cos(self.phi))**4) * (61 - (58 * (t**2)) + (t**4) + (270 * n2) - (330 * n2 * (t**2))))
                ygk_00 = dlam_00 * (N * np.cos(self.phi)) * (1 + ((((dlam_00**2)/6) * (np.cos(self.phi))**2) * (1 - t**2 + n2)) + (((dlam_00**4)/(120)) * (np.cos(self.phi)**4)) * (5 - (18 * (t**2)) + (t**4) + (14 * n2) - (58 * n2 * (t**2))))
                m_00 = 0.999923 #skala PL-2000
                x2000 = round((xgk_00 * m_00), 5)
                y2000 = round(((ygk_00 * m_00) + (strefa_00 * 1000000) + 500000), 5)
                self.ui.label_9.setText(str(x2000) + ' ' + '[m]')
                self.ui.label_10.setText(str(y2000) + ' ' + '[m]')
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Wybrano nieprawidłową strefę')
                msg.setInformativeText
                msg.setWindowTitle("Critical Error")
                msg.exec_()
            
        elif self.ui.radioButton_2.isChecked():
            strefa_00 = 7
            lam_0 = 21
            if (float(self.ui.lineEdit_lambda.text()) - lam_0) >= -1.5 and (float(self.ui.lineEdit_lambda.text()) - lam_0) <= 1.5:
                b2 = (self.a**2)*(1 - self.ecc2)
                ep2 = ((self.a**2 - b2))/(b2)
                t = np.tan(self.phi)
                n2 = ep2 * ((np.cos(self.phi))**2)
                N =  self.a / (np.sqrt(1 - self.ecc2 * (np.sin(self.phi)) ** 2))
                A0 = 1-(self.ecc2/4) - ((3*(self.ecc2**2))/64)-((5*(self.ecc2**3))/256)
                A2 = (3/8)*(self.ecc2+((self.ecc2**2)/4)+((15*(self.ecc2**3))/128))
                A4 = (15/256)*((self.ecc2**2)+((3*(self.ecc2**3))/4))
                A6 = (35*(self.ecc2**3))/3072
                lam_0 = radians(lam_0)
                dlam_00 = self.lam - lam_0
                sigma = self.a * (A0 * (self.phi) - (A2 * np.sin(2 * self.phi)) + (A4 * np.sin(4 * self.phi)) - (A6 * np.sin(6 * self.phi)))
                xgk_00 = sigma + ((dlam_00**2)/2) * N * np.sin(self.phi) * np.cos(self.phi) * (1 + ((dlam_00**2)/12) * ((np.cos(self.phi))**2) * (5 - t**2 + 9 * n2 + 4 * (n2**2)) + ((dlam_00**4)/360) * ((np.cos(self.phi))**4) * (61 - (58 * (t**2)) + (t**4) + (270 * n2) - (330 * n2 * (t**2))))
                ygk_00 = dlam_00 * (N * np.cos(self.phi)) * (1 + ((((dlam_00**2)/6) * (np.cos(self.phi))**2) * (1 - t**2 + n2)) + (((dlam_00**4)/(120)) * (np.cos(self.phi)**4)) * (5 - (18 * (t**2)) + (t**4) + (14 * n2) - (58 * n2 * (t**2))))
                m_00 = 0.999923 #skala PL-2000
                x2000 = round((xgk_00 * m_00), 5)
                y2000 = round(((ygk_00 * m_00) + (strefa_00 * 1000000) + 500000), 5)
                self.ui.label_9.setText(str(x2000) + ' ' + '[m]')
                self.ui.label_10.setText(str(y2000) + ' ' + '[m]')
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Wybrano nieprawidłową strefę')
                msg.setInformativeText
                msg.setWindowTitle("Critical Error")
                msg.exec_()
            
        elif self.ui.radioButton_4.isChecked():
            strefa_00 = 8
            lam_0 = 24
            if (float(self.ui.lineEdit_lambda.text()) - lam_0) >= -1.5 and (float(self.ui.lineEdit_lambda.text()) - lam_0) <= 1.5:
                b2 = (self.a**2)*(1 - self.ecc2)
                ep2 = ((self.a**2 - b2))/(b2)
                t = np.tan(self.phi)
                n2 = ep2 * ((np.cos(self.phi))**2)
                N =  self.a / (np.sqrt(1 - self.ecc2 * (np.sin(self.phi)) ** 2))
                A0 = 1-(self.ecc2/4) - ((3*(self.ecc2**2))/64)-((5*(self.ecc2**3))/256)
                A2 = (3/8)*(self.ecc2+((self.ecc2**2)/4)+((15*(self.ecc2**3))/128))
                A4 = (15/256)*((self.ecc2**2)+((3*(self.ecc2**3))/4))
                A6 = (35*(self.ecc2**3))/3072
                lam_0 = radians(lam_0)
                dlam_00 = self.lam - lam_0
                sigma = self.a * (A0 * (self.phi) - (A2 * np.sin(2 * self.phi)) + (A4 * np.sin(4 * self.phi)) - (A6 * np.sin(6 * self.phi)))
                xgk_00 = sigma + ((dlam_00**2)/2) * N * np.sin(self.phi) * np.cos(self.phi) * (1 + ((dlam_00**2)/12) * ((np.cos(self.phi))**2) * (5 - t**2 + 9 * n2 + 4 * (n2**2)) + ((dlam_00**4)/360) * ((np.cos(self.phi))**4) * (61 - (58 * (t**2)) + (t**4) + (270 * n2) - (330 * n2 * (t**2))))
                ygk_00 = dlam_00 * (N * np.cos(self.phi)) * (1 + ((((dlam_00**2)/6) * (np.cos(self.phi))**2) * (1 - t**2 + n2)) + (((dlam_00**4)/(120)) * (np.cos(self.phi)**4)) * (5 - (18 * (t**2)) + (t**4) + (14 * n2) - (58 * n2 * (t**2))))
                m_00 = 0.999923 #skala PL-2000
                x2000 = round((xgk_00 * m_00), 5)
                y2000 = round(((ygk_00 * m_00) + (strefa_00 * 1000000) + 500000), 5)
                self.ui.label_9.setText(str(x2000) + ' ' + '[m]')
                self.ui.label_10.setText(str(y2000) + ' ' + '[m]')
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Wybrano nieprawidłową strefę')
                msg.setInformativeText
                msg.setWindowTitle("Critical Error")
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nie wybrano strefy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            
        
    #Przeliczenie ze współrzędnych geodezyjnych phi, lambda, helip na współrzędne geocentryczne XYZ dla karty 1   
    def pl2XYZ(self):
        """
        Przeliczenie ze współrzędnych geodezyjnych phi, lambda, helip na współrzędne geocentryczne XYZ dla karty 1

        Raises
        ------
        ValueError
        Jeżeli wyjdziemy poza zakres wartoci phi bądź lambda program nie pozwala policzyć dalej 

        Returns
        -------
        None.

        """
        if len(self.ui.lineEdit_phi.text()) != 0 and float(self.ui.lineEdit_phi.text()) >= 49 and float(self.ui.lineEdit_phi.text()) <= 54.8333: # zakres na phi <49 stopni, 54 stopni 50 minut>
            phi = float(self.ui.lineEdit_phi.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_lambda.text()) != 0 and float(self.ui.lineEdit_lambda.text()) >= 14.1167 and float(self.ui.lineEdit_lambda.text()) <= 24.15: # zakres na lambda <14 stopni 07 minut, 24 stopnie 09 minut>
            lam = float(self.ui.lineEdit_lambda.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla lambdy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit.text()) != 0:
            hel = float(self.ui.lineEdit.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nie podano wysokości')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            
        self.phi = radians(phi)
        self.lam = radians(lam)
        
        N =  self.a / (sqrt(1 - self.ecc2 * (np.sin(self.phi)) ** 2))
        
        X = round(((N + hel) * np.cos(self.phi) * np.cos(self.lam)), 3)
        Y = round(((N + hel) * np.cos(self.phi) * np.sin(self.lam)), 3)
        Z = round(((N * (1 - self.ecc2) + hel) * np.sin(self.phi)), 3)
        
        self.ui.label_16.setText(str(X) + ' ' + '[m]')
        self.ui.label_17.setText(str(Y) + ' ' + '[m]')
        self.ui.label_18.setText(str(Z) + ' ' + '[m]')
        
        
    # elipsoida dla karty 2
    def select_elipsoida2(self):
        """
        Funkcja, która pozwala wybrać parametry elipsoidy dla karty 2

        Raises
        ------
        NotImplementedError
            Nie zaimplementowano wyboru parametrów elipsoidy

        Returns
        -------
        None.

        """
        if self.ui.radioButton_GRS_4.isChecked() == True:
            self.a = 6378137.0
            self.b = 6356752.31414036
            print("GRS80")
        elif self.ui.radioButton_WGS_4.isChecked() == True:
            self.a = 6378137.0 
            self.b = 6356752.31424518 
            print("WRS84")
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nie wybrano elipsoidy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
         
        
        self.flattening = (self.a - self.b) / self.a
        self.ecc2 = (2 * self.flattening - self.flattening ** 2)
        
    #UKŁAD PL-1992 dla Karty 2
    def XY1992_Karta2(self):
        """
        Przeliczenie na współrzędne do układu PL-1992 dla karty 2

        Raises
        ------
        ValueError
        Jeżeli wyjdziemy poza zakres wartoci phi bądź lambda program nie pozwala policzyć dalej 

        Returns
        -------
        None.

        """
        
        if len(self.ui.lineEdit_4.text())!=0 and float(self.ui.lineEdit_4.text()) >= 0 and float(self.ui.lineEdit_4.text()) <= 60:
            m_phi = float(self.ui.lineEdit_4.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla minut dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_5.text())!=0 and float(self.ui.lineEdit_5.text()) >= 0 and float(self.ui.lineEdit_5.text()) <= 60:
            s_phi = float(self.ui.lineEdit_5.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla sekund dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_7.text())!=0 and float(self.ui.lineEdit_7.text()) >= 0 and float(self.ui.lineEdit_7.text()) <= 60:
            m_lam = float(self.ui.lineEdit_7.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla minut dla lambdy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_8.text())!=0 and float(self.ui.lineEdit_8.text()) >= 0 and float(self.ui.lineEdit_8.text()) <= 60:
            s_lam = float(self.ui.lineEdit_8.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla sekund dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_3.text()) == 0 or len(self.ui.lineEdit_6.text()) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Źle wpisane współrzędne phi lub lambda')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            raise UnboundLocalError('Źle wpisane współrzędne phi lub lambda')
            
        suma_phi = float(self.ui.lineEdit_3.text()) + float(m_phi/60) + float(s_phi/3600)
        suma_lambda = float(self.ui.lineEdit_6.text()) + float(m_lam/60) + float(s_lam/3600)
        
        if len(self.ui.lineEdit_3.text()) != 0 and float(suma_phi) >= 49 and float(suma_phi) <= 54.8333: # zakres na phi <49 stopni, 54 stopni 50 minut>
            phi = float(suma_phi)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_4.text())!= 0 and float(self.ui.lineEdit_4.text()) >= 0 and float(self.ui.lineEdit_4.text()) <= 60:
            pass
        elif len(self.ui.lineEdit_4.text()) == 0 or (float(self.ui.lineEdit_4.text() not in range(0,61))):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla minut dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_6.text()) != 0 and float(suma_lambda) >= 14.1167 and float(suma_lambda) <= 24.15: # zakres na lambda <14 stopni 07 minut, 24 stopnie 09 minut>
            lam = float(suma_lambda)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla lambdy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            
        self.phi = radians(phi)
        self.lam = radians(lam)
            
        #UKŁAD PL-1992
        lam0 = radians(19)
        b2 = (self.a**2)*(1 - self.ecc2)
        ep2 = ((self.a**2 - b2))/(b2)
        t = np.tan(self.phi)
        n2 = ep2 * ((np.cos(self.phi))**2)
        N =  self.a / (np.sqrt(1 - self.ecc2 * (np.sin(self.phi)) ** 2))
        A0 = 1-(self.ecc2/4) - ((3*(self.ecc2**2))/64)-((5*(self.ecc2**3))/256)
        A2 = (3/8)*(self.ecc2+((self.ecc2**2)/4)+((15*(self.ecc2**3))/128))
        A4 = (15/256)*((self.ecc2**2)+((3*(self.ecc2**3))/4))
        A6 = (35*(self.ecc2**3))/3072
        dlam = self.lam - lam0
        sigma = self.a * (A0 * (self.phi) - (A2 * np.sin(2 * self.phi)) + (A4 * np.sin(4 * self.phi)) - (A6 * np.sin(6 * self.phi)))
        xgk = sigma + ((dlam**2)/2) * N * np.sin(self.phi) * np.cos(self.phi) * (1 + ((dlam**2)/12) * ((np.cos(self.phi))**2) * (5 - t**2 + 9 * n2 + 4 * (n2**2)) + ((dlam**4)/360) * ((np.cos(self.phi))**4) * (61 - (58 * (t**2)) + (t**4) + (270 * n2) - (330 * n2 * (t**2))))
        ygk = dlam * (N * np.cos(self.phi)) * (1 + ((((dlam**2)/6) * (np.cos(self.phi))**2) * (1 - t**2 + n2)) + (((dlam**4)/(120)) * (np.cos(self.phi)**4)) * (5 - (18 * (t**2)) + (t**4) + (14 * n2) - (58 * n2 * (t**2))))
        m0 = 0.9993
        x1992 = round((xgk * m0) - 5300000, 5)
        y1992 = round((ygk * m0) + 500000, 5)
        
        self.ui.label_30.setText(str(x1992) + ' ' + '[m]')
        self.ui.label_32.setText(str(y1992) + ' ' + '[m]')
        
        
    #UKŁAD PL-2000 dla karty 2
    def XY2000_Karta2(self):
        """
        Przeliczenie na współrzędne do układu PL-2000 dla karty 2

        Raises
        ------
        ValueError
        Jeżeli wyjdziemy poza zakres wartoci phi bądź lambda program nie pozwala policzyć dalej 

        Returns
        -------
        None.

        """
        if len(self.ui.lineEdit_4.text())!=0 and float(self.ui.lineEdit_4.text()) >= 0 and float(self.ui.lineEdit_4.text()) <= 60:
            m_phi = float(self.ui.lineEdit_4.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla minut dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_5.text())!=0 and float(self.ui.lineEdit_5.text()) >= 0 and float(self.ui.lineEdit_5.text()) <= 60:
            s_phi = float(self.ui.lineEdit_5.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla sekund dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_7.text())!=0 and float(self.ui.lineEdit_7.text()) >= 0 and float(self.ui.lineEdit_7.text()) <= 60:
            m_lam = float(self.ui.lineEdit_7.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla minut dla lambdy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_8.text())!=0 and float(self.ui.lineEdit_8.text()) >= 0 and float(self.ui.lineEdit_8.text()) <= 60:
            s_lam = float(self.ui.lineEdit_8.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla sekund dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            
        if len(self.ui.lineEdit_3.text()) == 0 or len(self.ui.lineEdit_6.text()) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Źle wpisane współrzędne phi lub lambda')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            raise UnboundLocalError('Źle wpisane współrzędne phi lub lambda')
            
        suma_phi = float(self.ui.lineEdit_3.text()) + float(m_phi/60) + float(s_phi/3600)
        suma_lambda = float(self.ui.lineEdit_6.text()) + float(m_lam/60) + float(s_lam/3600)
        
        if len(self.ui.lineEdit_3.text()) != 0 and float(suma_phi) >= 49 and float(suma_phi) <= 54.8333: # zakres na phi <49 stopni, 54 stopni 50 minut>
            phi = float(suma_phi)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            
        if len(self.ui.lineEdit_6.text()) != 0 and float(suma_lambda) >= 14.1167 and float(suma_lambda) <= 24.15: # zakres na lambda <14 stopni 07 minut, 24 stopnie 09 minut>
            lam = float(suma_lambda)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla lambdy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            
        self.phi = radians(phi)
        self.lam = radians(lam)
        
        if self.ui.radioButton_10.isChecked():
            strefa_00 = 5
            lam_0 = 15
            if (float(suma_lambda) - lam_0) >= -1.5 and (float(suma_lambda) - lam_0) <= 1.5:
                b2 = (self.a**2)*(1 - self.ecc2)
                ep2 = ((self.a**2 - b2))/(b2)
                t = np.tan(self.phi)
                n2 = ep2 * ((np.cos(self.phi))**2)
                N =  self.a / (np.sqrt(1 - self.ecc2 * (np.sin(self.phi)) ** 2))
                A0 = 1-(self.ecc2/4) - ((3*(self.ecc2**2))/64)-((5*(self.ecc2**3))/256)
                A2 = (3/8)*(self.ecc2+((self.ecc2**2)/4)+((15*(self.ecc2**3))/128))
                A4 = (15/256)*((self.ecc2**2)+((3*(self.ecc2**3))/4))
                A6 = (35*(self.ecc2**3))/3072
                lam_0 = radians(lam_0)
                dlam_00 = self.lam - lam_0
                sigma = self.a * (A0 * (self.phi) - (A2 * np.sin(2 * self.phi)) + (A4 * np.sin(4 * self.phi)) - (A6 * np.sin(6 * self.phi)))
                xgk_00 = sigma + ((dlam_00**2)/2) * N * np.sin(self.phi) * np.cos(self.phi) * (1 + ((dlam_00**2)/12) * ((np.cos(self.phi))**2) * (5 - t**2 + 9 * n2 + 4 * (n2**2)) + ((dlam_00**4)/360) * ((np.cos(self.phi))**4) * (61 - (58 * (t**2)) + (t**4) + (270 * n2) - (330 * n2 * (t**2))))
                ygk_00 = dlam_00 * (N * np.cos(self.phi)) * (1 + ((((dlam_00**2)/6) * (np.cos(self.phi))**2) * (1 - t**2 + n2)) + (((dlam_00**4)/(120)) * (np.cos(self.phi)**4)) * (5 - (18 * (t**2)) + (t**4) + (14 * n2) - (58 * n2 * (t**2))))
                m_00 = 0.999923 #skala PL-2000
                x2000 = round((xgk_00 * m_00), 5)
                y2000 = round(((ygk_00 * m_00) + (strefa_00 * 1000000) + 500000), 5)
                self.ui.label_36.setText(str(x2000) + ' ' + '[m]')
                self.ui.label_31.setText(str(y2000) + ' ' + '[m]')
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Wybrano nieprawidłową strefę')
                msg.setInformativeText
                msg.setWindowTitle("Critical Error")
                msg.exec_()
            
        elif self.ui.radioButton_11.isChecked():
            strefa_00 = 6
            lam_0 = 18
            if (float(suma_lambda) - lam_0) >= -1.5 and (float(suma_lambda) - lam_0) <= 1.5:
                b2 = (self.a**2)*(1 - self.ecc2)
                ep2 = ((self.a**2 - b2))/(b2)
                t = np.tan(self.phi)
                n2 = ep2 * ((np.cos(self.phi))**2)
                N =  self.a / (np.sqrt(1 - self.ecc2 * (np.sin(self.phi)) ** 2))
                A0 = 1-(self.ecc2/4) - ((3*(self.ecc2**2))/64)-((5*(self.ecc2**3))/256)
                A2 = (3/8)*(self.ecc2+((self.ecc2**2)/4)+((15*(self.ecc2**3))/128))
                A4 = (15/256)*((self.ecc2**2)+((3*(self.ecc2**3))/4))
                A6 = (35*(self.ecc2**3))/3072
                lam_0 = radians(lam_0)
                dlam_00 = self.lam - lam_0
                sigma = self.a * (A0 * (self.phi) - (A2 * np.sin(2 * self.phi)) + (A4 * np.sin(4 * self.phi)) - (A6 * np.sin(6 * self.phi)))
                xgk_00 = sigma + ((dlam_00**2)/2) * N * np.sin(self.phi) * np.cos(self.phi) * (1 + ((dlam_00**2)/12) * ((np.cos(self.phi))**2) * (5 - t**2 + 9 * n2 + 4 * (n2**2)) + ((dlam_00**4)/360) * ((np.cos(self.phi))**4) * (61 - (58 * (t**2)) + (t**4) + (270 * n2) - (330 * n2 * (t**2))))
                ygk_00 = dlam_00 * (N * np.cos(self.phi)) * (1 + ((((dlam_00**2)/6) * (np.cos(self.phi))**2) * (1 - t**2 + n2)) + (((dlam_00**4)/(120)) * (np.cos(self.phi)**4)) * (5 - (18 * (t**2)) + (t**4) + (14 * n2) - (58 * n2 * (t**2))))
                m_00 = 0.999923 #skala PL-2000
                x2000 = round((xgk_00 * m_00), 5)
                y2000 = round(((ygk_00 * m_00) + (strefa_00 * 1000000) + 500000), 5)
                self.ui.label_36.setText(str(x2000) + ' ' + '[m]')
                self.ui.label_31.setText(str(y2000) + ' ' + '[m]')
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Wybrano nieprawidłową strefę')
                msg.setInformativeText
                msg.setWindowTitle("Critical Error")
                msg.exec_()
            
        elif self.ui.radioButton_9.isChecked():
            strefa_00 = 7
            lam_0 = 21
            if (float(suma_lambda) - lam_0) >= -1.5 and (float(suma_lambda) - lam_0) <= 1.5:
                b2 = (self.a**2)*(1 - self.ecc2)
                ep2 = ((self.a**2 - b2))/(b2)
                t = np.tan(self.phi)
                n2 = ep2 * ((np.cos(self.phi))**2)
                N =  self.a / (np.sqrt(1 - self.ecc2 * (np.sin(self.phi)) ** 2))
                A0 = 1-(self.ecc2/4) - ((3*(self.ecc2**2))/64)-((5*(self.ecc2**3))/256)
                A2 = (3/8)*(self.ecc2+((self.ecc2**2)/4)+((15*(self.ecc2**3))/128))
                A4 = (15/256)*((self.ecc2**2)+((3*(self.ecc2**3))/4))
                A6 = (35*(self.ecc2**3))/3072
                lam_0 = radians(lam_0)
                dlam_00 = self.lam - lam_0
                sigma = self.a * (A0 * (self.phi) - (A2 * np.sin(2 * self.phi)) + (A4 * np.sin(4 * self.phi)) - (A6 * np.sin(6 * self.phi)))
                xgk_00 = sigma + ((dlam_00**2)/2) * N * np.sin(self.phi) * np.cos(self.phi) * (1 + ((dlam_00**2)/12) * ((np.cos(self.phi))**2) * (5 - t**2 + 9 * n2 + 4 * (n2**2)) + ((dlam_00**4)/360) * ((np.cos(self.phi))**4) * (61 - (58 * (t**2)) + (t**4) + (270 * n2) - (330 * n2 * (t**2))))
                ygk_00 = dlam_00 * (N * np.cos(self.phi)) * (1 + ((((dlam_00**2)/6) * (np.cos(self.phi))**2) * (1 - t**2 + n2)) + (((dlam_00**4)/(120)) * (np.cos(self.phi)**4)) * (5 - (18 * (t**2)) + (t**4) + (14 * n2) - (58 * n2 * (t**2))))
                m_00 = 0.999923 #skala PL-2000
                x2000 = round((xgk_00 * m_00), 5)
                y2000 = round(((ygk_00 * m_00) + (strefa_00 * 1000000) + 500000), 5)
                self.ui.label_36.setText(str(x2000) + ' ' + '[m]')
                self.ui.label_31.setText(str(y2000) + ' ' + '[m]')
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Wybrano nieprawidłową strefę')
                msg.setInformativeText
                msg.setWindowTitle("Critical Error")
                msg.exec_()
            
        elif self.ui.radioButton_12.isChecked():
            strefa_00 = 8
            lam_0 = 24
            if (float(suma_lambda) - lam_0) >= -1.5 and (float(suma_lambda) - lam_0) <= 1.5:
                b2 = (self.a**2)*(1 - self.ecc2)
                ep2 = ((self.a**2 - b2))/(b2)
                t = np.tan(self.phi)
                n2 = ep2 * ((np.cos(self.phi))**2)
                N =  self.a / (np.sqrt(1 - self.ecc2 * (np.sin(self.phi)) ** 2))
                A0 = 1-(self.ecc2/4) - ((3*(self.ecc2**2))/64)-((5*(self.ecc2**3))/256)
                A2 = (3/8)*(self.ecc2+((self.ecc2**2)/4)+((15*(self.ecc2**3))/128))
                A4 = (15/256)*((self.ecc2**2)+((3*(self.ecc2**3))/4))
                A6 = (35*(self.ecc2**3))/3072
                lam_0 = radians(lam_0)
                dlam_00 = self.lam - lam_0
                sigma = self.a * (A0 * (self.phi) - (A2 * np.sin(2 * self.phi)) + (A4 * np.sin(4 * self.phi)) - (A6 * np.sin(6 * self.phi)))
                xgk_00 = sigma + ((dlam_00**2)/2) * N * np.sin(self.phi) * np.cos(self.phi) * (1 + ((dlam_00**2)/12) * ((np.cos(self.phi))**2) * (5 - t**2 + 9 * n2 + 4 * (n2**2)) + ((dlam_00**4)/360) * ((np.cos(self.phi))**4) * (61 - (58 * (t**2)) + (t**4) + (270 * n2) - (330 * n2 * (t**2))))
                ygk_00 = dlam_00 * (N * np.cos(self.phi)) * (1 + ((((dlam_00**2)/6) * (np.cos(self.phi))**2) * (1 - t**2 + n2)) + (((dlam_00**4)/(120)) * (np.cos(self.phi)**4)) * (5 - (18 * (t**2)) + (t**4) + (14 * n2) - (58 * n2 * (t**2))))
                m_00 = 0.999923 #skala PL-2000
                x2000 = round((xgk_00 * m_00), 5)
                y2000 = round(((ygk_00 * m_00) + (strefa_00 * 1000000) + 500000), 5)
                self.ui.label_36.setText(str(x2000) + ' ' + '[m]')
                self.ui.label_31.setText(str(y2000) + ' ' + '[m]')
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText('Wybrano nieprawidłową strefę')
                msg.setInformativeText
                msg.setWindowTitle("Critical Error")
                msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nie wybrano strefy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            
        #Przeliczenie ze współrzędnych geodezyjnych phi, lambda, helip na współrzędne geocentryczne XYZ dla karty 2   
    def pl2XYZ_Karta2(self):
        """
        Przeliczenie ze współrzędnych geodezyjnych phi, lambda, helip na współrzędne geocentryczne XYZ dla karty 2

        Raises
        ------
        ValueError
        Jeżeli wyjdziemy poza zakres wartoci phi bądź lambda program nie pozwala policzyć dalej 

        Returns
        -------
        None.

        """
        if len(self.ui.lineEdit_4.text())!=0 and float(self.ui.lineEdit_4.text()) >= 0 and float(self.ui.lineEdit_4.text()) <= 60:
            m_phi = float(self.ui.lineEdit_4.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla minut dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_5.text())!=0 and float(self.ui.lineEdit_5.text()) >= 0 and float(self.ui.lineEdit_5.text()) <= 60:
            s_phi = float(self.ui.lineEdit_5.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla sekund dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_7.text())!=0 and float(self.ui.lineEdit_7.text()) >= 0 and float(self.ui.lineEdit_7.text()) <= 60:
            m_lam = float(self.ui.lineEdit_7.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla minut dla lambdy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_8.text())!=0 and float(self.ui.lineEdit_8.text()) >= 0 and float(self.ui.lineEdit_8.text()) <= 60:
            s_lam = float(self.ui.lineEdit_8.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla sekund dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_3.text()) == 0 or len(self.ui.lineEdit_6.text()) == 0:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Źle wpisane współrzędne phi lub lambda')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            raise UnboundLocalError('Źle wpisane współrzędne phi lub lambda')
        
        suma_phi = float(self.ui.lineEdit_3.text()) + float(m_phi/60) + float(s_phi/3600)
        suma_lambda = float(self.ui.lineEdit_6.text()) + float(m_lam/60) + float(s_lam/3600)
        
        if len(self.ui.lineEdit_3.text()) != 0 and float(suma_phi) >= 49 and float(suma_phi) <= 54.8333: # zakres na phi <49 stopni, 54 stopni 50 minut>
            phi = float(suma_phi)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_4.text())!= 0 and float(self.ui.lineEdit_4.text()) >= 0 and float(self.ui.lineEdit_4.text()) <= 60:
            pass
        elif len(self.ui.lineEdit_4.text()) == 0 or (float(self.ui.lineEdit_4.text() not in range(0,61))):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla minut dla phi')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
        if len(self.ui.lineEdit_6.text()) != 0 and float(suma_lambda) >= 14.1167 and float(suma_lambda) <= 24.15: # zakres na lambda <14 stopni 07 minut, 24 stopnie 09 minut>
            lam = float(suma_lambda)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nieprawidłowy zakres dla lambdy')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            
        if len(self.ui.lineEdit_2.text()) != 0:
            hel = float(self.ui.lineEdit_2.text())
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText('Nie podano wysokości')
            msg.setInformativeText
            msg.setWindowTitle("Critical Error")
            msg.exec_()
            
        self.phi = radians(phi)
        self.lam = radians(lam)
        
        N =  self.a / (sqrt(1 - self.ecc2 * (np.sin(self.phi)) ** 2))
        
        X = round(((N + hel) * np.cos(self.phi) * np.cos(self.lam)), 3)
        Y = round(((N + hel) * np.cos(self.phi) * np.sin(self.lam)), 3)
        Z = round(((N * (1 - self.ecc2) + hel) * np.sin(self.phi)), 3)
        
        self.ui.label_34.setText(str(X) + ' ' + '[m]')
        self.ui.label_33.setText(str(Y) + ' ' + '[m]')
        self.ui.label_35.setText(str(Z) + ' ' + '[m]')

if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyApp()
    w.show()
    sys.exit(app.exec_())