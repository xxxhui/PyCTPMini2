# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\CTP\PyCTP\PyCTP_Client\PyCTP_ClientUI\QOrderWidget.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1425, 326)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setMargin(5)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.container_order = QtGui.QWidget(Form)
        self.container_order.setObjectName(_fromUtf8("container_order"))
        self.horizontalLayout_container_order = QtGui.QHBoxLayout(self.container_order)
        self.horizontalLayout_container_order.setMargin(5)
        self.horizontalLayout_container_order.setSpacing(5)
        self.horizontalLayout_container_order.setObjectName(_fromUtf8("horizontalLayout_container_order"))
        self.tableWidget_all_orders = QtGui.QTableWidget(self.container_order)
        self.tableWidget_all_orders.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidget_all_orders.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidget_all_orders.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget_all_orders.setGridStyle(QtCore.Qt.DashDotDotLine)
        self.tableWidget_all_orders.setObjectName(_fromUtf8("tableWidget_all_orders"))
        self.tableWidget_all_orders.setColumnCount(16)
        self.tableWidget_all_orders.setRowCount(3)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setHorizontalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 8, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 9, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 10, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 13, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_all_orders.setItem(0, 14, item)
        self.tableWidget_all_orders.verticalHeader().setVisible(False)
        self.horizontalLayout_container_order.addWidget(self.tableWidget_all_orders)
        self.groupBox_order_insert = QtGui.QGroupBox(self.container_order)
        self.groupBox_order_insert.setAutoFillBackground(False)
        self.groupBox_order_insert.setObjectName(_fromUtf8("groupBox_order_insert"))
        self.label_buyorsell = QtGui.QLabel(self.groupBox_order_insert)
        self.label_buyorsell.setGeometry(QtCore.QRect(8, 69, 30, 16))
        self.label_buyorsell.setObjectName(_fromUtf8("label_buyorsell"))
        self.lineEdit_heyue = QtGui.QLineEdit(self.groupBox_order_insert)
        self.lineEdit_heyue.setGeometry(QtCore.QRect(70, 21, 117, 40))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_heyue.sizePolicy().hasHeightForWidth())
        self.lineEdit_heyue.setSizePolicy(sizePolicy)
        self.lineEdit_heyue.setObjectName(_fromUtf8("lineEdit_heyue"))
        self.label_heyue = QtGui.QLabel(self.groupBox_order_insert)
        self.label_heyue.setGeometry(QtCore.QRect(8, 32, 30, 16))
        self.label_heyue.setObjectName(_fromUtf8("label_heyue"))
        self.radioButton_kaicang = QtGui.QRadioButton(self.groupBox_order_insert)
        self.radioButton_kaicang.setGeometry(QtCore.QRect(70, 93, 57, 19))
        self.radioButton_kaicang.setObjectName(_fromUtf8("radioButton_kaicang"))
        self.buttonGroup_kaiping = QtGui.QButtonGroup(Form)
        self.buttonGroup_kaiping.setObjectName(_fromUtf8("buttonGroup_kaiping"))
        self.buttonGroup_kaiping.addButton(self.radioButton_kaicang)
        self.radioButton_maichu = QtGui.QRadioButton(self.groupBox_order_insert)
        self.radioButton_maichu.setGeometry(QtCore.QRect(130, 69, 57, 19))
        self.radioButton_maichu.setObjectName(_fromUtf8("radioButton_maichu"))
        self.buttonGroup_buysell = QtGui.QButtonGroup(Form)
        self.buttonGroup_buysell.setObjectName(_fromUtf8("buttonGroup_buysell"))
        self.buttonGroup_buysell.addButton(self.radioButton_maichu)
        self.label_kaiping = QtGui.QLabel(self.groupBox_order_insert)
        self.label_kaiping.setGeometry(QtCore.QRect(8, 93, 30, 16))
        self.label_kaiping.setObjectName(_fromUtf8("label_kaiping"))
        self.label_shoushu = QtGui.QLabel(self.groupBox_order_insert)
        self.label_shoushu.setGeometry(QtCore.QRect(8, 117, 30, 16))
        self.label_shoushu.setObjectName(_fromUtf8("label_shoushu"))
        self.radioButton_pingcang = QtGui.QRadioButton(self.groupBox_order_insert)
        self.radioButton_pingcang.setGeometry(QtCore.QRect(130, 93, 57, 19))
        self.radioButton_pingcang.setObjectName(_fromUtf8("radioButton_pingcang"))
        self.buttonGroup_kaiping.addButton(self.radioButton_pingcang)
        self.spinBox_shoushu = QtGui.QSpinBox(self.groupBox_order_insert)
        self.spinBox_shoushu.setGeometry(QtCore.QRect(70, 117, 42, 21))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_shoushu.sizePolicy().hasHeightForWidth())
        self.spinBox_shoushu.setSizePolicy(sizePolicy)
        self.spinBox_shoushu.setObjectName(_fromUtf8("spinBox_shoushu"))
        self.radioButton_pingjin = QtGui.QRadioButton(self.groupBox_order_insert)
        self.radioButton_pingjin.setGeometry(QtCore.QRect(192, 93, 57, 19))
        self.radioButton_pingjin.setObjectName(_fromUtf8("radioButton_pingjin"))
        self.buttonGroup_kaiping.addButton(self.radioButton_pingjin)
        self.radioButton_mairu = QtGui.QRadioButton(self.groupBox_order_insert)
        self.radioButton_mairu.setGeometry(QtCore.QRect(70, 69, 57, 19))
        self.radioButton_mairu.setObjectName(_fromUtf8("radioButton_mairu"))
        self.buttonGroup_buysell.addButton(self.radioButton_mairu)
        self.doubleSpinBox_xiadanjiage = QtGui.QDoubleSpinBox(self.groupBox_order_insert)
        self.doubleSpinBox_xiadanjiage.setGeometry(QtCore.QRect(70, 157, 90, 21))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_xiadanjiage.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_xiadanjiage.setSizePolicy(sizePolicy)
        self.doubleSpinBox_xiadanjiage.setMaximum(99999.0)
        self.doubleSpinBox_xiadanjiage.setProperty("value", 12345.67)
        self.doubleSpinBox_xiadanjiage.setObjectName(_fromUtf8("doubleSpinBox_xiadanjiage"))
        self.label_xiadanjiage = QtGui.QLabel(self.groupBox_order_insert)
        self.label_xiadanjiage.setGeometry(QtCore.QRect(8, 157, 30, 16))
        self.label_xiadanjiage.setObjectName(_fromUtf8("label_xiadanjiage"))
        self.pushButton_xiadantiaocang = QtGui.QPushButton(self.groupBox_order_insert)
        self.pushButton_xiadantiaocang.setGeometry(QtCore.QRect(192, 251, 93, 28))
        self.pushButton_xiadantiaocang.setObjectName(_fromUtf8("pushButton_xiadantiaocang"))
        self.pushButton_xiandan = QtGui.QPushButton(self.groupBox_order_insert)
        self.pushButton_xiandan.setGeometry(QtCore.QRect(8, 218, 181, 61))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_xiandan.sizePolicy().hasHeightForWidth())
        self.pushButton_xiandan.setSizePolicy(sizePolicy)
        self.pushButton_xiandan.setObjectName(_fromUtf8("pushButton_xiandan"))
        self.pushButton_xiadanquxiao = QtGui.QPushButton(self.groupBox_order_insert)
        self.pushButton_xiadanquxiao.setGeometry(QtCore.QRect(192, 218, 93, 28))
        self.pushButton_xiadanquxiao.setObjectName(_fromUtf8("pushButton_xiadanquxiao"))
        self.label_pankouguadansell = QtGui.QLabel(self.groupBox_order_insert)
        self.label_pankouguadansell.setGeometry(QtCore.QRect(192, 157, 95, 16))
        self.label_pankouguadansell.setObjectName(_fromUtf8("label_pankouguadansell"))
        self.label_dietingjia = QtGui.QLabel(self.groupBox_order_insert)
        self.label_dietingjia.setGeometry(QtCore.QRect(192, 178, 55, 16))
        self.label_dietingjia.setObjectName(_fromUtf8("label_dietingjia"))
        self.label_zuidashoushu = QtGui.QLabel(self.groupBox_order_insert)
        self.label_zuidashoushu.setGeometry(QtCore.QRect(192, 117, 23, 16))
        self.label_zuidashoushu.setObjectName(_fromUtf8("label_zuidashoushu"))
        self.label_zhangtingjia = QtGui.QLabel(self.groupBox_order_insert)
        self.label_zhangtingjia.setGeometry(QtCore.QRect(192, 137, 55, 16))
        self.label_zhangtingjia.setObjectName(_fromUtf8("label_zhangtingjia"))
        self.label_pankouguadanbuy = QtGui.QLabel(self.groupBox_order_insert)
        self.label_pankouguadanbuy.setGeometry(QtCore.QRect(192, 198, 103, 16))
        self.label_pankouguadanbuy.setObjectName(_fromUtf8("label_pankouguadanbuy"))
        self.checkBox_taoli = QtGui.QCheckBox(self.groupBox_order_insert)
        self.checkBox_taoli.setGeometry(QtCore.QRect(192, 21, 57, 19))
        self.checkBox_taoli.setObjectName(_fromUtf8("checkBox_taoli"))
        self.checkBox_baozhi = QtGui.QCheckBox(self.groupBox_order_insert)
        self.checkBox_baozhi.setGeometry(QtCore.QRect(192, 45, 57, 19))
        self.checkBox_baozhi.setObjectName(_fromUtf8("checkBox_baozhi"))
        self.horizontalLayout_container_order.addWidget(self.groupBox_order_insert)
        self.horizontalLayout_container_order.setStretch(0, 14)
        self.horizontalLayout_container_order.setStretch(1, 6)
        self.verticalLayout.addWidget(self.container_order)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(0)
        item.setText(_translate("Form", "期货账号", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(1)
        item.setText(_translate("Form", "策略编号", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(2)
        item.setText(_translate("Form", "合约", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(3)
        item.setText(_translate("Form", "买卖", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(4)
        item.setText(_translate("Form", "开平", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(5)
        item.setText(_translate("Form", "挂单状态", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(6)
        item.setText(_translate("Form", "报单价格", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(7)
        item.setText(_translate("Form", "报单手数", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(8)
        item.setText(_translate("Form", "未成交手数", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(9)
        item.setText(_translate("Form", "成交手数", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(10)
        item.setText(_translate("Form", "详细状态", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(11)
        item.setText(_translate("Form", "报单时间", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(12)
        item.setText(_translate("Form", "最后成交时间", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(13)
        item.setText(_translate("Form", "报单编号", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(14)
        item.setText(_translate("Form", "投保", None))
        item = self.tableWidget_all_orders.horizontalHeaderItem(15)
        item.setText(_translate("Form", "交易所", None))
        __sortingEnabled = self.tableWidget_all_orders.isSortingEnabled()
        self.tableWidget_all_orders.setSortingEnabled(False)
        item = self.tableWidget_all_orders.item(0, 0)
        item.setText(_translate("Form", "800658", None))
        item = self.tableWidget_all_orders.item(0, 1)
        item.setText(_translate("Form", "1", None))
        item = self.tableWidget_all_orders.item(0, 2)
        item.setText(_translate("Form", "cu1610", None))
        item = self.tableWidget_all_orders.item(0, 3)
        item.setText(_translate("Form", "买", None))
        item = self.tableWidget_all_orders.item(0, 4)
        item.setText(_translate("Form", "开", None))
        item = self.tableWidget_all_orders.item(0, 5)
        item.setText(_translate("Form", "未成交", None))
        item = self.tableWidget_all_orders.item(0, 6)
        item.setText(_translate("Form", "82990", None))
        item = self.tableWidget_all_orders.item(0, 7)
        item.setText(_translate("Form", "1", None))
        item = self.tableWidget_all_orders.item(0, 8)
        item.setText(_translate("Form", "1", None))
        item = self.tableWidget_all_orders.item(0, 9)
        item.setText(_translate("Form", "0", None))
        item = self.tableWidget_all_orders.item(0, 10)
        item.setText(_translate("Form", "未成交", None))
        item = self.tableWidget_all_orders.item(0, 13)
        item.setText(_translate("Form", "291759", None))
        item = self.tableWidget_all_orders.item(0, 14)
        item.setText(_translate("Form", "投机", None))
        self.tableWidget_all_orders.setSortingEnabled(__sortingEnabled)
        self.groupBox_order_insert.setTitle(_translate("Form", "下单板", None))
        self.label_buyorsell.setText(_translate("Form", "买卖", None))
        self.lineEdit_heyue.setText(_translate("Form", "cu1601", None))
        self.label_heyue.setText(_translate("Form", "合约", None))
        self.radioButton_kaicang.setText(_translate("Form", "开仓", None))
        self.radioButton_maichu.setText(_translate("Form", "卖出", None))
        self.label_kaiping.setText(_translate("Form", "开平", None))
        self.label_shoushu.setText(_translate("Form", "手数", None))
        self.radioButton_pingcang.setText(_translate("Form", "平仓", None))
        self.radioButton_pingjin.setText(_translate("Form", "平今", None))
        self.radioButton_mairu.setText(_translate("Form", "买入", None))
        self.label_xiadanjiage.setText(_translate("Form", "价格", None))
        self.pushButton_xiadantiaocang.setText(_translate("Form", "调仓", None))
        self.pushButton_xiandan.setText(_translate("Form", "下单", None))
        self.pushButton_xiadanquxiao.setText(_translate("Form", "取消", None))
        self.label_pankouguadansell.setText(_translate("Form", "卖 82990 / 3", None))
        self.label_dietingjia.setText(_translate("Form", "↓88020", None))
        self.label_zuidashoushu.setText(_translate("Form", "≤0", None))
        self.label_zhangtingjia.setText(_translate("Form", "↑88020", None))
        self.label_pankouguadanbuy.setText(_translate("Form", "买 82970 / 20", None))
        self.checkBox_taoli.setText(_translate("Form", "套利", None))
        self.checkBox_baozhi.setText(_translate("Form", "保值", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

