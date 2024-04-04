from django.db import models

class Gita(models.Model):
    STATO_CHOICES = (
        ('IN_PROGRAMMA', 'In programma'),
        ('IN_CORSO', 'In corso'),
        ('TERMINATA', 'Terminata'),
    )

    Nome = models.CharField(max_length=20)
    Prezzo = models.FloatField()
    Stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='IN_PROGRAMMA')
    Data_partenza = models.DateTimeField(null=True, blank=True)
    Data_ritorno = models.DateTimeField(null=True, blank=True)
    Luogo_partenza = models.CharField(max_length=20)
    Luogo_ritorno = models.CharField(max_length=20)
    Proposta_Gita = models.ForeignKey('Proposta_Gita', on_delete=models.CASCADE)

    def __str__(self):
        return self.Nome
        
    class Meta:
         verbose_name_plural = 'Gita'

class Proposta_Gita(models.Model):
    STATO_CHOICES = (
        ('IN_ELABORAZIONE', 'In elaborazione'),
        ('CONFERMATA', 'Confermata'),
        ('RIFIUTATA', 'Rifiutata'),
    )
    Nome = models.CharField(max_length=20)
    Descrizione = models.CharField(max_length=300)
    Data_partenza = models.DateTimeField(null=True, blank=True)
    Luogo = models.CharField(max_length=20)
    Prezzo = models.FloatField()
    Stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='IN_ELABORAZIONE')

    def __str__(self):
        return self.Nome

    class Meta:
         verbose_name_plural = 'Proposte_Gita'

class Attività(models.Model):
    STATO_CHOICES = (
        ('IN_ELABORAZIONE', 'In elaborazione'),
        ('CONFERMATA', 'Confermata'),
        ('RIFIUTATA', 'Rifiutata'),
    )
    Nome = models.CharField(max_length=20)
    Descrizione = models.CharField(max_length=300)
    prezzo = models.FloatField()
    
    Stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='IN_ELABORAZIONE')

    Proposta_Gita = models.ForeignKey('Proposta_Gita', on_delete=models.CASCADE)

    def __str__(self):
        return self.Nome
        
    class Meta:
         verbose_name_plural = 'Attività'

class Docenti_gita(models.Model):
    Nome = models.CharField(max_length=20)
    prezzo = models.FloatField()

    def __str__(self):
        return self.Nome
        
    class Meta:
         verbose_name_plural = 'Docenti_gita'

class Documenti(models.Model):
    Nome = models.CharField(max_length=20)
    prezzo = models.FloatField()

    def __str__(self):
        return self.Nome
        
    class Meta:
         verbose_name_plural = 'Documenti'

class Classe_gita(models.Model):
    Nome = models.CharField(max_length=20)
    prezzo = models.FloatField()

    def __str__(self):
        return self.Nome
        
    class Meta:
         verbose_name_plural = 'Classe_gita'


class Classe(models.Model):
    Nome = models.CharField(max_length=20)
    prezzo = models.FloatField()

    def __str__(self):
        return self.Nome
        
    class Meta:
         verbose_name_plural = 'Classe'

class Presenti_prenotati(models.Model):
    Nome = models.CharField(max_length=20)
    prezzo = models.FloatField()

    def __str__(self):
        return self.Nome
        
    class Meta:
         verbose_name_plural = 'Presenti_prenotati'