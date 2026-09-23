# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 14:00:43 2026

@author: pemb6626
"""

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #

                    #       S Y N O P S I S        #
                    
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #

# This code creates .inp files for ABAQUS

# It reads a list of input Excel files listed as rows in the 'bank' file

# The user can select either Steel or Aluminium as the material

# The user can choose either S4 or S4R elements

# A linear (_L) and a nonlinear (_NL) input file is created for ABAQUS

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# 1. Linear .inp file

# The code reads an input file, which is an Excel file with two worksheets:
    
    # PC: Co-ordinates of the plate i.e. the length (XMAX - XMIN) and the width (YMAX - YMIN), and the plate thickness
    
    # HC: Co-ordinates of the holes i.e. the length (x2 - x1) and the width (y2 - y1)
    
# The user specifies the minimum and maximum permissible element size
    
# Two extra worksheets are saved to the Excel file:
    
    # NODES: with the node number, x, y and z co-ordinates (4 columns)
    
    # ELEMENTS: with the element number, n1, n2, n3 and n4 (5 columns) for an S4 or S4R element. Quadratic elements are not possible with this code
    
# The linear .inp file is saved and ready to be submitted in ABAQUS command.
    
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# 2. Nonlinear .inp file
    
# This requires all four Excel worksheets to exist in the Excel file

# Different nonlinear controls and parameters can be chosen:
    
    # Newton Raphson Method with no damping (NO)
    
    # Newton Raphson Method with damping (ND)
    
    # Newton Raphson Method with time incrementation controls (NT)
    
    # Riks Arc Length Method with load control (L) or displacement control (D)
    
        # Note that the Newton Raphson Method parameters considered for each of these nonlinear controls is found in:
            #Z. Yao., K. J. Rasmussen., 2014, Design of Perforated Thin-Walled Steel Columns (No. R949), SeS faculties schools: Faculty of Engineering: School of Civil Engineering, https://hdl.handle.net/2123/24066
            
# The user may choose the number eigenmode considered as the geometric imperfection. If unspecified, the default of 1 is chosen. This can be determined by the user after running the linear input file in ABAQUS.

# The nonlinear .inp file is saved and ready to be submitted in ABAQUS command.

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #

            #       I M P O R T    L I B R A R I E S        #
                    
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #

import itertools
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #

            #       H O M E - M A D E    F U N C T I O N S        #
                    
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #

# THIS FUNCTION TAKES A LIST OF ITEMS AND TURNS IT INTO A LIST OF ONE ITEM, A STRING OF ALL THE ITEMS.
def HAPPY_STRING(happy_list):
    combo = ''.join(map(str,happy_list))
    happy_list = [combo]

# THIS FUNCTION TAKES A LIST OF LISTS AND PUTS IT INTO A LIST OF SINGLE ITEMS.    
def SMUSH(s):
    return [item for sublist in s for item in sublist]

# Nodes must lie outside of a hole region
# The hole region is defined if the central co-ordinate in the list is at the centre of a hole
# This is identified with the hole_region_identifier variable (True for no hole, False for hole)
def Nodes_In_Region(idr):
    
    hole_region_identifier = True
    
    XCORDS = []
    YCORDS = []
    
    for x in X_NODES:
        if D_R_DF.iloc[idr,0]<=x<=D_R_DF.iloc[idr,1]:
            XCORDS.append(x)
            
        XCORDS = list(dict.fromkeys(XCORDS))
        LENXM = int(len(XCORDS)/2)
        
    for y in Y_NODES:
        if D_R_DF.iloc[idr,2]<=y<=D_R_DF.iloc[idr,3]:
            YCORDS.append(y)
        
        YCORDS = list(dict.fromkeys(YCORDS))
        LENYM = int(len(YCORDS)/2)
        
    for ih in list(range(N_HOLES)):
        
        if HOLECOORDS.iloc[ih,0]<= XCORDS[LENXM] <= HOLECOORDS.iloc[ih,1] and HOLECOORDS.iloc[ih,2]<= YCORDS[LENYM] <= HOLECOORDS.iloc[ih,3]:
            hole_region_identifier = False
            
    return hole_region_identifier, XCORDS, YCORDS

# Fast vectorised search for adjacent nodes to define elements
def Define_Element(nodes_lookup, data_frame, x, y, new_id):
    
    tmp = data_frame.merge(nodes_lookup, how = 'left', left_on=[x, y], right_on=['x', 'y']).rename(columns={'nid': new_id}).drop(columns=['x', 'y'])
    
    return tmp

# Functions used for writing the .inp files
def EXTRACTOR(NAME):
    data_store = ""
    with open(NAME) as fp:
        data = ""
        data = fp.read()
        data_store+=data
    return(data_store)

def LIST_WRITER(NAME):
    with open("C:/Users/pemb6626/Documents/YEAR2/WP1_PLATES/COMPUTATIONAL/RIKS_PACKAGE/TEMPORARY_FILE.txt","w+") as f:
        count = 1
        print(len(NAME))
        for i in NAME:
            if NAME.index(i)==0 and count==1:
                f.write(str(i))
            elif NAME.index(i)!=0 and (count-1)%16!=0 :
                f.write(","+str(i))
            elif NAME.index(i)!=0 and (count-1)%16 ==0:
                f.write(str(i))
            if count%16==0 and i!=NAME[-1]:
                f.write("\n")
            count+=1
            #print(i)
    return("C:/Users/pemb6626/Documents/YEAR2/WP1_PLATES/COMPUTATIONAL/RIKS_PACKAGE/TEMPORARY_FILE.txt")
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #

                    #       S E T - U P        #
                    
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #
# Set to True if want to create the following .inp files (both can be true)
Linear_Input_File = True
Nonlinear_Input_File = True
# Set to false and default of the first eigenmode is selected. Otherwise, user can specify the first positive eigenmode if Eigenmode_Choice is True.
Eigenmode_Choice = False

MATERIAL = "STEEL_SD"
# STEEL_RO  >> RAMBERG OSGOOD MODEL WITH ABAQUS FROM https://classes.engineering.wustl.edu/2009/spring/mase5513/abaqus/docs/v6.6/books/stm/default.htm?startat=ch04s03ath111.html
# STEEL_SD  >> STEEL DESIGN MANUAL EQUATIONS FROM P.G. 155 (STEEL DESIGN 4TH EDITION - SEE RAMBERG OSGOOD FOLDER ON NEXUS, SEE 1. New material Model - Ellie Excel)
# ALUMINIUM >> MEASURED FROM TENSILE TEST DATA (see 01_11_MATERIAL_DATA in C:\Users\pemb6626\OneDrive - Nexus365\Documents\YEAR2\WP1_PLATES\EXPERIMENTS_PROCESSING\EXCEL\MATERIAL)

#(SEE Yao, Z., & Rasmussen, K. (2014). Design of Perforated Thin-Walled Steel Columns. Sydney: The University of Sydney School of Civil Engineering.  p. 21)
if Nonlinear_Input_File:
    inc = int(input("N U M B E R   O F   I N C R E M E N T S = "))
    CONTROL = str(input("""S E L E C T   N O N - L I N E A R   S O L U T I O N   C O N T R O L
