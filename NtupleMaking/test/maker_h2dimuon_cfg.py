#
#   Ntuple Making Stage
#

import FWCore.ParameterSet.Config as cms
process = cms.Process("NtupleMaking")

#
#   loading sequences
#
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load('Configuration.EventContent.EventContent_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

import os
import sys
import shelve
import pickle
if "ANALYSISHOME" not in os.environ.keys():
    raise NameError("Can not find ANALYSISHOME env var")
sys.path.append(os.path.join(
    os.environ["ANALYSISHOME"], "Configuration", "higgs"))
import Samples as S
jsonfiles = S.jsonfiles
jsontag = "2017"
jsonfile = jsonfiles[jsontag]
json = "json/" + jsonfile.filename
thisIsData = True
globalTag = S.data_global_tag_2017
year = "2017"

if not thisIsData:
    if year == "2016":
        process.load("HMuMu.NtupleMaking.H2DiMuonMaker_94X16MC")
    elif year == "2017":
        process.load("HMuMu.NtupleMaking.H2DiMuonMaker_94X17MC")
    elif year == "2018":
        process.load("HMuMu.NtupleMaking.H2DiMuonMaker_102X18MC")
else:
    if year == "2016":
        process.load("HMuMu.NtupleMaking.H2DiMuonMaker_94X16Data")
    elif year == "2017":
        process.load("HMuMu.NtupleMaking.H2DiMuonMaker_94X17DataLocal")
    elif year == "2018":
        process.load("HMuMu.NtupleMaking.H2DiMuonMaker_102X18Data")

print("")
print('Loading Global Tag: ' + globalTag)
process.GlobalTag.globaltag = globalTag
print("")
print("")
print('Running over data sample')

# JET ENERGY CORRECTIONS

from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

if thisIsData:
    corrections = cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
else:
    corrections = cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute'])

updateJetCollection(
    process,
    jetSource=cms.InputTag('slimmedJets'),
    labelName='UpdatedJEC',
    # Update: Safe to always add 'L2L3Residual' as MC contains dummy L2L3Residual corrections (always set to 1)
    jetCorrections=('AK4PFchs', corrections, 'None')
)


## only for 2017? check this

if year == "2017":

    # EE noise mitigation fix SEE https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETUncertaintyPrescription#Instructions_for_9_4_X_X_9_for_2

    from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD

    runMetCorAndUncFromMiniAOD(
        process,
        isData=thisIsData,  # false for MC
        fixEE2017=True,
        fixEE2017Params={'userawPt': True, 'ptThreshold': 50.0,
                        'minEtaThreshold': 2.65, 'maxEtaThreshold': 3.139},
        postfix="ModifiedMET"
    )


## era based on year 2016/2017/2018

runVid = True
runCorrections = False
egammaEra = '2017-Nov17ReReco'
if year == "2016":
    print("running on 2016")
    egammaEra = '2016-Legacy'
    prefire_era = "2016BtoH"
if year == "2017":
    print("running on 2017")
    egammaEra = '2017-Nov17ReReco'
    runVid = False
    runCorrections = True
    prefire_era = "2017BtoF"
if year == "2018":
    print("running on 2018")
    egammaEra = '2018-Prompt'

    # vid = False
# electron energy scale correction fix SEE https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaMiniAODV2
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       runEnergyCorrections=runCorrections,
                       runVID=runVid,  # saves CPU time by not needlessly re-running VID
                       era=egammaEra)



# only applied to "2016" and 2017

if year == "2016" or year == "2017":
    ## prefiring weights
    from PhysicsTools.PatUtils.l1ECALPrefiringWeightProducer_cfi import l1ECALPrefiringWeightProducer
    process.prefiringweight = l1ECALPrefiringWeightProducer.clone(
        DataEra = cms.string(prefire_era), #Use 2016BtoH for 2016
        UseJetEMPt = cms.bool(False),
        PrefiringRateSystematicUncty = cms.double(0.2),
        SkipWarnings = False)


# FSR RECOVERY
from FSRPhotonRecovery.FSRPhotons.FSRphotonSequence_cff import addFSRphotonSequence
PhotonMVA="FSRPhotonRecovery/FSRPhotons/data/PhotonMVAv9_BDTG800TreesDY.weights.xml"
addFSRphotonSequence(process, 'slimmedMuons', PhotonMVA)


process.jecSequence = cms.Sequence(
    process.patJetCorrFactorsUpdatedJEC * 
    process.updatedPatJetsUpdatedJEC)


process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(100))

process.source = cms.Source("PoolSource", fileNames=cms.untracked.vstring(
    # 'file:DE1721FC-10D9-E711-B475-0025907B4F04.root'))
    'file:/eos/cms/store/user/amarini/Sync/0E555487-7241-E811-9209-002481CFC92C.root'))


process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(False))

import FWCore.PythonUtilities.LumiList as LumiList

process.source.lumisToProcess = LumiList.LumiList(filename=json).getVLuminosityBlockRange()


process.TFileService = cms.Service(
    "TFileService", fileName=cms.string("ntuple_Data.root"))

process.jecSequence = cms.Sequence(
    process.patJetCorrFactorsUpdatedJEC * process.updatedPatJetsUpdatedJEC)

if year == "2016":
    process.p = cms.Path(
    process.prefiringweight *
    process.egammaPostRecoSeq *
    process.jecSequence * 
    process.FSRphotonSequence*
    process.ntuplemaker_H2DiMuonMaker)
if year == "2017":
    process.p = cms.Path(
    process.prefiringweight *
    process.egammaPostRecoSeq *
    process.jecSequence * 
    process.fullPatMetSequenceModifiedMET * 
    process.FSRphotonSequence*
    process.ntuplemaker_H2DiMuonMaker)
if year == "2018":
        process.p = cms.Path(
    process.egammaPostRecoSeq *
    process.jecSequence * 
    process.FSRphotonSequence*
    process.ntuplemaker_H2DiMuonMaker)

