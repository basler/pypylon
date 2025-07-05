QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # Disables all the APIs before Qt 6.0.0 because they are deprecated.


SOURCES += \
    guicamera.cpp \
    main.cpp \
    maindialog.cpp

HEADERS += \
    guicamera.h \
    maindialog.h

FORMS += \
    maindialog.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

# Add Pylon
win32 {
    INCLUDEPATH += "$$(PYLON_ROOT)/include"
    contains(QMAKE_TARGET.arch, x86_64) {
        LIBS += -L"$$(PYLON_ROOT)/lib/x64"
    } else {
        LIBS += -L"$$(PYLON_ROOT)/lib/win32"
    }
}
linux {
    INCLUDEPATH += "$$(PYLON_ROOT)/include"
    LIBS += -L"$$(PYLON_ROOT)/lib" -lpylonbase -lpylonutility -lGenApi_gcc_v3_1_Basler_pylon -lGCBase_gcc_v3_1_Basler_pylon
}
macx {
    QMAKE_RPATHDIR += "/Library/Frameworks/"
    CONFIG-=app_bundle
    INCLUDEPATH += "/Library/Frameworks/pylon.framework/Headers/GenICam"
    QMAKE_CXXFLAGS += -F"/Library/Frameworks"
    LIBS += -F"/Library/Frameworks" -framework pylon
}
