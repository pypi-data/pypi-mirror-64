#!/usr/bin/env python

"""
This project allows interaction with the Trello application via the command line.
This project is written in python scripting language and implements the web service rest api to ensure interaction with the Trello application.
This project contains four features which are:
*Add a list to a board.
*Add a Trello card to a column.
*Be able to label on a card (X column of board Y).
*Be able to comment on a card (X column of board Y).
"""

import argparse
import sys
# Install requests library if import of it fails
try:
	import requests
except ImportError:
	print ("Trying to Install required module: requests\n")
	# Try to install requests module if not present
	os.system('python -m pip install requests')
	# Import required module again ( for global access)
	import requests

class TrelloInterractorCLI(object):
	FAIL, SUCCESS = 0, 1
	"""
	This class contains the features of the project
	"""
	def __init__(self, mode = 'normal', test_param = None):
		"""
		defines the way of executing the code in the command line.
		First: the funtion name
		Second: the parameters	
		"""
		self.status = self.FAIL
		parseArgumentOk =self.parse_args(mode, test_param)
		# use dispatch pattern to invoke method with same name if parsing argument was successful
		if(parseArgumentOk):
			getattr(self, self.command)()

	def parse_args(self, mode, test_param):
		"""
		Defines the way of executing the code in the command line
		in normal mode and simulating arguments values in case
		of unit-test mode.
		"""
		returnValue = True
		if mode == 'unittest':
			if test_param is None:
				print("Missing test parameters !!!")
				sys.exit()
			self.command = test_param['command']
			if (self.command == "addList"):
				self.boardId = test_param['board_id']
				self.listName = test_param['list_name']
			elif (self.command == "addCard"):
				self.listId = test_param['list_id']
				self.cardName = test_param['card_name']
				self.cardDescription = test_param['card_desc']
			elif (self.command == "labelCard"):
				self.cardId = test_param['card_id']
				self.labelId = test_param['label_id']			
			elif (self.command == "commentCard"):
				self.cardId = test_param['card_id']
				self.commentText = test_param['comment_text']			 
			else:
				returnValue = False

			self.key = test_param['app_key']
			self.token = test_param['app_token']
		else:
			parser = argparse.ArgumentParser(
			description='Project interaction with trello',
			usage='''trello <command> [<args>]

			The only available trello commands for now are:
				addList		 Add a new list to an existing board
				addCard		 Add a new card to an existing list
				labelCard	 Add a label to an existing card
				commentCard	 Add a comment to an existing card
			''')
			parser.add_argument('command', help='Subcommand to run')
			# parse_args defaults to [1:] for args, but you need to
			# exclude the rest of the args too, or validation will fail
			args = parser.parse_args(sys.argv[1:2])
			if not hasattr(self, args.command):
				print ("Unrecognized command")
				parser.print_help()
				exit(1)

			self.command = args.command
			if (self.command == "addList"):
				parser = argparse.ArgumentParser(
					description='Add a trello list to an existing board')
				parser.add_argument('-i','--board_id',	required=True, help='trello board id')
				parser.add_argument('-n','--list_name', type=str ,required=True, help='trello name list of board, in case of multiple string please put it between two " "')
				parser.add_argument('-k', '--app_key' , required=True, help='trello key')
				parser.add_argument('-t', '--app_token' , required=True, help='trello token')
				# TWO argvs, ie the command (git) and the subcommand (commit)
				args = parser.parse_args(sys.argv[2:])

				self.boardId = args.board_id
				self.listName = args.list_name
				self.key = args.app_key
				self.token = args.app_token
			elif (self.command == "addCard"):
				parser = argparse.ArgumentParser(
					description='Add a trello card to an existing list')
				parser.add_argument('-i','--list_id', required=True, help='trello list id')
				parser.add_argument('-n', '--card_name', type=str, required=True, help='trello card name')
				parser.add_argument('-d', '--card_desc', type=str, required=False, help='trello card description')
				parser.add_argument('-k', '--app_key' , required=True, help='trello key')
				parser.add_argument('-t', '--app_token' , required=True, help='trello token')
				args = parser.parse_args(sys.argv[2:])

				self.listId = args.list_id
				self.cardName = args.card_name
				self.cardDescription = args.card_desc
				self.key = args.app_key
				self.token = args.app_token
			elif (self.command == "labelCard"):
				parser = argparse.ArgumentParser(
					description='Add a trello label to an existing card')
				parser.add_argument('-c','--card_id', required=True)
				parser.add_argument('-l','--label_id', required=True)
				parser.add_argument('-k', '--app_key' , required=True)
				parser.add_argument('-t', '--app_token' , required=True)
				args = parser.parse_args(sys.argv[2:])

				self.cardId = args.card_id
				self.labelId = args.label_id
				self.key = args.app_key
				self.token = args.app_token			   
			elif (self.command == "commentCard"):
				parser = argparse.ArgumentParser(
					description='Add a comment to an existing card')
				parser.add_argument('-i','--id_card', required=True)
				parser.add_argument('-c','--comment_text', type=str, required=True)
				parser.add_argument('-k', '--app_key' , required=True)
				parser.add_argument('-t', '--app_token' , required=True)
				args = parser.parse_args(sys.argv[2:])

				self.cardId = args.card_id
				self.commentText = args.comment_text
				self.key = args.app_key
				self.token = args.app_token			   
			else:
				print("Invalid command !!!")
				returnValue = False
				sys.exit(1)
		return returnValue

	def addList(self):
		"""
		Allows adding a trello list to a board.
		To add the list the following parameters are required 
		board_id ---> The board identifier to which we will add a list
		list_name ---> The name of the list to be added
		app_key ---> The key of the application
		app_token ---> The token of the application
		These parameters are entered via the command line
		Example of command to add a list to a board: 
		python trello.py addList -i 5e7a49129485c7470316045a -n "Coding features" -k e84fd113f9554e16c58ac2652984eef4 -t 21c74bc55f315e804cd455935b4e91c17a9fb38670bf26ae9a84e62a20acc358
		"""
		baseRestServiceUrl = "https://trello.com/1/boards/"

		PostData = {'name' : self.listName, 'key' : self.key, 'token' : self.token}
		postUrl = baseRestServiceUrl+self.boardId+"/lists"
		try:
			responseAddList = requests.post(url = postUrl, data = PostData)
			if responseAddList.ok:
				self.status = self.SUCCESS
		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)
		except requests.exceptions.RequestException as err:
			print ("OOps: Something Else",err)

	def addCard(self):
		"""
		Allows adding a card to a column.
		To be able to add a card the following parameters are required
		list_id ---> The list identifier to which we will add a card
		card_name ---> The name of the card to be added
		card_desc ---> The dexcription of the card which is not required
		app_key ---> The key of the application
		app_token ---> The token of the application
		These parameters are entered via the command line
		Example of command to add a card to a column(a list).
		C:\trello>python trello.py addCard -i 5e7d0c995478192bc367c2d2 -n "AddCardFeature" -d "add a card to a list" -k e84fd113f9554e16c58ac2652984eef4 -t 21c74bc55f315e804cd455935b4e91c17a9fb38670bf26ae9a84e62a20acc358
		"""
		baseRestServiceUrl = "https://api.trello.com/1/lists/"

		PostData = {'name' : self.cardName, 'desc' : self.cardDescription , 'key' : self.key, 'token' : self.token}
		postUrl = baseRestServiceUrl+self.listId+"/cards"
		try:
			responseAddCard = requests.post(url = postUrl, data = PostData)
			if responseAddCard.ok:
				self.status = self.SUCCESS
		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)
		except requests.exceptions.RequestException as err:
			print ("OOps: Something Else",err)

	def labelCard(self):
		"""
		Allows to label on a a card.
		To be able to label on a card the following parameters are required
		card_id ---> The identifier of the card to which we will add a label
		label_id ---> The identifier of the label color to be added
		app_key ---> The key of the application
		app_token ---> The token of the application
		These parameters are entered via the command line
		Example of command to label on a card.
		C:\trello>C:\trello>python trello.py labelCard -c 5e7d0f97b042ac75bd0e4137 -l 5e7a49127669b22549aa63b6	-k e84fd113f9554e16c58ac2652984eef4 -t 21c74bc55f315e804cd455935b4e91c17a9fb38670bf26ae9a84e62a20acc358
		"""
		baseRestServiceUrl = "https://api.trello.com/1/cards/"

		PostData = {'value' : self.labelId, 'key' : self.key, 'token' : self.token}
		postUrl = baseRestServiceUrl+self.cardId+"/idLabels"
		try:
			responseLabelCard = requests.post(url = postUrl, data = PostData)
			if responseLabelCard.ok:
				self.status = self.SUCCESS
		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)
		except requests.exceptions.RequestException as err:
			print ("OOps: Something Else",err)

	def commentCard(self):
		"""
		Allows to comment on a card.
		To be able to comment on a card the following parameters are required
		card_id ---> The identifier of the card to which we will add a label
		comment_text ---> The comment text to be added
		app_key ---> The key of the application
		app_token ---> The token of the application
		These parameters are entered via the command line
		Example of command to comment on a card.
		C:\trello>python trello.py commentCard -i 5e7d0f97b042ac75bd0e4137 -c "must be ended this day"	-k e84fd113f9554e16c58ac2652984eef4 -t 21c74bc55f315e804cd455935b4e91c17a9fb38670bf26ae9a84e62a20acc358
		"""
		baseRestServiceUrl = "https://api.trello.com/1/cards/"

		PostData = {'text' : self.commentText, 'key' : self.key, 'token' : self.token}
		postUrl = baseRestServiceUrl+self.cardId+"/actions/comments"
		try:
			responseCommentCard = requests.post(url = postUrl, data = PostData)
			if responseCommentCard.ok:
				self.status = self.SUCCESS
		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)
		except requests.exceptions.RequestException as err:
			print ("OOps: Something Else",err)

	def getStatus(self):
		"""
		Returns the status of last class invokation.
		This function is added to be able to do unit test. 
		"""
		print("status= %s" % self.status)
		return self.status

if __name__ == '__main__':
	trelloInterractorCli = TrelloInterractorCLI()