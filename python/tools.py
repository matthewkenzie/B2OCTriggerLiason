#!/usr/bin/env python
import ROOT as r
import sys

def getLumi( tf ):

  tree = tf.Get('GetIntegratedLuminosity/LumiTuple')
  if not tree:
    sys.exit('Tools: cannot getLumi as tree is null')
  lumi = 0.
  for ev in range(tree.GetEntries()):
    tree.GetEntry(ev)
    lumi += tree.IntegratedLuminosity

  return lumi

def printInfo(lumi, ntuples):

  print '%5s  |  %8s  |  %6s  |  %10s  |  %10s  |'%('Year','Decay','Lumi','Events','Events/pb')
  for i in range(62): sys.stdout.write('-')
  print ''

  for year, trees in ntuples.iteritems():
    for decay, tree in trees.iteritems():
      print '%-5s  |  %-8s  |  %6.2f  |  %10d  |  %10.2f  |'%(year,decay,lumi[year][decay],tree.GetEntries(), float(tree.GetEntries())/lumi[year][decay])

def printEvDict( ev_dict, name='' ) :

  for i in range(78): sys.stdout.write('-')
  print ''
  print name
  for i in range(78): sys.stdout.write('-')
  print ''
  print '   %5s  |  %8s  |  %6s  |  %10s  |  %10s +/- %8s  |'%('Year','Decay','Lumi','Events','Events/pb','Err')
  for i in range(78): sys.stdout.write('-')
  print ''

  for year, events in ev_dict.iteritems():
    for decay, ev in events.iteritems():

      evs = ev[1]
      evs_err = float(ev[1])**0.5
      lumi = ev[0]
      lumi_err = 0.03*lumi
      evs_per_pb = float(ev[1]/ev[0])
      evs_per_pb_err = evs_per_pb
      if evs>0:
        evs_per_pb_err = evs_per_pb*( (evs_err/evs)**2 + (lumi_err/lumi)**2 )**0.5
      print '   %-5s  |  %-8s  |  %6.2f  |  %10d  |  %10.2f +/- %8.2f  |'%(year,decay,ev[0],ev[1],evs_per_pb, evs_per_pb_err)

  for i in range(78): sys.stdout.write('-')
  print ''

def getEventDict( name, lumi, ntuples, all_cuts={}, specific_cuts={} ) :

  ev_dict = {}
  for year, trees in ntuples.iteritems():
    ev_dict[year] = {}
    for decay, tree in trees.iteritems():
      print year, decay
      all_cut  = all_cuts[year] if year in all_cuts.keys() else r.TCut()
      spec_cut = specific_cuts[decay] if decay in specific_cuts.keys() else r.TCut()
      the_cut = all_cut + spec_cut
      evs = tree.GetEntries(str(the_cut))
      ev_dict[year][decay] = [ lumi[year][decay], evs ]

  printEvDict( ev_dict, name )
  return ev_dict

def convertToCompHists( ev_dict, name='', title='' ) :

  list_of_all_decay_keys = []
  for year, decays_dict in ev_dict.iteritems():
    list_of_all_decay_keys.append( decays_dict.keys() )
  common_keys = set(list_of_all_decay_keys[0]).intersection(*list_of_all_decay_keys)

  # one histogram bin for each common key
  # and one histogram for each year
  th1fs = []
  for year in sorted(ev_dict.keys()):
    decays_dict = ev_dict[year]
    th1fs.append( r.TH1F('%s_%s'%(name,year),year,len(common_keys),0,len(common_keys)) )
    for i, bin_name in enumerate(common_keys):
      th1fs[-1].GetXaxis().SetBinLabel(i+1,bin_name)
      evs = decays_dict[bin_name][1]
      evs_err = decays_dict[bin_name][1]**0.5
      lumi = decays_dict[bin_name][0]
      lumi_err = 0.03*decays_dict[bin_name][0]
      evs_per_pb = evs/lumi
      evs_per_pb_err = evs_per_pb
      if evs>0:
        evs_per_pb_err = evs_per_pb*( (evs_err/evs)**2 + (lumi_err/lumi)**2 )**0.5
      th1fs[-1].SetBinContent( i+1, evs_per_pb)
      th1fs[-1].SetBinError( i+1, evs_per_pb_err )

  max_val = 0.
  for th1f in th1fs: max_val = max(max_val,th1f.GetMaximum())

  colors = [r.kBlue, r.kRed, r.kGreen+1 ]

  r.gROOT.ProcessLine(".x ~/lhcbStyle.C")
  r.gROOT.ProcessLine(".x ~/Scratch/lhcb/lhcbStyle.C")
  canv = r.TCanvas()
  canv.SetTopMargin(0.13)
  leg = r.TLegend(0.15,0.88,0.3,1.)
  leg.SetFillColor(0)
  for i, th1f in enumerate(th1fs):
    th1f.GetYaxis().SetRangeUser(0.,1.1*max_val)
    th1f.GetYaxis().SetTitle("Events / pb")
    th1f.GetXaxis().SetTitle("Decay Channel")
    th1f.GetXaxis().SetLabelSize(0.05)
    th1f.GetXaxis().SetTitleSize(0.05)
    th1f.GetYaxis().SetLabelSize(0.05)
    th1f.GetYaxis().SetTitleSize(0.05)
    th1f.GetYaxis().SetTitleOffset(1.2)
    th1f.SetLineColor( colors[i] )
    th1f.SetLineWidth(2)
    th1f.SetMarkerColor( colors[i] )
    th1f.SetMarkerSize(1.5)
    leg.AddEntry(th1f, th1f.GetTitle(), "L")
    if i==0:
      th1f.Draw("HISTTEXT00")
    else:
      th1f.Draw("HISTTEXT00SAME")

  pave = r.TPaveText(0.4,0.92,0.6,0.98,"ndc")
  pave.SetFillColor(0)
  pave.SetTextSize(0.05)
  pave.AddText(title)
  pave.Draw("same")
  leg.Draw("same")
  canv.Update()
  canv.Modified()

  return [canv, th1fs, leg, pave]

