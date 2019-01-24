#-------------------------------------------------
#
# Project created by QtCreator 2017-02-16T15:41:08
#
#-------------------------------------------------

QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = RobotOnSwingSimulator
TEMPLATE = app


SOURCES += main.cpp\
    controlWindow.cpp \
    displayWindow.cpp \
    twoVector.cpp

HEADERS  += \
    controlWindow.h \
    displayWindow.h \
    twoVector.h

FORMS    += \
    displayWindow.ui \
    controlWindow.ui
