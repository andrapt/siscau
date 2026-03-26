from django.db import models

class TipoFertilizante(models.Model):
    nome = models.CharField(max_length=45)

    def __str__(self):
        return self.nome

class Fertilizante(models.Model):
    nome = models.CharField(max_length=45)
    fabricante = models.CharField(max_length=45)
    linha = models.CharField(max_length=45)
    forma_fisica = models.CharField(max_length=128)
    finalidade = models.CharField(max_length=128)
    nutrientes_primarios = models.CharField(max_length=128)
    nutrientes_secundarios = models.CharField(max_length=128)
    micronutrientes = models.CharField(max_length=128, null=True)
    fonte_nutrientes = models.CharField(max_length=128, null=True)
    data_cadastro = models.DateField(auto_now_add=True)
    tipo_fertilizante = models.ForeignKey(TipoFertilizante, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
