import requests
import os
import urllib.request

def internet_on():
    try:
        urllib.request.urlopen('https://github.com', timeout=10)
        return True
    except:
        return False
class gitAutoUpdate:
    def __init__(self,url,versionurl,version,past_versions,name,ext=".py"):
        if internet_on():
            self.delete_past(past_versions,name,ext)
            #Part 1 -- Should We update
            response = requests.get(versionurl).text
            print(str(response).replace('\n','').replace('\t','').replace(' ',''),version)
            if str(response).replace('\n','').replace('\t','').replace(' ','')==version:
                print("No update needed")
            else:
                #Yes we should!
                #Part 2 -- Download new code
                code = requests.get(url).text
                #Part 3 -- Create File
                print("Writing to {}".format(name+response.replace('\n','').replace('\t','').replace(' ','')+ext))
                with open(name+response.replace('\n','').replace('\t','').replace(' ','')+ext,"w+") as f:
                    f.write(code)
                #Now we need to raise an exception as the only thing left to do is delete this script
                print("Please re-open the latest version which was installed at :{}".format(os.getcwd()+"\\"+name+response.replace('\n','').replace('\t','').replace(' ','')+ext))
    def delete_past(self,past_versions,name,ext):
        for v in past_versions:
            if os.path.exists(os.path.join(os.getcwd(),name+v+ext)):
                os.remove(os.path.join(os.getcwd(),name+v+ext))
        #this runs at the start so that it doesn't exit out.
