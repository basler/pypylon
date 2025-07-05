/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample illustrates the use of a Qt GUI together with the pylon C++ API to enumerate the attached cameras, to
    configure a camera, to start and stop the grab and to display grabbed images.
    It shows how to use GUI controls to display and modify camera parameters.
*/
#include <QMessageBox>
#include <QPainter>
#include <QDebug>
#include "maindialog.h"
#include "ui_maindialog.h"



MainDialog::MainDialog(QWidget *parent)
    : QDialog(parent)
    , ui(new Ui::MainDialog)
{
    ui->setupUi(this);

    for (int i = 0; i < MaxCamera; i++)
    {
        m_camera[i].SetUserHint( i );

        // Connect signals from CGuiCamera class to this dialog.
        QObject::connect( &(m_camera[i]), &CGuiCamera::NewGrabResult, this, &MainDialog::OnNewGrabResult );
        QObject::connect( &(m_camera[i]), &CGuiCamera::StateChanged, this, &MainDialog::OnStateChanged );
        QObject::connect( &(m_camera[i]), &CGuiCamera::DeviceRemoved, this, &MainDialog::OnDeviceRemoved );
        QObject::connect( &(m_camera[i]), &CGuiCamera::NodeUpdated, this, &MainDialog::OnNodeUpdated );
    }

    // Remove question mark from the title bar.
    setWindowFlags(windowFlags() & ~Qt::WindowContextHelpButtonHint);
}


MainDialog::~MainDialog()
{
    for (int i = 0; i < MaxCamera; i++)
    {
        m_camera[i].Close();
    }

    delete ui;
}


// When the dialog is shown, update the dialog, start a 1 s update timer and scan for cameras.
void MainDialog::showEvent(QShowEvent *event)
{
    QDialog::showEvent( event );

    // Enable/disable controls.
    for (int i = 0; i < MaxCamera; i++)
    {
        UpdateCameraDialog( i );
    }

    // Set timer for status bar (1000 ms update interval).
    connect(&m_updateTimer, SIGNAL(timeout()), this, SLOT(OnUpdateTimer()));
    m_updateTimer.start(1000);

    // Simulate the user clicking the Discover Cameras button.
    on_scanButton_clicked();
}


// Update the camera dialog by enabling/disabling control elements according to the camera state.
void MainDialog::UpdateCameraDialog( int cameraId )
{
    bool isCameraSelected = (ui->cameraList->currentIndex() != -1);
    bool isOpen = m_camera[cameraId].IsOpen();
    bool isGrabbing = isOpen && m_camera[cameraId].IsGrabbing();
    bool isSingleShotSupported = m_camera[cameraId].IsSingleShotSupported();

    if (cameraId == 0)
    {
        ui->openSelected_1->setEnabled( !isOpen && isCameraSelected );
        ui->editSN_1->setEnabled( !isOpen );
        ui->editUserID_1->setEnabled( !isOpen );
        ui->close_1->setEnabled( isOpen );
        ui->singleShot_1->setEnabled( isOpen && !isGrabbing && isSingleShotSupported );
        ui->continuous_1->setEnabled( isOpen && !isGrabbing );
        ui->stop_1->setEnabled( isGrabbing );
        ui->softwareTrigger_1->setEnabled( isOpen );
        ui->invertPixel_1->setEnabled( isOpen );

        // Disable these controls when a camera is open. Otherwise, check input.
        if (isOpen)
        {
            ui->openBySN_1->setEnabled( !isOpen );
            ui->openByUserID_1->setEnabled( !isOpen );
        }
        else
        {
            on_editSN_1_textEdited( ui->editSN_1->text() );
            on_editUserID_1_textEdited( ui->editUserID_1->text() );

            // Clear feature controls.
            ClearSlider( ui->exposure_1, ui->exposureLabel_1 );
            ClearSlider( ui->gain_1, ui->gainLabel_1 );
            ClearEnumeration( ui->pixelFormat_1 );
            ClearEnumeration( ui->triggerMode_1 );
            ClearEnumeration( ui->triggerSource_1 );
        }
    }
    else if (cameraId == 1)
    {
        ui->openSelected_2->setEnabled( !isOpen && isCameraSelected );
        ui->editSN_2->setEnabled( !isOpen );
        ui->editUserID_2->setEnabled( !isOpen );
        ui->close_2->setEnabled( isOpen );
        ui->singleShot_2->setEnabled( isOpen && !isGrabbing && isSingleShotSupported );
        ui->continuous_2->setEnabled( isOpen && !isGrabbing );
        ui->stop_2->setEnabled( isGrabbing );
        ui->softwareTrigger_2->setEnabled( isOpen );
        ui->invertPixel_2->setEnabled( isOpen );

        // Disable these controls when a camera is open. Otherwise, check input.
        if (isOpen)
        {
            ui->openBySN_2->setEnabled( !isOpen );
            ui->openByUserID_2->setEnabled( !isOpen );
        }
        else
        {
            on_editSN_2_textEdited( ui->editSN_2->text() );
            on_editUserID_2_textEdited( ui->editUserID_2->text() );

            // Clear feature controls.       
            ClearSlider( ui->exposure_2, ui->exposureLabel_2 );
            ClearSlider( ui->gain_2, ui->gainLabel_2 );
            ClearEnumeration( ui->pixelFormat_2 );
            ClearEnumeration( ui->triggerMode_2 );
            ClearEnumeration( ui->triggerSource_2 );
        }
    }
    else
    {
        assert( false );
    }
}


