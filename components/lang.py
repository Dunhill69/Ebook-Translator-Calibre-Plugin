from calibre.utils.filenames import ascii_text
from calibre.utils.localization import get_lang, lang_as_iso639_1


try:
    from qt.core import pyqtSignal, pyqtSlot, QComboBox
except ImportError:
    from PyQt5.Qt import pyqtSignal, pyqtSlot, QComboBox

load_translations()


class SourceLang(QComboBox):
    refresh = pyqtSignal(dict, bool)

    def __init__(self, parent=None, book_lang=None):
        QComboBox.__init__(self, parent)
        self.book_lang = book_lang
        self.refresh.connect(self.set_codes)

    @pyqtSlot(dict, bool)
    def set_codes(self, codes, auto_detect=True):
        current = self.currentText()
        self.clear()
        self.book_lang = lang_as_iso639_1(self.book_lang)
        for lang in sorted(codes, key=ascii_text):
            code = codes.get(lang).lower()
            if self.book_lang is not None and code.startswith(self.book_lang):
                self.insertItem(0, lang)
            else:
                self.addItem(lang)
        if auto_detect:
            self.insertItem(0, _('Auto detect'))
        if current and current in codes:
            self.setCurrentText(current)
        else:
            self.setCurrentIndex(0)


class TargetLang(QComboBox):
    refresh = pyqtSignal(dict)

    def __init__(self, parent=None):
        QComboBox.__init__(self, parent)
        self.refresh.connect(self.set_codes)

    @pyqtSlot(dict)
    def set_codes(self, codes):
        default = self.itemText(0)
        current = self.currentText()
        self.clear()
        recommend, rest = [], []
        ui_lang = get_lang().lower()
        for lang in codes:
            code = codes.get(lang).replace('-', '_').lower()
            if code.startswith(lang_as_iso639_1(ui_lang)):
                recommend.append(lang)
            else:
                rest.append(lang)
            if code == ui_lang and current == default:
                current = lang
        langs = sorted(recommend, key=ascii_text)
        langs += sorted(rest, key=ascii_text)
        for lang in langs:
            self.addItem(lang)
        if current and current in codes:
            self.setCurrentText(current)
        else:
            self.setCurrentIndex(0)
