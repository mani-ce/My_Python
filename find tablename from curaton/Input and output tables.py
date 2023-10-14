import re
import pandas as pd
import tkinter
from tkinter import filedialog
import sqlparse

def get_file_paths():
  root = tkinter.Tk()
  root.withdraw()

  file_path_variable = filedialog.askopenfilename(parent=root, title='Please select a directory')

  file_paths = []
  with open(file_path_variable, 'r') as f:
    for line in f:
      line = line.strip()
      if 'run_first.sql' not in line:
        file_paths.append(line[11:])
  return file_paths

matches1 = set()
matches2 = set()
CREATE_TEMP = set()
crt=set()
drop_matches=set()
trc=set()
inc=set()
det=set()
upd=set()
lst=get_file_paths()
def parse_sql_queries(sql_text):
  parsed_queries = []
  statements = sqlparse.split(sql_text)
  for statement in statements:
    parsed_queries.append(sqlparse.format(statement, reindent=True,strip_comments=True,keyword_case='upper'))
  return parsed_queries

for ii in lst:
    # file_path=r'E:/Leoawsran/LEO%20RAP3iD%20Implementation%20%28Infra-CDW-MDM%29/leo_prefect/'+ii
    file_path=r'E:/Leoaws/LEO%20AWS%20Migration/Curation/procedures/'+ii
    # print(file_path)

# file_path =r"E:/Leoawsran/LEO%20RAP3iD%20Implementation%20%28Infra-CDW-MDM%29/leo_prefect/Development/aggregator_procedures/Copay_SP_HUB/L3_SP_HUB_Base.sql" # Replace with the actual file path
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    # frm=set()
    for lineby in lines:
        # print(lineby)
        # print('mani')

        line = lineby.strip().upper()#here strip removed '\n'
        # print(line)
        if not (line.startswith("--") or line.startswith("---") or line.startswith("//")):#j4.1 updated
            # print(line)
            if "TEMP" in line and "TEMP_" not in line:
                # print(line)
                CREATE_TEMP.update(re.findall(r'CREATE\s+OR\s+REPLACE\s+TEMP(?:ORARY)?\s+TABLE\s+(\S+)\s', line))
            elif "CREATE " in line:
                crt.update(re.findall(r'CREATE(?:\s+OR\s+REPLACE)?\s+TABLE(?:\s+IF\s+NOT\s+EXISTS)?\s+(\w+\.\w+)\s+', line))
            elif "DROP " in line:
                # print(line)
                drop_matches.update(re.findall(r'DROP\s+TABLE\s+(\S+);', line))
            elif "TRUNCATE " in line:
                # print(line)
                trc.update(re.findall(r'TRUNCATE\s+(?:TABLE\s+)?(\S+);', line))
            elif "INSERT " in line:
                # print(line)
                inc.update(re.findall(r'INSERT\s+INTO\s+(\S+)', line))
            elif "DELETE " in line:
                # print(line)
                det.update(re.findall(r'DELETE\s+FROM\s+(\S+)', line))
            elif "UPDATE " in line:
                # print(line)
                upd.update(re.findall(r'UPDATE\s+(\S+)\s', line))
            # elif "FROM " in line:
            #     # print(line)
            #     frm.update(re.findall(r'(L1.|L2\.|L3\.|QC\.|MDM\.|NPA_REF\.|ETL\.|MDM_L1\.|INFORMATION_SCHEMA\.)\s*(\w+)', line))
            else:
                # print(line)
                matches1.update(re.findall(r'(L1\.|L2\.|L3\.|QC\.|MDM\.|NPA_REF\.|ETL\.|MDM_L1\.|INFORMATION_SCHEMA\.)\s*(\w+)', line))
                matches2.update(re.findall(r'"(L1|L2|L3|QC|MDM|NPA_REF|ETL|MDM_L1|INFORMATION_SCHEMA)"\."(\w+)"', line))

    # print(matches1)
    # print(matches2)
    # Two values change into one set of values in matches
matches1 = set(f"{match[0]}{match[1]}" for match in matches1)
    # Add a dot after L1, L2, L3 in matches2
matches2 = set(f"{match[0]}.{match[1]}" for match in matches2)
    # print(matches1)
    # print(matches2)
    # trunc_1= set(f"{match[0]}.{match[1]}" for trc in trunc_1)
    # insert_1 = set(f"{match[0]}.{match[1]}" for inc in insert_1)
    
input_matches = matches1.union(matches2)

   
trunc_1 = {item.replace('"', '') for item in trc}
insert_1 = {item.replace('"', '') for item in inc}
    

output_matches=insert_1.union(trunc_1)
output_matches=output_matches.union(crt)

    # CREATE_TEMP=CREATE_TEMP.union(trc)
    # CREATE_TEMP=CREATE_TEMP.union(inc)
    # CREATE_TEMP=CREATE_TEMP.union(det)
    # CREATE_TEMP=CREATE_TEMP.union(upd)

    # merged_matches = merged_matches.difference(temp_matches)# TEMPORARY key work capture two table but one table valid another nor valid(ex:-L2.TIMEPERIOD_BOUNDARIES(valid),L2.TIMEPERIOD_BOUNDARIES_SOB it's temp table)
output_matches = output_matches.difference(CREATE_TEMP)
update_matches= upd.difference(output_matches)
delete_matches= det.difference(output_matches)

input_matches=input_matches.union(update_matches)
input_matches=input_matches.union(delete_matches)
input_matches=input_matches.difference(output_matches)
input_matches=input_matches.difference(CREATE_TEMP)#here i remove temp table from input tables
merged_matches1=sorted(input_matches)
merged_matches2=sorted(output_matches)


    # print(r'E:/Leoawsran/LEO%20RAP3iD%20Implementation%20%28Infra-CDW-MDM%29/leo_prefect/'+ii,': ')

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