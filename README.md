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

### fins.toInt**(data)
Data Convert  
 toInt16  
 toUInt16  
 toInt32  
 toUInt32  
 toInt64  
 toUInt64  
 return: list
 

# Example
```
finsudp = fins('192.168.250.1', '0.1.0', '0.10.0')
data = finsudp.read('E0_0", 10)
print(finsudp.toInt16(data))
```
