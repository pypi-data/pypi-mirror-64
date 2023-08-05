# -*- coding: utf-8 -*-
#
# codimension - graphics python two-way code editor and analyzer
# Copyright (C) 2020  Sergey Satskiy <sergey.satskiy@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""Codimension ide introspection plugin implementation"""


from distutils.version import StrictVersion
from plugins.categories.wizardiface import WizardInterface
from ui.qt import QTimer, QApplication, QCursor, Qt
from ui.labels import StatusBarFramedLabel
import psutil

UPDATE_INTERVAL = 10000     # 10 sec


class SysInfoPlugin(WizardInterface):

    """Codimension system info plugin"""

    def __init__(self):
        WizardInterface.__init__(self)
        self.__cpuWidget = None
        self.__memoryWidget = None
        self.__timer = None

    @staticmethod
    def isIDEVersionCompatible(ideVersion):
        """Checks if the IDE version is compatible with the plugin"""
        return StrictVersion(ideVersion) >= StrictVersion('4.7.1')

    def activate(self, ideSettings, ideGlobalData):
        """Activates the plugin"""
        WizardInterface.activate(self, ideSettings, ideGlobalData)

        # To have a bit time before the first update
        self.__getCPU()

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            statusBar = self.ide.mainWindow.statusBar()

            self.__timer = QTimer(self)
            self.__timer.setSingleShot(True)
            self.__timer.timeout.connect(self.__update)
            self.__timer.start(UPDATE_INTERVAL)

            self.__cpuWidget = StatusBarFramedLabel(parent=statusBar)
            self.__cpuWidget.setToolTip('Current system-wide CPU utilization')
            self.__memoryWidget = StatusBarFramedLabel(parent=statusBar)
            self.__memoryWidget.setToolTip('System memory usage')

            statusBar.addPermanentWidget(self.__cpuWidget)
            statusBar.addPermanentWidget(self.__memoryWidget)

            self.__update()
        except:
            QApplication.restoreOverrideCursor()
            raise
        QApplication.restoreOverrideCursor()

    def deactivate(self):
        """Deactivates the plugin"""
        statusBar = self.ide.mainWindow.statusBar()

        if self.__timer is not None:
            if self.__timer.isActive():
                self.__timer.stop()
            self.__timer.timeout.disconnect(self.__update)
            self.__timer.deleteLater()
            self.__timer = None

        if self.__cpuWidget is not None:
            statusBar.removeWidget(self.__cpuWidget)
            self.__cpuWidget.deleteLater()
            self.__cpuWidget = None

        if self.__memoryWidget is not None:
            statusBar.removeWidget(self.__memoryWidget)
            self.__memoryWidget.deleteLater()
            self.__memoryWidget = None

        WizardInterface.deactivate(self)

    def getConfigFunction(self):
        """Provides a plugun configuration function"""
        return None

    def populateMainMenu(self, parentMenu):
        """Populates the main menu"""
        del parentMenu      # unused argument

    def populateFileContextMenu(self, parentMenu):
        """Populates the file context menu"""
        del parentMenu      # unused argument

    def populateDirectoryContextMenu(self, parentMenu):
        """Populates the directory context menu"""
        del parentMenu      # unused argument

    def populateBufferContextMenu(self, parentMenu):
        """Populates the editing buffer context menu"""
        del parentMenu

    def __update(self):
        """Updates the UI"""
        self.__cpuWidget.setText(self.__getCPU())
        self.__memoryWidget.setText(self.__getMemory())
        self.__timer.start(UPDATE_INTERVAL)

    @staticmethod
    def __getCPU():
        """Provides the CPU usage percent as text"""
        txt = '%d%%' % psutil.cpu_percent(interval=0)
        return 'CPU: ' + txt.rjust(3)

    @staticmethod
    def __getMemory():
        """Provides the memory usage percent as text"""
        txt = '%d%%' % psutil.virtual_memory().percent
        return 'Mem: ' + txt.rjust(3)