// This gets called every second. Update the status bar texts.
void MainDialog::OnUpdateTimer()
{
    // Update the status bars.
    if (m_camera[0].IsOpen())
    {
        uint64_t imageCount = m_camera[0].GetGrabbedImages();
        uint64_t errorCount = m_camera[0].GetGrabErrors();
        // Very rough approximation approximation. The timer is triggerd every second.
        double fpsEstimate = (double) m_camera[0].GetGrabbedImagesDiff();

        QString status = QString( "Frame rate: %0 fps\tImages: %1\tErrors: %2").arg(fpsEstimate, 6, 'f', 1).arg(imageCount).arg(errorCount);
        ui->statusbar_1->setText( status );
    }
    else
    {
        ui->statusbar_1->setText( "" );
    }

    if (m_camera[1].IsOpen())
    {
        uint64_t imageCount = m_camera[1].GetGrabbedImages();
        uint64_t errorCount = m_camera[1].GetGrabErrors();
        // Very rough approximation approximation. The timer is triggerd every second.
        double fpsEstimate = (double) m_camera[1].GetGrabbedImagesDiff();

        QString status = QString( "Frame rate: %0 fps\tImages: %1\tErrors: %2").arg(fpsEstimate, 6, 'f', 1).arg(imageCount).arg(errorCount);
        ui->statusbar_2->setText( status );
    }
    else
    {
        ui->statusbar_2->setText( "" );
    }
}


// Helper function to get a list of all attached devices and store it in m_devices.
int MainDialog::EnumerateDevices()
{
    Pylon::DeviceInfoList_t devices;
    try
    {
        // Get the transport layer factory.
        Pylon::CTlFactory& TlFactory = Pylon::CTlFactory::GetInstance();

        // Get all attached cameras.
        TlFactory.EnumerateDevices( devices );
    }
    catch (const Pylon::GenericException& e)
    {
        PYLON_UNUSED( e );
        devices.clear();

        qDebug() << e.GetDescription();
    }

    m_devices = devices;

    // When calling this function, make sure to update the device list control
    // because its items store pointers to elements in the m_devices list.
    return (int) m_devices.size();
}


// Show a warning dialog.
void MainDialog::ShowWarning( QString warningText )
{
    QMessageBox::warning( this, "GUI Sample", warningText, QMessageBox::Ok );
}


