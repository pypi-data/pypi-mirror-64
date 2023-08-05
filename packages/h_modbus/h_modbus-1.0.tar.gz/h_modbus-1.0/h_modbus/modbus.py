import serial
import socket
class modbus():
	def _crc_cher_(self,modbus):
		_crc_=[]
		for i in xrange(len(modbus)/2):
			_crc_.append(int(modbus[0+i*2:2+i*2],16))
		CRC_recode=bin(int("FFFF",16))[2:].zfill(16)
		for i in _crc_:
			CRC_recode= bin(int(CRC_recode,2)^i)[2:].zfill(16)
			for i in xrange(8):
				ans_me=CRC_recode[-1]
				CRC_recode=CRC_recode[:-1].zfill(16)
				if ans_me=="1":
					CRC_recode=bin(int(CRC_recode,2)^int("A001",16))[2:].zfill(16)
		CRC_recode=CRC_recode[8:]+CRC_recode[:8]
		return hex(int(CRC_recode,2))[2:].upper().zfill(4)
	def _return_modbus_(self,modbus):
		self._recode_=''
		for i in xrange(len(modbus)/2):
			self._recode_+= chr(int(modbus[0+i*2:2+i*2],16))
		return self._recode_		
	def __init__(self,):
		self._com_link_=False
		self._recode_=''
		self._data_={"console":"",
					"baudrate":9600,
					"parity":"None",
					"bits":"8",
					"stopbits":"1",
					"timeout":0.05,
					"ip":"127.0.0.1",
					"port":502,
					"mode":"rtu"}
	def set_mode(self,**data):
		for i in data.keys():
			if self._data_.has_key(i):
				self._data_[i]=data[i]
		return True
	def link(self,**data):
		self.set_mode(**data)
		if self._data_["mode"]=="rtu":
			__parity__={"None":serial.PARITY_NONE,"Even":serial.PARITY_EVEN,"Odd":serial.PARITY_ODD}
			__bytesize__={'7':serial.SEVENBITS,'8':serial.EIGHTBITS}
			__stopbits__= {'1':serial.STOPBITS_ONE, '1.5':serial.STOPBITS_ONE_POINT_FIVE, '2':serial.STOPBITS_TWO}
			try:
				self._ser_=serial.Serial(self._data_["console"],int(self._data_["baudrate"]),
									stopbits=__stopbits__.get(self._data_["stopbits"],serial.STOPBITS_ONE),
									bytesize=__bytesize__.get(self._data_["bits"],serial.EIGHTBITS),
									parity =__parity__.get(self._data_["parity"],serial.PARITY_NONE),
									timeout=self._data_["timeout"])
				self._com_link_=True
				return True
			except:
				return False
		elif self._data_["mode"] == "tcp":
			self._ser_=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self._ser_.settimeout(3)
			try:
				self._ser_.connect((self._data_["ip"],int(self._data_["port"])))
				self._com_link_=True
				return True
			except  Exception as e:
				print e
				return False
		else:
			return False
	def close(self,):
		try:
			self._ser_.close()
		except:
			pass
		self.com_link=False
		return True
	def send(self,slave="",function="",position="",data_len="",writ_len=1,udf_date="",):
		def date_READ():
			date=""
			return_data=""
			if  udf_date!="":
				date=udf_date
			elif function =="0x01" or function =="0x02":
				date+=hex(slave)[2:].zfill(2)
				date+=function[2:]
				date+=hex(int(position))[2].zfill(4)
				date+=hex(int(data_len))[2].zfill(4)
				nb=1+1+1+2+int(data_len)
			elif function =="0x03" or function =="0x04":
				date+=hex(slave)[2:].zfill(2)
				date+=function[2:]
				date+=hex(int(position))[2].zfill(4)
				date+=hex(int(data_len))[2].zfill(4)
				nb=1+1+2+2+int(data_len)
			elif function =="0x05":
				date="%s%s%s"%(hex(slave)[2:].zfill(2),function[2:],hex(int(position))[2].zfill(4))
				if int(data_len,16) ==0:
					date+="0000"
				elif  int(data_len,16) ==1:
					date+="FF00"
				elif int(data_len,16) ==255:
					date+="FF00"
				else:
					date="data error"
				nb=8
			elif function =="0x06":
				date="%s%s%s%s"%(hex(slave)[2:].zfill(2),function[2:],hex(int(position))[2].zfill(4),hex(int(data_len))[2].zfill(4))
				nb=8
			elif function =="0x0f":
				s= hex(int(data_len))[2:]
				if len(s)%4!=0:
					s=s.zfill(4)
				date+=hex(slave)[2:].zfill(2)
				date+=function[2:]
				date+=hex(int(position))[2].zfill(4)
				
				date+=hex(writ_len)[2].zfill(4)
				date+=hex(len(s))[2:].zfill(2)
				print s
				date+=s
				nb=8
			elif function =="0x10":
				date+=hex(slave)[2:].zfill(2)
				date+=function[2:]
				date+=hex(int(position))[2].zfill(4)
				date+=hex((len(data_len.split(","))))[2:].zfill(4)
				date+=hex((len(data_len.split(",")))*2)[2:].zfill(2)
				for i in data_len.split(","):
					date+=hex(int(i))[2:].zfill(4)
				nb=8
			else:
				date="function error"
			return date,nb
			
		if  self._com_link_:
			if (slave=="" or function=="" or position=="" or data_len=="" ) and udf_date=="":
				return False , "data error",""
			date,nb=date_READ()
			if "error" in date:
				return fmt_data,date,""
			elif self._data_.get("mode")=='rtu':
				fmt_data=False
				return_data=""
				try:
					date+=self._crc_cher_(date)
					
					self._ser_.write(self._return_modbus_(date))
					s=self._ser_.read(nb)
					if s is not '':
						return_data=s.encode('hex').upper()
						fmt_data= True
				except Exception as e:
					return_data=e
			elif self._data_.get("mode")=='tcp':
				date=date_READ()
				date="00010000%s%s"%(hex(len(date)/2).split("x")[1].zfill(4),date)
				self.ser.sendall(self._return_modbus_(date))
				try :
					s=self.ser.recv(nb)
				except:
					s=''
				fmt_data=False
				if s is not '':
					return_data=s.encode('hex').upper()
					fmt_data= True
		else:
			fmt_data=False
		return fmt_data,date.upper(),return_data		