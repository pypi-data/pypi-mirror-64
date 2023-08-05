import pathlib
import math
import tempfile
import time

import nibabel as nib
import numpy as np
import pydicom
import vtk
from PySide2.QtGui import *
from typing import Union, Optional, List
from numba import jit
from acetabular_segment import bulid_model, get_center, get_radius

import vmi


def ary_flip_pre(ary: np.ndarray):
    return np.flip(np.flip(ary.swapaxes(0, 2), 1), 0)


def pre_flip_ary(ary: np.ndarray):
    return np.flip(np.flip(ary, 0), 1).swapaxes(0, 2)


def bone_win_nor(image_data):
    image_data[image_data < -100] = -100
    image_data[image_data > 900] = 900
    image_data = (image_data + 100) / 1000
    return image_data


@jit(nopython=True)
def ary_pad(input_ary, constant):
    for k in [0, input_ary.shape[0] - 1]:
        for j in range(input_ary.shape[1]):
            for i in range(input_ary.shape[2]):
                input_ary[k][j][i] = constant
    for k in range(input_ary.shape[0]):
        for j in [0, input_ary.shape[1] - 1]:
            for i in range(input_ary.shape[2]):
                input_ary[k][j][i] = constant
    for k in range(input_ary.shape[0]):
        for j in range(input_ary.shape[1]):
            for i in [0, input_ary.shape[2] - 1]:
                input_ary[k][j][i] = constant


def imReslice(image: vtk.vtkImageData,
              cs: Optional[vmi.CS4x4] = None,
              size: Union[np.ndarray, List[float]] = None,
              back_scalar: Union[int, float] = 0) -> vtk.vtkImageData:
    if cs is None:
        cs = vmi.CS4x4()

    if size is None:
        size = [vmi.imSize_Vt(image, cs.axis(0)),
                vmi.imSize_Vt(image, cs.axis(1)),
                vmi.imSize_Vt(image, cs.axis(2))]

    spc = np.array([1, 1, 1])

    ext = [0, int(size[0]) - 1,
           0, int(size[1]) - 1,
           0, int(size[2]) - 1]

    re = vtk.vtkImageReslice()
    re.SetInputData(image)
    re.SetInterpolationModeToCubic()
    re.SetResliceAxes(cs.matrix4x4())
    re.SetOutputOrigin([0, 0, 0])
    re.SetOutputSpacing(spc)
    re.SetOutputExtent(ext)
    re.SetBackgroundLevel(back_scalar)
    re.Update()

    return re.GetOutput()


def modelToLargestRegion(pd: vtk.vtkPolyData):
    pdcf = vtk.vtkPolyDataConnectivityFilter()
    pdcf.SetInputData(pd)
    pdcf.SetExtractionModeToLargestRegion()
    pdcf.Update()

    smooth = vtk.vtkSmoothPolyDataFilter()
    smooth.SetInputData(pdcf.GetOutput())
    smooth.SetNumberOfIterations(20)
    smooth.Update()

    sinc = vtk.vtkWindowedSincPolyDataFilter()
    sinc.SetInputData(smooth.GetOutput())
    sinc.SetNumberOfIterations(20)
    sinc.SetBoundarySmoothing(0)
    sinc.SetFeatureEdgeSmoothing(0)
    sinc.SetFeatureAngle(60)
    sinc.SetPassBand(0.1)
    sinc.SetNonManifoldSmoothing(1)
    sinc.SetNormalizeCoordinates(1)
    sinc.Update()

    return sinc.GetOutput()


def read_dicom():
    dcmdir = vmi.askDirectory('DICOM')  # 用户选择文件夹

    if dcmdir is not None:  # 判断用户选中了有效文件夹并点击了确认
        series_list = vmi.sortSeries(dcmdir)  # 将文件夹及其子目录包含的所有DICOM文件分类到各个系列

        if len(series_list) > 0:  # 判断该文件夹内包含有效的DICOM系列
            global series
            series = vmi.askSeries(series_list)  # 用户选择DICOM系列

            if series is not None:  # 判断用户选中了有效系列并点击了确认
                with pydicom.dcmread(series.filenames()[0]) as ds:
                    global patient_name
                    patient_name = str(ds.PatientName)
                    patient_name_box.draw_text('姓名：{}'.format(patient_name))
                    patient_name_box.setVisible(True)

                    global dicom_ds
                    dicom_ds = series.toKeywordValue()
                return series.read()  # 读取DICOM系列为图像数据


