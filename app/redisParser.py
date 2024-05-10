import json
import os
class RedisParser:
    class encode :
        def bulk_string(string):
            length = str(len(string))
            res = "$"+length+"\r\n"+string+"\r\n"
            return res
        
        def simple_string(string):
            res = "+"+string+"\r\n"
            return res

        def null():
            return "$-1\r\n"
    class decode:

        def executeSet(val1,val2):
            data = {val1:val2}

            if os.path.exists('data.json'):
                with open('data.json') as f:
                    json_data = json.load(f)
                    # print(json_data)
                    json_data.update(data)
                with open('data.json','w') as f:
                    json.dump(json_data,f)
            else :
                with open('data.json', 'w+') as f:
                    json.dump(data,f,ensure_ascii=False)
            
            return RedisParser.encode.simple_string("OK")

        def executeGet(val1):
            with open('data.json') as f:
                json_data = json.load(f)
            try :
                obj_val = json_data[val1]
                return RedisParser.encode.simple_string(obj_val)
            except:
                return RedisParser.encode.null()
        def executeCommand(cmnd,lst):
            print(cmnd,lst)
            if(cmnd=='ECHO'):
                # print(lst[1])
                word = lst[1]     
                return RedisParser.encode.bulk_string(word)
            
            if(cmnd=='SET') : 
                val1 = lst[1]
                val2 = lst[3]
                return RedisParser.decode.executeSet(val1,val2)
            
            if(cmnd=='GET'):
                val1 = lst[1]
                return RedisParser.decode.executeGet(val1)
            
            if(cmnd=='PING'):
                return RedisParser.encode.simple_string("PONG")

        def decodeArrays(string):
                lst = string.split("\r\n")
                length = lst[0][1]
                actLength = len(lst)
                if(length==0): return
                cmnd = lst[2] 
                # print(cmnd,length)
                return RedisParser.decode.executeCommand(cmnd,lst[3-actLength::])
