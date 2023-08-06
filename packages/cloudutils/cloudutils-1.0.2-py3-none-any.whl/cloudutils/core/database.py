# Copyright © 2020 Noel Kaczmarek
from contextlib import closing

import sqlite3
import uuid
import os


class Database:
    def __init__(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()
        self.file = file

    def connect(self):
        self.connection = sqlite3.connect(self.file)
        self.cursor = self.connection.cursor()

    def insert(self, values):
        command = 'INSERT INTO %s (user, firstname, lastname, username, password, gender, email, birthdate, adress, ' \
                  'rank) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s);' % (
                      values[0], values[1], values[2], values[3], values[4],
                      values[5], values[6], values[7], values[8])

        self.execute(command)
        self.commit()

    def get(self):
        self.connect()
        return self.connection, self.cursor

    def query(self, sql, **kwargs):
        with closing(sqlite3.connect(self.file)) as con, con,  \
                closing(con.cursor()) as cur:
            cur.execute(sql)
            if kwargs.get('fetchone', False):
                return cur.fetchone()
            return cur.fetchall()

    def execute(self, command):
        self.cursor.execute(command)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def list_directory(self, path):

        self.c.execute('SELECT * WHERE parent = (?)', '/')
        return self.fetchall()

    def make_directory(self, user, name, parent):
        self.execute("INSERT INTO virtual_file (id, owner, name, parent, type) VALUES ('{}','{}','{}','{}','{}')".format(
            uuid.uuid4().hex, 
            user,
            name,
            parent,
            0
        ))

    @property
    def users(self):
        self.execute('SELECT username FROM user;')
        users = []

        user_list = self.fetchall()

        for user in user_list:
            users.append(user[0])

        return users

    @property
    def chats(self):
        self.execute('SELECT * FROM chat;')
        chats = self.fetchall()

        return chats

    @property
    def notifications(self):
        self.execute('SELECT * FROM notification;')
        notifications = self.fetchall()

        return notifications

    def getUsernameByID(self, id):
        self.execute('SELECT username from user WHERE id = %d' % id)
        return self.fetchone()[0]

    def getUserID(self, username):
        self.execute('SELECT id from user WHERE username = \'%s\'' % username)
        return self.fetchone()[0]

    def getUser(self, id, key):
        self.execute('SELECT \'%s\' from user WHERE id = %d' % (key, id))
        return self.fetchone()[0]

    def getUserRank(self, id):
        self.execute('SELECT rank FROM user WHERE id = %d' % id)
        return self.fetchone()[0]

    def getUserNotifications(self, id):
        notifications = []

        for notification in self.notifications:
            if notification[3] == id:
                notifications.append({'id': notification[0], 'title': notification[1], 'body': notification[2],
                                      'recipient': notification[3], 'seen': notification[4]})

        return notifications

    def getUserChats(self, id):
        self.connect()

        chats = []
        alreadyAdded = False

        for item in self.chats:
            if id in item:
                chat = {'ID': item[0]}

                for addedChat in chats:
                    if addedChat['ID'] == chat['ID']:
                        alreadyAdded = True

                if not alreadyAdded:
                    if item[1] == id:
                        chat['user'] = item[2]
                        chat['username'] = self.getUsernameByID(item[2])
                    else:
                        chat['user'] = item[1]
                        chat['username'] = self.getUsernameByID(item[1])

                    if os.path.isfile(os.path.join(config['data'], 'user', chat['username'], '_profile', 'picture.jpg')):
                        chat['picture'] = 'picture.jpg'
                    else:
                        chat['picture'] = 'picture.png'

                    chatHistory = self.getChatHistory(chat['ID'])

                    if chatHistory:
                        chat['last'] = chatHistory[0]
                    else:
                        chat['last'] = {'message': ''}

                    chats.append(chat)
        return chats

    def getChatID(self, user, partner):
        self.connect()
        self.execute('SELECT id FROM chat WHERE user = %d AND partner = %d' % (user, partner))
        return self.fetchone()[0]

    def getChatHistory(self, chat):
        self.connect()
        self.cursor.execute('SELECT * FROM message WHERE chat = (?)', str(chat))

        return list(reversed(self.fetchall()))
