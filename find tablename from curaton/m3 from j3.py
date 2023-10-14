import re
import tkinter
from tkinter import filedialog
import sqlparse

root = tkinter.Tk()
root.withdraw() #use to hide tkinter window

def search_for_file_path ():
    # currdir = os.getcwd()
    currdir =r'E:/Leoaws/LEO%20AWS%20Migration/Curation/curation_procedure_order/'
    # tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    tempdir = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
    if len(tempdir) > 0:
        print ("You chose: %s" % tempdir)
    return tempdir

# Compile regular expressions
TEMP_TABLE_RE = re.compile(r'CREATE\s+OR\s+REPLACE\s+TEMP(?:ORARY)?\s+TABLE\s+(\S+)\s+AS', re.I)
DROP_TABLE_RE = re.compile(r'(L1\.|L2\.|L3\.|QC\.|MDM\.|NPA_REF\.|ETL\.|MDM_L1\.|INFORMATION_SCHEMA\.)\s*(\w+)', re.I)
TABLE_RE = re.compile(r"(L1\.|L2\.|L3\.|QC\.|MDM\.|NPA_REF\.|ETL\.|MDM_L1\.|INFORMATION_SCHEMA\.)\s*(\w+)", re.I)
# TABLE_RE = re.compile(r'^L1\.(?:\w+)(?:\.(?:\w+))*$', re.I)
# TABLE_RE = re.compile(r"^(L1|L2|L3)\.(.+)$", re.I)
# TABLE_RE = re.compile(r"^(L1|L2|L3)\.\s*(\w+)", re.I)
# TABLE_RE=re.compile(r"\b(L1.|L2\.|L3\.|QC\.|MDM\.|NPA_REF\.|ETL\.|MDM_L1\.|INFORMATION_SCHEMA\.)\w+", re.I)
TABLE_RE_WITH_DOT = re.compile(r'"(L1|L2|L3|QC|MDM|NPA_REF|ETL|MDM_L1|INFORMATION_SCHEMA)"\."(\w+)"', re.I)
# Create empty sets to store the matches
matches = set()
matches2 = set()
unwant_matches = {'L1','L2','L3'}
temp_matches = set()
drop_matches = set()

file_path_variable=search_for_file_path()
all_sql_content=''
with open("{}".format(file_path_variable))as f:
    linesby=f.readlines()
    for mp in linesby:
        if 'run_first.sql' in mp:
            # print(mp)
            pass
        else:
            # all_sql_content=''
            with open(file_path_variable[:41]+mp.strip('\n'), "r") as source_file:
                # Format the sql statement                
                sql_content_format=sqlparse.format(source_file, reindent=True, strip_comments=True , keyword_case='upper')                
                all_sql_content+=sql_content_format
                # print(all_sql_content)

lines=all_sql_content.splitlines()
for line in lines:
    # Match TEMP TABLE
    temp_matches.update(TEMP_TABLE_RE.findall(line))            
    # Match DROP TABLE
    drop_matches.update(DROP_TABLE_RE.findall(line))            
    # Match TABLE
    matches.update(TABLE_RE.findall(line))           
    # Match TABLE with dot
    matches2.update(TABLE_RE_WITH_DOT.findall(line))
    
# Convert the matches to sets
matches = set(f"{match[0]}{match[1]}" for match in matches)
matches2 = set(f"{match[0]}.{match[1]}" for match in matches2)
temp_matches = set(f"{match[0]}{match[1]}" for match in temp_matches)
drop_matches = set(f"{match[0]}{match[1]}" for match in drop_matches)


# Merge the matches sets
merged_matches = matches.union(matches2)
# Difference the merged matches with temp matches
merged_matches1 = merged_matches.difference(temp_matches)# TEMPORARY key work capture two table but one table valid another nor valid(ex:-L2.TIMEPERIOD_BOUNDARIES(valid),L2.TIMEPERIOD_BOUNDARIES_SOB it's temp table)
merged_matches2 = merged_matches1.difference(unwant_matches)
# merged_matches = merged_matches.difference(drop_matches)
# tempdrop_matches = temp_matches.union(drop_matches)

if merged_matches2:
    print("Merged matches found:")
    for match in sorted(merged_matches2):
        print(match)
    print('----------------------------------------------------------------------------------------')
else:
    print("No matches found in the text file.")
print('\n')