// The Discover Cameras button has been clicked.
void MainDialog::on_scanButton_clicked()
{
    // Remove all items from the combo box.
    ui->cameraList->clear();

    QApplication::setOverrideCursor(QCursor(Qt::WaitCursor));
    // Enumerate devices.
    int deviceCount = EnumerateDevices();
    QApplication::restoreOverrideCursor();

    if (deviceCount == 0)
    {
       ShowWarning( "No camera found." );
       return;
    }

    // Fill the combo box.
    for (Pylon::DeviceInfoList_t::const_iterator it = m_devices.begin(); it != m_devices.end(); ++it)
    {
       // Get the pointer to the current device info.
       const Pylon::CDeviceInfo* const pDeviceInfo = &(*it);

       // Add the friendly name to the list.
       Pylon::String_t friendlyName = pDeviceInfo->GetFriendlyName();
       // Add a pointer to CDeviceInfo as item data so we can use it later.
       ui->cameraList->addItem( friendlyName.c_str(), QVariant::fromValue( (void *)pDeviceInfo ) );
    }

    // Select first item.
    ui->cameraList->setCurrentIndex( 0 );

    // Enable/disable controls.
    on_cameraList_currentIndexChanged( -1 );
}


// The Open Selected button for camera 1 has been clicked.
void MainDialog::on_openSelected_1_clicked()
{
    int index = ui->cameraList->currentIndex();
    if ( index < 0 )
    {
        return;
    }

    // Get the pointer to Pylon::CDeviceInfo selected.
    const Pylon::CDeviceInfo* pDeviceInfo = (const Pylon::CDeviceInfo*) ui->cameraList->itemData( index ).value<void *>();

    // Open the camera.
    InternalOpenCamera( *pDeviceInfo, 0 );
}


// The Open Selected button for camera 2 has been clicked.
void MainDialog::on_openSelected_2_clicked()
{
    int index = ui->cameraList->currentIndex();
    if ( index < 0 )
    {
        return;
    }

    // Get the pointer to Pylon::CDeviceInfo selected.
    const Pylon::CDeviceInfo* pDeviceInfo = (const Pylon::CDeviceInfo*) ui->cameraList->itemData( index ).value<void *>();

    // Open the camera.
    InternalOpenCamera( *pDeviceInfo, 1 );
}


// Enable the Open by SN button if a serial number has been entered.
void MainDialog::on_editSN_1_textEdited(const QString &arg1)
{
    ui->openBySN_1->setEnabled( ! arg1.trimmed().isEmpty() );
}


// Enable the Open by SN button if a serial number has been entered.
void MainDialog::on_editSN_2_textEdited(const QString &arg1)
{
    ui->openBySN_2->setEnabled( ! arg1.trimmed().isEmpty() );
}


// The Open by SN button for camera 1 has been clicked.
void MainDialog::on_openBySN_1_clicked()
{
    Pylon::CDeviceInfo devInfo;
    devInfo.SetSerialNumber( ui->editSN_1->text().trimmed().toStdString().c_str() );

    InternalOpenCamera( devInfo, 0 );
}


// The Open by SN button for camera 2 has been clicked.
void MainDialog::on_openBySN_2_clicked()
{
    Pylon::CDeviceInfo devInfo;
    devInfo.SetSerialNumber( ui->editSN_2->text().trimmed().toStdString().c_str() );

    InternalOpenCamera( devInfo, 1 );
}


// Enable the Open by User ID button if a user ID has been entered.
void MainDialog::on_editUserID_1_textEdited(const QString &arg1)
{
    ui->openByUserID_1->setEnabled( ! arg1.trimmed().isEmpty() );
}


// Enable the Open by User ID button if a user ID has been entered.
void MainDialog::on_editUserID_2_textEdited(const QString &arg1)
{
    ui->openByUserID_2->setEnabled( ! arg1.trimmed().isEmpty() );
}


