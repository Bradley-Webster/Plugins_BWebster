# Context menu option to create new sequences from selected Clips in the Bin View.
# If Clips are named as Stereo left and right then one sequence will be created with left and right tagged tracks.

from PySide2 import QtCore, QtGui, QtWidgets

Signal = QtCore.Signal

import hiero.core

import shotgun_utils as su
import re
import subprocess as sub
import os
import sys
import Queue as queue
import bb_python.Workspace as bbw

from threading import Thread
from bb_python.gui.Style import *
from bb_python.gui.Widget import *

import datetime as dt
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

import pprint


class PublishCutAction(QtWidgets.QAction):

    def __init__(self):
        QtWidgets.QAction.__init__(self, "Cut Publish", None)

        self.triggered.connect(self.doit)
        hiero.core.events.registerInterest((hiero.core.events.EventType.kShowContextMenu, hiero.core.events.EventType.kBin), self.eventHandler)
        hiero.core.events.registerInterest(hiero.core.events.EventType.kSelectionChanged, self.eventHandler)

    class PublishCutWindow(BlueBoltWindow):
        def __init__(self, selected, parent=None, title="Cut Publish " + version_str, style=BlueBoltDarkStyle):
            super(PublishCutAction.PublishCutWindow, self).__init__(title, style, parent)
            QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            self.setWindowFlags(Qt.Window)

            self.resize(400, 200)

            self.setWindowOpacity(1.0)
            self.centralFrame = QtWidgets.QFrame()
            self.centralLayout = QtWidgets.QVBoxLayout()
            self.centralFrame.setLayout(self.centralLayout)
            self.centralFrame.setObjectName('centralFrame')

            self.centralFrame.setStyleSheet("QFrame#centralFrame {border:1px solid rgba(0,0,0,0); background-color:rgba(56,56,56,255)}")

            self.setCentralWidget(self.centralFrame)

            self.sequence = selected

            self.create_center_frame_widgets()
            centerDialog(self)

        def create_center_frame_widgets(self):
            self.cut_name_label = QtWidgets.QLabel("Cut Name:")
            self.cut_name_dropdown = QtWidgets.QComboBox()
            self.cut_name_dropdown.setEditable(True)
            for item in self.get_cut_names():
                self.cut_name_dropdown.addItem(str(item))
            self.cut_name_dropdown.currentIndexChanged.connect(self.cut_name_changed)

            self.new_cut_version_checkbox = QtWidgets.QCheckBox("Publish new version")
            self.new_cut_version_checkbox.setChecked(True)
            self.new_cut_version_checkbox.setChecked(True)
            self.new_cut_version_checkbox.stateChanged.connect(self.version_check_changed)

            self.cut_version_label = QtWidgets.QLabel("Publish over version:")
            self.cut_version_dropdown = QtWidgets.QComboBox()
            self.cut_version_dropdown.setEditable(True)
            self.cut_version_label.setEnabled(False)
            self.cut_version_dropdown.setEnabled(False)

            self.thumbFrameLabel = QtWidgets.QLabel("Frame For Thumbnail:")
            self.thumbFrame = QtWidgets.QSpinBox()
            self.thumbFrame.setMinimumHeight(25)
            self.thumbFrame.setMinimum(self.sequence.videoTracks()[0].items()[0].timelineIn())
            self.thumbFrame.setMaximum(self.sequence.videoTracks()[0].items()[-1].timelineOut())

            self.publish_button = QtWidgets.QPushButton("Publish")
            self.publish_button.setMinimumWidth(70)
            self.publish_button.setMinimumHeight(30)
            self.publish_button.clicked.connect(self.publish)

            hStyle = """QFrame#hframe{border:0px solid rgba(0,0,0,0); background-color:rgba(56,56,56,255)}
                QLabel:!enabled{color:rgba(100,100,100,255)}"""

            hFrame1 = QtWidgets.QFrame()
            hLayout1 = QtWidgets.QHBoxLayout()
            hFrame1.setLayout(hLayout1)
            hFrame1.setObjectName("hframe")
            hFrame1.setStyleSheet(hStyle)

            hFrame2 = QtWidgets.QFrame()
            hLayout2 = QtWidgets.QHBoxLayout()
            hFrame2.setLayout(hLayout2)
            hFrame2.setObjectName("hframe")
            hFrame2.setStyleSheet(hStyle)

            hFrame3 = QtWidgets.QFrame()
            hLayout3 = QtWidgets.QHBoxLayout()
            hFrame3.setLayout(hLayout3)
            hFrame3.setObjectName("hframe")
            hFrame3.setStyleSheet(hStyle)

            hFrame4 = QtWidgets.QFrame()
            hLayout4 = QtWidgets.QHBoxLayout()
            hFrame4.setLayout(hLayout4)
            hFrame4.setObjectName("hframe")
            hFrame4.setStyleSheet(hStyle)

            hFrame5 = QtWidgets.QFrame()
            hLayout5 = QtWidgets.QHBoxLayout()
            hFrame5.setLayout(hLayout5)
            hFrame5.setObjectName("hframe")
            hFrame5.setStyleSheet(hStyle)

            hLayout1.addWidget(self.cut_name_label)
            hLayout1.addWidget(self.cut_name_dropdown)

            hLayout2.addWidget(self.cut_version_label)
            hLayout2.addWidget(self.cut_version_dropdown)

            hLayout3.addWidget(self.new_cut_version_checkbox)

            hLayout4.addWidget(self.thumbFrameLabel)
            hLayout4.addWidget(self.thumbFrame)

            hLayout5.insertStretch(0)
            hLayout5.addWidget(self.publish_button)

            self.centralLayout.addWidget(hFrame1)
            self.centralLayout.addWidget(hFrame2)
            self.centralLayout.addWidget(hFrame3)
            self.centralLayout.addWidget(hFrame4)
            self.centralLayout.addWidget(hFrame5)

        def publish(self):
            cut_data = self.get_cut_data()
            thumbnail_frame = self.thumbFrame.value()
            try:
                self.publish_cut(cut_data, thumbnail_frame)
            except Exception, e:
                self.showMessage("Error While Publishing Cut", "Error: " + str(e))

        def showMessage(self, title, message):
            global dialog
            dialog = BlueBoltMessageDialog(title, message=message, style=BlueBoltDarkStyle)
            centerDialog(dialog)
            dialog.setOkVisible(True)
            dialog.setCancelVisible(False)
            dialog.setCloseVisible(False)
            height = 200

            return dialog.exec_()

        def get_cut_data(self):
            data = {}
            data["code"] = self.cut_name_dropdown.currentText().replace(" ", "_")

            revision_number_str = self.cut_version_dropdown.currentText()
            get_latest = False
            if self.new_cut_version_checkbox.isChecked():
                get_latest = True
            if not revision_number_str.isdigit():
                get_latest = True

            if get_latest:
                revision_number = 0
                sg = su.get_sg_instance()
                cuts = sg.find("Cut",
                               [["project.Project.code", "is", os.environ.get("SHOW")],
                                ["code", "is", str(self.cut_name_dropdown.currentText())]],
                               ["code", "revision_number"])
                for cut in cuts:
                    if cut["revision_number"] and cut["revision_number"] > revision_number:
                        revision_number = cut["revision_number"]
                revision_number += 1

            else:
                revision_number = int(revision_number_str)

            data["revision_number"] = revision_number
            return data

        def version_check_changed(self):
            self.cut_version_dropdown.setEnabled(not self.sender().isChecked())
            self.cut_version_label.setEnabled(not self.sender().isChecked())

        def get_cut_names(self):
            sg = su.get_sg_instance()
            cuts = sg.find("Cut", [["project.Project.code", "is", os.environ.get("SHOW")]], ["code"])
            cut_names = [""]
            for cut in cuts:
                if cut['code'] not in cut_names:
                    cut_names.append(cut['code'])
            return cut_names

        def cut_name_changed(self):

            sg = su.get_sg_instance()
            cuts = sg.find("Cut",
                           [["project.Project.code", "is", os.environ.get("SHOW")],
                            ["code", "is", str(self.cut_name_dropdown.currentText())]],
                           ["code", "revision_number"])

            self.cut_version_dropdown.clear()
            for cut in cuts:
                if cut["revision_number"]:
                    if self.cut_version_dropdown.findText(str(cut["revision_number"])) == -1:
                        self.cut_version_dropdown.addItem(str(cut["revision_number"]))

        def publish_cut(self, cut_data, thumbnail_frame):
            self.close()
            window = self.PublishCutProgress(cut_data, self.sequence, thumbnail_frame, parent=QApplication.desktop())
            window.show()
            QtGui.qApp.processEvents()
            window.create_cut()

        class PublishCutProgress(BlueBoltWindow):
            def __init__(self, cut_data, sequence, thumbnail_frame, parent=None, title="Cut Publish Progress " + version_str, style=BlueBoltDarkStyle):
                super(PublishCutAction.PublishCutWindow.PublishCutProgress, self).__init__(title, style, parent)
                QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                self.setWindowFlags(Qt.Window)

                self.resize(600, 200)

                self.setWindowOpacity(1.0)
                self.centralFrame = QFrame()
                self.centralLayout = QVBoxLayout()
                self.centralFrame.setLayout(self.centralLayout)
                self.centralFrame.setObjectName('centralFrame')

                self.centralFrame.setStyleSheet("QFrame#centralFrame {border:1px solid rgba(0,0,0,0); background-color:rgba(56,56,56,255)}")

                self.setCentralWidget(self.centralFrame)

                self.sequence = sequence
                self.thumbnail_frame = thumbnail_frame
                self.cut_data = cut_data

                self.create_center_frame_widgets()
                centerDialog(self)

            def create_center_frame_widgets(self):

                self.progress_label = QtWidgets.QLabel("Creating shotgun cut for %s" % (self.sequence.name()))

                self.progress1 = QtWidgets.QProgressBar()
                self.progress1.setRange(0, 4)
                self.progress1.setTextVisible(True)

                self.progress2 = QtWidgets.QProgressBar()
                self.progress2.setTextVisible(True)

                self.closeB = QtWidgets.QPushButton("Close")
                self.closeB.clicked.connect(self.close)
                self.closeB.setMinimumWidth(70)
                self.closeB.setMinimumHeight(30)

                hStyle = """QFrame#hframe{border:0px solid rgba(0,0,0,0); background-color:rgba(56,56,56,255)}
                  QLabel:!enabled{color:rgba(100,100,100,255)}
                  QProgressBar
                  {
                      border: 2px solid grey;
                      border-radius: 5px;
                      text-align: center;
                  }
                  QProgressBar::chunk
                  {
                      background-color: #F7921E;
                      border-width: 0px;
                  }"""

                hFrame1 = QtWidgets.QFrame()
                hLayout1 = QtWidgets.QHBoxLayout()
                hFrame1.setLayout(hLayout1)
                hFrame1.setObjectName("hframe")
                hFrame1.setStyleSheet(hStyle)

                hFrame2 = QtWidgets.QFrame()
                hLayout2 = QtWidgets.QHBoxLayout()
                hFrame2.setLayout(hLayout2)
                hFrame2.setObjectName("hframe")
                hFrame2.setStyleSheet(hStyle)

                hFrame3 = QtWidgets.QFrame()
                hLayout3 = QtWidgets.QHBoxLayout()
                hFrame3.setLayout(hLayout3)
                hFrame3.setObjectName("hframe")
                hFrame3.setStyleSheet(hStyle)

                hFrame4 = QtWidgets.QFrame()
                hLayout4 = QtWidgets.QHBoxLayout()
                hFrame4.setLayout(hLayout4)
                hFrame4.setObjectName("hframe")
                hFrame4.setStyleSheet(hStyle)

                hLayout1.addWidget(self.progress_label)
                hLayout2.addWidget(self.progress1)
                hLayout3.addWidget(self.progress2)
                hLayout4.insertStretch(0)
                hLayout4.addWidget(self.closeB)

                self.centralLayout.addWidget(hFrame1)
                self.centralLayout.addWidget(hFrame2)
                self.centralLayout.addWidget(hFrame3)
                self.centralLayout.addWidget(hFrame4)

            def create_cut(self):
                self.progress1.setValue(0)
                self.progress1.setFormat("Uploading Cut Reference")
                QtGui.qApp.processEvents()
                self.upload_cut_reference()
                self.progress1.setValue(1)
                self.progress1.setFormat("Uploading Cut")
                QtGui.qApp.processEvents()
                self.upload_cut()
                self.progress1.setValue(2)
                self.progress1.setFormat("Creating cut items from timeline")
                QtGui.qApp.processEvents()
                cut_item_data = self.get_cut_item_data()
                self.progress1.setValue(3)
                self.progress1.setFormat("Uploading cut items")
                QtGui.qApp.processEvents()
                self.upload_cut_items(cut_item_data)
                self.progress1.setValue(4)
                self.progress1.setFormat("Upload Complete")
                QtGui.qApp.processEvents()

            def upload_cut_reference(self):
                self.cut_ref_frames = self.create_cut_reference_frames()
                version = {"project": su.get_sg_project(os.environ.get("SHOW")),
                           "code": "Cut Reference for %s_v%03d" % (self.cut_data["code"], self.cut_data["revision_number"]),
                           "sg_path_to_frames": self.cut_ref_frames}
                sg = su.get_sg_instance()
                self.sg_cut_ref_version = sg.create("Version", version)
                sg.upload_thumbnail("Version", self.sg_cut_ref_version['id'], self.cut_ref_frames % self.thumbnail_frame)

            def create_cut_reference_frames(self):
                path = os.path.join(os.environ.get("SHOW_PATH"), "editorial/cut_references/for_shotgun/%s_v%03d" % (self.cut_data["code"], self.cut_data["revision_number"]))
                if not os.path.exists(path):
                    os.makedirs(path)
                cut_ref_track = self.sequence.videoTracks()[0]

                self.progress2.setRange(cut_ref_track.items()[0].timelineIn(), cut_ref_track.items()[-1].timelineOut())
                c = cut_ref_track.items()[0].timelineIn()
                for item in cut_ref_track.items():
                    for frame in self.split_cut_item_into_frames(item):
                        symlink_path = os.path.join(path, frame[0])
                        if os.path.exists(symlink_path):
                            os.remove(symlink_path)
                        os.symlink(frame[1], symlink_path)
                        self.progress2.setValue(c)
                        c += 1

                return os.path.join(path, "frame.%08d.dpx")

            def split_cut_item_into_frames(self, item):
                file_infos = item.source().mediaSource().fileinfos()[0]
                formatted_path = file_infos.filename().replace("/mnt/SSD/_shows/", "/shows/")

                first = self.get_first_frame()
                symlink_filenames = []
                for frame_no in range(int(item.timelineIn()), 1 + int(item.timelineOut())):

                    symlink_filenames.append("frame.%08d.dpx" % (frame_no - first))

                frames = []
                for frame_no in range(int(item.sourceIn()), 1 + int(item.sourceOut())):
                    frames.append(formatted_path % (frame_no))

                return zip(symlink_filenames, frames)

            def upload_cut(self):
                self.sg_cut = self.upload_cut_to_sg()
                sg = su.get_sg_instance()
                sg.upload_thumbnail("Cut", self.sg_cut['id'], self.cut_ref_frames % self.thumbnail_frame)

            def upload_cut_to_sg(self):

                self.cut_data["project"] = su.get_sg_project(os.environ.get("SHOW"))
                self.cut_data["version"] = self.sg_cut_ref_version

                sg = su.get_sg_instance()
                finds = sg.find('Cut', [['project.Project.code', 'is', self.cut_data["project"]["code"]],
                                        ['revision_number', 'is', self.cut_data["revision_number"]],
                                        ['code', 'is', self.cut_data["code"]]])
                for find in finds:
                    sg.delete("Cut", find['id'])

                cut = sg.create('Cut', self.cut_data)
                return cut

            def get_cut_item_data(self):
                last_frame = self.get_last_frame()
                first_frame = self.get_first_frame()
                padding = first_frame

                current_item = None
                current_item_edit_in = 0
                cut_items = []
                self.progress2.setRange(first_frame, last_frame)
                for frame in range(first_frame, last_frame + 2):
                    self.progress2.setValue(frame)
                    QtGui.qApp.processEvents()

                    item_at_frame = self.sequence.trackItemAt(frame)

                    if current_item != item_at_frame:

                        if current_item:
                            edit_range = (current_item_edit_in, frame - 1)
                            cut_item = self.track_item_to_cut_item(current_item, edit_range)
                            cut_item = self.remove_start_padding_from_cut_item(cut_item, padding)
                            cut_item = self.add_descriptive_name_to_cut_item(cut_item)
                            cut_item = self.add_index_to_cut_item(cut_item, len(cut_items))
                            cut_items.append(cut_item)

                        current_item_edit_in = frame
                        current_item = item_at_frame

                return cut_items

            def track_item_to_cut_item(self, track_item, edit_range):
                item_dict = {
                    "sg_data": {
                        "cut_item_in": self.get_frame_of_track_item_from_sequence_frame(track_item, edit_range[0]),
                        "cut_item_out": self.get_frame_of_track_item_from_sequence_frame(track_item, edit_range[1]),
                        "edit_in": edit_range[0],
                        "edit_out": edit_range[1],
                        "cut_item_duration": edit_range[1] - edit_range[0]
                    },
                    "ref_data": {
                        "workspace": self.get_item_workspace_path(track_item),
                        "publish_path": self.get_item_publish_path(track_item),
                        "track_name": track_item.parent().name(),
                    }
                }

                return item_dict

            def remove_start_padding_from_cut_item(self, cut_item, padding):
                cut_item['sg_data']['edit_in'] = int(cut_item['sg_data']['edit_in'] - padding)
                cut_item['sg_data']['edit_out'] = int(cut_item['sg_data']['edit_out'] - padding)
                return cut_item

            def add_duration_to_cut_item(self, cut_item):
                duration = cut_item['sg_data']['cut_item_out'] - cut_item['sg_data']['cut_item_in']
                cut_item['sg_data']['cut_item_duration'] = duration
                return cut_item

            def add_index_to_cut_item(self, cut_item, index):
                cut_item['sg_data']['cut_order'] = index
                return cut_item

            def add_descriptive_name_to_cut_item(self, cut_item):
                cut_item['sg_data']['code'] = cut_item['ref_data']['track_name']
                return cut_item

            def get_frame_of_track_item_from_sequence_frame(self, track_item, sequence_frame):
                cut_in = int(track_item.sourceIn()) + int(track_item.source().mediaSource().timecodeStart())
                edit_in = int(track_item.timelineIn())
                frames_into_item = sequence_frame - edit_in
                frame_of_item = cut_in + frames_into_item
                return frame_of_item

            def get_last_frame(self):
                last = 0
                for video_track in self.sequence.videoTracks():
                    if len(video_track.items()):
                        last_in_track = video_track.items()[-1].timelineOut()
                        if last_in_track > last:
                            last = last_in_track
                return last

            def get_first_frame(self):
                first = None
                for video_track in self.sequence.videoTracks():
                    if len(video_track.items()):
                        first_in_track = video_track.items()[0].timelineIn()
                        if first == None or first_in_track < first:
                            first = first_in_track

                return first

            def get_item_workspace_path(self, item):
                file_path = item.source().mediaSource().firstpath()
                workspace = bbw.Workspace(os.path.dirname(file_path))
                return str(workspace.path).replace(os.environ.get("SHOW_SERVER"), "")

            def get_item_publish_path(self, item):
                file_path = item.source().mediaSource().firstpath()
                while file_path != "" and file_path != "/":
                    file_path = os.path.dirname(file_path)
                    job_data_path = os.path.join(file_path, ".jobdata")
                    if os.path.exists(job_data_path):
                        break
                return file_path.replace(os.environ.get("SHOW_SERVER"), "")

            def combine_cut_item_dicts(self, cut_item_dict_a, cut_item_dict_b):
                cut_item_dict_a["sg_data"]["edit_out"] = cut_item_dict_b["sg_data"]["edit_out"]
                cut_item_dict_a["sg_data"]["cut_item_out"] = cut_item_dict_b["sg_data"]["cut_item_out"]
                cut_item_dict_a["sg_data"]["cut_item_duration"] = cut_item_dict_b["sg_data"]["cut_item_out"] - cut_item_dict_a["sg_data"]["cut_item_in"]
                return cut_item_dict_a

            def upload_cut_items(self, cut_item_data):
                self.progress2.setRange(0, -1 + len(cut_item_data) * 2)
                cut_items_with_links = self.link_cut_items_to_sg_entities(cut_item_data)
                self.upload_sg_cut_items(cut_items_with_links)

            def link_cut_items_to_sg_entities(self, cut_item_data):
                items_for_upload = []
                sg_project = su.get_sg_project(os.environ.get("SHOW"))

                list_of_shots = su.get_sg_shots(os.environ.get("SHOW"), more_fields=["sg_path"])
                dict_of_shots = {}
                for shot in list_of_shots:
                    dict_of_shots[shot["sg_path"]] = shot

                list_of_versions = su.get_sg_version_by_filters(os.environ.get("SHOW"), {'project.Project.code': os.environ.get("SHOW")}, more_fields=["sg_bundle_path"])
                dict_of_versions = {}
                for version in list_of_versions:
                    dict_of_versions[version["sg_bundle_path"]] = version
                c = 0

                for cut_item in cut_item_data:
                    self.progress2.setValue(c)
                    QtGui.qApp.processEvents()
                    c += 1
                    sg_data = cut_item["sg_data"]
                    sg_data["project"] = sg_project

                    if dict_of_shots.get(cut_item["ref_data"]["workspace"]):
                        sg_data["shot"] = dict_of_shots.get(cut_item["ref_data"]["workspace"])

                    if dict_of_versions.get(cut_item["ref_data"]["publish_path"]):
                        sg_data["version"] = dict_of_versions.get(cut_item["ref_data"]["publish_path"])

                    sg_data["cut"] = self.sg_cut

                    items_for_upload.append(sg_data)
                return items_for_upload

            def upload_sg_cut_items(self, items):
                sg = su.get_sg_instance()
                c = len(items)
                for item in items:
                    self.progress2.setValue(c)
                    QtGui.qApp.processEvents()
                    c += 1
                    cut = sg.create('CutItem', item)

    def doit(self):

        selection = list(hiero.ui.activeView().selection())
        if self.is_selection_sequence(selection):
            window = self.PublishCutWindow(selection[0].items()[0].item(), parent=QApplication.desktop())
            window.show()
        else:
            self.showMessage("Incorrect Selection", "Publish cut only works with single sequences")

    def is_selection_sequence(self, selection):
        if len(selection) == 1:
            try:
                return type(selection[0].items()[0].item()) == hiero.core.Sequence
            except Exception, e:
                return False

        return False

    def showMessage(self, title, message):
        global dialog
        dialog = BlueBoltMessageDialog(title, message=message, style=BlueBoltDarkStyle)
        centerDialog(dialog)
        dialog.setOkVisible(True)
        dialog.setCancelVisible(False)
        dialog.setCloseVisible(False)
        height = 200

        return dialog.exec_()

    def eventHandler(self, event):
        if not hasattr(event.sender, 'selection'):
            return

        selection = event.sender.selection()

        if selection is None:
            selection = ()

        title = "Publish Cut"
        self.setText(title)
        self.setEnabled(len(selection) > 0)
        if hasattr(event, "menu"):
            event.menu.addAction(self)


action = PublishCutAction()
