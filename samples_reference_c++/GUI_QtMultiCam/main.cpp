/*
    Note: Before getting started, Basler recommends reading the "Programmer's Guide" topic
    in the pylon C++ API documentation delivered with pylon.
    If you are upgrading to a higher major version of pylon, Basler also
    strongly recommends reading the "Migrating from Previous Versions" topic in the pylon C++ API documentation.

    This sample illustrates the use of a Qt GUI together with the pylon C++ API to enumerate the attached cameras, to
    configure a camera, to start and stop the grab and to display grabbed images.
    It shows how to use GUI controls to display and modify camera parameters.
*/
#include "maindialog.h"
#include <QApplication>
#include <pylon/PylonIncludes.h>


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);

    Pylon::PylonAutoInitTerm pylonInit;

    MainDialog w;
    w.show();
    return a.exec();
}
