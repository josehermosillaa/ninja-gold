from django.shortcuts import render, HttpResponse, redirect
from random import randint

def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        if request.POST['name'] == '':
            context = {'mensaje': 'Ingrese un nombre de usuario valido'}
            return render(request, 'index.html', context)
        else:
            name_from_form = request.POST['name']
            request.session['name'] = request.POST['name']
            return redirect('/condiciones')


def condiciones(request):
    if request.method == 'GET':
        return render(request, 'condiciones.html')

    else:
        request.session['condicion1'] = request.POST['condicion1']
        request.session['condicion2'] = request.POST['condicion2']

        return redirect('/ninja_gold')


def ninja_gold(request):
    oro = request.session.get('oro', 0)

    if 'oro' not in request.session:
        request.session['oro'] = 0

    if 'turnos' not in request.session:
        request.session['turnos'] = 0
    context = {'oro': request.session['oro'], 
                'Turnos': request.session['condicion1'],
                'MaxOro': request.session['condicion2']}

    return render(request, 'ninja_gold.html', context)

def set_defaults(request):

    if 'turnos' not in request.session:
        request.session['turnos'] = 0

    if 'condicion1' not in request.session:
        request.session['condicion1'] = 10
    
    if 'condicion2' not in request.session:
        request.session['condicion2'] = 250
    
    if 'activities' not in request.session:
        request.session['activities'] = []

def process_money(request):
    turnos = request.session.get('turnos',0)
    Maxturnos = int(request.session.get('condicion1',10))
    Aoro = request.session.get('oro',0)
    MaxOro = int(request.session.get('condicion2',240))

    set_defaults(request)

    oro = 0 
    
    if request.POST['place'] == 'granja':
        oro = randint(10,20)
        request.session['turnos'] += 1
        
    
    elif request.POST['place'] == 'cueva':
        oro = randint(5,10)
        request.session['turnos'] += 1
    
    elif request.POST['place'] == 'casa':
        oro = randint(2,5)
        request.session['turnos'] += 1
    
    else:
        oro = randint(-50,50)
        request.session['turnos'] += 1

    request.session['oro'] += oro
    
    if oro > 0:
        request.session['activities'].insert(0,{
            'text': f"Obtuviste {oro} de Oro en la {request.POST['place']}",
            'oro': oro
        })
        
    else:
        request.session['activities'].insert(0,{
            'text': f"Perdiste {oro} de oro en el Casino",
            'oro': oro
        })
    request.session.save()

    if Aoro >= MaxOro:
        request.session['msg'] = "Felicidades has ganado"
        request.session['img'] =  "https://img.freepik.com/free-vector/pixel-art-luxury-treasure-pile_150088-456.jpg?size=626&ext=jpg&ga=GA1.2.501542633.1626566400"
        return redirect('/end')

    elif turnos >= Maxturnos or Aoro <0:
        request.session['msg'] = "Fin del juego"
        request.session['img'] = "https://www.8bitish.com/wp-content/uploads/2019/05/change_bridge_animated.gif"
        return redirect('/end')
    print(Aoro)
    return redirect('/ninja_gold')

def reset(request):
    request.session['turnos'] = 0
    request.session['oro'] = 0
    request.session['activities'] = []

    return redirect('/ninja_gold')
    

def end(request):
    if request.method == 'GET':
        reset(request)
    return render(request,'end.html')
    
def logout(request):    
    del request.session['name']
    return redirect('/')