def makePlot( name, title, lumi, ntuples, cut_list, spec_cuts) :

  comb_cuts = {}
  for cut_dict in cut_list:
    for year, cut in cut_dict.iteritems():
      if year in comb_cuts.keys():
        comb_cuts[year] += cut
      else:
        comb_cuts[year] = cut

  raw_evs = getEventDict( title, lumi, ntuples, comb_cuts, spec_cuts )
  objs = convertToCompHists( raw_evs, name, title )
  objs[0].Print("plots/%s.pdf"%name)
  return objs

def makeDist( name, title, var, bins, xmin, xmax, ntuples, cut_list, spec_cuts ):

  r.gROOT.ProcessLine('.x ~/Scratch/lhcb/lhcbStyle.C')

  comb_cuts = {}
  for cut_dict in cut_list:
    for year, cut in cut_dict.iteritems():
      if year in comb_cuts.keys():
        comb_cuts[year] += cut
      else:
        comb_cuts[year] = cut

  th1fs = {}
  for year, dec_tup in ntuples.iteritems():
    th1fs[year] = {}
    for decay, ntuple in dec_tup.items():
      all_cut  = comb_cuts[year] if year in comb_cuts.keys() else r.TCut()
      spec_cut = spec_cuts[decay] if decay in spec_cuts.keys() else r.TCut()
      the_cut = all_cut + spec_cut
      if decay in ['D2KP', 'D2K3P', 'D24P']:
        th1f_name = '%s_%s_%s_%s'%(name,year,decay,var)
        th1f = r.TH1F(th1f_name, title, bins, xmin, xmax)
        var_draw = var
        if year=='2012' and var=='L0Data_Spd_Mult':
          var_draw = 'nSPDHits'
        ntuple.Draw('%s>>%s'%(var_draw,th1f_name), the_cut, 'goff')
        th1fs[year][decay] = th1f

  colors = [r.kBlue, r.kGreen+1, r.kRed]
  for decay in ['D2KP', 'D2K3P', 'D24P']:
    canv = r.TCanvas()
    leg = r.TLegend(0.6,0.6,0.89,0.89)
    leg.SetFillColor(0)
    for i, year in enumerate(th1fs.keys()):
      if year == '2015_tl0' : continue
      th1fs[year][decay].SetLineWidth(2)
      th1fs[year][decay].SetLineColor(colors[i])
      th1fs[year][decay].GetXaxis().SetTitle(var)
      th1fs[year][decay].GetXaxis().SetTitleOffset(0.8)
      if th1fs[year][decay].GetEntries()>0:
        th1fs[year][decay].Scale(1./th1fs[year][decay].Integral())
      leg.AddEntry(th1fs[year][decay], year, "L")
      if i==0:
        th1fs[year][decay].Draw("HIST")
      else:
        th1fs[year][decay].Draw("HISTsame")
    leg.Draw("same")
    canv.Update()
    canv.Modified()
    canv.Print("plots/%s_%s_%s.pdf"%(name,var,decay))

  return [canv, th1fs, leg]


