import requests
import os
import tempfile
import csv

'''
TODO:

1. stitch together data files into one text file that can be pasted into excel
2. fasta if possible only
3. delete the data files after finished stitching
4. fix that print thing with the mod to cover 3 outcomes
5. make sure to delete things

'''

input_string = input("Enter a list of geneIDs separated by spaces ")

print("\n")
genes = input_string.split()
print("your gene library is ", genes, "\n")

def saveFolder(gene, data, url, mod):
  if mod is not "data":
    if gene not in os.listdir():
        os.mkdir(gene)    
    #the mod will be like "data" or "gint" or "prot"
    f = open(gene + '/{}'.format(mod) + gene + '.out', 'w')
    f.write(requests.post(url, data = data).text)
    print('recorded ' + gene + ' {} sequence'.format("protein" if mod == "prot" else "with/without intron"))
    f.close()
  else:
    if gene not in os.listdir():
      os.mkdir(gene)
    os.mkdir(gene + '/data')
    f = open(gene + "/data/{}".format(mod)+gene+'.out', 'w')
    f.write(requests.post(url, data = data).text)
    print('recorded ' + gene + ' {} sequence'.format("data"))
    f.close()


for gene in genes:
    url = 'https://plasmodb.org/plasmo/service/answer/report'

    data = {
        'data':
        '{"answerSpec":{"questionName":"__GeneRecordClasses.GeneRecordClass__singleRecordQuestion__","parameters":{"primaryKeys":"PF3D7_0419900,PlasmoDB"}},"formatting":{"format":"fullRecord","formatConfig":{"attributes":["primary_key","chromosome"],"tables":["Alias","GeneLocation","OrthologsLite","pfal3D7_phenotype_pB_mutagenesis_MIS_MFS_RSRC","SignalP","TMHMM","GOTerms","Notes","ProteinProperties"],"includeEmptyTables":true,"attachmentType":"plain"}}}'
    }

    
    saveFolder(gene, data, url, "data")

for gene in genes:
    url = 'https://plasmodb.org/plasmo/service/answer/report'

    data = {
        'data':
        '{"answerSpec":{"questionName":"__GeneRecordClasses.GeneRecordClass__singleRecordQuestion__","parameters":{"primaryKeys":"PF3D7_0419900,PlasmoDB"}},"formatting":{"format":"srt","formatConfig":{"attachmentType":"plain","endOffset3":0,"type":"genomic","sourceIdFilter":"genesOnly","upstreamAnchor":"Start","upstreamSign":"plus","upstreamOffset":0,"downstreamAnchor":"End","downstreamSign":"plus","downstreamOffset":0,"onlyIdDefLine":"0","noLineBreaks":"0","startAnchor3":"Start","startOffset3":0,"endAnchor3":"End"}}}'
    }

    saveFolder(gene, data, url, "gint")

for gene in genes:
    url = 'https://plasmodb.org/plasmo/service/answer/report'

    data = {
        'data':
        '{"answerSpec":{"questionName":"__GeneRecordClasses.GeneRecordClass__singleRecordQuestion__","parameters":{"primaryKeys":"PF3D7_0419900,PlasmoDB"}},"formatting":{"format":"srt","formatConfig":{"attachmentType":"plain","endOffset3":0,"type":"CDS","sourceIdFilter":"genesOnly","upstreamAnchor":"Start","upstreamSign":"plus","upstreamOffset":0,"downstreamAnchor":"End","downstreamSign":"plus","downstreamOffset":0,"onlyIdDefLine":"0","noLineBreaks":"0","startAnchor3":"Start","startOffset3":0,"endAnchor3":"End"}}}'
    }

    saveFolder(gene, data, url, "gseq")

for gene in genes:
    url = 'https://plasmodb.org/plasmo/service/answer/report'

    data = {
        'data':
        '{"answerSpec":{"questionName":"__GeneRecordClasses.GeneRecordClass__singleRecordQuestion__","parameters":{"primaryKeys":"PF3D7_0419900,PlasmoDB"}},"formatting":{"format":"srt","formatConfig":{"attachmentType":"plain","endOffset3":0,"type":"protein","sourceIdFilter":"genesOnly","upstreamAnchor":"Start","upstreamSign":"plus","upstreamOffset":0,"downstreamAnchor":"End","downstreamSign":"plus","downstreamOffset":0,"onlyIdDefLine":"0","noLineBreaks":"0","startAnchor3":"Start","startOffset3":0,"endAnchor3":"End"}}}'
    }

    saveFolder(gene, data, url, "prot")

print('query complete')
