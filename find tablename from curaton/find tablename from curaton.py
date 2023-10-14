#read the text file
lst=[]
lst_truncin=[]
with open(r"E:\Leotesting\LEO%20RAP3iD%20Implementation%20%28Infra-CDW-MDM%29\leo_prefect\Development\sob\SOB_WEEKLY_MONTHLY\Consolidate_Week_And_Month_NBRX.sql","r") as file1:
    for i in file1: 
        i=i.upper()

        # print(i)
        # x = i.count("L1.")
        # print(x>2)
        if r"--" in i or r"//" in i:
                    continue
        elif 'TRUNCATE' in i or 'INSERT' in i:
            
            # print('true of nested if')
            if 'L1.' in i:                
                a=i.find('L1.')
                # print(a,aa)
                # print(i[a:i.find('\n',a)+1])
                # print(i[a:i.find(';',a)+1])                
                lst_truncin.append(i[a:i.find(' ',a)+1])
                lst_truncin.append(i[a:i.find('\n',a)])                
            elif r'"L1".' in i:#it work
                aa=i.find(r'"L1".')
                lst_truncin.append(i[aa:i.find(' ',aa)+1])
                lst_truncin.append(i[aa:i.find('\n',aa)])
            elif "L2."in i or r'"L2".' in i:
                a=i.find('L2.')
                aa=i.find(r'"L2".')
                lst_truncin.append(i[a:i.find('\n',a)])
                lst_truncin.append(i[a:i.find(' ',a)+1])
                lst_truncin.append(i[aa:i.find('\n',aa)])
                lst_truncin.append(i[aa:i.find(' ',aa)+1])
            elif "L3." in i or r'"L3".' in i:
                a=i.find('L3.')
                aa=i.find(r'"L3".')
                lst_truncin.append(i[a:i.find('\n',a)])
                lst_truncin.append(i[a:i.find(' ',a)+1])
                lst_truncin.append(i[aa:i.find('\n',aa)])
                lst_truncin.append(i[aa:i.find(' ',aa)+1])
        elif 'L1.' in i:
            a=i.find('L1.')           
            lst.append(i[a:i.find(' ',a)+1])
            lst.append(i[a:i.find('\n',a)+1])
        elif r'"L1".' in i:
            aa=i.find(r'"L1".')
            lst.append(i[aa:i.find(' ',aa)+1])
            lst.append(i[aa:i.find('\n',aa)+1])
        # elif r'"L1".' in i:
        #     a=i.find(r'"L1".')
        #     lst.append(i[a:i.find('\n',a)+1])
        elif "L2."in i or r'"L2".' in i:
            a=i.find('L2.')
            aa=i.find(r'"L2".')
            lst.append(i[a:i.find(' ',a)+1])
            lst.append(i[a:i.find('\n',a)+1])
            lst.append(i[aa:i.find(' ',aa)+1])
            lst.append(i[aa:i.find('\n',aa)+1])
        elif "L3." in i or r'"L3".' in i:
            a=i.find('L3.')
            aa=i.find(r'"L3".')
            lst.append(i[a:i.find(' ',a)+1])
            lst.append(i[a:i.find('\n',a)+1])
            lst.append(i[aa:i.find(' ',aa)+1])
            lst.append(i[aa:i.find('\n',aa)+1])
        elif "QC." in i:
            a=i.find('QC.')
            lst.append(i[a:i.find(' ',a)+1])
            lst.append(i[a:i.find('\n',a)+1])
        # elif (("TRUNCATE" in i and (('L1.' in i or r'"L1".' in i)or("L2."in i or r'"L2".' in i)or("L3." in i or r'"L3".' in i))) or ("INSERT INTO" in i and (('L1.' in i or r'"L1".' in i)or("L2."in i or r'"L2".' in i)or("L3." in i or r'"L3".' in i)))):
        # print(len('( SELECT SUM(TRX) FROM L3.'))
print(lst)
print(lst_truncin)
# print("Output of Read function is ")
# lst = list(dict.fromkeys(lst))
# lst.sort()
# for j in lst:
#     print(j)
# print("Truncate or insert tables list: ")
# lst_truncin = list(dict.fromkeys(lst_truncin))
# lst_truncin.sort()
# for j in lst_truncin:
#     jj=j.strip(';')
#     print(jj)
