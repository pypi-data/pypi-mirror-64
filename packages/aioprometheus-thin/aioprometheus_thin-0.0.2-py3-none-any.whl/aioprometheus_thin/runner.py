import asyncio
from typing import Callable
from aioprometheus import Service


async def server(svc: Service, metrics_list: list, addr: str, port: int, collector: Callable) -> None:
    """
    This function runs the metrics updater task, that runs forever.
    :param svc:
    :param metrics_list:
    :param addr:
    :param port:
    :param collector:
    :return:
    """
    [svc.register(my_metric.metric) for my_metric in metrics_list]
    await svc.start(addr=addr, port=port)
    print(f"Serving prometheus metrics on: {svc.metrics_url}")
    await collector(metrics_list)


def run_async(metrics_list: list, addr: str, port: int, collector: Callable) -> None:
    """
    This function starts the async loop with the aio-prometheus server.
    :param metrics_list:
    :param addr:
    :param port:
    :param collector:
    :return: None
    """
    loop = asyncio.get_event_loop()
    svr = Service()
    try:
        loop.run_until_complete(server(svr, metrics_list, addr, port, collector))
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(svr.stop())
    loop.close()
