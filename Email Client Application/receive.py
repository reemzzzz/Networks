

from PyQt5.QtWidgets import QMainWindow, QApplication, QTextEdit
from PyQt5 import uic
import imaplib
import email as email_module  # Rename the imported module to avoid conflicts
from email.mime.multipart import MIMEMultipart



print("Hello")

class receiverInterface(QMainWindow):
    def __init__(self):
        super(receiverInterface,self).__init__()
        uic.loadUi("receiverGUI.ui",self)
        self.show()
        self.loginbtn.clicked.connect(self.login)
        self.emailContent = self.findChild(QTextEdit, "emailContent") 
        


    def login(self):
     imap_server = self.imaptext.text()
     email = self.emailtext.text()
     password = self.passwordtext.text()


     try:
         imap = imaplib.IMAP4_SSL(imap_server)
         imap.login(email,password)
         imap.select("Inbox")
        
         print("It is me") 
    

         _, msgnums =imap.search(None, "ALL")

         email_content = ""

         for index, msgnum in enumerate(reversed(msgnums[0].split())):
           if index >= 5:
             break
    
           _, data = imap.fetch(msgnum, "(RFC822)")
           
           message = email_module.message_from_bytes(data[0][1])
      
           email_content += f"Message Number: {msgnum}\n"
           email_content += f"From: {message.get('From')}\n"
           email_content += f"To: {message.get('To')}\n"
           email_content += f"BCC: {message.get('BCC')}\n"
           email_content += f"Date: {message.get('Date')}\n"
           email_content += f"Subject: {message.get('Subject')}\n"
           email_content += "Content: \n"
           for part in message.walk():
               if part.get_content_type() == "text/plain":
                  #  print(part.as_string())
                  email_content += part.as_string() + "\n\n"
         self.emailContent.setText(email_content)
             
         imap.close()  

     except Exception as e:
            print("Error:", e)

                    
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = receiverInterface()
    sys.exit(app.exec_())
