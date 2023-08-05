from urllib.request import Request,urlopen
from time import sleep,time
from queue import Queue
from typing import List
from threading import Thread
from operator import itemgetter
import os,random, traceback, math, datetime, http
from jivi.util import to_string,to_int

class DownloadFileInternal:
	block_size            : int          = 0
	nthreads              : int          = 0
	url                   : str          = None
	fp                    : str          = None
	size                  : int          = 0
	accept_ranges         : bool         = False

	info_thread           : Thread     
	info_write_speed = 0
	info_download_speed = 0

	writer_bytes_written  : int          = 0
	writer_blocks_written : int          = 0
	writer_q              : Queue        = None
	writer_thread         : Thread      

	dblock_bytes_loaded   : int          = 0
	dblock_success        : int          = 0
	dblock_total          : int          = 0
	dblock_failed         : int          = 0
	dblock_q              : Queue        = None
	dblock_threads        : List[Thread] = []

	status_running        : bool         = False

        

	
	def __init__(self,url:str,fp:str,block_size_kb:int=500,nthreads:int=5):
		self.url             = url
		self.fp              = fp
		self.block_size      = block_size_kb * 1024
		self.nthreads        = nthreads
		
		self.info_init()
		self.dlbock_init()
		self.status_init()
		self.writer_init()

	def status_init(self):
		self.status_running  = False


	def dlbock_init(self):
		self.dblock_q        = Queue()
		self.dblock_threads  = [Thread(target=self.dblock_thread_func,daemon=True) for i in range(self.nthreads)]


	def dblock_reset(self):
		self.dblock_bytes_loaded = 0
		self.dblock_success      = 0
		self.dblock_total        = 0
		self.dblock_failed       = 0

	def dblock_start(self):
		self.dblock_reset()
		self.dblock_total = self.dblock_q.qsize()
		for t in self.dblock_threads:
			t.start()

	def dblock_thread_func(self):
		def download_block(index=0,failed=0):
			def action_success():
				self.dblock_success += 1
			def action_failed():
				if failed < 2:
					self.dblock_q.put(dict(index=index,failed=failed+1))
					return
				else:
					self.dblock_failed += 1
			
			block_start, block_stop = ((index*self.block_size), min( (self.size - 1) , ((index + 1) * self.block_size - 1) ) )

			data_len = block_stop - block_start + 1
			request    = None

			for attemp in range(5):
				try:
					request                  = Request(self.url)
					request.headers["Range"] = 'bytes=%d-%d'%(block_start,block_stop)
					break
				except:
					print(traceback.format_exc())
					sleep(3)
			
			if request is None:
				return action_failed()
			for attemp in range(10):
				try:
					data = urlopen(request)
					data = data.read()
					self.dblock_bytes_loaded += data_len
					self.writer_q.put(dict(index=index,data=data))
					return action_success()
				except (http.client.IncompleteRead) as e:
					data_len_to_do = (block_stop - block_start + 1)
					self.dblock_bytes_loaded += data_len_to_do
					data_to_write = e.partial + str.encode('0'*( data_len_to_do - len(e.partial)))
					self.writer_q.put(dict(index=index,data=data_to_write))
					
		
					return action_success()
				except:
					print(traceback.format_exc())
					sleep(2)
		
			return action_failed()
		
		while self.status_running and ( not self.status_finished ):
			while self.dblock_q.empty():
				if self.dblock_finished:
					return
				sleep(2)
			
			todo        = self.dblock_q.get()
			download_block(**todo)
	
	def writer_init(self):
		self.writer_q        = Queue()
		self.writer_thread   = Thread(target=self.writer_thread_func,daemon=True)

	def writer_reset(self):
		self.writer_bytes_written = 0
		self.writer_blocks_written = 0

	def writer_start(self):
		self.writer_reset() #!
		self.writer_thread.start()

	def writer_thread_func(self):
		def try_writing():
			todo = []
			while not self.writer_q.empty():
				q = self.writer_q.get()
				todo.append(q)
			
			if not todo:
				return
			todo.sort(key=lambda x: x.get('index'))

			with open(self.fp, "r+b") as f:
				cursor_now  = 0
				for td in todo:
					index,data 		   = itemgetter('index','data')(td)
					cursor_destination = index * self.block_size
					if (cursor_delta := cursor_destination-cursor_now) > 0:
						f.seek(cursor_delta,1)
					f.write(data)
					writtenNow    = len(data)
					cursor_now    = cursor_destination+writtenNow
					self.writer_bytes_written += writtenNow
					self.writer_blocks_written += 1

		
		while self.status_running and ( not self.status_finished ):
			try_writing()
			sleep(1)
			
	def info_init(self):
		self.info_thread     = Thread(target=self.info_thread_func,daemon=True)

	def info_start(self):
		self.info_thread.start()



	def info_thread_func(self):

		self.info_write_speed          = 0
		self.info_download_speed       = 0
		sleep_time = 1

		def get_data_now():
			return dict(
				t=time(),
				written=self.writer_bytes_written,
				downloaded=self.dblock_bytes_loaded
			)
		data = []
		data.append(get_data_now())
		sleep(1)
		while self.status_running and ( not self.status_finished ):
			data.append(get_data_now())
			data = data[-5:]

			first_data_entry = data[0]
			last_data_entry = data[-1]
			
			delta = {k : last_data_entry[k] - first_data_entry[k] for k in ['t','written','downloaded']}
			
			self.info_write_speed		= delta.get('written') / delta.get('t')
			self.info_download_speed	= delta.get('downloaded') / delta.get('t')

			sleep_time_more = max(0, sleep_time - (time() - last_data_entry.get('t')))
			if sleep_time_more:
				sleep(sleep_time_more)

	

	
	def reload(self):
		def reload_header():
			self.size          = 0
			self.accept_ranges = False
			for attempt in range(5):
				try:
					open_response = urlopen(self.url,timeout=10)
					self.size = to_int(open_response.headers.get('Content-Length',0))
					if not self.size:
						return False
					self.accept_ranges  = open_response.headers.get('accept-ranges','no') == 'bytes'
					return True
				except:
					sleep(1)
			
			return False
	
		def reload_local_file():
			def write_empty_file_if_not_exist():
				file_already_started 			   = os.path.isfile(self.fp) and (os.path.getsize(self.fp) == self.size)
				if file_already_started:
					return
				
				bytes_written 					   = 0
				bytes_to_write                     = self.size
				empty_str_20mb_len                 = 1024*1024*20
				empty_str_20mb                     = str.encode('0'*empty_str_20mb_len)
				with open(self.fp,"wb") as f:
					while bytes_written + empty_str_20mb_len <= bytes_to_write:
						f.write(empty_str_20mb)
						bytes_written += empty_str_20mb_len
					
					bytes_to_write_more = bytes_to_write -  bytes_written
					if bytes_to_write_more:

						f.write(str.encode('0'*bytes_to_write_more))
						

				sleep(1)

			def get_block_indexes_to_download():
				block_size             = self.block_size
				empty_block_str        = str.encode('0'*block_size)
				block_index            = 0
				indexes_to_download    = []
				blocks_already_written = 0
				
				with open(self.fp,"rb") as f:
					data = f.read(block_size)
					while data:
						data_len  = len(data)
						do_append = ((data_len == block_size) and (data == empty_block_str)) or ((data_len != block_size) and (data == str.encode('0'*data_len)))
						if do_append:
							indexes_to_download.append(block_index)
						else:
							blocks_already_written 	+= 1

						block_index += 1
						data 		= f.read(block_size)


				return indexes_to_download	

			def set_block_indexes_to_download(indexes):
				for i in indexes:
					self.dblock_q.put((dict(index=i,failed=0)))

			write_empty_file_if_not_exist()
			block_indexes_to_download = get_block_indexes_to_download()


			set_block_indexes_to_download(block_indexes_to_download)
		reload_header()
		reload_local_file()

	def stop(self):
		self.status_running = False
		return True
	
	def start(self):
		self.reload()
		self.status_running = True
		funcs_to_do = [self.dblock_start,self.writer_start,self.info_start]
		for t in funcs_to_do:
			t()
		

	def reset(self):
		print(f'Reset not yet implemented')

	def move(self,new_fp):
		print(f'Move not yet implemented!')
	
	@property
	def writer_finished(self) ->bool:
		return self.writer_blocks_written >= (self.dblock_total - self.dblock_failed)

	@property
	def dblock_finished(self) ->bool:
		return self.dblock_total == (self.dblock_success + self.dblock_failed)

	
	@property
	def status_finished(self) -> bool:
		return self.writer_finished and self.dblock_finished
	

