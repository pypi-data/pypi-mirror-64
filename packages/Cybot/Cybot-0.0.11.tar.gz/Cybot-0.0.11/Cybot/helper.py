from pprint import pprint

def e2e(msg):
	api  = {'chat':{'image':{}}, "message":{}, "type": "new_conversation"}
	chat = msg['chat']['contact']
	api['chat']['title'] = chat['pushname']
	api['chat']['id']    = chat['id']['_serialized']
	api['chat']['isBusiness'] = chat['isBusiness']
	api['chat']['isMe'] = chat['isMe']
	api['chat']['image'] = chat['profilePicThumbObj']['imgFull']
	api['timestamp'] = msg['timestamp']
	return api

def serialize(msg):
	pprint(msg)
	if msg['type'] == 'e2e_notification':
		return e2e(msg)
	
	# Chat
	if msg['chat']['isGroup'] == False:
		if msg['type'] == 'chat':
			api = {"chat":{"image":{}}, "message":{}, 'type': 'chat',"quoted":{}}
		if msg['type'] == 'image':
			api = {"chat":{"image":{}}, "message":{}, "image":{}, 'type': 'image',"quoted":{}}
		if msg['type'] == 'video':
			api = {"chat":{"image":{}}, "message":{}, "video":{}, 'type':'video',"quoted":{}}
		if msg['type'] == 'ptt':
			api = {"chat":{"image":{}}, "message":{}, "voice":{},'type':'voice',"quoted":{}}
		if msg['type'] == 'audio':
			api = {"chat":{"image":{}}, "message":{}, "audio":{},'type':'audio',"quoted":{}}
		if msg['type'] == 'location':
			api = {"chat":{"image":{}}, "message":{}, "location":{},'type':'location',"quoted":{}}
		if msg['type'] == 'vcard':
			api = {"chat":{"image":{}}, "message":{}, "contact":{},'type':'contact',"quoted":{}}
		if msg['type'] == 'document':
			api = {"chat":{"image":{}}, "message":{}, "document":{},'type':'document',"quoted":{}}
		if msg['type'] == 'sticker':
			api = {"chat":{"image":{}}, "message":{}, "sticker":{},'type':'sticker',"quoted":{}}

		if 'quotedMsg' in msg:
			pprint(msg)
			api['quoted']['text']=  msg['quotedMsg']['body']
			api['quoted']['id']=  msg['quotedParticipant']['_serialized']
		# Basic
		try:api['ack']            = msg['ack']
		except:pass
		if msg['type'] == 'chat':
			api['body']  = msg['body']
		try:api['broadcast']        = msg['broadcast']
		except:pass
		try:api['isGroup']          = msg['chat']['isGroup']
		except:pass
		try:api['isReadOnly']       = msg['chat']['isReadOnly']
		except:pass
		try:api['isReadOnly']       = None
		except:pass
		try:api['message']['type']  = msg['chat']['kind']
		except:pass
		try:api['isForwarded']      = msg['isForwarded']
		except:pass
		try:api['star']             = msg['star']
		except:pass
		try:api['timestamp']        = msg['timestamp']
		except:pass
		#___________________________________________________________________
		
		# CHAT
		chat = msg['chat']['contact']
		api['chat']['title']       = chat['formattedName']
		api['chat']['id']          = chat['id']['_serialized']
		api['chat']['isBusiness']  = chat['isBusiness']
		api['chat']['isEnterprise']= chat['isEnterprise']
		api['chat']['isMe']		   = chat['isMe']
		api['chat']['isMyContact'] = chat['isMyContact']
		if len(chat['labels']) >1:
			api['labels'] = chat['labels']
		api['chat']['image']['full'] = chat['profilePicThumbObj']['imgFull']
		api['chat']['image']['eurl'] = chat['profilePicThumbObj']['eurl']
		api['chat']['image']['img'] = chat['profilePicThumbObj']['img']
		#______________________________________________________________________

		 # IMAGE
		if msg['type'] == 'image':
			api['body']  = None
			api['image']['body']      = msg['body']
			api['image']['clientUrl'] = msg['clientUrl']
			api['image']['content']   = msg['content']
			api['image']['directPath']= msg['directPath']
			api['image']['filehash']  = msg['filehash']
			api['image']['height']    = msg['height']
			api['image']['width']     = msg['mediaData']['fullWidth']
			api['image']['mimetype']  = msg['mediaData']['mimetype']
			api['image']['preview']   = msg['mediaData']['preview']
			api['image']['mediaKey']  = msg['mediaKey']
			api['image']['size']      = msg['size']
			api['image']['uploadhash']= msg['uploadhash']
		#_______________________________________________________________________

		# VIDEO
		if msg['type'] == 'video':
			api['body']  = None
			api['video']['body']      = msg['body']
			api['video']['clientUrl'] = msg['clientUrl']
			api['video']['content']   = msg['content']
			api['video']['directPath']= msg['directPath']
			api['video']['filehash']  = msg['filehash']
			api['video']['height']    = msg['height']
			api['video']['width']     = msg['mediaData']['fullWidth']
			api['video']['mimetype']  = msg['mediaData']['mimetype']
			api['video']['preview']   = msg['mediaData']['preview']
			api['video']['mediaKey']  = msg['mediaKey']
			api['video']['size']      = msg['size']
			api['video']['uploadhash']= msg['uploadhash']

		# Audio message
		if msg['type'] == 'ptt':
			api['body'] = None
			api['voice']['clientUrl']  = msg['clientUrl']
			api['voice']['directPath'] = msg['directPath']
			api['voice']['duration']   = msg['duration']
			api['voice']['filehash']   = msg['filehash']
			api['voice']['mimetype']   = msg['mediaData']['mimetype']
			api['voice']['size']       = msg['mediaData']['size']
			api['voice']['mediaKey']   = msg['mediaKey']
			api['voice']['mimetype']   = msg['mimetype']
			api['voice']['uploadhash'] = msg['uploadhash']

		# Music message
		if msg['type'] == 'audio':
			api['body'] = None
			api['audio']['clientUrl']  = msg['clientUrl']
			api['audio']['directPath'] = msg['directPath']
			api['audio']['duration']   = msg['duration']
			api['audio']['filehash']   = msg['filehash']
			api['audio']['size']       = msg['mediaData']['size']
			api['audio']['mediaKey']   = msg['mediaKey']
			api['audio']['mimetype']   = msg['mimetype']
			api['audio']['uploadhash'] = msg['uploadhash']
		
		# location message
		if msg['type'] == 'location':
			api['location']['body']    = msg['body']
			api['location']['content'] = msg['content']
			api['location']['lat']     = msg['lat']
			api['location']['lng']     = msg['lng']

		# Contact message
		if msg['type'] == 'vcard':
			api['contact']['name']    = msg['subtype']
			api['contact']['content'] = msg['content']

		# Document message
		if msg['type'] == 'document':
			api['document']['body']       = msg['body']
			api['document']['caption']    = msg['caption']
			api['document']['clientUrl']  = msg['clientUrl']
			api['document']['directPath'] = msg['directPath']
			api['document']['filehash']   = msg['filehash']
			api['document']['filename']   = msg['filename']
			api['document']['preview']    = msg['mediaData']['preview']
			api['document']['size']       = msg['mediaData']['size']
			api['document']['mediaKey']   = msg['mediaKey']
			api['document']['mimetype']   = msg['mimetype']
			api['document']['uploadhash'] = msg['uploadhash']

		if msg['type'] == 'sticker':
			api['sticker']['clientUrl']  = msg['clientUrl']
			api['sticker']['directPath'] = msg['directPath']
			api['sticker']['filehash']   = msg['filehash']
			api['sticker']['mediaKey']   = msg['mediaKey']
			api['sticker']['mimetype']   = msg['mimetype']
			api['sticker']['uploadhash'] = msg['uploadhash']
	

	## GROUP
	elif msg['chat']['isGroup'] == True:
		if msg['type'] == 'gp2':
			# add ou removed members
			api = {"chat":{"image":{}}, "from":{}, "message":{}, "member":{},'type': {}}
			api['chat']['title'] = msg['chat']['contact']['formattedName']
			api['chat']['id']    = msg['chat']['contact']['id']['_serialized']
			api['chat']['image'] = msg['chat']['contact']['profilePicThumbObj']
			api['chat']['owner'] = msg['chat']['groupMetadata']['owner']['_serialized']
			api['chat']['participants'] = msg['chat']['groupMetadata']['participants']
			api['chat']['isReadOnly'] = msg['chat']['isReadOnly']
			api['from']['name']       = msg['sender']['formattedName']
			api['from']['id']         = msg['sender']['id']['_serialized']
			api['from']['isBusiness'] = msg['sender']['isBusiness']
			api['from']['isMe']       = msg['sender']['isMe']
			try:api['from']['photo']      = msg['sender']['eurl']
			except:pass
			api['member']		  = msg['from']['_serialized']
			api['type'] = msg['subtype']

		# conversation group chat
		if msg['type'] == 'chat':
			api = {"chat":{"image":{}}, "from":{}, "message":{}, "member":{},'type': 'chat',"quoted":{}}

		else:
			if msg['type'] == 'image':
				api = {"chat":{"image":{}},"from":{}, "message":{},"member":{}, "image":{}, 'type':'image',"quoted":{}}
			if msg['type'] == 'video':
				api = {"chat":{"image":{}},"from":{}, "message":{},"member":{} ,"video":{},'type':'video',"quoted":{}}
			if msg['type'] == 'ptt':
				api = {"chat":{"image":{}},"from":{}, "message":{},"member":{} ,"voice":{},'type':'voice',"quoted":{}}
			if msg['type'] == 'audio':
				api = {"chat":{"image":{}},"from":{}, "message":{},"member":{} ,"audio":{},'type':'audio',"quoted":{}}
			if msg['type'] == 'location':
				api = {"chat":{"image":{}},"from":{}, "message":{},"member":{} ,"location":{},'type':'location',"quoted":{}}
			if msg['type'] == 'vcard':
				api = {"chat":{"image":{}},"from":{}, "message":{},"member":{} ,"contact":{},'type':'contact',"quoted":{}}
			if msg['type'] == 'document':
				api = {"chat":{"image":{}},"from":{}, "message":{},"member":{} ,"document":{},'type':'document',"quoted":{}}
			if msg['type'] == 'sticker':
				api = {"chat":{"image":{}},"from":{},  "message":{}, "member":{} ,"sticker":{},"sticker":{},'type':'sticker',"quoted":{}}
			# CHAT
			

			if msg['type'] == 'image':
				api['body']  = None
				api['image']['body']      = msg['body']
				api['image']['clientUrl'] = msg['clientUrl']
				api['image']['content']   = msg['content']
				api['image']['directPath']= msg['directPath']
				api['image']['filehash']  = msg['filehash']
				api['image']['height']    = msg['height']
				api['image']['width']     = msg['mediaData']['fullWidth']
				api['image']['mimetype']  = msg['mediaData']['mimetype']
				api['image']['preview']   = msg['mediaData']['preview']
				api['image']['mediaKey']  = msg['mediaKey']
				api['image']['size']      = msg['size']
				api['image']['uploadhash']= msg['uploadhash']
		#_______________________________________________________________________

		# VIDEO
			if msg['type'] == 'video':
				api['body']  = None
				api['video']['body']      = msg['body']
				api['video']['clientUrl'] = msg['clientUrl']
				api['video']['content']   = msg['content']
				api['video']['directPath']= msg['directPath']
				api['video']['filehash']  = msg['filehash']
				api['video']['height']    = msg['height']
				api['video']['width']     = msg['mediaData']['fullWidth']
				api['video']['mimetype']  = msg['mediaData']['mimetype']
				api['video']['preview']   = msg['mediaData']['preview']
				api['video']['mediaKey']  = msg['mediaKey']
				api['video']['size']      = msg['size']
				api['video']['uploadhash']= msg['uploadhash']

			# Audio message
			if msg['type'] == 'ptt':
				api['body'] = None
				api['voice']['clientUrl']  = msg['clientUrl']
				api['voice']['directPath'] = msg['directPath']
				api['voice']['duration']   = msg['duration']
				api['voice']['filehash']   = msg['filehash']
				api['voice']['mimetype']   = msg['mediaData']['mimetype']
				api['voice']['size']       = msg['mediaData']['size']
				api['voice']['mediaKey']   = msg['mediaKey']
				api['voice']['mimetype']   = msg['mimetype']
				api['voice']['uploadhash'] = msg['uploadhash']

			# Music message
			if msg['type'] == 'audio':
				api['body'] = None
				api['audio']['clientUrl']  = msg['clientUrl']
				api['audio']['directPath'] = msg['directPath']
				api['audio']['duration']   = msg['duration']
				api['audio']['filehash']   = msg['filehash']
				api['audio']['size']       = msg['mediaData']['size']
				api['audio']['mediaKey']   = msg['mediaKey']
				api['audio']['mimetype']   = msg['mimetype']
				api['audio']['uploadhash'] = msg['uploadhash']
			
			# location message
			if msg['type'] == 'location':
				api['location']['body']    = msg['body']
				api['location']['content'] = msg['content']
				api['location']['lat']     = msg['lat']
				api['location']['lng']     = msg['lng']

			# Contact message
			if msg['type'] == 'vcard':
				api['contact']['name']    = msg['subtype']
				api['contact']['content'] = msg['content']

			# Document message
			if msg['type'] == 'document':
				api['document']['body']       = msg['body']
				api['document']['caption']    = msg['caption']
				api['document']['clientUrl']  = msg['clientUrl']
				api['document']['directPath'] = msg['directPath']
				api['document']['filehash']   = msg['filehash']
				api['document']['filename']   = msg['filename']
				api['document']['preview']    = msg['mediaData']['preview']
				api['document']['size']       = msg['mediaData']['size']
				api['document']['mediaKey']   = msg['mediaKey']
				api['document']['mimetype']   = msg['mimetype']
				api['document']['uploadhash'] = msg['uploadhash']

			if msg['type'] == 'sticker':
				api['sticker']['clientUrl']  = msg['clientUrl']
				api['sticker']['directPath'] = msg['directPath']
				api['sticker']['filehash']   = msg['filehash']
				api['sticker']['mediaKey']   = msg['mediaKey']
				api['sticker']['mimetype']   = msg['mimetype']
				api['sticker']['uploadhash'] = msg['uploadhash']
		try:api['body'] = msg['body']
		except:pass
		chat = msg['chat']['contact']
		api['chat']['id']     = chat['id']['_serialized']
		api['chat']['title']  = chat['formattedName']
		api['chat']['isGroup']= msg['chat']['isGroup']
		api['chat']['photo']  = chat['profilePicThumbObj']['eurl']
		chat = msg['chat']['groupMetadata']
		api['chat']['owner']  = chat['owner']['_serialized']
		api['chat']['participants'] = chat['participants']
		api['chat']['isReadOnly']   = msg['chat']['isReadOnly']
		api['reply'] = msg['quotedMsgObj'] = msg['isNotification']
		api['isNotification'] = msg['isNotification']
		sender = msg['sender']
		api['from']['name'] = sender['formattedName']
		api['from']['id']   = sender['id']['_serialized']
		try:api['from']['isBusiness'] = sender['isBusiness']
		except:pass
		api['from']['photo'] = sender['profilePicThumbObj']['eurl']
		api['from']['pushname'] = sender['pushname']
		api['star'] = msg['star']
		api['timestamp'] = msg['timestamp']
		if 'quotedMsg' in msg:
			api['quoted']['text']=  msg['quotedMsg']['body']
			api['quoted']['id']=  msg['quotedParticipant']['_serialized']
	
	return api


