import json
import aiohttp
import asyncio
import aiosqlite
import aiofiles
from aiohttp import web

routes = web.RouteTableDef()
global DATABASE
DATABASE = "db/distsys-projekt1.db"


def cleanData(obj):
    record = (
        obj["repo_name"].split("/")[0],
        "https://github.com/" + obj["repo_name"],
        obj["path"].split("/")[-1],
        obj['content']
    )
    return record


async def loadDb():
    async with aiofiles.open("podaci.json", mode="r") as f:
        i = 0
        async for line in f:
            print(f"file {i}",end='\r')

            async with aiosqlite.connect(DATABASE) as db:
                await db.execute(
                    "INSERT INTO Zadace (username,ghlink,filename,content) VALUES (?,?,?,?)",
                    cleanData(json.loads(line)),
                )
                await db.commit()
            i += 1
            if i == 10000:
                return


async def startDb():
    async with aiosqlite.connect(DATABASE) as db:
        cur = await db.cursor()
        await cur.execute("SELECT COUNT(*) FROM Zadace")
        count = await cur.fetchall()

        if count[0][0] == 0:
            await loadDb()


@routes.get("/m0")
async def m0(request):
    try:
        offset = request.query['offset'] 
        response = {
            "service_id": 0,
            "data": {"usernames": [], "githubLinks": [], "filenames": [],
            'content':[]},
        }
        async with aiosqlite.connect(DATABASE) as db:
            async with db.execute(f"SELECT * FROM Zadace LIMIT 100 OFFSET {offset}") as cur:
                async for row in cur:
                    response["data"]["usernames"].append(row[1])
                    response["data"]["githubLinks"].append(row[2])
                    response["data"]["filenames"].append(row[3])
                    response['data']['content'].append(row[4])
                await db.commit()
        
        return web.json_response(response, status=200)
    except Exception as e:
        return web.json_response({"status": "failed", "message":
        str(e)},status=500)


asyncio.run(startDb())

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8080)
