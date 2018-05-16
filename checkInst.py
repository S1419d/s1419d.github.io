import random
import asyncio
from aiohttp import ClientSession

usersList = [] 

def addToList():
 usersFile = open("newList.txt","r")
 for user in usersFile:
  usersList.append(user.strip())

addToList()

async def fetch(url, session):
    async with session.get(url) as response:
     if response.status == 404:
      user = url.split("/")[3]
      print(user)
     return await response.read()


async def bound_fetch(sem, url, session):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session)


async def run(r):
    url = "https://instagram.com/{}"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(1000)

    # Create client session that will ensure we dont open new connection per each request.
    async with ClientSession() as session:
        for i in r:
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(sem, url.format(i), session))
            tasks.append(task)

        responses = asyncio.gather(*tasks)
        await responses

while True:
 try:
  loop = asyncio.get_event_loop()
  future = asyncio.ensure_future(run(usersList))
  loop.run_until_complete(future)
  break
 except:
  continue

