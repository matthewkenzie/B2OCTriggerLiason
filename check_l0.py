import ROOT as r

def printEvs( name, tree, pid_cut_string = 'K_PIDK>2 && P0_PIDK<-2 && P1_PIDK<-2 && P2_PIDK<-2', scale=1. ):

  cut_string = 'Bu_DPVCFIT_CHI2>0 && D0_M > 1839.86 && D0_M < 1889.86 && Bach_PIDK<4 && Bu_M > 5247 && Bu_M < 5317'

  l0     = '( Bu_L0HadronDecision_TOS )'
  hlt1   = '%s && ( Bu_Hlt1TrackMVADecision_TOS || Bu_Hlt1TwoTrackMVADecision_TOS )'%l0
  hlt2   = '%s && ( Bu_Hlt2Topo2BodyDecision_TOS || Bu_Hlt2Topo3BodyDecision_TOS || Bu_Hlt2Topo4BodyDecision_TOS || Bu_Hlt2TopoOSTF2BodyDecision_TOS || Bu_Hlt2TopoOSTF3BodyDecision_TOS || Bu_Hlt2TopoOSTF4BodyDecision_TOS)'%hlt1

  all_cuts = '(%s) && (%s)'%(cut_string,pid_cut_string)

  evs_all  = scale * tree.GetEntries(all_cuts)
  evs_l0   = scale * tree.GetEntries('(%s) && (%s)'%(all_cuts,l0))
  evs_hlt1 = scale * tree.GetEntries('(%s) && (%s)'%(all_cuts,hlt1))
  evs_hlt2 = scale * tree.GetEntries('(%s) && (%s)'%(all_cuts,hlt2))

  all_cuts += ' && (L0Data_Hadron_Et*24 > 2500 || L0Data_Electron_Et*24 > 1700 || L0Data_Photon_Et*24 > 1700 || L0Data_Muon1_Pt*50 > 1800 || L0Data_DiMuon_Pt*50 > 1200)'
  middle_evs_all  = scale * tree.GetEntries(all_cuts)
  middle_evs_l0   = scale * tree.GetEntries('(%s) && (%s)'%(all_cuts,l0))
  middle_evs_hlt1 = scale * tree.GetEntries('(%s) && (%s)'%(all_cuts,hlt1))
  middle_evs_hlt2 = scale * tree.GetEntries('(%s) && (%s)'%(all_cuts,hlt2))

  all_cuts += ' && (L0Data_Hadron_Et*24 > 4500 || L0Data_Electron_Et*24 > 2700 || L0Data_Photon_Et*24 > 2700 || L0Data_Muon1_Pt*50 > 2800 || L0Data_DiMuon_Pt*50 > 1800)'
  tight_evs_all  = scale * tree.GetEntries(all_cuts)
  tight_evs_l0   = scale * tree.GetEntries('(%s) && (%s)'%(all_cuts,l0))
  tight_evs_hlt1 = scale * tree.GetEntries('(%s) && (%s)'%(all_cuts,hlt1))
  tight_evs_hlt2 = scale * tree.GetEntries('(%s) && (%s)'%(all_cuts,hlt2))

  print name
  print '\t all    %5d  %5d  %5d'%( evs_all , middle_evs_all , tight_evs_all )
  print '\t l0     %5d  %5d  %5d'%( evs_l0  , middle_evs_l0  , tight_evs_l0  )
  print '\t hlt1   %5d  %5d  %5d'%( evs_hlt1, middle_evs_hlt1, tight_evs_hlt1)
  print '\t hlt2   %5d  %5d  %5d'%( evs_hlt2, middle_evs_hlt2, tight_evs_hlt2)


# __main__


## -- 4 body --
tf = r.TFile('Bu2D0X_2015_mu_S23test.root')

lumi = 0
lumi_tree = tf.Get('GetIntegratedLuminosity/LumiTuple')
for ev in range(lumi_tree.GetEntries()):
  lumi_tree.GetEntry(ev)
  lumi += lumi_tree.IntegratedLuminosity

print 'Lumi = %5.3fpb'%lumi

print 'Evs per pb in Bu mass'

printEvs( 'K3PiFAV', tf.Get('Bu2D0pi_D02K3PiFAVTuple/Bu2D0X') , 'K_PIDK>2 && P0_PIDK<-2 && P1_PIDK<-2 && P2_PIDK<-2'  , 1./lumi )
printEvs( 'K3PiSUP', tf.Get('Bu2D0pi_D02K3PiSUPTuple/Bu2D0X') , 'K_PIDK>2 && P0_PIDK<-2 && P1_PIDK<-2 && P2_PIDK<-2'  , 1./lumi )
printEvs( '4Pi'    , tf.Get('Bu2D0pi_D024PiTuple/Bu2D0X'    ) , 'P0_PIDK<-2 && P1_PIDK<-2 && P2_PIDK<-2 && P3_PIDK<-2', 1./lumi )
printEvs( 'KKPiPi' , tf.Get('Bu2D0pi_D02KKPiPiTuple/Bu2D0X' ) , 'K0_PIDK>2 && K1_PIDK>2 && P0_PIDK<-2 && P1_PIDK<-2'  , 1./lumi )

tf.Close()

## -- 2 body --
tf = r.TFile('Bu2D0X_twobody_2015_mu_S23test.root')

lumi = 0
lumi_tree = tf.Get('GetIntegratedLuminosity/LumiTuple')
for ev in range(lumi_tree.GetEntries()):
  lumi_tree.GetEntry(ev)
  lumi += lumi_tree.IntegratedLuminosity

print 'Lumi = %5.3fpb'%lumi

print 'Evs per pb in Bu mass'

printEvs( 'KPiFAV', tf.Get('Bu2D0pi_D02KPiFAVTuple/Bu2D0X') , 'K_PIDK>2 && P_PIDK<-2'   , 1./lumi )
printEvs( 'KPiSUP', tf.Get('Bu2D0pi_D02KPiSUPTuple/Bu2D0X') , 'K_PIDK>2 && P_PIDK<-2'   , 1./lumi )
printEvs( 'KK'    , tf.Get('Bu2D0pi_D02KKTuple/Bu2D0X'    ) , 'K0_PIDK>2 && K1_PIDK>2'  , 1./lumi )
printEvs( 'PiPi'  , tf.Get('Bu2D0pi_D02PiPiTuple/Bu2D0X'  ) , 'P0_PIDK<-2 && P1_PIDK<-2', 1./lumi )

