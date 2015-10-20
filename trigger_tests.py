#!/usr/bin/env python

#################################################
# cheeky little script to check B2OC trigger stuff
#################################################

import ROOT as r
from python.tools import getLumi
from python.tools import printInfo
from python.tools import getEventDict
from python.tools import convertToCompHists
from python.tools import makePlot
from python.tools import makeDist

######
## setup files and trees into dictionary
######
tf_2body_2012 = r.TFile('Bu2D0X_twobody_2012_sample_1_44_percent.root')
tf_2body_2015 = r.TFile('Bu2D0X_twobody_2015_mu_S23test.root')
tf_4body_2012 = r.TFile('Bu2D0X_2012_sample.root')
tf_4body_2015 = r.TFile('Bu2D0X_2015_mu_S23test.root')

lumi_2body_2012 = 0.0144*2000.
lumi_4body_2012 = getLumi( tf_4body_2012 )
lumi_2body_2015 = getLumi( tf_2body_2015 )
lumi_4body_2015 = getLumi( tf_4body_2015 )

lumi    = { '2012' : { 'D2KP'    : lumi_2body_2012 ,
                       'D2K3P'   : lumi_4body_2012 ,
                       'D24P'    : lumi_4body_2012 ,
                     } ,

            '2015' : { 'D2KP'    : lumi_2body_2015 ,
                       'D2KPSUP' : lumi_2body_2015 ,
                       'D2KK'    : lumi_2body_2015 ,
                       'D2PP'    : lumi_2body_2015 ,
                       'D2KKP'   : lumi_4body_2015 ,
                       'D2PPP'   : lumi_4body_2015 ,
                       'D2KPP'   : lumi_4body_2015 ,
                       'D2KPPSUP': lumi_4body_2015 ,
                       'D2K3P'   : lumi_4body_2015 ,
                       'D2K3PSUP': lumi_4body_2015 ,
                       'D24P'    : lumi_4body_2015 ,
                       'D2KKPP'  : lumi_4body_2015 ,
                     } ,
            '2015_tl0' : { 'D2KP'    : lumi_2body_2015 ,
                       'D2KPSUP' : lumi_2body_2015 ,
                       'D2KK'    : lumi_2body_2015 ,
                       'D2PP'    : lumi_2body_2015 ,
                       'D2KKP'   : lumi_4body_2015 ,
                       'D2PPP'   : lumi_4body_2015 ,
                       'D2KPP'   : lumi_4body_2015 ,
                       'D2KPPSUP': lumi_4body_2015 ,
                       'D2K3P'   : lumi_4body_2015 ,
                       'D2K3PSUP': lumi_4body_2015 ,
                       'D24P'    : lumi_4body_2015 ,
                       'D2KKPP'  : lumi_4body_2015 ,
                     }
           }

