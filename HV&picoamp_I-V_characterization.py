import serial
import time
import os
from pycaenhv.wrappers import init_system, deinit_system, get_board_parameters, get_crate_map, get_channel_parameter, set_channel_parameter
from pycaenhv.enums import CAENHV_SYSTEM_TYPE, LinkType
from pycaenhv.errors import CAENHVError

# Set environments variables (CAENHV_BOARD_TYPE, CAENHV_LINK_TYPE, CAENHV_BOARD_ADDRESS, CAENHV_USER, CAENHV_PASSWORD) See:https://github.com/vasoto/pycaenhv

def SetHV(BoardNum, Channel, Voltage):
	system_type = CAENHV_SYSTEM_TYPE[os.environ['CAENHV_BOARD_TYPE']]
	link_type = LinkType[os.environ['CAENHV_LINK_TYPE']]
	handle = init_system(system_type, link_type,
						 os.environ['CAENHV_BOARD_ADDRESS'],
						 os.environ.get('CAENHV_USER', ''),
						 os.environ.get('CAENHV_PASSWORD', ''))
	try:
		#print("Setting Voltage From %d to %d"%(get_channel_parameter(handle, BoardNum, Channel, "V0Set"),Voltage))
		set_channel_parameter(handle, BoardNum, Channel, "V0Set", Voltage)
		#time.sleep(1)
		#if (get_channel_parameter(handle, BoardNum, Channel, "V0Set") == float(Voltage)):
			#print("Voltage set Successfully to %d"%(get_channel_parameter(handle, BoardNum, Channel, "V0Set")))
	except CAENHVError as err:
		print(f"Got error: {err}\nExiting ...")
	finally:
		deinit_system(handle=handle)


def HVpower(BoardNum, Channel, Power):
	system_type = CAENHV_SYSTEM_TYPE[os.environ['CAENHV_BOARD_TYPE']]
	link_type = LinkType[os.environ['CAENHV_LINK_TYPE']]
	handle = init_system(system_type, link_type,
						 os.environ['CAENHV_BOARD_ADDRESS'],
						 os.environ.get('CAENHV_USER', ''),
						 os.environ.get('CAENHV_PASSWORD', ''))
	try:
		#print("Setting Power From %d to %d"%(get_channel_parameter(handle, BoardNum, Channel, "Pw"),Power))
		set_channel_parameter(handle, BoardNum, Channel, "Pw", Power)
		#time.sleep(1)
		#if (get_channel_parameter(handle, BoardNum, Channel, "Pw") == float(Power)):
			#print("Power set Successfully to %d"%(get_channel_parameter(handle, BoardNum, Channel, "Pw")))
	except CAENHVError as err:
		print(f"Got error: {err}\nExiting ...")
	finally:
		deinit_system(handle=handle)





if __name__ == '__main__':

	os.environ['CAENHV_BOARD_TYPE'] = 'SY1527'
	os.environ['CAENHV_LINK_TYPE'] = 'TCPIP'
	os.environ['CAENHV_BOARD_ADDRESS'] = '152.84.100.112 1527'
	os.environ['CAENHV_USER'] = 'user'
	os.environ['CAENHV_PASSWORD'] = 'flango'

file_name=input("digite o nome do arquivo texto (sem a extensao): ")

Vstop=float(input("digite o valor de parada: "))

SetHV( 0, 5, 0)
HVpower( 0, 5, 1)

Vplus=float(input("digite de quanto em quanto a tensão deve variar: "))
events_num=int(Vstop//Vplus)+1

tempo=(4*Vplus)/5 #pois com 4 segundos da pra variar 5 Volts e fazer uma medida com tranquilidade, mas da pra melhorar esse tempo ai!!

Voltage_list=list(range(events_num))
Current_list=list(range(events_num))

Vput=0
event=0
while(Vput<=Vstop):

	#picoamperimetro entra aqui

    time.sleep(tempo)

    Voltage_list[event]=Vput #depois da pra tentar usar a tensão de fato medida pela fonte 

    SetHV( 0, 5, Vput)
    Vput=Vput+Vplus
    event=event+1
print("o loop acabou.")

time.sleep(tempo)
HVpower( 0, 5, 0)
SetHV( 0, 5, 0)

print(Voltage_list) #teste
print(Current_list) #teste

a=0
b=0

with open(file_name+".txt", "w") as arquivo:

    arquivo.write("Voltagens: ")
    while(a<events_num):
        arquivo.write(str(Voltage_list[a])+" ")
        a=a+1
        
    arquivo.write("\nCorrentes: ")

    while(b<events_num):
        arquivo.write(str(Current_list[b])+" ")
        b=b+1