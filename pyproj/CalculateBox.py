"""
By Nicholas Hylands
This program was created to solve the 9-box problem:
   [ ][ ][ ]
   [ ][ ][ ]
[ ][ ][ ][x]
we need to fill this up so that each row and column in the middle are the sum of their
respective adjacent numbers on the outside.

A possibility for the question was considered so that 1,1 and 1,2 would be the sum of [0,3] * 10 + [1,2]
this possibility has been proven wrong, as when we run this program, we go over every single possibility.
"""

myData = range(1,9)


print myData, " "
print "========================="

#first, check the digits to the right of curDig
def checkFromRight(givenList, num): #num, is the number to check to from the right...
	##print num, ' ', len(givenList)
	#print "checking from right to: ", num
	if num >= len(givenList)-1:
		#print "num is equal or greater than length"
		return 0
	for i in range(len(givenList)-1, num, -1):
		#print "Comparing ", num,givenList[num],',', " to ",i,',', givenList[i], " in ", givenList
		if givenList[i] > givenList[num]:
			#print 'Time to Swap', i, ' ', num
			return i
	#print "nope, time to shift..."
	return 0
	

#reverse a sub-array in an array between two points
#remember to use the function so that the numbers given are actual numbs
#in array: start with 0
def reverseBetween(start, finish, given):
	if start > 0 and finish < (len(given)):
		swap = [given[finish]]#create the swap variable
		for i in range(finish-1, start-1, -1):
			swap.append(given[i]) #do our temp-function thing
		for i in range(start, finish+1): #why is it finish + 1?
			given[i] = swap[i-start]
	return given
	
#here we check a list of 8, and if it solves the box, we return true.
def checkSolvedBoxWithFixedOne(given):
	#check the list with the box
	check = given
	check[check.index(8)] = 9
	if check[0] + check[3] == check[7]:
		if check[1] + check[4] == 8:
			if check[0] + check[1] == check[2]:
				if check[3] + check[4] == check[5]:
					if check[6] == 1:
						check[check.index(9)] = 8
						return 2 #case 2, the box is solved WITH the one in the bottom left.
						
					else:
						check[check.index(9)] = 8
						return 1
	check[check.index(9)] = 8
	return 0

#test an array for the possibilities
def testList(given, curDig = None):
	if curDig is None:
		curDig = len(given)-1 #remember curDig will be 7 if list has 8 digits.
	#create our list to return
	results = [0]
	resultsSolvedWithOne = []
	resultsSolvedWithoutOne = []
	#first check from the right from the current digit.
	listToTest = given
	#print "list to test is: ", listToTest
	  
	while curDig is not -1:
		numToSwap = checkFromRight(listToTest,curDig)
		#print 'num to swap is: ', numToSwap
		if numToSwap is not 0:
			#swap:
			#print 'swapping: ', listToTest, ' ', curDig, ' ', numToSwap
			listToTest[curDig], listToTest[numToSwap] = listToTest[numToSwap], listToTest[curDig]
			#print 'swapped: ', listToTest
			
			#print "reversing after curDig..."
			listToTest = reverseBetween(curDig+1,len(listToTest)-1,listToTest)
			#print "result is... ", listToTest
			#CHECK TO SEE IF ITS SOLVED:
			#print "=========================="
			#print listToTest
			#print "num results was ", results[0]
			results[0] = results[0] + 1
			#print "num results now is ", results[0]
			#print "=========================="
			if results[0] > 40321:
				return results
			
			#Check the results############
			checkIfSolved = checkSolvedBoxWithFixedOne(listToTest)
			
			if checkIfSolved == 1:
				resultsSolvedWithoutOne.append(listToTest)
			if checkIfSolved == 2:
				if listToTest is not [8,7,6,5,4,3,2,1]:
					resultsSolvedWithOne.append(listToTest)
			##############################
			
			#reset:
			#print "resetting curDig to length from: ", curDig
			curDig = len(given) - 1
			#repeat:
			#how to repeat? Run a loop!
		else:
			#print 'shifting curdigit', curDig, curDig-1
			#shift to the left
			#sort the digits to the right of curDig
			curDig = curDig - 1	
	results.append(resultsSolvedWithOne)
	results.append(resultsSolvedWithoutOne)
	return results

myResult = testList(myData)

print 'possibilities total: ', myResult[0]
print 'possibilities if bottom left is 1: ',myResult[1]
print 'possibilities if bottom left can be anything: ',myResult[2]
			
			