RIKS METHODS (RECOMMENDED WHEN EXPECT SNAP-THROUGH)
L >> RIKS ARC LENGTH LOAD CONTROL
D >> RIKS ARC LENGTH DISP CONTROL

NEWTON RAPHSON METHOD (RECOMMENDED BY YAO & RASMUSSEN, 2014)
NO >> NEWTON RAPHSON WITH NO DAMPING - START
ND >> NEWTON RAPHSON WITH DAMPING - ONLY SELECT IF NO DID NOT CONVERGE
NT >> NEWTON RAPHSON WITH TIME INCREMENTATION CONTROL

>> """))

    assert CONTROL != ("L", "D", "NR", "NO", "ND", "NT"), "I N V A L I D   S O L U T I O N   C O N T R O L   C H O S E N"

    if CONTROL == "L" or CONTROL == "D":
        print("RIKS METHOD SELECTED.")
    
        Default = str(input(""""D E F A U L T   V A L U E S   F O R   R I K S ? (Y/N)
    Initial Step Size = 1
    Arc Length = 5
    Min Step Size = 0.0001
    Max Step Size = 5
    Load Proportionality Factor = 2
    Max Displacement = 5"""))
        if Default == "N":
            start_ss = input("I N I T I A L   S T E P   S I Z E = ")
            arc = input("A R C   L E N G T H  = ")
            min_ss = input("M I N   S T E P   S I Z E = ")
            max_ss = input("M A X   S T E P   S I Z E = ")
            lpf = input("L O A D   P R O P O R T I O N A L I T Y   F A C T O R = ")
            disp_max = input("M A X   D I S P L A C E M E N T = ")
        else:
            start_ss = 1                    # DEFAULT >> 1
            arc = 5                         # DEFAULT >> 5
            min_ss = 0.0001                 # DEFAULT >> 0.0001
            max_ss = 5                      # DEFAULT >> 5
            lpf = 2.0                       # DEFAULT >> 2
            disp_max = 5                    # DEFAULT >> 5
            
    elif CONTROL == "NO" or CONTROL == "ND" or CONTROL == "NT":
        print("""NEWTON RAPHSON METHOD WITH DAMPING SELECTED.
    ITERATIVELY INCREASE THE ACCURACY_TOLERANCE BY THE DEFAULT VALUE""")
    
        Default = str(input(""""D E F A U L T   V A L U E S   F O R   N R   W I T H   D A M P I N G ? (Y/N)
    Accuracy Tolerance = 0.005      
    Initial Step Size = 0.001             
    Time Increment = 1                     
    Min Step Size = 0.000001            
    Max Step Size = 0.015               
    Max Displacement = 1"""))
        if Default == "N":
            accuracy_tolerance = input("A C C U R A C Y   T O L E R A N C E = ")
            start_ss_nr = input("I N I T I A L   S T E P   S I Z E = ")
            time_nr = input("T I M E   I N C R E M E N T = ")
            min_ss_nr = input("M I N   S T E P   S I Z E = ")
            max_ss_nr = input("M A X   S T E P   S I Z E = ")
            nr_disp = input("M A X   D I S P L A C E M E N T = ")
        else:
            accuracy_tolerance = 0.005      # DEFAULT >> 0.005, INCREASE BY 0.005 FOR EVERY UNCONVERGED SIMULATION
            start_ss_nr = 0.001             # DEFAULT >> 0.001
            time_nr = 1                     # DEFAULT >> 1
            min_ss_nr = 0.000001            # DEFAULT >> 0.000001
            max_ss_nr = 0.015               # DEFAULT >> 0.015
            nr_disp = 1                     # DEFAULT >> 1

element_type = "S4"
# S4  >> 4-NODE GENERAL PURPOSE FULLY INTEGRATED FINITE MEMBRANE STRAIN QUAD SHELL ELEMENT
# S4R >> ABAOVE, WITH REDUCED INTEGRATION

# MINIMUM ELEMENT SIZE PERMITTED
min_ele_size = 0.5
# MAXIMUM ELEMENT SIZE PERMITTED
max_ele_size = 1
# AIM TO SPECIFY NO MORE THAN MAX_ELE_SIZE = 2 * MIN_ELE_SIZE TO TARGET ELEMENTS WITH A SMALL ASPECT RATIO, BETTER FOR MESHING, SEE:
    # C. Moen., 2008. Direct Strength Design of Cold-Formed Steel Members with Perforations. Dissertation (Ph. D), Vols. Johns Hopkins University, Baltimore, Maryland.

DIRI_EXT = ""
# FOLDER WHERE THE BANK FILE IS STORED
DIRECTORYJ = ""
# FOLDER WHERE THE ABAQUS INPUT FILES WILL BE SAVED
DIRECTORYO = ""
# FOLDER PROVIDING TEMPORARY STORAGE (LIKE A RECYCLE BIN)
DIRECTORYX = ""
# BANK FILE NAME
EXCEL_NAME = "29_07_Staggered_Perforations_Bank_Copy.xlsx"
SHEET_NAME = "Sheet1"

mypath = r"C:\Users"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        
SKIPROWS = 0 #list(range(1,17))
# IF NOT 0, SKIPROWS MUST START WITH 1 SO THAT HEADERS ARE INCLUDED, AND ADD THE skiprows = SKIPROWS in below line

DATA = pd.read_excel(DIRECTORYJ + DIRI_EXT + EXCEL_NAME, index_col = "NAME", sheet_name = SHEET_NAME, skiprows=SKIPROWS)

# LIST OF EXCEL FILES TO CREATE INPUT FILES FOR ABAQUS FROM
INP_FIL_NAME_LIST = DATA.index.tolist()
print(INP_FIL_NAME_LIST)

# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #

            #       C R E A T I N G    T H E    M E S H        #
                    
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #

for FIL_NAME in INP_FIL_NAME_LIST:
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Read the PC and HC worksheets
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    
    TITLE = FIL_NAME
    
    INP_FIL_NAME = DIRECTORYJ + DIRI_EXT + FIL_NAME
    OUT_FIL_NAME_L = DIRECTORYO + DIRI_EXT+ FIL_NAME +"_L.inp"
    OUT_FIL_NAME_NL = DIRECTORYO + DIRI_EXT+ FIL_NAME +"_NL" + str(CONTROL) + ".inp"
    
    n_sheets = len((pd.ExcelFile(INP_FIL_NAME +".xlsx")).sheet_names)
    
    PLATECOORDS = pd.read_excel(INP_FIL_NAME +".xlsx",sheet_name='PC')
    
    XMIN = PLATECOORDS.iloc[0,0]
    XMAX = PLATECOORDS.iloc[0,1]
    YMIN = (PLATECOORDS.iloc[0,2])
    YMAX = (PLATECOORDS.iloc[0,3])
    thickness = PLATECOORDS.iloc[0,4]
    
    MIDX = (XMAX-XMIN)/2
    MIDY = (YMAX-YMIN)/2
    
    HOLECOORDS = pd.read_excel(INP_FIL_NAME +".xlsx",sheet_name='HC', index_col="number")
    
    # The total number of holes in the plate
    N_HOLES = len(HOLECOORDS.iloc[:,0])
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Make a list of the x and y co-ordinates marking important locations, i.e.
        # The x and y co-ordinate of the holes
        # The x and y co-ordinate mid-way along each edge (MIDX, MIDY)
        # The maximum x and y co-ordinae (XMAX, YMAX)
    # Co-ordinates are rounded to 5 decimal places and any repeats are removed.
    # The list is ordered from smallest to greatest.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    
    # x co-ordinates
    X_HC_DF = HOLECOORDS.iloc[:,0:2]
    X_HC_LIST = list(dict.fromkeys(SMUSH(X_HC_DF.values.tolist())))
    
    X_HC_LIST.append(MIDX)
    X_HC_LIST.append(XMAX)
    X_HC_LIST.sort()
    X_HC_LIST = [round(elem,5) for elem in X_HC_LIST]
    X_HC_LIST = list(dict.fromkeys(X_HC_LIST))
    
    # y co-ordinates
    Y_HC_DF = HOLECOORDS.iloc[:,2:4]
    Y_HC_LIST = list(dict.fromkeys(SMUSH(Y_HC_DF.values.tolist())))
    
    Y_HC_LIST.append(MIDY)
    Y_HC_LIST.append(YMAX)
    Y_HC_LIST.sort()
    Y_HC_LIST = [round(elem,5) for elem in Y_HC_LIST]
    Y_HC_LIST = list(dict.fromkeys(Y_HC_LIST))

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # The nodes between the important locations found previously are now determined.
    # The region between two important locations is of length l
    # l is split into an integer number n such that d = l/n
    # Where d must satisfy min_ele_size <= d <= max_ele_size
    # The nodes are appended to the appropriate list
    # If min_ele_size is too large, the while loop exits and the user must reduce min_ele_size
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    # x co-ordinates
    X_NODES = []
    for i in list(range(len(X_HC_LIST))):
        if i != 0:
            xi = X_HC_LIST[i]
            xo = X_HC_LIST[i-1]
        else:
            xi = X_HC_LIST[i]
            xo = XMIN
            
        l = xi-xo
        n = 1
        d = l/n
        s = True
        
        while s:
            if min_ele_size<=d<=max_ele_size:
                s = False
            else:
                n+=1
                d = l/n
                assert n < 1000, "Minimum element size too large. Try reducing min_ele_size"
        x = xo
        X_NODES.append(x)
        while x<xi:
            x+=d
            X_NODES.append(x)
    X_NODES.append(XMAX)
            
    # y co-ordinates
    Y_NODES = []    
    for i in list(range(len(Y_HC_LIST))):
        
        if i != 0:
            yi = Y_HC_LIST[i]
            yo = Y_HC_LIST[i-1]
        else:
            yi = Y_HC_LIST[i]
            yo = YMIN
            
        l = yi-yo
        n = 1
        d = l/n
        s = True
        
        while s:
            if min_ele_size<=d<=max_ele_size:
                s = False
            else:
                n+=1
                d = l/n
                assert n < 1000, "Minimum element size too large. Try reducing min_ele_size"
        y = yo
        Y_NODES.append(y)
        while y<yi:
            y+=d
            Y_NODES.append(y)
    Y_NODES.append(YMAX)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # The previous list comprehension stops appending when the element has exceeded the boundary limit.
    # e.g. for a region between 20 and d=2.25, we have in the list:
        # 20, 22.25, 24.5, 26.75
    # The next region could be between 25 and 30, therefore the final list is:
        # 20, 22.25, 24.5, 26.75, 25, 27.25, ...
    # But 25 < 26.75 and so this would make very erroneous elements
    # Therefore if the element at 'val - 1' > element at 'val', it is deleted from the list.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    
    lengthx = len(X_NODES)
    val=1
    while val<lengthx-1:
        if X_NODES[val+1]<X_NODES[val] or X_NODES[val-1]>X_NODES[val]:
            X_NODES.pop(val)
            lengthx= len(X_NODES)
        val+=1
    
    lengthy = len(Y_NODES)
    val=1
    while val<lengthy-1:
        if Y_NODES[val+1]<Y_NODES[val] or Y_NODES[val-1]>Y_NODES[val]:
            print(Y_NODES[val])
            Y_NODES.pop(val)
            
            lengthy= len(Y_NODES)
        val+=1
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # We also want to mitigate really small elements like the following:
        # 20, 24.4449, 25.5, ...
    # Therefore such elements are deleted from the list.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    
    lengthx = len(X_NODES)
    val=1
    while val<lengthx-1:
        if float(round(X_NODES[val+1],1))==float(round(X_NODES[val],1)) or float(round(X_NODES[val+1],2))==float(round(X_NODES[val],2)):
            X_NODES.pop(val)
            lengthx= len(X_NODES)
        val+=1
    
    lengthy = len(Y_NODES)
    val=1
    while val<lengthy-1:
        if float(round(Y_NODES[val+1],1))==float(round(Y_NODES[val],1)) or float(round(Y_NODES[val+1],2))==float(round(Y_NODES[val],2)):
            print(Y_NODES[val])
            Y_NODES.pop(val)
            
            lengthy= len(Y_NODES)
        val+=1
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Append the minimum co-ordinate to the relevant list
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    X_HC_LIST.append(XMIN)
    X_HC_LIST.sort()
    
    Y_HC_LIST.append(YMIN)
    Y_HC_LIST.sort()
    
    print("SORTED")
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Creating the nodes
    
    # First, a dataframe informs what the regions are in terms of x1r, x2r, y1r, y2r
    # i.e. left-most co-ordinate, right-most co-ordinate, bottom-most co-ordinate, top-most co-ordinate
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    
    x1r = []
    x2r = []
    y1r = []
    y2r = []
    
    yi = 0
    xi = 0
    
    while yi +1<len(Y_HC_LIST):
        xi = 0
        while xi+1< len(X_HC_LIST):
            x1r.append(X_HC_LIST[xi])
            x2r.append(X_HC_LIST[xi+1])
            y1r.append(Y_HC_LIST[yi])
            y2r.append(Y_HC_LIST[yi+1])
            xi+=1
        yi+=1
    
    DATA_REGION = {"x1r":x1r,"x2r":x2r,"y1r":y1r,"y2r":y2r}
    D_R_DF = pd.DataFrame(DATA_REGION)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # For each row in the region dataframe, I want a list of x and y co-ordinates at locations from the list of nodes
    # Use the Nodes_In_Region function to identify the eligible regions
    # Nodes associated with regions outside of holes are appended to the final node list.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    
    nrdr, ncdr = D_R_DF.shape
    idr = 0
    
    XFINALS = []
    YFINALS = []
    FINALS = []
    NONFINALS = []
    
    while idr < nrdr:
        
        REGION = []
        
        hole_region_identifier, XCORDS, YCORDS = Nodes_In_Region(idr)
                
        if hole_region_identifier:
            ly = 0
            while ly<len(YCORDS):
                lx = 0
                while lx<len(XCORDS):
                            
                    REGION.append([XCORDS[lx],YCORDS[ly]])
                        
                    lx+=1
                ly+=1
                
            FINALS.append(REGION)  
        idr+=1
    
    # NEXT LINE CREATES A LIST OF VALUES WITH COORDINATES X,Y,X,Y...
    FINALS = SMUSH(FINALS)
    FINALS.sort()
    FINALS = list(FINALS for FINALS,_ in itertools.groupby(FINALS))
    FINALS = SMUSH(FINALS)
    
    for i in list(range(len(FINALS))):
        if i%2 == 0:
            XFINALS.append(FINALS[i])
        else:
            YFINALS.append(FINALS[i])

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Fine-comb for more repeats. Check the y-values and delete accordingly.
    # Must delete the x-value with the same index.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    
    lengthy = len(YFINALS)
    val=1
    while val<lengthy:
        if float(round(YFINALS[val-1],1))==float(round(YFINALS[val],1)):
            YFINALS.pop(val-1)
            XFINALS.pop(val-1)
            lengthy= len(YFINALS)
        val+=1
    
    newindex = list(range(1,len(XFINALS)+1))
    DATA_NODES = {"x":XFINALS,"y":YFINALS,"z":[0]*len(XFINALS)}
    D_N_DF = pd.DataFrame(DATA_NODES,index=newindex)
    
    nr, nc = D_N_DF.shape
    in_final=nr
    D_N_DF_ROUNDED = D_N_DF.round(4)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Creating the elements
    
    # Elements must not be accross regions as this would be erroneous.
    # Therefore, elements are sorted according to D_R_DF
    # All of the x- and y- nodes associated with each region are again identified,
    # and nodes within a 'hole region' are skipped according to the hole_region_identifier variable
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

    EL1 = []
    EL2 = []
    EL3 = []
    EL4 = []
    
    idr = 0
       
    while idr < nrdr:
        
        X1 = []
        X2 = []
        Y1 = []
        Y2 = []
        
        hole_region_identifier, XCORDS, YCORDS = Nodes_In_Region(idr)
        
        if hole_region_identifier:
            ly = 0
            while ly+1<len(YCORDS):#max(L_R_Y):
                lx = 0
                while lx+1<len(XCORDS):
                        
                    X1.append(XCORDS[lx])
                    Y1.append(YCORDS[ly])
                    X2.append(XCORDS[lx+1])
                    Y2.append(YCORDS[ly+1])
                            
                    #N_VAL += 1
                    lx+=1
                ly+=1
            
            DATA_EL_NODES = {"X1":X1,"X2":X2,"Y1":Y1,"Y2":Y2}
            D_EN_DF = pd.DataFrame(DATA_EL_NODES).round(4)
            
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
            # Nodes are ordered anticlockwise from the bottom left corner in ABAQUS S4 elements
            # The appropriate neighboring nodes for each element is search for using fast vectorised mapping.
            # The nodes are appended to the master list defined outside of the while loop
            # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
            nodes_lookup = D_N_DF_ROUNDED.reset_index().rename(columns={'index': 'nid'})[['nid', 'x', 'y']]
            
            tmp = Define_Element(nodes_lookup, D_EN_DF, 'X1', 'Y1', 'N1')
            tmp = Define_Element(nodes_lookup, tmp, 'X2', 'Y1', 'N2')
            tmp = Define_Element(nodes_lookup, tmp, 'X2', 'Y2', 'N3')
            tmp = Define_Element(nodes_lookup, tmp, 'X1', 'Y2', 'N4')
    
            D_E_DF_part = tmp[['N1', 'N2', 'N3', 'N4']]
    
            # Drop degenerate or missing elements
            D_E_DF_part = D_E_DF_part.dropna()
            D_E_DF_part = D_E_DF_part.astype(int)
            D_E_DF_part = D_E_DF_part[
                (D_E_DF_part['N1'] != D_E_DF_part['N4'])
                & (D_E_DF_part['N1'] != D_E_DF_part['N2'])
            ]
    
            # Append to master lists
            EL1.extend(D_E_DF_part['N1'].tolist())
            EL2.extend(D_E_DF_part['N2'].tolist())
            EL3.extend(D_E_DF_part['N3'].tolist())
            EL4.extend(D_E_DF_part['N4'].tolist())
            
        idr+=1
    
    # Element dataframe
    DATA_ELES = {"N1":EL1,"N2":EL2,"N3":EL3,"N4":EL4}
    D_E_DF = pd.DataFrame(DATA_ELES)
    
    # Get rid of illegal groupings
    D_NEW = (D_E_DF.index[(D_E_DF["N1"] == D_E_DF["N4"])]).tolist()
    D_E_DF.drop(D_NEW, axis=0, inplace=True)
    D_NEW = (D_E_DF.index[(D_E_DF["N1"] == D_E_DF["N2"])]).tolist()
    D_E_DF.drop(D_NEW, axis=0, inplace=True)
    
    D_E_2_r1 = np.array((D_E_DF).iloc[:,0])
    D_E_2_r2 = np.array((D_E_DF).iloc[:,1])
    D_E_2_r3 = np.array((D_E_DF).iloc[:,2])
    D_E_2_r4 = np.array((D_E_DF).iloc[:,3])
    
    # Re-index element dataframe into final state (omitting illegal groupings)
    newindex = list(range(1,len(D_E_2_r1)+1))
    DATA_ELES = {"N1":D_E_2_r1,"N2":D_E_2_r2,"N3":D_E_2_r3,"N4":D_E_2_r4}
    D_E_DF = pd.DataFrame(DATA_ELES,index=newindex)
    er, ec = D_E_DF.shape
    ie_final=er
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Save element dataframe to ELEMENTS worksheet in Excel input file (if they don't already exist)
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    if n_sheets !=4:
        with pd.ExcelWriter(INP_FIL_NAME +".xlsx",mode='a') as writer:
            D_N_DF.to_excel(writer,"NODES")
            D_E_DF.to_excel(writer,"ELEMENTS")
    
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #

#       C R E A T I N G    T H E    L I N E A R    I N P U T    F I L E       #
                    
# . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . #

    D_N_DF = pd.read_excel(INP_FIL_NAME+".xlsx",sheet_name="NODES")
    D_N_DF_inds = pd.read_excel(INP_FIL_NAME+".xlsx",sheet_name="NODES",index_col=0)
    nr, nc = D_N_DF.shape
    number_of_nodes=nr
    
    D_E_DF = pd.read_excel(INP_FIL_NAME+".xlsx",sheet_name='ELEMENTS')
    D_E_DF_inds = pd.read_excel(INP_FIL_NAME+".xlsx",sheet_name='ELEMENTS',index_col=0)
    nr, nc = D_E_DF.shape
    number_of_elements=nr
    
    X_L_NSET=(D_N_DF_inds.index[(D_N_DF_inds["x"]==XMIN)]).tolist()
    X_R_NSET=(D_N_DF_inds.index[(D_N_DF_inds["x"]==XMAX)]).tolist()

    Y_T_NSET=(D_N_DF_inds.index[(D_N_DF_inds["y"]==YMAX)]).tolist()
    Y_B_NSET=(D_N_DF_inds.index[(D_N_DF_inds["y"]==YMIN)]).tolist()
    
    X_L_MID = X_L_NSET[int(len(X_L_NSET)/2)]
    X_R_MID = X_R_NSET[int(len(X_R_NSET)/2)]
    
    Y_B_MID = Y_B_NSET[int(len(Y_B_NSET)/2)]
    Y_T_MID = Y_T_NSET[int(len(Y_T_NSET)/2)]
    
    # SETS
    # LOADED POINT (MAKE IN LINE WITH MID-POINT)
    co_ord_x_load_left = XMIN - 10
    co_ord_x_load_right = XMAX + 10
    
    co_ord_y_load_left = MIDY
    co_ord_y_load_right = MIDY
    
    co_ord_z_load_left = 0
    co_ord_z_load_right = 0
    
    # FIRST LINES FOR THE HEADING AND JOB NAMES ETC
    D_N_DF.to_csv(r"C:/Users/pemb6626/Documents/YEAR2/WP1_PLATES/COMPUTATIONAL/LIBRARY_TOOLKIT/CODE/SS/OUTPUT_ABAQUS_NODES.txt",header=False,index=False)
    D_E_DF.to_csv(r"C:/Users/pemb6626/Documents/YEAR2/WP1_PLATES/COMPUTATIONAL/LIBRARY_TOOLKIT/CODE/SS/OUTPUT_ABAQUS_ELEMENTS.txt",header=False,index=False)
    
    D_N_DF_inds.to_csv(r"C:/Users/pemb6626/Documents/YEAR2/WP1_PLATES/COMPUTATIONAL/LIBRARY_TOOLKIT/CODE/SS/OUTPUT_ABAQUS_NODES_INDS.txt",header=False,index=False)
    D_E_DF_inds.to_csv(r"C:/Users/pemb6626/Documents/YEAR2/WP1_PLATES/COMPUTATIONAL/LIBRARY_TOOLKIT/CODE/SS/OUTPUT_ABAQUS_ELEMENTS_INDS.txt",header=False,index=False)
    
    NODES = "C:/Users/pemb6626/Documents/YEAR2/WP1_PLATES/COMPUTATIONAL/LIBRARY_TOOLKIT/CODE/SS/OUTPUT_ABAQUS_NODES.txt"
    ELEMENTS = "C:/Users/pemb6626/Documents/YEAR2/WP1_PLATES/COMPUTATIONAL/LIBRARY_TOOLKIT/CODE/SS/OUTPUT_ABAQUS_ELEMENTS.txt"
    
    NODES_INDS = "C:/Users/pemb6626/Documents/YEAR2/WP1_PLATES/COMPUTATIONAL/LIBRARY_TOOLKIT/CODE/SS/OUTPUT_ABAQUS_NODES_INDS.txt"
    ELEMENTS_INDS = "C:/Users/pemb6626/Documents/YEAR2/WP1_PLATES/COMPUTATIONAL/LIBRARY_TOOLKIT/CODE/SS/OUTPUT_ABAQUS_ELEMENTS_INDS.txt"
    
    WRITE_FILE = "10_06_PRACTICE"
    READ_FILE = [NODES, ELEMENTS]
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Create Part
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    P2 = "\n** PARTS\n**\n*Part, name=PART-1\n*Node\n"
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Create Elements
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    P3 = "\n*Element, type=" +str(element_type)+"\n"
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Define element set for whole geometry and set material
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    P4 = "*Elset, elset=WHOLE_GEOMETRY, generate\n1,"+str(number_of_elements)+",1"
    P4 += F"\n** Section: Section-1-WHOLE_GEOMETRY\n*Shell Section, elset=WHOLE_GEOMETRY, material={MATERIAL}\n"
    P4 += str(thickness)+", 5\n*End Part\n**\n**\n"
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Define assembly and loaded nodes
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    P5 ="** ASSEMBLY\n**\n*Assembly, name=Assembly\n**\n*Instance, name=PART-1-1, part=PART-1\n*End Instance\n**\n"
    P5 += "*Node\n1,"+str(co_ord_x_load_left)+","+str(co_ord_y_load_left)+","+str(co_ord_z_load_left)
    P5 += "\n*Node\n2,"+str(co_ord_x_load_right)+","+str(co_ord_y_load_right)+","+str(co_ord_z_load_right)
    P5 += "\n*Nset, nset=WHOLE_GEOMETRY, instance=PART-1-1, generate\n1," +str(number_of_nodes)+",1"
    P5 += "\n*Nset, nset=XL, instance=PART-1-1\n"+EXTRACTOR(LIST_WRITER([X_L_MID]))+","
    P5 += "\n*Nset, nset=XR, instance=PART-1-1\n"+EXTRACTOR(LIST_WRITER([X_R_MID]))+","
    P5 += "\n*Nset, nset=YB, instance=PART-1-1\n"+EXTRACTOR(LIST_WRITER([Y_B_MID]))+","
    P5 += "\n*Nset, nset=YT, instance=PART-1-1\n"+EXTRACTOR(LIST_WRITER([Y_T_MID]))+","
    P5 += "\n*Nset, nset=X_L_EDGE, instance=PART-1-1\n"+EXTRACTOR(LIST_WRITER(X_L_NSET))
    P5 += "\n*Nset, nset=X_R_EDGE, instance=PART-1-1\n"+EXTRACTOR(LIST_WRITER(X_R_NSET))
    P5 += "\n*Nset, nset=Y_B_EDGE, instance=PART-1-1\n"+EXTRACTOR(LIST_WRITER(Y_B_NSET))
    P5 += "\n*Nset, nset=Y_T_EDGE, instance=PART-1-1\n"+EXTRACTOR(LIST_WRITER(Y_T_NSET))
    P5 += "\n*Nset, nset=loaded_left\n1,"
    P5 += "\n*Nset, nset=loaded_right\n2,"
    P5 += "\n*Surface, type=NODE, name=X_L_EDGE_CNS_, internal\nX_L_EDGE, 1."
    P5 += "\n*Surface, type=NODE, name=X_R_EDGE_CNS_, internal\nX_R_EDGE, 1."
    P5 +="\n** Constraint: Constraint-1\n*Coupling, constraint name=Constraint-1, ref node=loaded_left, surface=X_L_EDGE_CNS_\n*Distributing, weighting method=UNIFORM"
    P5 +="\n** Constraint: Constraint-2\n*Coupling, constraint name=Constraint-2, ref node=loaded_right, surface=X_R_EDGE_CNS_\n*Distributing, weighting method=UNIFORM\n*End Assembly\n**\n"
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    # Define material properties
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    if MATERIAL == "STEEL_RO":
        Default = str(input(""""D E F A U L T   V A L U E S   F O R   S T E E L ? (Y/N)
