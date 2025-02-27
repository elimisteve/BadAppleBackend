# General imports:
from django.db import models
from django.utils import timezone
from uuid import uuid4
from gnupg import GPG

# Import reference data:
import mainSite.extendedModels.modelCodes as choices

# Import administrative models:
from mainSite.extendedModels.administrative import *



# Main database models:

class PRATemplate(models.Model):
	# Filters:
	country = models.CharField('Country' , max_length = 3 , choices = choices.COUNTRIES , default = 'USA')
	stateTerritoryProvince = models.CharField('State/Territory/Province' , max_length = 6 , choices = choices.STATES_TERRITORIES_PROVINCES , default = 'USA-CA')
	subject = models.CharField('Subject' , max_length = 3 , choices = choices.PRA_SUBJECTS , default = '11')

	# Template Contents:
	title = models.CharField('Title' , max_length = 300 , blank = True)
	letterBody = models.TextField('Letter Body' , max_length = 10000 , blank = True)

	# Administrative:
	createdOn = models.DateTimeField('Template Created On (Auto-Filled)' , auto_now_add = True)
	updatedOn = models.DateTimeField('Template Last Updated On (Auto-Filled)' , auto_now = True)
	lastChangedBy = models.CharField('Last Changed By' , max_length = 50 , blank = True)
	toBeDeleted = models.BooleanField('Delete' , default = False)
	daysUntilDeletion = models.IntegerField('Days Until Deletion (When Marked For Deletion)' , default = 30)

	# Permissions:
	approved = models.BooleanField('Template Approved' , default = False)
	public = models.BooleanField('Template Public' , default = False)



	# Manage metadata:
	class Meta:
		verbose_name = 'PRA Template'
		verbose_name_plural = 'PRA Templates'



class OversightCommission(models.Model):
	def generateUniqueID():
		while (True):
			uniqueID = str(uuid4())
			if (len(OversightCommission.objects.filter(commissionID = uniqueID)) == 0):
				return uniqueID


	# Profile:
	name = models.CharField('Name' , max_length = 150)
	type = models.CharField('Type' , max_length = 2 , choices = choices.COMMISSIONS , default = '0')
	website = models.URLField('Website URL' , max_length = 300 , blank = True)

	# Location:
	country = models.CharField('Country' , max_length = 3 , choices = choices.COUNTRIES , default = 'USA')
	stateTerritoryProvince = models.CharField('State/Territory/Province' , max_length = 6 , choices = choices.STATES_TERRITORIES_PROVINCES , default = 'USA-CA')
	cityTown = models.CharField('City/Town' , max_length = 60 , blank = True)
	postalCode = models.CharField('Postal Code' , max_length = 15 , blank = True)
	address1 = models.CharField('Address (Line 1)' , max_length = 100 , blank = True)
	address2 = models.CharField('Address (Line 2)' , max_length = 100 , blank = True)

	# General Contact Info:
	email = models.EmailField('Email Address' , blank = True)
	phone = models.CharField('Phone Number (Format: 1-123-555-1234)' , max_length = 18 , blank = True)
	phoneTDD = models.CharField('TTD/TTY Phone Number (Format: 1-123-555-1234)' , max_length = 18 , blank = True)
	fax = models.CharField('Fax Number (Format: 1-123-555-1234)' , max_length = 18 , blank = True)
	contactForm = models.URLField('Contact Form URL' , max_length = 300 , blank = True)

	# Press Contact Info:
	pressEmail = models.EmailField('Press Email Address' , blank = True)
	pressPhone = models.CharField('Press Phone Number (Format: 1-123-555-1234)' , max_length = 18 , blank = True)
	pressContactForm = models.URLField('Press Contact Form URL' , max_length = 300 , blank = True)

	# Contents:
	aboutSummary = models.TextField('About/Summary' , max_length = 10000 , blank = True)
	complaintInfo1 = models.URLField('Complaint Information (URL 1)' , max_length = 300 , blank = True)
	complaintInfo2 = models.URLField('Complaint Information (URL 2)' , max_length = 300 , blank = True)
	complaintForm = models.URLField('Complaint Form URL' , max_length = 300 , blank = True)
	alternateComplaintFormType = models.CharField('Alternate Complaint Form Type' , max_length = 2 , choices = choices.COMPLAINT_FORMS , default = '0')
	alternateComplaintForm = models.URLField('Alternate Complaint Form URL' , max_length = 300 , blank = True)
	membersPage = models.URLField('Members Page URL' , max_length = 300 , blank = True)
	faqPage = models.URLField('FAQ Page URL' , max_length = 300 , blank = True)

	# Administrative:
	commissionID = models.CharField('Commission ID' , max_length = 36 , default = generateUniqueID)
	createdOn = models.DateTimeField('Record Created On' , auto_now_add = True)
	updatedOn = models.DateTimeField('Record Last Updated On' , auto_now = True)
	lastChangedBy = models.CharField('Last Changed By' , max_length = 50 , blank = True)
	toBeDeleted = models.BooleanField('Delete' , default = False)
	daysUntilDeletion = models.IntegerField('Days Until Deletion' , default = 30)
	completed = models.BooleanField('Completed' , default = True)

	# Permissions:
	approved = models.BooleanField('Record Approved' , default = False)
	public = models.BooleanField('Record Public' , default = False)



	# Manage metadata:
	class Meta:
		verbose_name = 'Oversight Commission'
		verbose_name_plural = 'Oversight Commissions'



