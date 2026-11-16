import asyncio
import time

# encendido = True
# async def bucle():
#     asyncio.create_task(desactivador())
#     contador = 0
#     while encendido:
#         print(contador+1)
#         contador+=1
#         await asyncio.sleep(1)
#     print(f"se termino favorablemente la ejecucion con el contador a {contador}")
# async def desactivador():
#     global encendido
#     await asyncio.sleep(8)
#     encendido = False
    

    
# asyncio.run(bucle())


async def bucle():
    asyncio.create_task(listo())
    preparado = False
    counter = 0
    while preparado == False:
        print(f"Preparando...")
        counter+=1
        await asyncio.sleep(1)
        if counter == 3:
            preparado = True

async def listo():
    counter = 0

    while counter!=2:
        print(f"¡Listo!")
        counter+=1
        await asyncio.sleep(2)

asyncio.run(bucle())