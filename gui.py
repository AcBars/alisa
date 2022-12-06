from PyQt6.QtCore import QAbstractTableModel, QModelIndex, QRegularExpression, Qt
from PyQt6.QtGui import QAction, QIntValidator, QRegularExpressionValidator
from PyQt6.QtWidgets import QComboBox, QLineEdit, QMainWindow, QMdiArea, QMdiSubWindow, \
    QMessageBox, QStyledItemDelegate, \
    QTableView, QToolBar, QVBoxLayout, QWidget

import db_app

TABLES = 'students', 'classes', 'subjects', 'schedule', 'week'

HEADERS = {
    'students': ['id', 'first_name', 'last_name', 'id_class'],
    'classes': ['id', 'level', 'symbol', 'class'],
    'subjects': ['id', 'subject'],
    'schedule': ['id', 'id_week', 'time_start', 'id_class', 'id_subject'],
    'week': ['id', 'name', 'short_name']
}

ID_DESCRIPTIONS = {
    'classes': (3, 0),
    'week': (2, 0),
    'subjects': (1, 0)
}

FK_MAP = {
    'id_class': 'classes',
    'id_week': 'week',
    'id_subject': 'subjects'
}


def get_table(table_id):
    match table_id:
        case 'students':
            return [
                [1, 'Игорь', 'Попов', 2],
                [2, 'Станислав', 'Смирнов', None],
                [3, 'Николай', 'Денисов', None],
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
        case 'schedule':
            return [
                [1, 1, '10:00', 2, 2],
                [2, 1, '19:00', 2, 1],
                [3, 4, '12:00', 1, 3]
            ]
        case 'week':
            return [
                [1, 'понедельник', 'пн'],
                [2, 'вторник', 'вт'],
                [3, 'среда', 'ср'],
                [4, 'четверг', 'чт'],
                [5, 'пятница', 'пт'],
                [6, 'суббота', 'сб'],
                [7, 'воскресенье', 'вс']
            ]


def get_table_from_db(table_id):
    return db_app.read(table_id)


def show_message(message_text):
    msg = QMessageBox()
    msg.setWindowTitle('SQL Query Result')
    msg.setText(message_text)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.exec()


def db_insert(title, table_row, header):
    return db_app.crud('insert', title,
                       {col_title: table_row[col]
                        for col, col_title in enumerate(header)})


def db_update(title, table_row, header, col):
    return db_app.crud('update', title,
                       {'id': table_row[0], header[col]: table_row[col]})


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

        # data = get_table(title)
        data = [list(row) for row in get_table_from_db(title)]
        if title == 'classes':
            data = [row + [''.join(map(str, row[1:3]))] for row in data]

        model = TableModel(tableview, data, title)
        self.tables[title] = model

        tableview.setModel(model)
        tableview.setAlternatingRowColors(True)
        tableview.setItemDelegate(Delegate(tableview))

        header = HEADERS.get(title, [])
        for col, col_title in enumerate(header[1:], start=1):
            if col_title.startswith('id'):
                tableview.setItemDelegateForColumn(col, ComboDelegate(tableview))

        if title == 'classes':
            tableview.hideColumn(3)

        # tableview.resizeColumnsToContents()

        widget = QWidget(sub_window)
        layout = QVBoxLayout(widget)
        toolbar = QToolBar('Actions', tableview)
        add_action = QAction('Add', tableview)
        add_action.triggered.connect(model._add)
        del_action = QAction('Delete', tableview)
        del_action.triggered.connect(model._remove)
        submit_action = QAction('Submit', tableview)
        submit_action.triggered.connect(model._submit)
        toolbar.addActions((add_action, del_action, submit_action))

        layout.addWidget(toolbar)
        layout.addWidget(tableview)

        sub_window.setWidget(widget)
        if title == 'week':
            sub_window.hide()

        return sub_window

    def _add_toolbar_action(self, title):
        if title == 'week':
            return
        action = QAction(title.capitalize(), self)
        action.triggered.connect(lambda: self._add_sub_window(title))
        self.toolbar.addAction(action)


class TableModel(QAbstractTableModel):
    def __init__(self, parent, data, title):
        super().__init__()
        self.parent = parent
        self._data = data
        self.title = title
        self._rows_to_add = set()

    def data(self, index, role):
        if role not in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole):
            return
        row = index.row()
        col = index.column()

        if (value := self._data[row][col]) and col > 0:
            tables = self.parent.window().tables
            table_id = self.title
            header = HEADERS.get(table_id, [])
            fk_table = FK_MAP.get(header[col], '')
            if header[col].startswith('id') and fk_table in tables:
                id_desc = ID_DESCRIPTIONS.get(fk_table, (0, 0))
                if found_value := [row[id_desc[0]]
                                   for row in tables[fk_table]._data
                                   if row[id_desc[1]] == value]:
                    return found_value[0]

        return self._data[row][col]

    def rowCount(self, index=None):
        return len(self._data)

    def columnCount(self, index=None):
        return len(self._data[0])

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole \
                and orientation == Qt.Orientation.Horizontal:
            return HEADERS.get(self.title, [])[section]
        return super().headerData(section, orientation, role)

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            row = index.row()
            col = index.column()
            table_id = index.model().title
            header = HEADERS.get(table_id, [])

            self._data[row][col] = int(value) \
                if header[col].startswith('id') or header[col] == 'level' \
                else value
            if self.title == 'classes':
                self._data[row][3] = ''.join(map(str, self._data[row][1:3]))

            return db_update(self.title, self._data[row], header, col)
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
        if not (indices := self.parent.selectedIndexes()):
            return
        deleted = set()
        for index in indices:
            row = index.row()
            del_id = self._data[row][0]
            if del_id in self._rows_to_add:
                self._rows_to_add.discard(del_id)
                result = True
            else:
                result = db_app.crud('delete', self.title,
                                     {'id': del_id})
                if result:
                    deleted.add(del_id)
                else:
                    break

        if result:
            self.removeRows(indices[0].row(), len(indices))
            txt = f'Successfully deleted rows with ids:' \
                  f' {", ".join(map(str, deleted))}.'
        else:
            txt = f'Error deleting rows with ids:' \
                  f' {", ".join(map(str, set(indices).difference(deleted)))}.'

        show_message(txt)

    def _submit(self):
        header = HEADERS.get(self.title, [])
        if self.title == 'classes':
            header = header[:-1]
        rows_to_add = self._rows_to_add.copy()
        for add_id in rows_to_add:
            if rows := [row for row in self._data if row[0] == add_id]:
                table_row = rows[0]
                if db_insert(self.title, table_row, header):
                    self._rows_to_add.discard(add_id)
        rows_to_add.difference(self._rows_to_add)

        txt = f'Successfully added rows with ids: {", ".join(map(str, rows_to_add.difference(self._rows_to_add)))}.'
        if self._rows_to_add:
            txt += f'\nComplete all fields in the rows with ids: {", ".join(map(str, self._rows_to_add))}.'
        show_message(txt)


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

        if index.model().title == 'schedule' and index.column() == 2:
            line_edit = QLineEdit(parent)
            line_edit.setValidator(QRegularExpressionValidator(QRegularExpression('([01][0-9]|2[0-3]):[0-5][0-9]')))
            line_edit.setPlaceholderText('10:00')
            return line_edit

        return super().createEditor(parent, option, index)

    def setEditorData(self, editor, index):
        value = index.data()
        if isinstance(editor, QLineEdit):
            editor.setText(str(value))


class ComboDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(ComboDelegate, self).__init__(parent)
        self.parent = parent

    def createEditor(self, parent, option, index):
        self.combobox = QComboBox(parent)
        tables = parent.window().tables
        table_id = index.model().title
        header = HEADERS.get(table_id, [])
        items = []
        col = index.column()
        if col > 0:
            if fk_table := FK_MAP.get(header[col], ''):
                id_desc = ID_DESCRIPTIONS.get(fk_table, (0, 0))
                items = [(row[id_desc[0]], row[id_desc[1]]) for row in tables[fk_table]._data]
                if fk_table != 'week':
                    items.sort()

        for item in items:
            self.combobox.addItem(item[0], item[1])

        return self.combobox

    def setEditorData(self, editor, index):
        value = index.data()
        editor.setCurrentText(str(value))

    def setModelData(self, editor, model, index):
        table_id = model.title
        header = HEADERS.get(table_id, [])
        model.setData(index, editor.itemData(editor.currentIndex()), Qt.ItemDataRole.EditRole)
        db_update(table_id, model._data[index.row()], header, index.column())
