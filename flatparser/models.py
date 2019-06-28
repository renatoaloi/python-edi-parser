from django.db import models

class EdiFile(models.Model):
    resumo_operacoes = models.IntegerField()
    valor_venda = models.FloatField()

    tipo_registro = models.CharField(max_length=200)
    date_created = models.DateField(auto_now_add=True)