class Officer(models.Model):
	def generateUniqueID():
		while (True):
			uniqueID = str(uuid4())
			if (len(Officer.objects.filter(officerID = uniqueID)) == 0):
				return uniqueID


	# Profile:
	firstName = models.CharField('First Name(s)' , max_length = 150)
	middleName = models.CharField('Middle Name/Initial' , max_length = 150 , blank = True)
	lastName = models.CharField('Last Name(s)' , max_length = 150)

	# Administrative:
	internalNotes = models.TextField('Internal Notes' , max_length = 10000 , blank = True)
	officerID = models.CharField('Officer ID' , max_length = 36 , default = generateUniqueID)
	createdOn = models.DateTimeField('Record Created On' , auto_now_add = True)
	updatedOn = models.DateTimeField('Record Last Updated On' , auto_now = True)
	lastChangedBy = models.CharField('Last Changed By' , max_length = 50 , blank = True)
	toBeDeleted = models.BooleanField('Delete' , default = False)
	daysUntilDeletion = models.IntegerField('Days Until Deletion' , default = 30)

	# Permissions:
	approved = models.BooleanField('Record Approved' , default = False)
	public = models.BooleanField('Record Public' , default = False)


	def __str__(self):
		return (str(self.id) + ' - ' + self.firstName + ' ' + self.lastName)



	# Manage metadata:
	class Meta:
		verbose_name = 'Officer'
		verbose_name_plural = 'Officers'



class InvestigativeReport(models.Model):
	def generateUniqueID():
		while (True):
			uniqueID = str(uuid4())
			if (len(InvestigativeReport.objects.filter(reportID = uniqueID)) == 0):
				return uniqueID


	# Related Models:
	subjectOfInvestigation = models.ForeignKey(Officer , null = True , on_delete = models.SET_NULL , verbose_name = 'Subject of Investigation (Officer)')

	# Location:
	country = models.CharField('Country' , max_length = 3 , choices = choices.COUNTRIES , default = 'USA')
	stateTerritoryProvince = models.CharField('State/Territory/Province' , max_length = 6 , choices = choices.STATES_TERRITORIES_PROVINCES)
	cityTown = models.CharField('City/Town/County' , max_length = 60)

	# Investigator Metadata:
	investigator = models.CharField('Investigator' , max_length = 500 , blank = True)
	license = models.CharField('Investigator License' , max_length = 500 , blank = True)
	investigatorEmployer = models.CharField('Investigator Employer' , max_length = 500 , blank = True)

	# Contents Metadata:
	reportType = models.CharField('Report Type' , max_length = 2 , choices = choices.REPORT_TYPES , default = '0')
	client = models.CharField('Client' , max_length = 300 , blank = True)
	investigationID = models.CharField('Investigation ID' , max_length = 60 , blank = True)
	officerBadgeNumber = models.CharField('Officer Badge Number' , max_length = 60 , blank = True)
	incidentDate = models.DateTimeField('Incident Date' , null = True)
	reportDate = models.DateTimeField('Report Date' , default = timezone.now)

	# Contents:
	findingsSummary = models.TextField('Summary' , max_length = 10000 , blank = True)
	conclusion = models.TextField('Conclusion' , max_length = 10000 , blank = True)

	# References:
	fullReportURL = models.URLField('Full Report Download URL' , max_length = 300 , blank = True)
	fullArchiveURL = models.URLField('Full Archive Download URL' , max_length = 300 , blank = True)
	sourceURL = models.URLField('Source URL' , max_length = 300 , blank = True)
	praURL = models.URLField('Originating PRA Download URL' , max_length = 300 , blank = True)

	# Administrative:
	internalNotes = models.TextField('Internal Notes' , max_length = 10000 , blank = True)
	reportID = models.CharField('Report ID' , max_length = 36 , default = generateUniqueID)
	createdOn = models.DateTimeField('Record Created On' , auto_now_add = True)
	updatedOn = models.DateTimeField('Record Last Updated On' , auto_now = True)
	lastChangedBy = models.CharField('Last Changed By' , max_length = 50 , blank = True)
	toBeDeleted = models.BooleanField('Delete' , default = False)
	daysUntilDeletion = models.IntegerField('Days Until Deletion' , default = 30)

	# Permissions:
	approved = models.BooleanField('Record Approved' , default = False)
	public = models.BooleanField('Record Public' , default = False)


	def __str__(self):
		return (str(self.id) + ' - ' + self.reportDate.strftime('%x') + ' ' + self.client)



	# Manage metadata:
	class Meta:
		verbose_name = 'Investigative Report'
		verbose_name_plural = 'Investigative Reports'



