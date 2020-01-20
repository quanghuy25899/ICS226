from django.test import TestCase
from game.models import Player
import game.constants

# Create your tests here.
class PlayerTestCase(TestCase):
    def test_create(self):
        response = self.client.post("/game/player/create/", 
        { 'tag':'T', 'row':3, 'col':7 })
        p = Player.objects.get(tag='T')
        self.assertEqual(p.tag, 'T')
        self.assertEqual(p.row, 3)
        self.assertEqual(p.col, 7)
    
    def test_out_of_bounds_row_neg(self):
        response = self.client.post("/game/player/create/", { 'tag' : 'X', 'row' : -3, 'col' : 4})
        self.assertFormError(response, 'form', 'row', 'Out of range')
        try:
            Player.objects.get(tag='X')
            self.fail()
        except Player.DoesNotExist:
            pass

    def test_out_of_bounds_row_pos(self):
        response = self.client.post("/game/player/create/", { 'tag' : 'Y', 'row' : 11, 'col' : 4})
        self.assertFormError(response, 'form', 'row', 'Out of range')
        try:
            Player.objects.get(tag='Y')
            self.fail()
        except Player.DoesNotExist:
            pass

    def test_out_of_bounds_col_neg(self):
        response = self.client.post("/game/player/create/", { 'tag' : 'H', 'row' : 3, 'col' : -3 })
        self.assertFormError(response, 'form', 'col', 'Out of range')
        try:
            Player.objects.get(tag='H')
            self.fail()
        except Player.DoesNotExist:
            pass
    
    def test_out_of_bounds_col_pos(self):
        response = self.client.post("/game/player/create/", { 'tag' : 'G', 'row' : 3, 'col' : 11 })
        self.assertFormError(response, 'form', 'col', 'Out of range')
        try:
            Player.objects.get(tag='G')
            self.fail()
        except Player.DoesNotExist:
            pass
    
    def test_duplicate_tag(self):
        player1 = self.client.post("/game/player/create/", 
        { 'tag':'T', 'row':3, 'col':7 })
        try:
            player2 = self.client.post("/game/player/create/", 
            { 'tag':'T', 'row':3, 'col':7 })
            self.assertIn(b'Tag already taken', player2._container[0])
        except:
            pass
    
    def test_invalid_move_row_neg(self):
        response = self.client.post("/game/player/create/", 
        { 'tag':'T', 'row':0, 'col':0 })
        try:
            response_update = self.client.post("/game/player/1/update", 
            { 'row': -1, 'col' : 0 })
            self.assertIn(b'Out of range', response_update._container[0])
        except:
            pass


    def test_invalid_move_row_pos(self):
        response = self.client.post("/game/player/create/", 
        { 'tag':'T', 'row':9, 'col':0 })
        try:
            response_update = self.client.post("/game/player/1/update", 
            { 'row': 10, 'col' : 0 })
            self.assertIn(b'Out of range', response_update._container[0])
        except:
            pass
    
    def test_invalid_move_col_neg(self):
        response = self.client.post("/game/player/create/", 
        { 'tag':'T', 'row':0, 'col':0 })
        try:
            response_update = self.client.post("/game/player/1/update", 
            { 'row': 0, 'col' : -1 })
            self.assertIn(b'Out of range', response_update._container[0])
        except:
            pass

    def test_invalid_move_col_pos(self):
        response = self.client.post("/game/player/create/", 
        { 'tag':'T', 'row':0, 'col':9 })
        try:
            response_update = self.client.post("/game/player/1/update", 
            { 'row': 0, 'col' : 10 })
            self.assertIn(b'Out of range', response_update._container[0])
        except:
            pass
    
    def test_move_row_too_far(self):
        response = self.client.post("/game/player/create/", 
        { 'tag':'T', 'row':0, 'col':0 })
        try:
            response_update = self.client.post("/game/player/1/update", 
            { 'row': 3, 'col' : 0 })
            self.assertIn(b'Row too far', response_update._container[0])
        except:
            pass
    
    def test_move_col_too_far(self):
        response = self.client.post("/game/player/create/", 
        { 'tag':'T', 'row':0, 'col':0 })
        try:
            response_update = self.client.post("/game/player/1/update", 
            { 'row': 0, 'col' : 3 })
            self.assertIn(b'Row too far', response_update._container[0])
        except:
            pass