// The Open by User ID button for camera 1 has been clicked.
void MainDialog::on_openByUserID_1_clicked()
{
    Pylon::CDeviceInfo devInfo;
    devInfo.SetUserDefinedName( ui->editUserID_1->text().trimmed().toStdString().c_str() );

    InternalOpenCamera( devInfo, 0 );
}


// The Open by User ID button for camera 2 has been clicked.
void MainDialog::on_openByUserID_2_clicked()
{
    Pylon::CDeviceInfo devInfo;
    devInfo.SetUserDefinedName( ui->editUserID_2->text().trimmed().toStdString().c_str() );

    InternalOpenCamera( devInfo, 0 );
}


// Helper function to open a CGuiCamera and update controls.
// After the camera has been opened, we adjust the controls to configure
// the camera features. Slider ranges are set and drop-down lists are filled
// with enumeration entries.
bool MainDialog::InternalOpenCamera( const Pylon::CDeviceInfo& devInfo, int cameraId )
{
    try
    {
        // Open() may throw exceptions.
        m_camera[cameraId].Open( devInfo );
    }
    catch (const Pylon::GenericException& e)
    {
        ShowWarning( QString("Could not open camera!\n") + QString( e.GetDescription() ) );

        return false;
    }

    try
    {
        // Update controls.
        UpdateCameraDialog( cameraId );
        if (cameraId == 0)
        {
            UpdateSlider( ui->exposure_1, m_camera[cameraId].GetExposureTime() );
            UpdateSliderText( ui->exposureLabel_1, m_camera[cameraId].GetExposureTime() );
            UpdateSlider( ui->gain_1, m_camera[cameraId].GetGain() );
            UpdateSliderText( ui->gainLabel_1, m_camera[cameraId].GetGain() );
            UpdateEnumeration( ui->pixelFormat_1, m_camera[cameraId].GetPixelFormat() );
            UpdateEnumeration( ui->triggerMode_1, m_camera[cameraId].GetTriggerMode() );
            UpdateEnumeration( ui->triggerSource_1, m_camera[cameraId].GetTriggerSource() );
        }
        else if (cameraId == 1)
        {
            UpdateSlider( ui->exposure_2, m_camera[cameraId].GetExposureTime() );
            UpdateSliderText( ui->exposureLabel_2, m_camera[cameraId].GetExposureTime() );
            UpdateSlider( ui->gain_2, m_camera[cameraId].GetGain() );
            UpdateSliderText( ui->gainLabel_2, m_camera[cameraId].GetGain() );
            UpdateEnumeration( ui->pixelFormat_2, m_camera[cameraId].GetPixelFormat() );
            UpdateEnumeration( ui->triggerMode_2, m_camera[cameraId].GetTriggerMode() );
            UpdateEnumeration( ui->triggerSource_2, m_camera[cameraId].GetTriggerSource() );
        }
        else
        {
            assert( false );
        }

        return true;
    }
    catch (const Pylon::GenericException& e)
    {
        PYLON_UNUSED( e );
        return false;
    }
}


// Helper function to close a CGuiCamera and update controls.
// After the camera has been closed, we disable controls to configure the camera.
// Slider ranges are reset and drop-down lists are cleared.
void MainDialog::InternalCloseCamera( int cameraId )
{
    try
    {
        m_camera[cameraId].Close();

        // Enable/disable controls.
        UpdateCameraDialog( cameraId );
    }
    catch (const Pylon::GenericException& e)
    {
        PYLON_UNUSED( e );
    }
}


// The Close button for camera 1 has been clicked.
void MainDialog::on_close_1_clicked()
{
    InternalCloseCamera( 0 );

    // Make sure to repaint the image control.
    // The actual drawing is done in paintEvent.
    ui->image_1->repaint();
}


// The Close button for camera 2 has been clicked.
void MainDialog::on_close_2_clicked()
{
    InternalCloseCamera( 1 );

    // Make sure to repaint the image control.
    // The actual drawing is done in paintEvent.
    ui->image_2->repaint();
}


