from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from django.core.validators import MaxValueValidator
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

class Gita(models.Model):
    STATO_CHOICES = (
        ('IN_PROGRAMMA', 'In programma'),
        ('IN_CORSO', 'In corso'),
        ('TERMINATA', 'Terminata'),
    )
    
    
    Stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='IN_PROGRAMMA')
    Data_ritrovo = models.DateTimeField(null=True, blank=True)
    Data_rientro = models.DateTimeField(null=True, blank=True)
    Luogo_ritrovo = models.CharField(max_length=20)
    Luogo_rientro = models.CharField(max_length=20)
    Proposta_Gita = models.ForeignKey('Proposta_Gita', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.Proposta_Gita.Titolo
        
    class Meta:
         verbose_name_plural = 'Gita'

class Proposta_Gita(models.Model):
    STATO_CHOICES = (
        ('IN_ELABORAZIONE', 'In elaborazione'),
        ('CONFERMATA', 'Confermata'),
        ('RIFIUTATA', 'Rifiutata'),
    )
    Titolo = models.CharField(max_length=20)
    Descrizione = models.CharField(max_length=300)
    Data = models.DateTimeField(null=True, blank=True)
    Posto = models.CharField(max_length=20)
    Costo = models.FloatField()
    Stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='IN_ELABORAZIONE')

    def __str__(self):
        return self.Titolo

    class Meta:
         verbose_name_plural = 'Proposte_Gita'

class Attività(models.Model):
    STATO_CHOICES = (
        ('IN_ELABORAZIONE', 'In elaborazione'),
        ('CONFERMATA', 'Confermata'),
        ('RIFIUTATA', 'Rifiutata'),
    )
    Titolo = models.CharField(max_length=20)
    Descrizione = models.CharField(max_length=300)
    Costo = models.FloatField()
    Stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='IN_ELABORAZIONE')
    
    Proposta_Gita = models.ForeignKey('Proposta_Gita', on_delete=models.CASCADE)

    def __str__(self):
        return self.Titolo
        
    class Meta:
         verbose_name_plural = 'Attività'

class Docenti_gita(models.Model):
    Gita = models.ForeignKey('Gita', on_delete=models.CASCADE, default='')
    utente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default='')
    
    def __str__(self):
        return "{} - {}".format(self.Gita, self.utente.username)
        
    class Meta:
         verbose_name_plural = 'Docenti_gita'

class Documenti(models.Model):
    Titolo = models.CharField(max_length=20)
    Descrizione = models.CharField(max_length=300, default='')
    Gita = models.ForeignKey('Gita', on_delete=models.CASCADE, default='')
    Allegato = models.FileField(upload_to='documenti/',default='')

    def __str__(self):
        return self.Titolo
        
    class Meta:
         verbose_name_plural = 'Documenti'

class Classe_gita(models.Model):
    Gita = models.ForeignKey('Gita', on_delete=models.CASCADE, default='')
    Classe = models.ForeignKey('Classe', on_delete=models.CASCADE, default='')
    def __str__(self):
        return "{} - {}".format(self.Classe, self.Gita)
        
    class Meta:
         verbose_name_plural = 'Classe_gita'


class Classe(models.Model):
    anno = models.IntegerField(validators=[MaxValueValidator(5)],default=0)
    sezione = models.CharField(max_length=3,default='')


    def __str__(self):
        return "{}{}".format(self.anno, self.sezione)
        
    class Meta:
         verbose_name_plural = 'Classe'

class Presenti_prenotati(models.Model):
    Gita = models.ForeignKey('Gita', on_delete=models.CASCADE, default='')
    utente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default='')
    
    def __str__(self):
        return "{} - {}".format(self.Gita, self.utente.username)
        
    class Meta:
        verbose_name_plural = 'Presenti_prenotati'
