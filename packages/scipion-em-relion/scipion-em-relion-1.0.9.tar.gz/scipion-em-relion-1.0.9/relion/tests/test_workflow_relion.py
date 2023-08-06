# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se) [1]
# *
# * [1] SciLifeLab, Stockholm University
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os

from pyworkflow.em import *
from pyworkflow.em.convert import ImageHandler
from pyworkflow.tests import *
from pyworkflow.utils import importFromPlugin
from pyworkflow.tests.em.workflows.test_workflow import TestWorkflow

import relion
from relion.protocols import *
from relion.constants import (RUN_OPTIMIZE, REF_AVERAGES,
                              RUN_COMPUTE, REF_BLOBS)

ProtCTFFind = importFromPlugin('grigoriefflab.protocols', 'ProtCTFFind')
XmippProtPreprocessMicrographs = importFromPlugin(
    'xmipp3.protocols', 'XmippProtPreprocessMicrographs')


class TestWorkflowRelionPick(TestWorkflow):
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        cls.ds = DataSet.getDataSet('relion_tutorial')

    def _launchPick(self, pickProt, validate=True):
        """ Simple wrapper to launch a pickig protocol.
        If validate=True, the output will be validated to exist and
        with non-zero elements.
        """
        self.launchProtocol(pickProt)

        if validate:
            # We have changed the name of the output to 'outputCoordinatesSubset'
            # when optimizing the wizard, so we need to consider this here
            # for testing the output is not None
            if hasattr(pickProt, 'outputCoordinatesSubset'):
                outputName = 'outputCoordinatesSubset'
            else:
                outputName = 'outputCoordinates'
            # Check the output coordinates is not None and has some items
            outputCoords = getattr(pickProt, outputName, None)
            self.assertIsNotNone(outputCoords)
            self.assertTrue(outputCoords.getSize() > 0,
                            msg="Output set (%s) is empty for protocol '%s'" %
                                (outputName, pickProt.getRunName()))

    def _runPickWorkflow(self):
        #First, import a set of micrographs
        print "Importing a set of micrographs..."
        protImport = self.newProtocol(ProtImportMicrographs,
                                      filesPath=self.ds.getFile('micrographs'),
                                      filesPattern='*.mrc',
                                      samplingRateMode=1,
                                      magnification=79096,
                                      scannedPixelSize=56, voltage=300,
                                      sphericalAberration=2.0)
        protImport.setObjLabel('import 20 mics')
        self.launchProtocol(protImport)
        self.assertIsNotNone(protImport.outputMicrographs,
                             "There was a problem with the import")
        
        print "Preprocessing the micrographs..."
        protCropMics = self.newProtocol(XmippProtPreprocessMicrographs,
                                        doCrop=True, cropPixels=25)
        protCropMics.inputMicrographs.set(protImport.outputMicrographs)
        protCropMics.setObjLabel('crop 50px')
        self.launchProtocol(protCropMics)
        self.assertIsNotNone(protCropMics.outputMicrographs,
                             "There was a problem with the downsampling")
        self.protCropMics = protCropMics

        # Now estimate CTF on the micrographs with ctffind
        print "Performing CTFfind..."
        protCTF = self.newProtocol(ProtCTFFind,
                                   useCtffind4=True,
                                   lowRes=0.02, highRes=0.45,
                                   minDefocus=1.2, maxDefocus=3,
                                   runMode=1,
                                   numberOfMpi=1, numberOfThreads=3)
        protCTF.inputMicrographs.set(protCropMics.outputMicrographs)
        protCTF.setObjLabel('CTF ctffind')
        self.protCTF = protCTF
        self.launchProtocol(protCTF)

        print "Importing 2D averages (subset of 4)"
        ih = ImageHandler()
        classesFn = self.ds.getFile('import/classify2d/extra/'
                                    'relion_it015_classes.mrcs')

        outputName = 'input_averages.mrcs'
        inputTmp = os.path.abspath(self.proj.getTmpPath())
        outputFn = self.proj.getTmpPath(outputName)

        for i, index in enumerate([5, 16, 17, 18, 24]):
            ih.convert((index, classesFn), (i+1, outputFn))

        protAvgs = self.newProtocol(ProtImportAverages,
                                    objLabel='avgs - 5',
                                    filesPath=inputTmp,
                                    filesPattern=outputName,
                                    samplingRate=7.08)

        self.launchProtocol(protAvgs)


        # Select some good averages from the iterations mrcs a

        protPick1 = self.newProtocol(
            ProtRelion2Autopick,
            objLabel='autopick refs (optimize)',
            runType=RUN_OPTIMIZE,
            micrographsList=5,
            referencesType=REF_AVERAGES,
            refsHaveInvertedContrast=True,
            particleDiameter=380)

        protPick1.inputMicrographs.set(protCropMics.outputMicrographs)
        protPick1.ctfRelations.set(protCTF.outputCTF)
        protPick1.inputReferences.set(protAvgs.outputAverages)

        self._launchPick(protPick1)

        return protPick1

    def test_ribo(self):
        protPick1 = self._runPickWorkflow()

        # Launch the same picking run but now for all micrographs
        protPick2 = self.proj.copyProtocol(protPick1)
        protPick2.setObjLabel('autopick refs (all)')
        protPick2.runType.set(RUN_COMPUTE)
        self._launchPick(protPick2)

        # Launch now using the Gaussian as references
        protPick3 = self.proj.copyProtocol(protPick1)
        if relion.Plugin.isVersion3Active():
            print("Importing volume")
            volFn = self.ds.getFile('import/case2/volume.mrc')
            protVol = self.newProtocol(ProtImportVolumes,
                                       objLabel='ref volume',
                                       filesPath=volFn,
                                       samplingRate=7.08)
            self.launchProtocol(protVol)
            protPick3.setObjLabel('autopick ref 3D (optimize)')
            protPick3.inputReferences3D.set(protVol.outputVolume)
        else:
            protPick3.setObjLabel('autopick gauss (optimize)')
        protPick3.referencesType.set(REF_BLOBS)
        protPick3.inputReferences.set(None)
        self._launchPick(protPick3)

        # Launch the same picking run but now in 1 GPU.
        protPick4 = self.proj.copyProtocol(protPick1)
        protPick4.setObjLabel('autopick refs (optimize) 1 GPU')
        protPick4.gpusToUse.set('0:0:0:0')
        self._launchPick(protPick4)

    def test_ribo_LoG(self):
        if relion.Plugin.isVersion2Active():
            print("LoG picker requires Relion 3.0 or greater. Skipping test...")
            return

        # First, import a set of micrographs
        print "Importing a set of micrographs..."
        protImport = self.newProtocol(ProtImportMicrographs,
                                      filesPath=self.ds.getFile('micrographs'),
                                      filesPattern='*.mrc',
                                      samplingRateMode=1,
                                      magnification=79096,
                                      scannedPixelSize=56, voltage=300,
                                      sphericalAberration=2.0)
        protImport.setObjLabel('import 20 mics')
        self.launchProtocol(protImport)
        self.assertIsNotNone(protImport.outputMicrographs,
                             "There was a problem with the import")

        print "Preprocessing the micrographs..."
        protCropMics = self.newProtocol(XmippProtPreprocessMicrographs,
                                        doCrop=True, cropPixels=25)
        protCropMics.inputMicrographs.set(protImport.outputMicrographs)
        protCropMics.setObjLabel('crop 50px')
        self.launchProtocol(protCropMics)
        self.assertIsNotNone(protCropMics.outputMicrographs,
                             "There was a problem with the downsampling")

        protPick = self.newProtocol(ProtRelionAutopickLoG,
                                    objLabel='autopick LoG',
                                    boxSize=60,
                                    minDiameter=30,
                                    maxDiameter=50)
        protPick.inputMicrographs.set(protCropMics.outputMicrographs)
        self._launchPick(protPick)