// Grab a single image.
void MainDialog::on_singleShot_1_clicked()
{
    try
    {
        m_camera[0].SingleGrab();
    }
    catch (const Pylon::GenericException& e)
    {
        ShowWarning( QString( "Could not start grab!\n" ) + QString( e.GetDescription() ) );
    }
}


// Grab a single image.
void MainDialog::on_singleShot_2_clicked()
{
    try
    {
        m_camera[1].SingleGrab();
    }
    catch (const Pylon::GenericException& e)
    {
        ShowWarning( QString( "Could not start grab!\n" ) + QString( e.GetDescription() ) );
    }
}


// Start a continuous grab.
void MainDialog::on_continuous_1_clicked()
{
    try
    {
        m_camera[0].ContinuousGrab();
    }
    catch (const Pylon::GenericException& e)
    {
        ShowWarning( QString( "Could not start grab!\n" ) + QString( e.GetDescription() ) );
    }
}


// Start a continuous grab.
void MainDialog::on_continuous_2_clicked()
{
    try
    {
        m_camera[1].ContinuousGrab();
    }
    catch (const Pylon::GenericException& e)
    {
        ShowWarning( QString( "Could not start grab!\n" ) + QString( e.GetDescription() ) );
    }
}


// Stop a continuous grab.
void MainDialog::on_stop_1_clicked()
{
    try
    {
        m_camera[0].StopGrab();
    }
    catch (const Pylon::GenericException& e)
    {
        ShowWarning( QString( "Could not stop grab!\n" ) + QString( e.GetDescription() ) );
    }
}


// Stop a continuous grab.
void MainDialog::on_stop_2_clicked()
{
    try
    {
        m_camera[1].StopGrab();
    }
    catch (const Pylon::GenericException& e)
    {
        ShowWarning( QString( "Could not stop grab!\n" ) + QString( e.GetDescription() ) );
    }
}


// Called to update value of slider.
void MainDialog::UpdateSlider( QSlider* pCtrl, Pylon::IIntegerEx& integerParameter )
{
    if (pCtrl == nullptr)
    {
        qDebug() << "Invalid control ID";
        return;
    }

    if (!integerParameter.IsValid())
    {
        pCtrl->setEnabled( false );
        return;
    }

    if (integerParameter.IsReadable())
    {
        int64_t minimum = integerParameter.GetMin();
        int64_t maximum = integerParameter.GetMax();
        int64_t value = integerParameter.GetValue();

        // NOTE:
        // Possible loss of data because controls only support
        // 32-bit values while GenApi supports 64-bit values.
        pCtrl->setRange( static_cast<int>(minimum), static_cast<int>(maximum) );
        pCtrl->setValue( static_cast<int>(value) );
    }

    pCtrl->setEnabled( integerParameter.IsWritable() );
}


// Update the control with the value of a camera parameter.
void MainDialog::UpdateSliderText( QLabel *pString, Pylon::IIntegerEx& integerParameter )
{
    if (pString == NULL)
    {
        qDebug() << "Invalid control ID";
        return;
    }

    if (integerParameter.IsReadable())
    {
        // Set the value as a string in wide character format.
        pString->setText( integerParameter.ToString().c_str() );
    }
    else
    {
        pString->setText( "n/a" );
    }
    pString->setEnabled( integerParameter.IsWritable() );
}