def on_init_voi():
    global voi_image
    voi_image = original_slice.data()
    voi_volume.setData(voi_image)
    voi_view.setCamera_Coronal()
    voi_view.setCamera_FitAll()


def init_pelvis():
    global model
    if td_pts[0].sum() != 0 and td_pts[1].sum() != 0:
        cs = vmi.CS4x4(axis0=np.array([1, 0, 0]),
                       axis1=np.array([0, 1, 0]),
                       axis2=np.array([0, 0, 1]),
                       origin=vmi.imOrigin(voi_image))

        seg_origin_pts = [td_pts[0] - 64 * cs.axis(0) - 48 * cs.axis(1) - 32 * cs.axis(2),
                          td_pts[1] - 32 * cs.axis(0) - 48 * cs.axis(1) - 32 * cs.axis(2)]

        seg_cs = [vmi.CS4x4(axis0=np.array([1, 0, 0]),
                            axis1=np.array([0, 1, 0]),
                            axis2=np.array([0, 0, 1]),
                            origin=seg_origin_pts[0]),
                  vmi.CS4x4(axis0=np.array([1, 0, 0]),
                            axis1=np.array([0, 1, 0]),
                            axis2=np.array([0, 0, 1]),
                            origin=seg_origin_pts[1])]

        size = np.array([96, 96, 96])
        seg_image = [imReslice(voi_image, seg_cs[0], size),
                     imReslice(voi_image, seg_cs[1], size)]

        seg_image[0].SetOrigin(seg_cs[0].origin())
        seg_image[1].SetOrigin(seg_cs[1].origin())

        model = bulid_model('nomal_model.h5')

        seg_ary = [vmi.imArray_VTK(seg_image[0]),
                   vmi.imArray_VTK(seg_image[1])]
        seg_pre = [np.squeeze(model.predict(bone_win_nor(ary_flip_pre(seg_ary[0]))[np.newaxis, :, :, :, np.newaxis])),
                   np.squeeze(model.predict(bone_win_nor(ary_flip_pre(seg_ary[1]))[np.newaxis, :, :, :, np.newaxis]))]
        seg_pre[0] = pre_flip_ary(seg_pre[0]) * (bone_value / probability)
        seg_pre[1] = pre_flip_ary(seg_pre[1]) * (bone_value / probability)

        voi_ext = np.array([vmi.imExtent(voi_image)[1] + 1,
                            vmi.imExtent(voi_image)[3] + 1,
                            vmi.imExtent(voi_image)[5] + 1])

        voi_ary = vmi.imArray_VTK(imReslice(voi_image, cs, voi_ext))

        seg_ijk_ori = [np.array((seg_origin_pts[0] - vmi.imOrigin(voi_image))).astype('int16'),
                       np.array((seg_origin_pts[1] - vmi.imOrigin(voi_image))).astype('int16')]

        voi_ary[seg_ijk_ori[0][2]:seg_ijk_ori[0][2] + 96,
        seg_ijk_ori[0][1]:seg_ijk_ori[0][1] + 96,
        seg_ijk_ori[0][0]:seg_ijk_ori[0][0] + 96] = seg_pre[0]

        voi_ary[seg_ijk_ori[1][2]:seg_ijk_ori[1][2] + 96,
        seg_ijk_ori[1][1]:seg_ijk_ori[1][1] + 96,
        seg_ijk_ori[1][0]:seg_ijk_ori[1][0] + 96] = seg_pre[1]

        pre_image = vmi.imVTK_Array(voi_ary, [0, 0, 0], [1, 1, 1])
        pre_image = vmi.imResample_Isotropic(pre_image)
        pd = vmi.imIsosurface(pre_image, bone_value)

        pelvis_prop.setData(modelToLargestRegion(pd))
        pelvis_view.setCamera_Coronal()
        pelvis_view.setCamera_FitAll()

        model.load_weights('acetabular_cup_placement_model.h5')
        pre = [np.squeeze(model.predict(bone_win_nor(ary_flip_pre(seg_ary[0]))[np.newaxis, :, :, :, np.newaxis])),
               np.squeeze(model.predict(bone_win_nor(ary_flip_pre(seg_ary[1]))[np.newaxis, :, :, :, np.newaxis]))]
        pre[0] = pre_flip_ary(pre[0])
        pre[1] = pre_flip_ary(pre[1])

        acetabular_center = [get_center(pre[0]), get_center(pre[1])]
        acetabular_radius = [get_radius(pre[0]), get_radius(pre[1])]

        acetabular_center[0] += seg_ijk_ori[0]
        acetabular_center[1] += seg_ijk_ori[1]

        cup_prop[0].setData(vmi.pdSphere(acetabular_radius[0], acetabular_center[0]))
        cup_prop[1].setData(vmi.pdSphere(acetabular_radius[1], acetabular_center[1]))

        # # 保存
        # nib.save(nib.Nifti1Image(bone_win_nor(ary_flip_pre(seg_ary[0])), None), 'p0.nii.gz')
        # nib.save(nib.Nifti1Image(bone_win_nor(ary_flip_pre(seg_ary[1])), None), 'p1.nii.gz')
        # nib.save(nib.Nifti1Image(seg_pre[0], None), '0.nii.gz')
        # nib.save(nib.Nifti1Image(seg_pre[1], None), '1.nii.gz')
        # nib.save(nib.Nifti1Image(pre[0], None), 's0.nii.gz')
        # nib.save(nib.Nifti1Image(pre[1], None), 's1.nii.gz')


