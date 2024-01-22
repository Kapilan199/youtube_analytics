import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import base64

## Mail Sending function

def mailsend(emailto, encoded_image):

  ## Mail details
  emailfrom = "sentimentanalysiskr@gmail.com"
  fileToSend = ["Full Comments.csv", "Positive Comments.csv", "Negative Comments.csv"]
  username = "sentimentanalysiskr@gmail.com"
  password = "xylh djhb yfwp ckgu"

  ## Mail Subject

  msg = MIMEMultipart()
  msg["From"] = emailfrom
  msg["To"] = emailto
  msg["Subject"] = "Hi your youtube comments excel file and graphs are here   -Youtube Comment Scraper"
  # msg.preamble = "Hi your csv file is ready from  -Youtube Comment Scraper"

  ## Adding attachments

  subtype = 'vnd.ms-excel'  # Subtype for excel or csv files
  for f in fileToSend:
    fp = open(f, encoding = 'utf8')
    attachment = MIMEText(fp.read(), _subtype = subtype)
    fp.close()
    attachment.add_header("Content-Disposition", "attachment", filename=f)
    msg.attach(attachment)



    image_data = base64.b64decode(encoded_image)
    image_attachment = MIMEImage(image_data, name='image.png')
    image_attachment.add_header('Content-ID', '<inline-image>')
    msg.attach(image_attachment)

  ## Sending mail to the user

  server = smtplib.SMTP("smtp.gmail.com:587")
  server.starttls()
  server.login(username,password)
  server.sendmail(emailfrom, emailto, msg.as_string())
  server.quit()