// Stores GenApi enumeration items into CComboBox.
void MainDialog::UpdateEnumeration( QComboBox* pCtrl, Pylon::IEnumerationEx& enumParameter )
{
    if (pCtrl == NULL)
    {
        qDebug() << "Invalid control ID";
        return;
    }

    if (enumParameter.IsReadable())
    {
        // Enum entries can become invalid if the camera is reconfigured
        // so we may have to remove existing entries.
        // By iterating from the end to the beginning we don't have to adjust the
        // index when removing an entry.
        for (int index = pCtrl->count(); --index >= 0; /* empty intentionally */)
        {
            GenApi::IEnumEntry* pEntry = reinterpret_cast<GenApi::IEnumEntry*>(pCtrl->itemData( index ).value<void*>());
            if ( ! Pylon::CParameter( pEntry ).IsReadable() )
            {
                // Entry in control is not valid enum entry anymore, so we remove it.
                pCtrl->removeItem( index );
            }
        }

        // Remember the current entry so we can select it later.
        GenApi::IEnumEntry* pCurrentEntry = enumParameter.GetCurrentEntry();

        // Retrieve the list of entries.
        Pylon::StringList_t symbolics;
        enumParameter.GetSettableValues( symbolics );

        // Specify the index you want to select.
        int selectedIndex = -1;

        // Add items if not already present.
        for (GenApi::StringList_t::iterator it = symbolics.begin(), end = symbolics.end(); it != end; ++it)
        {
            const Pylon::String_t symbolic = *it;
            GenApi::IEnumEntry* pEntry = enumParameter.GetEntryByName( symbolic );
            if (pEntry != NULL && Pylon::CParameter( pEntry ).IsReadable())
            {
                // Show the display name / friendly name in the GUI.
                const QString displayName = pEntry->GetNode()->GetDisplayName().c_str();

                int index = pCtrl->findText( displayName );
                if (index == -1)
                {
                    // The entry doesn't exist. Add it to the list.
                    // Set the name in wide character format.
                    // Store the pointer for easy node access.
                    pCtrl->addItem( displayName, QVariant::fromValue( (void*) pEntry ) );
                }

                // If it is the current entry, we will select it after adding all entries.
                if (pEntry == pCurrentEntry)
                {
                    selectedIndex = index;
                }
            }
        }

        // If one index should be selected, select it in the list.
        if(selectedIndex > 0)
        {
            pCtrl->setCurrentIndex( selectedIndex );
        }
    }

    // Enable/disable control depending on the state of the enum parameter.
    // Also disable if there are no valid entries.
    pCtrl->setEnabled( enumParameter.IsWritable() && pCtrl->count() > 0 );
}


// Reset a slider control to default values.
void MainDialog::ClearSlider( QSlider* pCtrl, QLabel* pString )
{
    pCtrl->setValue( 0 );
    pCtrl->setRange( 0, 0 );
    pCtrl->setEnabled( false );

    pString->setText( "" );
}


// Called to update the enumeration in a combo box.
void MainDialog::ClearEnumeration( QComboBox* pCtrl )
{
    pCtrl->clear();
    pCtrl->setEnabled( false );
}


// This will be called in response to the NewGrabResult signal posted by
// CGuiCamera when a new grab result has been received.
// This function is called in the GUI thread so you can access GUI elements.
void MainDialog::OnNewGrabResult( int userHint )
{
    if ((userHint == 0) && m_camera[0].IsOpen())
    {
        // Make sure to repaint the image control.
        // The actual drawing is done in paintEvent.
        ui->image_1->repaint();
    }

    if ((userHint == 1) && m_camera[1].IsOpen())
    {
        // Make sure to repaint the image control.
        // The actual drawing is done in paintEvent.
        ui->image_2->repaint();
    }
}


// This overrides the paintEvent of the dialog to paint the images.
// For better performance and easy maintenance a custom control should be used.
void MainDialog::paintEvent(QPaintEvent *ev)
{
    QDialog::paintEvent(ev);

    // Repaint image of camera 1.
    if( m_camera[0].IsOpen())
    {
        QPainter painter(this);
        QRect target = ui->image_1->geometry();

        QMutexLocker locker( m_camera[0].GetBmpLock() );
        QImage image = m_camera[0].GetImage();
        QRect source = QRect(0, 0, image.width(), image.height());
        painter.drawImage(target, image, source);
    }

    // Repaint image of camera 2.
    if( m_camera[1].IsOpen())
    {
        QPainter painter(this);
        QRect target = ui->image_2->geometry();

        QMutexLocker locker( m_camera[1].GetBmpLock() );
        QImage image = m_camera[1].GetImage();
        QRect source = QRect(0, 0, image.width(), image.height());
        painter.drawImage(target, image, source);
    }
}


