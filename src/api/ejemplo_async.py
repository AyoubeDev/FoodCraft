import asyncio
import time

encendido = True
async def bucle():
    asyncio.create_task(desactivador())
    contador = 0
    while encendido:
        print(contador+1)
        contador+=1
        await asyncio.sleep(1)
    print(f"se termino favorablemente la ejecucion con el contador a {contador}")
async def desactivador():
    global encendido
    await asyncio.sleep(8)
    encendido = False
    

    
asyncio.run(bucle())