import asyncio
from site_monitor.monitor import SiteMonitorManager
from site_monitor.utils import MONITORING_DURATION
import nest_asyncio
import ipywidgets as widgets
from IPython.display import display

def main():
    sites = {
        'Sberbank': 'https://www.sberbank.ru/',
        'VTB': 'https://www.vtb.ru/',
        'Gazprombank': 'https://www.gazprombank.ru/',
        'Raiffeisen': 'https://www.raiffeisen.ru/',
        'Tinkoff': 'https://www.tinkoff.ru/'
    }

    manager = SiteMonitorManager(sites)
    stop_button = widgets.Button(description="Stop Monitoring")
    stop_button.on_click(lambda _: manager.stop())
    display(stop_button)

    nest_asyncio.apply()
    asyncio.run(manager.monitor_sites(MONITORING_DURATION))

if __name__ == "__main__":
    main()
