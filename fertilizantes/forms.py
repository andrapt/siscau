from django import forms
from .models import Fertilizante

class FertilizanteForm(forms.ModelForm):
    class Meta:
        model = Fertilizante
        fields = '__all__'
        widgets = {
            'data_cadastro': forms.DateInput(attrs={'type': 'date'}),
            'tipo_fertilizante': forms.Select(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'fabricante': forms.TextInput(attrs={'class': 'form-control'}),
            'linha': forms.TextInput(attrs={'class': 'form-control'}),
            'forma_fisica': forms.TextInput(attrs={'class': 'form-control'}),
            'finalidade': forms.TextInput(attrs={'class': 'form-control'}),
            'nutrientes_primarios': forms.TextInput(attrs={'class': 'form-control'}),
            'nutrientes_secundarios': forms.TextInput(attrs={'class': 'form-control'}),
            'micronutrientes': forms.TextInput(attrs={'class': 'form-control'}),
            'fonte_nutrientes': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        if len(nome) < 4:
            raise forms.ValidationError("O nome deve ter pelo menos 5 caracteres.")
        return nome
