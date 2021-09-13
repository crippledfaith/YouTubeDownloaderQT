from downloadManger import Download_Manger
from PySide6 import QtWidgets
import ctypes,os,sys
from mainWindowUI import Ui_MainWindow


def main():
    if __name__ == "__main__":
        myappid = u'mycompany.myproduct.subproduct.version_1' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        Download_Manger(ui)
        MainWindow.show()
        sys.exit(app.exec())

main()