#!/usr/bin/env python
# -*- coding:utf-8 -*-
import httplib2
import base64
import email
from apiclient.discovery import build
from apiclient import errors
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow as run

def GetService():
    CLIENT_SECRET_FILE = 'client_secret.json'
    #OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/gmail.modify'
    STORAGE = Storage('gmail.storage')

    flow = flow_from_clientsecrets(CLIENT_SECRET_FILE, scope=OAUTH_SCOPE)
    http = httplib2.Http()
    credentials = STORAGE.get()

    if credentials is None or credentials.invalid:
        credentials = run(flow, STORAGE, http=http)

    http = credentials.authorize(http)
    gmail_service = build('gmail', 'v1', http=http)

    return gmail_service

def ListLabels(service, user_id):
  """Get a list all labels in the user's mailbox.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.

  Returns:
    A list all Labels in the user's mailbox.
  """
  try:
    response = service.users().labels().list(userId=user_id).execute()
    labels = response['labels']
    return labels
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def ListMessagesMatchingQuery(service, user_id, query=''):
  """List all Messages of the user's mailbox matching the query.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    query: String used to filter messages returned.
    Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

  Returns:
    List of Messages that match the criteria of the query. Note that the
    returned list contains Message IDs, you must use get with the
    appropriate ID to get the details of a Message.
  """
  try:
    response = service.users().messages().list(userId=user_id, q=query).execute()
    messages = []
    if 'messages' in response:
      messages.extend(response['messages'])

    while 'nextPageToken' in response:
      page_token = response['nextPageToken']
      response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
      messages.extend(response['messages'])

    return messages
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    #print 'Message snippet: %s' % message['snippet']

    return message
  except errors.HttpError, error:
    print 'An error occurred: %s' % error


def GetMimeMessage(service, user_id, msg_id):
  """Get a Message and use it to create a MIME Message.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A MIME Message, consisting of data from Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id,
                                             format='raw').execute()

    #print 'Message snippet: %s' % message['snippet']

    msg_str = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))

    mime_msg = email.message_from_string(msg_str)

    return mime_msg
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def GetAttachments(service, user_id, msg_id, store_dir):
  """Get and store attachment from Message with given id.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: ID of Message containing attachment.
    store_dir: The directory used to store attachments.
  """
  list_attachments = []

  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    if 'parts' in message['payload']:
        for part in message['payload']['parts']:
          if part['filename']:
            filename = part['filename']
            attachment_id = part['body']['attachmentId']

            attachment = service.users().messages().attachments().get(userId=user_id, messageId=msg_id, id=attachment_id).execute()
            file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))
            path = ''.join([store_dir, msg_id + '_' +part['filename'].replace('/','_')])

            f = open(path, 'w')
            f.write(file_data)
            f.close()
            list_attachments.append(path)

    return list_attachments
  except errors.HttpError, error:
    print 'An error occurred: %s' % error

def AddLabelToMessage(service, user_id, msg_id, label_id):
    try:
        message = service.users().messages().modify(userId=user_id, id=msg_id,
                    body={'addLabelIds':[label_id]}).execute()
        return True
    except errors.HttpError, error:
        print 'An error occurred: %s' % error

def RemoveLabelToMessage(service, user_id, msg_id, label_id):
    try:
        message = service.users().messages().modify(userId=user_id, id=msg_id,
                    body={'removeLabelIds':[label_id]}).execute()
        return True
    except errors.HttpError, error:
        print 'An error occurred: %s' % error

def GetHeader(headers, name):
    for header in headers:
        if header['name'] == name:
            return header['value'].encode('utf-8')
    return None

def GetLabelId(labels, name):
    for label in labels:
        if label['name'] == name:
            return label['id']
    return None

def __getBody__(part):
    body = ''
    if len(part['filename']) == 0:
        if part['body']['size'] > 0 and 'data' in part['body']:
            body64 = part['body']['data']
            body += base64.urlsafe_b64decode(body64.encode('UTF-8'))
    return body

def _getBody_(parts):
    body = ''
    for part in parts:
        body += __getBody__(part)
        if 'parts' in part:
            body += _getBody_(part['parts'])
    return body

def GetBody(message):
    body = ''
    if 'parts' in message['payload']:
        body = _getBody_(message['payload']['parts'])
    return body