def LeftButtonPress(**kwargs):
    global td_pts
    if kwargs['picked'] is voi_view:
        if tdpick_box.text() == '请选取右侧泪滴':
            td_pts[0] = voi_view.pickPt_Cell()
            td_prop[0].setData(vmi.pdSphere(2.5, td_pts[0]))
            tdpick_box.draw_text('请选取左侧泪滴')
        elif tdpick_box.text() == '请选取左侧泪滴':
            td_pts[1] = voi_view.pickPt_Cell()
            td_prop[1].setData(vmi.pdSphere(2.5, td_pts[1]))
            tdpick_box.draw_text('选取泪滴标志点')


def LeftButtonPressRelease(**kwargs):
    global bone_value
    if kwargs['picked'] is dicom_box:
        original_image = read_dicom()
        if original_image is not None:
            original_slice.setData(original_image)
            original_slice.setSlicePlaneOrigin_Center()
            original_slice.setSlicePlaneNormal_Coronal()
            original_view.setCamera_Coronal()
            original_view.setCamera_FitAll()
            on_init_voi()

        return True
    elif kwargs['picked'] is bone_value_box:
        v = vmi.askInt(-1000, bone_value, 3000)
        if v is not None:
            bone_value = v
            bone_value_box.draw_text('骨阈值：{:.0f} HU'.format(bone_value))
            voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})

        return True
    elif kwargs['picked'] is tdpick_box:
        if tdpick_box.text() == '选取泪滴标志点':
            tdpick_box.draw_text('请选取右侧泪滴')

        return True
    elif kwargs['picked'] is init_pelvis_box:
        init_pelvis_box.draw_text('请耐心等待')
        init_pelvis()
        init_pelvis_box.draw_text('创建骨盆')
        return True


def NoButtonWheel(**kwargs):
    global bone_value
    if kwargs['picked'] is bone_value_box:
        bone_value = min(max(bone_value + 10 * kwargs['delta'], -1000), 3000)
        bone_value_box.draw_text('骨阈值：{:.0f} HU'.format(bone_value))
        voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})


def return_globals():
    return globals()