Young's Modulus = 203400 MPa
Poisson's Ratio = 0.3
Yield Strength = 450 MPa
Hardening Exponent = 8
Yield Offset = 0.904"""))
        if Default == "N":
            E = str(input("Y O U N G S   M O D U L U S   (M P a) = "))
            v = str(input("P O I S S O N ' S   R A T I O = "))
            ys = str(input("Y I E L D   S T R E N G T H   (M P a) = "))
            nexp = str(input("H A R D E N I N G   E X P O N E N T = "))
            alpha = str(input("Y I E L D   O F F S E T = "))
        else:
            E = "203400"
            v = "0.3"
            ys = "450"
            nexp = "8"
            alpha = "0.904"
        P6 = f"** MATERIALS\n**\n*Material, name={MATERIAL}\n*Deformation Plasticity\n"+E+","+v+","+ys+","+nexp+","+alpha+"\n**"
    elif MATERIAL == "STEEL_SD":
         P6 = f"""** MATERIALS
** 
*Material, name={MATERIAL}
*Elastic
 203400, 0.3
*Plastic
 450,          0.
 455.09, 0.00021
 460.23, 0.00051
 465.52, 0.00111
 471.12, 0.00239
 477.29, 0.00483
 485.35, 0.00907
 492.69, 0.01585
 502.75, 0.02602
 515.04, 0.04048
 530.09, 0.06018
