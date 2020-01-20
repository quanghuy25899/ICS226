from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from game.models import Player
import json
import game.constants

# Create your views here.
def index(request):
    map = [['_'] * game.constants.MAX_COLS for _ in range(game.constants.MAX_ROWS)]
    players = Player.objects.all()

    for player in players:
        map[player.row][player.col] = player.tag
    
    display = json.dumps(map)
    return HttpResponse(display)

def get_player(request, id):
    player = Player.objects.filter(id=id)
    if (len(player) == 1):
        return HttpResponse(json.dumps(player[0], cls=PlayerEncoder))
        # "Player %(id)s is at row %(row)s and col %(col)s" % {'id':player[0].tag, 'row':str(player[0].row), 'col':str(player[0].col)}
    else:
        return HttpResponse("No such player")

def get_all_player(request):
    players = Player.objects.all()
    display = []
    if (len(players) > 0):
        for player in players:
            display.append(json.dumps(player, cls=PlayerEncoder))
        return HttpResponse(display)
    else:
        return HttpResponse("No such player")

class PlayerCreate(CreateView):
    model = Player
    fields = '__all__'
    success_url = reverse_lazy('index')

class PlayerUpdate(UpdateView):
    model = Player
    fields = ['row', 'col']
    success_url = reverse_lazy('index')

class PlayerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Player):
            return { 'id' : obj.id, 'tag' : obj.tag, 'row' : obj.row, 'col' : obj.col }
        return json.JSONEncoder.default(self, obj)