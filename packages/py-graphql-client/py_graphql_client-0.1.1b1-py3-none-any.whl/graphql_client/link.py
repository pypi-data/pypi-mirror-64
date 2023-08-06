# -*- coding: utf-8 -*-
"""
Module for links
"""

import asyncio
#  import time

async def waiter():
    await asyncio.gather(
        cook('Pasta', 4),
        cook('Ceasar Salad', 3),
        cook('Lamb Chops', 6)
    )

async def cook(order: str, prep_time: int) -> None:
    print(f'Got order: {order}')
    await asyncio.sleep(prep_time)
    print(order, 'ready')


if __name__ == '__main__':
    asyncio.run(waiter())
