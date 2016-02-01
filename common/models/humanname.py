from django.db import models

#Clase HumanName
#Seg�n FHIR "A name of a human with text, parts and usage information."
#Mas Info: https://www.hl7.org/fhir/datatypes.html#HumanName
class HumanName(models.Model):
    #constantes para use (https://www.hl7.org/fhir/valueset-name-use.html)
    USUAL = 'usual'
    OFFICIAL = 'official'
    TEMP = 'temp'
    NICK = 'nickname'
    ANONYMOUS = 'anonymous'
    OLD = 'old'
    MAIDEN = 'maiden'

    #choices para use
    USE_CHOICES=(
        (USUAL, 'Usual'),
        (OFFICIAL, 'Official'),
        (TEMP, 'Temporal'),
        (NICK, 'Nickname'),
        (ANONYMOUS, 'Anonymous'),
        (OLD, 'Old'),
        (MAIDEN, 'Maiden')
    )

    use = models.CharField(max_length=9, choices=USE_CHOICES, default=USUAL)                #usual | official | temp | nickname | anonymous | old | maiden
    text = models.TextField()                                                               #Text representation of the full name
    family = models.TextField()                                                             #Family name (often called 'Surname') - debe devolverse como  una colecci�n
    given = models.TextField()                                                              #Given names (not always 'first'). Includes middle names - debe devolverse como una colecci�n
    prefix = models.TextField()                                                             #Parts that come before the name - debe devolverse como una colecci�n
    suffix = models.TextField()                                                             #Parts that come after the name - debe devolverse como una colecci�n
    period = models.ForeignKey("NamePeriod")                                                  #Time period when name was/is in use

#Periodo de tiempo en el que un nombre es valido
#La estructura sigue las definiciones de FHIR en https://www.hl7.org/fhir/datatypes.html#Period
class NamePeriod(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
