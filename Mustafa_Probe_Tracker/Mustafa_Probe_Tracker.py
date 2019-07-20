import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import time

# Mustafa_Probe_Tracker
class Mustafa_Probe_Tracker(ScriptedLoadableModule):

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Mustafa_Probe_Tracker" # TODO make this more human readable by adding spaces
    self.parent.categories = ["MEDLAB Probe Tracker"]
    self.parent.dependencies = []


# Mustafa_Probe_TrackerWidget
class Mustafa_Probe_TrackerWidget(ScriptedLoadableModuleWidget):
  """ This class is GUI buttons side of the extension. """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    
    # Adding new collapsible button to loading probe model and tranformation
    loadingCollapsibleButton = ctk.ctkCollapsibleButton()
    loadingCollapsibleButton.text = "Load Probe Model and Transformation"
    self.layout.addWidget(loadingCollapsibleButton)

    # Layout within the dummy collabsible button
    loadingFormLayout = qt.QFormLayout(loadingCollapsibleButton)

    # Create a Mustafa_Probe_TrackerLogic() class for "connect" functions for buttons
    self.logic = Mustafa_Probe_TrackerLogic()

    # "Load Probe" Button
    self.probeButton = qt.QPushButton("Load Probe")
    self.probeButton.toolTip = "Load the Probe Model."
    self.probeButton.enabled = True
    loadingFormLayout.addRow(self.probeButton)

    # "Launch the Plus Server" Button
    self.launchPlusServerButton = qt.QPushButton("Launch the Plus Server")
    self.launchPlusServerButton.toolTip = "Starts the Plus Server"
    self.launchPlusServerButton.enabled = True
    loadingFormLayout.addRow(self.launchPlusServerButton)

    # "Load Transformation and Apply It" Button
    self.transformationButton = qt.QPushButton("Load Transformation and Apply It")
    self.transformationButton.toolTip = "Load the Transformation."
    self.transformationButton.enabled = True
    loadingFormLayout.addRow(self.transformationButton)

    # "Start the camera" Button
    self.markerTrackerButton = qt.QPushButton("Start the camera")
    self.markerTrackerButton.toolTip = "Starts the camera"
    self.markerTrackerButton.enabled = True
    loadingFormLayout.addRow(self.markerTrackerButton)

    # "Load the 3D Model" Button
    self.load3DModelButton = qt.QPushButton("Load the 3D Model")
    self.load3DModelButton.toolTip = "Loads the 3D Model and Fudicial points"
    self.load3DModelButton.enabled = True
    loadingFormLayout.addRow(self.load3DModelButton)

    # "Stop the camera" Button
    self.stopTrackerButton = qt.QPushButton("Stop the camera")
    self.stopTrackerButton.toolTip = "Stops the camera"
    self.stopTrackerButton.enabled = True
    loadingFormLayout.addRow(self.stopTrackerButton)
    
    # Connections for Buttons
    self.probeButton.connect('clicked(bool)',self.logic.loadProbeModel)
    #self.launchPlusServerButton.connect('clicked(bool)', self.logic.launchPlusServer)
    self.transformationButton.connect('clicked(bool)', self.logic.loadPivotTransform)
    self.markerTrackerButton.connect('clicked(bool)', self.logic.startCamera)
    self.load3DModelButton.connect('clicked(bool)', self.logic.load3DModel)
    self.stopTrackerButton.connect('clicked(bool)', self.logic.stopCamera)

    
    # Add vertical spacer
    self.layout.addStretch(1)


# Mustafa_Probe_TrackerLogic
class Mustafa_Probe_TrackerLogic(ScriptedLoadableModuleLogic):

  def __init__(self):
    self.trackerNode = None
    self.transformNode = None
    self.markerModel = None
    self.cameraState = False
    self.launcherNode = None


  # This function loads the Needle Model that we created previously.
  def loadProbeModel(self):
    slicer.util.loadModel("C:\Users\Mustafa Ugur\Documents\NeedleModel.vtk")  
  """
  # This function launchs the Plus Server
  def launchPlusServer(self):
    fn = "C:\Users\Mustafa Ugur\PlusApp-2.8.0.20190617-Win64\config\PlusDeviceSet_Server_OpticalMarkerTracker_Mmf.xml"
    with open(fn, 'r') as file:
      configText = file.read()



    logging.info("Empty now!")
  """

  # This function loads the transformation from the pivot calibration that we
  # done previously sets the hierarcy between needle and transformation.
  def loadPivotTransform(self):
    slicer.util.loadTransform("C:\Users\Mustafa Ugur\Documents\NeedleTipToMarker.h5")
    needleModel = slicer.util.getNode('NeedleModel')
    self.transformNode = slicer.util.getNode('NeedleTipToMarker')
    needleModel.SetAndObserveTransformNodeID(self.transformNode.GetID())

    if not self.trackerNode:
      self.trackerNode = slicer.vtkMRMLIGTLConnectorNode()
      slicer.mrmlScene.AddNode(self.trackerNode)
      self.trackerNode.SetName('markerTracker')
      
    self.trackerNode.Start()
    self.cameraState = True

  # This fuction starts camera for tracking.
  def startCamera(self):
    # Starting the camera and create a node for camera.
    """
    if not self.trackerNode:
      self.trackerNode = slicer.vtkMRMLIGTLConnectorNode()
      slicer.mrmlScene.AddNode(self.trackerNode)
      self.trackerNode.SetName('markerTracker')
    """
    if self.cameraState is False:
      self.trackerNode.Start()

    try:
      self.setHierarcy()
    except:
      print("Marker4ToTracker Exepcion occured, please show the chechkerboard to camera and press Start the Camera Button Again")
    

  def setHierarcy(self): 
    # Setting the hierarchy again
    self.transformNode = slicer.util.getNode('NeedleTipToMarker')
    self.markerModel = slicer.util.getNode('Marker4ToTracker')
    self.transformNode.SetAndObserveTransformNodeID(self.markerModel.GetID())

  # This function stops the camera.
  def stopCamera(self):
    self.trackerNode.Stop()
    self.cameraState = False

  # This function loads the 3D file was created for surface tracking.
  def load3DModel(self):
    slicer.util.loadModel("C:\Users\Mustafa Ugur\Desktop\simple_box\simple_box.STL")
    slicer.util.loadMarkupsFiducialList("C:\Users\Mustafa Ugur\Documents\From.fcsv")
