import os,errno
import shutil
import glob
import hashlib
from .status import error,success,info
from . import cryptopidb as crdb
from .functions import *
from .operators import *


class pi7db:
  def __init__(self,db_name,db_path=os.getcwd()):
   self.db_np,self.db_name = os.path.join(db_path,db_name),db_name
   self.config_file,self.coll_name = os.path.join(self.db_np,db_name),None
   if not os.path.exists(self.db_np):os.makedirs(self.db_np)
   if not os.path.exists(f"{self.config_file}.json"):
    self.config = {'secret-key':None}
    writejson(self.config_file,self.config)
   else:self.config=openjson(self.config_file)
     
  def __getattr__(self, attrname):
   path=self.coll_name=os.path.join(self.db_np,attrname)
   SubClass = type(attrname,(),{'filter':self.filter,'update':self.update,'read':self.read,'write':self.write,'trash':self.trash})
   if not os.path.exists(path):os.mkdir(path)
   return SubClass
  
  def key(self,password):
   key = hashlib.md5(password.encode()).hexdigest()
   if self.config['secret-key'] is not None: 
    if key != self.config['secret-key']:raise ValueError(error.e0)
   else:
     self.config = {'secret-key':key}
     writejson(self.config_file,self.config)

  def changekey(self,old_key,New_key):
   files,old_key,New_key = glob.glob(f"{self.db_np}/*/*."),hashlib.md5(old_key.encode()).hexdigest(),hashlib.md5(New_key.encode()).hexdigest()
   if old_key == openjson(self.config_file)['secret-key']:
    for x_js in files:
     writejson(x_js[:-5],openjson(x_js[:-5],old_key),New_key)
     if os.path.exists(x_js):os.remove(x_js)
    writejson(self.config_file,{'secret-key':New_key})
   else:raise ValueError(error.e1)

  def write(self,file_name,data):
   try:
      writejson(os.path.join(self.db_name,self.coll_name,file_name),data,self.config['secret-key'])
      return success.s0(file_name, self.coll_name)
   except Exception as e:return error.e4
  
  def update(self,file_name,*data_arg):
   try: 
    file_path,js_data= os.path.join(self.coll_name,file_name),openjson(file_path,self.config['secret-key']) 
    for data in data_arg:     
     if isinstance(data,dict):js_data.update(data)
     else:return error.e2
    writejson(file_path,js_data,self.config['secret-key'])
    return success.s1(file_name)
   except OSError as e:
    if e.errno == errno.ENOENT:return error.e3(self.coll_name)
    else:return e
  
  def read(self,file_name=None,key_name=None):    
   if isinstance(self.coll_name,str):
    if key_name is not None:return openjson(f"{self.coll_name}/{file_name}",self.config['secret-key'])[key_name]
    elif file_name is not None:data_files=glob.glob(f"{self.coll_name}/{file_name}.json")
    else:data_files = glob.glob(f"{self.coll_name}/*")
   else:data_files = glob.glob(f"{self.db_np}/*/*")  
   r_data = {"data":[],"status":1}
   for x_file in data_files:r_data['data'].append(openjson(x_file[:-5],self.config['secret-key']))
   return r_data  
    
  def trash(self,file_name=None,key_name=None):
   if isinstance(self.coll_name,str):
    if key_name is not None:
      tr_data = openjson(f"{self.coll_name}/{file_name}",self.config['secret-key']).pop(key_name)
      writejson(f"{self.coll_name}/{file_name}",tr_data,self.config['secret-key'])
      return success.s2(key_name,file_name)
    elif file_name is not None:
      os.remove(f"{self.coll_name}/{file_name}.json")
      return success.s3(file_name)
    else:
      shutil.rmtree(self.coll_name, ignore_errors=False, onerror=None)
      return success.s4(self.coll_name)
   else:return info.i0
 
  def filter(self,*command_tup):
   if isinstance(self.coll_name,str):all_files = glob.glob(f"{self.coll_name}/*")
   else:all_files = glob.glob(f"{self.db_np}/*/*")  
   r_data,command_arr= {"data":[],'status':1},[]
   if OR in command_tup:
    for x_p in command_tup:
      if x_p != OR:command_arr.append(x_p)
    for command in command_arr:
     data_get = andfilter(command,self.config['secret-key'],all_files)
     for x in data_get:
      if x not in r_data['data']:r_data['data'].append(x)
    return r_data
   else:
    for x_r in andfilter(command_tup[0],self.config['secret-key'],all_files):r_data['data'].append(x_r)
    return r_data
    
    
