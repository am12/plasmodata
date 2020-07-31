import requests

genes = ['PF3D7_0102900', 'PF3D7_1218800', 'PF3D7_0411200', 'PF3D7_0419900', 'PF3D7_0526600', 'PF3D7_0604600', 'PF3D7_0608900', 'PF3D7_0826000', 'PF3D7_1414700']

for gene in genes:
    url = 'https://plasmodb.org/plasmo/service/answer/report'

    data = {'data': '{"answerSpec":{"questionName":"__GeneRecordClasses.GeneRecordClass__singleRecordQuestion__","parameters":{"primaryKeys":"PF3D7_0419900,PlasmoDB"}},"formatting":{"format":"fullRecord","formatConfig":{"attributes":["primary_key","chromosome"],"tables":["Alias","GeneLocation","OrthologsLite","pfal3D7_phenotype_pB_mutagenesis_MIS_MFS_RSRC","SignalP","TMHMM","GOTerms","Notes","ProteinProperties"],"includeEmptyTables":true,"attachmentType":"plain"}}}'}
        
    with open('data' + gene + '.out', 'w') as f:
        f.write(requests.post(url, data = data).text)
        print('recorded ' + gene + ' report')

for gene in genes:
    url = 'https://plasmodb.org/plasmo/service/answer/report'

    data = {'data': '{"answerSpec":{"questionName":"__GeneRecordClasses.GeneRecordClass__singleRecordQuestion__","parameters":{"primaryKeys":"PF3D7_0419900,PlasmoDB"}},"formatting":{"format":"srt","formatConfig":{"attachmentType":"plain","endOffset3":0,"type":"genomic","sourceIdFilter":"genesOnly","upstreamAnchor":"Start","upstreamSign":"plus","upstreamOffset":0,"downstreamAnchor":"End","downstreamSign":"plus","downstreamOffset":0,"onlyIdDefLine":"0","noLineBreaks":"0","startAnchor3":"Start","startOffset3":0,"endAnchor3":"End"}}}'}

    with open('gint' + gene + '.out', 'w') as f:
        f.write(requests.post(url, data = data).text)
        print('recorded ' + gene + ' genomic sequence with introns')

for gene in genes:
    url = 'https://plasmodb.org/plasmo/service/answer/report'

    data = {'data': '{"answerSpec":{"questionName":"__GeneRecordClasses.GeneRecordClass__singleRecordQuestion__","parameters":{"primaryKeys":"PF3D7_0419900,PlasmoDB"}},"formatting":{"format":"srt","formatConfig":{"attachmentType":"plain","endOffset3":0,"type":"CDS","sourceIdFilter":"genesOnly","upstreamAnchor":"Start","upstreamSign":"plus","upstreamOffset":0,"downstreamAnchor":"End","downstreamSign":"plus","downstreamOffset":0,"onlyIdDefLine":"0","noLineBreaks":"0","startAnchor3":"Start","startOffset3":0,"endAnchor3":"End"}}}'}

    with open('gseq' + gene + '.out', 'w') as f:
        f.write(requests.post(url, data = data).text)
        print('recorded ' + gene + ' genomic sequence without introns')


for gene in genes:
    url = 'https://plasmodb.org/plasmo/service/answer/report'

    data = {'data': '{"answerSpec":{"questionName":"__GeneRecordClasses.GeneRecordClass__singleRecordQuestion__","parameters":{"primaryKeys":"PF3D7_0419900,PlasmoDB"}},"formatting":{"format":"srt","formatConfig":{"attachmentType":"plain","endOffset3":0,"type":"protein","sourceIdFilter":"genesOnly","upstreamAnchor":"Start","upstreamSign":"plus","upstreamOffset":0,"downstreamAnchor":"End","downstreamSign":"plus","downstreamOffset":0,"onlyIdDefLine":"0","noLineBreaks":"0","startAnchor3":"Start","startOffset3":0,"endAnchor3":"End"}}}'}

    with open('prot' + gene + '.out', 'w') as f:
        f.write(requests.post(url, data = data).text)
        print('recorded ' + gene + ' protein sequence')

print('query complete')