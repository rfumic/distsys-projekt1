import aiohttp
from aiohttp import web

routes = web.RouteTableDef()


def extract_data(dic):
    result = []
    for i, v in enumerate(dic["usernames"]):
        if v[0].lower() == "w":
            result.append(
                {
                    "username": v,
                    "githubLink": dic["githubLinks"][i],
                    "filename": dic["filenames"][i],
                    "content": dic["content"][i],
                }
            )

    return result


@routes.post("/wt")
async def wt(request):
    try:
        req = await request.json()
        async with aiohttp.ClientSession() as s:
            r = await s.post(
                "http://0.0.0.0:8084/gatherData", json=extract_data(req["data"])
            )
        return web.json_response(
            {"service_id": 3, "response": r},
            status=200,
        )
    except Exception as e:
        return web.json_response({"status": "failed", "message": str(e)})


app = web.Application()
app.router.add_routes(routes)
web.run_app(app, port=8083)
