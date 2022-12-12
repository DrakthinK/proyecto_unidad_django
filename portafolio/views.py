from django.shortcuts import render,redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from portafolio.forms import  ProyectoForm
from portafolio.models import Proyecto,Ipvisitante
from ipware import get_client_ip

# Create your views here.
class Inicio(View):

    #login_url = '/signin/'
    template_get = "inicio.html"
    def get(self,request):
        context={}
        if User.is_authenticated:
            context ={'usuario':User}
        return render(request, self.template_get, context)


class perfilportafolio(LoginRequiredMixin,View):

    #login_url = '/signin/'
    template_get = "index.html"
    def get(self,request,usuario):
        context={}
        if User.is_authenticated:
            proyectos=Proyecto.objects.filter(usuario_id=request.user.id)
            #print(proyectos)
            context ={'usuario':usuario,
                      'proyectos':proyectos}

            #print(User)
        return render(request, self.template_get, context)

class CrearPortafolio(LoginRequiredMixin,View):
    #login_url = '/signin/'
    def get(self,request):
        return render(request,"crearportafolio.html",{
            'form':ProyectoForm()
        })
    def post(self,request):

            formulario = ProyectoForm(request.POST,request.FILES)
            if formulario.is_valid():
                titulo = formulario.cleaned_data["titulo"]
                descripcion = formulario.cleaned_data["descripcion"]
                fecha = formulario.cleaned_data["fecha"]
                tag=formulario.cleaned_data["tag"]
                url_github = formulario.cleaned_data["url_github"]
                foto = formulario.cleaned_data["foto"]

                obj = Proyecto.objects.create(
                    titulo=titulo,
                    descripcion=descripcion,
                    fecha=fecha,
                    tag=tag,
                    url_github=url_github,
                    foto=foto,
                    usuario =request.user
                )
                obj.save()
                return redirect("perfil",usuario=request.user.username)
            else:
                #print(formulario.cleaned_data['foto'])
                return render(request,"crearportafolio.html",{
                'form':ProyectoForm(),
                "errores":"error al validar formulario"
                })


class VerDetalleProyecto(LoginRequiredMixin,View):
      def get(self,request,id):
          proyecto=Proyecto.objects.get(usuario_id=request.user.id,id=id)
          return render(request,'detalleproyecto.html',{
              'proyecto':proyecto
          })


class verIps(LoginRequiredMixin, View):
    def get(self, request):
        #proyecto = Proyecto.objects.get(usuario_id=request.user.id, id=id)
        ip, is_routable = get_client_ip(request)
        print(ip)
        print(is_routable)
        ip_current=Ipvisitante.objects.filter(ipvisita=ip).first()
        print(ip_current)
        if ip_current is  None:
            #return HttpResponse("xd")
            ip=Ipvisitante.objects.create(
                ipvisita=ip
                    )
            ip.save()
        IPS=Ipvisitante.objects.filter(ipvisita=ip)
        return render(request, 'ipvisitas.html', {
            'IPS': IPS
        })

class InfoPerfilDetalle(LoginRequiredMixin,View):
    #login_url = '/signin/'
    def get(self,request):
        return render(request,"about.html")

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:
        if len(request.POST['username'])==0 or  len(request.POST['password1'])==0 or len(request.POST['password2'])==0:
            return render(request, 'signup.html', {"form": UserCreationForm, "error": "no se permiten campos vacios"})

        if request.POST["password1"] == request.POST["password2"]:
            try:
                #usuario = User.objects.get(username=request.POST["username"])
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                #request.session['usuario'] = request.POST["username"]
                return redirect('perfil', request.POST["username"])
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:

        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        #request.session["name_usuario"]=user.get_username()
        #request.session["id_usuario"]=user.id

        return redirect('perfil',usuario=user.get_username())

@login_required
def contacto(request):
    if request.method=='GET':
        return  render(request,'contacto.html')
    else:
        return  HttpResponse("OK LOGICA ENVIAR CORREO")
@login_required
def signout(request):
    logout(request)
    return redirect('inicio')


#ipware
