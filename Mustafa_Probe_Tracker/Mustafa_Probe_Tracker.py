import os
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging
import time

#
# Mustafa_Probe_Tracker
#




class Mustafa_Probe_Tracker(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Mustafa_Probe_Tracker" # TODO make this more human readable by adding spaces
    self.parent.categories = ["MEDLAB Probe Tracker"]
    self.parent.dependencies = []


#
# Mustafa_Probe_TrackerWidget
#

class Mustafa_Probe_TrackerWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)
    
    # Adding new collapsible button to loading probe model and tranformation  This was editied by Mustafa UGUR 07/10/2019
    loadingCollapsibleButton = ctk.ctkCollapsibleButton()
    loadingCollapsibleButton.text = "Load Probe Model and Transformation"
    self.layout.addWidget(loadingCollapsibleButton)

    
    # Layout within the dummy collabsible button                              This was editied by Mustafa UGUR 07/10/2019
    loadingFormLayout = qt.QFormLayout(loadingCollapsibleButton)
    
    self.logic = Mustafa_Probe_TrackerLogic()

    #
    # Load Probe Button                             This was editied by Mustafa UGUR 07/09/2019
    #
    self.probeButton = qt.QPushButton("Load Probe")
    self.probeButton.toolTip = "Load the Probe Model."
    self.probeButton.enabled = True
    loadingFormLayout.addRow(self.probeButton)
    
    #
    # Load Transformation Button                    This was editied by Mustafa UGUR 07/09/2019
    # 
    self.transformationButton = qt.QPushButton("Load Transformation and Apply It")
    self.transformationButton.toolTip = "Load the Transformation."
    self.transformationButton.enabled = True
    loadingFormLayout.addRow(self.transformationButton)
    
    
    
    #
    # Start the marker tracker                      
    #
    self.markerTrackerButton = qt.QPushButton("Start the camera")
    self.markerTrackerButton.toolTip = "Starts the camera"
    self.markerTrackerButton.enabled = True
    loadingFormLayout.addRow(self.markerTrackerButton)
    
    #
    # Load the 3D Model
    #
    self.load3DModelButton = qt.QPushButton("Load the 3D Model")
    self.load3DModelButton.toolTip = "Loads the 3D Model and Fudicial points"
    self.load3DModelButton.enabled = True
    loadingFormLayout.addRow(self.load3DModelButton)
    
    #
    # Do hierarchy setting again
    #
    #self.setHierarchyButton = qt.QPushButton("Set the hierarchy")
    #self.setHierarchyButton.toolTip = "Sets the hieararchy again for tracking"
    #self.setHierarchyButton.enabled = True
    #loadingFormLayout.addRow(self.setHierarchyButton)
    
    #
    # Stop the camera
    #
    self.stopTrackerButton = qt.QPushButton("Stop the camera")
    self.stopTrackerButton.toolTip = "Stops the camera"
    self.stopTrackerButton.enabled = True
    loadingFormLayout.addRow(self.stopTrackerButton)
    
    # connections
    self.probeButton.connect('clicked(bool)',self.logic.loadProbeModel)
    self.transformationButton.connect('clicked(bool)', self.logic.loadPivotTransform)
    self.markerTrackerButton.connect('clicked(bool)', self.logic.startCamera)
    #self.setHierarchyButton.connect('clicked(bool)', self.logic.setHierarcy)
    self.stopTrackerButton.connect('clicked(bool)', self.logic.stopCamera)
    self.load3DModelButton.connect('clicked(bool)', self.logic.load3DModel)
    
    # Add vertical spacer
    self.layout.addStretch(1)

  
  
  
    
#
# Mustafa_Probe_TrackerLogic
#

class Mustafa_Probe_TrackerLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  
  def __init__(self):
    self.trackerNode = None
    #self.markerModel = None
  
  #This was editied by Mustafa UGUR 07/09/2019
  def loadProbeModel(self):
    slicer.util.loadModel("C:\Users\Mustafa Ugur\Documents\NeedleModel.vtk")  
  
  def loadPivotTransform(self):
    slicer.util.loadTransform("C:\Users\Mustafa Ugur\Documents\NeedleTipToMarker.h5")
    needleModel = slicer.util.getNode('NeedleModel')
    transformNode = slicer.util.getNode('NeedleTipToMarker')
    needleModel.SetAndObserveTransformNodeID(transformNode.GetID())
  
  # This fuction starts camera for tracking 
  def startCamera(self):
    # Starting the camera
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
  def stopCamera(self):
    self.trackerNode.Stop()
    
  def load3DModel(self):
    slicer.util.loadModel("C:\Users\Mustafa Ugur\Desktop\simple_box\simple_box.STL")
    slicer.util.loadMarkupsFiducialList("C:\Users\Mustafa Ugur\Documents\From.fcsv")


