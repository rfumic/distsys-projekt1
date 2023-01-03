import aiohttp
import asyncio
from aiohttp import web

routes = web.RouteTableDef()


async def fetch_from_m0(session, offset):
    r = await session.get(f"http://0.0.0.0:8080/m0?offset={offset}")
    return await r.json()


@routes.get("/m1")
async def m1(request):
    try:
        tasks = []
        async with aiohttp.ClientSession() as s:
            for response in asyncio.as_completed(
                [fetch_from_m0(s, i) for i in range(0, 10000, 100)]
            ):
                zadace = await response

                tasks.append(
                    asyncio.create_task(s.post("http://0.0.0.0:8082/wt", json=zadace))
                )
                tasks.append(
                    asyncio.create_task(s.post("http://0.0.0.0:8083/wt", json=zadace))
                )

            await asyncio.gather(*tasks)
        return web.json_response(
            {
                "status": "ok",
            },
            status=200,
        )
    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)})


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8081)
