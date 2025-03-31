from app.resolver import Resolver, load_dns, load_urls, save_to_file


async def generate_table():
    resolver = Resolver(await load_dns(), await load_urls())
    ips = await resolver.resolve_all()
    result_file = save_to_file(ips)
    return result_file
