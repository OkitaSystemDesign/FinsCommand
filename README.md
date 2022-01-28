# finsudp.py
OMRON FINS protocol UDP connection  
Memory Area Read

# Constructor
fins(host, destFinsAddress, sorceFinsAddres)

# Functions
### fins.read(memAddres, size)
Memory Area Read  
memAddress = D0-D32767, E0_0-EF_32767, W0-511, 0-6143  
Return: bytes()

### fins.toInt16(data)
Convert to 16bit data  
### fins.toInt32(data)
Convert to 32bit data  
### fins.toInt64(data)
Convert to 64bit data  
### fins.toUInt16(data)
Convert to Unsigned 16bit data  
### fins.toUInt32(data)
Convert to Unsigned 32bit data  
### fins.toUInt64(data)
Convert to Unsigned 64bit data  
### fins.toFloat(data)
Convert to Float data  
### fins.toDouble(data)
Convert to Double data  

 return: list
 

# Example
```
finsudp = fins('192.168.250.1', '0.1.0', '0.10.0')
data = finsudp.read('E0_0", 10)
print(finsudp.toInt16(data))
```