// This will be called in response to the DeviceRemoved signal posted by
// CGuiCamera when the camera has been disconnected.
// This function is called in the GUI thread so you can access GUI elements.
void MainDialog::OnDeviceRemoved( int userHint )
{
    InternalCloseCamera( userHint );

    repaint();

    ShowWarning( "A camera device has been disconnected." );

    // Scan for camera devices and refill the list of devies.
    on_scanButton_clicked();
}


// This will be called in response to the NodeUpdated signal posted by
// CGuiCamera when a camera parameter changes its attributes or value.
// This function is called in the GUI thread so you can access GUI elements.
void MainDialog::OnNodeUpdated( int userHint, GenApi::INode* pNode )
{
    // Display the current values.
    if ((userHint == 0) && m_camera[0].IsOpen() && (!m_camera[0].IsCameraDeviceRemoved()))
    {
        if (m_camera[userHint].GetExposureTime().GetNode() == pNode)
        {
            UpdateSlider( ui->exposure_1, m_camera[userHint].GetExposureTime() );
            UpdateSliderText( ui->exposureLabel_1, m_camera[userHint].GetExposureTime() );
        }

        if (m_camera[userHint].GetGain().IsValid() && (m_camera[userHint].GetGain().GetNode() == pNode) )
        {
            UpdateSlider( ui->gain_1, m_camera[userHint].GetGain() );
            UpdateSliderText( ui->gainLabel_1, m_camera[userHint].GetGain() );
        }

        if (m_camera[userHint].GetPixelFormat().GetNode() == pNode)
        {
            UpdateEnumeration( ui->pixelFormat_1, m_camera[userHint].GetPixelFormat() );
        }

        if (m_camera[userHint].GetTriggerMode().GetNode() == pNode)
        {
            UpdateEnumeration( ui->triggerMode_1, m_camera[userHint].GetTriggerMode() );
        }

        if (m_camera[userHint].GetTriggerSource().GetNode() == pNode)
        {
            UpdateEnumeration( ui->triggerSource_1, m_camera[userHint].GetTriggerSource() );
        }
    }
    else if ((userHint == 1) && m_camera[1].IsOpen() && (!m_camera[1].IsCameraDeviceRemoved()))
    {
        if (m_camera[userHint].GetExposureTime().GetNode() == pNode)
        {
            UpdateSlider( ui->exposure_2, m_camera[userHint].GetExposureTime() );
            UpdateSliderText( ui->exposureLabel_2, m_camera[userHint].GetExposureTime() );
        }

        if (m_camera[userHint].GetGain().IsValid() && (m_camera[userHint].GetGain().GetNode() == pNode) )
        {
            UpdateSlider( ui->gain_2, m_camera[userHint].GetGain() );
            UpdateSliderText( ui->gainLabel_2, m_camera[userHint].GetGain() );
        }

        if (m_camera[userHint].GetPixelFormat().GetNode() == pNode)
        {
            UpdateEnumeration( ui->pixelFormat_2, m_camera[userHint].GetPixelFormat() );
        }

        if (m_camera[userHint].GetTriggerMode().GetNode() == pNode)
        {
            UpdateEnumeration( ui->triggerMode_2, m_camera[userHint].GetTriggerMode() );
        }

        if (m_camera[userHint].GetTriggerSource().GetNode() == pNode)
        {
            UpdateEnumeration( ui->triggerSource_2, m_camera[userHint].GetTriggerSource() );
        }
    }
}


// This will be called in response to the StateChanged signal posted by
// CGuiCamera when the grab is started or stopped.
// This function is called in the GUI thread so you can access GUI elements.
void MainDialog::OnStateChanged( int userHint, bool isGrabbing )
{
    PYLON_UNUSED( isGrabbing );

    // Enable/disable Start/Stop buttons
    UpdateCameraDialog( userHint );
}


