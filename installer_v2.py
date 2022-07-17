import os, shutil, stat, subprocess, sys, time, base64, json
from ctypes import windll
import urllib.request as URL
from urllib.parse import urlencode
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from start_design import Ui_StartWindow
from load_design import Ui_LoadWindow

windll.shell32.SetCurrentProcessExplicitAppUserModelID('L3.minecraft.1341.101')

logo = '''
iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAASGSURBVHhe7Zt9aFZVHMe/jyUzX8JKy0yc1cyyNyoZlqi0EBpIos5YZX8oIg6dsVAGFWjgC4Mgav4zJppkNMtpGriJ9KYj0hZR5EzyZbjZ1LTUkQ3L5vf33N9jZw97ec7dyHOf83zgt3N+594/9vvee37n5T4nhk5ob28fwKKANoM2gTaGFkUaafW0HbStsVisTRq7hcEX0Jpo6YbEJA+1A9feAF68kcXbtCXxhvRlHa2Eb8M/4pgClLNI9+ATrKMAxVKJC6CvxsdS94g5FGFrjMFLwvuFNire7A/NtLH9+Eeevm/BCxJzgQggQ52vzJAucJyVqI7zvaVRBGhXx0ukC3hNRgAtvSUjgJbekhFAS2+xnwcsfx/YfkAdJf8xoHy+On3I9v3Ad8eApnPAibPA8JuB+0ZyBj8CeIAz2dwcvTE8bgrw7i7gwzrgt1Zt6IJZuVzA5wOjh2mDPe51gbJPKEBNz8EL2/gg8t5kyTclJG4JsPIjoPIzdQxuGwxMHNv1k15VTcEuqmOHOwKcZQCb96lj8NpMYP9aXlsKfL4C2FkK3DlULyoX/wJWU4QQuCNAxR6tGCx5Fpifp44ynslvSwmQJVuYBl81aMUOdwQYdxcw6X51lAVJwScYeWuQeE1a24DDJ9VJHXcEKJgIbFoMHCkHNhQBcycDg2/Si53wSLZWDI6d0UrquJUEE0wZz4T4vDpdcPq8Vgwe7USUHnBTgFRoSHrdb+ckSbqGJdEUoPobYN8hdZRXp2vFjmgJ8OvvwUSp9ANtUPIeYg55Uh073F4LLKwADjUDA7OAlj+AS5f1gkHhU5wIvaCOPe6/AS1MdkdPdwy+/w0cIp8J5gO9CF6IZg74+wpQ8z3w7dHgzegF0R0FTjIfvLWT3W8NsDfcLFBwOwf8qb9nuMwn3sr5/hl2h9ofgPe+DNpNyl4CZnMyZYnbb8CgAYHdMihYCU7IAd6YTbHn6Q0G5bVasSOaXSD/caCYCyWT5nNcMe5VJ3WimwOmP6EVg4PyxduO6Apw7wj+90m/8WpMl8VQqgyR33YYyPBoiTsCXPkX+LQeKKoEcoqDIa47LlyicWQweXi0VlLHDQFkN2fcK0DJJmDPj0Fb3c9B2RWyZZ7MdRVAphO2lmAq1//ZSRuePzUBG79QJ4kGJrt3dqljEEKAvpkIhWX360EyE6rqOMZvCeomsjM0Mxe45w7gFCdC8r2g6mtOjuI/8/uPRdOAZc+pkzruCCCUbuZaP8Qe/9MPApWL1LHDrVGgbC7w8hR1UkS+F6x9UR173BsGV8wBKhb2/N1PvhOuYeDyvWAY6yGx7wKyK9NX9LSHd+AI+z2Xu7InIP1/KNcEkiyzhwffB7L6643hsRcgzXCvC/zPZATQ0lsyAmjpLRkBtPQWEcB+Hyl9aBYB5Fydr9SLAHKo0Fd2yFRYNtaO04x1qRecot3dT4+TlsSb/EIOT7bFRwFWqlisl7onrNeYOwyDRTQfRJAYJdbOYU4opLXIMjnNkJgKNcxrdHd8Xm5OHJ+P6sFKmeMkjs9Xab4zAK4C8+8I8SO2mboAAAAASUVORK5CYII=
'''


