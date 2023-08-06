#!/usr/bin/python3



import warnings
import sys
import typing
import trio

import jk_console
import jk_json
import jk_argparsing

import jk_trioping

warnings.filterwarnings("ignore")








ap = jk_argparsing.ArgsParser("multiping", "Ping multiple hosts at the same time.")

ap.optionDataDefaults.set("help", False)
ap.optionDataDefaults.set("output-format", "text")
#ap.optionDataDefaults.set("color", True)

ap.createOption("h", "help", "Display this help text.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("help", True)
ap.createOption("j", "json", "Print output in JSON format.").onOption = \
	lambda argOption, argOptionArguments, parsedArgs: \
		parsedArgs.optionData.set("output-format", "json")

ap.createAuthor("Jürgen Knauth", "jk@binary-overflow.de")
ap.setLicense("Apache", YEAR = 2020, COPYRIGHTHOLDER = "Jürgen Knauth")

ap.createReturnCode(0, "Everything is okay.")
ap.createReturnCode(1, "An error occurred.")






parsedArgs = ap.parse()

if parsedArgs.optionData["help"] or not parsedArgs.programArgs:
	ap.showHelp()
	sys.exit(0)





async def main(ipAddresses:typing.Union[list,tuple]):
	ret = await jk_trioping.multiPing(ipAddresses)
	if parsedArgs.optionData["output-format"] == "json":
		jk_json.prettyPrint(ret)
	else:
		table = jk_console.SimpleTable()
		table.addRow("IP Address", "Ping").hlineAfterRow = True
		for key in sorted(ret.keys()):
			value = ret[key]
			table.addRow(key, "-" if value is None else (str(value) + " ms"))
		table.print()
#

trio.run(main, parsedArgs.programArgs)












