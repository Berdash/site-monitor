import aiohttp
import asyncio
import logging
from datetime import datetime, timedelta
from .utils import REQUEST_TIMEOUT, PAUSE_BETWEEN_CHECKS

class SiteMonitor:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.is_up = True
        self.downtime_seconds = 0
        self.last_downtime = None
        self.last_uptime = None

    async def check_availability(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, timeout=REQUEST_TIMEOUT, headers=headers) as response:
                    response.raise_for_status()
                    logging.info(f"{self.name} - {datetime.now()} - сайт доступен")
                    return True
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logging.error(f"{self.name} - {datetime.now()} - отказ сайта: {str(e)}")
            return False
        except Exception as e:
            logging.error(f"{self.name} - {datetime.now()} - отказ сайта: {str(e)}")
            return False

    def log_status_change(self, status):
        current_time = datetime.now()
        if status and not self.is_up:
            self.last_uptime = current_time
            logging.info(f"{self.name} - {current_time} - восстановление сайта")
            self.is_up = True
        elif not status and self.is_up:
            self.last_downtime = current_time
            logging.error(f"{self.name} - {current_time} - отказ сайта")
            self.is_up = False
        if not status:
            self.downtime_seconds += PAUSE_BETWEEN_CHECKS

class SiteMonitorManager:
    def __init__(self, sites):
        self.sites = [SiteMonitor(name, url) for name, url in sites.items()]
        self.is_running = True
        self.start_time = time.time()
    async def monitor_sites(self, duration):
        self.start_time = time.time()
        end_time = self.start_time + duration
        while time.time() < end_time and self.is_running:
            tasks = [self.check_site(site) for site in self.sites]
            await asyncio.gather(*tasks)
            for _ in range(PAUSE_BETWEEN_CHECKS):
                if not self.is_running:
                    print("Monitoring stopped by user.")
                    self.generate_report(time.time() - self.start_time)
                    return
                await asyncio.sleep(1)
        self.generate_report(duration)

    async def check_site(self, site):
        current_status = await site.check_availability()
        site.log_status_change(current_status)

    def generate_report(self, duration):
        report = []
        for site in self.sites:
            uptime = ((duration - site.downtime_seconds) / duration) * 100
            downtime = timedelta(seconds=site.downtime_seconds)
            report.append({
                'Наименование организации': site.name,
                'Uptime, %': f"{uptime:.2f}",
                'Общее время недоступности сайта за период': str(downtime)
            })
        self.print_report(report)
        self.save_report(report)
        print(f"Отчет сгенерирован и сохранен в файл site_availability_report.txt")

    def print_report(self, report):
        header = ['Наименование организации', 'Uptime, %', 'Общее время недоступности сайта за период']
        print(f"{header[0]:<25} {header[1]:<10} {header[2]:<30}")
        print('-' * 70)
        for row in report:
            print(f"{row['Наименование организации']:<25} {row['Uptime, %']:<10} {row['Общее время недоступности сайта за период']:<30}")

    def save_report(self, report):
        with open('site_availability_report.txt', 'w', encoding='utf-8') as file:
            header = ['Наименование организации', 'Uptime, %', 'Общее время недоступности сайта за период']
            file.write(f"{header[0]:<25} {header[1]:<10} {header[2]:<30}\n")
            file.write('-' * 70 + '\n')
            for row in report:
                file.write(f"{row['Наименование организации']:<25} {row['Uptime, %']:<10} {row['Общее время недоступности сайта за период']:<30}\n")

    def stop(self):
        self.is_running = False
        self.generate_report(time.time() - self.start_time)
        print("Мониторинг остановлен пользователем.")
