import modbus
a=modbus.modbus()
print " "
print 1,a.link(console="COM3")
print 2,a.send(1,"0x03","1","10")
print 3,a.close()
#print 2,a.close()
#print 3,a.link(mode="tcp",ip="192.168.99.91")
#print 4,a.close()
#print 5,a.set_mode(timeout=1)