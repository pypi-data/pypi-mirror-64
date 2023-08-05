import os
import pathlib
import time

import gridfs
import pymongo
import requests
from PySide2.QtWidgets import *

import vmi
import vmi.application.skyward

case_db = vmi.application.skyward.case_db
order_db = vmi.application.skyward.order_db
user_db = vmi.application.skyward.user_db
role_customer_db = vmi.application.skyward.role_customer_db
role_sales_worker_db = vmi.application.skyward.role_sales_worker_db
role_product_designer_db = vmi.application.skyward.role_product_designer_db
role_quality_inspector_db = vmi.application.skyward.role_quality_inspector_db
dicom_fs = vmi.application.skyward.dicom_fs
vti_fs = vmi.application.skyward.vti_fs
vtp_fs = vmi.application.skyward.vtp_fs
stl_fs = vmi.application.skyward.stl_fs


def tray_icon_activated(reason: QSystemTrayIcon.ActivationReason):
    if reason is QSystemTrayIcon.Trigger:
        print(reason)


def download_order_files(order_uid: str):
    p = vmi.askDirectory('设计文件夹')
    if not p:
        return

    case = case_db.find_one({'order_uid': order_uid})

    for f in case['order_files']:
        if f.endswith('stl'):
            if not stl_fs.find_one({'_id': case[f]}):
                vmi.askInfo('错误：设计文件不存在 {}'.format(f))
                return

    p = pathlib.Path(p) / (order_uid + ' ' + time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime()))
    os.mkdir(p)

    for f in case['order_files']:
        if f.endswith('stl'):
            b = stl_fs.find_one({'_id': case[f]}).read()
            (pathlib.Path(p) / (f + '.stl')).write_bytes(b)

    vmi.askInfo('下载完成')


def find_order_released():
    combo = QComboBox()
    for case in case_db.find():
        if case['customer_confirmed']:
            if case['order_released'] and not case['order_inspected'] and not case['order_completed']:
                t = case['last_update_time'][:14]
                t = [t[:4], t[4:6], t[6:8], t[8:10], t[10:12], t[12:14]]
                t = '-'.join(t)
                combo.addItem(case['order_uid'] + ' ' + t, case['order_uid'])

    if not combo.count():
        vmi.askInfo('无待检生产单')
        return

    sizep = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    dialog = QDialog()
    dialog.setSizePolicy(sizep)
    dialog.setWindowTitle('选择待检生产单')
    dialog.setLayout(QVBoxLayout())
    dialog.setMinimumWidth(200)
    dialog.layout().addWidget(combo)

    ok_cancel = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
    ok_cancel.setSizePolicy(sizep)
    ok_cancel.accepted.connect(dialog.accept)
    ok_cancel.rejected.connect(dialog.reject)
    dialog.layout().addWidget(ok_cancel)

    if dialog.exec_() != QDialog.Accepted:
        return

    r = vmi.askButtons(['下载设计文件', '接受生产单', '驳回生产单'])
    if r == '下载设计文件':
        user = vmi.application.skyward.ask_user()
        if not user:
            return False

        role_quality_inspector_id = user['role_quality_inspector_id']
        if not role_quality_inspector_db.find_one({'_id': role_quality_inspector_id}):
            vmi.askInfo('错误：只有质量检验员可以下载设计文件')
            return False

        download_order_files(combo.currentData())
    elif r == '接受生产单':
        user = vmi.application.skyward.ask_user()
        if not user:
            return False

        role_quality_inspector_id = user['role_quality_inspector_id']
        if not role_quality_inspector_db.find_one({'_id': role_quality_inspector_id}):
            vmi.askInfo('错误：只有质量检验员可以接受生产单')
            return False

        case_set = {'role_quality_inspector_id': role_quality_inspector_id,
                    'order_released': True,
                    'order_inspected': True,
                    'order_completed': False}

        try:
            find = case_db.find_one({'order_uid': combo.currentData()})
            case_uid = vmi.convert_base(round(time.time() * 100))
            response = requests.post(url='http://med-3d.top:2334/sys/caseUpdate',
                                     headers={'_id': str(find['_id']), 'case_uid': case_uid})
            if response.text == 'true':
                case_db.find_one_and_update({'_id': find['_id']}, {'$set': case_set})
                vmi.askInfo('同步完成')
                return True
            else:
                vmi.askInfo('错误：' + response.text)
        except Exception as e:
            vmi.askInfo('错误：' + str(e))
    elif r == '驳回生产单':
        user = vmi.application.skyward.ask_user()
        if not user:
            return False

        role_quality_inspector_id = user['role_quality_inspector_id']
        if not role_quality_inspector_db.find_one({'_id': role_quality_inspector_id}):
            vmi.askInfo('错误：只有质量检验员可以驳回生产单')
            return False

        case_set = {'role_quality_inspector_id': role_quality_inspector_id,
                    'order_released': False,
                    'order_inspected': False,
                    'order_completed': False}

        try:
            find = case_db.find_one({'order_uid': combo.currentData()})
            case_uid = vmi.convert_base(round(time.time() * 100))
            response = requests.post(url='http://med-3d.top:2334/sys/caseUpdate',
                                     headers={'_id': str(find['_id']), 'case_uid': case_uid})
            if response.text == 'true':
                case_db.find_one_and_update({'_id': find['_id']}, {'$set': case_set})
                vmi.askInfo('同步完成')
                return True
            else:
                vmi.askInfo('错误：' + response.text)
        except Exception as e:
            vmi.askInfo('错误：' + str(e))


