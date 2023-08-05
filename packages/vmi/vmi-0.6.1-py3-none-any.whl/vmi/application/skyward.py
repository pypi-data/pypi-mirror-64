import csv
import hashlib
import time
from typing import Optional, Union

import gridfs
import pydicom
import pymongo
import requests
from PySide2.QtWidgets import *

import vmi

client = pymongo.MongoClient('mongodb://skyward:Yw309309@med-3d.top:27018/skyward', 27017)
database = client.skyward
case_db = database.get_collection('case')
order_db = database.get_collection('order')
user_db = database.get_collection('user')
role_customer_db = database.get_collection('role_customer')
role_sales_worker_db = database.get_collection('role_sales_worker')
role_product_designer_db = database.get_collection('role_product_designer')
role_quality_inspector_db = database.get_collection('role_quality_inspector')
dicom_fs = gridfs.GridFS(database, collection='dicom')
vti_fs = gridfs.GridFS(database, collection='vti')
vtp_fs = gridfs.GridFS(database, collection='vtp')
stl_fs = gridfs.GridFS(database, collection='stl')


def ask_user() -> Optional[dict]:
    ok, find_user = True, {}
    while ok:
        text, ok = QInputDialog.getText(None, '请输入', '手机号：', QLineEdit.Normal)
        if not ok:
            return None

        find_user = user_db.find_one({'telephone': text})
        if not find_user:
            vmi.askInfo('手机号未注册')
            ok = True
            continue

        ok = False

    ok = True
    while ok:
        text, ok = QInputDialog.getText(None, '请输入', '密码：', QLineEdit.Password)
        if not ok:
            return None

        if find_user['password'] != hashlib.md5(text.encode()).hexdigest():
            vmi.askInfo('密码错误')
            ok = True
            continue

        ok = False
    return find_user


def ask_customer_id() -> Optional[dict]:
    sizep = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    dialog = QDialog()
    dialog.setSizePolicy(sizep)
    dialog.setWindowTitle('选择顾客')
    dialog.setLayout(QVBoxLayout())
    dialog.setMinimumWidth(200)

    customer_combo = QComboBox()
    dialog.layout().addWidget(customer_combo)

    for i in role_customer_db.find():
        customer_combo.addItem('{} {} {}'.format(i['_id'], i['name'], i['organization']), i['_id'])

    ok_cancel = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
    ok_cancel.setSizePolicy(sizep)
    ok_cancel.accepted.connect(dialog.accept)
    ok_cancel.rejected.connect(dialog.reject)
    dialog.layout().addWidget(ok_cancel)

    if dialog.exec_() == QDialog.Accepted:
        return customer_combo.currentData()
    else:
        return None


def ask_sales_worker_id() -> Optional[dict]:
    sizep = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    dialog = QDialog()
    dialog.setSizePolicy(sizep)
    dialog.setWindowTitle('选择销售')
    dialog.setLayout(QVBoxLayout())
    dialog.setMinimumWidth(200)

    sales_worker_combo = QComboBox()
    dialog.layout().addWidget(sales_worker_combo)

    for i in role_sales_worker_db.find():
        sales_worker_combo.addItem('{} {} {}'.format(i['_id'], i['name'], i['organization']), i['_id'])

    ok_cancel = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
    ok_cancel.setSizePolicy(sizep)
    ok_cancel.accepted.connect(dialog.accept)
    ok_cancel.rejected.connect(dialog.reject)
    dialog.layout().addWidget(ok_cancel)

    if dialog.exec_() == QDialog.Accepted:
        return sales_worker_combo.currentData()
    else:
        return None


def dicom_kw_value(f: str) -> dict:
    kw_value = {}
    with pydicom.dcmread(f) as ds:
        for e in ds.iterall():
            if e.value.__class__ in [None, bool, int, float, str]:
                kw_value[e.keyword] = e.value
            elif e.value.__class__ in [bytes]:
                kw_value[e.keyword] = '{} bytes'.format(len(e.value))
            else:
                kw_value[e.keyword] = str(e.value)
    return {kw: kw_value[kw] for kw in sorted(kw_value)}


def case(order_model: str, order_uid: str, order_files: list,
         patient_name: str, patient_sex: str, patient_age: str,
         dicom_files: dict, vti_files: dict, vtp_files: dict, stl_files: dict,
         **kwargs) -> Optional[dict]:
    """
    构造本地案例
    :param order_model: 产品型号
    :param order_uid: 产品序列号
    :param order_files: 产品文件列表
    :param patient_name: 患者姓名
    :param patient_sex: 患者性别
    :param patient_age: 患者年龄
    :param dicom_files: 原始DICOM文件，每个关键词索引一个文件列表
    :param vti_files: vtkXMLImageData格式文件，每个关键词索引一个文件
    :param vtp_files: vtkXMLPolyData格式文件，每个关键词索引一个文件
    :param stl_files: STL格式文件，每个关键词索引一个文件
    :param kwargs: 其它相关信息，每个关键词索引一个支持数据库直接录入的对象
    :return: 案例信息
    """
    case_data = {}

    # 上传原始DICOM文件
    for kw in dicom_files:
        sop_uids = []
        for f in dicom_files[kw]:
            sop_uid = pydicom.dcmread(f).SOPInstanceUID
            sop_uids.append(sop_uid)

            if not dicom_fs.exists({'SOPInstanceUID': sop_uid}):
                dicom_fs.put(open(f, 'rb').read(), **dicom_kw_value(f))
        case_data[kw] = sop_uids

    # 上传其它格式文件
    files = [vti_files, vtp_files, stl_files]
    fs = [vti_fs, vtp_fs, stl_fs]
    for i in range(len(files)):
        for kw in files[i]:
            f_bytes = open(files[i][kw], 'rb').read()
            md5 = hashlib.md5(f_bytes).hexdigest()

            if fs[i].exists({'md5': md5}):
                case_data[kw] = fs[i].find_one({'md5': md5})._id
            else:
                case_data[kw] = fs[i].put(f_bytes)

    # 上传其它信息
    case_data['order_model'] = order_model
    case_data['order_uid'] = order_uid
    case_data['order_files'] = order_files
    case_data['patient_name'] = patient_name
    case_data['patient_sex'] = patient_sex
    case_data['patient_age'] = patient_age

    for kw in kwargs:
        case_data[kw] = kwargs[kw]
    return case_data


