import re 
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
      
def verificaEmail(email):  
    if(re.search(regex,email)):  
        print("Valid Email")     
    else:  
        print("Invalid Email")  
      

email = "ankitrai326@gmail.com"
verificaEmail(email) 
email = "my.ownsite@ourearth.org"
verificaEmail(email) 
email = "ankitrai326.com"
verificaEmail(email) 