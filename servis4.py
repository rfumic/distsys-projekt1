import aiohttp
import aiofiles
from aiohttp import web

routes = web.RouteTableDef()

global gathered_files
gathered_files = []


async def generate_files():
    for x in gathered_files:
        async with aiofiles.open(f"./output/{x['filename']}", mode="a") as f:
            print(f"Generating {x['filename']}...")
            await f.write(x["content"])


@routes.post("/gatherData")
async def gather_data(request):
    req = await request.json()

    gathered_files.extend(req)

    if len(gathered_files) > 10:
        await generate_files()

    return web.json_response(
        {
            "status": "ok",
        },
        status=200,
    )


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8084)
