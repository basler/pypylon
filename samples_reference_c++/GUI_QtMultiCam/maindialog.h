#ifndef MAINDIALOG_H
#define MAINDIALOG_H

/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample illustrates the use of a Qt GUI together with the pylon C++ API to enumerate the attached cameras, to
    configure a camera, to start and stop the grab and to display grabbed images.
    It shows how to use GUI controls to display and modify camera parameters.
*/

#include <QDialog>
#include <QTimer>
#include <QSlider>
#include <QComboBox>
#include <QLabel>
#include "guicamera.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainDialog; }
QT_END_NAMESPACE



class MainDialog : public QDialog
{
    Q_OBJECT

public:
    MainDialog(QWidget *parent = nullptr);
    ~MainDialog();

    int EnumerateDevices();

    void ShowWarning( QString warningText );

    void UpdateCameraDialog( int cameraId );
    void UpdateSlider( QSlider* pCtrl, Pylon::IIntegerEx& integerParameter );
    void UpdateSliderText( QLabel *pString, Pylon::IIntegerEx& integerParameter );
    void UpdateEnumeration( QComboBox* pCtrl, Pylon::IEnumerationEx& enumParameter );
    void ClearSlider( QSlider* pCtrl, QLabel* pString );
    void ClearEnumeration( QComboBox* pCtrl );
    bool InternalOpenCamera( const Pylon::CDeviceInfo& devInfo, int cameraId );
    void InternalCloseCamera( int cameraId );

protected:
    virtual void showEvent(QShowEvent *event) override;
    virtual void paintEvent(QPaintEvent *) override;

private slots:
    // Slots for GuiCamera signals
    void OnNewGrabResult( int userHint );
    void OnStateChanged( int userHint, bool isGrabbing );
    void OnDeviceRemoved( int userHint );
    void OnNodeUpdated( int userHint, GenApi::INode* pNode );

    // Slots for GUI signals
    void on_scanButton_clicked();
    void on_cameraList_currentIndexChanged(int index);
    void on_openSelected_1_clicked();
    void on_openSelected_2_clicked();
    void on_openBySN_1_clicked();
    void on_openBySN_2_clicked();
    void on_openByUserID_1_clicked();
    void on_openByUserID_2_clicked();
    void on_close_1_clicked();
    void on_close_2_clicked();
    void on_singleShot_1_clicked();
    void on_singleShot_2_clicked();
    void on_continuous_1_clicked();
    void on_continuous_2_clicked();
    void on_stop_1_clicked();
    void on_stop_2_clicked();
    void on_exposure_1_valueChanged(int value);
    void on_exposure_2_valueChanged(int value);
    void on_gain_1_valueChanged(int value);
    void on_gain_2_valueChanged(int value);
    void on_pixelFormat_1_currentIndexChanged(int index);
    void on_pixelFormat_2_currentIndexChanged(int index);
    void on_triggerMode_1_currentTextChanged(const QString &arg1);
    void on_triggerMode_2_currentTextChanged(const QString &arg1);
    void on_triggerSource_1_currentTextChanged(const QString &arg1);
    void on_triggerSource_2_currentTextChanged(const QString &arg1);
    void on_softwareTrigger_1_clicked();
    void on_softwareTrigger_2_clicked();
    void on_invertPixel_1_toggled(bool checked);
    void on_invertPixel_2_toggled(bool checked);

    void OnUpdateTimer();

    void on_editSN_1_textEdited(const QString &arg1);

    void on_editSN_2_textEdited(const QString &arg1);

    void on_editUserID_1_textEdited(const QString &arg1);

    void on_editUserID_2_textEdited(const QString &arg1);

private:
    Ui::MainDialog *ui;
    Pylon::DeviceInfoList_t m_devices;
    static const int MaxCamera = 2;
    CGuiCamera m_camera[MaxCamera];
    QTimer m_updateTimer;
};
#endif // MAINDIALOG_H
