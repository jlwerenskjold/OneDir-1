OneDir Server API Branch
======
This branch contains the initial OneDir server. Here are the available API commands: 
## /session [POST]
Starts a session with the OneDir server. 
##### Parameters
Username and password. Example: {"username":"OneDir", "password":"test"}
##### Return
A session cookie that must be saved and attached to all future API transactions. 
If login fails, then result will be -1 (no cookie will be given). If login succeeds, the result will be 1.
Message will return either username if successful, "not logged in" if unsuccessful, or "missing parameters".

## /session [DELETE]
Ends a session with the OneDir server  
##### Parameters
Session cookie must be provided
##### Return
Result, message, and session cookie that must be saved and attached to all future API transactions. 
If logout fails, then result will be -1. If logout succeeds, the result will be 1.
Message will return either username if successful or "not logged in" if unsuccessful. 

## /register [POST]
Creates a OneDir user  
##### Parameters
Username, password, and email. Example: {"username":"OneDir", "password":"test", "email":"onedir@gmail.com"}
##### Return
Result and message. If successful, result will be 1 and message will be "user created"
If unsuccessful, result will be -1. If due to missing parameters, message will be "missing parameters".
If due to non-unique email/username, message will be "registration failed"

## /file [POST]
Uploads a file to OneDir  
##### Parameters
File upload (titled "file"). Session cookie must be attached to request. 
##### Return
Result and message. If successful, result will be 1 and message will be "file uploaded"
If unsuccessful file upload, result will be -1. Result will be -2 if cookie is no good. 

## /file [GET]
Downloads a file to OneDir  
##### Parameters
File name as path, so "http://servername.com/file/the_file.txt". Session cookie must be attached to request. 
##### Return
Result and message. If successful, result will be file contents. 
If unsuccessful, result will be -1. Message will be 'file not found'. If cookie is no good, result will be -2