def find_order_inspected():
    combo = QComboBox()
    for case in case_db.find():
        if case['customer_confirmed']:
            if case['order_released'] and case['order_inspected'] and not case['order_completed']:
                t = case['last_update_time'][:14]
                t = [t[:4], t[4:6], t[6:8], t[8:10], t[10:12], t[12:14]]
                t = '-'.join(t)
                combo.addItem(case['order_uid'] + ' ' + t, case['order_uid'])

    if not combo.count():
        vmi.askInfo('无在产生产单')
        return

    sizep = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
    dialog = QDialog()
    dialog.setSizePolicy(sizep)
    dialog.setWindowTitle('选择在产生产单')
    dialog.setLayout(QVBoxLayout())
    dialog.setMinimumWidth(200)
    dialog.layout().addWidget(combo)

    ok_cancel = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
    ok_cancel.setSizePolicy(sizep)
    ok_cancel.accepted.connect(dialog.accept)
    ok_cancel.rejected.connect(dialog.reject)
    dialog.layout().addWidget(ok_cancel)

    if dialog.exec_() != QDialog.Accepted:
        return

    r = vmi.askButtons(['下载设计文件', '完成生产单'])
    if r == '下载设计文件':
        user = vmi.application.skyward.ask_user()
        if not user:
            return False

        role_quality_inspector_id = user['role_quality_inspector_id']
        if not role_quality_inspector_db.find_one({'_id': role_quality_inspector_id}):
            vmi.askInfo('错误：只有质量检验员可以下载设计文件')
            return False

        download_order_files(combo.currentData())
    elif r == '完成生产单':
        user = vmi.application.skyward.ask_user()
        if not user:
            return False

        role_quality_inspector_id = user['role_quality_inspector_id']
        if not role_quality_inspector_db.find_one({'_id': role_quality_inspector_id}):
            vmi.askInfo('错误：只有质量检验员可以完成生产单')
            return False

        case_set = {'role_quality_inspector_id': role_quality_inspector_id,
                    'order_released': True,
                    'order_inspected': True,
                    'order_completed': True}

        try:
            find = case_db.find_one({'order_uid': combo.currentData()})
            case_uid = vmi.convert_base(round(time.time() * 100))
            response = requests.post(url='http://med-3d.top:2334/sys/caseUpdate',
                                     headers={'_id': str(find['_id']), 'case_uid': case_uid})
            if response.text == 'true':
                case_db.find_one_and_update({'_id': find['_id']}, {'$set': case_set})
                vmi.askInfo('同步完成')
                return True
            else:
                vmi.askInfo('错误：' + response.text)
        except Exception as e:
            vmi.askInfo('错误：' + str(e))


if __name__ == '__main__':
    vmi.app.setApplicationName('Skyorder')
    vmi.app.setApplicationVersion('1.0')
    vmi.app.setQuitOnLastWindowClosed(False)

    client = pymongo.MongoClient('mongodb://root:medraw123@med-3d.top:27018/admin', 27017)
    database = client.skyward
    case_db = database.get_collection('case')
    order_db = database.get_collection('order')
    stl_fs = gridfs.GridFS(database, collection='stl')

    tray_icon_menu = QMenu()
    tray_icon_menu.addAction('待检生产单').triggered.connect(find_order_released)
    tray_icon_menu.addAction('在产生产单').triggered.connect(find_order_inspected)
    tray_icon_menu.addSeparator()
    tray_icon_menu.addAction('关于').triggered.connect(vmi.app_about)
    tray_icon_menu.addSeparator()
    tray_icon_menu.addAction('退出').triggered.connect(vmi.app.quit)

    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(QWidget().style().standardIcon(QStyle.SP_ComputerIcon))
    tray_icon.setToolTip('{} {}'.format(vmi.app.applicationName(), vmi.app.applicationVersion()))
    tray_icon.setContextMenu(tray_icon_menu)
    tray_icon.activated.connect(tray_icon_activated)
    tray_icon.show()

    vmi.app.exec_()
    vmi.appexit()