**"""

    elif MATERIAL == "ALUMINIUM":
         P6 = f"""** MATERIALS
** 
*Material, name={MATERIAL}
*Elastic
 60073.5, 0.33
*Plastic
 78.0955,          0.
 78.6679, 4.87013e-06
 83.0176, 3.47809e-05
   83.82, 4.02475e-05
  84.956, 6.56712e-05
  87.421, 0.000127628
 89.8845, 0.000221616
 92.0401, 0.000375636
 94.2774, 0.000633782
 96.5057,  0.00100217
 98.7358,  0.00155987
 100.966,  0.00227367
 103.195,  0.00309864
 105.425,   0.0039664
**"""
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
# Define boundary conditions
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
    P7 = """\n**BOUNDARY CONDITIONS
** 
** Name: Disp-BC-1 Type: Displacement/Rotation
*Boundary
XL, 2, 2
** Name: Disp-BC-2 Type: Displacement/Rotation
*Boundary
XR, 2, 2
** Name: Disp-BC-3 Type: Displacement/Rotation
*Boundary
YB, 1, 1
** Name: Disp-BC-4 Type: Displacement/Rotation
*Boundary
YT, 1, 1
** Name: Disp-BC-5 Type: Displacement/Rotation
*Boundary
X_L_EDGE, 3, 3
** Name: Disp-BC-6 Type: Displacement/Rotation
*Boundary
X_R_EDGE, 3, 3
** Name: Disp-BC-7 Type: Displacement/Rotation
*Boundary
Y_T_EDGE, 3, 3
** Name: Disp-BC-8 Type: Displacement/Rotation
*Boundary
Y_B_EDGE, 3, 3
** ----------------------------------------------------------------  
"""

    if Linear_Input_File:    
        
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # Define linear set-up
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        P1_L ="*Heading\n** Job name: "+str(FIL_NAME)+"_L Model name: "+str(FIL_NAME)+"_L"
        P1_L +="\n** Generated by: Abaqus/CAE 2022\n*Preprint, echo=NO, model=NO, history=NO, contact=NO\n**"
        P2 = "\n** PARTS\n**\n*Part, name=PART-1\n*Node\n"
        
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # Define linear step
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        P8_L = """** 
** STEP: Step-1
** 
*Step, name=Step-1, nlgeom=NO, perturbation
*Buckle
10, , 18, 300
**  
"""
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # Define linear loading
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        P9_L = "**LOADS\n**\n**Name: LEFTLOAD Type: Concentrated force\n*Cload\n"
        P9_L += "loaded_left, 1, "+str(1)
        P9_L +="\n"
        P9_L += "**Name: RIGHTLOAD Type: Concentrated force\n*Cload\n"
        P9_L += "loaded_right, 1, "+str(-1)
        P9_L +="\n**"
    
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # Linear output
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        P10_L = """\n** OUTPUT REQUESTS
** 
*Restart, write, frequency=0
** 
** FIELD OUTPUT: F-Output-1
* 
*Output, field, variable=PRESELECT
*NODE FILE, GLOBAL=NO,
MODE = 1, LAST MODE=5
U
*End Step
"""
        with open(OUT_FIL_NAME_L,"w+") as f:
            f.writelines(P1_L)
            f.writelines(P2)
            f.write(EXTRACTOR(NODES))
            f.write(P3)
            f.write(EXTRACTOR(ELEMENTS))
            f.write(P4)
            f.write(P5)
            f.write(P6)
            f.write(P7)
            f.write(P8_L)
            f.write(P9_L)
            f.write(P10_L)

    if Nonlinear_Input_File:
        
        if Eigenmode_Choice:
            EIG = int(input("F I R S T   P O S I T I V E   E I G E N M O D E  (G E O M E T R I C   I M P E R F E C T I O N) = "))
        else:
            EIG = 1
        
        EIGENSCALE = min((XMAX-XMIN)/200,(YMAX-YMIN)/200) # SCALE IS ARBITRARY, CHANGE TO BE SOME FACTOR OF LENGTH OR WIDTH ACCORDING TO GUIDANCE
        
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # Define nonlinear set-up
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        P1_NL ="*Heading\n** Job name: "+str(FIL_NAME)+"_NL Model name: "+str(FIL_NAME)+"_NL"
        P1_NL +="\n** Generated by: Abaqus/CAE 2022\n*Preprint, echo=NO, model=NO, history=NO, contact=NO\n**"
        
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # Define nonlinear imperfection
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        PI = "\n*IMPERFECTION, FILE= "+FIL_NAME+"_L, STEP=1, nset=WHOLE_GEOMETRY\n"+str(EIG)+","+str(EIGENSCALE)
        
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # Define nonlinear solution control
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        if CONTROL == "L":
            P8_NL = "**\n** STEP: Step-1\n**\n*Step, name=Step-1, nlgeom=YES, inc="+str(inc)+"\n*Static, riks\n"+str(start_ss)+","+str(arc)+","+str(min_ss)+","+str(max_ss)+","+str(lpf)+","+"\n**\n"
        
        elif CONTROL == "D":
            P8_NL = "**\n** STEP: Step-1\n**\n*Step, name=Step-1, nlgeom=YES, inc="+str(inc)+"\n*Static, riks\n"+str(start_ss)+","+str(arc)+","+str(min_ss)+","+str(max_ss)+","+str(lpf)+", loaded_left, 1, "+str(disp_max)+"\n**\n"
            
        elif CONTROL == "NO":
            P8_NL = "**\n** STEP: Step-1\n**\n*Step, name=Step-1, nlgeom=YES, inc="+str(inc)+"\n*Static\n"+str(start_ss_nr)+","+str(time_nr)+","+str(min_ss_nr)+","+str(max_ss_nr)+"\n**\n"
        
        elif CONTROL == "ND":
            P8_NL = "**\n** STEP: Step-1\n**\n*Step, name=Step-1, nlgeom=YES, inc="+str(inc)+"\n*Static, stabilize, allsdtol="+str(accuracy_tolerance)+"\n"+str(start_ss_nr)+","+str(time_nr)+","+str(min_ss_nr)+","+str(max_ss_nr)+"\n**\n"
        
        elif CONTROL == "NT":
            
            P8_NL = """**\n** STEP: Step-1
