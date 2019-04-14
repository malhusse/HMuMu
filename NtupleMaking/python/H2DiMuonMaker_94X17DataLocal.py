import FWCore.ParameterSet.Config as cms
pt = 27

name = "H2DiMuonMaker"

ntuplemaker_H2DiMuonMaker = cms.EDAnalyzer(
    name,
    #   Tags
    tagMuons=cms.untracked.InputTag("slimmedMuons"),
    tagElectrons=cms.untracked.InputTag("slimmedElectrons"),
    tagTaus=cms.untracked.InputTag("slimmedTaus"),
    tagPV=cms.untracked.InputTag("offlineSlimmedPrimaryVertices"),
    tagBS=cms.untracked.InputTag("offlineBeamSpot"),
    tagPrunedGenParticles=cms.untracked.InputTag("prunedGenParticles"),
    tagPackedGenParticles=cms.untracked.InputTag("packedGenParticles"),
    tagTriggerResults=cms.untracked.InputTag("TriggerResults", "", "HLT"),
    tagTriggerObjects=cms.untracked.InputTag("slimmedPatTrigger"),
    tagMetFilterResults=cms.untracked.InputTag("TriggerResults", "", "RECO"),
    tagMET=cms.untracked.InputTag("slimmedMETsModifiedMET"),
    tagJets=cms.untracked.InputTag("updatedPatJetsUpdatedJEC"),
    tagRho = cms.untracked.InputTag("fixedGridRhoFastjetAll"),
    tagGenJets=cms.untracked.InputTag("slimmedGenJets"),
    tagConversions=cms.untracked.InputTag("reducedEgamma:reducedConversions"),
    
    rochesterFile=cms.FileInPath("HMuMu/NtupleMaking/data/Roccor/RoccoR2017.txt"),
    btagFile=cms.FileInPath("HMuMu/NtupleMaking/data/BtagSF/DeepCSV_94XSF_V4_B_F.csv"),
    muonIsoFile=cms.FileInPath("HMuMu/NtupleMaking/data/MuonSF/RunBCDEF_SF_ISO.json"),
    muonIdFile=cms.FileInPath("HMuMu/NtupleMaking/data/MuonSF/RunBCDEF_SF_ID.json"),
    muonTrigFile=cms.FileInPath("HMuMu/NtupleMaking/data/MuonSF/EfficienciesAndSF_RunBtoF_Nov17Nov2017.root"),
   
    muon_id_sf_wp_num = cms.string("MediumID"),
    muon_id_sf_wp_den = cms.string("genTracks"),
    muon_iso_sf_wp_num = cms.string("LooseRelIso"),
    muon_iso_sf_wp_den = cms.string("MediumID"),

    #
    #	Meta Data
    #
    checkTrigger=cms.untracked.bool(True),
    isMC=cms.untracked.bool(False),
    triggerNames=cms.untracked.vstring(
        "HLT_IsoMu%d" % pt, "HLT_IsoTkMu%d" % pt),
    metFilterNames=cms.untracked.vstring(["Flag_goodVertices", "Flag_globalSuperTightHalo2016Filter", "Flag_HBHENoiseFilter", "Flag_HBHENoiseIsoFilter",
                                          "Flag_EcalDeadCellTriggerPrimitiveFilter", "Flag_BadPFMuonFilter", "Flag_BadChargedCandidateFilter"]),

    nMuons=cms.untracked.int32(2),
    isGlobalMuon=cms.untracked.bool(True),
    isStandAloneMuon=cms.untracked.bool(False),
    isTrackerMuon=cms.untracked.bool(True),
    minPt=cms.untracked.double(20),
    maxeta=cms.untracked.double(2.4),
    btagNames=cms.untracked.vstring(
        ["pfDeepCSVJetTags:probb", "pfDeepCSVJetTags:probbb"]),
    tauIDNames=cms.untracked.vstring([""]),

    #
    #  flags
    #
    useElectrons=cms.untracked.bool(False),
    useTaus=cms.untracked.bool(False),
)