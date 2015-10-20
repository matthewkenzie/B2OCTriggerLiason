#!usr/bin/env python

import ROOT as r

tf_2body = r.TFile("Bu2D0X_twobody_2015_mu_S23test.root")
tree_2body = tf_2body.Get('Bu2D0pi_D02KPiFAVTuple/Bu2D0X')
tf_4body = r.TFile("Bu2D0X_2015_mu_S23test.root")
tree_4body = tf_4body.Get('Bu2D0pi_D02K3PiFAVTuple/Bu2D0X')

trees = [tree_2body, tree_4body]

r.gROOT.ProcessLine('.x ~/Scratch/lhcb/lhcbStyle.C')
r.gStyle.SetPalette(1)
canvs = []
for i, t in enumerate(trees):

  canvs.append(r.TCanvas('c%d'%i,'c',1000,800))

  canvs[-1].cd()
  canvs[-1].SetRightMargin(0.15)

  t.Draw("L0Data_Hadron_Et:L0Data_Spd_Mult","","colz")

  h = canvs[-1].FindObject('htemp')
  h.Scale(1./h.Integral())
  h.GetXaxis().SetTitleOffset(0.8)
  h.GetYaxis().SetTitleOffset(0.8)
  h.GetZaxis().SetRangeUser(0.,0.02)

  canvs[-1].Update()
  canvs[-1].Modified()

  canvs[-1].Print("plots/plot2d%s.pdf"%i)
