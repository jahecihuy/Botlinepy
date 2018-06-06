# -*- coding: utf-8 -*-
from Api import Poll, Talk, channel
from lib.curve.ttypes import *
import requests
import shutil
import json
import urllib
import request
import os
import random,requests,shutil,tempfile,json
import subprocess
from random import randint
from gtts import gTTS

def def_callback(str):
    print(str)

class LINE:

  mid = None
  authToken = None
  cert = None
  channel_access_token = None
  token = None
  obs_token = None
  refresh_token = None


  def __init__(self):
    self.Talk = Talk()

  def login(self, mail=None, passwd=None, cert=None, token=None, qr=False, callback=None):
    if callback is None:
      callback = def_callback
    resp = self.__validate(mail,passwd,cert,token,qr)
    if resp == 1:
      self.Talk.login(mail, passwd, callback=callback)
    elif resp == 2:
      self.Talk.login(mail,passwd,cert, callback=callback)
    elif resp == 3:
      self.Talk.TokenLogin(token)
    elif resp == 4:
      self.Talk.qrLogin(callback)
    else:
      raise Exception("invalid arguments")

    self.authToken = self.Talk.authToken
    self.cert = self.Talk.cert

    self.authToken = self.Talk.authToken
    self.cert = self.Talk.cert
    self._session = requests.session()
    self._headers = {
              'X-Line-Application': 'DESKTOPMAC 10.10.2-YOSEMITE-x64    MAC 4.5.0',
              'X-Line-Access': self.authToken, 
              'User-Agent': 'Line/6.0.0 iPad4,1 9.0.2'
    }
    self.Poll = Poll(self.authToken)
    self.channel = channel.Channel(self.authToken)
    self.channel.login()
    self.mid = self.channel.mid
    self.channel_access_token = self.channel.channel_access_token
    self.token = self.channel.token
    self.obs_token = self.channel.obs_token
    self.refresh_token = self.channel.refresh_token

  """User"""

  def getProfile(self):
    return self.Talk.client.getProfile()

  def getClone(self):
    return self.Talk.client.getClone()

  def getSettings(self):
    return self.Talk.client.getSettings()

  def getUserTicket(self):
    return self.Talk.client.getUserTicket()

  def updateProfile(self, profileObject):
    return self.Talk.client.updateProfile(0, profileObject)

  def updateSettings(self, settingObject):
    return self.Talk.client.updateSettings(0, settingObject)

  def CloneContactProfile(self, mid):
    contact = self.getContact(mid)
    profile = self.getProfile()
    profile.displayName = contact.displayName
    profile.statusMessage = contact.statusMessage
    profile.pictureStatus = contact.pictureStatus
    self.updateDisplayPicture(profile.pictureStatus)
    return self.updateProfile(profile)

  def updateDisplayPicture(self, hash_id):
    return self.Talk.client.updateProfileAttribute(0, 8, hash_id)

  def CloneURL(self, URL):
    contact = self.getContact(URL)
    profile = self.getProfile()
    profile.displayName = contact.displayName
    profile.statusMessage = contact.statusMessage
    prifile.pictureStatus = contact.pictureStatus
    self.updateDisplayPicture(profile.pictureStatus)
    return self.updateProfile(profile)

  def CloneURL(self, hash_URL):
    return self.Talk.client.updateProfileAttribute(0, 8, hash_URL)

  """Operation"""

  def fetchOperation(self, revision, count):
        return self.Poll.client.fetchOperations(revision, count)

  def fetchOps(self, rev, count):
        return self.Poll.client.fetchOps(rev, count, 0, 0)

  def getLastOpRevision(self):
        return self.Talk.client.getLastOpRevision()

  def stream(self):
        return self.Poll.stream()

  """Message"""

  def kedapkedip(self, tomid, text):
        M = Message()
        M.to = tomid
        t1 = "\xf4\x80\xb0\x82\xf4\x80\xb0\x82\xf4\x80\xb0\x82\xf4\x80\xb0\x82"
        t2 = "\xf4\x80\x82\xb3\xf4\x8f\xbf\xbf"
        rst = t1 + text + t2
        M.text = rst.replace("\n", " ")
        return self.Talk.client.sendMessage(0, M)

  def sendMessage(self, messageObject):
        return self.Talk.client.sendMessage(0,messageObject)

  def sendText(self, Tomid, text):
        msg = Message()
        msg.to = Tomid
        msg.text = text

        return self.Talk.client.sendMessage(0, msg)
  def postContent(self, url, data=None, files=None):
        return self._session.post(url, headers=self._headers, data=data, files=files)

  def downloadFileURL(self, fileUrl):
        saveAs = '%s/linepy-%i.data' % (tempfile.gettempdir(), randint(0, 9))
        r = self.server.getContent(fileUrl)
        if r.status_code == 200:
            with open(saveAs, 'wb') as f:
                                shutil.copyfileobj(r.raw, f)
                                return saveAs
        else:
            raise Exception('Download file failure.')

  def downloadObjectMsgId(self, messageId):
        saveAs = '%s/%s-%i.bin' % (tempfile.gettempdir(), messageId, randint(0, 9))
        params = {'oid': messageId}
        url = self.server.urlEncode('https://obs.line-apps.com', '/talk/m/download.nhn', params)
        r = self.server.getContent(url)
        if r.status_code == 200:
            with open(saveAs, 'wb') as f:
                                shutil.copyfileobj(r.raw, f)
                                return saveAs
        else:
            raise Exception('Download file failure.')

  def post_content(self, url, data=None, files=None):
        return self._session.post(url, headers=self._headers, data=data, files=files)

  def sendImage(self, to_, path):
        M = Message(to=to_, text=None, contentType = 1)
        M.contentMetadata = None
        M.contentPreview = None
        M_id = self.Talk.client.sendMessage(0,M).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': 'media',
            'oid': M_id,
            'size': len(open(path, 'rb').read()),
            'type': 'image',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.post_content('https://os.line.naver.jp/talk/m/upload.nhn', data=data, files=files)
        print r
        if r.status_code != 201:
            raise Exception('Upload image failure.')
        return True

  def sendImageWithURL(self, to_, url):
        """Send a image with given image url
        :param url: image url to send
        """
        path = 'tmp/pythonLine.data'
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, 'w') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            raise Exception('Download image failure.')
        try:
            self.sendImage(to_, path)
        except Exception as e:
            raise e

  def getCover(self,mid):
        h = self.getHome(mid)
        objId = h["result"]["homeInfo"]["objectId"]
        return "http://dl.profile.line-cdn.net/myhome/c/download.nhn?userid=" +mid + "&oid=" + objId

  def getCover(self,mid):
        h = self.getHome(mid)
        objId = h["result"]["homeInfo"]["objectId"]
        return "http://dl.profile.line-cdn.net/myhome/c/download.nhn?userid=" + mid + "&oid=" + objId

  def sendVideo(self, to, path):
        contentMetadata = {
            'VIDLEN' : '60000',
            'DURATION' : '60000'
        }
        objectId = self.sendMessage(to=to, text=None, contentMetadata=contentMetadata, contentType = 2).id
        files = {
            'file': open(path, 'rb')
        }
        params = {
            'name': 'media',
            'oid': objectId,
            'size': len(open(path, 'rb').read()),
            'type': 'video',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.postContent('https://os.line.naver.jp/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload video failure.')
        return True

  def sendVideoWithURL(self, to, url):
        path = self.downloadFileURL(url)
        try:
            return self.sendVideo(to, path)
        except:
            raise Exception('Send video failure.')

  def sendAudio(self, to_, path):
		M = Message(to=to_,text=None,contentType=3)
		M.contentMetadata = {
		}
                M.contentPreview = None
		M_Id = self.Talk.client.sendMessage(0,M).id
		files = {
			'file': open(path, 'rb'),
                }
                params = {
			'name': 'media',
			'oid': M_Id,
			'size': len(open(path, 'rb').read()),
			'type': 'audio',
			'ver': '1.0',
                }
                data = {
			'params': json.dumps(params)
                }
                r = self.postContent('https://os.line.naver.jp/talk/m/upload.nhn', data=data, files=files)
		if r.status_code != 201:
			raise Exception('Upload audio failure.')
		return True

  def sendAudioWithURL(self, to_, url, header=None):
		path = '%s/linepy-%i.data' % (tempfile.gettempdir(), randint(0, 9))
		r = requests.get(url, stream=True,headers=header)
		if r.status_code == 200:
			with open(path, 'wb') as f:
				shutil.copyfileobj(r.raw, f)
		else:
                        print r.status_code
			raise Exception('Download audio failure.')
		try:
                        self.sendAudio(to_, path)
		except Exception as e:
			raise e

  def sendFile(self, to, path, file_name=''):
        if file_name == '':
            import ntpath
            file_name = ntpath.basename(path)
        file_size = len(open(path, 'rb').read())
        contentMetadata = {
            'FILE_NAME' : str(file_name),
            'FILE_SIZE' : str(file_size)
        }
        objectId = self.sendMessage(to=to, text=None, contentMetadata=contentMetadata, contentType = 14).id
        files = {
            'file': open(path, 'rb'),
        }
        params = {
            'name': file_name,
            'oid': objectId,
            'size': file_size,
            'type': 'file',
            'ver': '1.0',
        }
        data = {
            'params': json.dumps(params)
        }
        r = self.postContent('https://os.line.naver.jp/talk/m/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Upload file failure.')
        return True

  def sendFileWithURL(self, to, url, fileName=''):
        path = self.downloadFileURL(url)
        try:
            return self.sendFile(to, path, fileName)
        except:
            raise Exception('Send file failure.')

  def sendVideo(self, to_, path):
      M = Message(to=to_,contentType = 2)
      M.contentMetadata = {
           'VIDLEN' : '0',
           'DURATION' : '0'
      }
      M.contentPreview = None
      M_id = self.Talk.client.sendMessage(0,M).id
      files = {
         'file': open(path, 'rb'),
      }
      params = {
         'name': 'media',
         'oid': M_id,
         'size': len(open(path, 'rb').read()),
         'type': 'video',
         'ver': '1.0',
      }
      data = {
         'params': json.dumps(params)
      }
      r = self.post_content('https://os.line.naver.jp/talk/m/upload.nhn', data=data, files=files)
      if r.status_code != 201:
         raise Exception('Upload image failure.')
      return True

  def sendVideoWithURL(self, to_, url):
      path = 'pythonLines.data'
      r = requests.get(url, stream=True)
      if r.status_code == 200:
         with open(path, 'w') as f:
            shutil.copyfileobj(r.raw, f)
      else:
         raise Exception('Download Audio failure.')
      try:
         self.sendVideo(to_, path)
      except Exception as e:
         raise e

  def upload_tempimage(client):
     '''
         Upload a picture of a kitten. We don't ship one, so get creative!
     '''
     config = {
         'album': album,
         'name': 'bot auto upload',
         'title': 'bot auto upload',
         'description': 'bot auto upload'
     }
     print("Uploading image... ")
     image = cl.upload_from_path(image_path, config=config, anon=False)
     print("Done")
     print()
     return image

  def updateProfilePicture(self, path):
        file=open(path, 'rb')
        files = {
            'file': file
        }
        params = {
            'name': 'media',
            'type': 'image',
            'oid': self.getProfile().mid,
            'ver': '1.0',
        }
        data={
            'params': json.dumps(params)
        }
        r = self.post_content('https://os.line.naver.jp/talk/p/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Update profile picture failure.')
        return True
       
#  def updateProfilePicture
  def dl_line(self,url):
      file_name = os.path.splitext(url.split("/")[-1])[0] + '.png'
      req = urllib.request.Request(url, headers=self.headers) 
      r = urllib.request.urlopen( req )
      i = Image.open(io.BytesIO(r.read()))
      i.save('%s'%file_name)
      return '%s'%file_name

  def updateProfilePicture(self, path):
        file=open(path, 'rb')
        files = {
            'file': file
        }
        params = {
            'name': 'media',
            'type': 'image',
            'oid': self.getProfile().mid,
            'ver': '1.0',
        }
        data={
            'params': json.dumps(params)
        }
        r = self.post_content('https://os.line.naver.jp/talk/p/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Update profile picture failure.')
        return True
   
  def getContent(self, url, headers=None):
        if headers is None:
            headers=self._headers
        return self._session.get(url, headers=headers, stream=True)
  def urlEncode(self, url, path, params=[]):
        try:        # Works with python 2.x
            return url + path + '?' + urllib.urlencode(params)
        except:     # Works with python 3.x
            return url + path + '?' + urllib.parse.urlencode(params)
  def downloadObjectMsgId(self, messageId):
        saveAs = '%s/%s-%i.bin' % (tempfile.gettempdir(), messageId, randint(0, 9))
        params = {'oid': messageId}
        url = self.urlEncode('https://obs.line-apps.com', '/talk/m/download.nhn', params)
        r = self.getContent(url)
        if r.status_code == 200:
            with open(saveAs, 'wb') as f:
				shutil.copyfileobj(r.raw, f)			
				return saveAs
        else:
            raise Exception('Download file failure.')

  def updateGroupPicture(self, groupId, path):
        msg = Message()
        msg.to = groupId
        file=open(path, 'rb')
        files = {
            'file': file
        }
        params = {
            'name': 'media',
            'type': 'image',
            'oid': self.getGroup(msg.to).id,
            'ver': '1.0',
        }
        data={
            'params': json.dumps(params)
        }
        r = self.post_content('https://os.line.naver.jp/talk/g/upload.nhn', data=data, files=files)
        if r.status_code != 201:
            raise Exception('Update profile picture failure.')
        return True
    
  def sendEvent(self, messageObject):
        return self._client.sendEvent(0, messageObject)

  def sendChatChecked(self, mid, lastMessageId):
        return self.Talk.client.sendChatChecked(0, mid, lastMessageId)

  def getMessageBoxCompactWrapUp(self, mid):
        return self.Talk.client.getMessageBoxCompactWrapUp(mid)

  def getMessageBoxCompactWrapUpList(self, start, messageBox):
        return self.Talk.client.getMessageBoxCompactWrapUpList(start, messageBox)

  def getRecentMessages(self, messageBox, count):
        return self.Talk.client.getRecentMessages(messageBox.id, count)

  def getMessageBox(self, channelId, messageboxId, lastMessagesCount):
        return self.Talk.client.getMessageBox(channelId, messageboxId, lastMessagesCount)

  def getMessageBoxList(self, channelId, lastMessagesCount):
        return self.Talk.client.getMessageBoxList(channelId, lastMessagesCount)

  def getMessageBoxListByStatus(self, channelId, lastMessagesCount, status):
        return self.Talk.client.getMessageBoxListByStatus(channelId, lastMessagesCount, status)

  def getMessageBoxWrapUp(self, mid):
        return self.Talk.client.getMessageBoxWrapUp(mid)

  def getMessageBoxWrapUpList(self, start, messageBoxCount):
        return self.Talk.client.getMessageBoxWrapUpList(start, messageBoxCount)

  def getCover(self,mid):
        h = self.getHome(mid)
        objId = h["result"]["homeInfo"]["objectId"]
        return "http://dl.profile.line-cdn.net/myhome/c/download.nhn?userid=" + mid+ "&oid=" + objId

  """Contact"""


  def blockContact(self, mid):
        return self.Talk.client.blockContact(0, mid)


  def unblockContact(self, mid):
        return self.Talk.client.unblockContact(0, mid)


  def findAndAddContactsByMid(self, mid):
        return self.Talk.client.findAndAddContactsByMid(0, mid)


  def findAndAddContactsByMids(self, midlist):
        for i in midlist:
            self.Talk.client.findAndAddContactsByMid(0, i)

  def findAndAddContactsByUserid(self, userid):
        return self.Talk.client.findAndAddContactsByUserid(0, userid)

  def findContactsByUserid(self, userid):
        return self.Talk.client.findContactByUserid(userid)

  def findContactByTicket(self, ticketId):
        return self.Talk.client.findContactByUserTicket(ticketId)

  def getAllContactIds(self):
        return self.Talk.client.getAllContactIds()

  def getBlockedContactIds(self):
        return self.Talk.client.getBlockedContactIds()

  def getContact(self, mid):
        return self.Talk.client.getContact(mid)

  def getContacts(self, midlist):
        return self.Talk.client.getContacts(midlist)

  def getFavoriteMids(self):
        return self.Talk.client.getFavoriteMids()

  def getHiddenContactMids(self):
        return self.Talk.client.getHiddenContactMids()


  """Group"""

  def findGroupByTicket(self, ticketId):
        return self.Talk.client.findGroupByTicket(ticketId)

  def acceptGroupInvitation(self, groupId):
        return self.Talk.client.acceptGroupInvitation(0, groupId)

  def acceptGroupInvitationByTicket(self, groupId, ticketId):
        return self.Talk.client.acceptGroupInvitationByTicket(0, groupId, ticketId)

  def cancelGroupInvitation(self, groupId, contactIds):
        return self.Talk.client.cancelGroupInvitation(0, groupId, contactIds)

  def createGroup(self, name, midlist):
        return self.Talk.client.createGroup(0, name, midlist)

  def getGroup(self, groupId):
        return self.Talk.client.getGroup(groupId)

  def getGroups(self, groupIds):
        return self.Talk.client.getGroups(groupIds)

  def getGroupIdsInvited(self):
        return self.Talk.client.getGroupIdsInvited()

  def getGroupIdsJoined(self):
        return self.Talk.client.getGroupIdsJoined()
  def getGroupIdsJoineds(self):
        return self.Talk.client.getGroupIdsJoineds()

  def inviteIntoGroup(self, groupId, midlist):
        return self.Talk.client.inviteIntoGroup(0, groupId, midlist)

  def kickoutFromGroup(self, groupId, midlist):
        return self.Talk.client.kickoutFromGroup(0, groupId, midlist)

  def leaveGroup(self, groupId):
        return self.Talk.client.leaveGroup(0, groupId)

  """TIMELINE"""
  def createGroupPost(self, mid, text):
        payload = {'postInfo': {'readPermission': {'homeId': mid}}, 'sourceType': 'TIMELINE', 'contents': {'text': text}}
        data = json.dumps(payload)
        r = self.server.postContent(self.server.LINE_TIMELINE_API + '/v27/post/create', data=data, headers=self.server.channelHeaders)
        return r.json()

  def getGroupPost(self, mid, postLimit=10, commentLimit=1, likeLimit=1):
        params = {'homeId': mid, 'commentLimit': commentLimit, 'likeLimit': likeLimit, 'sourceType': 'TALKROOM'}
        url = self.server.urlEncode(self.server.LINE_TIMELINE_API, '/v27/post/list', params)
        r = self.server.getContent(url, headers=self.server.channelHeaders)
        return r.json()

  def new_post(self, text):
    return self.channel.new_post(text)

  def rejectGroupInvitation(self, groupId):
        return self.Talk.client.rejectGroupInvitation(0, groupId)

  def reissueGroupTicket(self, groupId):
        return self.Talk.client.reissueGroupTicket(groupId)

  def updateGroup(self, groupObject):
        return self.Talk.client.updateGroup(0, groupObject)
  def findGroupByTicket(self,ticketId):
        return self.Talk.client.findGroupByTicket(0,ticketId)

  def findGroupByTicket(self,ticketId):
        return self.Talk.client.findGroupByTicket(ticketId)

  """Room"""

  def createRoom(self, midlist):
    return self.Talk.client.createRoom(0, midlist)

  def getRoom(self, roomId):
    return self.Talk.client.getRoom(roomId)

  def inviteIntoRoom(self, roomId, midlist):
    return self.Talk.client.inviteIntoRoom(0, roomId, midlist)

  def leaveRoom(self, roomId):
    return self.Talk.client.leaveRoom(0, roomId)

  """TIMELINE"""

  def new_post(self, text):
    return self.channel.new_post(text)

  def like(self, mid, postid, likeType=1001):
    return self.channel.like(mid, postid, likeType)

  def comment(self, mid, postid, text):
    return self.channel.comment(mid, postid, text)

  def activity(self, limit=20):
    return self.channel.activity(limit)

  def getAlbum(self, gid):

      return self.channel.getAlbum(gid)
  def changeAlbumName(self, gid, name, albumId):
      return self.channel.changeAlbumName(gid, name, albumId)

  def deleteAlbum(self, gid, albumId):
      return self.channel.deleteAlbum(gid,albumId)

  def getNote(self,gid, commentLimit, likeLimit):
      return self.channel.getNote(gid, commentLimit, likeLimit)

  def getDetail(self,mid):
      return self.channel.getDetail(mid)

  def getHome(self,mid):
      return self.channel.getHome(mid)

  def createAlbum(self, gid, name):
      return self.channel.createAlbum(gid,name)

  def createAlbum2(self, gid, name, path):
      return self.channel.createAlbum(gid, name, path, oid)


  def __validate(self, mail, passwd, cert, token, qr):
    if mail is not None and passwd is not None and cert is None:
      return 1
    elif mail is not None and passwd is not None and cert is not None:
      return 2
    elif token is not None:
      return 3
    elif qr is True:
      return 4
    else:
      return 5

  def loginResult(self, callback=None):
    if callback is None:
      callback = def_callback

      prof = self.getProfile()

      print("KANINO-BOT")
      print("mid -> " + prof.mid)
      print("name -> " + prof.displayName)
      print("authToken -> " + self.authToken)
      print("cert -> " + self.cert if self.cert is not None else "")
