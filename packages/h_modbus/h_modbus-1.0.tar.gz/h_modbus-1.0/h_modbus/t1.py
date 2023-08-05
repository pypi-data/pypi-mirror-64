import pymodbus.utilities
import time
def crc_cher(modbus):
	_crc_=[]
	for i in xrange(len(modbus)/2):
		_crc_.append(int(modbus[0+i*2:2+i*2],16))
	CRC_recode=bin(int("FFFF",16))[2:].zfill(16)
	for i in _crc_:
		CRC_recode= bin(int(CRC_recode,2)^i)[2:].zfill(16)
		for i in xrange(8):
			
			if CRC_recode[-1]=="1":
				CRC_recode=CRC_recode[:-1].zfill(16)
				CRC_recode=bin(int(CRC_recode,2)^int("A001",16))[2:].zfill(16)
			else:
				CRC_recode=CRC_recode[:-1].zfill(16)
	CRC_recode=CRC_recode[8:]+CRC_recode[:8]
	return hex(int(CRC_recode,2))[2:].upper().zfill(4)
def __crc_cher__(modbus):
	crc=''
	for i in xrange(len(modbus)/2):
		crc+= chr(int(modbus[0+i*2:2+i*2],16))
	return ("{0:0>4X}".format(pymodbus.utilities.computeCRC(crc)))
t1=time.clock()
print crc_cher("01030000000F")
t2=time.clock()
print __crc_cher__("01030000000F")
t3=time.clock()
t4=time.clock()
print("my\t",(t2-t1)-(t4-t3))
print("py\t",t3-t2-(t4-t3))