import time
from datetime import datetime
from moment import Moment
import csv

storeColumns = []

class parser: 
    #get the first item in the column and do logic based on name
    def convertByColumn(self, column):
        columnName = str(column[0]).lower()
        newColumn = column

        if columnName == 'timestamp':
            newColumn = self.convertTimestampToEastern(newColumn)
            print(columnName, newColumn)

        elif columnName == 'address':
            newColumn = self.checkAddressUnicode(newColumn);
            print(newColumn, columnName)
        
        elif columnName == 'zip':
            newColumn = self.convertZipcode(newColumn)
            print(columnName, newColumn)

        elif columnName == 'fullname':
            newColumn = self.convertNameUppercase(newColumn)
            print(columnName, newColumn)

        elif columnName == 'fooduration':
            newColumn = self.convertDatetoFloat(newColumn)
            print(columnName, newColumn)

        elif columnName == 'barduration':
            newColumn = self.convertDatetoFloat(newColumn)
            print(columnName, newColumn)

        elif columnName == 'totalduration':
            newColumn = self.combineValuesForBothColumns(newColumn, storeColumns[4], storeColumns[5])
            print(columnName, newColumn)

        elif columnName == 'notes':
            newColumn = self.checkNotesUnicode(newColumn);
            print(columnName, newColumn)

        else:
            print('NOT VALID')

        storeColumns.append(newColumn)

        if len(storeColumns) == 8:
           self.writeCsvFile(storeColumns)




    # takes a column and converts its contents to utf-8, must be string
    def convertToUtf8(self, arrayOfStringsToConvert):
        newArrayOfString = []
        
        for item in arrayOfStringsToConvert:
            if not(self.isUTF8(item)):
                encodedStr = item.encode(encoding='UTF-8')
                print('MUST ENCODE STRING!', encodedStr, '\n')
                newArrayOfString.append(encodedStr)
            else:
                newArrayOfString.append(item)

        return newArrayOfString


    def isUTF8(self, strData):
        try:
            bytes(strData, 'unicode').decode('UTF-8', 'strict')
        except Exception:
            return False
        else:
            return True



    #takes column and converts dates to eastern, with iso format, returns string
    def convertTimestampToEastern(self, arrayOfTimeStamps):
        newArrayOfTimeStamps = []
        dateFormat = '%m-%d-%y %H:%M:%S'

        for i, val in enumerate(arrayOfTimeStamps):
            if i != 0:
                newTime = Moment(val, dateFormat).timezone("US/Eastern").strftime(dateFormat)
                newArrayOfTimeStamps.append(str(newTime))
            
        return newArrayOfTimeStamps




    #takes a column with zipcodes and returns a string with zipcode formated
    def convertZipcode(self, arrayOfZipcodes):
        newArrayOfZipcodes = []

        for i, val in enumerate(arrayOfZipcodes):
            zipcode = str(val)
            if i != 0:
                if len(zipcode) < 5:
                    while len(zipcode) < 5:
                        zipcode = zipcode + '0'
                    newArrayOfZipcodes.append(zipcode)
                else: 
                    newArrayOfZipcodes.append(zipcode)
            
        return newArrayOfZipcodes




    # converts name string to uppercase
    def convertNameUppercase(self, arrayOfNames):
        newArrayOfNames = []

        for i, val in enumerate(arrayOfNames):
            newArrayOfNames.append(str(val).upper())
            

        return self.convertToUtf8(newArrayOfNames)
 


    

    # checks address for unicode validation
    def checkAddressUnicode(self, arrayOfAddress):
        return self.convertToUtf8(arrayOfAddress)




    # checks notes for unicode validation
    def checkNotesUnicode(self, arrayOfNotes):
        return self.convertToUtf8(arrayOfNotes)




    #converts date to a floating point seconds format.
    def convertDatetoFloat(self, dateArray):
        newArrayofDates = []
        
        for i, val in enumerate(dateArray):
            if i != 0:
                h, m, s = val.split(':')
                seconds =  float(h) * 3600 + float(m) * 60 + float(s)
                newArrayofDates.append(seconds)
            else:
                newArrayofDates.append(val)

        
        return newArrayofDates

    
    def combineValuesForBothColumns(self, currentColumn, column1, column2):
        newDuration = []
        
        for i, val in enumerate(column1):
            if i != 0:
                fullDuration = column1[i] + column2[i];
                newDuration.append(fullDuration);
            else:
                newDuration.append(currentColumn[0])

        return newDuration;




    def writeCsvFile(self, allColumns):

        name = 'completed/complete-'+fileName.split('/')[1];

        with open(name, 'w', newline='') as csvfile:
            csvWriter = csv.writer(
                csvfile,
                delimiter=',',
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL
                )
            
            rows=list(allColumns)
            rowLength = len(rows[0])
            index = 0
            column = []

            while index < rowLength:
                for i, val in enumerate(rows):
                    column.append(rows[i][index])
                    if i == len(rows) - 1:
                        index += 1
                        csvWriter.writerow(column)
                        column = []
                        print('\n')
                        break
    
    storeColumns = []



    def openCsvFile(self, file):

        rows = []
        column = []

        with open(file, newline='', encoding='UTF-8') as csvFile:
            csvReader = csv.reader(
                csvFile,
                delimiter=',',
                quotechar='"',
                skipinitialspace=False)

            rows=list(csvReader)
            rowLength = len(rows[0])
            index = 0

            while index < rowLength:
                for i, val in enumerate(rows):
                    column.append(rows[i][index])
                    if i == len(rows) - 1:
                        index += 1
                        self.convertByColumn(column)
                        column = []
                        print('\n')
                        break

        
fileName = 'csv/sample.csv'
parser().openCsvFile(fileName)