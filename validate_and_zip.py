import csv, zipfile, glob, os, datetime, pandas, sys
from tkinter.filedialog import askdirectory
import tkinter

dir_path = os.path.dirname(os.path.realpath(__file__))

#initalize TKinter
root = tkinter.Tk()
root.withdraw()
folder = askdirectory()
root.destroy


def validate_csv_and_pdfs(instance):
    files = glob.glob(instance + '/*.pdf')

    #Check filesystem for files read from filesystem
    for file in files:
        
        if os.path.isfile(file) == False:
            print('missing file!')
            return(False)
            #exit()
            
    indexcsv = ('{}/index.csv'.format(instance))
    csvdata = read_csv(indexcsv)

    #Check filesystem for files read from CSV
    for file in csvdata:
        inferred_path = '{}/{}'.format(instance, file)
        
        if os.path.isfile(inferred_path) == False:
            print('{} is missing!'.format(inferred_path))
            return(False)
            #exit()
            
    #print('{} PDFs: {}'.format(batches, len(files)))
    print('PDFs: {}'.format(len(files)))
    #print('{} CSV: {}'.format(batches, len(csvdata)))
    print('CSV: {}'.format(len(csvdata)))

    #Compare lengths of CSV and counts of PDFs
    if len(files) != len(csvdata):
        print('Mismatched CSV and File count. Likely a surplus PDF or a defecient line in CSV.\n')
        print('Please review {}'.format(instance))
        return(False)
        exit()
    else:
        print('All good.')
        return(True)


def zip_instance(instance):

    curtime = datetime.datetime.now().strftime('%Y%m%d-%S%f')
    curtime2 = curtime[:-4]
    
    
    print('Doing zipping things')
    batchinstance = os.path.basename(os.path.normpath(instance))
    zipname = '{}_{}.zip'.format(batchinstance, curtime2)

    #Path and zip name defines the archive
    #print(folder + '/' + zipname)

    zf = zipfile.ZipFile(folder + '/' + zipname, 'w')
    
    for root, dirs, files in os.walk(instance):
        for filename in files:
            #print(root, filename)
            zf.write(folder + '/' + '/' + batchinstance + '/' +filename, filename)
    zf.close()
    


def read_csv(csvpath):
    """Reads a single CSV and returns the column of 'FILE_NAME'"""
    df = pandas.read_csv(csvpath)
    #df = pandas.read_csv(csvpath, error_bad_lines=False)
    column = df['FILE_NAME']
    return(column)


def list_dirs(folder):
    """Reads a path, returns only the directories at the upper-most level
    within the path"""
    return [
        d for d in (os.path.join(folder, d1) for d1 in os.listdir(folder))
        if os.path.isdir(d)
    ]


batches = list_dirs(folder)
for instance in batches:
    validation = validate_csv_and_pdfs(instance)

    if validation == False:
        print('Halting now. Review problematic batch')
        exit()
    
    else:
        print('Proceed to zipping')
        print('DO ZIPPING STUFF!')
        zip_instance(instance)

print('\nProgram completed successfully!')
input('Press enter to exit')
sys.exit()
