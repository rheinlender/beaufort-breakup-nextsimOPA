"""
Standard definitions and functions

Created on Wed Dec 01 2021
@authors: Jonathan Rheinlænder
"""

BOXNAMES_LIST = ["ICEsat","CFR","Arctic","BFG","EBB","CREG","BGR","Fram","BBB","ALL","NANUK_PAPER","NANUK_PAPER_leads"]

# NSIDC regions
NSIDC_region_dic={"Other":1, 
                  "Japan":2,
                  "Bering":3,
                  "Hudson":4,
                  "StLaurent":5, 
                  "Greenland":6,
                  "Labrador":7,
                  "Barents":8,
                  "Kara":9,
                  "Laptev":10,
                  "Siberia":11,
                  "Chukchi":12,
                  "Beaufort":13,
                  "CAA":14,
                  "Arctic":15,
                  "Land":20,
                  "Coast":21}


# dictionary with box definitions on the nextsim grid
BOXNAMES = {"Beaufort": (95,225,425,575),
            "Large_Arctic": (0,528,0,603)}