from .internal import DownloadFileInternal,to_string
from time import time
from jivi import jvWrapper

class _DownloadHelperData:
	__downloader : DownloadFileInternal
	def __init__(self,downloader):
		self.__downloader = downloader

	@property
	def total(self):						return self.__downloader.size
	
	@property
	def downloaded(self):					return self.__downloader.dblock_bytes_loaded

	@property
	def written(self):						return self.__downloader.writer_bytes_written

	@property
	def to_download(self):					return self.total - self.downloaded

	@property
	def to_write(self):						return self.total - self.written

	@property
	def speed(self):						return self.__downloader.info_download_speed



class _DownloadHelperDataHuman:
	__data : _DownloadHelperData
	def __init__(self,data):
		self.__data = data

	@property
	def total(self) -> str:				return to_string.bytes(self.__data.total)
	
	@property
	def downloaded(self) -> str:		return to_string.bytes(self.__data.downloaded)
	
	@property
	def written(self) -> str:			return to_string.bytes(self.__data.written)
	
	@property
	def to_download(self) -> str:		return to_string.bytes(self.__data.to_download)
	
	@property
	def to_write(self) -> str:			return to_string.bytes(self.__data.to_write)
	
	@property
	def speed(self) -> str:				return to_string.bytes(self.__data.speed) + '/s'



class _DownloadHelperTime:
	__downloader : DownloadFileInternal
	def __init__(self,downloader):
		self.__downloader = downloader
	
	@property
	def remaining(self):
		speed = self.__downloader.info.speed
		to_download = self.__downloader.src.size - self.__downloader.blocks.bytes_downloaded
		if speed == 0:
			return -1
		return to_download / speed


	@property
	def elapsed(self):				return time() - self.__downloader.time_started

	@property
	def started(self):				return self.__downloader.time_started

	@property
	def ended(self):				return self.__downloader.time_ended



class _DownloadHelperTimeHuman:

	__time : _DownloadHelperTime
	def __init__(self,timeOb):
		self.__time = timeOb

	@property
	def remaining(self) -> str:		return to_string.sec(self.__time.remaining)
	
	@property
	def elapsed(self) -> str:		return to_string.sec(self.__time.elapsed)
	
	@property
	def started(self) -> str:		return to_string.unix(self.__time.started)
	
	@property
	def ended(self) -> str:			return to_string.unix(self.__time.ended)

class _DownloadHelperError:
	src          : str                 
	download     : str                 
	write        : str                 
	__downloader : DownloadFileInternal
	
	def __init__(self,downloader):
		self.__downloader = downloader
	@property
	def has(self):
		return self.src or self.download or self.write
	
class _DownloadHelperStatus:
	__downloader : DownloadFileInternal
	def __init__(self,downloader):
		self.__downloader = downloader

	@property
	def finished(self) -> bool:				return self.__downloader.status_finished
	
	@property
	def running(self) -> bool:				return self.__downloader.status_running

	@property
	def stopped(self) -> bool:				return not self.__downloader.status_running

	@property
	def started(self) -> bool:				return self.__downloader.status_finished or self.__downloader.status_running

	@property
	def error(self) -> bool:
		return False
#		return self.__downloader.has_errors
	

class _DownloadHelperControl:
	__downloader : DownloadFileInternal
	def __init__(self,downloader):
		self.__downloader = downloader

	def start(self):							return self.__downloader.start()
	def stop(self):								return self.__downloader.stop()
	def reset(self):							return self.__downloader.reset()
	def move(self,new_fp=r'C:\temp\temp.tmp'):	return self.__downloader.move(new_fp)



class Download:
	__downloader : DownloadFileInternal              
	data         : _DownloadHelperData     
	dataHuman    : _DownloadHelperDataHuman
	time         : _DownloadHelperTime     
	timeHuman    : _DownloadHelperTimeHuman
	error        : _DownloadHelperError    
	status       : _DownloadHelperStatus   
	control      : _DownloadHelperControl  

	def __init__(self,url:str,fp:str, block_size_kb : int = 400, max_threads : int = 10):
		self.__downloader = DownloadFileInternal(url,fp,block_size_kb,max_threads)
		self.data         = _DownloadHelperData(self.__downloader)
		self.dataHuman    = _DownloadHelperDataHuman(self.data)
		self.time         = _DownloadHelperTime(self.__downloader)
		self.timeHuman    = _DownloadHelperTimeHuman(self.time)
		self.error        = _DownloadHelperError(self.__downloader)
		self.status       = _DownloadHelperStatus(self.__downloader)
		self.control 	  = _DownloadHelperControl(self.__downloader)
