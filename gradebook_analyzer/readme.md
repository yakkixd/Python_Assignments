# GradeBook Analyzer

This is my mini project for the course **Programming for Problem Solving using Python**.  
The goal of the project is to read student marks, analyse them, assign grades, and print useful summaries through a simple CLI program.

## How it works
The program lets the user choose between:
1. Manual input of student names and marks
2. Loading the data from a CSV file

All marks are stored in a dictionary.  
The script computes:
- Average marks
- Median marks
- Highest scorer
- Lowest scorer

It also assigns grades using:
A (90+), B (80–89), C (70–79), D (60–69), F (<60)

The program shows:
- A formatted results table
- Grade distribution (A–F)
- Pass/Fail student lists using list comprehension
- Option to save the final results table to a CSV file
- Option to run multiple analyses (loop)

## Folder Structure
gradebook_analyzer/
│
├── gradebook.py
├── sample_students.csv
└── README.md


## Requirements
- Python 3.x
- No external libraries needed (only csv, statistics, datetime)
