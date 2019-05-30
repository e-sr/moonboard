
import aiosqlite
import json
from pathlib import Path
from . import DB_PATH


async def create_problemMoves_setup_table(setup, db_path):
    async with aiosqlite.connect(db_path) as db:
        t = f"problemMoves_{setup}"
        try:
            await db.execute(f"DROP TABLE {t}")
        except aiosqlite.OperationalError as e:
            pass
        cmd = f"""
                create table {t} 
                    as 
                        select t.Problem,t.Position,holds.HoldSet,t.IsStart,t.IsEnd
                        from
                            (select * from problemMoves where Setup={setup}) as t
                            inner join holds on holds.Position=t.Position
                """
        await db.execute(cmd)

    return t

async def get_problem_holds(conn, Id):
    d = {'START': [], "TOP": [], "MOVES": []}
    async with conn.execute("SELECT * FROM problemMoves WHERE Problem=:Id", {'Id': Id}) as cursor:
        async for (_, h, _, start, top) in cursor :
            if start:
                d["START"].append(h)
            elif top:
                d["TOP"].append(h)
            else:
                d["MOVES"].append(h)
    return d


async def get_setup_hold_positions(conn, setup, holdSet):
    cmd = f"select Position from holds where (Setup=:setup and HoldSet=:holdSet)"
    holdlist=[]
    async with conn.execute(cmd,{'setup':setup,"holdSet":holdSet}) as cursor :
        async for r in  cursor:
            holdlist.extend(r)
    return sorted(holdlist)


async def get_problems_list_from_ids(conn, Ids):
    IdsStr = ', '.join('{!r}'.format(s) for s in Ids)
    async with conn.execute(f"SELECT * FROM problems WHERE Id IN ({IdsStr})") as cursor:
        return await cursor.fetchall()


async def user_query_get_problems(conn, Grades, Name, Setter, holdSetMounted={'A', 'B', 'OS'}, Benchmark=False, limit=2001,**kwargs):
    #hold set to remove
    GradeStr = ', '.join('{!r}'.format(s) for s in Grades)
    cmd = f"""
    SELECT Id, Name, Grade, (Firstname|| " " || Lastname) AS Setter, IsBenchmark  
    FROM problems 
    WHERE 
        Grade IN ({GradeStr})
        and
        Name LIKE "%{Name}%"
        and 
        Setter LIKE "%{Setter}%"
        --{"and IsBenchmark IS true" if Benchmark else ""}   
    LIMIT {limit}
    """
    async with conn.execute(cmd) as cursor:
        results = [p async for p in cursor]
        return results, (len(results) != limit)

"""
intersect = "\n".join(
f"INTERSECT SELECT DISTINCT Problem FROM problemMoves_2016 WHERE Position='{p}'" for p in wantedHold)
{intersect}
EXCEPT
SELECT DISTINCT Problem FROM problemMoves_2016 WHERE HoldSet IN({holdSetRmStr})

"""