if __name__ == '__main__':
    global original_view, voi_view, pelvis_view

    main = vmi.Main(return_globals)
    main.setAppName('全髋关节置换(THA)规划')
    main.setAppVersion(vmi.version)
    main.excludeKeys += ['main', 'i', 'box', 'prop', 'voi_image']

    select = vmi.askButtons(['新建', '打开'], title=main.appName())
    if select is None:
        vmi.appexit()

    if select == '打开':
        open_file = vmi.askOpenFile(nameFilter='*.vmi', title='打开存档')
        if open_file is not None:
            main.loads(pathlib.Path(open_file).read_bytes())
        else:
            vmi.appexit()
    elif select == '新建':
        patient_name = str()

        # 0 原始图像
        original_target, LR = np.zeros(3), 1
        original_view = vmi.View()

        original_slice = vmi.ImageSlice(original_view)  # 断层显示
        original_slice.setColorWindow_Bone()
        original_slice.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        dicom_box = vmi.TextBox(original_view, text='DICOM', pickable=True,
                                size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0])
        dicom_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        patient_name_box = vmi.TextBox(original_view, text='姓名', visible=False,
                                       size=[0.2, 0.04], pos=[0, 0.1], anchor=[0, 0])

        # 1 目标区域
        voi_view = vmi.View()
        voi_view.mouse['LeftButton']['Press'] = [LeftButtonPress]

        bone_value, target_value = 200, -1100

        bone_value_box = vmi.TextBox(voi_view, text='骨阈值：{:.0f} HU'.format(bone_value),
                                     size=[0.2, 0.04], pos=[0, 0.04], anchor=[0, 0], pickable=True)
        bone_value_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]
        bone_value_box.mouse['NoButton']['Wheel'] = [NoButtonWheel]

        voi_size, voi_center, voi_origin, voi_cs = np.zeros(3), np.zeros(3), np.zeros(3), vmi.CS4x4()
        voi_image = vtk.vtkImageData()

        voi_volume = vmi.ImageVolume(voi_view, pickable=True)
        voi_volume.setOpacityScalar({bone_value - 1: 0, bone_value: 1})
        voi_volume.setColor({bone_value: [1, 1, 0.6]})

        # 泪滴选点
        td_pts = np.zeros((2, 3))
        td_prop = [vmi.PolyActor(voi_view, color=[0.4, 0.6, 1]),
                   vmi.PolyActor(voi_view, color=[0.4, 0.6, 1])]

        tdpick_box = vmi.TextBox(voi_view, text='选取泪滴标志点', size=[0.2, 0.04], pos=[0, 0.1], anchor=[0, 0], pickable=True)
        tdpick_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        probability = 0.6

        # 创建骨盆
        init_pelvis_box = vmi.TextBox(voi_view, text='创建骨盆', fore_color=QColor('white'), back_color=QColor('crimson'),
                                      bold=True, size=[0.2, 0.04], pos=[1, 0.04], anchor=[1, 0], pickable=True)
        init_pelvis_box.mouse['LeftButton']['PressRelease'] = [LeftButtonPressRelease]

        # 5 骨盆视图
        pelvis_view = vmi.View()
        pelvis_prop = vmi.PolyActor(pelvis_view, color=[1, 1, 0.6])

        cup_prop = [vmi.PolyActor(pelvis_view, color=[0.4, 0.6, 1], line_width=3, pickable=True),
                    vmi.PolyActor(pelvis_view, color=[0.4, 0.6, 1], line_width=3, pickable=True)]

    # 视图布局
    for v in [original_view, voi_view, pelvis_view]:
        v.setMinimumWidth(round(0.5 * main.screenWidth()))

    original_view.setParent(main.scrollArea())
    main.layout().addWidget(original_view, 0, 0, 1, 1)
    main.layout().addWidget(voi_view, 0, 1, 1, 1)
    main.layout().addWidget(pelvis_view, 0, 2, 1, 1)

    vmi.appexec(main)  # 执行主窗口程序
    vmi.appexit()  # 清理并退出程序
