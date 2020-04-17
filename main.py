import pathlib
import random
from datetime import datetime


class Transaction():

    def getTransactionNumber(self):
        try:
            transactionInfoRead = open("Transactions.txt", "r")
            fileLines = transactionInfoRead.readlines()
            maxCount = 0

            for line in fileLines:
                if(line is not None and line.strip() != ''):
                    line = line.split(",")
                    line = [x.strip() for x in line]

                    if(maxCount < int(line[0])):
                        maxCount = int(line[0])
            transactionInfoRead.close()
            return (maxCount + 1)
        except Exception:
            print("Error in getTransactionNumber")

    def record_transaction(self, accountFrom, amount, trasactionType, accountTo):
        print("Recording trasaction....")
        transactionNumber = self.getTransactionNumber()

        try:
            transactionInfo = open("Transactions.txt", "a+")
            transactionInfo.write("%d,%s,%f,%s,%d,%d\r\n" % (transactionNumber, trasactionType, float(amount), datetime.now(), int(accountFrom), int(accountTo)))
            transactionInfo.close()
        except Exception:
            print("Error in record_transaction")

    def print_transaction(self, accountFrom):
        try:
            transactionInfoRead = open("Transactions.txt", "r")
            fileLines = transactionInfoRead.readlines()

            for line in fileLines:
                if(line is not None and line.strip() != ''):
                    line = line.split(",")
                    line = [x.strip() for x in line]

                    if(int(accountFrom) == int(line[4])):
                        print("Transaction number : " + str(line[0]))
                        print("Transaction type : " + line[1])
                        print("Transaction amount : " + line[2])
                        print("Transaction date : " + str(line[3]))
                        print("Transaction from account : " + str(line[4]))
                        print("Transaction to account : " + str(line[5]))
                        print("\n")
            transactionInfoRead.close()
        except Exception:
            print("Error in print_transaction")


class Account(Transaction):

    def show_menu(self, userInfo):
        print("-------------------Enter Account details---------------------")

        while True:
            print("Choose account type")
            print("\t1. Savings")
            print("\t2. Checking")
            try:
                self.accountType = int(input("Enter account type: "))

                if(self.accountType > 0):
                    if(self.accountType == 1 or self.accountType == 2):
                        break
                else:
                    print("\tInvalid option selected...Try again")
            except ValueError:
                print("\tInvalid option selected...Try again")

        while True:
            try:
                self.balance = float(input("Enter initial balance: "))
                break
            except ValueError:
                print("\tIncorrect balance entered...Try again")
        self.lastAccessed = datetime.now()
        self.accountNumber = userInfo.accountNumber
        self.customerNumber = userInfo.customerNumber

    def createNewAccount(self):
        try:
            print("Creating new account.....")
            accounInfo = open("Accounts.txt", "a+")
            accounInfo.write("%d,%s,%f,%s,%d\r\n" % (self.accountNumber, "Savings" if(self.accountType == 1) else "Checking", self.balance, self.lastAccessed, self.customerNumber))
            self.record_transaction(self.accountNumber, self.balance, "Deposite", self.accountNumber)
            accounInfo.close()
            return 1
        except Exception:
            print("Error in createNewAccount")
            return 0

    def showTransactions(self, customerNumber):
        try:
            accounInfo = open("Accounts.txt", "r")
            fileLines = accounInfo.readlines()

            for line in fileLines:
                if(line is not None and line.strip() != ''):
                    line = line.split(",")
                    line = [x.strip() for x in line]

                    if(customerNumber == int(line[4])):
                        self.accountNumber = line[0]
                        self.print_transaction(self.accountNumber)

            accounInfo.close()
        except Exception:
            print("Error in showTransactions")

    def showAccountDetails(self, customerNumber):
        try:
            accounInfo = open("Accounts.txt", "r")
            fileLines = accounInfo.readlines()

            for line in fileLines:
                if(line is not None and line.strip() != ''):
                    line = line.split(",")
                    line = [x.strip() for x in line]

                    if(customerNumber == int(line[4])):
                        print("Account number : " + line[0])
                        print("Account type : " + line[1])
                        print("Account balance : " + line[2])
                        print("Account last accessed : " + line[3])
                        print("\n")

            accounInfo.close()
        except Exception:
            print("Error in showAccountDetails")

    def getAllAccountInfo(self):
        try:
            accounInfo = open("Accounts.txt", "r")
            fileLines = accounInfo.readlines()
            accounInfo.close()
            return fileLines
        except Exception:
            print("Error in getAllAccountInfo")

    def depositeMoney(self, amount, customerNumber):
        accountsInfo = self.getAllAccountInfo()

        for i in range(0, len(accountsInfo)):
            line = accountsInfo[i].split(",")
            line = [x.strip() for x in line]

            if(int(customerNumber) == int(line[4])):
                self.accountNumber = line[0]
                line[2] = str(float(line[2]) + float(amount))
                line[3] = str(datetime.now())
                accountsInfo[i] = ",".join(line)
                self.record_transaction(self.accountNumber, amount, "Deposite", self.accountNumber)

        try:
            print("Depositing money.....")
            accounInfo = open("Accounts.txt", "w+")

            for line in accountsInfo:
                accounInfo.write(line)
            accounInfo.write("\r\n")
            accounInfo.close()
        except Exception:
            print("Error in depositeMoney")

    def withdrawMoney(self, amount, customerNumber):
        accountsInfo = self.getAllAccountInfo()

        for i in range(0, len(accountsInfo)):
            line = accountsInfo[i].split(",")
            line = [x.strip() for x in line]

            if(int(customerNumber) == int(line[4])):
                self.accountNumber = line[0]

                if(float(line[2]) > float(amount)):
                    line[2] = str(float(line[2]) - float(amount))
                else:
                    print("Insufficient fund...")
                    return
                line[3] = str(datetime.now())
                accountsInfo[i] = ",".join(line)
                self.record_transaction(self.accountNumber, amount, "Withdrawal", self.accountNumber)

        try:
            print("Withdrawing money.....")
            accounInfo = open("Accounts.txt", "w+")

            for line in accountsInfo:
                accounInfo.write(line)
            accounInfo.write("\r\n")
            accounInfo.close()
        except Exception:
            print("Error in withdrawMoney")

    def transferMoney(self, accountFromNumber, accountToNumber, amount):
        accountsInfo = self.getAllAccountInfo()

        for i in range(0, len(accountsInfo)):
            line = accountsInfo[i].split(",")
            line = [x.strip() for x in line]

            if(int(accountFromNumber) == int(line[0])):
                if(float(line[2]) > float(amount)):
                    line[2] = str(float(line[2]) - float(amount))
                else:
                    print("Insufficient fund...")
                    return
                line[3] = str(datetime.now())
                accountsInfo[i] = ",".join(line)
                self.record_transaction(accountFromNumber, amount, "Withdrawal", accountToNumber)
            if(int(accountToNumber) == int(line[0])):
                line[2] = str(float(line[2]) + float(amount))
                accountsInfo[i] = ",".join(line)
                self.record_transaction(accountFromNumber, amount, "Deposite", accountToNumber)

        try:
            print("Transfering money.....")
            accounInfo = open("Accounts.txt", "w+")

            for line in accountsInfo:
                accounInfo.write(line + "\r\n")
            accounInfo.close()
        except Exception:
            print("Error in withdrawMoney")


