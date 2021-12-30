# WS server example that synchronizes state across clients
import asyncio
import json
import websockets
from functools import partial
import problems.db_query as query
#from problems.draw_problem import draw_Problem, colormap
import aiosqlite
import problems
from led.drive_moonboard_LEDS import show_problem

CLIENTS = {}
CLIENT_N = 0
HISTORY = [None]*10
LIMIT = 2001

async def notify_all_clients(d):
    for ws in CLIENTS.values():
        await ws.send(json.dumps(d))


async def register(ws,conn, mounted_holds, logger,**kwargs):
    global HISTORY, CLIENT_N, CLIENTS
    CLIENT_N += 1
    client = CLIENT_N
    CLIENTS[CLIENT_N] = ws
    gradi=['6B+','6C','6C+','7A']
    search_param={
        'Grades': gradi, 'Name': '', 'Setter': '','Benchmarks':True, 
        'RmHolds':{k:[] for k in mounted_holds.keys()},
        'RequireHolds':{k:[] for k in mounted_holds.keys()}
        }
    p,_=await query.user_query_get_problems(conn=conn, limit=LIMIT, **search_param)

    logger.info(
        f'Add client n. {CLIENT_N}, number of clients is {len(CLIENTS)}')

    d = {"type": "INIT",
         "grades": problems.GRADES,
         "holds": mounted_holds,
         "history": HISTORY,
         "problems":  p[:LIMIT],
         "search_param": search_param,
         }
    await ws.send(json.dumps(d))
    return client

async def unregister(ws,client,logger,**kwargs):
    global CLIENTS
    CLIENTS.pop(client)
    logger.info(
        f'Remove client n. {client}, number of clients is {len(CLIENTS)}')

async def handle_search_submit_action(ws, msg, conn, logger,**kwargs):
    search_param=msg['search_parameter']
    logger.info(search_param)
    p, limit_reach=await query.user_query_get_problems(conn=conn, limit=LIMIT, **search_param)
    if limit_reach:
        p=p[:LIMIT]
    d = {"type": "SEARCH_RESULTS",
         "problems":p
         }
    await ws.send(json.dumps(d))


async def handle_illuminate_problem_action(ws, msg, conn, moonboard,  logger, **kwargs):
    global HISTORY
    problemId = msg['problem'][0]
    try:
        idx = HISTORY.index(problemId)
    except ValueError:
        HISTORY.pop(0)
    else:
        HISTORY.pop(idx)
    finally:
        HISTORY.append(problemId)
        holds = await query.get_problem_holds(conn,problemId)
        logger.debug(f"{holds}")
        d = {'type': 'HISTORY',
         'history':HISTORY,
        }
        await notify_all_clients(d)
        moonboard.show_problem(holds=holds)

async def usr_handler(ws, path, register, unregister, event_handlers):
    #register ws
    client_n = await register(ws)
    #main loop
    try:
        async for message in ws:
            msg = json.loads(message)
            try:
                handler = event_handlers[msg['type']]
            except KeyError:
                pass
                #event_handlers['default']
            else:
                await handler(ws, msg)
    ## exit
    finally:
        await unregister(ws, client_n)



async def main(logger, moonboard, setup, hold_sets,**kwargs):
    conn = await aiosqlite.connect(problems.DB_PATH)
    mounted_holds = {hold_set:(await query.get_setup_hold_positions(conn, setup, hold_set)) \
                        for hold_set in hold_sets}
    kwargs = {
            'conn':conn,
            'logger':logger, 
            'moonboard':moonboard,
            'setup':setup, 
            'mounted_holds':mounted_holds, 
            'hold_sets':hold_sets
        }

    handlers = {}
    handlers['SEARCH_SUBMIT'] = partial(handle_search_submit_action, **kwargs)
    handlers['ILLUMINATE_PROBLEM'] = partial(
                                        handle_illuminate_problem_action, 
                                        **kwargs
                                        )

    user_handler = partial(
                    usr_handler, 
                    register= partial(register, **kwargs), 
                    unregister= partial(unregister, **kwargs), 
                    event_handlers= handlers
                    )

    await websockets.serve(user_handler, '0.0.0.0', 6789)
