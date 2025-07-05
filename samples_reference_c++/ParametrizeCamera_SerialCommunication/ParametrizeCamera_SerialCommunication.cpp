// ParametrizeCamera_SerialCommunication.cpp
/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample program demonstrates the use of the UART (asynchronous serial communication) feature
    that is available on some camera models, e.g., ace 2 Pro cameras. This allows you to establish 
    serial communication between a host and an external device through the camera.
*/

// Include files to use the pylon API.
#include <pylon/PylonIncludes.h>

// Include file to use pylon universal instant camera parameters.
#include <pylon/BaslerUniversalInstantCamera.h>

// Include vector for transmitting/receiving data buffers.
#include <vector>

// Namespace for using pylon objects.
using namespace Pylon;

// Namespace for using pylon universal instant camera parameters.
using namespace Basler_UniversalCameraParams;

// Namespace for using GenApi objects.
using namespace GenApi;

// Namespace for using cout.
using namespace std;

// Data type for storing bytes for serial transmission.
typedef vector<uint8_t> SerialDataBuffer_t;


// Transmit data:
// -----------------
//
// 1. Write the data to BslSerialTransferBuffer (for GigE, you need to write multiples of 4 bytes).
// 2. Write the real (not the padded) length (in bytes) of data to BslSerialTransferLength.
// 3. Execute BslSerialTransmit.
// 4. Wait for BslSerialTxFifoEmpty to become true before further transmissions.
// 5. Repeat until all data has been transmitted.

void SerialTransmit( CBaslerUniversalInstantCamera &camera, const SerialDataBuffer_t &transmitData )
{
    // Get the max buffer size for transmission.
    const size_t max_tx_size = static_cast<size_t>(camera.BslSerialTransferBuffer.GetLength());

    SerialDataBuffer_t::const_iterator currentPosition = transmitData.begin();
    while (currentPosition != transmitData.end())
    {
        // Calculate the number of bytes that can be transferred at once.
        size_t bytesToSend = static_cast<size_t>(transmitData.end() - currentPosition);
        size_t transferLength = min( bytesToSend, max_tx_size );

        // Create and fill transfer buffer with the calculated length.
        SerialDataBuffer_t dataBuffer( currentPosition, currentPosition + transferLength );

        // As GigE devices only allow multiples of 4 bytes for data transfer, add padding to the buffer if necessary.
        size_t paddedLength = transferLength + (4 - (transferLength % 4)) % 4;
        dataBuffer.resize( paddedLength );

        // Write padded data to the camera buffer and set transfer length to the unpadded value.
        camera.BslSerialTransferBuffer.Set( dataBuffer.data(), paddedLength );
        camera.BslSerialTransferLength.SetValue( transferLength );

        // Start the transmission.
        camera.BslSerialTransmit.Execute();
        currentPosition += transferLength;

        // Poll every 100 ms until FIFO is empty.
        size_t count = 0;
        while (!camera.BslSerialTxFifoEmpty.GetValue() && (count++ < 100))
        {
            WaitObject::Sleep( 1 );
        }

        // Check for overflow status (updated by the transmit command).
        if (camera.BslSerialTxFifoOverflow.GetValue())
        {
            cerr << "WARNING: Serial transmit overflow!" << endl;
        }
    }
}


// Receive data:
// -------------
//
// 1. Execute BslSerialReceive.
// 2. Check for flags in BslSerialRxFifoOverflow, BslSerialRxParityError, and BslSerialRxStopBitError.
// 3. Read BslSerialTransferLength to obtain the length of received data.
// 4. Read BslSerialTransferLength bytes from BslSerialTransferBuffer (for GigE you need to read multiples of 4 bytes).
// 5. Repeat if BslSerialTransferLength was not 0.

SerialDataBuffer_t SerialReceive( CBaslerUniversalInstantCamera &camera )
{
    SerialDataBuffer_t receiveData; // Buffer for receiving data.
    size_t bytesReceived = 0;       // Number of bytes used by the complete transmission.
    size_t transferLength = 0;      // Number of bytes received at once.
    do
    {
        // Receive data from FIFO.
        camera.BslSerialReceive.Execute();

        // Check for overflow of receive FIFO. If this is set, data was lost!
        if (camera.BslSerialRxFifoOverflow.GetValue())
        {
            cerr << "WARNING: Receive overflow detected!" << endl;
        }

        // Check for a receive parity error. If this is set, data may be incorrect!
        if (camera.BslSerialRxParityError.GetValue())
        {
            cerr << "WARNING: Parity error in received data stream detected!" << endl;
        }

        // Check for a stop bit error. If this is set, data may be incorrect!
        // Also, this bit is normally set when a break condition occurred.
        if (camera.BslSerialRxStopBitError.GetValue())
        {
            cerr << "WARNING: Stop bit error in received data stream detected!" << endl;
        }

        // Check how many bytes where received and fetch the data from the transfer buffer.
        transferLength = static_cast<size_t>(camera.BslSerialTransferLength.GetValue());
        if (transferLength)
        {
            // GigE devices only allow multiples of 4 bytes for data transfer. Add padding to the buffer if necessary.
            size_t paddedLength = transferLength + (4 - (transferLength % 4)) % 4;
            receiveData.resize( bytesReceived + paddedLength );

            // Read padded data but only count unpadded length.
            camera.BslSerialTransferBuffer.Get( &receiveData[bytesReceived], paddedLength );
            bytesReceived += transferLength;

        }
    } while (transferLength);

    // Finally, remove padding from received data.
    receiveData.resize( bytesReceived );

    return receiveData;
}