def delete_file(list_file: list, path: os.path):
    for file in list_file:
        try:
            os.remove(f"{path}\\{file}")
        except:
            continue


class DownloadTread(QObject):
    progress_value = pyqtSignal(int)
    status_label = pyqtSignal(str)
    speed_label = pyqtSignal(str)

    def __init__(self, main_path, delete, file, checkedJson):
        super().__init__()
        self.checkedJson = checkedJson
        self.main_path = main_path
        self.delete = delete
        self.file = file
        self.file_size = 0
        self.yandex_disk = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
        self.url_download = None

    def remove_readonly(self, func, path_i, _):
        os.chmod(self.main_path, stat.S_IWRITE)
        func(path_i)

    def run(self):
        try:
            self.status_label.emit("Делаем запрос...")
            time.sleep(0.2)
            # get Json(where url to download) from yandex
            if self.delete:
                url = URL.urlopen(self.yandex_disk + urlencode(dict(public_key=self.checkedJson['url_mini_minecraft'])))
            else:
                url = URL.urlopen(self.yandex_disk + urlencode(dict(public_key=self.checkedJson['url_full_minecraft'])))
            start_download = time.time()
            # and put URL and File_size to Object
            self.url_download = URL.urlopen(json.loads(url.read().decode())['href'])
            self.file_size = int(self.url_download.info()['Content-Length'])
        except:
            self.status_label.emit("Ошибка запроса, возможна проблема с интернетом")
            self.file.close()
            time.sleep(2)
            widget.close()
        # Download
        file_size_dl = 0
        try:
            self.status_label.emit("Пошёл процесс загрузки")
            while True:
                buffer = self.url_download.read(1024)
                if not buffer:
                    break
                file_size_dl += len(buffer)
                self.file.write(buffer)
                self.progress_value.emit(int(file_size_dl * 100 / self.file_size))
                self.speed_label.emit(f"{(file_size_dl // (time.time() - start_download)) / 1024:.{2}f} Kb/s")
        except:
            self.status_label.emit("Ошибка загрузки файла, возможно нестабильное интернет соединение")
            self.file.close()
            time.sleep(2)
            widget.close()
        self.file.close()
        # Finish Download
        if self.delete:
            self.status_label.emit("Удаляем файлы из .minecraft и .tlauncher")
            # delete files in .minecraft
            delete_file(self.checkedJson['del_file_in_minecraft'], f"{self.main_path}\\.minecraft")
            delete_file(self.checkedJson['del_file_in_tlauncher'], f"{self.main_path}\\.tlauncher")
            for dir_in_minecraft in self.checkedJson['del_dir_in_minecraft']:
                try:
                    shutil.rmtree(f"{self.main_path}\\{dir_in_minecraft}",
                                  ignore_errors=False, onerror=self.remove_readonly)
                except:
                    continue
            self.status_label.emit("Удаление завершено успешно")
            time.sleep(0.2)
            self.status_label.emit("Распаковываем архив...")
            shutil.unpack_archive(f"{self.main_path}\\.minecraft\\client.zip", f"{self.main_path}\\.minecraft")
            os.remove(f"{self.main_path}\\.minecraft\\client.zip")
            # replace some file in tlauncher
            for file_in_tlauncher in self.checkedJson['del_file_in_tlauncher']:
                os.replace(f"{self.main_path}\\.minecraft\\{file_in_tlauncher}",
                           f"{self.main_path}\\.tlauncher\\{file_in_tlauncher}")
            self.status_label.emit("Всё готово. Сейчас запуститься TLauncher")
        else:
            self.status_label.emit("Распаковываем архив...")
            time.sleep(0.2)
            shutil.unpack_archive(f"{self.main_path}\\client.zip", self.main_path)
            os.remove(f"{self.main_path}\\client.zip")
            try:
                os.symlink(os.path.join('C:\\Users', os.getlogin(), 'AppData\\Roaming\\.minecraft\\TLauncher.exe'),
                           os.path.join('C:\\Users', os.getlogin(), 'Desktop\\TLauncher'))
            except:
                pass
        #start tlauncher
        self.status_label.emit("Всё готово. Сейчас запуститься TLauncher")
        subprocess.Popen(f"{self.main_path}\\.minecraft\\TLauncher.exe")
        time.sleep(2)
        widget.close()


