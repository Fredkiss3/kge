import asyncio

loop = None


async def find_divisibles(inrange, div_by):
    print("finding nums in range {} divisible by {}".format(inrange, div_by))
    located = []
    for i in range(inrange):
        if i % div_by == 0:
            located.append(i)

        if i % 500000 == 0:
            await asyncio.sleep(0.0001)
    print("Done w/ nums in range {} divisible by {}".format(inrange, div_by))
    return located


async def main():
    global loop
    divs1 = loop.create_task(find_divisibles(508000, 34113))
    divs2 = loop.create_task(find_divisibles(100052, 3210))
    divs3 = loop.create_task(find_divisibles(500, 3))
    await asyncio.wait([divs1, divs2, divs3])


def find_divisibles2(inrange, div_by):
    print("finding nums in range {} divisible by {}".format(inrange, div_by))
    located = []
    for i in range(inrange):
        if i % div_by == 0:
            located.append(i)
    print("Done w/ nums in range {} divisible by {}".format(inrange, div_by))
    return located


def main2():
    divs1 = find_divisibles2(508000, 34113)
    divs2 = find_divisibles2(100052, 3210)
    divs3 = find_divisibles2(500, 3)


def run1():
    global loop
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()


def run2():
    main2()