ntuples = { '2012' : { 'D2KP'    : tf_2body_2012.Get('Bu2Dst0piFAVTuple/DecayTree')  ,
                       'D2K3P'   : tf_4body_2012.Get('B2DPi_D2K3Pi/DecayTree')       ,
                       'D24P'    : tf_4body_2012.Get('B2DPi_D24Pi/DecayTree')
                     } ,

            '2015' : { 'D2KP'    : tf_2body_2015.Get('Bu2D0pi_D02KPiFAVTuple/Bu2D0X') ,
                       'D2KPSUP' : tf_2body_2015.Get('Bu2D0pi_D02KPiSUPTuple/Bu2D0X') ,
                       'D2KK'    : tf_2body_2015.Get('Bu2D0pi_D02KKTuple/Bu2D0X')     ,
                       'D2PP'    : tf_2body_2015.Get('Bu2D0pi_D02PiPiTuple/Bu2D0X')   ,
                       'D2KKP'   : tf_4body_2015.Get('Bu2D0pi_D02KKPi0ResolvedTuple/Bu2D0X') ,
                       'D2PPP'   : tf_4body_2015.Get('Bu2D0pi_D02PiPiPi0ResolvedTuple/Bu2D0X') ,
                       'D2KPP'   : tf_4body_2015.Get('Bu2D0pi_D02KPiPi0FAVResolvedTuple/Bu2D0X') ,
                       'D2KPPSUP': tf_4body_2015.Get('Bu2D0pi_D02KPiPi0SUPResolvedTuple/Bu2D0X') ,
                       'D2K3P'   : tf_4body_2015.Get('Bu2D0pi_D02K3PiFAVTuple/Bu2D0X') ,
                       'D2K3PSUP': tf_4body_2015.Get('Bu2D0pi_D02K3PiSUPTuple/Bu2D0X') ,
                       'D24P'    : tf_4body_2015.Get('Bu2D0pi_D024PiTuple/Bu2D0X') ,
                       'D2KKPP'  : tf_4body_2015.Get('Bu2D0pi_D02KKPiPiTuple/Bu2D0X') ,
                     } ,
            '2015_tl0' : { 'D2KP'    : tf_2body_2015.Get('Bu2D0pi_D02KPiFAVTuple/Bu2D0X') ,
                       'D2KPSUP' : tf_2body_2015.Get('Bu2D0pi_D02KPiSUPTuple/Bu2D0X') ,
                       'D2KK'    : tf_2body_2015.Get('Bu2D0pi_D02KKTuple/Bu2D0X')     ,
                       'D2PP'    : tf_2body_2015.Get('Bu2D0pi_D02PiPiTuple/Bu2D0X')   ,
                       'D2KKP'   : tf_4body_2015.Get('Bu2D0pi_D02KKPi0ResolvedTuple/Bu2D0X') ,
                       'D2PPP'   : tf_4body_2015.Get('Bu2D0pi_D02PiPiPi0ResolvedTuple/Bu2D0X') ,
                       'D2KPP'   : tf_4body_2015.Get('Bu2D0pi_D02KPiPi0FAVResolvedTuple/Bu2D0X') ,
                       'D2KPPSUP': tf_4body_2015.Get('Bu2D0pi_D02KPiPi0SUPResolvedTuple/Bu2D0X') ,
                       'D2K3P'   : tf_4body_2015.Get('Bu2D0pi_D02K3PiFAVTuple/Bu2D0X') ,
                       'D2K3PSUP': tf_4body_2015.Get('Bu2D0pi_D02K3PiSUPTuple/Bu2D0X') ,
                       'D24P'    : tf_4body_2015.Get('Bu2D0pi_D024PiTuple/Bu2D0X') ,
                       'D2KKPP'  : tf_4body_2015.Get('Bu2D0pi_D02KKPiPiTuple/Bu2D0X') ,
                     }
           }

######
## define cuts
######
common_cuts = { '2012'     : r.TCut('Bu_DPVCFIT_CHI2>0 && D0_M > 1839.86 && D0_M < 1889.86 && Bach_PIDK<4') ,
                '2015'     : r.TCut('Bu_DPVCFIT_CHI2>0 && D0_M > 1839.86 && D0_M < 1889.86 && Bach_PIDK<4') ,
                '2015_tl0' : r.TCut('Bu_DPVCFIT_CHI2>0 && D0_M > 1839.86 && D0_M < 1889.86 && Bach_PIDK<4')
              }
bu_mass_cut = { '2012'     : r.TCut('Bu_M > 5247 && Bu_M < 5317') ,
                '2015'     : r.TCut('Bu_M > 5247 && Bu_M < 5317') ,
                '2015_tl0' : r.TCut('Bu_M > 5247 && Bu_M < 5317')
              }
l0     = { '2012'     : r.TCut('Bu_L0HadronDecision_TOS') ,
           '2015'     : r.TCut('Bu_L0HadronDecision_TOS') ,
           '2015_tl0' : r.TCut('Bu_L0HadronDecision_TOS && (L0Data_Hadron_Et*24 > 4500 || L0Data_Electron_Et*24 > 2700 || L0Data_Photon_Et*24 > 2700 || L0Data_Muon1_Pt*50 > 2800 || L0Data_DiMuon_Pt*50 > 1800)')
         }
