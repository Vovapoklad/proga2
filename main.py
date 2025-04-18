import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                            QTableWidgetItem, QVBoxLayout, QWidget, 
                            QComboBox, QLabel, QHBoxLayout, QHeaderView,
                            QMessageBox)  # Добавлен QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QColor, QBrush

class ProductInventoryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TechStore Manager - JSON Edition")
        self.setMinimumSize(1024, 768)
        
        # Инициализация данных
        self.json_file = "products.json"
        self.products = self.load_or_initialize_data()
        
        # Создание интерфейса
        self.init_ui()
        self.load_data()
    
    def load_or_initialize_data(self):
        """Загрузка данных из JSON или инициализация тестовыми данными"""
        default_data = [
            {
                "id": 1,
                "name": "Ноутбук ASUS",
                "description": "15.6 дюймов, 8GB RAM",
                "manufacturer": "ASUS",
                "price": 45000,
                "discount": 10,
                "stock": 5,
                "image": ""
            },
            {
                "id": 2,
                "name": "Смартфон Samsung",
                "description": "6.2 дюйма, 128GB",
                "manufacturer": "Samsung",
                "price": 32000,
                "discount": 5,
                "stock": 8,
                "image": ""
            },
            {
                "id": 3,
                "name": "Наушники Sony",
                "description": "Беспроводные",
                "manufacturer": "Sony",
                "price": 12000,
                "discount": 25,  # Скидка более 20% для теста подсветки
                "stock": 12,
                "image": ""
            },
            {
                "id": 4,
                "name": "Монитор LG",
                "description": "27 дюймов, 4K",
                "manufacturer": "LG",
                "price": 28000,
                "discount": 0,
                "stock": 3,
                "image": ""
            },
            {
                "id": 5,
                "name": "Клавиатура Logitech",
                "description": "Механическая",
                "manufacturer": "Logitech",
                "price": 7000,
                "discount": 15,
                "stock": 20,
                "image": ""
            }
        ]
        
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default_data
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")
            return default_data
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Фильтры и сортировка
        filter_panel = QHBoxLayout()
        
        self.discount_filter = QComboBox()
        self.discount_filter.addItems(["Все диапазоны", "0-15,99%", "15-20,99%", "20% и более"])
        self.discount_filter.currentIndexChanged.connect(self.load_data)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Без сортировки", "Цена по возрастанию", "Цена по убыванию"])
        self.sort_combo.currentIndexChanged.connect(self.load_data)
        
        filter_panel.addWidget(QLabel("Фильтр по скидке:"))
        filter_panel.addWidget(self.discount_filter)
        filter_panel.addWidget(QLabel("Сортировка:"))
        filter_panel.addWidget(self.sort_combo)
        
        # Таблица товаров
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Изображение", "Наименование", "Описание", 
            "Цена", "Скидка", "Остаток", "Производитель"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(100)
        
        # Статусная строка
        self.status_label = QLabel()
        self.status_label.setAlignment(Qt.AlignRight)
        
        # Компоновка
        layout.addLayout(filter_panel)
        layout.addWidget(self.table)
        layout.addWidget(self.status_label)
    
    def load_data(self):
        """Загрузка данных в таблицу с учетом фильтров и сортировки"""
        filtered_products = self.apply_filters()
        sorted_products = self.apply_sorting(filtered_products)
        
        self.table.setRowCount(len(sorted_products))
        
        for row, product in enumerate(sorted_products):
            # Изображение (заглушка)
            img_item = QTableWidgetItem()
            pixmap = QPixmap()
            pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            img_item.setData(Qt.DecorationRole, pixmap)
            self.table.setItem(row, 0, img_item)
            
            # Наименование
            self.table.setItem(row, 1, QTableWidgetItem(product["name"]))
            
            # Описание
            desc_item = QTableWidgetItem(product.get("description", ""))
            desc_item.setToolTip(product.get("description", ""))
            self.table.setItem(row, 2, desc_item)
            
            # Цена
            price = product["price"]
            discount = product.get("discount", 0)
            price_item = QTableWidgetItem()
            
            if discount > 0:
                final_price = price * (1 - discount / 100)
                price_item.setText(f"{price:.2f} → {final_price:.2f} руб.")
            else:
                price_item.setText(f"{price:.2f} руб.")
                
            self.table.setItem(row, 3, price_item)
            
            # Скидка
            self.table.setItem(row, 4, QTableWidgetItem(f"{discount}%"))
            
            # Остаток
            self.table.setItem(row, 5, QTableWidgetItem(str(product.get("stock", 0))))
            
            # Производитель
            self.table.setItem(row, 6, QTableWidgetItem(product.get("manufacturer", "")))
            
            # Подсветка для товаров со скидкой >20% (цвет #7ffd00)
            if discount > 20:
                highlight_color = QColor("#7ffd00")
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item:
                        item.setBackground(QBrush(highlight_color))
        
        self.status_label.setText(f"Показано: {len(sorted_products)} из {len(self.products)} товаров")
    
    def apply_filters(self):
        """Применение фильтров по скидке"""
        filter_index = self.discount_filter.currentIndex()
        
        if filter_index == 0:  # Все диапазоны
            return self.products.copy()
        elif filter_index == 1:  # 0-15,99%
            return [p for p in self.products if 0 <= p.get("discount", 0) <= 15.99]
        elif filter_index == 2:  # 15-20,99%
            return [p for p in self.products if 15 <= p.get("discount", 0) <= 20.99]
        else:  # 20% и более
            return [p for p in self.products if p.get("discount", 0) > 20]
    
    def apply_sorting(self, products):
        """Применение сортировки"""
        sort_index = self.sort_combo.currentIndex()
        
        if sort_index == 1:  # Цена по возрастанию
            return sorted(products, key=lambda x: x["price"])
        elif sort_index == 2:  # Цена по убыванию
            return sorted(products, key=lambda x: x["price"], reverse=True)
        else:  # Без сортировки
            return products

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductInventoryApp()
    window.show()
    sys.exit(app.exec_())