def case_sync(case: dict, ukw: list) -> Union[dict, bool]:
    """
    同步案例
    :param case: 本地案例信息
    :param ukw: 特征键列表，用于判断相同案例
    :return: 同步后的案例信息
    """
    ukw_value = {kw: case[kw] for kw in ukw}

    # 清理相同无效案例
    for c in case_db.find(ukw_value):
        if 'case_uid' not in c:
            case_db.delete_one({'_id': c['_id']})

    # 查找相同有效案例
    find = case_db.find_one(ukw_value)

    if find and 'case_uid' in find:
        if find['order_released']:
            vmi.askInfo('生产单已发布')
            r = vmi.askButtons(['下载案例'])
        elif find['customer_confirmed']:
            vmi.askInfo('顾客已确认')
            r = vmi.askButtons(['上传案例', '下载案例', '发布生产单'])
        else:
            r = vmi.askButtons(['上传案例', '下载案例'])
    else:
        r = vmi.askButtons(['创建案例'])

    if r == '创建案例':
        user = ask_user()
        if not user:
            return False

        role_product_designer_id = user['role_product_designer_id']
        print(role_product_designer_id)
        if not role_product_designer_db.find_one({'_id': role_product_designer_id}):
            vmi.askInfo('错误：只有产品设计师可以创建案例')
            return False

        customer_uid = ask_customer_id()
        if not customer_uid:
            return False

        sales_worker_uid = ask_sales_worker_id()
        if not sales_worker_uid:
            return False

        case['role_product_designer_id'] = role_product_designer_id
        case['role_customer_id'] = customer_uid
        case['role_sales_worker_id'] = sales_worker_uid
        case['role_quality_inspector_id'] = None
        case['customer_confirmed'] = False
        case['order_released'] = False
        case['order_inspected'] = False
        case['order_completed'] = False

        _id = case_db.insert_one({kw: case[kw] for kw in sorted(case)}).inserted_id
        try:
            case_uid = vmi.convert_base(round(time.time() * 100))
            response = requests.post(url='http://med-3d.top:2334/sys/caseCreate',
                                     headers={'_id': str(_id), 'case_uid': case_uid})
            if response.text == 'true':
                find = case_db.find_one({'_id': _id})
                if 'case_uid' in find:
                    return True
                else:
                    case_db.delete_one({'_id': _id})
                    vmi.askInfo('错误：云端未分配编号')
            else:
                case_db.delete_one({'_id': _id})
                vmi.askInfo('错误：' + response.text)
        except Exception as e:
            case_db.delete_one({'_id': _id})
            vmi.askInfo('错误：' + str(e))
    elif r == '上传案例':
        user = ask_user()
        if not user:
            return False

        role_product_designer_id = user['role_product_designer_id']
        if not role_product_designer_db.find_one({'_id': role_product_designer_id}):
            vmi.askInfo('错误：只有产品设计师可以上传案例')
            return False

        case['role_product_designer_id'] = role_product_designer_id
        case['customer_confirmed'] = False
        case['order_released'] = False
        case['order_inspected'] = False
        case['order_completed'] = False

        try:
            case_uid = vmi.convert_base(round(time.time() * 100))
            response = requests.post(url='http://med-3d.top:2334/sys/caseUpdate',
                                     headers={'_id': str(find['_id']), 'case_uid': case_uid})
            if response.text == 'true':
                case_db.find_one_and_update({'_id': find['_id']}, {'$set': case})
                return True
            else:
                vmi.askInfo('错误：' + response.text)
        except Exception as e:
            vmi.askInfo('错误：' + str(e))
    elif r == '下载案例':
        return case_db.find_one({'_id': find['_id']})
    elif r == '发布生产单':
        user = ask_user()
        if not user:
            return False

        role_product_designer_id = user['role_product_designer_id']
        if not role_product_designer_db.find_one({'_id': role_product_designer_id}):
            vmi.askInfo('错误：只有产品设计师可以发布生产单')
            return False

        case_set = {'role_product_designer_id': role_product_designer_id, 'order_released': True}

        try:
            case_uid = vmi.convert_base(round(time.time() * 100))
            response = requests.post(url='http://med-3d.top:2334/sys/caseUpdate',
                                     headers={'_id': str(find['_id']), 'case_uid': case_uid})
            if response.text == 'true':
                case_db.find_one_and_update({'_id': find['_id']}, {'$set': case_set})
                return True
            else:
                vmi.askInfo('错误：' + response.text)
        except Exception as e:
            vmi.askInfo('错误：' + str(e))


def csv_update(db: str):
    f = vmi.askOpenFile('*.csv', db)
    if f is None:
        return

    db = database.get_collection(db)

    with open(f, newline='') as f:
        kw = []
        for row in csv.reader(f):
            if len(kw):
                kw[0] = '_id'
                i = dict(zip(kw, row))
                db.find_one_and_update({'_id': i['_id']}, {'$set': i}, upsert=True)
            else:
                kw = row.copy()


if __name__ == '__main__':
    csv_update('role_customer')
    csv_update('role_sales_worker')
    csv_update('role_product_designer')
    csv_update('role_quality_inspector')
