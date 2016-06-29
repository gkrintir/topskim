bsub -q 1nd -J runJob_1 -o runJob_1.log < runJob_1.sh
bsub -q 1nd -J runJob_2 -o runJob_2.log < runJob_2.sh
