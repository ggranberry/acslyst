import matplotlib.pyplot as plt
import numpy as np

# Simulated data structure for demonstration. Replace with your actual data extraction logic.
data = {
  "Struct": {
    "count_annotations/3_generations/Struct": {"ensures": 9, "behavior": 6, "assumes": 6, "requires": 3, "complete behaviors": 3, "disjoint behaviors": 3, "invariant": 2, "assigns": 1},
    "count_annotations_eva/backup_first_run/Struct": {"ensures": 4, "requires": 3, "behavior": 2, "assumes": 2, "complete behaviors": 1, "disjoint behaviors": 1},
    "count_annotations_pathcrawler/third_run_headers/Struct": {"ensures": 4, "requires": 2, "behavior": 2, "assumes": 2, "assigns": 1, "complete behaviors": 1, "disjoint behaviors": 1}
  },
  "MergeWithBreaks": {
    "count_annotations/3_generations/MergeWithBreaks": {"loop invariant": 18, "requires": 10, "loop assigns": 9, "loop variant": 6, "ensures": 5, "behavior": 2, "assumes": 2, "assigns": 2, "complete behaviors": 1, "disjoint behaviors": 1},
    "count_annotations_eva/backup_first_run/MergeWithBreaks": {"loop invariant": 17, "loop assigns": 9, "requires": 7, "ensures": 7, "loop variant": 3, "assigns": 1},
    "count_annotations_pathcrawler/third_run_headers/MergeWithBreaks": {"loop invariant": 18, "requires": 12, "loop assigns": 9, "ensures": 8, "loop variant": 6, "assigns": 1}
  },
  "BugKpath": {
    "count_annotations/3_generations/BugKpath": {"loop invariant": 8, "requires": 7, "loop assigns": 6, "loop variant": 6, "ensures": 3, "ghost": 3, "assigns": 2, "behavior": 1, "assert": 1},
    "count_annotations_eva/backup_first_run/BugKpath": {"loop invariant": 8, "requires": 7, "loop assigns": 6, "ensures": 5, "assert": 5, "assigns": 2, "loop variant": 2},
    "count_annotations_pathcrawler/third_run_headers/BugKpath": {"loop invariant": 9, "requires": 8, "loop assigns": 6, "loop variant": 6, "ensures": 3, "assert": 1, "assigns": 1}
  },
  "FloatTritypeLabels": {
    "count_annotations/3_generations/FloatTritypeLabels": {"assert": 13, "requires": 5, "ensures": 3, "assigns": 2},
    "count_annotations_eva/backup_first_run/FloatTritypeLabels": {"requires": 9, "ensures": 3, "assigns": 1},
    "count_annotations_pathcrawler/third_run_headers/FloatTritypeLabels": {"ensures": 9, "behavior": 6, "assumes": 6, "requires": 5, "complete behaviors": 2, "disjoint behaviors": 2}
  },
  "TestCondCoverage1": {
    "count_annotations/3_generations/TestCondCoverage1": {"ensures": 15, "requires": 10, "assigns": 5, "behavior": 3, "assumes": 3, "loop invariant": 2, "loop assigns": 2, "loop variant": 2},
    "count_annotations_eva/backup_first_run/TestCondCoverage1": {"ensures": 9, "requires": 7, "assigns": 4, "loop invariant": 2, "loop assigns": 2, "loop variant": 2},
    "count_annotations_pathcrawler/third_run_headers/TestCondCoverage1": {"ensures": 21, "requires": 8, "behavior": 6, "assumes": 6, "assigns": 4, "loop invariant": 3, "loop assigns": 3, "loop variant": 3, "complete behaviors": 1, "disjoint behaviors": 1}
  },
  "DatesBranches": {
    "count_annotations/3_generations/DatesBranches": {"requires": 15, "ensures": 15, "loop invariant": 7, "loop assigns": 7, "assigns": 6, "loop variant": 6, "predicate": 4},
    "count_annotations_eva/backup_first_run/DatesBranches": {"requires": 12, "ensures": 11, "loop invariant": 8, "loop assigns": 8, "assert": 7, "assigns": 5, "loop variant": 4},
    "count_annotations_pathcrawler/third_run_headers/DatesBranches": {"requires": 6, "behavior": 4, "assumes": 4, "ensures": 4, "loop invariant": 2, "loop assigns": 2, "loop variant": 2, "complete behaviors": 1, "disjoint behaviors": 1, "assert": 1}
  },
  "TestCondCoverage3": {
    "count_annotations/3_generations/TestCondCoverage3": {"requires": 12, "ensures": 8, "assigns": 7, "loop invariant": 1, "loop assigns": 1, "loop variant": 1},
    "count_annotations_eva/backup_first_run/TestCondCoverage3": {"ensures": 11, "requires": 7, "assigns": 7, "ghost": 4, "loop invariant": 3, "loop assigns": 2, "loop variant": 2},
    "count_annotations_pathcrawler/third_run_headers/TestCondCoverage3": {"requires": 23, "ensures": 9, "loop invariant": 4, "loop assigns": 3, "loop variant": 3, "assigns": 2}
  },
  "MergePrecond": {
    "count_annotations/3_generations/MergePrecond": {"loop invariant": 28, "requires": 14, "loop assigns": 13, "loop variant": 13, "ensures": 10, "assigns": 7, "predicate": 1},
    "count_annotations_eva/backup_first_run/MergePrecond": {"requires": 23, "loop invariant": 19, "loop assigns": 11, "loop variant": 11, "assumes": 4, "ensures": 3, "assigns": 2, "behavior": 1},
    "count_annotations_pathcrawler/third_run_headers/MergePrecond": {"loop invariant": 18, "loop assigns": 9, "requires": 8, "ensures": 5, "loop variant": 3}
  },
  "Interp": {
    "count_annotations/3_generations/Interp": {"requires": 14, "loop invariant": 5, "assigns": 3, "ensures": 2, "loop variant": 2, "loop assigns": 2},
    "count_annotations_eva/backup_first_run/Interp": {"requires": 9, "ensures": 5, "loop invariant": 3, "loop assigns": 3, "assert": 1, "assigns": 1},
    "count_annotations_pathcrawler/third_run_headers/Interp": {"requires": 14, "ensures": 8, "loop invariant": 4, "loop assigns": 3, "loop variant": 2, "assigns": 1}
  },
  "AssertAssume": {
    "count_annotations/3_generations/AssertAssume": {"requires": 10, "ensures": 8, "predicate": 7, "behavior": 6, "assumes": 6, "complete behaviors": 2, "disjoint behaviors": 2, "loop invariant": 2, "loop assigns": 2, "loop variant": 2},
    "count_annotations_eva/backup_first_run/AssertAssume": {},
    "count_annotations_pathcrawler/third_run_headers/AssertAssume": {"requires": 9, "ensures": 9, "behavior": 4, "assumes": 4, "loop invariant": 3, "loop assigns": 3, "loop variant": 3, "predicate": 2, "complete behaviors": 2, "disjoint behaviors": 2}
  },
  "ADPCM1": {
    "count_annotations/3_generations/ADPCM1": {"requires": 12, "ensures": 11, "assumes": 5, "loop invariant": 3, "loop assigns": 3, "loop variant": 3, "behavior": 2},
    "count_annotations_eva/backup_first_run/ADPCM1": {"requires": 12, "ensures": 6, "assigns": 4, "loop invariant": 3, "loop assigns": 3, "loop variant": 1},
    "count_annotations_pathcrawler/third_run_headers/ADPCM1": {"requires": 17, "ensures": 13, "assigns": 4, "behavior": 4, "assumes": 4, "loop invariant": 2, "loop assigns": 2, "loop variant": 1}
  },
  "Test_ptr_out": {
    "count_annotations/3_generations/Test_ptr_out": {"ensures": 14, "requires": 3, "assigns": 2},
    "count_annotations_eva/backup_first_run/Test_ptr_out": {"ensures": 4, "requires": 3},
    "count_annotations_pathcrawler/third_run_headers/Test_ptr_out": {"ensures": 9, "requires": 5, "assigns": 2}
  },
  "VariableDimArray2": {
    "count_annotations/3_generations/VariableDimArray2": {"requires": 7, "ensures": 4, "assert": 4, "assigns": 3, "behavior": 2, "assumes": 2, "disjoint behaviors": 1, "complete behaviors": 1},
    "count_annotations_eva/backup_first_run/VariableDimArray2": {"requires": 11, "assigns": 2, "ensures": 2},
    "count_annotations_pathcrawler/third_run_headers/VariableDimArray2": {"requires": 8, "ensures": 6, "behavior": 3, "assumes": 3, "complete behaviors": 1, "disjoint behaviors": 1}
  },
  "PointeurFonction1": {
    "count_annotations/3_generations/PointeurFonction1": {"ensures": 14, "behavior": 7, "assumes": 7, "requires": 6, "assigns": 5, "complete behaviors": 2, "disjoint behaviors": 2},
    "count_annotations_eva/backup_first_run/PointeurFonction1": {"requires": 10, "ensures": 6, "assigns": 1},
    "count_annotations_pathcrawler/third_run_headers/PointeurFonction1": {"ensures": 11, "requires": 4, "behavior": 2, "assumes": 2, "complete behaviors": 1, "disjoint behaviors": 1}
  },
  "BsearchPrecond": {
    "count_annotations/3_generations/BsearchPrecond": {"ensures": 17, "requires": 15, "loop invariant": 10, "behavior": 8, "assumes": 8, "loop assigns": 6, "loop variant": 6, "complete behaviors": 4, "disjoint behaviors": 4, "assigns": 2, "predicate": 1},
    "count_annotations_eva/backup_first_run/BsearchPrecond": {"requires": 13, "ensures": 12, "loop invariant": 9, "assigns": 8, "loop assigns": 6, "loop variant": 6},
    "count_annotations_pathcrawler/third_run_headers/BsearchPrecond": {"ensures": 12, "requires": 10, "loop invariant": 5, "loop assigns": 4, "loop variant": 2, "behavior": 2, "assumes": 2, "predicate": 1, "assigns": 1, "complete behaviors": 1, "disjoint behaviors": 1}
  },
  "LabelsTcas": {
    "count_annotations/3_generations/LabelsTcas": {"ensures": 24, "requires": 7, "assigns": 2, "predicate": 2},
    "count_annotations_eva/backup_first_run/LabelsTcas": {"ensures": 16, "requires": 9, "assigns": 5, "ghost": 2, "assumes": 1},
    "count_annotations_pathcrawler/third_run_headers/LabelsTcas": {"requires": 30, "ensures": 20, "invariant": 13, "assigns": 7}
  },
  "Tritype": {
    "count_annotations/3_generations/Tritype": {"ensures": 9, "assigns": 7, "requires": 6, "behavior": 4, "assumes": 4},
    "count_annotations_eva/backup_first_run/Tritype": {"requires": 5, "ensures": 3},
    "count_annotations_pathcrawler/third_run_headers/Tritype": {"ensures": 16, "behavior": 14, "assumes": 14, "requires": 3, "complete behaviors": 2, "disjoint behaviors": 2, "assigns": 1}
  },
  "MutualRecursion": {
    "count_annotations/3_generations/MutualRecursion": {"requires": 8, "ensures": 6, "assert": 4, "behavior": 2, "assumes": 2, "complete behaviors": 1, "disjoint behaviors": 1},
    "count_annotations_eva/backup_first_run/MutualRecursion": {"requires": 6, "assigns": 6, "ensures": 6},
    "count_annotations_pathcrawler/third_run_headers/MutualRecursion": {"requires": 6, "ensures": 4, "assigns": 2}
  },
  "IntTritypeLabels": {
    "count_annotations/3_generations/IntTritypeLabels": {"ensures": 16, "behavior": 12, "assumes": 12, "requires": 7, "assert": 3, "assigns": 2},
    "count_annotations_eva/backup_first_run/IntTritypeLabels": {"assigns": 8, "behavior": 7, "assumes": 7, "requires": 4, "assert": 4, "ensures": 3},
    "count_annotations_pathcrawler/third_run_headers/IntTritypeLabels": {"ensures": 7, "assert": 7, "behavior": 6, "assumes": 6, "requires": 3, "ghost": 1, "complete behaviors": 1, "disjoint behaviors": 1}
  },
  "BsearchPrecond1": {
    "count_annotations/3_generations/BsearchPrecond1": {"requires": 20, "ensures": 16, "loop invariant": 13, "behavior": 8, "assumes": 8, "assigns": 7, "loop assigns": 6, "loop variant": 6, "complete behaviors": 4, "disjoint behaviors": 4, "predicate": 1},
    "count_annotations_eva/backup_first_run/BsearchPrecond1": {"requires": 16, "loop invariant": 12, "ensures": 11, "assigns": 8, "loop assigns": 6, "loop variant": 6, "assert": 4, "behavior": 2, "assumes": 2, "ghost": 1, "complete behaviors": 1, "disjoint behaviors": 1},
    "count_annotations_pathcrawler/third_run_headers/BsearchPrecond1": {"requires": 16, "loop invariant": 15, "ensures": 9, "loop assigns": 6, "loop variant": 6, "assigns": 3, "behavior": 2, "assumes": 2, "complete behaviors": 1, "disjoint behaviors": 1}
  },
  "PointeurFonction5": {
    "count_annotations/3_generations/PointeurFonction5": {"ensures": 12, "requires": 10, "assigns": 5},
    "count_annotations_eva/backup_first_run/PointeurFonction5": {"requires": 40, "ensures": 12, "assert": 4, "loop invariant": 1, "loop assigns": 1, "loop variant": 1, "assigns": 1},
    "count_annotations_pathcrawler/third_run_headers/PointeurFonction5": {"requires": 13, "ensures": 10, "behavior": 4, "assumes": 4, "complete behaviors": 2, "disjoint behaviors": 2}
  },
  "Luhn": {
    "count_annotations/3_generations/Luhn": {"requires": 15, "loop invariant": 9, "assert": 8, "ensures": 7, "assigns": 6, "loop assigns": 6, "loop variant": 6},
    "count_annotations_eva/backup_first_run/Luhn": {"requires": 14, "ensures": 6, "loop invariant": 5, "ghost": 4, "loop assigns": 4, "loop variant": 4},
    "count_annotations_pathcrawler/third_run_headers/Luhn": {"requires": 17, "ensures": 11, "loop invariant": 6, "behavior": 5, "assumes": 5, "loop assigns": 4, "loop variant": 4, "assigns": 4, "disjoint behaviors": 2, "complete behaviors": 2}
  },
  "Sample": {
    "count_annotations/3_generations/Sample": {"requires": 9, "loop invariant": 6, "loop assigns": 6, "loop variant": 6, "ensures": 3, "assert": 2, "assigns": 1},
    "count_annotations_eva/backup_first_run/Sample": {"requires": 8, "ensures": 6, "loop invariant": 6, "loop assigns": 6, "loop variant": 6, "behavior": 4, "assumes": 4, "complete behaviors": 2, "disjoint behaviors": 2},
    "count_annotations_pathcrawler/third_run_headers/Sample": {"loop invariant": 8, "loop assigns": 6, "loop variant": 6, "ensures": 5, "requires": 4, "behavior": 2, "assumes": 2}
  },
  "Merge": {
    "count_annotations/3_generations/Merge": {"loop invariant": 21, "requires": 9, "loop assigns": 9, "loop variant": 9, "ensures": 4, "assigns": 3, "behavior": 1, "assumes": 1},
    "count_annotations_eva/backup_first_run/Merge": {"loop invariant": 10, "loop assigns": 9, "requires": 7, "ensures": 3, "assigns": 1},
    "count_annotations_pathcrawler/third_run_headers/Merge": {"requires": 11, "loop invariant": 10, "loop assigns": 9, "ensures": 6, "loop variant": 3}
  },
  "Alias3": {
    "count_annotations/3_generations/Alias3": {"requires": 10, "assigns": 6, "ensures": 5, "assert": 2, "behavior": 2, "assumes": 2, "complete behaviors": 1, "disjoint behaviors": 1},
    "count_annotations_eva/backup_first_run/Alias3": {"requires": 5, "ensures": 4, "assigns": 2, "assert": 2},
    "count_annotations_pathcrawler/third_run_headers/Alias3": {"requires": 8, "assigns": 4, "ensures": 4}
  },
  "VariableDimArray1": {
    "count_annotations/3_generations/VariableDimArray1": {"ensures": 5, "requires": 4, "assigns": 2, "assert": 2, "behavior": 2, "assumes": 2},
    "count_annotations_eva/backup_first_run/VariableDimArray1": {"requires": 9, "assert": 3, "assigns": 1},
    "count_annotations_pathcrawler/third_run_headers/VariableDimArray1": {"ensures": 6, "requires": 4, "behavior": 2, "assumes": 2, "assigns": 1, "complete behaviors": 1, "disjoint behaviors": 1}
  },
  "Alias5": {
    "count_annotations/3_generations/Alias5": {"assigns": 12, "ensures": 11, "assert": 9, "requires": 7},
    "count_annotations_eva/backup_first_run/Alias5": {"requires": 9, "ensures": 7, "assumes": 6, "behavior": 5, "assigns": 5, "assert": 3},
    "count_annotations_pathcrawler/third_run_headers/Alias5": {"requires": 9, "assert": 9, "assigns": 4, "ensures": 4}
  },
  "TestCondCoverage2": {
    "count_annotations/3_generations/TestCondCoverage2": {"assigns": 15, "requires": 12, "ensures": 11, "loop invariant": 3, "loop assigns": 3, "loop variant": 3},
    "count_annotations_eva/backup_first_run/TestCondCoverage2": {"ensures": 8, "loop invariant": 3, "requires": 3, "loop assigns": 2, "loop variant": 1},
    "count_annotations_pathcrawler/third_run_headers/TestCondCoverage2": {"requires": 17, "ensures": 13, "behavior": 3, "assumes": 3, "loop invariant": 2, "loop assigns": 2, "loop variant": 2, "assigns": 2}
  },
  "MutualRecursionNoRecurLimit": {
    "count_annotations/3_generations/MutualRecursionNoRecurLimit": {"requires": 6, "ensures": 6, "assigns": 4, "behavior": 2, "assumes": 2, "assert": 2},
    "count_annotations_eva/backup_first_run/MutualRecursionNoRecurLimit": {"ensures": 7, "requires": 4, "assigns": 4, "assert": 3, "assumes": 2},
    "count_annotations_pathcrawler/third_run_headers/MutualRecursionNoRecurLimit": {"ensures": 8, "requires": 6, "behavior": 2, "assumes": 2}
  },
  "Bsearch": {
    "count_annotations/3_generations/Bsearch": {"ensures": 18, "assigns": 18, "loop invariant": 7, "requires": 6, "loop assigns": 3, "loop variant": 3, "behavior": 2, "assumes": 2, "complete behaviors": 1, "disjoint behaviors": 1},
    "count_annotations_eva/backup_first_run/Bsearch": {"loop invariant": 8, "assert": 7, "requires": 6, "ensures": 6, "behavior": 4, "assumes": 4, "loop assigns": 3, "loop variant": 3, "complete behaviors": 2, "disjoint behaviors": 2},
    "count_annotations_pathcrawler/third_run_headers/Bsearch": {"requires": 5, "loop invariant": 4, "assigns": 4, "ensures": 3, "loop assigns": 3, "loop variant": 2}
  },
  "EchoBranches": {
    "count_annotations/3_generations/EchoBranches": {"ensures": 9, "requires": 7, "assigns": 4, "behavior": 2, "assumes": 2, "complete behaviors": 1, "disjoint behaviors": 1},
    "count_annotations_eva/backup_first_run/EchoBranches": {"requires": 9, "loop assigns": 5, "loop invariant": 4, "loop variant": 4, "assigns": 3, "assert": 2, "ensures": 2},
    "count_annotations_pathcrawler/third_run_headers/EchoBranches": {"requires": 8, "ensures": 3, "loop invariant": 1}
  },
  "Tcas": {
    "count_annotations/3_generations/Tcas": {"ensures": 14, "requires": 10},
    "count_annotations_eva/backup_first_run/Tcas": {"ensures": 17, "requires": 12},
    "count_annotations_pathcrawler/third_run_headers/Tcas": {"ensures": 9, "requires": 8, "assigns": 4}
  },
  "Heat1": {
    "count_annotations/3_generations/Heat1": {"requires": 14, "ensures": 14, "ghost": 9, "assigns": 3},
    "count_annotations_eva/backup_first_run/Heat1": {"requires": 22, "ensures": 11, "assigns": 9},
    "count_annotations_pathcrawler/third_run_headers/Heat1": {"requires": 14, "ensures": 9, "assigns": 3}
  },
  "Heat": {
    "count_annotations/3_generations/Heat": {"requires": 13, "ensures": 10, "ghost": 9, "assigns": 3, "behavior": 2, "assumes": 2, "loop invariant": 2, "loop assigns": 2, "complete behaviors": 1, "disjoint behaviors": 1},
    "count_annotations_eva/backup_first_run/Heat": {"ensures": 20, "requires": 19, "assigns": 1},
    "count_annotations_pathcrawler/third_run_headers/Heat": {"requires": 17, "ensures": 4, "loop invariant": 1, "loop assigns": 1}
  },
  "Bsort": {
    "count_annotations/3_generations/Bsort": {"requires": 6, "assigns": 6, "loop invariant": 6, "loop assigns": 6, "loop variant": 6, "ensures": 3, "behavior": 1},
    "count_annotations_eva/backup_first_run/Bsort": {"ensures": 8, "requires": 7, "loop invariant": 6, "loop assigns": 6, "assigns": 2, "loop variant": 2, "assert": 1},
    "count_annotations_pathcrawler/third_run_headers/Bsort": {"loop invariant": 8, "loop assigns": 6, "requires": 4, "loop variant": 4, "ensures": 3, "assigns": 1}
  },
  "ExSysC": {
    "count_annotations/3_generations/ExSysC": {"assert": 10, "ensures": 4, "assigns": 4, "requires": 3, "behavior": 2, "assumes": 2, "predicate": 1},
    "count_annotations_eva/backup_first_run/ExSysC": {"assert": 5, "ensures": 4, "requires": 3, "assigns": 2},
    "count_annotations_pathcrawler/third_run_headers/ExSysC": {"ensures": 5, "requires": 3, "assigns": 2}
  },
  "Alias1": {
    "count_annotations/3_generations/Alias1": {"ensures": 7, "requires": 6, "assert": 4, "assigns": 3, "behavior": 2, "assumes": 2},
    "count_annotations_eva/backup_first_run/Alias1": {"assert": 9, "requires": 3, "ensures": 1, "assigns": 1},
    "count_annotations_pathcrawler/third_run_headers/Alias1": {"ensures": 6, "requires": 4, "assert": 4, "behavior": 2, "assumes": 2, "assigns": 1}
  },
  "ApacheBranches": {
    "count_annotations/3_generations/ApacheBranches": {"ensures": 14, "requires": 13, "loop invariant": 12, "loop assigns": 10, "loop variant": 10, "assigns": 9, "behavior": 8, "assumes": 8, "complete behaviors": 1, "disjoint behaviors": 1},
    "count_annotations_eva/backup_first_run/ApacheBranches": {"requires": 11, "assigns": 10, "loop assigns": 9, "loop invariant": 8, "ensures": 6, "loop variant": 6},
    "count_annotations_pathcrawler/third_run_headers/ApacheBranches": {"requires": 11, "assigns": 9, "loop invariant": 8, "ensures": 7, "loop assigns": 7, "loop variant": 3}
  },
  "PointeurFonction2": {
    "count_annotations/3_generations/PointeurFonction2": {"requires": 14, "assigns": 7, "ensures": 6, "assert": 1},
    "count_annotations_eva/backup_first_run/PointeurFonction2": {"requires": 14, "ensures": 11, "assigns": 4, "assert": 2, "logic": 1},
    "count_annotations_pathcrawler/third_run_headers/PointeurFonction2": {"requires": 8, "ensures": 5, "assigns": 2, "assert": 2, "behavior": 2, "assumes": 2}
  },
  "ExNikoWCET": {
    "count_annotations/3_generations/ExNikoWCET": {"loop invariant": 12, "loop assigns": 9, "loop variant": 9, "requires": 5, "ensures": 2, "assigns": 2},
    "count_annotations_eva/backup_first_run/ExNikoWCET": {"loop invariant": 9, "loop assigns": 9, "requires": 8, "ensures": 8, "loop variant": 6, "assert": 5, "assigns": 2},
    "count_annotations_pathcrawler/third_run_headers/ExNikoWCET": {"loop invariant": 9, "loop assigns": 9, "loop variant": 9, "requires": 3, "ensures": 1}
  },
  "LabelsTriTyp": {
    "count_annotations/3_generations/LabelsTriTyp": {"behavior": 31, "assumes": 31, "ensures": 20, "assigns": 16, "requires": 3},
    "count_annotations_eva/backup_first_run/LabelsTriTyp": {"requires": 7, "ensures": 4, "assigns": 3},
    "count_annotations_pathcrawler/third_run_headers/LabelsTriTyp": {"ensures": 13, "behavior": 8, "assumes": 8, "requires": 3, "assigns": 1, "complete behaviors": 1, "disjoint behaviors": 1}
  },
  "Alias4": {
    "count_annotations/3_generations/Alias4": {"assigns": 9, "ensures": 8, "requires": 5},
    "count_annotations_eva/backup_first_run/Alias4": {"ensures": 6, "requires": 5, "assert": 5, "behavior": 2, "assigns": 2, "assumes": 2, "complete behaviors": 1, "disjoint behaviors": 1},
    "count_annotations_pathcrawler/third_run_headers/Alias4": {"assert": 6, "requires": 5, "ensures": 5, "assigns": 2}
  },
  "MultiDimArray": {
    "count_annotations/3_generations/MultiDimArray": {"requires": 23, "assigns": 17, "assert": 13, "ensures": 8},
    "count_annotations_eva/backup_first_run/MultiDimArray": {"requires": 19, "assert": 11, "ensures": 4, "assigns": 3},
    "count_annotations_pathcrawler/third_run_headers/MultiDimArray": {"assigns": 18, "requires": 17, "ensures": 1, "assert": 1}
  },
  "Alias2": {
    "count_annotations/3_generations/Alias2": {"requires": 7, "ensures": 5, "assert": 5, "loop invariant": 3, "loop assigns": 3, "loop variant": 2, "ghost": 2},
    "count_annotations_eva/backup_first_run/Alias2": {"requires": 7, "loop invariant": 3, "loop assigns": 3, "loop variant": 3, "assert": 3, "ensures": 2},
    "count_annotations_pathcrawler/third_run_headers/Alias2": {"requires": 7, "ensures": 7, "loop invariant": 3, "loop assigns": 3, "loop variant": 3, "assert": 2, "behavior": 2, "assumes": 2}
  },
  "PointeurFonction4": {
    "count_annotations/3_generations/PointeurFonction4": {"requires": 15, "ensures": 8, "behavior": 3, "assumes": 3, "complete behaviors": 1, "disjoint behaviors": 1, "assigns": 1, "assert": 1},
    "count_annotations_eva/backup_first_run/PointeurFonction4": {"requires": 6, "ensures": 4, "assigns": 1},
    "count_annotations_pathcrawler/third_run_headers/PointeurFonction4": {"requires": 12, "ensures": 10, "behavior": 2, "assumes": 2, "assigns": 1, "complete behaviors": 1, "disjoint behaviors": 1}
  },
  "ADPCM": {
    "count_annotations/3_generations/ADPCM": {"ensures": 22, "behavior": 15, "assumes": 15, "requires": 12, "assigns": 6, "complete behaviors": 4, "disjoint behaviors": 4, "loop invariant": 3, "loop assigns": 3, "loop variant": 3},
    "count_annotations_eva/backup_first_run/ADPCM": {"requires": 10, "ensures": 6, "loop invariant": 4, "loop assigns": 3, "loop variant": 3, "assert": 2, "assigns": 2},
    "count_annotations_pathcrawler/third_run_headers/ADPCM": {"requires": 12, "ensures": 8, "assert": 5, "loop invariant": 3, "loop assigns": 3, "loop variant": 3, "assigns": 2}
  },
  "Fibonacci": {
    "count_annotations/3_generations/Fibonacci": {"ensures": 8, "assigns": 6, "requires": 4, "behavior": 4, "assumes": 4, "complete behaviors": 1, "disjoint behaviors": 1},
    "count_annotations_eva/backup_first_run/Fibonacci": {"assigns": 5, "ensures": 5, "requires": 3, "behavior": 2, "assumes": 2},
    "count_annotations_pathcrawler/third_run_headers/Fibonacci": {"ensures": 6, "requires": 3, "behavior": 2, "assumes": 2, "assigns": 1}
  },
  "TestShiftRt": {
    "count_annotations/3_generations/TestShiftRt": {"assert": 10, "requires": 3, "ensures": 3, "assigns": 2},
    "count_annotations_eva/backup_first_run/TestShiftRt": {"requires": 8, "assert": 6, "ensures": 3},
    "count_annotations_pathcrawler/third_run_headers/TestShiftRt": {"assert": 10, "ensures": 4, "requires": 3, "assigns": 1}
  },
  "LuhnBranches": {
    "count_annotations/3_generations/LuhnBranches": {"requires": 17, "loop invariant": 7, "assigns": 6, "ensures": 6, "loop assigns": 6, "loop variant": 6},
    "count_annotations_eva/backup_first_run/LuhnBranches": {"requires": 11, "ensures": 6, "assigns": 5, "loop invariant": 4, "loop assigns": 4, "loop variant": 4},
    "count_annotations_pathcrawler/third_run_headers/LuhnBranches": {"requires": 12, "assert": 9, "ensures": 8, "assigns": 6, "loop invariant": 4, "loop assigns": 4, "loop variant": 4, "behavior": 2}
  },
  "Dates": {
    "count_annotations/3_generations/Dates": {"requires": 24, "assigns": 14, "loop invariant": 8, "loop assigns": 8, "ensures": 8, "loop variant": 4, "predicate": 2},
    "count_annotations_eva/backup_first_run/Dates": {"requires": 18, "ensures": 17, "loop invariant": 8, "loop assigns": 8, "assigns": 7, "loop variant": 6},
    "count_annotations_pathcrawler/third_run_headers/Dates": {"requires": 18, "ensures": 5, "loop invariant": 4, "behavior": 4, "assumes": 4, "loop variant": 3, "loop assigns": 2, "assert": 1, "complete behaviors": 1, "disjoint behaviors": 1}
  },
  "FibonacciRecurLimit": {
    "count_annotations/3_generations/FibonacciRecurLimit": {"requires": 7, "ensures": 7, "assigns": 3, "behavior": 2, "assumes": 2},
    "count_annotations_eva/backup_first_run/FibonacciRecurLimit": {"ensures": 8, "behavior": 6, "assumes": 6, "assigns": 5, "requires": 3},
    "count_annotations_pathcrawler/third_run_headers/FibonacciRecurLimit": {"requires": 3, "ensures": 3, "assert": 1}
  },
  "TcasBranches": {
    "count_annotations/3_generations/TcasBranches": {"requires": 27, "ensures": 6, "behavior": 3, "assumes": 3, "loop invariant": 1, "loop assigns": 1, "loop variant": 1, "complete behaviors": 1, "disjoint behaviors": 1},
    "count_annotations_eva/backup_first_run/TcasBranches": {"ensures": 25, "requires": 11},
    "count_annotations_pathcrawler/third_run_headers/TcasBranches": {"requires": 26, "ensures": 6, "assigns": 1}
  },
  "Apache": {
    "count_annotations/3_generations/Apache": {"requires": 16, "ensures": 13, "loop invariant": 11, "loop assigns": 11, "loop variant": 11, "assigns": 9, "behavior": 7, "assumes": 7},
    "count_annotations_eva/backup_first_run/Apache": {"requires": 12, "loop invariant": 9, "loop assigns": 9, "loop variant": 6, "assert": 6, "ensures": 4, "assigns": 3},
    "count_annotations_pathcrawler/third_run_headers/Apache": {"requires": 17, "loop invariant": 8, "assigns": 6, "loop assigns": 6, "ensures": 4, "loop variant": 4}
  },
  "TestLabels": {
    "count_annotations/3_generations/TestLabels": {"ensures": 12, "behavior": 6, "assumes": 6, "requires": 6, "complete behaviors": 2, "disjoint behaviors": 2},
    "count_annotations_eva/backup_first_run/TestLabels": {"ensures": 6, "requires": 5, "assigns": 2},
    "count_annotations_pathcrawler/third_run_headers/TestLabels": {"ensures": 8, "requires": 6, "behavior": 4, "assumes": 4, "assert": 3, "complete behaviors": 1, "disjoint behaviors": 1}
  }
}

# Assuming all programs have the same set of directories to compare
directories = ["output/count_annotations/3_generations", "output/count_annotations_pathcrawler/third_run_headers", "count_annotations_eva/backup_first_run"]
programs = list(data.keys())

# Preparing data for plotting
ensures_counts = {dir_: [] for dir_ in directories}
for program in programs:
    for dir_ in directories:
        ensures_counts[dir_].append(data[program].get(dir_, {}).get("ensures", 0))  # Default to 0 if not found

# Plotting
x = np.arange(len(programs))  # the label locations
width = 0.2  # the width of the bars

fig, ax = plt.subplots()
for i, dir_ in enumerate(directories):
    ax.bar(x + i*width, ensures_counts[dir_], width, label=dir_)

ax.set_xlabel('Program')
ax.set_ylabel('Counts of "ensures"')
ax.set_title('Counts of "ensures" by Program and Directory')
ax.set_xticks(x + width / len(directories))
ax.set_xticklabels(programs, rotation=45, ha="right")
ax.legend()

plt.tight_layout()
plt.show()