hlt1   = { '2012'     : r.TCut('Bu_Hlt1TrackAllL0Decision_TOS') ,
           '2015'     : r.TCut('Bu_Hlt1TrackMVADecision_TOS || Bu_Hlt1TwoTrackMVADecision_TOS') ,
           '2015_tl0' : r.TCut('Bu_Hlt1TrackMVADecision_TOS || Bu_Hlt1TwoTrackMVADecision_TOS')
         }
hlt2   = { '2012'     : r.TCut('Bu_Hlt2Topo2BodyBBDTDecision_TOS || Bu_Hlt2Topo3BodyBBDTDecision_TOS || Bu_Hlt2Topo4BodyBBDTDecision_TOS') ,
           '2015'     : r.TCut('Bu_Hlt2Topo2BodyDecision_TOS || Bu_Hlt2Topo3BodyDecision_TOS || Bu_Hlt2Topo4BodyDecision_TOS || Bu_Hlt2TopoOSTF2BodyDecision_TOS || Bu_Hlt2TopoOSTF3BodyDecision_TOS || Bu_Hlt2TopoOSTF4BodyDecision_TOS') ,
           '2015_tl0' : r.TCut('Bu_Hlt2Topo2BodyDecision_TOS || Bu_Hlt2Topo3BodyDecision_TOS || Bu_Hlt2Topo4BodyDecision_TOS || Bu_Hlt2TopoOSTF2BodyDecision_TOS || Bu_Hlt2TopoOSTF3BodyDecision_TOS || Bu_Hlt2TopoOSTF4BodyDecision_TOS')
         }

hlt2_topo2   = { '2012'     : r.TCut('Bu_Hlt2Topo2BodyBBDTDecision_TOS') ,
                 '2015'     : r.TCut('Bu_Hlt2Topo2BodyDecision_TOS || Bu_Hlt2TopoOSTF2BodyDecision_TOS') ,
                 '2015_tl0' : r.TCut('Bu_Hlt2Topo2BodyDecision_TOS || Bu_Hlt2TopoOSTF2BodyDecision_TOS')
         }

hlt2_topo3   = { '2012'     : r.TCut('Bu_Hlt2Topo3BodyBBDTDecision_TOS') ,
                 '2015'     : r.TCut('Bu_Hlt2Topo3BodyDecision_TOS || Bu_Hlt2TopoOSTF3BodyDecision_TOS') ,
                 '2015_tl0' : r.TCut('Bu_Hlt2Topo3BodyDecision_TOS || Bu_Hlt2TopoOSTF3BodyDecision_TOS')
         }

hlt2_topo4   = { '2012'     : r.TCut('Bu_Hlt2Topo4BodyBBDTDecision_TOS') ,
                 '2015'     : r.TCut('Bu_Hlt2Topo4BodyDecision_TOS || Bu_Hlt2TopoOSTF4BodyDecision_TOS') ,
                 '2015_tl0' : r.TCut('Bu_Hlt2Topo4BodyDecision_TOS || Bu_Hlt2TopoOSTF4BodyDecision_TOS')
         }

pid_cuts = {  'D2KP'    : r.TCut('K_PIDK>2 && P_PIDK<-2') ,
              'D2KPSUP' : r.TCut('K_PIDK>2 && P_PIDK<-2') ,
              'D2KK'    : r.TCut('K0_PIDK>2 && K1_PIDK>2') ,
              'D2PP'    : r.TCut('P0_PIDK<-2 && P1_PIDK<-2') ,
              'D2KKP'   : r.TCut('K0_PIDK>2 && K1_PIDK>2') ,
              'D2PPP'   : r.TCut('P0_PIDK<-2 && P1_PIDK<-2') ,
              'D2KPP'   : r.TCut('K_PIDK>2 && P_PIDK<-2') ,
              'D2KPPSUP': r.TCut('K_PIDK>2 && P_PIDK<-2') ,
              'D2K3P'   : r.TCut('K_PIDK>2 && P0_PIDK<-2 && P1_PIDK<-2 && P2_PIDK<-2') ,
              'D2K3PSUP': r.TCut('K_PIDK>2 && P0_PIDK<-2 && P1_PIDK<-2 && P2_PIDK<-2') ,
              'D24P'    : r.TCut('P0_PIDK<-2 && P1_PIDK<-2 && P2_PIDK<-2 && P3_PIDK<-2') ,
              'D2KKPP'  : r.TCut('K0_PIDK>2 && K1_PIDK>2 && P0_PIDK<-2 && P1_PIDK<-2')
            }