int main( int /*argc*/, char* /*argv*/[] )
{
    // The exit code of the sample application.
    int exitCode = 0;

    // Before using any pylon methods, the pylon runtime must be initialized. 
    PylonInitialize();

    try
    {
        // Create an instant camera object with the first camera device found.
        CBaslerUniversalInstantCamera camera( CTlFactory::GetInstance().CreateFirstDevice() );

        // Print the model name of the camera.
        cout << "Using device: " << camera.GetDeviceInfo().GetModelName() << endl << endl;

        cout << "Opening camera...";

        // Open the camera.
        camera.Open();

        cout << "done" << endl;

        // Check whether the device supports asynchronous serial communication.
        if (!camera.BslSerialReceive.IsWritable() || !camera.BslSerialTransmit.IsWritable())
        {
            throw RUNTIME_EXCEPTION( "The device doesn't support asynchronous serial communication." );
        }

        // === Configure I/O ===

        // Change this to 'false' to use the camera's digital I/O lines for communication.
        // This requires a UART device to be attached to the camera. Leave the switch
        // 'true' to demonstrate the UART in loopback mode.
        const bool loopback = true;
        if (loopback)
        {
            // Loopback: Simply use SerialTx as source for receive.
            cout << "Configure loopback for serial communication...";

            camera.BslSerialRxSource = BslSerialRxSource_SerialTx;

            cout << "done" << endl;
        }
        else
        {
            // On ace 2 cameras, lines 2 and 3 are GPIO lines.
            // Do not use the opto-coupled input for UART communications!
            cout << "Configure GPIO lines for serial communication..." << endl;

            // Use line 2 as TX (Output).
            camera.LineSelector = LineSelector_Line2;
            camera.LineMode = LineMode_Output;
            camera.LineSource = LineSource_SerialTx;

            // Use line 3 as RX (Input).
            camera.LineSelector = LineSelector_Line3;
            camera.LineMode = LineMode_Input;

            camera.BslSerialRxSource = BslSerialRxSource_Line3;

            cout << "done" << endl;
        }

        // === Configure the serial communication module (115200 baud - 8n1) ===
        cout << "Configure UART to 115200 8N1...";
        camera.BslSerialBaudRate = BslSerialBaudRate_Baud115200;
        camera.BslSerialNumberOfDataBits = BslSerialNumberOfDataBits_Bits8;
        camera.BslSerialParity = BslSerialParity_None;
        camera.BslSerialNumberOfStopBits = BslSerialNumberOfStopBits_Bits1;
        cout << "done" << endl;

        // === Transmit data ===
        const std::string message( "For documentation, see: https://docs.baslerweb.com/serial-communication" );
        const SerialDataBuffer_t transmitData( message.begin(), message.end() );

        cout << "Transmit: " << "'" << message << "'" << endl;
        SerialTransmit( camera, transmitData );
        cout << "Transmit: done!" << endl;

        // === Receive data ===
        // Note: For loopback the message transmitted was too long and the RX-FIFO is in overflow condition!
        cout << "Receive: Starting..." << endl;
        if (loopback)
        {
            cout << "Note: In loopback mode, the message is too long for the receive FIFO and an overflow message will appear! \n";
            cout << "Note: The received message seen here will be truncated!" << endl;
        }
        SerialDataBuffer_t receivedData = SerialReceive( camera );
        cout << "Receive: " << "'" << std::string( receivedData.begin(), receivedData.end() ) << "'" << endl;

        // === Transmit & check break condition ===
        cout << "Receive break: " << camera.BslSerialRxBreak.GetValue() << endl;
        camera.BslSerialRxBreakReset.Execute();

        cout << "Set break condition...";
        camera.BslSerialTxBreak.SetValue( true );
        WaitObject::Sleep( 10 );
        camera.BslSerialTxBreak.SetValue( false );
        cout << "done!" << endl;

        cout << "Receive break: " << camera.BslSerialRxBreak.GetValue() << endl;
        camera.BslSerialRxBreakReset.Execute();

        // After a break, the receive FIFO contains errors, so flush the FIFO.
        cout << "Note: After a break condition framing error flags will probably be set!" << endl;
        SerialReceive( camera );

        // Close the camera.
        camera.Close();

    }
    catch (const GenericException &e)
    {
        // Error handling.
        cerr << "An exception occurred." << endl
            << e.GetDescription() << endl;
        exitCode = 1;
    }

    // Comment the following two lines to disable waiting on exit.
    cerr << endl << "Press enter to exit." << endl;
    while (cin.get() != '\n');

    // Releases all pylon resources. 
    PylonTerminate();

    return exitCode;
}
