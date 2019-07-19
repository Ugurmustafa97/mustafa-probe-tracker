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

    # Do hierarchy setting again
    #self.setHierarchyButton = qt.QPushButton("Set the hierarchy")
    #self.setHierarchyButton.toolTip = "Sets the hieararchy again for tracking"
    #self.setHierarchyButton.enabled = True
    #loadingFormLayout.addRow(self.setHierarchyButton)

    # "Stop the camera" Button
    self.stopTrackerButton = qt.QPushButton("Stop the camera")
    self.stopTrackerButton.toolTip = "Stops the camera"
    self.stopTrackerButton.enabled = True
    loadingFormLayout.addRow(self.stopTrackerButton)
    
    # Connections for Buttons
    self.probeButton.connect('clicked(bool)',self.logic.loadProbeModel)
    self.transformationButton.connect('clicked(bool)', self.logic.loadPivotTransform)
    self.markerTrackerButton.connect('clicked(bool)', self.logic.startCamera)
    #self.setHierarchyButton.connect('clicked(bool)', self.logic.setHierarcy)
    self.stopTrackerButton.connect('clicked(bool)', self.logic.stopCamera)
    self.load3DModelButton.connect('clicked(bool)', self.logic.load3DModel)
    
    # Add vertical spacer
    self.layout.addStretch(1)


# Mustafa_Probe_TrackerLogic
class Mustafa_Probe_TrackerLogic(ScriptedLoadableModuleLogic):

  def __init__(self):
    self.trackerNode = None
    #self.markerModel = None

  # This function loads the Needle Model that we created previously.
  def loadProbeModel(self):
    slicer.util.loadModel("C:\Users\Mustafa Ugur\Documents\NeedleModel.vtk")  

  # This function loads the transformation from the pivot calibration that we
  # done previously sets the hierarcy between needle and transformation.
  def loadPivotTransform(self):
    slicer.util.loadTransform("C:\Users\Mustafa Ugur\Documents\NeedleTipToMarker.h5")
    needleModel = slicer.util.getNode('NeedleModel')
    transformNode = slicer.util.getNode('NeedleTipToMarker')
    needleModel.SetAndObserveTransformNodeID(transformNode.GetID())
  
  # This fuction starts camera for tracking.
  def startCamera(self):
    # Starting the camera and create a node for camera.
    if not self.trackerNode:
      self.trackerNode = slicer.vtkMRMLIGTLConnectorNode()
      slicer.mrmlScene.AddNode(self.trackerNode)
      self.trackerNode.SetName('markerTracker')  
    
    self.trackerNode.Start()

    try:
      transformNode = slicer.util.getNode('NeedleTipToMarker')
      markerModel = slicer.util.getNode('Marker4ToTracker')
      transformNode.SetAndObserveTransformNodeID(markerModel.GetID())
    except:
      print("Marker4ToTracker Exepcion occured, please show the chechkerboard to camera and press Start the Camera Button Again")
    
  """
  def setHierarcy(self): 
    # Setting the hierarchy again
    transformNode = slicer.util.getNode('NeedleTipToMarker')
    markerModel = slicer.util.getNode('Marker4ToTracker')
    transformNode.SetAndObserveTransformNodeID(markerModel.GetID())
  """
  # This function stops the camera.
  def stopCamera(self):
    self.trackerNode.Stop()

  # This function loads the 3D file was created for surface tracking.
  def load3DModel(self):
    slicer.util.loadModel("C:\Users\Mustafa Ugur\Desktop\simple_box\simple_box.STL")
    slicer.util.loadMarkupsFiducialList("C:\Users\Mustafa Ugur\Documents\From.fcsv")
