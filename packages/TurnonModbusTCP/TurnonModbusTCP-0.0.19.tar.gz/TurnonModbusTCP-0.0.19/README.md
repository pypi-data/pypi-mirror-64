TurnonModbusTCP



Python3.X :  import TurnonModbusTCP



clear_print()

	type: < Operation >
	request type: {}
	result type: {}

	Explanation: Clear the command line.


get_my_IP()

	type: < Event >
	request type: {}
	result type: { [string] }

	Explanation:  Get your IP.


set_client()

	type: < Operation >
	request type: { ServerIP= [string] , ServerPORT= [int] }
	result type: {}

	Explanation: Set up for connect to Modbus server.


client_start()

	type: < Operation >
	request type: {}
	result type: {}

	Explanation: Connect to Modbus server.


state()

	type: < Event >
	request type: { address= [int] }
	result type: { [int] }

	Explanation: Get Modbus's value.


state()

	type: < Event >
	request type: { address= [int] , ID= [int] }
	result type: { [bool] }

	Explanation: Get Modbus's value.


mode()

	type: < Event >
	request type: {}
	result type: { [int] }

	Explanation: It will return Franka arm's mode which are working.


ECHO_FRANKA_STATE()

	type: < Event >
	request type: {}
	result type: {}

	Explanation: Repeat output Modbus's value and print on command line.


visual_command_Read()

	type: < Event >
	request type: {}
	result type: { [string] }

	Explanation: Get command from Franka apps by Modbus.


visual_wait_command()

	type: < Event >
	request type: {}
	result type: { [string] }

	Explanation: Waiting for Franka apps command and then return it.


visual_output_Write()

	type: < Operation >
	request type: { [string] }
	result type: {}

	Explanation: Send the information to Franka arm by Modbus.









