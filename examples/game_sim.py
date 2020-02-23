import os
import asyncio
import random


class Enemy(object):
    nbItems = 0

    def __init__(self):
        self.health = 100
        Enemy.nbItems += 1
        self.name = f"Enemy {Enemy.nbItems}"

    def take_damage(self):
        if self.health <= 0:
            return
        amount = random.randint(0, 100)
        self.health -= amount

        if amount > 0:
            print(
                f"{self.name} took a Damage ! (amount={amount}) (health left : {self.health})")
        else:
            print(
                f"{self.name} Had been lucky and didn't took any Damage ! (health left : {self.health})")

        if self.health <= 0:
            print(f"{self.name} Died !")
            # self.health = 0


# loop
loop = None

# Prepare enemies
enemies = [Enemy() for i in range(50)]


async def update(callback: callable, *args):
    """
    Asynchronous Update of entities
    """
    await asyncio.sleep(0.0001)
    callback(*args)

    # if enemy.health < 0:
    #     raise ValueError(f"{enemy.name} Health should not be less than Zero !")

# func = async lambda v: print("Value")


async def main(stop: bool = True):
    global loop, enemies

    results = []

    def callback(fut):
        # Handle an exception occuring in the code
        try:
            future.result()
        except Exception as e:
            print(f"An Exception Happened : {e} ({type(e)})")
            print(f"Continuing the game...")

    for e in enemies:
        future = loop.create_task(update(e.take_damage))
        if not stop:
            future.add_done_callback(callback)
        results.append(future)
    await asyncio.gather(*results)
    # print(results)
    # return results


def run(stop: bool = True):
    global loop
    asyncio.set_event_loop(asyncio.new_event_loop())
    try:
        loop = asyncio.get_event_loop()
        loop.set_debug(1)
        loop.run_until_complete(main(stop))
        loop.close()
    except Exception as e:
        # Handles a global exception
        print(f"An Error Happenned : {e}")
        pass
    finally:
        loop.close()


def fixed_update(enemy: Enemy):
    """
    Synchronous Update of entities
    """
    enemy.take_damage()


def fixed_main():
    global enemies
    # Handle Fixed Updates for enemies
    for e in enemies:
        fixed_update(e)


def cls(): return os.system("cls")
