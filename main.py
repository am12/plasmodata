import requests
import os
import shutil
import csv

#initializes the headers, will contain all data in tsv
allFields = [[
    'Gene ID', 'Product Description', 'Chromosome', 'ORF/Locus', 'Other Accession #', 'Plasmodium berghei Orthologs', 'Plasmodium falciparum Orthologs', 'Plasmodium vivax P01 Orthologs', 'Plasmodium vivax Sal1 Orthologs', 'Molecular Weight', 'Protein Length', '# Transmembrane Domains', 'Has SignalP', 'Mutagenesis Index Score', 'GO Terms', 'Gene Seq. w/ Introns', 'Gene Seq. w/o Introns', 'Protein Seq.'
]]

#input sequence
genes = input('Enter a list of geneIDs separated by spaces ').split()
print('your gene library is ', genes, '\n')

#deletes already made gene folders (for troubleshooting/updates)
for gene in genes:
    if gene in os.listdir():
        shutil.rmtree(gene)

#gene list
f = open('genes.txt', 'w+')
f.write(' '.join(genes))
f.close()

#reads the information in data report
def readData(gene, data, url):

    #thing for skipping
    global skip
    skip = False

    #makes raw_data if the folder doesn't exist
    if 'raw_data' not in os.listdir():
        os.mkdir('raw_data')

    #post request writes to new file
    with open('raw_data/data' + gene + '.out', 'w+') as f:
        writeData = requests.post(url, data=data).text
        f.write(writeData)
        print('\nrecorded ' + gene + ' data sequence')

    #reading from recently made file
    with open('raw_data/data' + gene + '.out', 'r') as dataFile:
        #lambda for a template search function
        get_indexes = lambda searchTerm, fullTxt: [i for (y, i) in zip(fullTxt, range(len(fullTxt))) if searchTerm in y]

        #gets all the text of the file
        global text
        text = dataFile.readlines()
        if text[0] == "Internal Error":
            skip = True

    #just in case the gene is not in PlasmoDB
    if skip:
        print("ERROR")
        allFields.append([gene, 'No data in PlasmoDB'])
        return

    #list containing all the data (no headers)
    fieldFills = []

    #cuts up text by only \n newspaces
    nSplit = ''.join(text).split('\n')

    #cutting by \n newspaces and \t tabs
    t_n_Split = '\t'.join(''.join(text).split('\n')).split('\t')

    #cuts up by only \t tabs
    tSplit = ''.join(text).split('\t')

    #cuts up by ' ' spaces and \n newspaces
    n_space_Split = '\n'.join(' '.join(text).split(' ')).split('\n')

    #Gene ID
    print('Gene ID: ' + gene)
    fieldFills.append(gene)

    #Product Description
    print('Product Description: ' + nSplit[2][21:])
    fieldFills.append(nSplit[2][21:])

    #Chromosome
    indexOfChromosome = get_indexes('Chromosome:', n_space_Split)
    print('Chromosome: ' + n_space_Split[indexOfChromosome[0] + 1])
    fieldFills.append(n_space_Split[indexOfChromosome[0] + 1])

    #ORF/Locus
    indexOfORF = get_indexes(' - ', tSplit)
    print('ORF/Locus: ' + tSplit[indexOfORF[0]])
    fieldFills.append(tSplit[indexOfORF[0]])

    #Other Accession
    accession = []
    tempNumOne = get_indexes('Table: Orthologs and Paralogs within VEuPathDB', t_n_Split)[0] - get_indexes('Name/ID/Alias', t_n_Split)[0] - 2
    tempStartOne = get_indexes('Name/ID/Alias', t_n_Split)[0]
    for i in range(3, tempNumOne, 3):
        accession.append(t_n_Split[i + tempStartOne])
    print('Other Accessions: {}'.format(accession))
    fieldFills.append(', '.join(accession))

    #PBANKA Orthologs
    indexOfPlasmoBerg = get_indexes('Plasmodium berghei ANKA', t_n_Split)
    berghei = []
    addToArr = False
    if len(indexOfPlasmoBerg) > 0:
        try:
            for i in range(0, len(indexOfPlasmoBerg)):
                berghei.append(t_n_Split[indexOfPlasmoBerg[i] - 1])
                addToArr = True
        except:
            print('PBANKA Orthologs: none')
            fieldFills.append('none')
        if addToArr:
            fieldFills.append(', '.join(berghei))
            print('PBANKA Orthologs: {}'.format(berghei))
    else:
        print('PBANKA Orthologs: none')
        fieldFills.append('none')

    #PF3D7 Orthologs
    indexOfPlasmoFalc = get_indexes('Plasmodium falciparum 3D7', t_n_Split)
    falciparum = []
    addToArr = False
    if len(indexOfPlasmoFalc) > 0:
        try:
            for i in range(0, len(indexOfPlasmoFalc)):
                falciparum.append(t_n_Split[indexOfPlasmoFalc[i] - 1])
                addToArr = True
        except:
            print('PF3D7 Orthologs: none')
            fieldFills.append('none')
        if addToArr:
            fieldFills.append(', '.join(falciparum))
            print('PF3D7 Orthologs: {}'.format(falciparum))
    else:
        print('PF3D7 Orthologs: none')
        fieldFills.append('none')

    #PVP01 Orthologs
    indexOfPlasmoP01 = get_indexes('Plasmodium vivax P01', t_n_Split)
    p01 = []
    addToArr = False
    if len(indexOfPlasmoP01) > 0:
        try:
            for i in range(0, len(indexOfPlasmoP01)):
                p01.append(t_n_Split[indexOfPlasmoP01[i] - 1])
                addToArr = True
        except:
            print('PVP01 Orthologs: none')
            fieldFills.append('none')
        if addToArr:
            fieldFills.append(', '.join(p01))
            print('PVP01 Orthologs: {}'.format(p01))
    else:
        print('PVP01 Orthologs: none')
        fieldFills.append('none')

    #PVX Orthologs
    indexOfPlasmoSal1 = get_indexes('Plasmodium vivax Sal-1', t_n_Split)
    sal = []
    addToArr = False
    if len(indexOfPlasmoSal1) > 0:
        try:
            for i in range(0, len(indexOfPlasmoSal1)):
                sal.append(t_n_Split[indexOfPlasmoSal1[i] - 1])
                addToArr = True
        except:
            print('PVX Orthologs: none')
            fieldFills.append('none')
        if addToArr:
            fieldFills.append(', '.join(sal))
            print('PVX Orthologs: {}'.format(sal))
    else:
        print('PVX Orthologs: none')
        fieldFills.append('none')

    #Molecular Weight
    indexOfMolWeight = get_indexes('Molecular Weight', tSplit)[0] + 13
    print('Molecular Weight: ' + tSplit[indexOfMolWeight])
    fieldFills.append(tSplit[indexOfMolWeight])

    #Protein Length
    indexOfProtLen = get_indexes('Molecular Weight', tSplit)[0] + 18
    print('Protein Length: ' + tSplit[indexOfProtLen])
    fieldFills.append(tSplit[indexOfProtLen])

    #TMHMM
    tempNumTwo = get_indexes('Table: GO Terms', nSplit)[0] - get_indexes(
        'Table: Transmembrane Domains', nSplit)[0]
    print('Transmembrane Domains: ' +
          str((tempNumTwo - 2) if tempNumTwo > 2 else '0'))
    fieldFills.append(str((tempNumTwo - 2) if tempNumTwo > 2 else '0'))

    #Has SignalP
    indexOfSignalP = get_indexes('Molecular Weight', tSplit)[0] + 14
    print('Has SignalP: ' + tSplit[indexOfSignalP])
    fieldFills.append(tSplit[indexOfSignalP])

    #Mutagenesis Score
    try:
        indexOfMutScore = get_indexes('mutagenesis index score',(t_n_Split))[0] - 1
        print('Mutagenesis Score: ' + t_n_Split[indexOfMutScore] + (' (Essential)' if float(t_n_Split[indexOfMutScore]) < 0.5 else ' (Dispensable)'))
        fieldFills.append(t_n_Split[indexOfMutScore] + (' (Essential)' if float(t_n_Split[indexOfMutScore]) < 0.5 else ' (Dispensable)'))
    except:
        print('Mutagenesis Score: none')
        fieldFills.append('none')

    #GO Terms
    goTerms = []
    tempNumThree = get_indexes('Table: Gene Location', t_n_Split)[0] - get_indexes('Table: GO Terms', t_n_Split)[0] - 1
    tempStartThree = get_indexes('Table: GO Terms', t_n_Split)[0] + 1
    for i in range(11, tempNumThree, 11):
        goTerms.append(t_n_Split[i + tempStartThree + 3])
    print('GO Terms: {}'.format(goTerms if len(goTerms) > 0 else 'n/a'))
    fieldFills.append(', '.join(goTerms) if len(goTerms) > 0 else 'n/a')

    #adds all the data to new row in the tsv
    allFields.append(fieldFills)