# print info
#printInfo(lumi,ntuples)

#objs = {
  #'no_cuts'              : makePlot( 'no_cuts'              , 'No Cuts'                          , lumi, ntuples, [], {} )                                            ,
  #'sel_cuts'             : makePlot( 'sel_cuts'             , 'Selection Cuts'                   , lumi, ntuples, [common_cuts]                          , pid_cuts ) ,
  #'sel_cuts_bu_mass'     : makePlot( 'sel_cuts_bu_mass'     , 'Sel Cuts w/ Mass Window'          , lumi, ntuples, [common_cuts,bu_mass_cut]              , pid_cuts ) ,
  #'sel_cuts_bu_mass_l0'  : makePlot( 'sel_cuts_bu_mass_l0'  , 'Sel Cuts w/ Mass w/ L0'           , lumi, ntuples, [common_cuts,bu_mass_cut,l0]           , pid_cuts ) ,
  #'sel_cuts_bu_mass_hlt1': makePlot( 'sel_cuts_bu_mass_hlt1', 'Sel Cuts w/ Mass w/ L0+HLT1'      , lumi, ntuples, [common_cuts,bu_mass_cut,l0,hlt1]      , pid_cuts ) ,
  #'sel_cuts_bu_mass_hlt2': makePlot( 'sel_cuts_bu_mass_hlt2', 'Sel Cuts w/ Mass w/ L0+HLT1+HLT2' , lumi, ntuples, [common_cuts,bu_mass_cut,l0,hlt1,hlt2] , pid_cuts )
#}

#objs = {
  #'hlt2_2body'         : makePlot( 'hlt2_2body',   'Hlt2 2-body',  lumi,  ntuples, [common_cuts,bu_mass_cut,hlt2_topo2] , pid_cuts ) ,
  #'hlt2_3body'         : makePlot( 'hlt2_3body',   'Hlt2 3-body',  lumi,  ntuples, [common_cuts,bu_mass_cut,hlt2_topo3] , pid_cuts ) ,
  #'hlt2_4body'         : makePlot( 'hlt2_4body',   'Hlt2 4-body',  lumi,  ntuples, [common_cuts,bu_mass_cut,hlt2_topo4] , pid_cuts )
#}

dist_objs = {
    #'Bu_M'      :   makeDist( 'no_cuts',  'No Cuts', 'Bu_M', 50, 4750, 7000, ntuples, [], {} )        ,
    #'SPD'       :   makeDist( 'no_cuts',  'No Cuts', 'L0Data_Spd_Mult', 50, 0, 1000, ntuples, [], {} ) ,
    #'Bu_M_pid'  :   makeDist( 'pid_cuts', 'PID Cuts', 'Bu_M', 50, 4750, 7000, ntuples, [], pid_cuts )        ,
    #'SPD_pid'   :   makeDist( 'pid_cuts', 'PID Cuts', 'L0Data_Spd_Mult', 50, 0, 1000, ntuples, [], pid_cuts ) ,
    'Bu_M_sel'  :   makeDist( 'sel_cuts', 'Sel Cuts', 'Bu_M', 50, 4750, 7000, ntuples, [common_cuts], pid_cuts )        ,
    #'SPD_sel'   :   makeDist( 'sel_cuts', 'Sel Cuts', 'L0Data_Spd_Mult', 50, 0, 1000, ntuples, [common_cuts], pid_cuts ) ,
    #'Bu_M_l0'   :   makeDist( 'l0_cuts',  'L0 Cuts', 'Bu_M', 50, 4750, 7000, ntuples, [l0], {} )        ,
    #'SPD_l0'    :   makeDist( 'l0_cuts',  'L0 Cuts', 'L0Data_Spd_Mult', 50, 0, 1000, ntuples, [l0], {} )
}
raw_input()
