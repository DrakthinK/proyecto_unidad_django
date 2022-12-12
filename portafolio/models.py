import datetime

from django.db import models
from django.contrib.auth.models import User
class Proyecto(models.Model):
        foto=models.ImageField(upload_to="portfolio/images")
        fecha = models.DateField(null=True)
        fecha_creacion = models.DateTimeField(default=datetime.datetime.now())
        titulo = models.TextField()
        descripcion = models.TextField()
        tag=models.TextField()
        url_github=models.URLField(blank=True)
        usuario= models.ForeignKey(User, on_delete=models.CASCADE)
        def __str__(self):
            return self.titulo

        def to_json(self):
            Proyecto_json={
                 'foto':self.foto,
                 'fecha':str(self.fecha),
                 'titulo':self.titulo,
                 'descripcion':self.descripcion,
                 'tag':self.tag,
                 'url_github':self.url_github
            }

            return Proyecto_json


class Ipvisitante(models.Model):
      ipvisita=models.CharField(max_length=100)
      fecha_creacion = models.DateTimeField(default=datetime.datetime.now())
      def __str__(self):
          return self.ipvisita