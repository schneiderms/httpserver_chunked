from aiohttp import web
import asyncio
import aiofiles

import argparse

# chunk_size = 8895

def main():
    parser = argparse.ArgumentParser(description="Example of an executable Python script with options")
    parser.add_argument("-c", "--chunksize", type=int, help="Size of a Chunk", required=True)

    args = parser.parse_args()

    print(f"ChunkSize: {args.chunksize}!")
    global chunk_size
    chunk_size = args.chunksize

    web.run_app(app, host='0.0.0.0', port=3030)
    




async def get_chunk_data(): 
    async with aiofiles.open('./get_orders_response_rn.xml', 'rb') as f: 
        while chunk := await f.read(512): 
            #chunk_length = f"{len(chunk):x}\r\n"
            #chunk_length = chunk_length.encode('utf8')
            chunk_length = f"{chunk_size}:\r\n".encode('utf8')
            yield chunk_length
            #chunk[chunk_size] += '\r\n'
            yield chunk
            yield b'\r\n'
            await asyncio.sleep(0.1)

async def get_chunk_data2(): 
    async with aiofiles.open('./get_orders_response.txt', 'rb') as f: 
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

    # response.enable_chunked_encoding()
    await response.prepare(request)
    

    # await send_data(response)
    
    # chunk = await getData()
    # await response.write(chunk)

    # Daten in Chunks senden


    async for chunk in get_chunk_data2():
        await response.write(chunk)
        


    # # Response abschließen
    #await response.write(b'0\r\n\r\n')
    await response.write_eof()
    return response


app = web.Application()
app.add_routes([web.post('/getOrdersResponse', handle_get)])

if __name__ == '__main__':
    main()