from django.contrib import admin
from .models import Gita
from .models import Proposta_Gita
from .models import Attività
from .models import Docenti_gita
from .models import Documenti
from .models import Classe_gita
from .models import Classe
from .models import Presenti_prenotati
from .models import Notifica
from .models import User_classe



# Register your models here.
admin.site.register(Gita)
admin.site.register(Proposta_Gita)
admin.site.register(Attività)
admin.site.register(Docenti_gita)
admin.site.register(Documenti)
admin.site.register(Classe_gita)
admin.site.register(Classe)
admin.site.register(Presenti_prenotati)
admin.site.register(Notifica)
admin.site.register(User_classe)


