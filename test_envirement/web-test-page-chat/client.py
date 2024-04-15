import asyncio
import websockets

async def receive_messages(ws):
    async for message in ws:
        print(f"Received message: {message}")
        return

async def send_messages(ws):
    while True:
        user_input = input("Enter message to send (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            await ws.close()
            break
        await ws.send(user_input)
        await receive_messages(ws)

async def main():
    async with websockets.connect('ws://localhost:8080/') as ws:
        print("Connection opened")
        send_task = asyncio.create_task(send_messages(ws))

        # Wait for both tasks to complete
        await asyncio.gather(send_task)

if __name__ == "__main__":
    asyncio.run(main())
