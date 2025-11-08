# Name: Yaksh Kundu
# Date: 7 November, 2025
# Project Title: GradeBook Analyzer

import csv
from statistics import median
from datetime import datetime

def avg(d):
    return sum(d.values())/len(d) if d else 0.0

def med(d):
    xs=list(d.values())
    return median(xs) if xs else 0.0

def mx(d):
    if not d: return ("",0.0)
    k=max(d,key=d.get)
    return (k,d[k])

def mn(d):
    if not d: return ("",0.0)
    k=min(d,key=d.get)
    return (k,d[k])

def g_for(x):
    x=float(x)
    if x>=90: return "A"
    elif x>=80: return "B"
    elif x>=70: return "C"
    elif x>=60: return "D"
    else: return "F"

def grade_map(d):
    return {k:g_for(v) for k,v in d.items()}

def dist(gd):
    c={"A":0,"B":0,"C":0,"D":0,"F":0}
    for v in gd.values():
        if v in c: c[v]+=1
    return c

def get_pass_fail(d):
    p=[k for k,v in d.items() if float(v)>=40]
    f=[k for k,v in d.items() if float(v)<40]
    return p,f

def show_table(d,gd):
    print("\nName\tMarks\tGrade")
    print("---------------------------------")
    for k in d:
        print(f"{k}\t{d[k]}\t{gd[k]}")
    a=avg(d)
    m=med(d)
    mxn=mx(d)
    mnn=mn(d)
    print("\nSummary")
    print("---------------------------------")
    print(f"Average:\t{a:.2f}")
    print(f"Median:\t{m:.2f}")
    print(f"Max:\t{mxn[0]} ({mxn[1]})")
    print(f"Min:\t{mnn[0]} ({mnn[1]})")

def save_csv(d,gd,path):
    with open(path,"w",newline="") as f:
        w=csv.writer(f)
        w.writerow(["Name","Marks","Grade","Timestamp"])
        ts=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for k in d:
            w.writerow([k,d[k],gd[k],ts])

def read_csv(path):
    d={}
    with open(path,"r",newline="") as f:
        r=csv.reader(f)
        rows=list(r)
    i=0
    if rows and len(rows[0])>=2 and rows[0][0].lower().startswith("name"):
        i=1
    for row in rows[i:]:
        if not row: continue
        if len(row)<2: continue
        nm=row[0].strip()
        try:
            sc=float(row[1])
        except:
            continue
        if nm:
            d[nm]=sc
    return d

def read_manual():
    d={}
    while True:
        try:
            n=int(input("How many students? "))
            if n<=0: print("Enter a positive number."); continue
            break
        except:
            print("Enter a valid integer.")
    for i in range(1,n+1):
        nm=input(f"Name {i}: ").strip()
        while not nm:
            nm=input("Name cannot be empty. Re-enter: ").strip()
        while True:
            s=input(f"Marks for {nm}: ").strip()
            try:
                d[nm]=float(s)
                break
            except:
                print("Enter a valid number.")
    return d

def run_once(d):
    if not d:
        print("No data found.")
        return
    gd=grade_map(d)
    c=dist(gd)
    show_table(d,gd)
    print("\nGrade Distribution")
    print("---------------------------------")
    for k in ["A","B","C","D","F"]:
        print(f"{k}:\t{c[k]}")
    p,f=get_pass_fail(d)
    print("\nPass/Fail")
    print("---------------------------------")
    print(f"Passed ({len(p)}): {', '.join(p) if p else '-'}")
    print(f"Failed ({len(f)}): {', '.join(f) if f else '-'}")
    while True:
        z=input("\nSave table to CSV? (y/n): ").strip().lower()
        if z in ("y","n"): break
    if z=="y":
        fn=input("Filename (e.g., results.csv): ").strip() or "results.csv"
        save_csv(d,gd,fn)
        print(f"Saved to {fn}")

def main():
    print("GradeBook Analyzer")
    print("------------------")
    while True:
        print("\n1) Manual input")
        print("2) Load from CSV")
        print("3) Exit")
        ch=input("Choose: ").strip()
        if ch=="1":
            d=read_manual()
            run_once(d)
        elif ch=="2":
            p=input("CSV path: ").strip()
            try:
                d=read_csv(p)
                run_once(d)
            except FileNotFoundError:
                print("File not found.")
            except:
                print("Could not read file.")
        elif ch=="3":
            break
        else:
            print("Invalid choice.")
        x=input("\nRun again? (y/n): ").strip().lower()
        if x!="y": break
    print("Bye")

if __name__=="__main__":
    main()
      
