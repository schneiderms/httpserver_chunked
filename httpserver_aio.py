from aiohttp import web
import asyncio
import aiofiles

chunk_size = 512

async def get_chunk_data(): 
    async with aiofiles.open('./get_orders_response.xml', 'rb') as f: 
        while chunk := await f.read(chunk_size): 
            chunk_length = f"{len(chunk):x}\r\n"
            chunk_length = chunk_length.encode('utf8')
            yield chunk_length
            yield chunk
            yield b'\r\n'
            await asyncio.sleep(0.1)

async def get_chunk_data2(): 
    async with aiofiles.open('./get_orders_response.xml', 'rb') as f: 
        while chunk := await f.read(chunk_size): 
            yield chunk
            await asyncio.sleep(0.1)

async def getData(): 
    async with aiofiles.open('./get_orders_response.xml', 'rb') as f: 
        chunk = await f.read()
        return chunk

        

async def handle_get(request):
    print(request)
    # Erstelle eine Chunked-Response
    response = web.StreamResponse(status=200, reason='OK', headers={
        'Content-Type': 'text/xml',
        'Transfer-Encoding': 'chunked'
    })

    response.enable_chunked_encoding()
    await response.prepare(request)
    

    # await send_data(response)
    
    # chunk = await getData()
    # await response.write(chunk)

    # Daten in Chunks senden


    async for chunk in get_chunk_data():
        await response.write(chunk)
        


    # # Response abschließen
    await response.write(b'0\r\n\r\n')
    await response.write_eof()
    return response


app = web.Application()
app.add_routes([web.get('/getOrdersResponse', handle_get)])

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=3030)