#saves gene/protein sequences to gene folder
def saveFolder(gene, data, url, mod):

    #makes gene directory if it doesn't exist
    if gene not in os.listdir():
        os.mkdir(gene)

    #pulls protein seq from UniProt if no data in PlasmoDB
    if skip:
        with open(gene + '/prot' + gene + '.fasta', 'w') as f:
            url = 'https://www.uniprot.org/uniprot/?query='+gene+'&format=fasta'
            f.write(requests.get(url).text)
        print('recorded ' + gene + ' protein sequence')
        return

    #post request for sequences and saves as fasta
    with open(gene + '/{}'.format(mod) + gene + '.fasta', 'w') as f:
        f.write(requests.post(url, data=data).text)
        print('recorded ' + gene + ' {} sequence {}'.format(
            'protein' if mod == 'prot' else 'genomic', 'without introns' if mod == 'gseq' else 'with introns' if mod == 'gint' else ''))

#post request info for gene report
for gene in genes:

    url = 'https://plasmodb.org/plasmo/service/record-types/gene/searches/single_record_question_GeneRecordClasses_GeneRecordClass/reports/fullRecord'

    data = {
        'data':
        '{"searchConfig":{"parameters":{"primaryKeys":"'+gene+',PlasmoDB"}},"reportConfig":{"attributes":["primary_key","chromosome","product"],"tables":["Alias","OrthologsLite","pfal3D7_phenotype_pB_mutagenesis_MIS_MFS_RSRC","SignalP","TMHMM","GOTerms","GeneLocation","Notes","ProteinProperties"],"includeEmptyTables":true,"attachmentType":"plain"}}'
    }
    
    readData(gene, data, url)
    
    #post info for sequences
    for mod in ('genomic', 'CDS', 'protein'):
        url = 'https://plasmodb.org/plasmo/service/record-types/gene/searches/single_record_question_GeneRecordClasses_GeneRecordClass/reports/srt'

        data = {
            'data':
            '{"searchConfig":{"parameters":{"primaryKeys":"'+gene+',PlasmoDB"}},"reportConfig":{"attachmentType":"plain","endOffset3":0,"type":"'+mod+'","sourceIdFilter":"genesOnly","upstreamAnchor":"Start","upstreamSign":"plus","upstreamOffset":0,"downstreamAnchor":"End","downstreamSign":"plus","downstreamOffset":0,"onlyIdDefLine":"0","noLineBreaks":"0","startAnchor3":"Start","startOffset3":0,"endAnchor3":"End"}}'
        }

        if mod == 'genomic':
            mod = 'gint'
        if mod == 'CDS':
            mod = 'gseq'
        if mod == 'protein':
            mod = 'prot'

        saveFolder(gene, data, url, mod)   

#writes all protein data to data.tsv file
with open('data.csv', 'w', newline='') as report:

    writer = csv.writer(report, delimiter='\t')

    writer.writerows(allFields)

print('\nquery complete')

print('\nRunning excelMaker file')
os.system('python excelMaker.py')

print('\ndone')