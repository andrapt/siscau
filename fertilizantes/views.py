from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib import messages
from datetime import datetime
from . models import Fertilizante
from . forms import FertilizanteForm


def listaFertilizantes (request):
    fertilizantes = Fertilizante.objects.all()
    context = {"fertilizantes": fertilizantes}
    
    return render(request, "listaFertilizantes.html", context)

def informar (request, id):
    fertilizante = Fertilizante.objects.get(id=id)
    context = {"fertilizante": fertilizante}
    
    return render(request, "informar.html", context)

def mensagem(request):
    hora_atual = datetime.now().hour
    if hora_atual < 12:
        saudacao = "Bom dia!"
    elif hora_atual < 18:
        saudacao = "Boa tarde!"
    else:
        saudacao = "Boa noite!"

    fertilizantes = {
         "Nitrogênio",
         "Fosfato",
         "Potássio"
    }
    nome = "Arley de Andrade Pinto"
    return render(request,"mensagem.html", {"nome":nome, "saudacao": saudacao, "fertilizantes": fertilizantes})

def saudacao(request, nome):
    mensagem = f"Olá, {nome}! Bem-vindo ao sistema de controle de fertilizantes!"
    return HttpResponse(mensagem)

def novo_fertilizante(request):
    if request.method == "POST":
        form = FertilizanteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fertilizante cadastrado com sucesso!")
            return redirect('fertilizantes')
    else:
        form = FertilizanteForm()

    return render(request, "novo_fertilizante.html", {"form": form})

def editar_fertilizante(request, id):
    fertilizante = get_object_or_404(Fertilizante,id=id)
    if request.method == "POST":
        form = FertilizanteForm(request.POST, instance=fertilizante)
        if form.is_valid():
            form.save()
            messages.success(request, "Fertilizante atualizado com sucesso!")
            return redirect('fertilizantes')
    else:
        form = FertilizanteForm(instance=fertilizante)

    return render(request, "novo_fertilizante.html", {"form": form, 'editar':True})