**
*Step, name=Step-1, nlgeom=YES, inc=175
*Static, stabilize, allsdtol=0.01
*Controls, parameters=Time Incrementation
** Relax checks on rate of convergence:
** IO   IR   IP   IC   IL   IG
   16 , 18 , 20 , 40 , 30 ,  6
0.001,1,1e-06,0.01
**\n"""
   
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # Define nonlinear loading
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        ELASTIC_CAPACITY = float(input("E L A S T I C   C A P A C I T Y   F R O M   L I N E A R   P E R T U R B A T I O N   A S S E S S M E N T   (N) = "))
        if CONTROL == "L":
            
            P9_NL = "**LOADS\n**\n**Name: LEFTLOAD Type: Concentrated force\n*Cload\n"
            P9_NL += "loaded_left, 1, "+str(ELASTIC_CAPACITY)
            #P9 += "\nloaded_left, 2,"+str(ELASTIC_CAPACITY*y_load_mag)
            #P9+="\nloaded_left,3,"+str(ELASTIC_CAPACITY*z_load_mag)
            P9_NL +="\n"
            P9_NL += "**Name: RIGHTLOAD Type: Concentrated force\n*Cload\n"
            P9_NL += "loaded_right, 1, "+str(-1*ELASTIC_CAPACITY)
            #P9 += "\nloaded_right, 2,"+str(-1*ELASTIC_CAPACITY*y_load_mag)
            #P9+="\nloaded_right,3,"+str(-1*ELASTIC_CAPACITY*z_load_mag)+"\n**"
            P9_NL +="\n**"
        
        elif CONTROL == "D":
            
            P9_NL = "**LOADS\n**\n**Name: BC-9 Type: Displacement/Rotation\n*Boundary\n"
            P9_NL += "loaded_left, 1, 1, "+str(ELASTIC_CAPACITY/100)
            P9_NL +="\n"
            P9_NL += "**Name: BC-10 Type: Displacement/Rotation\n*Boundary\n"
            P9_NL += "loaded_right, 1, 1, "+str(-1*ELASTIC_CAPACITY/100)
            P9_NL +="\n**"
            
        elif CONTROL == "NO" or CONTROL == "ND" :
            
            P9_NL = "**LOADS\n**\n**Name: BC-9 Type: Displacement/Rotation\n*Boundary\n"
            P9_NL += "loaded_left, 1, 1, "+str(nr_disp)
            P9_NL +="\n"
            P9_NL += "**Name: BC-10 Type: Displacement/Rotation\n*Boundary\n"
            P9_NL += "loaded_right, 1, 1, "+str(-1*nr_disp)
            P9_NL +="\n**"

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        # Nonlinear Output
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
        P10_NL = """\n** OUTPUT REQUESTS
** 
*Restart, write, frequency=0
** 
** FIELD OUTPUT: F-Output-1
** 
*Output, field
*Node Output
CF, RF, U
*Element Output, directions=YES
LE, PE, PEEQ, PEMAG, S, SF
*Contact Output
CDISP, CSTRESS
** 
** HISTORY OUTPUT: H-Output-1
** 
*Output, history
*Node Output, nset=loaded_left
CF1, CF2, CF3, CM1, CM2, CM3, RF1, RF2
RF3, RM1, RM2, RM3, U1, U2, U3, UR1
UR2, UR3
*End Step 
"""
        with open(OUT_FIL_NAME_NL,"w+") as f:
            f.writelines(P1_NL)
            f.writelines(P2)
            f.write(EXTRACTOR(NODES))
            f.write(P3)
            f.write(EXTRACTOR(ELEMENTS))
            f.write(P4)
            f.write(P5)
            f.write(P6)
            f.write(PI)
            f.write(P7)
            f.write(P8_NL)
            f.write(P9_NL)
            f.write(P10_NL)
            








