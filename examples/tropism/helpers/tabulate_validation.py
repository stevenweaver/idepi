import json, sys, csv, argparse, operator, re
from math import sqrt

ccr5_res = re.compile ('^.+\_R5\_.*$')

parser = argparse.ArgumentParser(
    description='tabulate validation results for the tropism example')


parser.add_argument (
    '-j', '--json',
    type=argparse.FileType('r'),
    help='IDEPI prediction file',
    required = True,
)


def report (cfm):
    N = sum ([sum (k) for k in cfm])
    accu  = (cfm[0][0] + cfm[1][1]) / N
    specificity = cfm[1][1] / (cfm [0][1] + cfm[1][1])
    sensitivity = cfm[1][1] / (cfm[1][0] + cfm[1][1])
    mcc = (cfm[1][1]*cfm[0][0]-cfm[1][0]*cfm[0][1])/sqrt ((cfm[1][1]+cfm[0][1])*(cfm[1][1]+cfm[1][0])*(cfm[0][0]+cfm[0][1])*(cfm[0][0]+cfm[1][0]))

    return [specificity, sensitivity, accu, mcc]
    

args = None
retcode = -1
args = parser.parse_args()

labels = json.load (args.json)['predictions']
idepi_ids = {}

confusion_matrix = [[0,0],[0,0]]

for s in labels:
    row = 0 if ccr5_res.match (s["id"]) is not None else 1
    column = 1 if s["value"] > 0 else 0
    
    confusion_matrix[row][column] += 1


        
N = sum ([sum (r) for r in confusion_matrix])        

print ("\nN = %d\n" % N)

print (  "IDEPI     Measured     Count   Percentage",
       "\nCCR5      CCR5         %6d    %.3g" % (confusion_matrix[0][0], confusion_matrix[0][0]/N*100.),
       "\nCXCR4     CXCR4        %6d    %.3g" % (confusion_matrix[1][1], confusion_matrix[1][1]/N*100.),
       "\nCCR5      CXCR4        %6d    %.3g" % (confusion_matrix[0][1], confusion_matrix[0][1]/N*100.),
       "\nCXCR4     CCR5         %6d    %.3g" % (confusion_matrix[1][0], confusion_matrix[1][0]/N*100.))
       
metrics = report (confusion_matrix)
 
print ("\nSpecificity %.2g" %   metrics[0],
       "\nSensitivity %.2g" %   metrics[1],
       "\nAccuracy    %.2g" %   metrics[2],
       "\nMCC         %.2g" %   metrics[3])
       
#print ("\nCohen's kappa = %g" % Cohen_kappa(confusion_matrix))        



