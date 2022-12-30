import aiohttp
from aiohttp import web

routes = web.RouteTableDef()


def extractData(dic):
    result = {"usernames": [], "githubLinks": [], "filenames": [], "content": []}
    for i, v in enumerate(dic["usernames"]):
        if v[0].lower() == "w":
            print(v)
            result["usernames"].append(v)
            result["githubLinks"].append(dic["githubLinks"][i])
            result["filenames"].append(dic["filenames"][i])
            result["content"].append(dic["content"][i])

    return result


@routes.post("/wt")
async def wt(request):
    try:
        req = await request.json()
        (extractData(req["data"]))
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
web.run_app(app, port=8083)
