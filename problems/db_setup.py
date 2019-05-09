#%%
import sqlite3, json
from  pathlib import Path 

def setup_problem_db(db_name = "moon_problems.db", init_script_path = Path("setup_sqlite.sql")):
    conn = sqlite3.connect(db_name)
    with init_script_path.open("r+") as f:
        init_script=f.read()
    #
    with conn:
        for cmd in init_script.split('--'):
            print(cmd)
            conn.executescript(cmd)
    return conn


def setup_holds(conn, hold_setup=Path("HoldSetup.json")):
    cmd = "INSERT INTO holds VALUES (?,?,?,?,?)"
    c = conn.cursor()
    with hold_setup.open("r+") as f:
        holds = json.load(f)
    print("insert holds")
    for setup,v in holds.items():
        print(setup)
        for pos, detail in v.items():
            c.execute(cmd, (pos, setup, detail['HoldSet'],
                       detail["Hold"], detail["Orientation"]))
    conn.commit()
    print("insert holds OK")


def insert_problem(conn,Id, Name,Grade,moves,
                IsBenchmark,IsAssessmentProblem, Method,
                setup,firstname,lastname,**kwargs):
    cmd0 = "INSERT INTO setter VALUES (?,?)"
    cmd1 = "INSERT INTO problems VALUES (?,?,?,?,?,?,?,?)"
    cmd2 = "INSERT INTO problemMoves VALUES (?,?,?,?,?)"

    c = conn.cursor()
    try:
        c.execute(cmd0,(firstname,lastname))
    except:
        conn.rollback()
    else:
        print(f"New Setter {firstname} {lastname}.")

    try:
        c.execute(cmd1,(Id, Name.strip(),Grade.strip(), IsBenchmark, 
        IsAssessmentProblem, Method, firstname.strip(),lastname.strip()))
    except Exception as e :
        conn.rollback()
        raise e
    else:
        try:
            for (position,start,stop) in moves:
                c.execute(cmd2,[Id, position, setup, start, stop])
        except Exception as e :
            conn.rollback()
            raise e  
        else:
            print(f"New problem {Id}.")
            conn.commit()

if __name__=="__main__":
    conn = setup_problem_db()
    setup_holds(conn)
    problem_path = Path("moonboard_problems_setup_2016.json")
    with problem_path.open("r+") as f:
        problems=json.load(f)

    errors=[]
    for Id, problem in problems.items():
        try:
            setup=problem["Holdsetup"]["Description"][-4:]
            moves = [[m['Description'],m["IsStart"], m["IsEnd"]] for m in problem['Moves']]
            insert_problem(conn, moves=moves,setup=setup,Id=Id, 
                            firstname= problem['Setter']['Firstname'], 
                            lastname= problem['Setter']['Lastname'], 
                            **problem
            )
        except:
            errors.append(Id)
    
    print(errors)
