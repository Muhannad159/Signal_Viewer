# PyQt5 importing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType  # Live updating the design

import pyqtgraph as pg
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
_translate = QtCore.QCoreApplication.translate

from pyqtgraph import PlotWidget, plot
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene
import numpy as np
import pandas as pd

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import os
from os import path
import sys

FORM_CLASS, _ = loadUiType(path.join(path.dirname(__file__), "main.ui"))  # connects the Ui file with the Python file


class MainApp(QMainWindow, FORM_CLASS):  # go to the main window in the form_class file

    def __init__(self, parent=None):  # constructor to intiate the main window  in the design
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        num_tabs = 1
        self.setupUi(self)
        self.Handle_btn()
        self.signals_data = {}
        self.count_signals = 0;


    def Handle_btn(self):
        # menu buttons
        self.open_menu_btn.triggered.connect(self.add_new_tab)
        self.make_pdf_btn.triggered.connect(self.gen_pdf)
        # graph buttons
        self.graph1_radio_btn.toggled.connect(self.graph1_selected)
        self.graph2_radio_btn.toggled.connect(self.graph2_selected)
        self.link_radio_btn.toggled.connect(self.link_selected)
        self.speed_push_btn.clicked.connect(self.speed_changed)
        self.play_push_btn.clicked.connect(self.play_changed)
        self.rewind_push_btn.clicked.connect(self.rewind_changed)
        self.zoom_slider.valueChanged.connect(self.zoom_slider_update)
        self.move_x_slider.valueChanged.connect(self.move_x_slider_update)
        self.move_y_slider.valueChanged.connect(self.move_y_slider_update)
        # signal buttons
        self.hide_g1_check_btn.stateChanged.connect(self.hide_g1_btn_checked)
        self.hide_g2_check_btn.stateChanged.connect(self.hide_g2_btn_checked)
        self.color_g1_combo_btn.activated[str].connect(self.color_combo_selected)
        self.color_g2_combo_btn.activated[str].connect(self.color_combo_selected)
        self.save_lbl_g1_btn.clicked.connect(self.line_edit_g1_selected)
        self.save_lbl_g2_btn.clicked.connect(self.line_edit_g2_selected)
        self.tab_widget_g1.currentChanged.connect(self.tab_widget_g1_changed)
        self.tab_widget_g2.currentChanged.connect(self.tab_widget_g2_changed)


    def create_new_tab(self):
        # new tab creating
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        # creating color label
        self.color_lbl = QtWidgets.QLabel(self.tab_1)
        self.color_lbl.setObjectName("color_lbl")
        self.color_lbl.setText(_translate("MainWindow", "Color"))
        self.horizontalLayout_6.addWidget(self.color_lbl)
        # creating color combo box
        self.color_g1_combo_btn = QtWidgets.QComboBox(self.tab_1)
        self.color_g1_combo_btn.setObjectName("color_g1_combo_btn")
        color_list = ["-----", "red", "blue", "green", "orange"]
        self.color_g1_combo_btn.addItems(color_list)
        self.horizontalLayout_6.addWidget(self.color_g1_combo_btn)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        spacerItem = QtWidgets.QSpacerItem(20, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem)
        # creating hide check box
        self.hide_g1_check_btn = QtWidgets.QCheckBox(self.tab_1)
        self.hide_g1_check_btn.setObjectName("hide_g1_check_btn")
        self.hide_g1_check_btn.setText(_translate("MainWindow", "Hide Signal"))
        self.verticalLayout_6.addWidget(self.hide_g1_check_btn)
        spacerItem1 = QtWidgets.QSpacerItem(20, 7, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.verticalLayout_6.addItem(spacerItem1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        # creating label for signal
        self.label_6 = QtWidgets.QLabel(self.tab_1)
        self.label_6.setObjectName("label_6")
        self.label_6.setText(_translate("MainWindow", "Label"))
        self.horizontalLayout_7.addWidget(self.label_6)
        # creating line edit
        self.line_edit_g1 = QtWidgets.QLineEdit(self.tab_1)
        self.line_edit_g1.setObjectName("line_edit_g1")
        self.horizontalLayout_7.addWidget(self.line_edit_g1)
        # creating save button
        self.save_lbl_g1_btn = QtWidgets.QPushButton(self.tab_1)
        self.save_lbl_g1_btn.setObjectName("save_lbl_g1_btn")
        self.save_lbl_g1_btn.setText(_translate("MainWindow", "Save"))
        self.horizontalLayout_7.addWidget(self.save_lbl_g1_btn)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        return self.tab_1

    def add_new_tab(self):
        new_tab_g_1 = self.create_new_tab()
        new_tab_g_2 = self.create_new_tab()
        self.tab_widget_g1.addTab(new_tab_g_1, "")
        self.tab_widget_g1.setTabText(self.tab_widget_g1.indexOf(new_tab_g_1), _translate("MainWindow", "Sig_3"))
        self.tab_widget_g2.addTab(new_tab_g_2, "")
        self.tab_widget_g2.setTabText(self.tab_widget_g2.indexOf(new_tab_g_2), _translate("MainWindow", "Sig_3"))

        # activating methods
        self.Handle_btn()

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_path:
            self.count_signals += 1
            file_name = file_path.split("/")[-1]
        #print(file_name)
            signal_data = pd.read_csv(file_name)
        #print(signal_data)
            time_column = signal_data.iloc[:, 0]  
            values_column = signal_data.iloc[:, 1]  
        # Convert the extracted columns to lists 
            time_values = time_column.tolist()
            v_values = values_column.tolist()
        # print(time_values)
        # print(v_values)
            print(self.count_signals)
            self.signals_data[self.count_signals] = [time_values,v_values, 'red',self.count_signals,False]
            print(self.signals_data[self.count_signals][2])

    def gen_pdf(self):
        pdf_filename = 'empty_pdf.pdf'
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        c.save()
        print(f'Empty PDF saved as {pdf_filename}')

    def graph1_selected(self, enabled):
        if enabled:
            print('graph1')

    def graph2_selected(self, enabled):
        if enabled:
            print('graph2')

    def link_selected(self, enabled):
        if enabled:
            print('link')

    def speed_changed(self):
        print("speed change")

    def play_changed(self, state):
        print("play")

    def rewind_changed(self):
        print("rewind")

    def zoom_slider_update(self):
        value = self.zoom_slider.value()
        print(value)

    def move_x_slider_update(self):
        value = self.move_x_slider.value()
        print(value)

    def move_y_slider_update(self):
        value = self.move_y_slider.value()
        print(value)

    def tab_widget_g1_changed(self):
        current_tab = self.tab_widget_g1.currentIndex()
        print(current_tab)

    def tab_widget_g2_changed(self):
        current_tab = self.tab_widget_g2.currentIndex()
        print(current_tab)

    def hide_g1_btn_checked(self):
        if self.hide_g1_check_btn.isChecked() == True:
            print("checked")

        else:
            print("unchecked")

    def hide_g2_btn_checked(self):
        if self.hide_g2_check_btn.isChecked() == True:
            print("checked")

        else:
            print("unchecked")

    def color_combo_selected(self, text):
        print(text)

    def line_edit_g1_selected(self):
        print(self.line_edit_g1.text())

    def line_edit_g2_selected(self):
        print(self.line_edit_g2.text())

def main():  # method to start app
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()  # infinte Loop


if __name__ == '__main__':
    main()
