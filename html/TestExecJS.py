from Naked.toolshed.shell import execute_js, muterun_js

def SendToDB(input):
	success = execute_js('DataBaseConnect_4.js', input)
	#Error Handling
	#if response.exitcode == 0:
	#  print(response.stdout)
	#else:
	#  sys.stderr.write(response.stderr)
