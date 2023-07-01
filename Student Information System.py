import sys
from PyQt5.QtWidgets import QTextEdit, QGridLayout, QApplication, QDialog, QLabel, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit, QMessageBox
import sqlite3
import datetime
from PyQt5.QtCore import Qt

class MainWindow(QDialog):
    def __init__(self, username, role):
        super().__init__()

        self.resize(650, 570)
        self.username = username
        self.role = role
        self.layout = QVBoxLayout()
        global window_width
        global window_height
        window_width = self.width()
        window_height = self.height()

        if self.role == "student":
            self.show_student_features()
            self.setWindowTitle("Öğrenci Bilgi Sistemi")
        elif self.role == "teacher":
            self.show_teacher_features()
            self.setWindowTitle("Akademik Bilgi Sistemi")

        self.setLayout(self.layout)

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
            else:
                layout = item.layout()
                if layout:
                    self.clear_layout(layout)

    def show_student_features(self):
        self.clear_layout()

        button_layout = QHBoxLayout()
        self.notes_button = QPushButton("Notlar", self)
        self.notes_button.clicked.connect(self.show_notes)
        button_layout.addWidget(self.notes_button)

        self.notifications_button = QPushButton("Bildirimler", self)
        self.notifications_button.clicked.connect(self.show_notifications)
        button_layout.addWidget(self.notifications_button)

        self.attendance_button = QPushButton("Devamsızlık Durumu", self)
        self.attendance_button.clicked.connect(self.show_attendance)
        button_layout.addWidget(self.attendance_button)

        table_layout = QHBoxLayout()
        self.notes_table = QTableWidget()
        table_layout.addWidget(self.notes_table)
        self.notes_table.hide()

        self.notifications_table = QTableWidget()
        table_layout.addWidget(self.notifications_table)
        self.notifications_table.hide()

        self.attendance_table = QTableWidget()
        table_layout.addWidget(self.attendance_table)
        self.attendance_table.hide()

        button_layout2 = QHBoxLayout()
        self.logout_button = QPushButton("Çıkış Yap", self)
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.setFixedSize(100, 25)
        button_layout2.addWidget(self.logout_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(table_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout2)
        
        self.setLayout(main_layout)
    

    def show_teacher_features(self):
        self.clear_layout()

        button_layout = QHBoxLayout()
        self.new_student_button = QPushButton("Yeni Öğrenci Kaydı", self)
        self.new_student_button.clicked.connect(self.show_new_student_screen)
        button_layout.addWidget(self.new_student_button)

        self.view_grades_button = QPushButton("Öğrencilerin Notlarını Görüntüle", self)
        self.view_grades_button.clicked.connect(self.show_grades_table)
        button_layout.addWidget(self.view_grades_button)

        self.view_attendance_button = QPushButton("Devamsızlık Durumlarını Görüntüle", self)
        self.view_attendance_button.clicked.connect(self.edit_attendance)
        button_layout.addWidget(self.view_attendance_button)

        self.send_notification_button = QPushButton("Duyuru Gönder", self)
        self.send_notification_button.clicked.connect(self.show_notification_dialog)
        button_layout.addWidget(self.send_notification_button)

        table_layout = QHBoxLayout()
        self.grades_table = QTableWidget()
        table_layout.addWidget(self.grades_table)
        self.grades_table.hide()

        self.attendance_table = QTableWidget()
        table_layout.addWidget(self.attendance_table)
        self.attendance_table.hide()

        button_layout2 = QHBoxLayout()
        self.update_grad = QPushButton("Notları Güncelle", self)
        self.update_grad.clicked.connect(self.update_grades)
        self.update_grad.setFixedSize(100, 25)
        button_layout2.addWidget(self.update_grad)
        self.update_grad.hide()

        self.update_att = QPushButton("Devamsızlık Güncelle", self)
        self.update_att.clicked.connect(self.update_attendance)
        self.update_att.setFixedSize(130, 25)
        button_layout2.addWidget(self.update_att)
        self.update_att.hide()

        self.logout_button = QPushButton("Çıkış Yap", self)
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.setFixedSize(100, 25)
        button_layout2.addWidget(self.logout_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(table_layout)
        main_layout.addStretch(1)
        main_layout.addLayout(button_layout2)
        
        self.setLayout(main_layout)


    def logout(self):
        self.close() 
        login_window = LoginWindow()
        login_window.exec_()


    def show_notes(self):
        self.notes_table.setColumnCount(3)
        self.notes_table.setHorizontalHeaderLabels(["Ders Adı", "Vize", "Final"])
        self.layout.addWidget(self.notes_table)

        table_width = self.notes_table.width()
        table_height = self.notes_table.height()
        window_width = self.width()
        window_height = self.height()
        x = (window_width - table_width) // 2
        y = (window_height - table_height) // 2
        self.notes_table.move(x, y)
        column_width = 200
        for col in range(self.notes_table.columnCount()):
            self.notes_table.setColumnWidth(col, column_width)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        dersler = {
            0: "Algoritma_Programlama",
            1: "Devre_teorileri",
            2: "Lineer_cebir",
            3: "Lojik_tasarım",
            4: "Veri_yapilari"
        }

        row = 0
        for i in range(len(dersler)):
            cursor.execute(f"SELECT ders_kodu, vize, final FROM {dersler[i]} WHERE ogrenci_numarasi=?", (self.username,))
            notlar = cursor.fetchall()
            for ders_kodu, vize, final in notlar:
                # Ders adını al
                cursor.execute("SELECT ders_adi FROM Dersler WHERE ders_kodu=?", (ders_kodu,))
                ders_adi = cursor.fetchone()[0]

                ders_adi_item = QTableWidgetItem(ders_adi)
                vize_item = QTableWidgetItem(str(vize))
                final_item = QTableWidgetItem(str(final))
                self.notes_table.setRowCount(row + 1)
                self.notes_table.setItem(row, 0, ders_adi_item)
                self.notes_table.setItem(row, 1, vize_item)
                self.notes_table.setItem(row, 2, final_item)

                row += 1

        conn.close()

        if self.notes_table.isHidden():
            self.notes_table.show()
            if self.notifications_table:
                self.notifications_table.hide()
            if self.attendance_table:
                self.attendance_table.hide()
        else:
            self.notes_table.hide()





    def show_notifications(self):
        self.notifications_table.setColumnCount(4)
        self.notifications_table.setHorizontalHeaderLabels(["Gönderen","Ders Adı","Duyuru", "Tarih"])
        self.layout.addWidget(self.notifications_table)

        table_width = self.notifications_table.width()
        table_height = self.notifications_table.height()
        window_width = self.width()
        window_height = self.height()
        x = (window_width - table_width) // 2
        y = (window_height - table_height) // 2
        self.notifications_table.move(x, y)
        column_width = 150
        for col in range(self.notifications_table.columnCount()):
            self.notifications_table.setColumnWidth(col, column_width)
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        table_names = ["Algoritma_Programlama", "Devre_teorileri", "Lineer_cebir", "Lojik_tasarım", "Veri_yapilari"]

        ders_kodlari = []

        for table_name in table_names:
            query = f"SELECT ders_kodu FROM {table_name} WHERE ogrenci_numarasi = ?"
            cursor.execute(query, (self.username,))
            results = cursor.fetchall()

            for result in results:
                ders_kodu = result[0]
                ders_kodlari.append(ders_kodu)

        bildirimler = []

        for ders_kodu in ders_kodlari:
            query = "SELECT ders_kodu, bildirim, tarih FROM Bildirimler WHERE ders_kodu = ?"
            cursor.execute(query, (ders_kodu,))
            results = cursor.fetchall()

            for result in results:
                bildirimler.append(result)

        row = 0
        self.notifications_table.setRowCount(len(bildirimler))
        for i in range(len(bildirimler)):
            for row, (ders_kodu, bildirim, tarih) in enumerate(bildirimler):
                cursor.execute("SELECT ders_adi FROM Dersler WHERE ders_kodu=?", (ders_kodu,))
                ders_adi = cursor.fetchone()[0]
                cursor.execute("SELECT ad FROM Ogretmenler WHERE ders_kodu=?", (ders_kodu,))
                ogretmen_adi = cursor.fetchone()[0]
                cursor.execute("SELECT soyad FROM Ogretmenler WHERE ders_kodu=?", (ders_kodu,))
                ogretmen_soyadi = cursor.fetchone()[0]
                ogretmen = ogretmen_adi + " " + ogretmen_soyadi
                ogretmen_item = QTableWidgetItem(ogretmen)
                ders_adi_item = QTableWidgetItem(ders_adi)
                bildirim_item = QTableWidgetItem(bildirim)
                tarih_item = QTableWidgetItem(tarih)
                self.notifications_table.setRowCount(row + 1)
                self.notifications_table.setItem(row, 0, ogretmen_item)
                self.notifications_table.setItem(row, 1, ders_adi_item)
                self.notifications_table.setItem(row, 3, tarih_item)

                show_noti_button = QPushButton("Göster")
                show_noti_button.clicked.connect(self.show_noti)
                self.notifications_table.setCellWidget(row, 2, show_noti_button)

                row += 1

        if self.notifications_table.isHidden():
            self.notifications_table.show()
            if self.notes_table:
                self.notes_table.hide()
            if self.attendance_table:
                self.attendance_table.hide()
        else:
            self.notes_table.hide()

    def show_noti(self):
        selected_row = self.notifications_table.currentRow()
        selected_row += 1

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT bildirim FROM Bildirimler WHERE bildirim_id=?", (selected_row,))
        bildirim = cursor.fetchone()[0]

        dialog = QDialog(self)
        dialog.setWindowTitle("Bildirim")
        dialog.setModal(True)

        bildirim_textbox = QLabel(bildirim)

        layout = QGridLayout()
        layout.addWidget(bildirim_textbox, 0, 0)

        dialog.setLayout(layout)
        dialog.exec_()


    def show_attendance(self):
        self.attendance_table.setColumnCount(2)
        self.attendance_table.setHorizontalHeaderLabels(["Ders Adı","Devamsızlık Durumu"])
        self.layout.addWidget(self.attendance_table)

        table_width = self.attendance_table.width()
        table_height = self.attendance_table.height()
        window_width = self.width()
        window_height = self.height()
        x = (window_width - table_width) // 2
        y = (window_height - table_height) // 2
        self.attendance_table.move(x, y)
        column_width = 200
        for col in range(self.attendance_table.columnCount()):
            self.attendance_table.setColumnWidth(col, column_width)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        dersler = {
            0: "Algoritma_Programlama",
            1: "Devre_teorileri",
            2: "Lineer_cebir",
            3: "Lojik_tasarım",
            4: "Veri_yapilari"
        }

        row = 0
        for i in range(len(dersler)):
            cursor.execute(f"SELECT ders_kodu, devamsizlik FROM {dersler[i]} WHERE ogrenci_numarasi=?", (self.username,))
            devamsizlik_durumu = cursor.fetchall()
            for ders_kodu, devamsizlik in devamsizlik_durumu:
                # Ders adını al
                cursor.execute("SELECT ders_adi FROM Dersler WHERE ders_kodu=?", (ders_kodu,))
                ders_adi = cursor.fetchone()[0]

                ders_adi_item = QTableWidgetItem(ders_adi)
                devamsizlik_item = QTableWidgetItem(str(devamsizlik))
                self.attendance_table.setRowCount(row + 1)
                self.attendance_table.setItem(row, 0, ders_adi_item)
                self.attendance_table.setItem(row, 1, devamsizlik_item)

                row += 1


        if self.attendance_table.isHidden():
            self.attendance_table.show()
            if self.notifications_table:
                self.notifications_table.hide()
            if self.notes_table:
                self.notes_table.hide()
        else:
            self.attendance_table.hide()


    def show_new_student_screen(self):
        if ders_kodu == 0:
            QMessageBox.warning(self, "Hata", "Kayıtlı olduğunuz ders yok")
        else:
            self.dialog = QDialog(self)
            self.dialog.setWindowTitle("Yeni Öğrenci Kaydı")

            layout = QVBoxLayout(self.dialog)
            layout.setContentsMargins(20, 20, 20, 20)

            self.name_label = QLabel("Ad:")
            self.name_input = QLineEdit()

            self.surname_label = QLabel("Soyad:")
            self.surname_input = QLineEdit()

            self.number_label = QLabel("Numara:")
            self.number_input = QLineEdit()

            self.class_label = QLabel("Sınıf:")
            self.class_input = QLineEdit()

            self.password_label = QLabel("Şifre:")
            self.password_input = QLineEdit()

            self.save_button = QPushButton("Kaydet")
            self.save_button.clicked.connect(self.save_student)

            self.back_button = QPushButton("Geri Dön")
            self.back_button.clicked.connect(self.dialog.close)

            layout.addWidget(self.name_label)
            layout.addWidget(self.name_input)
            layout.addWidget(self.surname_label)
            layout.addWidget(self.surname_input)
            layout.addWidget(self.number_label)
            layout.addWidget(self.number_input)
            layout.addWidget(self.class_label)
            layout.addWidget(self.class_input)
            layout.addWidget(self.password_label)
            layout.addWidget(self.password_input)
            layout.addWidget(self.save_button)
            layout.addWidget(self.back_button)

            self.dialog.exec_()

    def save_student(self):
        ad = self.name_input.text()
        soyad = self.surname_input.text()
        numara = self.number_input.text()
        sinif = self.class_input.text()
        sifre = self.password_input.text()

        if ad and soyad and numara and sifre and sinif:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT ogrenci_numarasi FROM Ogrenciler WHERE ogrenci_numarasi = ?", (numara,))
            ogrenci_kontrol = cursor.fetchone()
            cursor.execute(f"SELECT ogrenci_numarasi FROM {ders} WHERE ogrenci_numarasi = ?", (numara,))
            ders_kontrol = cursor.fetchone()
            if ogrenci_kontrol and ders_kontrol:
                QMessageBox.warning(self, "Hata", "Bu öğrenci numarası zaten mevcut.")
            elif ogrenci_kontrol:
                cursor.execute(f"INSERT INTO {ders} (ders_kodu, ogrenci_numarasi, vize, final) VALUES (?, ?, ?, ?)", (ders_kodu, numara, " ", " "))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Başarılı", "Yeni öğrenci kaydı başarıyla oluşturuldu.")
            else:
                cursor.execute("INSERT INTO Ogrenciler (ad, soyad, ogrenci_numarasi, sifre, sinif_bilgisi) VALUES (?, ?, ?, ?, ?)", (ad, soyad, numara, sifre, sinif))
                cursor.execute(f"INSERT INTO {ders} (ders_kodu, ogrenci_numarasi, vize, final) VALUES (?, ?, ?, ?)", (ders_kodu, numara, " ", " "))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Başarılı", "Yeni öğrenci kaydı başarıyla oluşturuldu.")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun.")

    def show_grades_table(self):
        if ders_kodu == 0:
            QMessageBox.warning(self, "Hata", "Kayıtlı olduğunuz ders yok.")
        else:
            self.grades_table.setColumnCount(5)
            self.grades_table.setHorizontalHeaderLabels(["Öğrenci Numarası","Öğrenci Adı Soyadı", "Vize", "Final", "Güncelle"])
            self.layout.addWidget(self.grades_table)

            table_width = self.grades_table.width()
            table_height = self.grades_table.height()
            window_width = self.width()
            window_height = self.height()
            x = (window_width - table_width) // 2
            y = (window_height - table_height) // 2
            self.grades_table.move(x, y)
            column_width = 115
            for col in range(self.grades_table.columnCount()):
                self.grades_table.setColumnWidth(col, column_width)

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute(f"SELECT ogrenci_numarasi, vize, final FROM {ders}")
            notlar_ = cursor.fetchall()

            row = 0
            for i in range(len(notlar_)):
                for row, (ogrenci_numarasi, vize, final) in enumerate(notlar_):
                    cursor.execute("SELECT ogrenci_numarasi FROM Ogrenciler WHERE ogrenci_numarasi=?", (ogrenci_numarasi,))
                    ogrenci_numarasi = cursor.fetchone()[0]

                    cursor.execute("SELECT ad FROM Ogrenciler WHERE ogrenci_numarasi=?", (ogrenci_numarasi,))
                    ogrenci_adi = cursor.fetchone()[0]

                    cursor.execute("SELECT soyad FROM Ogrenciler WHERE ogrenci_numarasi=?", (ogrenci_numarasi,))
                    ogrenci_soyadi = cursor.fetchone()[0]

                    ogrenci = ogrenci_adi + " " + ogrenci_soyadi
                    numara_item = QTableWidgetItem(str(ogrenci_numarasi))
                    ogrenci_item = QTableWidgetItem(ogrenci)
                    vize_item = QTableWidgetItem(str(vize))
                    final_item = QTableWidgetItem(str(final))

                    self.grades_table.setRowCount(row + 1)
                    self.grades_table.setItem(row, 0, numara_item)
                    self.grades_table.setItem(row, 1, ogrenci_item)
                    self.grades_table.setItem(row, 2, vize_item)
                    self.grades_table.setItem(row, 3, final_item)

                    update_student_button = QPushButton("Güncelle")
                    update_student_button.clicked.connect(self.update_student_info)
                    self.grades_table.setCellWidget(row, 4, update_student_button)

                    row += 1

            if self.update_grad.isHidden():
                self.update_grad.show()
                if self.update_att:
                    self.update_att.hide()


            if self.grades_table.isHidden():
                self.grades_table.show()
                if self.attendance_table:
                    self.attendance_table.hide()


    def update_grades(self):
        for row in range(self.grades_table.rowCount()):
            vize_item = self.grades_table.item(row, 2)
            final_item = self.grades_table.item(row, 3)
            ogrenci_numara = self.grades_table.item(row, 0).text()
            vize_notu = vize_item.text()
            final_notu = final_item.text()
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            sorgu = f"UPDATE {ders} SET vize = ?, final = ? WHERE ogrenci_numarasi = ?"
            cursor.execute(sorgu, (vize_notu, final_notu, ogrenci_numara))
            conn.commit()

            conn.close()

        QMessageBox.information(self, "Bilgi", "Notlar güncellendi!")
    
    def update_student_info(self):
        selected_row = self.grades_table.currentRow()

        ogrenci_numarasi_item = self.grades_table.item(selected_row, 0)
        ogrenci_numarasi = ogrenci_numarasi_item.text()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT ad FROM Ogrenciler WHERE ogrenci_numarasi=?", (ogrenci_numarasi,))
        ogrenci_adi = cursor.fetchone()[0]

        cursor.execute("SELECT soyad FROM Ogrenciler WHERE ogrenci_numarasi=?", (ogrenci_numarasi,))
        ogrenci_soyadi = cursor.fetchone()[0]

        cursor.execute("SELECT sifre FROM Ogrenciler WHERE ogrenci_numarasi=?", (ogrenci_numarasi,))
        ogrenci_sifresi = cursor.fetchone()[0]

        cursor.execute("SELECT sinif_bilgisi FROM Ogrenciler WHERE ogrenci_numarasi=?", (ogrenci_numarasi,))
        ogrenci_sinifi = cursor.fetchone()[0]

        dialog = QDialog(self)
        dialog.setWindowTitle("Öğrenci Bilgileri Güncelle")
        dialog.setModal(True)

        ad_label = QLabel("Ad:")
        soyad_label = QLabel("Soyad:")
        numara_label = QLabel("Öğrenci Numarası:")
        sifre_label = QLabel("Şifre:")
        sinif_label = QLabel("Sınıf:")

        ad_textbox = QLineEdit(ogrenci_adi)
        soyad_textbox = QLineEdit(ogrenci_soyadi)
        numara_textbox = QLineEdit(ogrenci_numarasi)
        sifre_textbox = QLineEdit(ogrenci_sifresi)
        sinif_textbox = QLineEdit(ogrenci_sinifi)

        kaydet_button = QPushButton("Kaydet")
        iptal_button = QPushButton("İptal")

        def kaydet():
            yeni_adi = ad_textbox.text()
            yeni_soyadi = soyad_textbox.text()
            yeni_numarasi = numara_textbox.text()
            yeni_sifre = sifre_textbox.text()
            yeni_sinif = sinif_textbox.text()

            sorgu = f"UPDATE Ogrenciler SET ad = ?, soyad = ?, ogrenci_numarasi = ?, sifre = ?, sinif_bilgisi = ? WHERE ogrenci_numarasi = ?"
            cursor.execute(sorgu, (yeni_adi, yeni_soyadi, yeni_numarasi, yeni_sifre, yeni_sinif, ogrenci_numarasi))
            sorgu = f"UPDATE {ders} SET ogrenci_numarasi = ? WHERE ogrenci_numarasi = ?"
            cursor.execute(sorgu, (yeni_numarasi, ogrenci_numarasi))
            conn.commit()
            yeni_adi_soyadi = yeni_adi + " " + yeni_soyadi
            self.grades_table.item(selected_row, 0).setText(f"{yeni_numarasi}")
            self.grades_table.item(selected_row, 1).setText(f"{yeni_adi_soyadi}")
            QMessageBox.information(self, "Bilgi", "Öğrenci bilgileri güncellendi!")

            dialog.close()

        def iptal():
            dialog.close()

        kaydet_button.clicked.connect(kaydet)
        iptal_button.clicked.connect(iptal)

        layout = QGridLayout()
        layout.addWidget(ad_label, 0, 0)
        layout.addWidget(ad_textbox, 0, 1)
        layout.addWidget(soyad_label, 1, 0)
        layout.addWidget(soyad_textbox, 1, 1)
        layout.addWidget(numara_label, 2, 0)
        layout.addWidget(numara_textbox, 2, 1)
        layout.addWidget(sifre_label, 3, 0)
        layout.addWidget(sifre_textbox, 3, 1)
        layout.addWidget(sinif_label, 4, 0)
        layout.addWidget(sinif_textbox, 4, 1)
        layout.addWidget(kaydet_button, 5, 0)
        layout.addWidget(iptal_button, 5, 1)

        dialog.setLayout(layout)
        dialog.exec_()

    
    def edit_attendance(self):
        if ders_kodu == 0:
            QMessageBox.warning(self, "Hata", "Kayıtlı olduğunuz ders yok")
        else:
            self.attendance_table.setColumnCount(3)
            self.attendance_table.setHorizontalHeaderLabels(["Öğrenci Numarası","Öğrenci Adı Soyadı", "Devamsızlık Durumu"])
            self.layout.addWidget(self.attendance_table)
            table_width = self.attendance_table.width()
            table_height = self.attendance_table.height()
            window_width = self.width()
            window_height = self.height()
            x = (window_width - table_width) // 2
            y = (window_height - table_height) // 2
            self.attendance_table.move(x, y)
            column_width = 190
            for col in range(self.attendance_table.columnCount()):
                self.attendance_table.setColumnWidth(col, column_width)
            
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute(f"SELECT ogrenci_numarasi, devamsizlik FROM {ders}")
            devamsizlik = cursor.fetchall()
            row = 0
            self.attendance_table.setRowCount(len(devamsizlik))
            for i in range(len(devamsizlik)):
                for row, (ogrenci_numarasi, devamsizlik_sayisi) in enumerate(devamsizlik):
                    cursor.execute("SELECT ogrenci_numarasi FROM Ogrenciler WHERE ogrenci_numarasi=?", (ogrenci_numarasi,))
                    ogrenci_numarasi = cursor.fetchone()[0]
                    cursor.execute("SELECT ad FROM Ogrenciler WHERE ogrenci_numarasi=?", (ogrenci_numarasi,))
                    ogrenci_adi = cursor.fetchone()[0]
                    cursor.execute("SELECT soyad FROM Ogrenciler WHERE ogrenci_numarasi=?", (ogrenci_numarasi,))
                    ogrenci_soyadi = cursor.fetchone()[0]
                    ogrenci = ogrenci_adi + " " + ogrenci_soyadi
                    numara_item = QTableWidgetItem(str(ogrenci_numarasi))
                    ogrenci_item = QTableWidgetItem(ogrenci)
                    devamsizlik_item = QTableWidgetItem(str(devamsizlik_sayisi))
                    self.attendance_table.setRowCount(row + 1)
                    self.attendance_table.setItem(row, 0, numara_item)
                    self.attendance_table.setItem(row, 1, ogrenci_item)
                    self.attendance_table.setItem(row, 2, devamsizlik_item)

                    row += 1

            if self.update_att.isHidden():
                self.update_att.show()
                if self.update_grad:
                    self.update_grad.hide()

            if self.attendance_table.isHidden():
                self.attendance_table.show()
                if self.grades_table:
                    self.grades_table.hide()

    def update_attendance(self):
        for row in range(self.attendance_table.rowCount()):
            devamsizlik_item = self.attendance_table.item(row, 2)
            ogrenci_numara = self.attendance_table.item(row, 0).text()
            devamsizlik_durumu = devamsizlik_item.text()
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            sorgu = f"UPDATE {ders} SET devamsizlik = ? WHERE ogrenci_numarasi = ?"
            cursor.execute(sorgu, (devamsizlik_durumu, ogrenci_numara))
            conn.commit()

            conn.close()

        QMessageBox.information(self, "Bilgi", "Devamsızlık güncellendi!")

    def show_notification_dialog(self):
        if ders_kodu == 0:
            QMessageBox.warning(self, "Hata", "Kayıtlı olduğunuz ders yok")
        else:
            self.notification_dialog = QDialog(self)
            self.notification_dialog.setWindowTitle("Duyuru Gönder")

            layout = QVBoxLayout()
            self.notification_textbox = QTextEdit()
            self.notification_textbox.setFixedWidth(600)
            self.notification_textbox.setFixedHeight(100)
            self.notification_textbox.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.notification_textbox.setLineWrapMode(QTextEdit.WidgetWidth)
            layout.addWidget(self.notification_textbox)

            send_button = QPushButton("Gönder")
            send_button.clicked.connect(self.send_notification)
            send_button.setFixedSize(100, 25)
            layout.addWidget(send_button)

            self.notification_dialog.setLayout(layout)
            self.notification_dialog.exec_()

    def send_notification(self):
        notification = self.notification_textbox.toPlainText()
        if notification:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            tarih = datetime.date.today().strftime("%d.%m.%Y")
            cursor.execute("INSERT INTO Bildirimler (ders_kodu, bildirim, tarih) VALUES (?, ?, ?)", (ders_kodu, notification, tarih))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Bilgi", "Duyuru gönderildi!")
        else:
            QMessageBox.warning(self, "Uyarı", "Duyuru metni boş olamaz!")

    


class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Giriş Ekranı")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.show_login_buttons()

    def show_login_buttons(self):
        self.clear_layout()
        self.student_button = QPushButton("Öğrenci Girişi", self)
        self.student_button.clicked.connect(self.show_student_login)
        self.student_button.setFixedSize(90, 75)

        self.teacher_button = QPushButton("Öğretmen Girişi", self)
        self.teacher_button.clicked.connect(self.show_teacher_login)
        self.teacher_button.setFixedSize(90, 75)

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.student_button)
        button_layout.addWidget(self.teacher_button)

        self.layout.addLayout(button_layout)

    def show_student_login(self):
        self.layout.removeWidget(self.student_button)
        self.layout.removeWidget(self.teacher_button)
        self.student_button.hide()
        self.teacher_button.hide()

        self.username_label = QLabel("Öğrenci Numarası:", self)
        self.username_input = QLineEdit(self)

        self.password_label = QLabel("Şifre:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Giriş", self)
        self.login_button.clicked.connect(self.student_login)

        self.back_button = QPushButton("Geri Dön", self)
        self.back_button.clicked.connect(self.show_login_buttons)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.back_button)

    def show_teacher_login(self):
        self.layout.removeWidget(self.student_button)
        self.layout.removeWidget(self.teacher_button)
        self.student_button.hide()
        self.teacher_button.hide()

        self.username_label = QLabel("Kullanıcı Adı:", self)
        self.username_input = QLineEdit(self)

        self.password_label = QLabel("Şifre:", self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Giriş", self)
        self.login_button.clicked.connect(self.teacher_login)

        self.register_button = QPushButton("Kayıt Ol", self)
        self.register_button.clicked.connect(self.show_teacher_sign_in_form)

        self.back_button = QPushButton("Geri Dön", self)
        self.back_button.clicked.connect(self.show_login_buttons)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.register_button)
        self.layout.addWidget(self.back_button)

    def clear_layout(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def student_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT sifre FROM Ogrenciler WHERE ogrenci_numarasi=?", (username,))
        ogrenci = cursor.fetchone()

        if ogrenci:
            dogru_sifre = ogrenci[0]
            if password == dogru_sifre:
                self.accept()
                main_window = MainWindow(username, "student")
                main_window.exec_()
            else:
                QMessageBox.warning(self, "Giriş Hatası", "Şifre yanlış!")
        else:
            QMessageBox.warning(self, "Giriş Hatası", "Kullanıcı adı bulunamadı!")



    def teacher_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT sifre FROM Ogretmenler WHERE kullanici_adi=?", (username,))
        ogretmen = cursor.fetchone()

        if ogretmen:
            dogru_sifre = ogretmen[0]
            if password == dogru_sifre:
                cursor.execute("SELECT ders_kodu FROM Ogretmenler WHERE kullanici_adi=?", (username,))
                kod = cursor.fetchone()[0]
                global ders_kodu
                ders_kodu = kod
                global ders
                if ders_kodu == 131712129:
                    ders = "Algoritma_Programlama"
                if ders_kodu == 131723108:
                    ders = "Devre_teorileri"
                if ders_kodu == 131711101:
                    ders = "Lineer_cebir"
                if ders_kodu == 131723109:
                    ders = "Lojik_tasarım"
                if ders_kodu == 131724111:
                    ders = "Veri_yapilari"
                self.accept()
                main_window = MainWindow(username, "teacher")
                main_window.exec_()
            else:
                QMessageBox.warning(self, "Giriş Hatası", "Şifre yanlış!")
        else:
            QMessageBox.warning(self, "Giriş Hatası", "Kullanıcı adı bulunamadı!")
    
    def show_teacher_sign_in_form(self):
        self.clear_layout()

        self.name_label = QLabel("Ad:", self)
        self.name_input = QLineEdit(self)

        self.surname_label = QLabel("Soyad:", self)
        self.surname_input = QLineEdit(self)

        self.username_label = QLabel("Kullanıcı Adı:", self)
        self.username_input = QLineEdit(self)

        self.password_label = QLabel("Şifre:", self)
        self.password_input = QLineEdit(self)

        self.sign_in_button = QPushButton("Kayıt Ol", self)
        self.sign_in_button.clicked.connect(self.register_teacher)

        self.back_button = QPushButton("Geri Dön", self)
        self.back_button.clicked.connect(self.show_login_buttons)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.surname_label)
        self.layout.addWidget(self.surname_input)
        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.sign_in_button)
        self.layout.addWidget(self.back_button)


    def register_teacher(self):
        ad = self.name_input.text()
        soyad = self.surname_input.text()
        kullanici_adi = self.username_input.text()
        sifre = self.password_input.text()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Ogretmenler (ad, soyad, kullanici_adi, sifre, ders_kodu) VALUES (?, ?, ?, ?, 0)",
                    (ad, soyad, kullanici_adi, sifre))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Bilgi", "Kayıt başarıyla tamamlandı!")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_window = LoginWindow()
    login_window.resize(200,90)
    if login_window.exec_() == QDialog.Accepted:
        main_window = MainWindow(login_window.username, login_window.role)
        main_window.exec_()

    sys.exit(app.exec_())
