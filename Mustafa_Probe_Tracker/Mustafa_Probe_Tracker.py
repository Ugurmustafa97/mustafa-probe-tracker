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
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
It performs a simple thresholding on the input volume and optionally captures a screenshot.
"""
    self.parent.helpText += self.getDefaultModuleDocumentationLink()
    self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# Mustafa_Probe_TrackerWidget
#

class Mustafa_Probe_TrackerWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    # Instantiate and connect widgets ...
    """ #Editied by mustafa
    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)
    """ #Editied by mustafa
    
    # Adding new collapsible button to loading probe model and tranformation  This was editied by Mustafa UGUR 07/10/2019
    loadingCollapsibleButton = ctk.ctkCollapsibleButton()
    loadingCollapsibleButton.text = "Load Probe Model and Transformation"
    self.layout.addWidget(loadingCollapsibleButton)
    
    """ #Editied by mustafa
    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)
    """ #Editied by mustafa
    
    # Layout within the dummy collabsible button                              This was editied by Mustafa UGUR 07/10/2019
    loadingFormLayout = qt.QFormLayout(loadingCollapsibleButton)
    
    self.logic = Mustafa_Probe_TrackerLogic()
    
    
    
    
    
    """ #Editied by mustafa
    #
    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)
    
    
    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ["vtkMRMLScalarVolumeNode"]
    self.outputSelector.selectNodeUponCreation = True
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = True
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # threshold value
    #
    self.imageThresholdSliderWidget = ctk.ctkSliderWidget()
    self.imageThresholdSliderWidget.singleStep = 0.1
    self.imageThresholdSliderWidget.minimum = -100
    self.imageThresholdSliderWidget.maximum = 100
    self.imageThresholdSliderWidget.value = 0.5
    self.imageThresholdSliderWidget.setToolTip("Set threshold value for computing the output image. Voxels that have intensities lower than this value will set to zero.")
    parametersFormLayout.addRow("Image threshold", self.imageThresholdSliderWidget)
    
    #
    # check box to trigger taking screen shots for later use in tutorials
    #
    self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    self.enableScreenshotsFlagCheckBox.checked = 0
    self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)
    
    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)
    """ #Editied by mustafa
    
    
    
    
    
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
    #self.applyButton.connect('clicked(bool)', self.onApplyButton)                  #Editied by mustafa
    #self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)  #Editied by mustafa
    #self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect) #Editied by mustafa
    self.probeButton.connect('clicked(bool)',self.logic.loadProbeModel)
    self.transformationButton.connect('clicked(bool)', self.logic.loadPivotTransform)
    self.markerTrackerButton.connect('clicked(bool)', self.logic.startCamera)
    #self.setHierarchyButton.connect('clicked(bool)', self.logic.setHierarcy)
    self.stopTrackerButton.connect('clicked(bool)', self.logic.stopCamera)
    self.load3DModelButton.connect('clicked(bool)', self.logic.load3DModel)
    
    # Add vertical spacer
    self.layout.addStretch(1)
    
    """ #Editied by mustafa
    # Refresh Apply button state
    self.onSelect()
    """ 
    
  def cleanup(self):
    pass
  
 
  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()
  
  
  def onApplyButton(self):
    logic = Mustafa_Probe_TrackerLogic()
    enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
    imageThreshold = self.imageThresholdSliderWidget.value
    logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), imageThreshold, enableScreenshotsFlag)
  
  
  
    
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
    
  def hasImageData(self,volumeNode):
    """This is an example logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      logging.debug('hasImageData failed: no volume node')
      return False
    if volumeNode.GetImageData() is None:
      logging.debug('hasImageData failed: no image data in volume node')
      return False
    return True
  

  
  def isValidInputOutputData(self, inputVolumeNode, outputVolumeNode):
    """
    Validates if the output is not the same as input
    """
    if not inputVolumeNode:
      logging.debug('isValidInputOutputData failed: no input volume node defined')
      return False
    if not outputVolumeNode:
      logging.debug('isValidInputOutputData failed: no output volume node defined')
      return False
    if inputVolumeNode.GetID()==outputVolumeNode.GetID():
      logging.debug('isValidInputOutputData failed: input and output volume is the same. Create a new volume for output to avoid this error.')
      return False
    return True
  
  
  
  def run(self, inputVolume, outputVolume, imageThreshold, enableScreenshots=0):
    """
    Run the actual algorithm
    """

    if not self.isValidInputOutputData(inputVolume, outputVolume):
      slicer.util.errorDisplay('Input volume is the same as output volume. Choose a different output volume.')
      return False

    logging.info('Processing started')

    # Compute the thresholded output volume using the Threshold Scalar Volume CLI module
    cliParams = {'InputVolume': inputVolume.GetID(), 'OutputVolume': outputVolume.GetID(), 'ThresholdValue' : imageThreshold, 'ThresholdType' : 'Above'}
    cliNode = slicer.cli.run(slicer.modules.thresholdscalarvolume, None, cliParams, wait_for_completion=True)

    # Capture screenshot
    if enableScreenshots:
      self.takeScreenshot('Mustafa_Probe_TrackerTest-Start','MyScreenshot',-1)

    logging.info('Processing completed')

    return True
  

class Mustafa_Probe_TrackerTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here. """
    self.setUp()
    self.test_Mustafa_Probe_Tracker1()

  def test_Mustafa_Probe_Tracker1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import SampleData
    SampleData.downloadFromURL(
      nodeNames='FA',
      fileNames='FA.nrrd',
      uris='http://slicer.kitware.com/midas3/download?items=5767')
    self.delayDisplay('Finished with download and loading')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = Mustafa_Probe_TrackerLogic()
    self.assertIsNotNone( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
