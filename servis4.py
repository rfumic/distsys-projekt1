import aiohttp
from aiohttp import web

routes = web.RouteTableDef()


@routes.get("/gatherData")
async def gather_data(request):
    try:
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
web.run_app(app, port=8084)