class Load(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LoadWindow()
        self.ui.setupUi(self)
        self.main_path = os.path.join('C:\\Users', os.getlogin(), 'AppData\\Roaming')
        self.delete = True  # if True -> delete file in minecraft, else -> install full_minecraft
        self.checkedJson = None
        self.file = None
        self.thread = QThread()

    def set_progress_bar(self, val):
        self.ui.progressBar.setValue(val)

    def set_status_label(self, val):
        self.ui.label_4.setText(f"Статус: {val}")

    def set_speed_label(self, val):
        self.ui.label_3.setText(f"Скорость: {val}")

    def Download(self):
        self.ui.label_4.setText("Статус: Проверка наличия клиента...")
        time.sleep(0.2)
        try:
            self.file = open(f"{self.main_path}\\.minecraft\\client.zip", 'wb')
        except:
            self.file = open(f"{self.main_path}\\client.zip", 'wb')
            self.delete = False
        # run thread download
        self.worker = DownloadTread(main_path=self.main_path, delete=self.delete,
                                    file=self.file, checkedJson=self.checkedJson)  # create thread
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress_value.connect(self.set_progress_bar)
        self.worker.status_label.connect(self.set_status_label)
        self.worker.speed_label.connect(self.set_speed_label)
        self.thread.start()


class Start(QMainWindow):
    def __init__(self, load_object, parent=None):
        super().__init__(parent)
        self.ui = Ui_StartWindow()
        self.ui.setupUi(self)
        self.load_object = load_object
        self.checkedJson = None
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton.setStyleSheet("background: #505050;")
        self.ui.pushButton.clicked.connect(lambda: self.btn_clicked())
        try:
            # download JSON, get versions and urls, files
            # here put your URL to JSON file
            with URL.urlopen(
                    "https://raw.githubusercontent.com/BitLittel/MinecraftReborn/main/minecraft_download.json") as url:
                self.checkedJson = json.loads(url.read().decode())
                for version in self.checkedJson:
                    self.ui.comboBox.addItem(version)  # add item to comboBox
            self.ui.pushButton.setEnabled(True)  # enable button
            self.ui.pushButton.setStyleSheet("background: #00e317;")
        except:
            self.ui.label_2.setText("Произошла ошибка при скачивании конфиг.файла, проверте подключение к интернету")

    def btn_clicked(self):
        self.load_object.checkedJson = self.checkedJson[self.ui.comboBox.currentText()]
        widget.setCurrentIndex(1)  # set to Load()
        self.load_object.Download()


app = QApplication([])
widget = QStackedWidget()
load = Load()  # initialise Load()
start = Start(load_object=load)  # and initialise Start() and putt Load()
pm = QPixmap()  # set icon
pm.loadFromData(base64.b64decode(logo))
i = QIcon()
i.addPixmap(pm)
widget.setWindowIcon(QIcon(i))  # end icon
widget.setWindowTitle("L3Reborn-Installer")
# set window index
widget.addWidget(start)  # he have index 0
widget.addWidget(load)  # index 1
# start application
widget.show()
sys.exit(app.exec())
# pyinstaller --windowed --onefile --name Install-L3 --clean --icon L3.ico --key be73cc3ea4050e65 installer_v2.py
