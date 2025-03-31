# Adapted from project DomainMapper (https://github.com/Ground-Zerro/DomainMapper),
# licensed under MIT
# Original author: Ground-Zerro


import asyncio
import datetime
import os
from asyncio import Semaphore
from collections import defaultdict
from pathlib import Path

import dns.asyncresolver


async def load_dns():
    try:
        with open("misc/dns_addresses", "r") as file:
            dns_servers = {}
            for line in file:
                if line.strip():
                    service, servers = line.split(": ", 1)
                    dns_servers[service.strip()] = servers.strip().split()
            return dns_servers
    except Exception as e:
        print(f"Failed to load DNS servers: {e}")
        return {}


async def load_urls():
    urls = dict()
    urls_folder = "misc/"
    try:
        for file in os.listdir(urls_folder):
            if not file.endswith(".urls"):
                continue

            with open(f"{urls_folder}{file}", "r") as f:
                service_name = Path(file).stem
                urls[service_name] = []
                for line in f:
                    if line.strip():
                        urls[service_name].append(line.strip())
    except Exception as e:
        print(f"Failed to load URLs: {e}")

    return urls


def group_ips_in_subnets(ips):
    subnets = set()

    octet_groups = {}
    for ip in list(ips):
        key = ".".join(ip.split(".")[:3])  # Группировка по первым трем октетам
        if key not in octet_groups:
            octet_groups[key] = []
        octet_groups[key].append(ip)

        # IP-адреса с совпадающими первыми тремя октетами
        network_24 = {
            key + ".0" for key, group in octet_groups.items() if len(group) > 1
        }  # Базовый IP для /24 подсетей
        # Удаляем IP с совпадающими первыми тремя октетами из множества
        ips -= {ip for group in octet_groups.values() if len(group) > 1 for ip in group}
        # Оставляем только IP без указания маски для /24 и одиночных IP
        subnets.update(ips)  # IP без маски для одиночных IP
        subnets.update(network_24)  # Базовые IP для /24 подсетей

    return subnets


# Ограничение числа запросов
def get_semaphore(request_limit):
    return defaultdict(lambda: Semaphore(request_limit))


# Инициализация semaphore для ограничения запросов
def init_semaphores(request_limit):
    return get_semaphore(request_limit)


async def resolve_domain(domain, resolver, semaphore):
    async with semaphore:
        filtered_ips = []

        try:
            response = await resolver.resolve(domain)
            ips = [ip.address for ip in response]
            for ip_address in ips:
                if (
                    ip_address not in ("127.0.0.1", "0.0.0.0")
                    and ip_address not in resolver.nameservers
                ):
                    filtered_ips.append(ip_address)
        except Exception as e:
            print(f"Failed to resolve {domain}: {e}")

        return filtered_ips


async def resolve_dns(dns_names, dns_servers, semaphore):
    tasks = []

    for server_name in dns_servers.keys():
        resolver = dns.asyncresolver.Resolver()
        resolver.nameservers = dns_servers[server_name]

        for domain in dns_names:
            tasks.append(resolve_domain(domain, resolver, semaphore[server_name]))

    results = await asyncio.gather(*tasks)
    ips = set()

    for result in results:
        for ip_address in result:
            ips.add(ip_address)

    return ips


def save_to_file(ips) -> str | None:
    def write_file(name, addresses, format_lambda):
        formatted_ips = [format_lambda(ip.strip()) for ip in addresses]
        with open(name, "w", encoding="utf-8") as file:
            file.write("\n".join(formatted_ips))

    if not ips:
        return None

    gateway = "0.0.0.0"

    def subnet_formatter(ip):
        return (
            f"{ip.strip()} mask 255.255.255.0"
            if ip.endswith(".0")
            else f"{ip.strip()} mask 255.255.255.255"
        )

    def formatter(ip):
        return f"route add {subnet_formatter(ip)} {gateway}"

    filename = f"routing_{datetime.date.today()}.txt"

    write_file(filename, ips, formatter)

    return filename


class Resolver:

    def __init__(self, dns_servers, urls):
        self.__dns_servers = dns_servers
        self.__urls = urls

    async def resolve_all(self) -> set[str]:
        semaphore = init_semaphores(20)

        tasks = []
        for service in self.__urls:
            tasks.append(
                resolve_dns(self.__urls[service], self.__dns_servers, semaphore)
            )
        results = await asyncio.gather(*tasks)

        all_ips = set()
        for result in results:
            for ip in result:
                all_ips.add(ip)

        grouped_ips = group_ips_in_subnets(all_ips)

        return grouped_ips