class UserInfo():

    def check_user(self):
        try:
            userinfo = open("userinfo.txt", "r")
            fileLines = userinfo.readlines()
            accountNumberList = []
            maxCount = 0

            for line in fileLines:
                if(line is not None and line.strip() != ''):
                    line = line.split(",")
                    line = [x.strip() for x in line]
                    # if(self.firstName == line[1] and self.lastName == line[2] and self.SSN == line[3]):
                    #     print("User exist")
                    #     return 0
                    if(maxCount < int(line[0])):
                        maxCount = int(line[0])
                    accountNumberList.append(int(line[5]))

            while(self.accountNumber in accountNumberList):
                self.accountNumber = random.randint(0, 99999999999999)

            userinfo.close()
            self.customerNumber = maxCount + 1
            return 1
        except Exception:
            print("Error in check_user")

    def createNewUser(self):
        try:
            print("Creating new user.....")
            userinfo = open("userinfo.txt", "a+")
            userinfo.write("%d,%s,%s,%s,%s,%d\r\n" % (self.customerNumber, self.firstName, self.lastName, self.SSN, self.address, self.accountNumber))
            userinfo.close()
            return 1
        except Exception:
            print("Error in createNewUser")
            return 0

    def openNewAccount(self, customerNumber):
        accountsInfo = self.getAllAccountInfo()

        for i in range(0, len(accountsInfo)):
            line = accountsInfo[i].split(",")
            line = [x.strip() for x in line]

            if(int(customerNumber) == int(line[4])):
                self.accountNumberList = line[0]
                accountsInfo[i] = ",".join(line)
                self.record_transaction(self.accountNumber, amount, "Deposit", self.accountNumber)

        try:
            print("Depositing money.....")
            accounInfo = open("Accounts.txt", "w+")

            for line in accountsInfo:
                accounInfo.write(line)
            accounInfo.close()
        except Exception:
            print("Error in depositeMoney")

    def show_menu(self):
        print("-------------------Enter user details---------------------")
        self.firstName = str(input("Enter your first name: "))
        self.lastName = str(input("Enter your last name: "))
        self.SSN = str(input("Enter SSN: "))
        self.address = str(input("Enter your address: "))
        self.accountNumber = random.randint(0, 99999999999999)

    def checkAccountNumber(self, accountNumber):
        try:
            userinfo = open("userinfo.txt", "r")
            fileLines = userinfo.readlines()

            for line in fileLines:
                if(line is not None and line.strip() != ''):
                    line = line.split(",")
                    line = [x.strip() for x in line]

                    if(str(accountNumber) in line[5:]):
                        self.customerNumber = int(line[0])
                        self.firstName = line[1]
                        self.lastName = line[2]
                        self.SSN = line[3]
                        self.address = line[4]
                        self.accountNumbers = line[5:]
                        return True
            userinfo.close()
            return False
        except Exception:
            print("Error in checkAccountNumber")
            return False

    def showUserDetails(self):
        print("First name : " + self.firstName)
        print("Last name : " + self.lastName)
        print("SSN : " + self.SSN)
        print("Accounts : " + str(self.accountNumbers))

    def login(self):
        print("-------------------Enter user details---------------------")

        while True:
            try:
                accountNumber = int(input("Enter your account number: "))
                doExist = self.checkAccountNumber(accountNumber)

                if(doExist is False):
                    print("Account number entered do not exist...Try again")
                    return 0
                else:
                    print("Logged in successfully")
                    return accountNumber
                break
            except ValueError:
                print("\tInvalid account number entered...Try again")
                return 0

    def showLoginMenu(self, accountFromNumber):
        optionSelected = None
        print("Choose one of the following options to proceed")
        print("\t1. Show user details")
        print("\t2. Show account details")
        print("\t3. Show transactions")
        print("\t4. Deposite money")
        print("\t5. Withdraw money")
        print("\t6. Transfer money")
        print("\t7. Quit")

        while True:
            try:
                optionSelected = int(input("Enter choice: "))

                if(optionSelected > 0):
                    if(optionSelected in range(1, 8, 1)):
                        break
                else:
                    print("\tInvalid option selected...Try again")
            except ValueError:
                print("\tInvalid option selected...Try again")

        if(optionSelected == 1):
            self.showUserDetails()
        elif(optionSelected == 2):
            account = Account()
            account.showAccountDetails(self.customerNumber)
        elif(optionSelected == 3):
            account = Account()
            account.showTransactions(self.customerNumber)
        elif(optionSelected == 4 or optionSelected == 5):
            amount = 0

            while True:
                try:
                    if(optionSelected == 4):
                        amount = float(input("Enter amount to deposite: "))
                    else:
                        amount = float(input("Enter amount to withdraw: "))

                    if(amount > 0):
                        break
                    else:
                        print("\tIncorrect amount entered...Try again")
                except ValueError:
                    print("\tIncorrect amount entered...Try again")
            account = Account()

            if(optionSelected == 4):
                account.depositeMoney(amount, self.customerNumber)
            else:
                account.withdrawMoney(amount, self.customerNumber)
        elif(optionSelected == 6):
            userTo = UserInfo()

            while True:
                accountToNumber = int(input("Enter account number of benificery : "))

                if(userTo.checkAccountNumber(accountToNumber) is False):
                    print("Invalid benificery account number")
                else:
                    break

            while True:
                try:
                    amount = float(input("Enter amount to transfer: "))

                    if(amount > 0):
                        break
                    else:
                        print("\tIncorrect amount entered...Try again")
                except ValueError:
                    print("\tIncorrect amount entered...Try again")

            accountFrom = Account()
            accountFrom.transferMoney(accountFromNumber, accountToNumber, amount)
        elif(optionSelected == 7):
            exit(0)


