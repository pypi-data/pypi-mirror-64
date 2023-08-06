import os
from os.path import basename
import traceback
import email
import imaplib
import smtplib
from email.utils import parsedate
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from dateutil import parser

import pandas as pd


class EmailTool:
	""" Tooling to handle emails """

	def __init__(self, email_user, email_password):
		""" Initialize the class
		:param email_user: Email address from where download attachments
		:param email_password: Email password for the address indicated above
		"""

		self.from_ = email_user
		self.pass_ = email_password

		self.m = imaplib.IMAP4_SSL("outlook.office365.com", 993)
		self.m.login(self.from_, email_password)
		self.mailserver = None

	def open_email(self):
		self.mailserver = smtplib.SMTP('smtp.office365.com', 587)
		self.mailserver.ehlo()
		self.mailserver.starttls()
		self.mailserver.login(self.from_, self.pass_)

	def close_email(self):
		self.mailserver.quit()

	def send_email(self, subject, body, recipient="", hidden_recipient=None, attachment=None):
		""" Send an email with attachment if required
		:param subject: Email subject
		:param body: Email body or message
		:param recipient: Email address to whom the email will be sent
		:param hidden_recipient: Email address for the hidden recipients
		:param attachment: File to attach if required
		:return: Send an email to the specified address
		"""
		try:

			if isinstance(recipient, list) is False:
				recipient = [recipient]

			self.open_email()

			msg = MIMEMultipart('alternative')
			msg['Subject'] = subject
			msg['From'] = self.from_
			msg['To'] = ', '.join(recipient)
			to_ = recipient

			if hidden_recipient is not None:
				if isinstance(hidden_recipient, list) is False:
					hidden_recipient = [hidden_recipient]
				msg['BCC'] = ', '.join(hidden_recipient)
				to_ = recipient + hidden_recipient

			if attachment is not None:
				if isinstance(attachment, list) is False:
					attachment = [attachment]
				for f in attachment or []:
					with open(f, "rb") as fil:
						part = MIMEApplication(fil.read(), Name=basename(f))
					# After the file is closed
					part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
					msg.attach(part)

			# Send as HTML
			part = MIMEText(body, 'html')

			msg.attach(part)

			self.mailserver.sendmail(self.from_, to_, msg.as_string())

		except Exception:
			print(traceback.format_exc())

		finally:
			self.close_email()

	def download_files(self, folder='Inbox', files=None, date_received=datetime.now(), from_date=datetime.now(),
	                   time_range=1, notz=False):
		""" Download all the email attachments
		:param folder: Email folder from which we want to retrieve the attachments
		:param files: List of the files that want to be retrieved
		:param from_date: Date from when the emails will be queried
		:param date_received: Indicate the date in which the emails were received
		:param time_range: Indicate the number of minutes from when the emails will be filtered
		:param notz: to remove time_zone
		:return: DataFrame tracking the downloaded files
		"""
		self.m.select(folder)

		status, items = self.m.search(None, '(SINCE "%s")' % from_date.strftime('%d-%b-%Y'))

		id_list = items[0].split()
		# Query the last 5 emails
		for num in id_list[-5:]:
			stat, data = self.m.fetch(num, '(RFC822)')
			raw_email = data[0][1]
			# Converts byte literal to string removing b''
			raw_email_string = raw_email.decode('utf-8')
			email_message = email.message_from_string(raw_email_string)

			# email_received = pd.to_datetime(email_message['Date'], format='%a, %d %b %Y %H:%M:%S +0000').
			# tz_localize('UTC')
			email_received = email.utils.parsedate(email_message['Date'])
			email_received = pd.to_datetime(datetime(*email_received[0:6])).tz_localize('UTC')
			if notz:
				email_received = email_received.replace(tzinfo=None)
			if (email_received >= date_received - timedelta(minutes=time_range)) & (
					email_received <= date_received + timedelta(minutes=time_range)):
				# Downloading attachments
				for part in email_message.walk():
					file_name = part.get_filename()
					# Evaluate whether get all the files or not
					if file_name is not None:
						if files is None:
							mask = bool(file_name)
						else:
							mask = bool(file_name) & (file_name in files)

						if mask:
							file_path = os.path.join(os.getcwd(), file_name)
							if not os.path.isfile(file_path):
								fp = open(file_path, 'wb')
								fp.write(part.get_payload(decode=True))
								fp.close()
							print('Downloaded "{file}".'.format(file=file_name))

	def retrieve_emails(self, folder='Inbox', from_date=datetime.today(), n_emails=5, remove_recipient=None,
	                    extension='', threshold=10):
		""" Returns a dataframe with all attachments names and needed metadata
		:param folder: Folder from which
		:param from_date: Date from when the emails will be queried
		:param n_emails: Number of emails to take care
		:param remove_recipient: List of emails to avoid when registering the emails
		:param extension: File extension to download. If extension is '', then retrieve everything
		:param threshold: Range to compare input emails with attachment created
		:return:

		ALTERNATIVE WAY TO PARSE DATE FROM EMAIL STRING, REMOVE AFTER CHECKING THE ACTUAL WORKS CORRECTLY
			text = created.splitlines()
			created = ''
			for x in text:
			    created = created + x
			created = created.rstrip().lstrip()
			created = datetime.strptime(created, '%a, %d %b %Y %H:%M:%S')

		"""

		if remove_recipient is None:
			remove_recipient = []
		self.m.select(folder)
		status, items = self.m.search(None, '(SINCE "%s")' % from_date.strftime('%d-%b-%Y'))

		# Query the last n_emails emails
		emails_df = pd.DataFrame()
		id_list = items[0].split()
		for num in id_list[-n_emails:]:
			stat, data = self.m.fetch(num, '(RFC822)')
			raw_email = data[0][1]

			# Converts byte literal to string removing b''
			raw_email_string = raw_email.decode('utf-8')
			email_message = email.message_from_string(raw_email_string)
			sender = email_message['From'].split('<')[1].split('>')[0]

			if sender not in remove_recipient:
				# email_received
				email_received = email.utils.parsedate(email_message['Date'])
				received_date = pd.to_datetime(datetime(*email_received[0:6]))

				# obtaining created
				created = email_message['Received'][::-1]
				created = created[created.find('+') + 1: created.find(';') - 1][::-1]
				created = parser.parse(created)

				inbox = self.m.get_folder(folder_name=folder)

				for message in inbox.get_messages(download_attachments=True):
					time_att = message.created.replace(tzinfo=None)
					if message.has_attachments & (time_att >= from_date):
						sender_att = str(message.sender)[str(message.sender).find('(') + 1:str(message.sender).find(')')]
						if sender_att == sender:
							if (time_att < created + timedelta(seconds=threshold)) & (
									time_att > created - timedelta(seconds=threshold)):
								for att in message.attachments:
									attachment_name = str(att)[str(att).find(' ') + 1:]
									if extension in attachment_name:
										inbox.get_message(download_attachments=True)
										aux = pd.DataFrame({
											'Sender': sender_att, 'Subject': message.subject,
											'Body': message.body, 'AttachmentName': attachment_name,
											'Created': created, 'Received': received_date
											}, index=[0])
										emails_df = emails_df.append(aux)

		return emails_df.reset_index(drop=True)
