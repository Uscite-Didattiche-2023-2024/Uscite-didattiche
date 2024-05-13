from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.conf import settings

character = RegexValidator(r'^[A-Z]*$', 'Only CAPS characters are allowed.')

def get_default_group():
    try:
        group = Group.objects.get(name='')
        return group.id 
    except Group.DoesNotExist:
        return None
    
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
    Creatore = models.ForeignKey(User, on_delete=models.CASCADE)

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
    Allegato = models.FileField(upload_to='documenti/', default='')
#    group = models.ForeignKey(Group, related_name="documenti", on_delete=models.CASCADE, default=get_default_group)
    groups = models.ManyToManyField(Group, related_name="documenti")

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
    anno = models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(1)])
    sezione = models.CharField(max_length=3,default='',validators=[character])


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

class Notifica(models.Model):
    Titolo = models.CharField(max_length=20)
    Descrizione = models.CharField(max_length=300, default='')
    Gita = models.ForeignKey('Gita', on_delete=models.CASCADE, default='')
    Proposta_Gita = models.ForeignKey('Proposta_Gita', on_delete=models.CASCADE, default='')
    Classe = models.ForeignKey('Classe', on_delete=models.CASCADE, default='')
    Documenti = models.ForeignKey('Documenti', on_delete=models.CASCADE, default='')


    groups = models.ManyToManyField(Group, related_name="notifica")

    def __str__(self):
        return self.Titolo

    class Meta:
        verbose_name_plural = 'Notifica'
