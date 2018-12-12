import smtplib
 

def errormail(subject='default', msg='empty error message sent'):
	from_email = 'error.imagine.ds@gmail.com'
	to_email_list = ['hpf.vanheijst@gmail.com', 'mauricerichard91@gmail.com']
	key = 'undying with analyst lucy'

	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(from_email, key)
	msg = f'Subject:{subject}\n\n{msg}'
	for to_email in to_email_list:
		server.sendmail(from_email, to_email, msg)
	server.quit()

if __name__ == "__main__":
    errormail()