class InvestigativeReportFinding(models.Model):
	# Related Models:
	investigativeReport = models.ForeignKey(InvestigativeReport , on_delete = models.CASCADE , verbose_name = 'Investigative Report')

	# Contents:
	findingPolicyCategory = models.CharField('Finding Policy Category' , max_length = 3 , choices = choices.POLICY_CATEGORIES)
	findingSummary = models.TextField('Summary of Finding' , max_length = 10000 , blank = True)
	findingBasis = models.CharField('Department Policy/Legal Code' , max_length = 500 , blank = True)
	finding = models.CharField('Finding' , max_length = 2 , choices = choices.FINDINGS , default = '0')

	# Administrative:
	internalNotes = models.TextField('Internal Notes' , max_length = 10000 , blank = True)
	createdOn = models.DateTimeField('Record Created On' , auto_now_add = True)
	updatedOn = models.DateTimeField('Record Last Updated On' , auto_now = True)
	lastChangedBy = models.CharField('Last Changed By' , max_length = 50 , blank = True)
	toBeDeleted = models.BooleanField('Delete' , default = False)
	daysUntilDeletion = models.IntegerField('Days Until Deletion' , default = 30)

	# Permissions:
	approved = models.BooleanField('Record Approved' , default = False)
	public = models.BooleanField('Record Public' , default = False)



	# Manage metadata:
	class Meta:
		verbose_name = 'Investigative Report Finding'
		verbose_name_plural = 'Investigative Report Findings'



class Tip(models.Model):
	# Contents:
	topic = models.CharField('Topic' , max_length = 2 , choices = choices.TIP_TOPICS , default = '6')
	message = models.TextField('Message' , max_length = 10000 , blank = False)

	# Status:
	encrypted = models.BooleanField('Encrypted' , default = False)
	viewed = models.BooleanField('Tip Viewed' , default = False)
	processed = models.BooleanField('Tip Processed' , default = False)
	archive = models.BooleanField('Archive' , default = False)
	archived = models.BooleanField('Archived' , default = False)
	daysUntilDeletion = models.IntegerField('Days Until Deletion' , default = 10)



	# Manage metadata:
	class Meta:
		verbose_name = 'Tip'
		verbose_name_plural = 'Tips'



	# Override the default save behavior to prevent unencrypted data from touching the database:
	def save(self , *args , **kwargs):
		if (self.encrypted):
			super().save(*args , **kwargs)
			return

		plaintextMessage = self.message
		self.message = 'This message has been saved in an encrypted format to an "Encrypted Message" object.'
		self.encrypted = True
		super().save(*args , **kwargs)

		gpg = GPG(gnupghome = '/home/ubuntu/.gnupg/')
		gpg.encoding = 'utf-8'

		fingerprints = []
		for key in gpg.list_keys():
			fingerprints.append(key['fingerprint'])

		for recipient in fingerprints:
			if (len(plaintextMessage) < 10000):
				encryptedMessage = str(gpg.encrypt(str(plaintextMessage) , recipient , always_trust = True))
				if (len(encryptedMessage) < 100000):
					EncryptedMessage.objects.create(parentTip = self , primaryPubKeyFingerprint = recipient , encryptedMessage = encryptedMessage)



class EncryptedMessage(models.Model):
	# Related Models:
	parentTip = models.ForeignKey(Tip , on_delete = models.CASCADE , verbose_name = 'Parent Tip')

	# Administrative:
	messageIsArchived = models.BooleanField('Message is Archived' , default = False)

	primaryPubKeyFingerprint = models.CharField('Primary Public Key Fingerprint' , max_length = 50 , blank = False)
	secondaryPubKeyFingerprint = models.CharField('Secondary Public Key Fingerprint' , max_length = 50 , blank = True)

	# Contents:
	encryptedMessage = models.TextField('Encrypted Message' , max_length = 100000 , blank = False)



	# Manage metadata:
	class Meta:
		verbose_name = 'Encrypted Message'
		verbose_name_plural = 'Encrypted Messages'



class APIAccount(models.Model):
	def generateAPIKey():
		while (True):
			proposedAPIKey = str(uuid4())
			if (len(APIAccount.objects.filter(apiKey = proposedAPIKey)) == 0):
				return proposedAPIKey


	# Profile:
	accountHolder = models.CharField('Account Holder' , max_length = 150)

	# Contents:
	apiKey = models.CharField('API Key' , max_length = 36 , default = generateAPIKey)
	weeklyQueryLimit = models.IntegerField('Weekly Query Limit' , default = 500)
	currentWeek = models.IntegerField('Number of Queries This Week' , default = 0)
	totalQueries = models.IntegerField('Lifetime Number of Queries' , default = 0)

	# Administrative:
	createdOn = models.DateTimeField('Account Created On' , auto_now_add = True)
	updatedOn = models.DateTimeField('Account Last Updated On' , auto_now = True)
	approved = models.BooleanField('Account Approved' , default = False)



	# Manage metadata:
	class Meta:
		verbose_name = 'API Account'
		verbose_name_plural = 'API Accounts'
