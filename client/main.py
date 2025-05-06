import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QLineEdit, QMessageBox, QHBoxLayout, QFormLayout
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt

API_URL = "http://localhost:8000"


class StyledWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                font-family: 'Arial';
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton#danger {
                background-color: #f44336;
            }
            QPushButton#danger:hover {
                background-color: #d32f2f;
            }
        """)


class LoginWindow(StyledWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VIP Banking - Вход")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)

        title = QLabel("VIP Banking")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        form = QFormLayout()
        form.setSpacing(15)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.Password)

        form.addRow("Логин:", self.username_input)
        form.addRow("Пароль:", self.password_input)

        self.login_button = QPushButton("Войти")
        self.login_button.clicked.connect(self.login)

        layout.addWidget(title)
        layout.addLayout(form)
        layout.addWidget(self.login_button)
        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля")
            return

        try:
            response = requests.post(
                f"{API_URL}/login",
                json={"username": username, "password": password},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            self.hide()
            self.main_window = MainWindow(
                user_id=data["user_id"],
                is_admin=data["is_admin"],
                username=username
            )
            self.main_window.show()

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self,
                "Ошибка входа",
                f"Не удалось войти в систему: {str(e)}"
            )


class MainWindow(StyledWindow):
    def __init__(self, user_id, is_admin, username):
        super().__init__()
        self.user_id = user_id
        self.is_admin = is_admin
        self.username = username
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(f"VIP Banking - {self.username}")
        self.setMinimumSize(600, 400)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(25)

        # Header
        header = QHBoxLayout()
        self.welcome_label = QLabel(f"Добро пожаловать, {self.username}!")
        self.welcome_label.setFont(QFont("Arial", 16, QFont.Bold))

        logout_btn = QPushButton("Выйти")
        logout_btn.setObjectName("danger")
        logout_btn.clicked.connect(self.logout)

        header.addWidget(self.welcome_label)
        header.addStretch()
        header.addWidget(logout_btn)

        # Balance section
        balance_box = QWidget()
        balance_box.setStyleSheet("background: white; border-radius: 8px; padding: 20px;")
        balance_layout = QVBoxLayout(balance_box)

        self.balance_label = QLabel("Загрузка баланса...")
        self.balance_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.balance_label.setAlignment(Qt.AlignCenter)

        btn_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.clicked.connect(self.load_balance)

        self.withdraw_button = QPushButton("Списать 100₽")
        self.withdraw_button.clicked.connect(self.withdraw)

        btn_layout.addWidget(self.refresh_button)
        btn_layout.addWidget(self.withdraw_button)

        balance_layout.addWidget(self.balance_label)
        balance_layout.addLayout(btn_layout)

        main_layout.addLayout(header)
        main_layout.addWidget(balance_box)
        main_layout.addStretch()

        if self.is_admin:
            admin_btn = QPushButton("Администрирование")
            admin_btn.setStyleSheet("background: #2196F3;")
            admin_btn.clicked.connect(self.open_admin_panel)
            main_layout.addWidget(admin_btn)

        self.setLayout(main_layout)
        self.load_balance()

    def load_balance(self):
        self.refresh_button.setEnabled(False)
        try:
            response = requests.get(
                f"{API_URL}/balance/{self.user_id}",
                timeout=5
            )
            response.raise_for_status()
            balance = response.json()["balance"]
            self.balance_label.setText(f"{balance:.2f}₽")

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось загрузить баланс: {str(e)}"
            )
        finally:
            self.refresh_button.setEnabled(True)

    def open_admin_panel(self):
        self.admin_panel = AdminPanel()
        self.admin_panel.show()

    def withdraw(self):
        confirm = QMessageBox.question(
            self,
            "Подтверждение",
            "Вы уверены, что хотите списать 100₽?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        try:
            response = requests.post(
                f"{API_URL}/transfer",
                json={"user_id": self.user_id, "amount": 100},
                timeout=5
            )
            response.raise_for_status()
            self.load_balance()
            QMessageBox.information(
                self,
                "Успешно",
                "Списание 100₽ выполнено успешно"
            )
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Ошибка при списании: {str(e)}"
            )

    def logout(self):
        self.close()
        login_window = LoginWindow()
        login_window.show()


class AdminPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Панель администратора")
        self.setMinimumSize(500, 400)
        self.setStyleSheet("background: #fff; padding: 20px;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title = QLabel("Управление пользователями")
        self.title.setFont(QFont("Arial", 18, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)

        self.user_list = QLabel("Загрузка пользователей...")
        self.user_list.setAlignment(Qt.AlignTop)
        self.user_list.setWordWrap(True)

        self.refresh_btn = QPushButton("Обновить список")
        self.refresh_btn.clicked.connect(self.load_users)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.refresh_btn)
        self.layout.addWidget(self.user_list)

        self.load_users()

    def load_users(self):
        try:
            response = requests.get(f"{API_URL}/admin/users")
            response.raise_for_status()
            users = response.json()
            user_text = ""
            for u in users:
                user_text += f"👤 ID: {u['id']} | Логин: {u['username']} | Баланс: {u['balance']:.2f}₽\n"
            self.user_list.setText(user_text or "Нет пользователей")
        except Exception as e:
            self.user_list.setText(f"Ошибка: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = LoginWindow()
    window.show()

    sys.exit(app.exec())