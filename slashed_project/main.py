from PyQt6.QtWidgets import QApplication
from launcher import Launcher

def main():
    app = QApplication([])
    ex = Launcher()
    ex.show()
    app.exec()

if __name__ == '__main__':
    main()