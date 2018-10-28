import openpyxl as xl
import datetime

# Return building letter and row index in Excel sheet for specified keycode.
def room_find(keycode, cChoice):
	if cChoice == '1' or cChoice == '3':
		if keycode in bCodes:
			return 'B' + str(bCodes.index(keycode))
		if keycode in cCodes:
			return 'C' + str(cCodes.index(keycode))
		if keycode in dCodes:
			return 'D' + str(dCodes.index(keycode))
		if keycode in eCodes:
			return 'E' + str(eCodes.index(keycode))
		if keycode in fCodes:
			return 'F' + str(fCodes.index(keycode))
		if keycode in gCodes:
			return 'G' + str(gCodes.index(keycode))
		if keycode in hCodes:
			return 'H' + str(hCodes.index(keycode))
		if keycode in iCodes:
			return 'I' + str(iCodes.index(keycode))
		if keycode in jCodes:
			return 'J' + str(jCodes.index(keycode))
		if keycode in kCodes:
			return 'K' + str(kCodes.index(keycode))
	else:
		return 'L' + str(lCodes.index(keycode))

# Keycodes of each building.
bCodes = list(range(1549, 1707))
cCodes = list(range(1708, 1866))
dCodes = list(range(1158, 1389))
eCodes = list(range(804, 808)) + list(range(926, 1127)) + list(range(1133, 1157))
fCodes = list(range(834, 925))
gCodes = list(range(602, 803)) + list(range(809, 833)) + list(range(1128, 1132))
hCodes = list(range(1390, 1548))
iCodes = list(range(363, 601))
jCodes = list(range(1, 4)) + list(range(150, 173)) + list(range(176, 183)) + list(range(186, 362))
kCodes = list(range(5, 149)) + [174, 175, 184, 185]
lCodes = list(range(1, 400))
		
# Load audit book.
fillBook = xl.load_workbook(filename = '../Fill.xlsx')

# Setup for reading audit.
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

# Determine what buildings to anticipate.
complexChoice = input('\nPlease choose a complex:\n1. Vista\n2. Villas\n3. Both\n\n')
while complexChoice != '1' and complexChoice != '2' and complexChoice != '3':
	print('\nInvalid choice, please input 1, 2 or 3\n')
	complexChoice = input('\n1. Vista\n2. Villas\n3. All?\n\n')

if (complexChoice == '1' or complexChoice == '3'):
	print('\nUsing Vista keycodes.')
else:
	print('\nUsing Villas Keycodes.')

inputKey = (input(
				'\nPlease begin entering keycodes.\n'
				'Enter h for help. Enter x to exit.\n\n'))

# Continuously read for input.
while inputKey != 'x' or complexChoice == 3:
	# Print help menu.
	if inputKey == 'h':
		print(
			'\nFormat of keycodes:\n'
			'INPUT = KEYCODE. .COMMENT\n'
			'KEYCODE = NUM.NUM.NUM | NUM.NUM.NUM.NUM\n'
			'COMMENT = r | m | f | u | lo | lc | COMMENT.COMMENT | EPSILON\n'
			'\n'
			'Comment definitions:\n'
			'r = room\n'
			'm = mail\n'
			'f = fob\n'
			'u = urgent\n'
			'lo = lock out\n'
			'lc = lock change\n'
			'none = full set\n')

	# inputKey is only numbers, so a full set.
	elif inputKey.isdigit():
		# room contains:
		# room[0] -> building letter.
		# int(room[1:]) -> row number in fillSheet for room.
		# Must add 2 to int(room[1:]) to compensate for 0-indexing and header in Excel.
		room = room_find(int(inputKey), complexChoice)
		fillSheet = fillBook[room[0]]

		# Determine if room is a studio.
		if fillSheet['G' + str(int(room[1:]) + 2)].value == 'Studio':
			# Fill in full set for studio.
			fillSheet['E' + str(int(room[1:]) + 2)].value = 1
			fillSheet['F' + str(int(room[1:]) + 2)].value = 1
		else:
			# Fill in full set for regular room.
			fillSheet['D' + str(int(room[1:]) + 2)].value = 1
			fillSheet['E' + str(int(room[1:]) + 2)].value = 1
			fillSheet['F' + str(int(room[1:]) + 2)].value = 1

	# inputKey has comments attached.
	elif inputKey != 'x':
		room = room_find(int(inputKey[0:inputKey.index(' ') - 1]), complexChoice)
		fillSheet = fillBook[str(room[0])]

		comments = inputKey[inputKey.index(' ') + 1:]
		# Iterate through comments.
		for comment in comments:
			if comment == 'r':
				fillSheet['D' + str(int(room[1:]) + 2)].value = 1
			elif comment == 'm':
				fillSheet['E' + str(int(room[1:]) + 2)].value = 1
			elif comment == 'f':
				fillSheet['F' + str(int(room[1:]) + 2)].value = 1
			elif comment == 'u':
				fillSheet['C' + str(int(room[1:]) + 2)].value = 0
				fillSheet['G' + str(int(room[1:]) + 2)].value = "Urgent"
			elif comment == 'lo':
				fillSheet['C' + str(int(room[1:]) + 2)].value = 0
				fillSheet['G' + str(int(room[1:]) + 2)].value = "Lock out"
			elif comment == 'lc':
				fillSheet['C' + str(int(room[1:]) + 2)].value = 0
				fillSheet['G' + str(int(room[1:]) + 2)].value = "Lock change"
	
	# Switch from Vista to Villas for doing all keys.
	if complexChoice == '3' and inputKey == 'x':
		complexChoice = '2'
		print("\n Switching to Villas keycodes.\n\n")

	inputKey = input()

fillBook.save("../[" + datetime.datetime.today().strftime('%y%m%d') + "]KeyAudit.xlsx")