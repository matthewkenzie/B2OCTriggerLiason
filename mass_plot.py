#!/usr/bin/env python

import ROOT as r
r.gROOT.ProcessLine(".x ~/Scratch/lhcb/lhcbStyle.C")
r.TH1.SetDefaultSumw2()

tf_2body_2012 = r.TFile('Bu2D0X_twobody_2012_sample_1_44_percent.root')
tf_2body_2015 = r.TFile('Bu2D0X_twobody_2015_mu_S23test.root')
tf_4body_2012 = r.TFile('Bu2D0X_2012_sample.root')
tf_4body_2015 = r.TFile('Bu2D0X_2015_mu_S23test.root')

ntuples = {
      '2012_KP'  : tf_2body_2012.Get('Bu2Dst0piFAVTuple/DecayTree')   ,
      '2012_K3P' : tf_4body_2012.Get('B2DPi_D2K3Pi/DecayTree')        ,
      '2015_KP'  : tf_2body_2015.Get('Bu2D0pi_D02KPiFAVTuple/Bu2D0X') ,
      '2015_K3P' : tf_4body_2015.Get('Bu2D0pi_D02K3PiFAVTuple/Bu2D0X')
    }

def getHists(ntuples):

  th1fs = {}
  ymax = 0.
  for name, tree in ntuples.iteritems():

    th1fs[name] = r.TH1F(name,'',100,4750,7000)
    tree.Draw('Bu_M>>%s'%name,'','goff')
    th1fs[name].Scale(1./th1fs[name].Integral())
    ymax = max(ymax,th1fs[name].GetMaximum())

  return (th1fs, ymax)

def drawCompTwo( name, h1, h2 ):

  canv = r.TCanvas()
  leg = r.TLegend(0.6,0.6,0.89,0.89)
  leg.SetFillColor(0)
  colors = [ r.kRed, r.kBlue ]
  h1.SetLineColor(colors[0])
  h2.SetLineColor(colors[1])
  h1.SetLineWidth(2)
  h2.SetLineWidth(2)
  ymax = max( h1.GetMaximum(), h2.GetMaximum() )
  h1.GetYaxis().SetRangeUser(0,ymax*1.1)
  h2.GetYaxis().SetRangeUser(0,ymax*1.1)
  leg.AddEntry(h1, h1.GetName(), "L" )
  leg.AddEntry(h2, h2.GetName(), "L" )
  h1.Draw("HIST")
  h2.Draw("HISTsame")
  leg.Draw("same")
  canv.Update()
  canv.Modified()
  canv.Print("plots/%s.pdf"%name)

  return (canv,leg)

th1fs, ymax = getHists(ntuples)
print th1fs
objs = {
    '2012': drawCompTwo('comp_mass_2012', th1fs['2012_KP'],th1fs['2012_K3P']),
    '2015': drawCompTwo('comp_mass_2015', th1fs['2015_KP'],th1fs['2015_K3P'])
    }

#canv = r.TCanvas()
#leg = r.TLegend(0.6,0.6,0.89,0.89)
#leg.SetFillColor(0)
#colors = [ r.kRed, r.kBlue, r.kMagenta+1, r.kGreen+1 ]
#for i, name in enumerate(th1fs.keys()):
  #th1fs[name].SetLineColor(colors[i])
  #th1fs[name].SetLineWidth(2)
  #th1fs[name].GetYaxis().SetRangeUser(0.,ymax*1.2)
  #color = r.kRed
  #fillcolor = r.kRed-7
  #if 'KP' in name:
    #color = r.kBlue
    #fillcolor = r.kBlue-7
  #col = r.gROOT.GetColor(fillcolor)
  #col.SetAlpha(0.5)

  #th1fs[name].SetFillColor(fillcolor)
  #th1fs[name].SetLineColor(color)
  #th1fs[name].SetMarkerColor(color)
  #th1fs[name].SetLineWidth(2)

  #drawopt = "LEP"
  #if '2015' in name:
    #drawopt = "HISTF"

  #leg.AddEntry(th1fs[name], name, drawopt.replace("HIST","L"))
  #if i==0:
    #th1fs[name].Draw(drawopt)
  #else:
    #th1fs[name].Draw(drawopt+"same")

#leg.Draw("same")
#canv.Update()
#canv.Modified()
#canv.Print("plots/comp_mass_2015.pdf")
#raw_input()
