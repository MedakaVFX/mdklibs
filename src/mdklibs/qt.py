""" mdklibs.data
 
* データ管理用モジュール

Info:
    * Created : 2024-11-10 Tatsuya YAMAGISHI
    * Coding : Python 3.12.4 & PySide6
    * Author : MedakaVFX <medaka.vfx@gmail.com>


Release Note:
    * LastUpdated : 2024-11-10 Tatsuya Yamagishi
"""

import dataclasses
import pprint

try:
    from PySide6 import QtCore, QtGui, QtWidgets
except:
    from qtpy import QtCore, QtGui, QtWidgets

import mdklibs as mdk
#=======================================#
# Settings
#=======================================#


#=======================================#
# Funcsions
#=======================================#
def create_menu(view, menu_name):
    _main_menu = view.menuBar()

    if _main_menu:
        _menu = get_menu_from_menubar(view.menuBar(), menu_name)

        if _menu:
            return _menu
        
        else:
            _menu = QtWidgets.QMenu(_main_menu)
            _menu.setTitle(menu_name)
            _main_menu.addAction(_menu.menuAction())

            return _menu
        

def get_hspacer():
    _hspacer = QtWidgets.QSpacerItem(
        40, 20, 
        QtWidgets.QSizePolicy.Expanding,
        QtWidgets.QSizePolicy.Minimum
    )
    
    return _hspacer


def get_menu_from_menubar(menubar, menu_name):
    """
    メニューバーからメニューを名前で取得
    """
    _menus = menubar.findChildren(QtWidgets.QMenu)
    for _menu in _menus:
        if _menu.title() == menu_name:
            return _menu
        
    return None


def get_qaction(name: str, parent: QtWidgets.QWidget):
    """ Qt5、Qt6 互換用関数
    
    * QActionのパッケージ場所が Qt5(PySide2) と Qt6(PySide6) で異なるため
    """
    try:
        return QtGui.QAction(name, parent)
    except:
        return QtWidgets.QAction(name, parent)


def get_vspacer():
    _vspacer = QtWidgets.QSpacerItem(
        40, 20, 
        QtWidgets.QSizePolicy.Minimum,
        QtWidgets.QSizePolicy.Expanding
    )
    
    return _vspacer



#=======================================#
# Class
#=======================================#
class Splitter(QtWidgets.QSplitter):
    """ Splitter 基底クラス """
    def __init__(self, parent=None):
        super().__init__(parent)


    def init_print_signal(self):
        self.splitterMoved.connect(self.print_sizes)


    def print_sizes(self):
        print(f'{self.objectName()} {self.sizes()}')

class HSplitter(Splitter):
    """ Vertical Splitter """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setOrientation(QtCore.Qt.Horizontal)


class VSplitter(Splitter):
    """ Horizontal Splitter """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setOrientation(QtCore.Qt.Vertical)


