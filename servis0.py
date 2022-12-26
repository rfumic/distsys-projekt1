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
    )
    return record


async def loadDb():
    async with aiofiles.open("podaci.json", mode="r") as f:
        i = 0
        async for line in f:
            print(f"file {i}")

            async with aiosqlite.connect(DATABASE) as db:
                await db.execute(
                    "INSERT INTO Zadace (username,ghlink,filename) VALUES (?,?,?)",
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
    #    req = await request.json()
    try:
        return web.json_response({"status": "ok"}, status=200)
    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)})


asyncio.run(startDb())

app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8080)
