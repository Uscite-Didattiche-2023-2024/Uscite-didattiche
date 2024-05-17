from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    
    # Opzioni per il campo 'caratteristiche'
    CARATTERISTICHE_CHOICES = [
        ('nessuna', 'Nessuna'),  
        ('dsa', 'DSA'),
        ('invalido', 'Invalido'),
        ('allergico', 'Allergico'),
        # Aggiungi altre opzioni se necessario
    ]
    
    # Usa il campo ChoiceField per le caratteristiche
    caratteristiche = models.CharField(max_length=100, choices=CARATTERISTICHE_CHOICES, blank=True, null=True) 
    tipi_allergie = models.CharField(max_length=100, blank=True, null=True)  # Aggiungi questo campo

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        # Se la caratteristica è cambiata in qualcosa di diverso da 'allergico', ripulisce 'tipi_allergie'
        if self.caratteristiche != 'allergico':
            self.tipi_allergie = ''
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
