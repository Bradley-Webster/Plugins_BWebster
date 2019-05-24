# Context menu option to create new sequences from selected Clips in the Bin View.
# If Clips are named as Stereo left and right then one sequence will be created with left and right tagged tracks.

from PySide2 import QtCore, QtGui, QtWidgets

Signal = QtCore.Signal

import hiero.core

import re
import subprocess as sub
import os
import sys
import Queue as queue

from threading import Thread
from bb_python.gui.Style import *
from bb_python.gui.Widget import *

import time
from datetime import datetime
import threading
from bb_python.gui.MainWindow import BlueBoltWindow

import bundleinterface.bundleMakerUI as BdMkUI
import bundlemakerclass.beputils as bepUtils

import PyOpenColorIO as OCIO

import trace
import version
version_str = version.getVersion()

class InputPlatePublishAction(QtWidgets.QAction):

    def __init__(self):
        QtWidgets.QAction.__init__(self, "Batch Publish", None)

        self.triggered.connect(self.doit)
        hiero.core.events.registerInterest((hiero.core.events.EventType.kShowContextMenu, hiero.core.events.EventType.kBin), self.eventHandler)
        hiero.core.events.registerInterest(hiero.core.events.EventType.kSelectionChanged, self.eventHandler)

    class PublishPlatesWindow(BlueBoltWindow):
        def loadConfig(self):
            global batch_config
            batch_config = {}
            plugin_paths = os.environ['HIERO_PLUGIN_PATH'].split(":")
            config_files = []
            for plugin_location in reversed(plugin_paths):
                config_files.append(os.path.join(plugin_location, "config/batch_config.py"))

            for config_file in config_files:
                if os.path.exists(config_file):
                    print config_file
                    execfile(config_file)

            self.batch_config = batch_config
            self.discipline = self.batch_config["default"].split("/")[0]
            self.bundleType = self.batch_config["default"].split("/")[1]
            self.batch_widgets = self.batch_config['definitions'][self.discipline][self.bundleType]['widgets']

        def disciplineChanged(self):
            self.discipline = self.disciplineCombo.currentText()
            self.bundleTypeCombo.clear()
            for bt in self.batch_config['definitions'][self.discipline].keys():
                self.bundleTypeCombo.addItem(bt)

        def bundleTypeChanged(self):
            self.clearPublishWidgets()
            self.bundleType = self.bundleTypeCombo.currentText()

            self.batch_widgets = self.batch_config['definitions'][self.discipline][self.bundleType]['widgets']
            self.loadBundleType()
            self.setlabels()

        def __init__(self, selected, parent=None, title="Batch Publish " + version_str, style=BlueBoltDarkStyle):
            super(InputPlatePublishAction.PublishPlatesWindow, self).__init__(title, style, parent)
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            self.loadConfig()
            self.selection = selected
            self.setWindowFlags(QtCore.Qt.Window)

            self.resize(900, 500)

            self.setWindowOpacity(1.0)
            self.centralFrame = QtWidgets.QFrame()
            self.centralFrame.setObjectName('centralFrame')

            self.centralFrame.setStyleSheet("QFrame#centralFrame {border:1px solid rgba(0,0,0,0); background-color:rgba(56,56,56,255)}")

            self.setCentralWidget(self.centralFrame)

            self.shots_deets = {}
            self.groupLayout = QtWidgets.QFormLayout()

            for select in self.selection:
                binChain = [select.parentBin()]
                while "parentBin" in dir(binChain[0]):
                    binChain.insert(0, binChain[0].parentBin())

                path = select.activeItem().mediaSource().fileinfos()[0].filename()
                bundle_name = binChain[5].name()
                shot = binChain[4].name()
                sequence = binChain[3].name()
                in_colorSpace = self.getCS(path % select.activeItem().mediaSource().fileinfos()[0].startFrame())

                if shot not in self.shots_deets.keys():
                    self.shots_deets[shot] = {}
                if 'bundle_names' not in self.shots_deets[shot].keys():
                    self.shots_deets[shot]['bundle_names'] = {}
                self.shots_deets[shot]['bundle_names'][bundle_name] = {"path": path, "shot": shot, "sequence": sequence, "bundle_name": bundle_name, "colorspace": in_colorSpace, }

            horizontalFrame = QtWidgets.QFrame()

            horizontalFrame.setObjectName('defFrame')
            horizontalFrame.setStyleSheet("QFrame#defFrame {border:1px solid rgba(0,0,0,255); background-color:rgba(80,80,80,255)}")
            horizontalLayout = QtWidgets.QHBoxLayout()

            horizontalFrame.setLayout(horizontalLayout)
            horizontalLayout.setSpacing(-1)
            horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            horizontalLayout.addStretch()
            horizontalLayout.addWidget(QtWidgets.QLabel("Batch publish with:"))

            self.disciplineCombo = QtWidgets.QComboBox()
            self.disciplineCombo.setMinimumWidth(100)
            for d in self.batch_config['definitions'].keys():
                self.disciplineCombo.addItem(d)
            self.disciplineCombo.setCurrentIndex(self.disciplineCombo.findText(self.discipline))
            self.disciplineCombo.currentIndexChanged.connect(self.disciplineChanged)

            self.bundleTypeCombo = QtWidgets.QComboBox()
            self.bundleTypeCombo.setMinimumWidth(100)
            for bt in self.batch_config['definitions'][self.discipline].keys():
                self.bundleTypeCombo.addItem(bt)

            self.bundleTypeCombo.setCurrentIndex(self.bundleTypeCombo.findText(self.bundleType))
            self.bundleTypeCombo.currentIndexChanged.connect(self.bundleTypeChanged)

            horizontalLayout.addWidget(self.disciplineCombo)
            horizontalLayout.addWidget(self.bundleTypeCombo)
            self.groupLayout.addWidget(horizontalFrame)

            self.collapsersFrame = QtWidgets.QFrame()

            self.collapsersFrame.setObjectName('collapsersFrame')
            self.collapsersFrame.setStyleSheet("QFrame#collapsersFrame {border:1px solid rgba(0,0,0,255); background-color:rgba(80,80,80,255)}")

            self.collapsersFrame.setObjectName('collapsersFrame')

            self.scrolly = QtWidgets.QScrollArea()
            self.scrolly.setFrameShape(QtWidgets.QFrame.NoFrame)
            self.scrolly.setFrameShadow(QtWidgets.QFrame.Plain)
            self.scrolly.setWidgetResizable(True)
            self.scrolly.setWidget(self.collapsersFrame)

            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(1)
            sizePolicy.setHeightForWidth(self.scrolly.sizePolicy().hasHeightForWidth())
            self.scrolly.setSizePolicy(sizePolicy)
            self.groupLayout.addWidget(self.scrolly)

            self.collapsers = QtWidgets.QFormLayout()
            self.collapsersFrame.setLayout(self.collapsers)

            self.loadBundleType()

            self.progressBar = QtWidgets.QProgressBar()
            self.progressBar.setRange(0, 100)
            self.progressBar.setValue(0)
            self.progressBar.setVisible(False)
            self.groupLayout.addWidget(self.progressBar)

            self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)
            self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setText("Publish")
            self.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setAutoDefault(True)
            self.buttonBox.accepted.connect(self.publish)
            self.buttonBox.rejected.connect(self.close)
            self.groupLayout.addWidget(self.buttonBox)

            # self.layout.addWidget(self.groupBox)
            self.centralFrame.setLayout(self.groupLayout)
            self.setlabels()
            QtWidgets.QApplication.restoreOverrideCursor()

        def clearPublishWidgets(self):
            if hasattr(self, "collapsers"):
                for i in reversed(range(self.collapsers.count())):
                    self.collapsers.itemAt(i).widget().setParent(None)

        def loadBundleType(self):

            self.buttonFrame = QtWidgets.QFrame()
            buttonLayout = QtWidgets.QHBoxLayout()
            self.buttonFrame.setLayout(buttonLayout)
            self.buttonFrame.setStyleSheet("QFrame {border-width:0px; background-color:rgba(80,80,80,255)}")
            buttonLayout.setSpacing(-1)
            buttonLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
            self.expandbutton = QtWidgets.QPushButton('Expand All', self)
            self.expandbutton.clicked.connect(self.toggleAll)
            buttonLayout.addWidget(self.expandbutton)
            buttonLayout.addStretch()
            for batch_widget in self.batch_widgets:
                if batch_widget["type"] == "checkbox":
                    label = batch_widget.get("label")
                    value = batch_widget.get("value")
                    name = batch_widget.get("name")
                    if value is True:
                        button = QtWidgets.QPushButton(label + ' None', self)
                    else:
                        button = QtWidgets.QPushButton(label + " All", self)
                    button.name = name
                    button.clicked.connect(self.check_all_or_none)
                    buttonLayout.addWidget(button)

            self.collapsers.addWidget(self.buttonFrame)
            self.collapsers.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

            self.collapse_widgets = []

            shots_deet_keys = self.shots_deets.keys()
            shots_deet_keys.sort()

            for key in shots_deet_keys:

                collapser = BBCollapseFrame()
                collapser.centreWidget.setObjectName('centreWidget')
                collapser.centreWidget.setStyleSheet("QFrame#centreWidget {border:1px solid rgba(0,0,0,255); background-color:rgba(100,100,100,255)}")
                self.shots_deets[key]['collapser'] = collapser

                shots_deets_key_keys = self.shots_deets[key]['bundle_names'].keys()
                shots_deets_key_keys.sort()
                for key2 in shots_deets_key_keys:

                    if type(self.shots_deets[key]['bundle_names'][key2]) != dict:
                        break
                    horizontalFrame = QtWidgets.QFrame()
                    horizontalFrame.setObjectName('horizontalFrame2')
                    horizontalLayout = QtWidgets.QHBoxLayout()

                    if key2 != shots_deets_key_keys[0]:
                        horizontalFrame.setStyleSheet("QFrame#horizontalFrame2 {border-width:1px 0px 0px 0px; border-color:rgba(56,56,56,255); background-color:rgba(100,100,100,255)}")
                    else:
                        horizontalFrame.setStyleSheet("QFrame#horizontalFrame2 {border-width:0px; background-color:rgba(100,100,100,255)}")

                    horizontalFrame.setLayout(horizontalLayout)
                    horizontalFrame.setMinimumSize(QtCore.QSize(400, 45))
                    horizontalLayout.setSpacing(-1)

                    cs = self.shots_deets[key]['bundle_names'][key2]['colorspace']
                    bn = self.shots_deets[key]['bundle_names'][key2]['bundle_name']
                    buzzwords = {
                        'in_colorSpace': cs,
                        'bundleName': bn
                    }

                    for batch_widget in self.batch_widgets:
                        if batch_widget['type'] == "text":
                            label = batch_widget.get("label")
                            value = batch_widget.get("value")
                            name = batch_widget.get("name")
                            lineEdit = QtWidgets.QLineEdit(self.solveVar(value, buzzwords))
                            lineEdit.setStyleSheet("QLineEdit {border:1px solid rgba(0,0,0,255); background-color:rgba(56,56,56,255)}")
                            self.shots_deets[key]['bundle_names'][key2][name] = lineEdit
                            l = QtWidgets.QLabel(label)
                            horizontalLayout.addWidget(l)
                            horizontalLayout.addWidget(lineEdit)
                        if batch_widget['type'] == "checkbox":
                            label = batch_widget.get("label")
                            value = batch_widget.get("value")
                            name = batch_widget.get("name")
                            check = BBCheckBox(label)
                            if type(value) == str:
                                value = self.solveVar(value, buzzwords)
                                if value == "false" or value == "False":
                                    check.setChecked(False)
                                else:
                                    check.setChecked(True)
                            else:
                                check.setChecked(value)
                            check.stateChanged.connect(self.setlabels)
                            self.shots_deets[key]['bundle_names'][key2][name] = check
                            horizontalLayout.addWidget(check)
                        if batch_widget['type'] == "combobox":
                            label = batch_widget.get("label")
                            value = batch_widget.get("value")
                            values = batch_widget.get("values")
                            name = batch_widget.get("name")

                            l = QtWidgets.QLabel(label)
                            horizontalLayout.addWidget(l)
                            dropdown = QtWidgets.QComboBox()
                            dropdown.setStyleSheet("QComboBox {border:1px solid rgba(0,0,0,255); background-color:rgba(56,56,56,255)} QComboBox QListView {border:1px solid rgba(0,0,0,255); background-color:rgba(56,56,56,255)}")
                            self.shots_deets[key]['bundle_names'][key2][name] = dropdown

                            for v in values:
                                dropdown.addItem(self.solveVar(v, buzzwords))
                            dropdown.setCurrentIndex(dropdown.findText(self.solveVar(value, buzzwords)))
                            dropdown.currentIndexChanged.connect(self.setlabels)

                            horizontalLayout.addWidget(dropdown)

                    horizontalLayout.setStretch(1, 40)
                    collapser.centreWidget.layout().addWidget(horizontalFrame)

                self.collapse_widgets.append(collapser)

                self.collapsers.addWidget(collapser)

        def solveVar(self, var, buzzwords={}):
            if var and var != "":
                for buzzword in buzzwords.keys():
                    buzzword_search = "<%s>" % buzzword
                    buzzword_search = str(buzzword_search)
                    var = var.replace(buzzword_search, buzzwords[buzzword])

                matches = re.findall("<\$\w*>", var)

                for match in matches:
                    env = os.environ.get(match[2:-1])
                    if env:
                        var = var.replace(str(match), env)

            return var

        def getAllCS(self):
            config = OCIO.GetCurrentConfig()
            colorspaces = []
            for cs in config.getColorSpaces():
                colorspaces.append(cs.getName())
            return colorspaces

        def getCS(self, path):
            config = OCIO.GetCurrentConfig()
            colorSpaceNames = [cs.getName() for cs in config.getColorSpaces()]
            color = None

            file = path.split('/')[-1]

            for colorspaces in colorSpaceNames:
                if file.find(colorspaces) > -1:
                    color = colorspaces

            if color:
                return color
            else:
                levelSolver = bepUtils.solveLevelConfig()
                defaultCSFile = levelSolver.getDefaultFile('tools', 'config/defaultColorSpaces.py')
                global defaultColorSpaces
                execfile(defaultCSFile)
                ext = os.path.splitext(path)[1][1:]
                if ext in defaultColorSpaces.keys():
                    return defaultColorSpaces[ext]
                else:
                    print ""

        def setlabels(self):

            for sht in self.shots_deets.keys():
                checkbox_counts = {}
                combo_values = {}
                for batch_widget in self.batch_widgets:
                    if batch_widget['type'] == "checkbox":
                        checkbox_counts[batch_widget['name']] = 0
                    if batch_widget['type'] == "combobox":
                        combo_values[batch_widget['name']] = []

                for bn in self.shots_deets[sht]['bundle_names'].keys():
                    for checkbox in checkbox_counts.keys():
                        if self.shots_deets[sht]['bundle_names'][bn][checkbox].isChecked() is True:
                            checkbox_counts[checkbox] += 1
                    for combobox in combo_values.keys():
                        val = self.shots_deets[sht]['bundle_names'][bn][combobox].currentText()
                        if val not in combo_values[combobox]:
                            combo_values[combobox].append(val)

                comboText = ""
                publish_count = len(self.shots_deets[sht]['bundle_names'].keys())
                for batch_widget in self.batch_widgets:
                    if batch_widget["type"] == "combobox":
                        combo = combo_values.get(batch_widget['name'])
                        if len(combo) == 1:
                            val = combo[0]
                        else:
                            val = "multiple"
                        text = "%s: %s" % (batch_widget['label'], val)
                        comboText += " " + text + ","

                checkText = ""
                for batch_widget in self.batch_widgets:
                    if batch_widget["type"] == "checkbox":
                        checkbox = checkbox_counts.get(batch_widget['name'])
                        text = None
                        text = "%s: %d/%d" % (batch_widget['label'], checkbox, publish_count)
                        checkText += " " + text + ","

                label_text = "%d Publishes under shot %s, %s %s" % (publish_count, sht, comboText, checkText)

                if "1 Publishes" in label_text:
                    label_text = label_text.replace("1 Publishes", "1 Publish")

                self.shots_deets[sht]['collapser'].setTitle(label_text[:-1])

        def toggleAll(self):
            if self.expandbutton.text() == "Expand All":
                self.expandbutton.setText("Collapse All")
                for collapser in self.collapse_widgets:
                    if collapser.isCollapsed():
                        collapser.toggle()
            elif self.expandbutton.text() == "Collapse All":
                self.expandbutton.setText("Expand All")
                for collapser in self.collapse_widgets:
                    if not collapser.isCollapsed():
                        collapser.toggle()

        def check_all_or_none(self):
            butt = self.sender()
            check_type = butt.name
            check_enable = False
            if butt.text().endswith(" All"):
                check_enable = True

            for seq in self.shots_deets.keys():
                for sht in self.shots_deets[seq]['bundle_names'].keys():
                    self.shots_deets[seq]['bundle_names'][sht][check_type].setChecked(check_enable)

            if check_enable:
                butt.setText(butt.text()[:-4] + " None")
            else:
                butt.setText(butt.text()[:-5] + " All")

            self.setlabels()

        def publish(self):
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            self.progressBar.setVisible(True)
            self.progressBar.setValue(0)
            turnovers = []
            self.create_logs()
            for select in self.selection:
                turnover = {}
                binChain = [select.parentBin()]
                while "parentBin" in dir(binChain[0]):
                    binChain.insert(0, binChain[0].parentBin())

                turnover['path'] = select.activeItem().mediaSource().fileinfos()[0].filename()
                turnover['bundle_name'] = binChain[5].name()
                turnover['shot'] = binChain[4].name()
                turnover['sequence'] = binChain[3].name()
                turnover['turnover'] = binChain[2].name()
                turnover['description'] = turnover['bundle_name'] + "_" + turnover['turnover']
                turnover['comment'] = turnover['description']
                turnover['workspacePath'] = os.path.abspath(os.path.join(os.environ["SHOWS"], os.environ["SHOW"], "shots", turnover['sequence'], turnover['shot']))
                turnover['workspacePath'] = turnover['workspacePath'].replace(os.environ["SHOW_SERVER"], "")

                turnover['firstFrame'] = select.activeItem().mediaSource().fileinfos()[0].startFrame()
                turnover['lastFrame'] = select.activeItem().mediaSource().fileinfos()[0].endFrame()

                turnover['files'] = []
                for frameNo in range(turnover['firstFrame'], turnover['lastFrame']):
                    filename = select.activeItem().mediaSource().fileinfos()[0].filename() % frameNo

                    turnover['files'].append(filename)

                arguments = []
                for widget_def in self.batch_widgets:

                    w_name = widget_def['name']
                    if w_name != "publish_this":
                        arguments.append("-" + w_name)
                        qt_widget = self.shots_deets[turnover['shot']]['bundle_names'][turnover['bundle_name']][w_name]
                        if type(qt_widget) == BBCheckBox:
                            arguments.append(str(qt_widget.isChecked()))
                        elif type(qt_widget) == QComboBox:
                            arguments.append(qt_widget.currentText())
                        elif type(qt_widget) == QLineEdit:
                            arguments.append(qt_widget.text())

                if not self.shots_deets[turnover['shot']]['bundle_names'][turnover['bundle_name']]['publish_this'].isChecked():
                    continue

                turnover['cmd'] = ['eval $(%s/workspace.py %s)' % (os.environ['WORKSPACE_TOOLS_BUILD_PATH'], turnover['workspacePath']),
                                   'python %s/bin/mkBundleParser.py' % os.environ['MKBUNDLE'],
                                   '-discipline', self.discipline.title(),
                                   '-description', str(turnover['description']),
                                   '-version', '-1',
                                   '-asset', str(turnover['shot']),
                                   '-workspacePath', str(turnover['workspacePath']),
                                   '-path', str(turnover['path']),
                                   '-bundleType', self.bundleType,
                                   '-comment', str(turnover['comment'])]

                turnover['cmd'] += arguments

                turnovers.append(turnover)

            missing_workspaces = []
            missing_frames = []

            for turnover in turnovers:
                print turnover['workspacePath']
                if not os.path.exists(turnover['workspacePath']):
                    missing_workspaces.append(turnover['workspacePath'])

                for frame in turnover['files']:
                    if not os.path.exists(frame):
                        missing_frames.append(frame)

            if len(missing_workspaces) != 0 and len(missing_frames) != 0:
                self.showMessage("Cannot Publish Plates", "One or more workspaces don't exist in the filesystem and there are missing files", missing_workspaces, missing_frames)
            elif len(missing_workspaces) != 0:
                self.showMessage("Cannot Publish Plates", "One or more workspaces don't exist in the filesystem", missing_workspaces, missing_frames)
            elif len(missing_frames) != 0:
                self.showMessage("Cannot Publish Plates", "There are missing files", missing_workspaces, missing_frames)

            else:
                c = 0.0
                for turnover in turnovers:
                    c += 1.0
                    self.progressBar.setValue((c / (len(turnovers))) * 100)
                    commandLineCommand = " ".join(turnover["cmd"])
                    self.writeToLog(str(commandLineCommand))

                    script = os.path.join(os.environ['HIERO_BUNDLE_TOOLS_SCRIPTS'], 'submitDeadlineJob.py')
                    process = sub.Popen([script, '-cmd', commandLineCommand, "-jobdata", "%s/jobdata/%s/%s/%s/%s/" % (str(self.log_path),
                                                                                                                      str(turnover['turnover']),
                                                                                                                      str(turnover['sequence']),
                                                                                                                      str(turnover['shot']),
                                                                                                                      str(turnover['bundle_name'])),
                                         "-name",
                                         "create_input_plate_publish",
                                         "-queue",
                                         str(queue)], stdout=sub.PIPE)
                    out, err = process.communicate()

                if len(turnovers) == 1:
                    self.showMessage("Publish Complete", "%d plates sent for publishing. Check its progress on the farm." % (len(turnovers)))
                else:
                    self.showMessage("Publish Complete", "%d plates sent for publishing. Check their progress on the farm." % (len(turnovers)))

                self.close()
            self.progressBar.setVisible(False)
            QtWidgets.QApplication.restoreOverrideCursor()

        def showMessage(self, title, message, missing_workspaces=[], missing_frames=[]):
            global dialog
            dialog = BlueBoltMessageDialog(title, message=message, style=self.style)
            centerDialog(dialog)
            dialog.setOkVisible(True)
            dialog.setCancelVisible(False)
            dialog.setCloseVisible(False)
            height = 200
            if len(missing_workspaces) and len(missing_frames):
                height = 300
            if len(missing_workspaces) != 0:
                setStaticSize(dialog, 400, height)
                textEdit = QtWidgets.QTextEdit()
                textEdit.setPlainText("\n".join(missing_workspaces))
                textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
                dialog.layout().insertWidget(3, QLabel("Missing Workspaces:"))
                dialog.layout().insertWidget(4, textEdit)

            if len(missing_frames) != 0:
                setStaticSize(dialog, 700, height)

                textEdit = QtWidgets.QTextEdit()
                textEdit.setPlainText("\n".join(missing_frames))
                textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
                dialog.layout().insertWidget(3, QLabel("Missing Frames:"))
                dialog.layout().insertWidget(4, textEdit)

            return dialog.exec_()

        def create_logs(self):
            show_path = os.path.join(os.environ["SHOWS"], os.environ["SHOW"])
            if not os.path.exists(show_path):
                print "The show %s doesnt seem to exist" % show_path
                system.exit(0)
            right_now = datetime.utcnow()

            self.log_path = os.path.join(show_path, "tools/logs/inputPlatePublish/input_publish_" + right_now.strftime('%Y-%m-%d_%H-%M-%S.%f'))

            while not os.path.exists(self.log_path):
                self.log_path = os.path.join(show_path, "tools/logs/inputPlatePublish/input_publish_" + right_now.strftime('%Y-%m-%d_%H-%M-%S.%f'))
                if not os.path.exists(self.log_path):
                    os.makedirs(self.log_path)

            logfile_name = self.log_path + "/publish_from_hieroplayer.log"
            self.logfile = open(logfile_name, "w")

            print "Log started: %s" % (logfile_name)

            self.logfile.write("Input Publish run by %s at %s\n\n" % (os.environ['USER'], right_now.strftime('%H:%M on %d/%m/%Y')))

        def writeToLog(self, s):
            self.logfile.write(str(s) + "\n")
            self.logfile.flush()

        def getQueue(self):
            if "SECURE" in os.environ:
                if os.environ['SECURE'] == 'True':
                    q = 'io.q'
                else:
                    q = 'bundle.q'
            else:
                q = 'bundle.q'

            return q

    def recursiveClips(self, selection, clips):

        for s in selection:

            print ""
            if isinstance(s, hiero.core.Bin):
                for item in s.items():
                    if isinstance(item, hiero.core.BinItem) and hasattr(item, "activeItem"):
                        if isinstance(item.activeItem(), hiero.core.Clip):
                            clips.append(item)
                    elif isinstance(item, hiero.core.Bin):
                        self.recursiveClips([item], clips)
            elif isinstance(s, hiero.core.BinItem) and hasattr(s, "activeItem"):
                if isinstance(s.activeItem(), hiero.core.Clip):
                    clips.append(s)
        selected_media = []
        for clip in clips:
            selected_media.append(clip.activeItem().mediaSource())

        return clips

    def doit(self):

        selection = list(hiero.ui.activeView().selection())

        ignoredItems = []
        for selected in selection:
            if isinstance(selected, hiero.core.BinItem) and hasattr(selected, "activeItem"):
                if isinstance(selected.activeItem(), hiero.core.Sequence):
                    ignoredItems.append(selected)

        if ignoredItems:
            for item in ignoredItems:
                selection.remove(item)

        if len(selection) == 1 and isinstance(selection[0], hiero.core.Bin):
            clips = []
            selection = self.recursiveClips(selection, clips)
            clip_dict = {}
            for c in selection:
                print c.parentBin()
                clip_dict[str(c)] = c
            clip_keys = clip_dict.keys()
            clip_keys.sort()
            sselection = []
            for c in clip_keys:
                sselection.append(clip_dict[c])
            print len(sselection)
            print len(selection)

        window = self.PublishPlatesWindow(selection, parent=QtWidgets.QApplication.desktop())
        window.show()

    def eventHandler(self, event):
        if not hasattr(event.sender, 'selection'):
            return

        # Disable if nothing is selected
        selection = event.sender.selection()

        if selection is None:
            selection = ()

        title = "Batch Publish"
        self.setText(title)
        self.setEnabled(len(selection) > 0)
        if hasattr(event, "menu"):
            event.menu.addAction(self)


action = InputPlatePublishAction()