class TestWorkflowRelionExtract(TestWorkflowRelionPick):
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        cls.ds = DataSet.getDataSet('relion_tutorial')

    def _checkOutput(self, prot, **kwargs):
        # Read expected parameters
        size = kwargs.get('size', 5828)
        sampling = kwargs.get('sampling', 7.08)
        dim = kwargs.get('dim', 64)

        outputParts = getattr(prot, 'outputParticles', None)

        self.assertIsNotNone(outputParts)
        # Maybe number of particles changes between different versions
        # of Relion, so let's give a delta
        self.assertAlmostEqual(outputParts.getSize(), size, delta=10)

        first = outputParts.getFirstItem()
        ctfModel = first.getCTF()

        ctfGold = self.protCTF.outputCTF.getFirstItem()
        
        self.assertEqual(first.getDim(), (dim, dim, 1))
        self.assertAlmostEqual(first.getSamplingRate(), sampling, delta=0.001)
        self.assertAlmostEqual(ctfModel.getDefocusU(), ctfGold.getDefocusU())
        self.assertAlmostEqual(ctfModel.getDefocusV(), ctfGold.getDefocusV())

    def test_ribo(self):
        """ Reimplement this test to run several extract cases. """
        protPick1 = self._runPickWorkflow()
        protPick1.runType.set(RUN_COMPUTE)
        self._launchPick(protPick1)
        proj = protPick1.getProject()
        size = protPick1.outputCoordinates.getSize()

        protExtract = self.newProtocol(ProtRelionExtractParticles,
                                       objLabel='extract - box=64',
                                       boxSize=64,
                                       doInvert=True)

        protExtract.inputCoordinates.set(protPick1.outputCoordinates)
        protExtract.ctfRelations.set(self.protCTF.outputCTF)

        self.launchProtocol(protExtract)
        self._checkOutput(protExtract, size=size)

        # Now test the re-scale option
        protExtract2 = self.proj.copyProtocol(protExtract)
        protExtract2.setObjLabel('extract - rescale 32')
        protExtract2.doRescale.set(True)
        protExtract2.rescaledSize.set(32)

        self.launchProtocol(protExtract2)
        self._checkOutput(protExtract2, size=size, dim=32, sampling=14.16)
        
        # Now test changing micrographs source option
        splitSetsProt = self.newProtocol(ProtSplitSet,
                                         randomize=False,
                                         numberOfSets=2)
        splitSetsProt.inputSet.set(self.protCropMics.outputMicrographs)
        self.launchProtocol(splitSetsProt)

        # We choose the first output to keep the assertion procedure
        otherSetMics = splitSetsProt.outputMicrographs01

        protExtract3 = self.proj.copyProtocol(protExtract)
        protExtract3.setObjLabel('extract - Other')
        protExtract3.downsampleType.set(1)
        protExtract3.inputMicrographs.set(otherSetMics)
        self.launchProtocol(protExtract3)
        
        # The number of particles is different than the imported coordinates
        # due to the subSet done.
        self._checkOutput(protExtract3, size=2616)
