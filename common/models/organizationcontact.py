from django.db import models

#Clase OrganizationContact
#Seg�n FHIR= "Contact for the organization for a certain purpose"
class OrganizationContact(models.Model):
    #Constantes para type (https://www.hl7.org/fhir/valueset-contactentity-type.html)
    BILL = 'bill'
    ADMIN = 'adm'
    HR = 'hr'
    PAYOR = 'pay'
    PATINF = 'pat'
    PRESS = 'pres'

    #Opciones del purpose
    PURPOSE_CHOICES = (
        (BILL, 'Billing'),
        (ADMIN, 'Administrative'),
        (HR, 'Human Resource'),
        (PAYOR, 'Payor'),
        (PATINF, 'Patient'),
        (PRESS, 'Press')
    )

    purpose = models.CharField(max_length=4, choices=PURPOSE_CHOICES, default=ADMIN)                #The type of contact
    name = models.ForeignKey("HumanName")                                                             #A name associated with the contact
    telecom = models.ForeignKey("ContactPoint")                                                       #Contact details (telephone, email, etc.) for a contact
    address = models.ForeignKey("Address")                                                            #Visiting or postal addresses for the contact
