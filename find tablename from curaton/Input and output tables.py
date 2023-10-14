import re
import tkinter
from tkinter import filedialog
import sqlparse

# Create empty sets to store the matches
matches = set()
matches_dot = set()
create_temp = set()
crt=set()
drp=set()
trc=set()
inc=set()
det=set()
upd=set()
unwant_matches = {'L1','L2','L3'}

# Compile regular expressions
create_temp_re=re.compile(r'CREATE\s+OR\s+REPLACE\s+TEMP(?:ORARY)?\s+TABLE\s+(\S+)\s',re.I)
crt_re=re.compile(r'CREATE(?:\s+OR\s+REPLACE)?\s+TABLE(?:\s+IF\s+NOT\s+EXISTS)?\s+(\w+\.\w+)\s+',re.I)
drp_re=re.compile(r'DROP\s+TABLE\s+(\S+);',re.I)
trc_re=re.compile(r'TRUNCATE\s+(?:TABLE\s+)?(\S+);',re.I)
inc_re=re.compile(r'INSERT\s+INTO\s+(\S+)',re.I)
det_re=re.compile(r'DELETE\s+FROM\s+(\S+)',re.I)
upd_re=re.compile(r'UPDATE\s+(\S+)\s',re.I)
matches_re= re.compile(r'(L[123]\.|QC\.|MDM\.|NPA_REF\.|ETL\.|MDM_L1\.|INFORMATION_SCHEMA\.)\s*(\w+)', re.I)
matches_dot_re=re.compile(r'"(L[123]|QC|MDM|NPA_REF|ETL|MDM_L1|INFORMATION_SCHEMA)"\."(\w+)"', re.I)

def search_for_file_path ():
    root = tkinter.Tk()
    root.withdraw() #use to hide tkinter window
    # currdir = os.getcwd()
    currdir =r'E:/Leoaws/LEO%20AWS%20Migration/Curation/curation_procedure_order/'
    # tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    tempdir = filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select a directory')
    if tempdir:
        print ("You chose: %s" % tempdir)
    return tempdir

file_path_variable=search_for_file_path()
all_sql_content=''
with open("{}".format(file_path_variable))as f:
    for mp in f:
        # print(mp)
        if 'run_first.sql' not in mp:
            # print(mp)
            with open(file_path_variable[:41]+mp.rstrip(), "r") as source_file:
                # Format the sql statement                
                sql_content_format=sqlparse.format(source_file, reindent=True, strip_comments=True , keyword_case='upper')                
                all_sql_content+=sql_content_format
                # print(all_sql_content)

# with open("myfile.txt", "w") as file1:
#     file1.writelines(all_sql_content)

lines=all_sql_content.splitlines()   
for line in lines:
    # print(lineby)
    # line = lineby.strip().upper()#here strip removed '\n'
    # print(line)
    if "TEMP" in line and "TEMP_" not in line:
        create_temp.update(create_temp_re.findall(line))
    elif "CREATE " in line:
        # print(line)
        crt.update(crt_re.findall(line))
    elif "DROP " in line:
        drp.update(drp_re.findall(line))
    elif "TRUNCATE " in line:
        trc.update(trc_re.findall(line))
    elif "INSERT " in line:
        inc.update(inc_re.findall(line))
    elif "DELETE " in line:
        det.update(det_re.findall(line))
    elif "UPDATE " in line:
        upd.update(upd_re.findall(line))
    # elif "FROM " in line:
    #     # print(line)
    #     frm.update(re.findall(r'(L1.|L2\.|L3\.|QC\.|MDM\.|NPA_REF\.|ETL\.|MDM_L1\.|INFORMATION_SCHEMA\.)\s*(\w+)', line))
    else:
        # print(line)
        matches.update(matches_re.findall(line))
        matches_dot.update(matches_dot_re.findall(line))
        # matches.update(re.findall(r'(L1\.|L2\.|L3\.|QC\.|MDM\.|NPA_REF\.|ETL\.|MDM_L1\.|INFORMATION_SCHEMA\.)\s*(\w+)', line))
        # matches_dot.update(re.findall(r'"(L1|L2|L3|QC|MDM|NPA_REF|ETL|MDM_L1|INFORMATION_SCHEMA)"\."(\w+)"', line))

    # print(matches1)
    # print(matches2)
    # Two values change into one set of values in matches
matches = set(f"{match[0]}{match[1]}" for match in matches)
    # Add a dot after L1, L2, L3 in matches2
matches_dot = set(f"{match[0]}.{match[1]}" for match in matches_dot)
    # print(matches1)
    # print(matches2)
    
input_matches = matches.union(matches_dot)
   
trunc_1 = {item.replace('"', '') for item in trc}
insert_1 = {item.replace('"', '') for item in inc}    

output_matches=insert_1.union(trunc_1)
output_matches=output_matches.union(crt)
# merged_matches = merged_matches.difference(temp_matches)# TEMPORARY key work capture two table but one table valid another nor valid(ex:-L2.TIMEPERIOD_BOUNDARIES(valid),L2.TIMEPERIOD_BOUNDARIES_SOB it's temp table)
output_matches = output_matches.difference(create_temp)
update_matches= upd.difference(output_matches)
delete_matches= det.difference(output_matches)
input_matches=input_matches.union(update_matches)
input_matches=input_matches.union(delete_matches)
input_matches=input_matches.difference(output_matches)
input_matches=input_matches.difference(create_temp)#here i remove temp table from input tables
merged_matches1=sorted(input_matches)
merged_matches2=sorted(output_matches)


if merged_matches1:
    print("Input tables found:")
    for match in merged_matches1:
        print(match)
else:
    print("No matches found in the text file.")
print('\n')
if merged_matches2:
    print("Output tables found:")
    for match in merged_matches2:
        print(match)
else:
    print("No matches found in the text file.")
print('\n')