// This will be called when the Exposure Time slider is changed.
void MainDialog::on_exposure_1_valueChanged(int value)
{
    m_camera[0].GetExposureTime().TrySetValue( value );
}


// This will be called when the Exposure Time slider is changed.
void MainDialog::on_exposure_2_valueChanged(int value)
{
    m_camera[1].GetExposureTime().TrySetValue( value );
}


// This will be called when the Gain slider is changed.
void MainDialog::on_gain_1_valueChanged(int value)
{
    m_camera[0].GetGain().TrySetValue( value );
}


// This will be called when the Gain slider is changed.
void MainDialog::on_gain_2_valueChanged(int value)
{
    m_camera[1].GetGain().TrySetValue( value );
}


// This will be called when the setting of the Pixel Format drop-down list changes.
void MainDialog::on_pixelFormat_1_currentIndexChanged(int index)
{
    if(index == -1)
    {
        return;
    }

    QVariant userData = ui->pixelFormat_1->itemData( index );
    GenApi::IEnumEntry* pEntry = reinterpret_cast<GenApi::IEnumEntry*>( userData.value<void*>() );
    m_camera[0].GetPixelFormat().SetValue( pEntry->GetSymbolic() );
}


// This will be called when the setting of the Pixel Format drop-down list changes.
void MainDialog::on_pixelFormat_2_currentIndexChanged(int index)
{
    if(index == -1)
    {
        return;
    }

    QVariant userData = ui->pixelFormat_2->itemData( index );
    GenApi::IEnumEntry* pEntry = reinterpret_cast<GenApi::IEnumEntry*>( userData.value<void*>() );
    m_camera[1].GetPixelFormat().SetValue( pEntry->GetSymbolic() );
}


// This will be called when the setting of the Trigger Source drop-down list changes.
void MainDialog::on_triggerMode_1_currentTextChanged(const QString &arg1)
{
    m_camera[0].GetTriggerMode().TrySetValue( arg1.toStdString().c_str() );
}


// This will be called when the setting of the Trigger Source drop-down list changes.
void MainDialog::on_triggerMode_2_currentTextChanged(const QString &arg1)
{
    m_camera[1].GetTriggerMode().TrySetValue( arg1.toStdString().c_str() );
}


// This will be called when the setting of the Trigger Source drop-down list changes.
void MainDialog::on_triggerSource_1_currentTextChanged(const QString &arg1)
{
    m_camera[0].GetTriggerSource().TrySetValue( arg1.toStdString().c_str() );
}


// This will be called when the setting of the Trigger Source drop-down list changes.
void MainDialog::on_triggerSource_2_currentTextChanged(const QString &arg1)
{
    m_camera[1].GetTriggerSource().TrySetValue( arg1.toStdString().c_str() );
}


// This will be called when the Software Trigger button is clicked.
void MainDialog::on_softwareTrigger_1_clicked()
{
    m_camera[0].ExecuteSoftwareTrigger();
}


// This will be called when the Software Trigger button is clicked.
void MainDialog::on_softwareTrigger_2_clicked()
{
    m_camera[1].ExecuteSoftwareTrigger();
}


// This will be called when the state of the Invert Pixel checkbox changes.
void MainDialog::on_invertPixel_1_toggled(bool checked)
{
    m_camera[0].SetInvertImage( checked );
}


// This will be called when the state of the Invert Pixel checkbox changes.
void MainDialog::on_invertPixel_2_toggled(bool checked)
{
    m_camera[1].SetInvertImage( checked );
}


// Enable/disable buttons when the user selects a camera in the camera box.
void MainDialog::on_cameraList_currentIndexChanged(int index)
{
    PYLON_UNUSED( index );

    // The combo box affects both open buttons.
    UpdateCameraDialog( 0 );
    UpdateCameraDialog( 1 );
}
