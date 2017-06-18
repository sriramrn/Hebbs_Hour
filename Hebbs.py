# -*- coding: utf8 -*-
"""
Created on Fri Sep  2 11:14:09 2016

@author: Sriram
"""

import xlrd
import numpy as np
import copy



def uniquify(seq, idfun=None): 
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

  
group_size=6
column_index_names=1
column_index_lab=3

workbook = xlrd.open_workbook("Hebb's Hour Registration (Responses).xlsx")
worksheet = workbook.sheet_by_index(0)

num_cols = worksheet.ncols
num_rows = worksheet.nrows

name=[]
lab=[]
i=1
while i<num_rows:
    n=worksheet.cell(i,column_index_names).value
    l=worksheet.cell(i,column_index_lab).value    
    name.append(n)
    lab.append(l)
    i+=1
    
lab_list=uniquify(lab)

names_sorted=[x for (y,x) in sorted(zip(lab,name))]
labs_sorted=sorted(lab)


PI_indices=[]
lab_groups=[]
i=0
while i<len(lab_list):
    k=[]
    k.append([x for x in names_sorted if lab_list.index(labs_sorted[names_sorted.index(x)]) == i])
    lab_groups.append(k[0])
    
    sub=lab_list[i]
    ind=[s for s in k[0] if sub.lower() in s.lower()]
    if ind!=[]:
        PI_indices.append([i,k[0].index(ind[0])])   
    else:
        PI_indices.append([])
    if len(ind)>1:
        print("{} lab has more than one PI".format(lab_list[i]))
    i+=1
    

i=0
lab_groups_no_pi=copy.deepcopy(lab_groups)
while i<len(lab_groups):
    if PI_indices[i]!=[]:
        lab_groups_no_pi[i].remove(lab_groups_no_pi[i][PI_indices[i][1]])
    i+=1
    
ngroups=round(len(names_sorted)/group_size)

lab_split=[]
i=0
while i<len(lab_groups_no_pi):
    x=0
    if PI_indices[i]!=[]:
        x=1

    allowed_groups=ngroups-x

    individuals=len(lab_groups_no_pi[i])    
    
    if individuals>allowed_groups:
        g=allowed_groups
    else:
        g=individuals
    
    if individuals>allowed_groups:
        num_per_group=np.ones(allowed_groups)+(np.floor(individuals/allowed_groups)-1)
        ii=0
        while ii<individuals%allowed_groups:
            num_per_group[ii]+=1
            ii+=1
    else:
        num_per_group=np.ones(g)
        
    lab_split.append([lab_list[i],g,list(num_per_group)])
    
    i+=1
    
    
i=0
groups=[]
while i<len(lab_split):
    g=[]
    ii=0
    count=0
    while ii<len(lab_split[i][2]):
        s=int(count)
        e=int(count+lab_split[i][2][ii])
        g.append(lab_groups_no_pi[i][s:e])
        count+=lab_split[i][2][ii]
        ii+=1
    groups.append(g)
    i+=1

print(lab_split)