class ComboBox(QtWidgets.QComboBox):
    """ カスタムコンボボックス
    
    Signals:
        * activated(int index) : Only User
        * currentIndexChanged(int index) : Any
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
    # ----------------------------------
    # Methods
    # ----------------------------------
    def select(self, name: str):
        """ 名前でアイテムを選択 """
        num = self.findText(name)
        if num == -1:
            num = 0
            
        self.setCurrentIndex(num)


class ListWidget(QtWidgets.QListWidget):
    """ TyListWidget 基底クラス 
    
    Attributes:
        setSortingEnabled(bool)
    
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSortingEnabled(True)

    # ----------------------------------
    # Get
    # ----------------------------------
    def get_all_items(self):
        return [self.item(index) for index in range(self.count())]


    def get_name_list(self) -> list[str]:
        return [item.text() for item in self.get_all_items()]


    def get_selected_name_list(self) -> list[str]:
        return [item.text() for item in self.selectedItems()]
    
    
    # ----------------------------------
    # Set
    # ----------------------------------
    def set_editable(self):
        for _index in range(self.count()):
            _item = self.item(_index)
            _item.setFlags(_item.flags() | QtCore.Qt.ItemIsEditable)


    def set_multi_selection(self):
        self.setSelectionMode(
		        QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        

    # ----------------------------------
    # Methods
    # ----------------------------------
    def add_items(self, items: list[str]):
        _name_list = self.get_name_list()
        _name_list.extend(items)

        self.clear()
        self.addItems(sorted(list(set(_name_list))))


    def item_exists(self, value: str):
        if self.find_items(value):
            return True
        else:
            return False


    def find_items(self, value:str):
        """
        Reference form : https://doc.qt.io/qtforpython-5/PySide2/QtCore/Qt.html

        Qt.MatchExactly : Performs QVariant -based matching.
        Qt.MatchFixedString : Performs string-based matching. String-based comparisons are case-insensitive unless the MatchCaseSensitive flag is also specified.
        Qt.MatchContains : The search term is contained in the item.
        Qt.MatchStartsWith : The search term matches the start of the item.
        Qt.MatchEndsWith : The search term matches the end of the item.
        Qt.MatchCaseSensitive : The search is case sensitive.
        Qt.MatchRegExp : Performs string-based matching using a regular expression as the search term. Uses the deprecated QRegExp class. This enum value is deprecated since Qt 5.15.
        Qt.MatchRegularExpression : Performs string-based matching using a regular expression as the search term. Uses QRegularExpression . When using this flag, a QRegularExpression object can be passed as parameter and will directly be used to perform the search. The case sensitivity flag will be ignored as the QRegularExpression object is expected to be fully configured. This enum value was added in Qt 5.15.
        Qt.MatchWildcard : Performs string-based matching using a string with wildcards as the search term.
        Qt.MatchWrap : Perform a search that wraps around, so that when the search reaches the last item in the model, it begins again at the first item and continues until all items have been examined.
        Qt.MatchRecursive : Searches the entire hierarchy.
        """

        return self.findItems(value, QtCore.Qt.MatchCaseSensitive)
            

    def remove_selected(self):
        _items = self.selectedItems()

        if _items is None:
            return
        
        for _item in _items:
            self.takeItem(self.row(_item))


    def select(self, item_name):
        """ Select item by name. """
        # print(item_name)
        # raise RuntimeError(item_name)

        _items = (self.findItems(item_name, QtCore.Qt.MatchContains))           
        if _items:
            self.setCurrentItem(_items[0])



class TreeWidget(QtWidgets.QTreeWidget):
    """Class Description
 
    * カスタムTreeWidget

    Signals:
        * currentItemChanged
        * itemClicked
        * itemDoubleClicked
        *  itemPressed

    Examples:
        >>> self.setAlternatingRowColors(True)
        >>> self.setRootIsDecorated(False)
        >>> self.setSortingEnabled(True)
        >>> self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        >>> 
        >>> self.setColumnCount(len(TASK_HEADERS))
        >>> self.setHeaderLabels(list(TASK_HEADERS))
        >>> 
        >>> for i, key in enumerate(TASK_HEADERS):
        >>>     self.header().resizeSection(i, TASK_HEADERS.get(key))
        >>> setSelectionMode(
        >>>     QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)

    """
    def __init__(self, parent=None) -> None:

        super().__init__(parent)

        self._headers = None
        
    #---------------------------------#
    # Init
    #---------------------------------#
    #---------------------------------#
    # Setup
    #---------------------------------#
    #---------------------------------#
    # Get
    #---------------------------------#
    def get_all_items(self):
        # all_items = self.findItems(
        #         '*', QtCore.Qt.MatchWrap |QtCore.Qt.MatchWildcard | QtCore.Qt.MatchRecursive,)

        # return all_items
    
        """Returns all QTreeWidgetItems in the given QTreeWidget."""
    
        _all_items = []
        for _i in range(self.topLevelItemCount()):
            _top_item = self.topLevelItem(_i)
            _all_items.extend(self.get_subtree_items(_top_item))
        
        return _all_items
    

    def get_header_index(self, name: str):
        if self._headers:
            for _i, key in enumerate(self._headers):
                if key == name:
                    return _i
            return None
        else:
            return None
    

    def get_item(self, index, name, create=True):
        """ Item を名前で取得 """
        _items = self.get_all_items()
        _result = None

        for _item in _items:
            if _item.text(index) == name:
                _result = _item

        if _result is None and create:
            _result = QtWidgets.QTreeWidgetItem(self)
            _result.setText(0, name)

        return _result
               

    def get_subtree_items(self, tree_widget_item):
        """Returns all QTreeWidgetItems in the subtree rooted at the given node."""
    
        _items = []
        _items.append(tree_widget_item)
        for i in range(tree_widget_item.childCount()):
            _items.extend(self.get_subtree_items(tree_widget_item.child(i)))
        
        return _items


    def get_top_item(self, name):
        _num = self.topLevelItemCount()
        _result = None

        if _num:
            for i in range(_num):
                _item = self.topLevelItem(i)
                if _item.text(0) == name:
                    _result = _item
                    break
        
        return _result


    #---------------------------------#
    # Set
    #---------------------------------#
    def set_fixed_height(self, value: int):
        """ TreeWidgetItemの高さを固定
        
        """
        _delegate = FixedHeightDelegate(value)
        self.setItemDelegate(_delegate)


    def set_font(self, font: QtGui.QFont):
        self.setFont(font)


    def set_headers(self, headers: dict):
        """ 辞書型でヘッダーを設定

        headers = {
            'Type:': <header_width: int>,
        }

        """
        self._headers = headers

        self.setColumnCount(len(headers))
        self.setHeaderLabels(headers)

        for _i, _key in enumerate(headers):
            self.header().resizeSection(_i, headers.get(_key)) 


    def set_multi_selection(self):
        self.setSelectionMode(
                QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)


    #---------------------------------#
    # Methods
    #---------------------------------#
    def add_item(self, name: str, parent=None):
        if parent is None:
            _parent = self
        else:
            _parent = self.get_item(0, parent, create=True)


        _item = QtWidgets.QTreeWidgetItem(_parent)
        _item.setText(0, name)

        return _item


    def add_items(self, items: list):
        self.clear()

        if type(items) == list:
            for _item in items:
                _new_item = QtWidgets.QTreeWidgetItem(self)
                _new_item.setText(0, _item)


    def hide_header(self):
        self.header().hide()


    def remove_selected(self):
        _items = self.selectedItems()

        for _item in _items:
            _index = self.indexFromItem(_item)
            self.takeTopLevelItem(_index.row())


    def select(self, index, name):        
        _cur_item = self.get_item(index, name, create=False)

        if _cur_item:
            self.setCurrentItem(_cur_item)




class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

    
    def get_tab_text(self):
        _index = self.currentIndex()
        return self.tabText(_index)
    

    def select(self, name: str):
        for _i in range(self.count()):
            if self.tabText(_i).lower() == name.lower():
                self.setCurrentIndex(_i)


#=======================================#
# QtTools
#=======================================#
class DictEditWidget(TreeWidget):
    """ 辞書型データ編集用TreeWidget
 
    """
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.HEADERS = {'Key': 160, 'Value': 0}

        self.setSortingEnabled(True)
        self.setAlternatingRowColors(False)
        self.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.setRootIsDecorated(False)

        self.setColumnCount(len(self.HEADERS))
        
        self.set_headers(self.HEADERS)


    #---------------------------------#
    # Init Context Menu
    #---------------------------------#
    def init_context_menu(self):
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._setup_context_menu)


    def _setup_context_menu(self, point):
        _menu = QtWidgets.QMenu(self)

        _action = QtGui.QAction('Add new', self)
        _action.triggered.connect(self._on_add_new)
        _menu.addAction(_action)

        _menu.exec_(self.mapToGlobal(point))

    
    #---------------------------------#
    # Methods
    #---------------------------------#
    def _on_add_new(self):
        self.add_item('key', 'value')

    #---------------------------------#
    # Get
    #---------------------------------#
    def get_value(self):
        return {item.text(0): item.text(1) for item in self.get_all_items()}


    #---------------------------------#
    # Set
    #---------------------------------#
    def set_value(self, data: dict):
        self.clear()

        if type(data) == dict:

            for key, value in data.items():
                self.add_item(key, value)

        else:
            _message = 'MDK | "data" type is not dict.'
            print(_message)
            print(data)


    #---------------------------------#
    # Method
    #---------------------------------#
    def add_item(self, key: str, value: str):
        item = QtWidgets.QTreeWidgetItem(self)
        item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)

        item.setText(0, str(key))
        if value is not None:
            item.setText(1, str(value))




if __name__ == '__main__':
    pass
