
import typing
import re
import trio


async def _singlePingR(host:str, timeout:int):
	cp = await trio.run_process(["ping", host, "-c", "1", "-W", str(timeout)], capture_stdout=True, capture_stderr=True, check=False)
	if cp.returncode == 0:
		lines = cp.stdout.decode("utf-8").split("\n")
		assert lines[0].startswith("PING ")
		# OUTPUT:
		#	64 bytes from 192.168.10.200: icmp_seq=1 ttl=64 time=0.215 ms
		#	64 bytes from media-router-fp1.prod1.media.vip.gq1.yahoo.com (98.137.246.7): icmp_seq=1 ttl=53 time=183 ms
		m1 = re.match(r"^\d+ bytes from [^\s]+: icmp_seq=1 ttl=\d+ time=([\d\.]+) ms$", lines[1])
		if m1:
			duration = float(m1.groups(1)[0])
		else:
			m2 = re.match(r"^\d+ bytes from [^\s]+ \([^\s]+\): icmp_seq=1 ttl=\d+ time=([\d\.]+) ms$", lines[1])
			if m2:
				duration = float(m2.groups(1)[0])
			else:
				duration = None
		return duration
	else:
		return None
#

async def _singlePingWB(host:str, timeout:int, output:typing.Union[typing.List,typing.Dict], position:typing.Union[int,str]):
	cp = await trio.run_process(["ping", host, "-c", "1", "-W", str(timeout)], capture_stdout=True, capture_stderr=True, check=False)
	if cp.returncode == 0:
		lines = cp.stdout.decode("utf-8").split("\n")
		assert lines[0].startswith("PING ")
		# OUTPUT:
		#	64 bytes from 192.168.10.200: icmp_seq=1 ttl=64 time=0.215 ms
		#	64 bytes from media-router-fp1.prod1.media.vip.gq1.yahoo.com (98.137.246.7): icmp_seq=1 ttl=53 time=183 ms
		m1 = re.match(r"^\d+ bytes from [^\s]+: icmp_seq=1 ttl=\d+ time=([\d\.]+) ms$", lines[1])
		if m1:
			duration = float(m1.groups(1)[0])
		else:
			m2 = re.match(r"^\d+ bytes from [^\s]+ \([^\s]+\): icmp_seq=1 ttl=\d+ time=([\d\.]+) ms$", lines[1])
			if m2:
				duration = float(m2.groups(1)[0])
			else:
				duration = None
		output[position] = duration
	else:
		output[position] = None
#

async def ping(host:str, timeout:int=2, repeats:int=1):
	assert isinstance(host, str)
	assert isinstance(timeout, int)
	assert isinstance(repeats, int)

	if repeats > 1:
		output = [ None ] * repeats
		async with trio.open_nursery() as nursery:
			for i in range(0, repeats):
				nursery.start_soon(_singlePingWB, host, timeout, output, i)
		for i in range(0, repeats):
			if output[i] is None:
				return None
		return sum(output) / repeats
	else:
		return await _singlePingR(host, timeout)
#

async def multiPing(hosts:typing.Union[typing.List,typing.Tuple], timeout:int=2, repeats:int=1):
	assert isinstance(hosts, (list, tuple))
	assert len(hosts) > 0
	assert isinstance(timeout, int)
	assert isinstance(repeats, int)

	if len(hosts) == 1:
		ret = await ping(hosts[0], timeout, repeats)
		return {
			hosts[0]: ret
		}

	else:
		if repeats > 1:
			output = {}

			async with trio.open_nursery() as nursery:
				for host in hosts:
					output[host] = [ None ] * repeats
					for i in range(0, repeats):
						nursery.start_soon(_singlePingWB, host, timeout, output[host], i)
	
			for host in hosts:
				bHasNone = None
				for i in range(0, repeats):
					if output[i] is None:
						bHasNone = True
				if bHasNone:
					output[host] = None
				else:
					output[host] = sum(output[host]) / repeats

			return output
		else:
			output = {}

			async with trio.open_nursery() as nursery:
				for host in hosts:
					nursery.start_soon(_singlePingWB, host, timeout, output, host)
	
			return output
#