def createNewAccountMenu():
    print("-------------------Welcome to account creation page---------------------")
    newUser = UserInfo()
    newUser.show_menu()
    newUser.check_user()
    newUser.createNewUser()
    account = Account()
    account.show_menu(newUser)
    account.createNewAccount()
    print("Account created with account number : " + str(account.accountNumber))


def createLoginMenu():
    print("-------------------Welcome to account login page---------------------")
    newUser = UserInfo()
    accountNumber = newUser.login()
    if(accountNumber > 0):
        while True:
            newUser.showLoginMenu(accountNumber)


def createMenu():
    optionSelected = None

    while True:
        print("Choose one of the following options to proceed")
        print("\t1. New User! Open an account")
        print("\t2. Continue to login")
        try:
            optionSelected = int(input("Enter choice: "))

            if(optionSelected > 0):
                if(optionSelected == 1 or optionSelected == 2):
                    break
            else:
                print("\tInvalid option selected...Try again")
        except ValueError:
            print("\tInvalid option selected...Try again")

    if(optionSelected == 1):
        createNewAccountMenu()
    elif(optionSelected == 2):
        createLoginMenu()


def startmenu():
    print("****************************************")
    print("\t\tWelcome to Goslee Bank")
    print("\t\tCEO Trenisha Goslee")
    print("****************************************")
    createMenu()


startmenu()
