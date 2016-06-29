#!/bin/bash
export OUTDIR=/afs/cern.ch/user/g/gkrintir/PbPb_Top1/topskim/test
cd /afs/cern.ch/user/g/gkrintir/PbPb_Top1/topskim/
root -l  -q -b makeEMuSkim_OnBatch2.C'("data.txt", 2, 4, "test_data.root", false)'
export OUTPUT=AnaResults_2.root
cp test_data.root $OUTDIR/$OUTPUT
rm test_data.root
