from PyQt6.QtCore import QAbstractTableModel, QModelIndex, QRegularExpression, Qt
from PyQt6.QtGui import QAction, QIntValidator, QRegularExpressionValidator
from PyQt6.QtWidgets import QComboBox, QLineEdit, QMainWindow, QMdiArea, QMdiSubWindow, \
    QStyledItemDelegate, \
    QTableView, QToolBar, QVBoxLayout, QWidget

TABLES = 'students', 'classes', 'subjects', 'schedule'


def get_table(table_id):
    match table_id:
        case 'students':
            return [
                [1, 'Попов', 'Игорь', 'Юрьевич', 2],
                [2, 'Смирнов', 'Станислав', 'Викторович', None],
                [3, 'Денисов', 'Николай', 'Дмитриевич', None],
            ]
        case 'classes':
            return [
                [1, 8, 'А'],
                [2, 8, 'Б'],
                [3, 9, 'А']
            ]
        case 'subjects':
            return [
                [1, 'Русский язык'],
                [2, 'Литература'],
                [3, 'Математика'],
                [4, 'Информатика'],
                [5, 'Физика']
            ]


def get_header(table_id):
    match table_id:
        case 'students':
            return ['student_id', 'last_name', 'first_name', 'second_name', 'class']
        case 'classes':
            return ['class_id', 'class_number', 'class_letter', 'class']
        case 'subjects':
            return ['subject_id', 'subject']


class ComboDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(ComboDelegate, self).__init__(parent)
        self.parent = parent

    def createEditor(self, parent, option, index):
        self.combobox = QComboBox(parent)
        table = ''
        if index.model().title == 'students' and index.column() == 4:
            table = 'classes'

        items = sorted([(row[3], row[0])
                        for row in parent.window().tables[table]._data])

        for item in items:
            self.combobox.addItem(item[0], item[1])

        return self.combobox

    def setEditorData(self, editor, index):
        value = index.data()
        editor.setCurrentText(str(value))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.itemData(editor.currentIndex()), Qt.ItemDataRole.EditRole)


class Delegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(Delegate, self).__init__(parent)
        self.parent = parent

    def createEditor(self, parent, option, index):
        if index.model().title == 'classes':
            line_edit = QLineEdit(parent)
            if index.column() == 1:
                line_edit.setValidator(QIntValidator(1, 11))
                line_edit.setPlaceholderText('1 - 11')
            elif index.column() == 2:
                line_edit.setValidator(QRegularExpressionValidator(QRegularExpression('[А-Д]')))
                line_edit.setPlaceholderText('А - Д')
            return line_edit
        elif index.model().title != 'students':
            combobox = QComboBox(parent)
            items = sorted({str(index.siblingAtRow(row).data())
                            for row in range(index.model().rowCount())})

            combobox.addItems(items)
            return combobox
        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        value = index.data()
        if index.model().title == 'subjects':
            editor.setCurrentText(str(value))
        elif isinstance(editor, QLineEdit):
            editor.setText(str(value))


class TableModel(QAbstractTableModel):
    def __init__(self, parent, data, title):
        super().__init__()
        self.parent = parent
        self._data = data
        self.title = title
        self._rows_to_add = set()

    def data(self, index, role):
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            if (value := self._data[index.row()][index.column()]) \
                    and self.title == 'students' and index.column() == 4:
                classes = self.parent.window().tables['classes']._data
                if class_desc := [row[3] for row in classes if row[0] == value]:
                    return class_desc[0]
            return self._data[index.row()][index.column()]

    def rowCount(self, index=None):
        return len(self._data)

    def columnCount(self, index=None):
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return get_header(self.title)[section]
        return super().headerData(section, orientation, role)

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data[index.row()][index.column()] = value
            if self.title == 'classes':
                self._data[index.row()][3] = ''.join(map(str, self._data[index.row()][1:3]))
            return True
        return False

    def flags(self, index):
        if index.column() > 0:
            return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable
        return super().flags(index)

    def insertRows(self, position, rows, parent):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        cols = self.columnCount()
        for _ in range(rows):
            new_id = self._data[-1][0] + 1
            self._data.append([new_id] + ['' for _ in range(cols - 1)])
            self._rows_to_add.add(new_id)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        del self._data[position:position + rows - 1]
        self.endRemoveRows()
        return True

    def _add(self):
        index = self.parent.currentIndex()
        row = self.rowCount()
        self.insertRow(row, index)
        self.parent.selectRow(row)

    def _remove(self):
        indices = self.parent.selectedIndexes()
        if indices:
            for index in indices:
                row = index.row()
                del_id = self._data[row][0]
                if del_id in self._rows_to_add:
                    self._rows_to_add.discard(del_id)
                else:
                    pass
            self.removeRows(indices[0].row(), len(indices))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Students Database')
        self.tables = {}

        self.mdi = QMdiArea()
        self.toolbar = QToolBar('Main')

        for i in range(len(TABLES)):
            self._add_sub_window(TABLES[-i - 1])
            self._add_toolbar_action(TABLES[i])

        self.mdi.tileSubWindows()
        self.addToolBar(self.toolbar)
        self.setCentralWidget(self.mdi)

    def _add_sub_window(self, title):
        for sub_window in self.mdi.subWindowList():
            if sub_window.objectName() == title:
                sub_window.widget().show()
                sub_window.show()
                sub_window.setFocus()
                return

        self.mdi.addSubWindow(self._create_window(title))

    def _create_window(self, title):
        sub_window = QMdiSubWindow(self)
        sub_window.setObjectName(title)
        sub_window.setWindowTitle(title.capitalize())

        tableview = QTableView(self)

        data = get_table(title)
        if title == 'classes':
            data = [row + [''.join(map(str, row[1:3]))] for row in data]

        model = TableModel(tableview, data, title)
        self.tables[title] = model

        tableview.setModel(model)
        tableview.setAlternatingRowColors(True)
        tableview.setItemDelegate(Delegate(tableview))
        if title == 'students':
            tableview.setItemDelegateForColumn(4, ComboDelegate(tableview))
        elif title == 'classes':
            tableview.hideColumn(3)

        widget = QWidget(sub_window)
        layout = QVBoxLayout(widget)
        toolbar = QToolBar('Actions', tableview)
        add_action = QAction('Add', tableview)
        add_action.triggered.connect(model._add)
        del_action = QAction('Delete', tableview)
        del_action.triggered.connect(model._remove)
        toolbar.addActions((add_action, del_action))

        layout.addWidget(toolbar)
        layout.addWidget(tableview)

        sub_window.setWidget(widget)

        return sub_window

    def _add_toolbar_action(self, title):
        action = QAction(title, self)
        action.triggered.connect(lambda: self._add_sub_window(title))
        self.toolbar.addAction(action)
