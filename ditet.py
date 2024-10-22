from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineRightIconListItem
from string import whitespace, ascii_letters, punctuation
from kivy.uix.label import Label
from kivymd.uix.menu import MDDropdownMenu  
from kivy.properties import ObjectProperty
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.treeview import TreeView, TreeViewLabel, TreeViewNode
from kivymd.uix.button import MDIconButton
from kivymd.uix.textfield import MDTextField
import string
from kivy.properties import StringProperty
import kivy
import json
from os.path import dirname, join
import shutil
import sqlite3
from socket import socket, AF_INET, SOCK_DGRAM, gethostbyname, gethostname
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.clock import Clock
from functools import partial
from kivy.lang import Builder
import sys
import os


os.environ['KIVY_IMAGE'] = 'pil,sdl2'
sys.setrecursionlimit(5000)

kivy.require('2.3.0')

class DeletePopup(Popup):
    def delete_diet(self):
        app = MDApp.get_running_app()
        disk = DiskMaster()
        name = app.root.ids.scr.children[0].diet_option_clicked.text + ".json"
        disk.delete_diet(name)
        app.root.ids.scr.children[0].display_diets()
        
    def delete_diet_clicked_variable(self):
        app = MDApp.get_running_app()
        app.root.ids.scr.children[0].diet_option_clicked = 0
        
class ChangeNamePopup(Popup):
    def change_diet_name(self):
        if self.ids.new_diet_name_tf.text == "" or self.ids.new_diet_name_tf.text == ".":
            pass
        else:
            app = MDApp.get_running_app()
            disk = DiskMaster()
            disk.change_diet_name(app.root.ids.scr.children[0].diet_option_clicked.text + ".json", self.ids.new_diet_name_tf.text + ".json")
            app.root.ids.scr.children[0].diet_option_clicked = 0 
            app.root.ids.scr.children[0].display_diets() 
            self.dismiss()
            
    def delete_diet_clicked_variable(self):
        app = MDApp.get_running_app()
        app.root.ids.scr.children[0].diet_option_clicked = 0
 
class NewDietIngredient(BoxLayout):
    food = StringProperty("")
    brand = StringProperty("")
    weight = StringProperty("")
    
    
    def delete_ingredient(self, instance1, instance2):
        app = MDApp.get_running_app()
        app.root.ids.scr.children[0].delte(instance1, instance2)
        instance1.remove_widget(instance2)
        
        
class NewDietListItem(OneLineRightIconListItem):
    def generate_diet_options(self,instance):
        app = MDApp.get_running_app()
        app.root.ids.scr.children[0].diet_options(instance)

class CalculatorFoodBlock(MDGridLayout):
    ...


class DietScreen(MDScreen):

    diet_option_clicked = 0
    def display_diets(self):
        disk = DiskMaster()
        diets = disk.list_all_diets()
        self.ids.box.clear_widgets()
        if diets == "":
            pass
        else:
            for diet in diets:
                self.ids.box.add_widget(NewDietListItem(text= diet.removesuffix(".json")))
                
    def buttonClicked(self):
        disk = DiskMaster()
        disk.create_diet()
        self.display_diets()
    
    def duplicate_diet(self):
        disk = DiskMaster()
        disk.duplicate_diet(self.diet_option_clicked.text)
        self.diet_option_clicked = 0 
        self.display_diets() 
          
    
    def set_diet_option__clicked(self, instance):
        self.diet_option_clicked = instance
    
    def diet_options(self, instance):
        menu_list = [
                    {
                        "viewclass": "OneLineListItem",
                        "text": "Cambiar Nombre",
                        "on_release": lambda x = "Cambiar Nombre": (ChangeNamePopup().open(),self.menu.dismiss())
                    },
                    {
                        "viewclass": "OneLineListItem",
                        "text": "Duplicar",
                        "on_release": lambda x = "Duplicar": (self.duplicate_diet(), self.menu.dismiss())
                    },
                    {
                        "viewclass": "OneLineListItem",
                        "text": "Eliminar",
                        "on_release": lambda x = "Eliminar": (DeletePopup().open(),self.menu.dismiss())
                    }
                    
                ]
        self.menu = MDDropdownMenu(
            caller = instance,
            items = menu_list,
            width_mult = 3
            )
        self.menu.open()
        
class DietInsightScreen(MDScreen):
    groupName = ObjectProperty(None)
    popup = ObjectProperty(None)
    id_focused = ""
    value = ""
    value2 = ""
    
    def set_value2(self,text):
        try:
            self.value2 = int(text)
        
        except:
            self.value2 = "0"
    
    def set_value(self,instance):
        self.value = instance.text
    
    def update_results_k(self):
        self.ids.kcal_food_result.text = str(round(float(self.ids.kcal_food_result_1.text) + float(self.ids.kcal_food_result_2.text) + float(self.ids.kcal_food_result_3.text) + float(self.ids.kcal_food_result_4.text) + float(self.ids.kcal_food_result_5.text) + float(self.ids.kcal_food_result_6.text),1) )
    def update_results_p(self):
        self.ids.proteins_food_result.text = str(round(float(self.ids.proteins_food_result_1.text) + float(self.ids.proteins_food_result_2.text) + float(self.ids.proteins_food_result_3.text) + float(self.ids.proteins_food_result_4.text) + float(self.ids.proteins_food_result_5.text) + float(self.ids.proteins_food_result_6.text),1))

    def update_results_c(self):
        self.ids.carbohydrates_food_result.text = str(round(float(self.ids.carbohydrates_food_result_1.text) + float(self.ids.carbohydrates_food_result_2.text) + float(self.ids.carbohydrates_food_result_3.text) + float(self.ids.carbohydrates_food_result_4.text) + float(self.ids.carbohydrates_food_result_5.text) + float(self.ids.carbohydrates_food_result_6.text),1))

    def update_results_s(self):
        self.ids.sugar_food_result.text = str(round(float(self.ids.sugar_food_result_1.text) + float(self.ids.sugar_food_result_2.text) + float(self.ids.sugar_food_result_3.text) + float(self.ids.sugar_food_result_4.text) + float(self.ids.sugar_food_result_5.text) + float(self.ids.sugar_food_result_6.text),1))

    def update_results_l(self):
        self.ids.lipids_food_result.text = str(round(float(self.ids.lipids_food_result_1.text) + float(self.ids.lipids_food_result_2.text) + float(self.ids.lipids_food_result_3.text) + float(self.ids.lipids_food_result_4.text) + float(self.ids.lipids_food_result_5.text) + float(self.ids.lipids_food_result_6.text),1))

    def update_results_sa(self):
        self.ids.salt_food_result.text = str(round(float(self.ids.salt_food_result_1.text) + float(self.ids.salt_food_result_2.text) + float(self.ids.salt_food_result_3.text) + float(self.ids.salt_food_result_4.text) + float(self.ids.salt_food_result_5.text) + float(self.ids.salt_food_result_6.text),1))

        
    def delte(self, instance1, instance2):
        db = DBMaster()
        if instance2.ids.food_name.text != "" and instance2.ids.brand_name.text != "" and instance2.ids.weight_name.text != "":        
            values =db.get_food_values(instance2.ids.food_name.text, instance2.ids.brand_name.text)
            for f in self.ids.food_1.children:
                if f == instance2:
                    self.ids.proteins_food_result_1.text = str(round(float(self.ids.proteins_food_result_1.text)- float(values[0][0])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.carbohydrates_food_result_1.text = str(round(float(self.ids.carbohydrates_food_result_1.text)- float(values[0][1])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.sugar_food_result_1.text = str(round(float(self.ids.sugar_food_result_1.text)- float(values[0][2])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.lipids_food_result_1.text = str(round(float(self.ids.lipids_food_result_1.text)- float(values[0][3])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.salt_food_result_1.text = str(round(float(self.ids.salt_food_result_1.text)- float(values[0][4])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.kcal_food_result_1.text = str(round(float(self.ids.kcal_food_result_1.text)- float(values[0][5])*float(instance2.ids.weight_name.text)/100,1)) 
                    return
           
            for f in self.ids.food_2.children:
                if f == instance2:
                    self.ids.proteins_food_result_2.text = str(round(float(self.ids.proteins_food_result_2.text)- float(values[0][0])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.carbohydrates_food_result_2.text = str(round(float(self.ids.carbohydrates_food_result_2.text)- float(values[0][1])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.sugar_food_result_2.text = str(round(float(self.ids.sugar_food_result_2.text)- float(values[0][2])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.lipids_food_result_2.text = str(round(float(self.ids.lipids_food_result_2.text)- float(values[0][3])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.salt_food_result_2.text = str(round(float(self.ids.salt_food_result_2.text)- float(values[0][4])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.kcal_food_result_2.text = str(round(float(self.ids.kcal_food_result_2.text)- float(values[0][5])*float(instance2.ids.weight_name.text)/100,1)) 
                    return
            
            for f in self.ids.food_3.children:
                if f == instance2:
                    self.ids.proteins_food_result_3.text = str(round(float(self.ids.proteins_food_result_3.text)- float(values[0][0])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.carbohydrates_food_result_3.text = str(round(float(self.ids.carbohydrates_food_result_3.text)- float(values[0][1])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.sugar_food_result_3.text = str(round(float(self.ids.sugar_food_result_3.text)- float(values[0][2])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.lipids_food_result_3.text = str(round(float(self.ids.lipids_food_result_3.text)- float(values[0][3])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.salt_food_result_3.text = str(round(float(self.ids.salt_food_result_3.text)- float(values[0][4])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.kcal_food_result_3.text = str(round(float(self.ids.kcal_food_result_3.text)- float(values[0][5])*float(instance2.ids.weight_name.text)/100,1)) 
                    
            for f in self.ids.food_4.children:
                if f == instance2:
                    self.ids.proteins_food_result_4.text = str(round(float(self.ids.proteins_food_result_4.text)- float(values[0][0])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.carbohydrates_food_result_4.text = str(round(float(self.ids.carbohydrates_food_result_4.text)- float(values[0][1])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.sugar_food_result_4.text = str(round(float(self.ids.sugar_food_result_4.text)- float(values[0][2])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.lipids_food_result_4.text = str(round(float(self.ids.lipids_food_result_4.text)- float(values[0][3])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.salt_food_result_4.text = str(round(float(self.ids.salt_food_result_4.text)- float(values[0][4])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.kcal_food_result_4.text = str(round(float(self.ids.kcal_food_result_4.text)- float(values[0][5])*float(instance2.ids.weight_name.text)/100,1)) 
                    return
            
            for f in self.ids.food_5.children:
                if f == instance2:
                    self.ids.proteins_food_result_5.text = str(round(float(self.ids.proteins_food_result_5.text)- float(values[0][0])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.carbohydrates_food_result_5.text = str(round(float(self.ids.carbohydrates_food_result_5.text)- float(values[0][1])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.sugar_food_result_5.text = str(round(float(self.ids.sugar_food_result_5.text)- float(values[0][2])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.lipids_food_result_5.text = str(round(float(self.ids.lipids_food_result_5.text)- float(values[0][3])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.salt_food_result_5.text = str(round(float(self.ids.salt_food_result_5.text)- float(values[0][4])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.kcal_food_result_5.text = str(round(float(self.ids.kcal_food_result_5.text)- float(values[0][5])*float(instance2.ids.weight_name.text)/100,1)) 
                    return
                    
            for f in self.ids.food_6.children:
                if f == instance2:
                    self.ids.proteins_food_result_6.text = str(round(float(self.ids.proteins_food_result_6.text)- float(values[0][0])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.carbohydrates_food_result_6.text = str(round(float(self.ids.carbohydrates_food_result_6.text)- float(values[0][1])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.sugar_food_result_6.text = str(round(float(self.ids.sugar_food_result_6.text)- float(values[0][2])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.lipids_food_result_6.text = str(round(float(self.ids.lipids_food_result_6.text)- float(values[0][3])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.salt_food_result_6.text = str(round(float(self.ids.salt_food_result_6.text)- float(values[0][4])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.kcal_food_result_6.text = str(round(float(self.ids.kcal_food_result_6.text)- float(values[0][5])*float(instance2.ids.weight_name.text)/100,1)) 
                    return
    
    def recom_salt(self):
        pass
    
    def disable_diet_ingredient(self):
        for a in self.ids.food_1.children:
            if "NewDietIngredient" in str(a):
                a.ids.food_name.disabled = True
                a.ids.brand_name.disabled = True
                a.ids.weight_name.disabled = True
                a.ids.delete_ingredient_diet.disabled = True
                
        for a in self.ids.food_2.children:
            if "NewDietIngredient" in str(a):
                a.ids.food_name.disabled = True
                a.ids.brand_name.disabled = True
                a.ids.weight_name.disabled = True
                a.ids.delete_ingredient_diet.disabled = True
                
        for a in self.ids.food_3.children:
            if "NewDietIngredient" in str(a):
                a.ids.food_name.disabled = True
                a.ids.brand_name.disabled = True
                a.ids.weight_name.disabled = True
                a.ids.delete_ingredient_diet.disabled = True
                
        for a in self.ids.food_4.children:
            if "NewDietIngredient" in str(a):
                a.ids.food_name.disabled = True
                a.ids.brand_name.disabled = True
                a.ids.weight_name.disabled = True
                a.ids.delete_ingredient_diet.disabled = True
                
        for a in self.ids.food_5.children:
            if "NewDietIngredient" in str(a):
                a.ids.food_name.disabled = True
                a.ids.brand_name.disabled = True
                a.ids.weight_name.disabled = True
                a.ids.delete_ingredient_diet.disabled = True
                
        for a in self.ids.food_6.children:
            if "NewDietIngredient" in str(a):
                a.ids.food_name.disabled = True
                a.ids.brand_name.disabled = True
                a.ids.weight_name.disabled = True
                a.ids.delete_ingredient_diet.disabled = True
        
    def enable_diet_ingredient(self):
        for a in self.ids.food_1.children:
            if "NewDietIngredient" in str(a):
                a.ids.food_name.disabled = False
                a.ids.brand_name.disabled = False
                a.ids.weight_name.disabled = False
                a.ids.delete_ingredient_diet.disabled = False
            
        for a in self.ids.food_2.children:
            if "NewDietIngredient" in str(a):
                a.ids.food_name.disabled = False
                a.ids.brand_name.disabled = False
                a.ids.weight_name.disabled = False
                a.ids.delete_ingredient_diet.disabled = False
        
        for a in self.ids.food_3.children:
            if "NewDietIngredient" in str(a):
                a.ids.food_name.disabled = False
                a.ids.brand_name.disabled = False
                a.ids.weight_name.disabled = False
                a.ids.delete_ingredient_diet.disabled = False
        
        for a in self.ids.food_4.children:
            if "NewDietIngredient" in str(a):
                a.ids.food_name.disabled = False
                a.ids.brand_name.disabled = False
                a.ids.weight_name.disabled = False
                a.ids.delete_ingredient_diet.disabled = False
        
        for a in self.ids.food_5.children:
            if "NewDietIngredient" in str(a):
                a.ids.food_name.disabled = False
                a.ids.brand_name.disabled = False
                a.ids.weight_name.disabled = False
                a.ids.delete_ingredient_diet.disabled = False
            
        for a in self.ids.food_6.children:
            if "NewDietIngredient" in str(a):
                a.ids.food_name.disabled = False
                a.ids.brand_name.disabled = False
                a.ids.weight_name.disabled = False
                a.ids.delete_ingredient_diet.disabled = False
    
    def delete_diet_temp(self):
        pass
    def get_diet_name(self):
        app = MDApp.get_running_app()
        return app.root.ids.diet_screen.diet_option_clicked.text
    
    def recover_diet(self):
            
        disk = DiskMaster()
        diet = disk.recover_diet(self.get_diet_name())
        
        food1_kcal = []
        food1_prot= []
        food1_carb = []
        food1_lip = []
        food1_sug = []
        food1_salt = []
        food2_kcal = []
        food2_prot= []
        food2_carb = []
        food2_lip = []
        food2_sug = []
        food2_salt = []
        food3_kcal = []
        food3_prot= []
        food3_carb = []
        food3_lip = []
        food3_sug = []
        food3_salt = []
        food4_kcal = []
        food4_prot= []
        food4_carb = []
        food4_lip = []
        food4_sug = []
        food4_salt = []
        food5_kcal = []
        food5_prot= []
        food5_carb = []
        food5_lip = []
        food5_sug = []
        food5_salt = []
        food6_kcal = []
        food6_prot= []
        food6_carb = []
        food6_lip = []
        food6_sug = []
        food6_salt = []
        
        try:    
            for ida, a in enumerate(diet["food1"]["name"]):
                g = diet["food1"]["grams"][ida]
                
                self.ids.food_1.add_widget(NewDietIngredient( food = a, brand = diet["food1"]["brand"][ida], weight =g), index = 2)
                
                food1_kcal.append(round(float(diet["food1"]["kcal"][ida]) * float(g)/100,1))
                food1_prot.append(round(float(diet["food1"]["proteins"][ida]) * float(g)/100,1))
                food1_carb.append(round(float(diet["food1"]["carbohydrates"][ida]) * float(g)/100,1))
                food1_sug.append(round(float(diet["food1"]["sugar"][ida]) * float(g)/100,1))
                food1_lip.append(round(float(diet["food1"]["lipids"][ida]) * float(g)/100,1))
                food1_salt.append(round(float(diet["food1"]["salt"][ida]) * float(g)/100,1))
                
            self.ids.proteins_food_result_1.text = str(round(sum(food1_prot),1))
            self.ids.carbohydrates_food_result_1.text = str(round(sum(food1_carb),1))
            self.ids.lipids_food_result_1.text = str(round(sum(food1_lip),1))
            self.ids.sugar_food_result_1.text = str(round(sum(food1_sug),1))
            self.ids.salt_food_result_1.text = str(round(sum(food1_salt),1))    
            self.ids.kcal_food_result_1.text = str(round(sum(food1_kcal),1)) 

            
                
        except:
            pass
            
            
        try:        
            for ida, a in enumerate(diet["food2"]["name"]):
                g =weight = diet["food2"]["grams"][ida]
                
                self.ids.food_2.add_widget(NewDietIngredient( food = a, brand = diet["food2"]["brand"][ida], weight = g), index = 2)
                
                food2_kcal.append(round(float(diet["food2"]["kcal"][ida]) * float(g)/100,1))
                food2_prot.append(round(float(diet["food2"]["proteins"][ida]) * float(g)/100,1))
                food2_carb.append(round(float(diet["food2"]["carbohydrates"][ida]) * float(g)/100,1))
                food2_sug.append(round(float(diet["food2"]["sugar"][ida]) * float(g)/100,1))
                food2_lip.append(round(float(diet["food2"]["lipids"][ida]) * float(g)/100,1))
                food2_salt.append(round(float(diet["food2"]["salt"][ida]) * float(g)/100,1))
            
            self.ids.proteins_food_result_2.text = str(round(sum(food2_prot),1))
            self.ids.carbohydrates_food_result_2.text = str(round(sum(food2_carb),1))
            self.ids.lipids_food_result_2.text = str(round(sum(food2_lip),1))
            self.ids.sugar_food_result_2.text = str(round(sum(food2_sug),1))
            self.ids.salt_food_result_2.text = str(round(sum(food2_salt),1))    
            self.ids.kcal_food_result_2.text = str(round(sum(food2_kcal),1)) 

        except:
            pass
    
        
        try:        
            for ida, a in enumerate(diet["food3"]["name"]):
                g =weight = diet["food3"]["grams"][ida]
                
                self.ids.food_3.add_widget(NewDietIngredient( food = a, brand = diet["food3"]["brand"][ida], weight = g), index = 2)
                
                food3_kcal.append(round(float(diet["food3"]["kcal"][ida]) * float(g)/100,1))
                food3_prot.append(round(float(diet["food3"]["proteins"][ida]) * float(g)/100, 1))
                food3_carb.append(round(float(diet["food3"]["carbohydrates"][ida]) * float(g)/100,1))
                food3_sug.append(round(float(diet["food3"]["sugar"][ida]) * float(g)/100,1))
                food3_lip.append(round(float(diet["food3"]["lipids"][ida]) * float(g)/100,1))
                food3_salt.append(round(float(diet["food3"]["salt"][ida]) * float(g)/100,1))
            
            
           
            self.ids.proteins_food_result_3.text = str(round(sum(food3_prot),1))
            self.ids.carbohydrates_food_result_3.text = str(round(sum(food3_carb),1))
            self.ids.lipids_food_result_3.text = str(round(sum(food3_lip),1))
            self.ids.sugar_food_result_3.text = str(round(sum(food3_sug),1))
            self.ids.salt_food_result_3.text = str(round(sum(food3_salt),1))    
            self.ids.kcal_food_result_3.text = str(round(sum(food3_kcal),1))
         
                 
        except:
            pass
    
         
        try:        
            for ida, a in enumerate(diet["food4"]["name"]):
                g =weight = diet["food4"]["grams"][ida]
                
                self.ids.food_4.add_widget(NewDietIngredient( food = a, brand = diet["food4"]["brand"][ida], weight =g), index = 2)
                food4_kcal.append(round(float(diet["food4"]["kcal"][ida]) * float(g)/100,1))
                food4_prot.append(round(float(diet["food4"]["proteins"][ida]) * float(g)/100,1))
                food4_carb.append(round(float(diet["food4"]["carbohydrates"][ida]) * float(g)/100,1))
                food4_sug.append(round(float(diet["food4"]["sugar"][ida]) * float(g)/100,1))
                food4_lip.append(round(float(diet["food4"]["lipids"][ida]) * float(g)/100,1))
                food4_salt.append(round(float(diet["food4"]["salt"][ida]) * float(g)/100,1))
            
            self.ids.proteins_food_result_4.text = str(round(sum(food4_prot),1))
            self.ids.carbohydrates_food_result_4.text = str(round(sum(food4_carb),1))
            self.ids.lipids_food_result_4.text = str(round(sum(food4_lip),1))
            self.ids.sugar_food_result_4.text = str(round(sum(food4_sug),1))
            self.ids.salt_food_result_4.text = str(round(sum(food4_salt),1))    
            self.ids.kcal_food_result_4.text = str(round(sum(food4_kcal),1)) 
         
                 
        except:
            pass
    
         
        try:        
            for ida, a in enumerate(diet["food5"]["name"]):
                g =weight = diet["food5"]["grams"][ida]
                
                self.ids.food_5.add_widget(NewDietIngredient( food = a, brand = diet["food5"]["brand"][ida], weight = g), index = 2)
                food5_kcal.append(round(float(diet["food5"]["kcal"][ida]) * float(g)/100,1))
                food5_prot.append(round(float(diet["food5"]["proteins"][ida]) * float(g)/100,1))
                food5_carb.append(round(float(diet["food5"]["carbohydrates"][ida]) * float(g)/100,1))
                food5_sug.append(round(float(diet["food5"]["sugar"][ida]) * float(g)/100,1))
                food5_lip.append(round(float(diet["food5"]["lipids"][ida]) * float(g)/100,1))
                food5_salt.append(round(float(diet["food5"]["salt"][ida]) * float(g)/100,1))
            
            self.ids.proteins_food_result_5.text = str(round(sum(food5_prot),1))
            self.ids.carbohydrates_food_result_5.text = str(round(sum(food5_carb),1))
            self.ids.lipids_food_result_5.text = str(round(sum(food5_lip),1))
            self.ids.sugar_food_result_5.text = str(round(sum(food5_sug),1))
            self.ids.salt_food_result_5.text = str(round(sum(food5_salt),1))    
            self.ids.kcal_food_result_5.text = str(round(sum(food5_kcal),1)) 
                
        except:
            pass
        
        try:     
            for ida, a in enumerate(diet["food6"]["name"]):
                g = weight = diet["food6"]["grams"][ida]
                
                self.ids.food_6.add_widget(NewDietIngredient( food = a, brand = diet["food6"]["brand"][ida], weight = g), index = 2)
                food6_kcal.append(round(float(diet["food6"]["kcal"][ida]) * float(g)/100,1))
                food6_prot.append(round(float(diet["food6"]["proteins"][ida]) * float(g)/100,1))
                food6_carb.append(round(float(diet["food6"]["carbohydrates"][ida]) * float(g)/100,1))
                food6_sug.append(round(float(diet["food6"]["sugar"][ida]) * float(g)/100,1))
                food6_lip.append(round(float(diet["food6"]["lipids"][ida]) * float(g)/100,1))
                food6_salt.append(round(float(diet["food6"]["salt"][ida]) * float(g)/100,1))
            
           
            
            self.ids.proteins_food_result_6.text = str(round(sum(food6_prot),1))
            self.ids.carbohydrates_food_result_6.text = str(round(sum(food6_carb),1))
            self.ids.lipids_food_result_6.text = str(round(sum(food6_lip,1)))
            self.ids.sugar_food_result_6.text = str(round(sum(food6_sug),1))
            self.ids.salt_food_result_6.text = str(round(sum(food6_salt),1))    
            self.ids.kcal_food_result_6.text = str(round(sum(food6_kcal),1))
        except:
            pass
        

        
    def set_food_values(self, instance):
        
        if instance.text != "" and instance.parent.ids.weight_name.text != "" and instance.parent.ids.brand_name.text != "" and self.value == "" and self.value2 != self.value: 
            instance2 = instance.parent
            db=DBMaster()
            values =db.get_food_values(instance2.ids.food_name.text, instance2.ids.brand_name.text)
            for f in self.ids.food_1.children:
                if f == instance2:
                    self.value = instance2.ids.weight_name.text
                    
                    self.ids.proteins_food_result_1.text = str(round(float(self.ids.proteins_food_result_1.text)+ float(values[0][0])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.carbohydrates_food_result_1.text = str(round(float(self.ids.carbohydrates_food_result_1.text)+ float(values[0][1])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.sugar_food_result_1.text = str(round(float(self.ids.sugar_food_result_1.text)+ float(values[0][2])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.lipids_food_result_1.text = str(round(float(self.ids.lipids_food_result_1.text)+ float(values[0][3])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.salt_food_result_1.text = str(round(float(self.ids.salt_food_result_1.text)+ float(values[0][4])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.kcal_food_result_1.text = str(round(float(self.ids.kcal_food_result_1.text)+ float(values[0][5])*float(instance2.ids.weight_name.text)/100,1)) 
                    return
           
            for f in self.ids.food_2.children:
                if f == instance2:
                    self.value = instance2.ids.weight_name.text
                    
                    self.ids.proteins_food_result_2.text = str(round(float(self.ids.proteins_food_result_1.text)+ float(values[0][0])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.carbohydrates_food_result_2.text = str(round(float(self.ids.carbohydrates_food_result_1.text)+ float(values[0][1])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.sugar_food_result_2.text = str(round(float(self.ids.sugar_food_result_1.text)+ float(values[0][2])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.lipids_food_result_2.text = str(round(float(self.ids.lipids_food_result_1.text)+ float(values[0][3])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.salt_food_result_2.text = str(round(float(self.ids.salt_food_result_1.text)+ float(values[0][4])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.kcal_food_result_2.text = str(round(float(self.ids.kcal_food_result_1.text)+ float(values[0][5])*float(instance2.ids.weight_name.text)/100,1)) 
                    return
            
            for f in self.ids.food_3.children:
                if f == instance2:
                    self.value = instance2.ids.weight_name.text
                    
                    self.ids.proteins_food_result_3.text = str(round(float(self.ids.proteins_food_result_1.text)+ float(values[0][0])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.carbohydrates_food_result_3.text = str(round(float(self.ids.carbohydrates_food_result_1.text)+ float(values[0][1])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.sugar_food_result_3.text = str(round(float(self.ids.sugar_food_result_1.text)+ float(values[0][2])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.lipids_food_result_3.text = str(round(float(self.ids.lipids_food_result_1.text)+ float(values[0][3])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.salt_food_result_3.text = str(round(float(self.ids.salt_food_result_1.text)+ float(values[0][4])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.kcal_food_result_3.text = str(round(float(self.ids.kcal_food_result_1.text)+ float(values[0][5])*float(instance2.ids.weight_name.text)/100,1)) 
                    
            for f in self.ids.food_4.children:
                if f == instance2:
                    self.value = instance2.ids.weight_name.text
                    
                    self.ids.proteins_food_result_4.text = str(round(float(self.ids.proteins_food_result_1.text)+ float(values[0][0])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.carbohydrates_food_result_4.text = str(round(float(self.ids.carbohydrates_food_result_1.text)+ float(values[0][1])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.sugar_food_result_4.text = str(round(float(self.ids.sugar_food_result_1.text)+ float(values[0][2])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.lipids_food_result_4.text = str(round(float(self.ids.lipids_food_result_1.text)+ float(values[0][3])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.salt_food_result_4.text = str(round(float(self.ids.salt_food_result_1.text)+ float(values[0][4])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.kcal_food_result_4.text = str(round(float(self.ids.kcal_food_result_1.text)+ float(values[0][5])*float(instance2.ids.weight_name.text)/100,1)) 
                    return
            
            for f in self.ids.food_5.children:
                if f == instance2:
                    self.value = instance2.ids.weight_name.text
                    
                    self.ids.proteins_food_result_5.text = str(round(float(self.ids.proteins_food_result_1.text)+ float(values[0][0])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.carbohydrates_food_result_5.text = str(round(float(self.ids.carbohydrates_food_result_1.text)+ float(values[0][1])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.sugar_food_result_5.text = str(round(float(self.ids.sugar_food_result_1.text)+ float(values[0][2])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.lipids_food_result_5.text = str(round(float(self.ids.lipids_food_result_1.text)+ float(values[0][3])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.salt_food_result_5.text = str(round(float(self.ids.salt_food_result_1.text)+ float(values[0][4])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.kcal_food_result_5.text = str(round(float(self.ids.kcal_food_result_1.text)+ float(values[0][5])*float(instance2.ids.weight_name.text)/100,1)) 
                    return
                    
            for f in self.ids.food_6.children:
                if f == instance2:
                    self.value = instance2.ids.weight_name.text
                    
                    self.ids.proteins_food_result_6.text = str(round(float(self.ids.proteins_food_result_1.text)+ float(values[0][0])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.carbohydrates_food_result_6.text = str(round(float(self.ids.carbohydrates_food_result_1.text)+ float(values[0][1])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.sugar_food_result_6.text = str(round(float(self.ids.sugar_food_result_1.text)+ float(values[0][2])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.lipids_food_result_6.text = str(round(float(self.ids.lipids_food_result_1.text)+ float(values[0][3])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.salt_food_result_6.text = str(round(float(self.ids.salt_food_result_1.text)+ float(values[0][4])*float(instance2.ids.weight_name.text)/100,1)) 
                    self.ids.kcal_food_result_6.text = str(round(float(self.ids.kcal_food_result_1.text)+ float(values[0][5])*float(instance2.ids.weight_name.text)/100,1)) 
                    return
        try:
            if instance.text != "" and instance.parent.ids.weight_name.text != "" and instance.parent.ids.brand_name.text != "" and float(self.value) < float(self.value2) or float(self.value) > float(self.value2):
                instance2 = instance.parent
                db=DBMaster()
                values =db.get_food_values(instance2.ids.food_name.text, instance2.ids.brand_name.text)
                for f in self.ids.food_1.children:
                    if f == instance2:
                        self.ids.proteins_food_result_1.text = str(round(float(self.ids.proteins_food_result_1.text)- float(values[0][0])*float(self.value)/100 + float(values[0][0])*float(self.value2)/100,1)) 
                        self.ids.carbohydrates_food_result_1.text = str(round(float(self.ids.carbohydrates_food_result_1.text)- float(values[0][1])*float(self.value)/100 + float(values[0][1])*float(self.value2)/100,1)) 
                        self.ids.sugar_food_result_1.text = str(round(float(self.ids.sugar_food_result_1.text)- float(values[0][2])*float(self.value)/100 + float(values[0][2])*float(self.value2)/100,1)) 
                        self.ids.lipids_food_result_1.text = str(round(float(self.ids.lipids_food_result_1.text)- float(values[0][3])*float(self.value)/100 + float(values[0][3])*float(self.value2)/100,1)) 
                        self.ids.salt_food_result_1.text = str(round(float(self.ids.salt_food_result_1.text)- float(values[0][4])*float(self.value)/100 + float(values[0][4])*float(self.value2)/100,1)) 
                        self.ids.kcal_food_result_1.text = str(round(float(self.ids.kcal_food_result_1.text)- float(values[0][5])*float(self.value)/100 + float(values[0][5])*float(self.value2)/100,1)) 
                        if self.value2 == "":
                            self.value = 0
                        else:
                            self.value = self.value2
                        return
                for f in self.ids.food_2.children:
                    if f == instance2:
                        self.ids.proteins_food_result_2.text = str(round(float(self.ids.proteins_food_result_2.text)- float(values[0][0])*float(self.value)/100 + float(values[0][0])*float(self.value2)/100,1)) 
                        self.ids.carbohydrates_food_result_2.text = str(round(float(self.ids.carbohydrates_food_result_2.text)- float(values[0][1])*float(self.value)/100 + float(values[0][1])*float(self.value2)/100,1)) 
                        self.ids.sugar_food_result_2.text = str(round(float(self.ids.sugar_food_result_2.text)- float(values[0][2])*float(self.value)/100 + float(values[0][2])*float(self.value2)/100,1)) 
                        self.ids.lipids_food_result_2.text = str(round(float(self.ids.lipids_food_result_2.text)- float(values[0][3])*float(self.value)/100 + float(values[0][3])*float(self.value2)/100,1)) 
                        self.ids.salt_food_result_2.text = str(round(float(self.ids.salt_food_result_2.text)- float(values[0][4])*float(self.value)/100 + float(values[0][4])*float(self.value2)/100,1)) 
                        self.ids.kcal_food_result_2.text = str(round(float(self.ids.kcal_food_result_2.text)- float(values[0][5])*float(self.value)/100 + float(values[0][5])*float(self.value2)/100,1)) 
                        if self.value2 == "":
                            self.value = 0
                        else:
                            self.value = self.value2
                        return
                for f in self.ids.food_3.children:
                    if f == instance2:
        
                        self.ids.proteins_food_result_3.text = str(round(float(self.ids.proteins_food_result_3.text)- float(values[0][0])*float(self.value)/100 + float(values[0][0])*float(self.value2)/100,1)) 
                        self.ids.carbohydrates_food_result_3.text = str(round(float(self.ids.carbohydrates_food_result_3.text)- float(values[0][1])*float(self.value)/100 + float(values[0][1])*float(self.value2)/100,1)) 
                        self.ids.sugar_food_result_3.text = str(round(float(self.ids.sugar_food_result_3.text)- float(values[0][2])*float(self.value)/100 + float(values[0][2])*float(self.value2)/100,1)) 
                        self.ids.lipids_food_result_3.text = str(round(float(self.ids.lipids_food_result_3.text)- float(values[0][3])*float(self.value)/100 + float(values[0][3])*float(self.value2)/100,1)) 
                        self.ids.salt_food_result_3.text = str(round(float(self.ids.salt_food_result_3.text)- float(values[0][4])*float(self.value)/100 + float(values[0][4])*float(self.value2)/100,1)) 
                        self.ids.kcal_food_result_3.text = str(round(float(self.ids.kcal_food_result_3.text)- float(values[0][5])*float(self.value)/100 + float(values[0][5])*float(self.value2)/100,1)) 
                        if self.value2 == "":
                            self.value = 0
                        else:
                            self.value = self.value2
                        return
                
                for f in self.ids.food_4.children:
                    if f == instance2:
        
                        self.ids.proteins_food_result_4.text = str(round(float(self.ids.proteins_food_result_4.text)- float(values[0][0])*float(self.value)/100 + float(values[0][0])*float(self.value2)/100,1)) 
                        self.ids.carbohydrates_food_result_4.text = str(round(float(self.ids.carbohydrates_food_result_4.text)- float(values[0][1])*float(self.value)/100 + float(values[0][1])*float(self.value2)/100,1)) 
                        self.ids.sugar_food_result_4.text = str(round(float(self.ids.sugar_food_result_4.text)- float(values[0][2])*float(self.value)/100 + float(values[0][2])*float(self.value2)/100,1)) 
                        self.ids.lipids_food_result_4.text = str(round(float(self.ids.lipids_food_result_4.text)- float(values[0][3])*float(self.value)/100 + float(values[0][3])*float(self.value2)/100,1)) 
                        self.ids.salt_food_result_4.text = str(round(float(self.ids.salt_food_result_4.text)- float(values[0][4])*float(self.value)/100 + float(values[0][4])*float(self.value2)/100,1)) 
                        self.ids.kcal_food_result_4.text = str(round(float(self.ids.kcal_food_result_4.text)- float(values[0][5])*float(self.value)/100 + float(values[0][5])*float(self.value2)/100,1)) 
                        if self.value2 == "":
                            self.value = 0
                        else:
                            self.value = self.value2
                        return
                    
                for f in self.ids.food_5.children:
                    if f == instance2:
        
                        self.ids.proteins_food_result_5.text = str(round(float(self.ids.proteins_food_result_5.text)- float(values[0][0])*float(self.value)/100 + float(values[0][0])*float(self.value2)/100,1)) 
                        self.ids.carbohydrates_food_result_5.text = str(round(float(self.ids.carbohydrates_food_result_5.text)- float(values[0][1])*float(self.value)/100 + float(values[0][1])*float(self.value2)/100,1)) 
                        self.ids.sugar_food_result_5.text = str(round(float(self.ids.sugar_food_result_5.text)- float(values[0][2])*float(self.value)/100 + float(values[0][2])*float(self.value2)/100,1)) 
                        self.ids.lipids_food_result_5.text = str(round(float(self.ids.lipids_food_result_5.text)- float(values[0][3])*float(self.value)/100 + float(values[0][3])*float(self.value2)/100,1)) 
                        self.ids.salt_food_result_5.text = str(round(float(self.ids.salt_food_result_5.text)- float(values[0][4])*float(self.value)/100 + float(values[0][4])*float(self.value2)/100,1)) 
                        self.ids.kcal_food_result_5.text = str(round(float(self.ids.kcal_food_result_5.text)- float(values[0][5])*float(self.value)/100 + float(values[0][5])*float(self.value2)/100,1)) 
                        if self.value2 == "":
                            self.value = 0
                        else:
                            self.value = self.value2
                        return
                    
                for f in self.ids.food_6.children:
                    if f == instance2:
        
                        self.ids.proteins_food_result_6.text = str(round(float(self.ids.proteins_food_result_6.text)- float(values[0][0])*float(self.value)/100 + float(values[0][0])*float(self.value2)/100,1)) 
                        self.ids.carbohydrates_food_result_6.text = str(round(float(self.ids.carbohydrates_food_result_6.text)- float(values[0][1])*float(self.value)/100 + float(values[0][1])*float(self.value2)/100,1)) 
                        self.ids.sugar_food_result_6.text = str(round(float(self.ids.sugar_food_result_6.text)- float(values[0][2])*float(self.value)/100 + float(values[0][2])*float(self.value2)/100,1)) 
                        self.ids.lipids_food_result_6.text = str(round(float(self.ids.lipids_food_result_6.text)- float(values[0][3])*float(self.value)/100 + float(values[0][3])*float(self.value2)/100,1)) 
                        self.ids.salt_food_result_6.text = str(round(float(self.ids.salt_food_result_6.text)- float(values[0][4])*float(self.value)/100 + float(values[0][4])*float(self.value2)/100,1)) 
                        self.ids.kcal_food_result_6.text = str(round(float(self.ids.kcal_food_result_6.text)- float(values[0][5])*float(self.value)/100 + float(values[0][5])*float(self.value2)/100,1)) 
                        if self.value2 == "":
                            self.value = 0
                        else:
                            self.value = self.value2
                        return
                    
        except Exception:
            import traceback
            traceback.print_exc()
        
        
    def delete_diet_content(self):        
            
        for b in range(4):    
            for a in self.ids.food_1.children:
                if "NewDietIngredient" in str(a):
                    self.ids.food_1.remove_widget(a)
            
        for b in range(4):            
            for a in self.ids.food_2.children:
                if "NewDietIngredient" in str(a):
                    self.ids.food_2.remove_widget(a)
         
        for b in range(4):                
            for a in self.ids.food_3.children:
                if "NewDietIngredient" in str(a):
                    self.ids.food_3.remove_widget(a)
        
        for b in range(4):                
            for a in self.ids.food_4.children:
                if "NewDietIngredient" in str(a):
                    self.ids.food_4.remove_widget(a)
        
        for b in range(4):                
            for a in self.ids.food_5.children:
                if "NewDietIngredient" in str(a):
                    self.ids.food_5.remove_widget(a)
        
        for b in range(4):                
            for a in self.ids.food_6.children:
                if "NewDietIngredient" in str(a):
                    self.ids.food_6.remove_widget(a)
    
    def save_diet(self):
        dict = {"food1":{"name":[],"brand":[], "grams": [], "kcal":[],"proteins": [], "carbohydrates": [] , "lipids":[] , "sugar": [], "salt": []}, "food2":{"name":[],"brand":[], "grams": [], "kcal":[],"proteins": [], "carbohydrates": [] , "lipids":[] , "sugar": [], "salt": []}, "food3":{"name":[],"brand":[], "grams": [], "kcal":[],"proteins": [], "carbohydrates": [] , "lipids":[] , "sugar": [], "salt": []}, "food4":{"name":[],"brand":[], "grams": [], "kcal":[],"proteins": [], "carbohydrates": [] , "lipids":[] , "sugar": [], "salt": []}, "food5":{"name":[],"brand":[], "grams": [], "kcal":[],"proteins": [], "carbohydrates": [] , "lipids":[] , "sugar": [], "salt": []}, "food6":{"name":[],"brand":[], "grams": [], "kcal":[],"proteins": [], "carbohydrates": [] , "lipids":[] , "sugar": [], "salt": []}}
        for item in self.ids.food_1.children:
            if "NewDietIngredient" in str(item):
                if item.ids.food_name.text == "":
                    pass
                elif item.ids.brand_name.text == "":
                    pass
                elif item.ids.weight_name.text == "":
                    pass
                else:
                    dict["food1"]["name"].append(item.ids.food_name.text)
                    dict["food1"]["brand"].append(item.ids.brand_name.text)
                    dict["food1"]["grams"].append(item.ids.weight_name.text)
                    db = DBMaster()
                    values = db.get_food_values(item.ids.food_name.text, item.ids.brand_name.text)
                    dict["food1"]["proteins"].append(values[0][0])
                    dict["food1"]["carbohydrates"].append(values[0][1])
                    dict["food1"]["sugar"].append(values[0][2])
                    dict["food1"]["lipids"].append(values[0][3])
                    dict["food1"]["salt"].append(values[0][4])
                    dict["food1"]["kcal"].append(values[0][5])

        for item in self.ids.food_2.children:
            if "NewDietIngredient" in str(item):
                if item.ids.food_name.text == "":
                    pass
                elif item.ids.brand_name.text == "":
                    pass
                elif item.ids.weight_name.text == "":
                    pass
                else:
                    dict["food2"]["name"].append(item.ids.food_name.text)
                    dict["food2"]["brand"].append(item.ids.brand_name.text)
                    dict["food2"]["grams"].append(item.ids.weight_name.text)
                    db = DBMaster()
                    values = db.get_food_values(item.ids.food_name.text, item.ids.brand_name.text)
                    dict["food2"]["proteins"].append(values[0][0])
                    dict["food2"]["carbohydrates"].append(values[0][1])
                    dict["food2"]["sugar"].append(values[0][2])
                    dict["food2"]["lipids"].append(values[0][3])
                    dict["food2"]["salt"].append(values[0][4])
                    dict["food2"]["kcal"].append(values[0][5])

        for item in self.ids.food_3.children:
            if "NewDietIngredient" in str(item):
                if item.ids.food_name.text == "":
                    pass
                elif item.ids.brand_name.text == "":
                    pass
                elif item.ids.weight_name.text == "":
                    pass
                else:
                    dict["food3"]["name"].append(item.ids.food_name.text)
                    dict["food3"]["brand"].append(item.ids.brand_name.text)
                    dict["food3"]["grams"].append(item.ids.weight_name.text)
                    db = DBMaster()
                    values = db.get_food_values(item.ids.food_name.text, item.ids.brand_name.text)
                    dict["food3"]["proteins"].append(values[0][0])
                    dict["food3"]["carbohydrates"].append(values[0][1])
                    dict["food3"]["sugar"].append(values[0][2])
                    dict["food3"]["lipids"].append(values[0][3])
                    dict["food3"]["salt"].append(values[0][4])
                    dict["food3"]["kcal"].append(values[0][5])
                    
        for item in self.ids.food_4.children:
            if "NewDietIngredient" in str(item):
                if item.ids.food_name.text == "":
                    pass
                elif item.ids.brand_name.text == "":
                    pass
                elif item.ids.weight_name.text == "":
                    pass
                else:
                    dict["food4"]["name"].append(item.ids.food_name.text)
                    dict["food4"]["brand"].append(item.ids.brand_name.text)
                    dict["food4"]["grams"].append(item.ids.weight_name.text)
                    db = DBMaster()
                    values = db.get_food_values(item.ids.food_name.text, item.ids.brand_name.text)
                    dict["food4"]["proteins"].append(values[0][0])
                    dict["food4"]["carbohydrates"].append(values[0][1])
                    dict["food4"]["sugar"].append(values[0][2])
                    dict["food4"]["lipids"].append(values[0][3])
                    dict["food4"]["salt"].append(values[0][4])
                    dict["food4"]["kcal"].append(values[0][5])
                    
        for item in self.ids.food_5.children:
            if "NewDietIngredient" in str(item):
                if item.ids.food_name.text == "":
                    pass
                elif item.ids.brand_name.text == "":
                    pass
                elif item.ids.weight_name.text == "":
                    pass
                else:
                    dict["food5"]["name"].append(item.ids.food_name.text)
                    dict["food5"]["brand"].append(item.ids.brand_name.text)
                    dict["food5"]["grams"].append(item.ids.weight_name.text)
                    db = DBMaster()
                    values = db.get_food_values(item.ids.food_name.text, item.ids.brand_name.text)
                    dict["food5"]["proteins"].append(values[0][0])
                    dict["food5"]["carbohydrates"].append(values[0][1])
                    dict["food5"]["sugar"].append(values[0][2])
                    dict["food5"]["lipids"].append(values[0][3])
                    dict["food5"]["salt"].append(values[0][4])
                    dict["food5"]["kcal"].append(values[0][5])
                    
        for item in self.ids.food_6.children:
            if "NewDietIngredient" in str(item):
                if item.ids.food_name.text == "":
                    pass
                elif item.ids.brand_name.text == "":
                    pass
                elif item.ids.weight_name.text == "":
                    pass
                else:
                    dict["food6"]["name"].append(item.ids.food_name.text)
                    dict["food6"]["brand"].append(item.ids.brand_name.text)
                    dict["food6"]["grams"].append(item.ids.weight_name.text)
                    db = DBMaster()
                    values = db.get_food_values(item.ids.food_name.text, item.ids.brand_name.text)
                    dict["food6"]["proteins"].append(values[0][0])
                    dict["food6"]["carbohydrates"].append(values[1])
                    dict["food6"]["sugar"].append(values[0][2])
                    dict["food6"]["lipids"].append(values[0][3])
                    dict["food6"]["salt"].append(values[0][4])
                    dict["food6"]["kcal"].append(values[0][5])
        
        name = self.get_diet_name()
        disk = DiskMaster()
        disk.save_diet(name, dict)
                    
        
                
    def display_groups(self, instance):
        if self.popup is None:
            self.popup = TreeviewGroup()
        self.popup.filter(instance.text)
        self.popup.open()
        
    def set_id(self, instance):
        self.id_focused = instance
    
    def add_ingredient(self, instance):
        instance.add_widget(NewDietIngredient(), index = 2)
        
    def exit_btn_press(self, instance):
        app = MDApp.get_running_app()
        if instance.text == "Salir":
            app.root.ids.scr.current = "diet_screen"
            
        else:
            self.delete_diet_content()
            self.recover_diet()
            self.ids.exit_btn.text = "Salir"
            self.ids.save_btn.disabled = True
            self.ids.edit_btn.disabled = False
            app.root.ids.nav_drawer.disabled = False
            self.ids.add_ingredient_1.disabled = True
            self.ids.add_ingredient_2.disabled = True
            self.ids.add_ingredient_3.disabled = True
            self.ids.add_ingredient_4.disabled = True
            self.ids.add_ingredient_5.disabled = True
            self.ids.add_ingredient_6.disabled = True 
            self.disable_diet_ingredient()
    
    def save_btn_press(self):
        pass
    




class MyMDTextField(MDTextField):


    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.icon_right:
                # icon position based on the KV code for MDTextField
                icon_x = (self.width + self.x) - 28 - dp(8)
                icon_y = self.center[1] - 14
                if self.mode == "rectangle":
                    icon_y -= dp(4)
                elif self.mode != 'fill':
                    icon_y += dp(8)

                # not a complete bounding box test, but should be sufficient
                if touch.pos[0] > icon_x and touch.pos[1] > icon_y:
                    
                    rec = Reccomendation()
                    rec.show_msg(self.hint_text)

                    # try to adjust cursor position
                    cursor = self.cursor
                    self.cursor = (0,0)
                    Clock.schedule_once(partial(self.set_cursor, cursor))  
        return super(MyMDTextField, self).on_touch_down(touch)

    def set_cursor(self, pos, dt):
        self.cursor = pos
  
class UserScreen(MDScreen):
    def error_message_letters(self, text, instance):
        for letter in text:
            if letter in ascii_letters or letter in whitespace or letter in punctuation:
                if letter in (",","."):
                    pass
                else:
                    instance.error = True
                    break
            else: 
                instance.error = False
    
        
    def save_btn_press(self):
        if self.ids.weight_tf_user.error or self.ids.height_tf_user.error or self.ids.age_tf_user.error or not self.ids.male_cb_user.active and not  self.ids.female_cb_user.active or not self.ids.sedentary_cb_user.active and not self.ids.low_cb_user.active and not self.ids.moderated_cb_user.active and not self.ids.high_cb_user.active and not self.ids.pro_cb_user.active or not self.ids.lose_cb_user.active and not self.ids.maintain_cb_user.active and not self.ids.define_cb_user.active and not self.ids.clean_vol_cb_user.active and not self.ids.vol_cb_user.active:
            pass
        elif self.ids.weight_tf_user.text == "" or self.ids.height_tf_user.text == "" or self.ids.age_tf_user.text == "":
            pass
        else:  
            self.ids.save_btn_user.disabled = True
            self.ids.save_btn_user.disabled = True
            self.ids.edit_btn_user.disabled = False
            self.ids.name_tf_user.readonly = True
            self.ids.weight_tf_user.readonly = True
            self.ids.height_tf_user.readonly = True
            self.ids.age_tf_user.readonly = True
            self.ids.male_cb_user.disabled = True
            self.ids.female_cb_user.disabled = True
            self.ids.sedentary_cb_user.disabled = True
            self.ids.low_cb_user.disabled = True
            self.ids.moderated_cb_user.disabled = True
            self.ids.high_cb_user.disabled = True
            self.ids.pro_cb_user.disabled = True
            self.ids.lose_cb_user.disabled = True
            self.ids.maintain_cb_user.disabled = True
            self.ids.define_cb_user.disabled = True
            self.ids.clean_vol_cb_user.disabled = True
            self.ids.vol_cb_user.disabled = True
            self.ids.cancel_btn_user.disabled = True
            self.save_user()
            app = MDApp.get_running_app()
            app.root.ids.nav_drawer.disabled = False
            
    def save_user(self):
        name = self.ids.name_tf_user.text
        weight = self.ids.weight_tf_user.text
        height = self.ids.height_tf_user.text
        age = self.ids.age_tf_user.text
        if self.ids.male_cb_user.active:
            sex = "male"
        elif self.ids.female_cb_user.active:
            sex = "female"
        
        if self.ids.sedentary_cb_user.active:
            exercise= "sedentary"
        
        elif self.ids.low_cb_user.active:
            exercise= "low"
        
        elif self.ids.moderated_cb_user.active:
            exercise= "moderated"
        elif self.ids.high_cb_user.active:
            exercise= "high"
        elif self.ids.pro_cb_user.active:
            exercise = "pro"
        
        """for i, cb in enumerate(self.ids):
            if cb.active:
                objective = cb.split("_")[0]"""

        if self.ids.lose_cb_user.active:
            objective= "lose"
        
        elif self.ids.maintain_cb_user.active:
            objective= "maintain"
        
        elif self.ids.define_cb_user.active:
            objective= "define"
            
        elif self.ids.clean_vol_cb_user.active:
            objective= "clean"
            
        elif self.ids.vol_cb_user.active:
            objective = "vol"
        
        dict = {"name": name, "weight": weight, "height": height, "age": age, "sex": sex, "exercise": exercise, "objective": objective}
        DiskMaster.save_user(dict, dict)
    
    def charge_user_info(self):
        try:    
            dict = DiskMaster.recover_user(self)
            self.ids.name_tf_user.text = dict["name"]
            self.ids.weight_tf_user.text = dict["weight"]
            self.ids.height_tf_user.text = dict["height"]
            self.ids.age_tf_user.text = dict["age"] 
             
            if dict["sex"] == "male":
                self.ids.male_cb_user.active = True
            
            elif dict["sex"] == "female": 
                self.ids.female_cb_user.active = True
                
            if dict["exercise"] == "sedentary":
                self.ids.sedentary_cb_user.active = True
                
            elif dict["exercise"] == "low":
                self.ids.low_cb_user.active = True
                
            elif dict["exercise"] == "moderated":
                self.ids.moderated_cb_user.active = True
                
            elif dict["exercise"] == "high":
                self.ids.high_cb_user.active = True
                
            elif dict["exercise"] == "pro":
                self.ids.pro_cb_user.active = True
            
            if dict["objective"] == "lose":
                self.ids.lose_cb_user.active = True
                
            elif dict["objective"] == "maintain":
                self.ids.maintain_cb_user.active = True
            
            elif dict["objective"] == "definition":
                self.ids.define_cb_user.active = True
                
            elif dict["objective"] == "clean":
                self.ids.clean_vol_cb_user.active = True
                
            elif dict["objective"] == "vol":
                self.ids.vol_cb_user.active = True
        except:
            pass               
class CalculatorScreen(MDScreen):
    groupName = ObjectProperty(None)
    popup = ObjectProperty(None)
    id_focused = ""
    def set_value(self,a):
        pass
    
    def display_groups(self, instance):
        if self.popup is None:
            self.popup = TreeviewGroup()
        self.popup.filter(instance.text)
        self.popup.open()

    def set_id(self, instance):
        self.id_focused = instance
    
    def buttonClicked(self):
        new_ingredient = CalculatorFoodBlock()

        self.ids.ingredients_box.add_widget(new_ingredient)
    
   
    
    def set_food_values(self, instance):
        try:    
            if "FoodTextInput" in str(instance):
                for a in instance.parent.children:
                    if "BrandTextInput" in str(a):
                        if a.text == "":
                            break
                        else:    
                            db = DBMaster()
                            values = db.get_food_values(instance.text, a.text)
                            for b in instance.parent.children:
                                if b.hint_text == "Proteínas":
                                    b.text = str(values[0][0])
                                elif b.hint_text == "Glúcidos":   
                                    b.text = str(values[0][1])
                                elif b.hint_text == "Azúcar":
                                    b.text = str(values[0][2])
                                elif b.hint_text == "Grasas":     
                                    b.text = str(values[0][3])
                                elif b.hint_text == "Sal":
                                    b.text = str(values[0][4])
                                elif b.hint_text == "Kcal":     
                                    b.text = str(values[0][5])
                            
                            
            elif "BrandTextInput" in str(instance):
                for a in instance.parent.children:
                    if "FoodTextInput" in str(a):
                        if a.text == "":
                            break
                        else:    
                            db = DBMaster()
                            values = db.get_food_values(a.text, instance.text)
                            for b in instance.parent.children:
                                if b.hint_text == "Proteínas":
                                    b.text = str(values[0][0])
                                elif b.hint_text == "Glúcidos":   
                                    b.text = str(values[0][1])
                                elif b.hint_text == "Azúcar":
                                    b.text = str(values[0][2])
                                elif b.hint_text == "Grasas":     
                                    b.text = str(values[0][3])
                                elif b.hint_text == "Sal":
                                    b.text = str(values[0][4])
                                elif b.hint_text == "Kcal":     
                                    b.text = str(values[0][5])
    
        except: 
            pass  
                                  
    def show_results_kcal(self):
        i1= 0
        grams=0
        kcal = 0
        all_results=[]
        for x in self.ids.ingredients_box.children:
            kcal = 0
            grams = 0
            for y in self.ids.ingredients_box.children[i1].children:
                if y.hint_text == "Kcal" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        kcal = float(y.text.replace(",","."))
                    else:
                        kcal = float(y.text)
                elif y.hint_text == "Gramos" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        grams = float(y.text.replace(",","."))
                    else:    
                        grams = float(y.text)
            all_results.append(grams * kcal)
            i1 +=1
        self.ids.kcal_result.text= str(round(sum(all_results)/100,2))
        
    def show_results_lipids(self):
        i1= 0
        grams=0
        lipids = 0
        all_results=[]
        for x in self.ids.ingredients_box.children:
            lipids = 0
            grams = 0
            for y in self.ids.ingredients_box.children[i1].children:
                if y.hint_text == "Grasas" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        lipids = float(y.text.replace(",","."))
                    else:
                        lipids = float(y.text)
                elif y.hint_text == "Gramos" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        grams = float(y.text.replace(",","."))
                    else:    
                        grams = float(y.text)
            all_results.append(grams * lipids)
            i1 +=1
        
        self.ids.lipids_result.text= str(round(sum(all_results)/100, 2))

        
    def show_results_carbohydrates(self):
        i1= 0
        grams=0
        carbohydrates = 0
        all_results=[]
        for x in self.ids.ingredients_box.children:
            carbohydrates = 0
            grams = 0
            for y in self.ids.ingredients_box.children[i1].children:
                if y.hint_text == "Glúcidos" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        carbohydrates = float(y.text.replace(",","."))
                    else:
                        carbohydrates = float(y.text)
                elif y.hint_text == "Gramos" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        grams = float(y.text.replace(",","."))
                    else:    
                        grams = float(y.text)
            all_results.append(grams * carbohydrates)
            i1 +=1
        self.ids.carbohydrates_result.text= str(round(sum(all_results)/100,2))
    def show_results_sugar(self):
        i1= 0
        grams=0
        sugar = 0
        all_results=[]
        for x in self.ids.ingredients_box.children:
            sugar = 0
            grams = 0
            for y in self.ids.ingredients_box.children[i1].children:
                if y.hint_text == "Azúcar" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        sugar = float(y.text.replace(",","."))
                    else:
                        sugar = float(y.text)
                elif y.hint_text == "Gramos" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        grams = float(y.text.replace(",","."))
                    else:    
                        grams = float(y.text)
            all_results.append(grams * sugar)
            i1 +=1
        self.ids.sugar_result.text= str(round(sum(all_results)/100,2 ))
    

    
    def show_results_proteins(self):
        i1= 0
        grams=0
        proteins = 0
        all_results=[]
        for x in self.ids.ingredients_box.children:
            proteins = 0
            grams = 0
            for y in self.ids.ingredients_box.children[i1].children:
                if y.hint_text == "Proteínas" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        proteins = float(y.text.replace(",","."))
                    else:
                        proteins = float(y.text)
                elif y.hint_text == "Gramos" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        grams = float(y.text.replace(",","."))
                    else:    
                        grams = float(y.text)
            all_results.append(grams * proteins)
            i1 +=1
        self.ids.proteins_result.text= str(round(sum(all_results)/100, 2))
    def show_results_salt(self):
        i1= 0
        grams=0
        salt = 0
        all_results=[]
        for x in self.ids.ingredients_box.children:
            salt = 0
            grams = 0
            for y in self.ids.ingredients_box.children[i1].children:
                if y.hint_text == "Sal" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        salt = float(y.text.replace(",","."))
                    else:
                        salt = float(y.text)
                elif y.hint_text == "Gramos" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        grams = float(y.text.replace(",","."))
                    else:    
                        grams = float(y.text)
            all_results.append(grams * salt)
            i1 +=1
        self.ids.salt_result.text= str(round(sum(all_results)/100,2))
    
    def show_results_grams(self):
        i1= 0
        grams=0
        kcal=0
        lipids = 0
        carbohydrates = 0
        sugar = 0
        proteins = 0
        salt= 0
        kcal_results=[]
        lipids_results=[]
        carbohydrates_results=[]
        sugar_results=[]
        proteins_results=[]
        salt_results=[]
        for x in self.ids.ingredients_box.children:
            grams=0
            kcal=0
            lipids = 0
            carbohydrates = 0
            sugar = 0
            proteins = 0
            salt= 0
            for y in self.ids.ingredients_box.children[i1].children:
                if y.hint_text == "Kcal" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        kcal = float(y.text.replace(",","."))
                    else:
                        kcal = float(y.text)
                elif y.hint_text == "Grasas" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        lipids = float(y.text.replace(",","."))
                    else:
                        lipids = float(y.text)
                elif y.hint_text == "Glúcidos" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        carbohydrates = float(y.text.replace(",","."))
                    else:
                        carbohydrates = float(y.text)
                elif y.hint_text == "Azúcar" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        sugar = float(y.text.replace(",","."))
                    else:
                        sugar = float(y.text)
                elif y.hint_text == "Proteínas" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        proteins = float(y.text.replace(",","."))
                    else:
                        proteins = float(y.text)
                elif y.hint_text == "Sal" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        salt = float(y.text.replace(",","."))
                    else:
                        salt = float(y.text)
                elif y.hint_text == "Gramos" and self.set_error(y.text):
                    if y.text == "":
                        pass
                    elif "," in y.text:
                        grams = float(y.text.replace(",","."))
                    else:    
                        grams = float(y.text)
            kcal_results.append(grams * kcal)
            lipids_results.append(grams * lipids)
            carbohydrates_results.append(grams * carbohydrates)
            sugar_results.append(grams * sugar)
            proteins_results.append(grams * proteins)
            salt_results.append(grams * salt)
            
            
            i1 +=1
        
        self.ids.kcal_result.text= str(round(sum(kcal_results)/100,2))
        self.ids.lipids_result.text= str(round(sum(lipids_results)/100, 2))
        self.ids.carbohydrates_result.text= str(round(sum(carbohydrates_results)/100, 2))
        self.ids.sugar_result.text= str(round(sum(sugar_results)/100,2))
        self.ids.proteins_result.text= str(round(sum(proteins_results)/100, 2))
        self.ids.salt_result.text= str(round(sum(salt_results)/100 , 2))
        
    def set_error(self, text):
        
        for letter in text:
            if letter in ascii_letters or letter in whitespace or letter in punctuation:
                if letter in (",","."):
                    pass
                else:
                    return False
             
        return True        
class TreeViewLabel(Label, TreeViewNode):
    
    
    def set_text(self, instance):
        app = MDApp.get_running_app()
        try:    
            i1 = 0
            i2 = 0
           
            for x in app.root.ids.scr.children[0].children[0].children[2].children[0].children:
                i2= 0
                for y in app.root.ids.scr.children[0].children[0].children[2].children[0].children[i1].children:
                    if y == instance:
                        break
                    i2 += 1
                if y == instance:
                    break
                i1 += 1
            
            app.root.ids.scr.children[0].children[0].children[2].children[0].children[i1].children[i2].text = self.text
            app.root.ids.scr.children[0].id_focused = ""
            app.root.ids.scr.children[0].popup.dismiss()
        
        except:
            instance.text = self.text
            app.root.ids.scr.children[0].id_focused = ""
            app.root.ids.scr.children[0].popup.dismiss()
            
    def set_text_food(self):
        app = MDApp.get_running_app()
        idd = app.root.ids.scr.children[0].id_focused
        self.set_text(idd)
        
class TreeviewGroup(Popup):
    
    treeview = ObjectProperty(None)
    tv = ObjectProperty(None)

    def populate_tree_view(self, tree_view, parent, node):
        if parent is None:
            tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                         is_open=True))
        else:
            tree_node = tree_view.add_node(TreeViewLabel(text=node['node_id'],
                                                         is_open=True), parent)
    
        for child_node in node['children']:
            self.populate_tree_view(tree_view, tree_node, child_node)
            
    def filter(self, f):
        app = MDApp.get_running_app()
        self.treeview.clear_widgets()
        self.tv = TreeView(root_options=dict(text=""),
                           hide_root=True,
                           indent_level=4)
        
        db = DBMaster()
        new_tree = []
        if app.root.ids.scr.current == "calculator_screen":
            
            if "FoodTextInput" in str(app.root.ids.scr.children[0].id_focused):
                tree = []
                for a in app.root.ids.scr.children[0].id_focused.parent.children:
                    if "BrandTextInput" in str(a):
                        rows = db.get_food(a.text)
    
                for r in rows:
                    tree.append({'node_id': r[0], 'children': []})
                for n in tree:
                    if f.lower() in n['node_id'].lower():
                        new_tree.append(n)
                for branch in new_tree:
                    self.populate_tree_view(self.tv, None, branch)
                self.treeview.add_widget(self.tv)
                
            elif "BrandTextInput" in str(app.root.ids.scr.children[0].id_focused):
                tree2 = []
                for a in app.root.ids.scr.children[0].id_focused.parent.children:
                    if "FoodTextInput" in str(a):
                        rows = db.get_brand(a.text)
                
                for r in rows:
                    tree2.append({'node_id': r[0], 'children': []})
                for n in tree2:
                    if f.lower() in n['node_id'].lower():
                        new_tree.append(n)
                for branch in new_tree:
                    self.populate_tree_view(self.tv, None, branch)
        
                self.treeview.add_widget(self.tv)
        
        elif app.root.ids.scr.current == "diet_insight_screen":
            if "FoodTextInput" in str(app.root.ids.scr.children[0].id_focused):
                tree = []
                for a in app.root.ids.scr.children[0].id_focused.parent.children:
                    if "BrandTextInput" in str(a):
                        rows = db.get_food(a.text)
    
                for r in rows:
                    tree.append({'node_id': r[0], 'children': []})
                for n in tree:
                    if f.lower() in n['node_id'].lower():
                        new_tree.append(n)
                for branch in new_tree:
                    self.populate_tree_view(self.tv, None, branch)
                self.treeview.add_widget(self.tv)
                
            elif "BrandTextInput" in str(app.root.ids.scr.children[0].id_focused):
                tree2 = []
                for a in app.root.ids.scr.children[0].id_focused.parent.children:
                    if "FoodTextInput" in str(a):
                        rows = db.get_brand(a.text)
                
                for r in rows:
                    tree2.append({'node_id': r[0], 'children': []})
                for n in tree2:
                    if f.lower() in n['node_id'].lower():
                        new_tree.append(n)
                for branch in new_tree:
                    self.populate_tree_view(self.tv, None, branch)
        
                self.treeview.add_widget(self.tv)
            

class DBMaster():
    
    def __init__(self):
        pass
    
    def get_brand(self, hint):
        
        
        if hint == "":    
            con = sqlite3.connect(join(dirname(__file__), "hola.db"))
            cur = con.cursor()
            cur.execute("SELECT brandname FROM brand ORDER BY brandname ASC")
            return cur.fetchall()
        else:
            con = sqlite3.connect(join(dirname(__file__), "hola.db"))
            cur = con.cursor()
            cur.execute("SELECT foodbrand FROM food WHERE foodname = '{}' ORDER BY foodbrand ASC".format(hint))
            brands = cur.fetchall()
            cur.execute("SELECT brandname FROM brand WHERE brandname NOT IN (SELECT foodbrand FROM food WHERE foodname = '{}' )ORDER BY brandname ASC".format(hint))
            for a in cur.fetchall():
                brands.append(a)
            return brands
        """
    
        sock = socket(AF_INET, SOCK_DGRAM)
        #sock.bind(gethostbyname(gethostname(), 0))
        sock.bind(("localhost",0))
        sock.sendto("0{}".format(hint).encode(),("localhost",2022))
        pack, a = sock.recvfrom(256)
        pack2 = pack.decode()
        res = []
        temp = []
        pack2 = pack2[1:len(pack2)-1]
        for token in pack2.split(", "):
            num = token.replace("(", "").replace(")", "").replace("'", "").replace(",", "")
            temp.append(num)
            if ")" in token:
                res.append(tuple(temp))
                temp = []
              
        sock.close()
        return res
        """
        
    def get_food(self, hint):
        if hint == "":    
            con = sqlite3.connect(join(dirname(__file__), "hola.db"))
            cur = con.cursor()
            cur.execute("SELECT foodname FROM food ORDER BY foodname ASC")
            return cur.fetchall()
        else:
            con = sqlite3.connect(join(dirname(__file__), "hola.db"))
            cur = con.cursor()
            cur.execute("SELECT foodname FROM food WHERE foodbrand = '{}' ORDER BY foodname ASC".format(hint))
            return cur.fetchall()
        """
        
        
        sock = socket(AF_INET, SOCK_DGRAM)
        #sock.bind((gethostbyname(gethostname()), 0))
        sock.bind(("localhost",0))
        sock.sendto("1{}".format(hint).encode(),("localhost",2022))
        pack, a = sock.recvfrom(512)
        pack2 = pack.decode()
        res = []
        temp = []
        pack2 = pack2[1:len(pack2)-1]
        for token in pack2.split(", "):
            num = token.replace("(", "").replace(")", "").replace("'", "").replace(",", "")
            temp.append(num)
            if ")" in token:
                res.append(tuple(temp))
                temp = []
              
        sock.close()
        return res
        """
        
    def get_food_values(self, hint, hint2):
        
        con = sqlite3.connect(join(dirname(__file__), "hola.db"))
        cur = con.cursor()
        cur.execute("SELECT proteins, carbohydrates, sugar, lipids, salt, kcal FROM food WHERE foodname = '{}' AND foodbrand = '{}' ".format(hint, hint2))
        return cur.fetchall()
        """
        
        sock = socket(AF_INET, SOCK_DGRAM)
        #sock.bind(gethostbyname(gethostname()),0)
        sock.bind(("localhost",0))
        sock.sendto("2{}.{}".format(hint,hint2).encode(),("localhost",2022))
        b, a = sock.recvfrom(256)
        data = b.decode()

        data = data[2:len(a)-4]
        values = data.split(", ")
        list = []
        list.append(tuple(values))
        sock.close()
        return list"""
        
        
        
class DiskMaster():
    def __init__(self):
        pass
    
    
    def save_user(self, dictionary):
        dir = join(dirname(__file__), "user.json")
        with open(dir, 'w') as outfile:
            json.dump(dictionary, outfile)
        
    
    def recover_user(self):
        dir = join(dirname(__file__), "user.json")
        with open(dir) as infile:
            data = json.load(infile)
        return data
        
    
    
    def list_all_diets(self):
        path = dirname(__file__) + "\diets"
     
        if not os.path.exists(path):
            os.makedirs(path)
       
        diets = os.listdir(dirname(__file__) + "\diets")
        return diets
    
    def create_diet(self):
        cond = True
        i = 1
        diets = self.list_all_diets()
        while cond:
            if "Dieta" + str(i) + ".json" not in diets:
                open(dirname(__file__) + "\diets\Dieta" + str(i) +".json", "w")
                cond = False
            i += 1
    def create_temp_diet(self,name):
        cond = True
        i = 1
        diets = self.list_all_diets()
        while cond:
            if name + "temp{}.json".format(i) not in diets:
                shutil.copyfile(dirname(__file__) + "\diets\\" + name + ".json", dirname(__file__) + "\diets\\" + name + "temp{}.json".format(i))
                cond = False
            i += 1
        return name + "temp{}.json".format(i-1)    
    
    
    def duplicate_diet(self, name):
        cond = True
        i = 1
        diets = self.list_all_diets()
        while cond:
            if name + "- copia{}.json".format(i) not in diets:
                shutil.copyfile(dirname(__file__) + "\diets\\" + name + ".json", dirname(__file__) + "\diets\\" + name + "- copia{}.json".format(i))
                cond = False
            i += 1
        
        
    def recover_diet(self, name):
        try:
            with open(dirname(__file__) + "\diets\\" +"{}.json".format(name)) as infile:
                data = json.load(infile)
            return data
        except:
            pass   

    def save_diet(self, name , dictionary):
        
        with open(dirname(__file__) + "\diets\\" +  name+ ".json", 'w') as outfile:
            json.dump(dictionary, outfile)
    
    def delete_diet(self, name):
        os.remove(dirname(__file__) + "\diets\\" + name)
                
    def change_diet_name(self, name1, name2):
        if name2 not in self.list_all_diets():
            os.rename(dirname(__file__) + "\diets\\" + name1, dirname(__file__) + "\diets\\" + name2)
 
class StartupPopup(Popup):
    pass
                    
class MainScreen(MDScreen):
    pass

class Reccomendation(ModalView):
    a = StringProperty("")
    
    def show_msg(self, instance):
        if instance == "Kcal":
            dk = DiskMaster()
            userinf = dk.recover_user()
            if userinf["objective"] == "lose":

                if userinf ["exercise"] == "sedentary":
                    if userinf["sex"] == "male":
                    
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"])))*1.2 )-500
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"])))*1.2)-500
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "low":
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"])))*1.375  )-500
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"])))*1.375)-500
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "moderated":
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) * 1.55 )-500
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) *1.55)-500
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "high":
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) * 1.725 )-500
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) * 1.725)-500
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                else:
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) *  1.9)-500
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) *  1.9)-500
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
            
            elif userinf["objective"] == "maintain":
                
                if userinf ["exercise"] == "sedentary":
                    if userinf["sex"] == "male":
                    
                        res = (5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"])))*1.2 
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = (-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"])))*1.2
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "low":
                    if userinf["sex"] == "male":
                        res = (5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"])))*1.375  
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = (-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"])))*1.375
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "moderated":
                    if userinf["sex"] == "male":
                        res = (5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) * 1.55 
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = (-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) *1.55
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "high":
                    if userinf["sex"] == "male":
                        res = (5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) * 1.725 
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = (-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) * 1.725
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                else:
                    if userinf["sex"] == "male":
                        res = (5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) *  1.9
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = (-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) *  1.9
                        self.a = "La cantidad de kcal recomendada es {}".format(round(res,2))
                        self.open()
                        
            elif userinf["objective"] == "define":
                if userinf ["exercise"] == "sedentary":
                    if userinf["sex"] == "male":
                    
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"])))*1.2) -500
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res+250,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"])))*1.2)-500
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res+250,2))
                        self.open()
                        
                elif userinf ["exercise"] == "low":
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"])))*1.375)-500  
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res+250,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"])))*1.375)-500
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res+250,2))
                        self.open()
                        
                elif userinf ["exercise"] == "moderated":
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) * 1.55)-500 
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res+250,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) *1.55)-500
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res+250,2))
                        self.open()
                        
                elif userinf ["exercise"] == "high":
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) * 1.725)-500
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res+250,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) * 1.725)-500
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res+250,2))
                        self.open()
                        
                else:
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) *  1.9)-500
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res+250,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) *  1.9)-500
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res+250,2))
                        self.open()
                        
            elif userinf["objective"] == "clean":
                if userinf ["exercise"] == "sedentary":
                    if userinf["sex"] == "male":
                    
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"])))*1.2 )*1.10
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res*1.2/1.1,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"])))*1.2)*1.10
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res*1.2/1.1,2))
                        self.open()
                        
                elif userinf ["exercise"] == "low":
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"])))*1.375 )*1.10 
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res*1.2/1.1,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"])))*1.375)*1.10
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res*1.2/1.1,2))
                        self.open()
                        
                elif userinf ["exercise"] == "moderated":
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) * 1.55)*1.10 
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res*1.2/1.1,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) *1.55)*1.10
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res*1.2/1.1,2))
                        self.open()
                        
                elif userinf ["exercise"] == "high":
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) * 1.725 )*1.10
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res*1.2/1.1,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) * 1.725)*1.10
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res*1.2/1.1,2))
                        self.open()
                        
                else:
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) *  1.9)*1.10
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res*1.2/1.1,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) *  1.9)*1.10
                        self.a = "La cantidad de kcal recomendada es entre {} y {}".format(round(res,2), round(res*1.2/1.1,2))
                        self.open()
                        
            else:
                
                if  userinf ["exercise"] == "sedentary": 
                    
                    if userinf["sex"] == "male":
                    
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"])))*1.2 )*1.20
                        self.a = "La cantidad de kcal recomendada es más de {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"])))*1.2)*1.20
                        self.a = "La cantidad de kcal recomendada es más de {}".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "low":
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"])))*1.375 )*1.20 
                        self.a = "La cantidad de kcal recomendada es más de {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"])))*1.375)*1.20
                        self.a = "La cantidad de kcal recomendada es más de {}".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "moderated":
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) * 1.55)*1.20 
                        self.a = "La cantidad de kcal recomendada es más de {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) *1.55)*1.20
                        self.a = "La cantidad de kcal recomendada es más de {}".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "high":
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) * 1.725 )*1.20
                        self.a = "La cantidad de kcal recomendada es más de {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) * 1.725)*1.20
                        self.a = "La cantidad de kcal recomendada es más de {}".format(round(res,2))
                        self.open()
                        
                else:
                    if userinf["sex"] == "male":
                        res = ((5 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * float(userinf["age"]))) *  1.9)*1.20
                        self.a = "La cantidad de kcal recomendada es más de {}".format(round(res,2))
                        self.open()
                        
                    else:
                        res = ((-161 + (10 * float(float(userinf["weight"])))+ (6.25 * float(userinf["height"])) - (5 * int(userinf["age"]))) *  1.9)*1.20
                        self.a = "La cantidad de kcal recomendada es más de {}".format(round(res,2))
                        self.open()
                        
        elif instance == "Proteínas":
            dk = DiskMaster()
            userinf = dk.recover_user()
            if userinf["objective"] == "lose":

                if userinf ["exercise"] == "sedentary":
                    if userinf["sex"] == "male":
                    
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteinas recomendada es entre {} y {}g".format(round(res,2), round(float(userinf["weight"]),2))
                        self.open()
                        
                    else:
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteinas recomendada es entre {} y {}g".format(round(res,2), round(float(userinf["weight"]),2))
                        self.open()
                        
                elif userinf ["exercise"] == "low":
                    if userinf["sex"] == "male":
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteinas recomendada es entre {} y {}g".format(round(res,2), round(float(userinf["weight"]),2))
                        self.open()
                        
                    else:
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteinas recomendada es entre {} y {}g".format(round(res,2), round(float(userinf["weight"]),2))
                        self.open()
                        
                elif userinf ["exercise"] == "moderated":
                    if userinf["sex"] == "male":
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteinas recomendada es entre {} y {}g".format(round(res,2), round(float(userinf["weight"]),2))
                        self.open()
                        
                    else:
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteinas recomendada es entre {} y {}g".format(round(res,2), round(float(userinf["weight"]),2))
                        self.open()
                        
                elif userinf ["exercise"] == "high":
                    if userinf["sex"] == "male":
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteinas recomendada es entre {} y {}g".format(round(res,2), round(float(userinf["weight"]),2))
                        self.open()
                        
                    else:
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteinas recomendada es entre {} y {}g".format(round(res,2), round(float(userinf["weight"]),2))
                        self.open()
                        
                else:
                    if userinf["sex"] == "male":
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteinas recomendada es entre {} y {}g".format(round(res,2), round(float(userinf["weight"]),2))
                        self.open()
                        
                    else:
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteinas recomendada es entre {} y {}g".format(round(res,2), round(float(userinf["weight"]),2))
                        self.open()
            
            elif userinf["objective"] == "maintain":
                
                if userinf ["exercise"] == "sedentary":
                    if userinf["sex"] == "male":
                    
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g o {}g".format(round(res,2), round(float(userinf["weight"]),2), round(float(userinf["weight"])*2.2, 2))
                        self.open()
                        
                    else:
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g o {}g".format(round(res,2), round(float(userinf["weight"]),2), round(float(userinf["weight"])*2.2, 2))
                        self.open()
                        
                elif userinf ["exercise"] == "low":
                    if userinf["sex"] == "male":
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g o {}g".format(round(res,2), round(float(userinf["weight"]),2), round(float(userinf["weight"])*2.2, 2))
                        self.open()
                        
                    else:
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g o {}g".format(round(res,2), round(float(userinf["weight"]),2), round(float(userinf["weight"])*2.2, 2))
                        self.open()
                        
                elif userinf ["exercise"] == "moderated":
                    if userinf["sex"] == "male":
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g o {}g".format(round(res,2), round(float(float(float(userinf["weight"]))),2), round(float(userinf["weight"])*2.2, 2))
                        self.open()
                        
                    else:
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g o {}g".format(round(res,2), round(float(userinf["weight"]),2), round(float(userinf["weight"])*2.2, 2))
                        self.open()
                        
                elif userinf ["exercise"] == "high":
                    if userinf["sex"] == "male":
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {} o {}g".format(round(res,2), round(float(userinf["weight"]),2), round(float(userinf["weight"])*2.2, 2))
                        self.open()
                        
                    else:
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {} o {}g".format(round(res,2), round(float(userinf["weight"]),2), round(float(userinf["weight"])*2.2, 2))
                        self.open()
                        
                else:
                    if userinf["sex"] == "male":
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {} o {}g".format(round(res,2), round(float(userinf["weight"]),2), round(float(userinf["weight"])*2.2, 2))
                        self.open()
                        
                    else:
                        res = 0.8 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {} o {}".format(round(res,2), round(float(userinf["weight"]),2), round(float(userinf["weight"])*2.2, 2))
                        self.open()
                        
            elif userinf["objective"] == "define":
                if userinf ["exercise"] == "sedentary":
                    if userinf["sex"] == "male":
                    
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g".format(round(res,2), round(res*3/2.2,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g".format(round(res,2), round(res*3/2.2,2))
                        self.open()
                        
                elif userinf ["exercise"] == "low":
                    if userinf["sex"] == "male":
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g".format(round(res,2), round(res*3/2.2,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g".format(round(res,2), round(res*3/2.2,2))
                        self.open()
                        
                elif userinf ["exercise"] == "moderated":
                    if userinf["sex"] == "male":
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g".format(round(res,2), round(res*3/2.2,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g".format(round(res,2), round(res*3/2.2,2))
                        self.open()
                        
                elif userinf ["exercise"] == "high":
                    if userinf["sex"] == "male":
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g".format(round(res,2), round(res*3/2.2,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g".format(round(res,2), round(res*3/2.2,2))
                        self.open()
                        
                else:
                    if userinf["sex"] == "male":
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g".format(round(res,2), round(res*3/2.2,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es entre {} y {}g".format(round(res,2), round(res*3/2.2,2))
                        self.open()
                        
            elif userinf["objective"] == "clean":
                if userinf ["exercise"] == "sedentary":
                    if userinf["sex"] == "male":
                    
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "low":
                    if userinf["sex"] == "male":
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "moderated":
                    if userinf["sex"] == "male":
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "high":
                    if userinf["sex"] == "male":
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                else:
                    if userinf["sex"] == "male":
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
            else:
                
                if  userinf ["exercise"] == "sedentary": 
                    
                    if userinf["sex"] == "male":
                    
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "low":
                    if userinf["sex"] == "male":
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "moderated":
                    if userinf["sex"] == "male":
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                elif userinf ["exercise"] == "high":
                    if userinf["sex"] == "male":
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                else:
                    if userinf["sex"] == "male":
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
                        
                    else:
                        res = 2.2 * float(float(userinf["weight"]))
                        self.a = "La cantidad de proteínas recomendada es {}g".format(round(res,2))
                        self.open()
        else:
            self.a = "La cantidad recomendada de sal es menos de 5g por día"
            self.open()
    
    
                
class DemoApp(MDApp):
    def build(self):
        self.title = "Ditet"
        self.icon = 'icon.ico'
        self.theme_cls.theme_style = ("Dark")
        return  Builder.load_string(
            """
<StartupPopup>:
    auto_dismiss: False
    title: ""                
    separator_height: 0 
    size_hint: (0.8,.5)
    BoxLayout:
        orientation: "vertical"
        padding: (0,"-45dp",0,0)
        
        MDIconButton:
            icon: "alert"
            icon_size: "160sp"
            pos_hint:{"center_x": 0.5, "top": 1}
            disabled: True

        BoxLayout:
            padding: ("15dp","-35dp","15dp",0)
            Label:
                text: "Esta no es una aplicacíon de uso médico, ante cualquier duda consulte con su médico de cabecera"
                font_size: "16dp"
                text_size: self.size
                
                valign: 'middle'
                halign: "middle"
                halign: "center"

        BoxLayout: 
            size_hint_y: None
            height: "33dp"  
            Button:
                text: "Vale"
                on_release: 
                    root.dismiss()
         


<Reccomendation>:
    size_hint: (0.6,.3)
    BoxLayout:
        orientation: "vertical"
        padding: "20dp"
        Label:
            text: root.a
            font_size: "16dp"
            text_size: self.size
            valign: 'middle'
            halign: "middle"
            halign: "center"

<DeletePopup>:
    auto_dismiss: False
    title: ""                
    separator_height: 0 
    size_hint: (0.8,.5)
    BoxLayout:
        orientation: "vertical"
        padding: (0,"-45dp",0,0)
        MDIconButton:
            icon: "alert"
            icon_size: "200sp"
            pos_hint:{"center_x": 0.5, "top": 1}
            disabled: True
        BoxLayout:
            padding: (0,"-20dp",0,0)
            Label:
                text: "¿Está seguro?"
                font_size: "18dp"
        BoxLayout: 
            size_hint_y: None
            height: "33dp"  
            spacing: "3dp" 
            Button:
                text: "Sí"
                on_release: 
                    root.delete_diet(),
                    root.dismiss()
            Button:
                text: "No"
                on_release: 
                    root.delete_diet_clicked_variable(),
                    root.dismiss()
                
<ChangeNamePopup>:
    auto_dismiss: False
    title: ""                
    separator_height: 0 
    size_hint: (0.8,None)
    height: "120dp"
    BoxLayout:
        orientation: "vertical"
        spacing: "10dp"
        MDTextField:
            id: new_diet_name_tf
            mode: "rectangle"
            hint_text: "Introduzca el nombre nuevo"
            pos_hint:{"center_x": 0.5, "top": 1}
            on_focus: self.required = True

            
        BoxLayout: 
            size_hint_y: None
            height: "33dp"  
            spacing: "3dp" 
            Button:
                text: "Cancelar"
                on_release: 
                    root.delete_diet_clicked_variable,
                    root.dismiss()
            Button:
                text: "Aceptar"
                on_release: 
                    root.change_diet_name()

<NewDietIngredient>:
    id: diet_ingredient
    size_hint:(1,None)
    height: "30dp"
    FoodTextInput:
        id : food_name
        size_hint_x: 0.3
        text: root.food
        
    BrandTextInput:
        id : brand_name
        size_hint_x: 0.3 
        text: root.brand
        
    MDTextFieldRect:
        id : weight_name
        hint_text: "Peso"
        readonly: False
        mode: "rectangle"
        size_hint: (0.20,None)
        height: "30dp" 
        text: root.weight
        on_text: 
            app.root.ids.scr.children[0].set_value2(self.text)
            app.root.ids.scr.children[0].set_food_values(self)
            
        on_focus:
            app.root.ids.scr.children[0].set_value(self)

          
    Widget:
        size_hint_x: 0.2
        
    
    MDIconButton:
        id : delete_ingredient_diet
        mode: "rectangle"
        icon: "delete"
        icon_size: "15sp"
        pos_hint:{"center_x": 1, "center_y": 0.5}

        on_release: root.delete_ingredient(root.parent, root)
            
                                    
<FoodTextInput@MDTextFieldRect>:
    hint_text: "Comida"
    readonly: True
    mode: "rectangle"
    size_hint: (0.3,None)
    height: "30dp"
    on_text: 
        app.root.ids.scr.children[0].set_food_values(self)
       
    on_focus: 
        app.root.ids.scr.children[0].set_id(self)
        app.root.ids.scr.children[0].set_value(self)
        app.root.ids.scr.children[0].display_groups(self)
        

        
<BrandTextInput@MDTextFieldRect>:
    hint_text: "Marca"
    readonly: True
    mode: "rectangle"
    size_hint: (0.3,None)
    height: "30dp"
        app.root.ids.scr.children[0].set_food_values(self)
     
    on_focus: 
        app.root.ids.scr.children[0].set_id(self)
        app.root.ids.scr.children[0].display_groups(self)
        app.root.ids.scr.children[0].set_value(self)


    
<CalculatorFoodBlock>
    id: food_block
    padding : ("5dp",0,"5dp",0)
    cols: 3
    BrandTextInput:
    
    FoodTextInput:
    
    MDTextFieldRect:
        hint_text: "Gramos"
        mode: "rectangle"
        size_hint: (0.3,None)
        height: "30dp"
    
        on_text: app.root.ids.scr.children[0].show_results_grams() 
    MDTextFieldRect:
        hint_text: "Kcal"
        mode: "rectangle"
        size_hint: (0.3,None)
        height: "30dp" 
        on_text: app.root.ids.scr.children[0].show_results_kcal()   
    MDTextFieldRect:
        hint_text: "Grasas"
        mode: "rectangle"
        size_hint: (0.3,None)
        height: "30dp"
        on_text: app.root.ids.scr.children[0].show_results_lipids()
    MDTextFieldRect:
        hint_text: "Glúcidos"
        mode: "rectangle"
        size_hint: (0.3,None)
        height: "30dp"
        on_text: app.root.ids.scr.children[0].show_results_carbohydrates()
    MDTextFieldRect:
        hint_text: "Azúcar"
        mode: "rectangle"
        size_hint: (0.3,None)
        height: "30dp"
        on_text: app.root.ids.scr.children[0].show_results_sugar()
    MDTextFieldRect:
        hint_text_font_size: "5dp"
        hint_text: "Proteínas"
        mode: "rectangle"
        size_hint: (0.3,None)
        height: "30dp"
        on_text: app.root.ids.scr.children[0].show_results_proteins()
    MDTextFieldRect:
        hint_text: "Sal"
        mode: "rectangle"
        size_hint: (0.3,None)
        height: "30dp"
        on_text: app.root.ids.scr.children[0].show_results_salt()

<NewDietListItem>:
    
    on_release:
        app.root.ids.diet_screen.set_diet_option__clicked(self)
        app.root.ids.scr.current= 'diet_insight_screen'
        
    IconRightWidget:
        icon: "dots-vertical" 
        on_press: 
            root.generate_diet_options(self)
            app.root.ids.scr.children[0].set_diet_option__clicked(root)
            
<TreeViewLabel>:
    on_touch_down: root.set_text_food()
        
<TreeviewGroup>:
    id: treeview
    treeview: treeview
    title: ""
    separator_height: 0
    ti: ti
    size_hint: 0.9, 0.5
    #size: 200, 200
    auto_dismiss: False

    BoxLayout
        orientation: "vertical"
        TextInput:
            id: ti
            size_hint_y: .2
            on_text: root.filter(self.text)
            hint_text: "Filtrar por nombre"
            multiline: False
        ScrollView:
            size_hint: (1, 1)
            
            GridLayout:
                id: output
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                id: treeview
        Button:
            size_hint: 1, 0.2
            text: "Cerrar"
            on_release: root.dismiss()

<DietScreen>:
    name: "diet_screen"
    on_pre_enter: 
        app.root.ids.scr.get_screen("diet_insight_screen").delete_diet_temp()
        self.display_diets()
        
    on_enter: self.ids.diet_option_clicked = 0
        
    
    MDBoxLayout:
        
        orientation: 'vertical'
        padding: ("5dp", "65dp" , "5dp", "5dp")
        pos_hint: {"top": 1}
        
        MDScrollView:
            
            MDList:
                id: box
                
        MDRaisedButton:
            text: "Nueva Dieta"
            md_bg_color: "white"
            text_color: "black"
            font_size: 16.2
            pos_hint: {"right": 1, "bottom": 1}
            on_press: root.buttonClicked()
            
<DietInsightScreen>:
    name: "diet_insight_screen"
    on_pre_enter: 
        self.recover_diet()
        self.disable_diet_ingredient()
      
    on_leave:
        self.delete_diet_content()
        
        
    MDBoxLayout:    
        padding: (0, "70dp",0,0)
        orientation: "vertical"
        ScrollView:
            size_hint: (1,1)
            GridLayout:
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: "50dp"
                padding: (0,0,0,"10dp")
                    
                GridLayout:
                    padding: ("5dp",0)
                    id: food_1
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    spacing:"2dp"
                    
                    
                    MDLabel: 
                        size_hint: (1,None)
                        
                        height: "40dp"
                        text: "Comida 1:"
                        pos_hint: {"top":0}
                        
                        
                    MDBoxLayout:    
                        id: results_food_block_1
                        
                        size_hint: (1,None)
                        height: "20dp"
                        padding: ("2dp",0,"2dp","-40dp")
                        
                        
                            
                        MDTextField:
                            id: kcal_food_result_1
                            hint_text: "Kcal"
                            size_hint: (0.14,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_k()
                        
                        MDTextField:
                            id: proteins_food_result_1
                            hint_text: "Proteínas"
                            size_hint: (0.185,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_p()

                        MDTextField:
                            id: carbohydrates_food_result_1
                            hint_text: "Glúcidos"
                            size_hint: (0.175,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_c()

                        
                        MDTextField:
                            id: lipids_food_result_1
                            hint_text: "Grasas"
                            size_hint: (0.15,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_l()

                          
                        MDTextField:
                            id: sugar_food_result_1
                            hint_text_font_size: "5dp"
                            hint_text: "Azúcar"
                            size_hint: (0.15,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_s()

                            
                        MDTextField:
                            id: salt_food_result_1
                            hint_text : "Sal"
                            size_hint: (0.10,None)
                            height: "5dp" 
                            readonly: True
                            text: "0"
                            on_text: root.update_results_sa()

                            
                    MDBoxLayout:
                        size_hint: (1, None)
                        height: "50dp"
                        
                        MDTextButton:
                            id: add_ingredient_1
                            text: "Añadir ingrediente"
                            font_size: "17dp"
                            on_release: 
                                root.add_ingredient(self.parent.parent)
                                
                            
                            disabled: True
                
                GridLayout:
                    
                    padding: ("5dp",0)
                    id: food_2
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    spacing:"2dp"
                    
                    MDLabel: 
                        size_hint: (1,None)
                        
                        height: "40dp"
                        text: "Comida 2:"
                        pos_hint: {"top":0}
                        
                    
                    MDBoxLayout:    
                        id: results_food_block_2
                        
                        size_hint: (1,None)
                        height: "20dp"
                        padding: ("2dp",0,"2dp","-40dp")
                        
                        
                            
                        MDTextField:
                            id: kcal_food_result_2
                            hint_text: "Kcal"
                            size_hint: (0.14,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            helper_text: "hola"
                            on_text: root.update_results_k()
                        
                        MDTextField:
                            id: proteins_food_result_2
                            hint_text: "Proteínas"
                            size_hint: (0.185,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_p()

                        MDTextField:
                            id: carbohydrates_food_result_2
                            hint_text: "Glúcidos"
                            size_hint: (0.175,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_c()

                        
                        MDTextField:
                            id: lipids_food_result_2
                            hint_text: "Grasas"
                            size_hint: (0.15,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_l()

                          
                        MDTextField:
                            id: sugar_food_result_2
                            hint_text_font_size: "5dp"
                            hint_text: "Azúcar"
                            size_hint: (0.15,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_s()

                            
                        MDTextField:
                            id: salt_food_result_2
                            hint_text : "Sal"
                            size_hint: (0.10,None)
                            height: "5dp" 
                            readonly: True
                            text: "0"
                            on_text: root.update_results_sa()
                            
                    MDBoxLayout:
                        size_hint: (1, None)
                        height: "50dp"
                        
                        MDTextButton:
                            id: add_ingredient_2
                            text: "Añadir ingrediente"
                            font_size: "17dp"
                            on_release: root.add_ingredient(self.parent.parent)
                            disabled: True
                
                GridLayout:
                    padding: ("5dp",0)
                    id: food_3
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    spacing:"2dp"
                    
                    MDLabel: 
                        size_hint: (1,None)
                        
                        height: "40dp"
                        text: "Comida 3:"
                        pos_hint: {"top":0}
                        
                    
                    MDBoxLayout:    
                        id: results_food_block_3
                        
                        size_hint: (1,None)
                        height: "20dp"
                        padding: ("2dp",0,"2dp","-40dp")
                        
                        
                            
                        MDTextField:
                            id: kcal_food_result_3
                            hint_text: "Kcal"
                            size_hint: (0.14,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_k()
                        
                        MDTextField:
                            id: proteins_food_result_3
                            hint_text: "Proteínas"
                            size_hint: (0.185,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_p()

                        MDTextField:
                            id: carbohydrates_food_result_3
                            hint_text: "Glúcidos"
                            size_hint: (0.175,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_c()

                        
                        MDTextField:
                            id: lipids_food_result_3
                            hint_text: "Grasas"
                            size_hint: (0.15,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_l()

                          
                        MDTextField:
                            id: sugar_food_result_3
                            hint_text_font_size: "5dp"
                            hint_text: "Azúcar"
                            size_hint: (0.15,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_s()

                            
                        MDTextField:
                            id: salt_food_result_3
                            hint_text : "Sal"
                            size_hint: (0.10,None)
                            height: "5dp" 
                            readonly: True
                            text: "0"
                            on_text: root.update_results_sa()
                            
                    MDBoxLayout:
                        size_hint: (1, None)
                        height: "50dp"
                        
                        MDTextButton:
                            id: add_ingredient_3
                            text: "Añadir ingrediente"
                            font_size: "17dp"
                            on_release: root.add_ingredient(self.parent.parent)
                            disabled: True
                        
                GridLayout:
                    padding: ("5dp",0)
                    id: food_4
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    spacing:"2dp"
                    
                    MDLabel: 
                        size_hint: (1,None)
                        
                        height: "40dp"
                        text: "Comida 4:"
                        pos_hint: {"top":0}
                        
                    
                    MDBoxLayout:    
                        id: results_food_block_4
                        
                        size_hint: (1,None)
                        height: "20dp"
                        padding: ("2dp",0,"2dp","-40dp")
                        
                        
                            
                        MDTextField:
                            id: kcal_food_result_4
                            hint_text: "Kcal"
                            size_hint: (0.14,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_k()
                        
                        MDTextField:
                            id: proteins_food_result_4
                            hint_text: "Proteínas"
                            size_hint: (0.185,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_p()

                        MDTextField:
                            id: carbohydrates_food_result_4
                            hint_text: "Glúcidos"
                            size_hint: (0.175,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_c()

                        
                        MDTextField:
                            id: lipids_food_result_4
                            hint_text: "Grasas"
                            size_hint: (0.15,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_l()

                          
                        MDTextField:
                            id: sugar_food_result_4
                            hint_text_font_size: "5dp"
                            hint_text: "Azúcar"
                            size_hint: (0.15,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_s()

                            
                        MDTextField:
                            id: salt_food_result_4
                            hint_text : "Sal"
                            size_hint: (0.10,None)
                            height: "5dp" 
                            readonly: True
                            text: "0"
                            on_text: root.update_results_sa()
                            
                    MDBoxLayout:
                        size_hint: (1, None)
                        height: "50dp"
                        
                        MDTextButton:
                            id: add_ingredient_4
                            text: "Añadir ingrediente"
                            font_size: "17dp"
                            on_release: root.add_ingredient(self.parent.parent)
                            disabled: True         
                            
                GridLayout:
                    padding: ("5dp",0)
                    id: food_5
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    spacing:"2dp"
                    
                    MDLabel: 
                        size_hint: (1,None)
                        
                        height: "40dp"
                        text: "Comida 5:"
                        pos_hint: {"top":0}
                        
                    
                    MDBoxLayout:    
                        id: results_food_block_5
                        
                        size_hint: (1,None)
                        height: "20dp"
                        padding: ("2dp",0,"2dp","-40dp")
                        
                        
                            
                        MDTextField:
                            id: kcal_food_result_5
                            hint_text: "Kcal"
                            size_hint: (0.14,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_k()
                        
                        MDTextField:
                            id: proteins_food_result_5
                            hint_text: "Proteínas"
                            size_hint: (0.185,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_p()

                        MDTextField:
                            id: carbohydrates_food_result_5
                            hint_text: "Glúcidos"
                            size_hint: (0.175,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_c()

                        
                        MDTextField:
                            id: lipids_food_result_5
                            hint_text: "Grasas"
                            size_hint: (0.15,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_l()

                          
                        MDTextField:
                            id: sugar_food_result_5
                            hint_text_font_size: "5dp"
                            hint_text: "Azúcar"
                            size_hint: (0.15,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_s()

                            
                        MDTextField:
                            id: salt_food_result_5
                            hint_text : "Sal"
                            size_hint: (0.10,None)
                            height: "5dp" 
                            readonly: True
                            text: "0"
                            on_text: root.update_results_sa()
                            
                    MDBoxLayout:
                        size_hint: (1, None)
                        height: "50dp"
                        
                        MDTextButton:
                            id: add_ingredient_5
                            text: "Añadir ingrediente"
                            font_size: "17dp"
                            on_release: root.add_ingredient(self.parent.parent)    
                            disabled: True
                
                
                GridLayout:
                    padding: ("5dp",0)
                    id: food_6
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    spacing:"2dp"
                    
                    MDLabel: 
                        size_hint: (1,None)
                        
                        height: "40dp"
                        text: "Comida 6:"
                        pos_hint: {"top":0}
                        
                    
                    MDBoxLayout:    
                        id: results_food_block_6
                        
                        size_hint: (1,None)
                        height: "20dp"
                        padding: ("2dp",0,"2dp","-40dp")
                        
                        
                            
                        MDTextField:
                            id: kcal_food_result_6
                            hint_text: "Kcal"
                            size_hint: (0.14,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_k()
                        
                        MDTextField:
                            id: proteins_food_result_6
                            hint_text: "Proteínas"
                            size_hint: (0.185,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_p()


                        MDTextField:
                            id: carbohydrates_food_result_6
                            hint_text: "Glúcidos"
                            size_hint: (0.175,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_c()

                        
                        MDTextField:
                            id: lipids_food_result_6
                            hint_text: "Grasas"
                            size_hint: (0.15,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_l()

                          
                        MDTextField:
                            id: sugar_food_result_6
                            hint_text_font_size: "5dp"
                            hint_text: "Azúcar"
                            size_hint: (0.15,None)
                            height: "30dp"
                            readonly: True
                            text: "0"
                            on_text: root.update_results_s()
                            
                        MDTextField:
                            id: salt_food_result_6
                            hint_text : "Sal"
                            size_hint: (0.10,None)
                            height: "5dp" 
                            readonly: True
                            text: "0"
                            on_text: root.update_results_sa()
                            
                    MDBoxLayout:
                        size_hint: (1, None)
                        height: "50dp"
                        
                        MDTextButton:
                            id: add_ingredient_6
                            text: "Añadir ingrediente"
                            font_size: "17dp"
                            on_release: root.add_ingredient(self.parent.parent)
                            disabled: True
        
        
        MDBoxLayout:    
            id: results_food_block
            size_hint: (1,None)
            height: "45dp"
            padding: ("2dp",0,"2dp","-18dp")
            canvas.before:    
                Color:
                    rgba: 0.08,0.07,0.45 ,1
                Rectangle:
                    pos: self.pos
                    size: self.size
            
                
            MyMDTextField:
                id: kcal_food_result
                hint_text: "Kcal"
                size_hint: (0.14,None)
                height: "30dp"
                readonly: True
                text: "0"
                icon_right: "information-outline"
            
            MyMDTextField:
                id: proteins_food_result
                hint_text: "Proteínas"
                size_hint: (0.185,None)
                height: "30dp"
                readonly: True
                text: "0"
                icon_right: "information-outline"

            MDTextField:
                id: carbohydrates_food_result
                hint_text: "Glúcidos"
                size_hint: (0.175,None)
                height: "30dp"
                readonly: True
                text: "0"
            
            MDTextField:
                id: lipids_food_result
                hint_text: "Grasas"
                size_hint: (0.15,None)
                height: "30dp"
                readonly: True
                text: "0"

              
            MDTextField:
                id: sugar_food_result
                hint_text_font_size: "5dp"
                hint_text: "Azúcar"
                size_hint: (0.15,None)
                height: "30dp"
                readonly: True
                text: "0"
                
            MyMDTextField:
                id: salt_food_result
                hint_text : "Sal"
                size_hint: (0.10,None)
                height: "5dp" 
                readonly: True
                text: "0"
                icon_right: "information-outline"
                                            
                               
        BoxLayout:
            
            canvas.before:    
                Color:
                    rgba: 0.08,0.07,0.45 ,1
                Rectangle:
                    pos: self.pos
                    size: self.size
            orientation: "horizontal"
            size_hint: (1,None)
            height: "35dp"
            
            MDRaisedButton:
                id: save_btn
                text: "Guardar"
                text_color: "white"
                md_bg_color: 0.08,0.07,0.45 
                font_size: 16.2
                size_hint_x: 1
                pos_hint: {"right": 1, "bottom": 1}
                disabled: True
                on_release:
                    root.save_diet()
                    app.root.ids.nav_drawer.disabled = False
                    exit_btn.text = "Salir"
                    save_btn.disabled = True
                    edit_btn.disabled = False
                    add_ingredient_1.disabled = True
                    add_ingredient_2.disabled = True
                    add_ingredient_3.disabled = True
                    add_ingredient_4.disabled = True
                    add_ingredient_5.disabled = True
                    add_ingredient_6.disabled = True
                    root.disable_diet_ingredient()
                    
            MDRaisedButton:
                id: exit_btn
                text: "Salir"
                text_color: "white"
                md_bg_color: 0.08,0.07,0.45 
                font_size: 16.2
                size_hint_x: 1
                pos_hint: {"left": 1, "bottom": 1}
                on_release: 
                    root.exit_btn_press(self)
                    
                
            MDRaisedButton:
                id: edit_btn
                text: "Editar"
                text_color: "white"
                md_bg_color: 0.08,0.07,0.45 
                font_size: 16.2
                size_hint_x: 1
                pos_hint: {"center_x": 0.5, "bottom": 1}
                on_release: 
                    exit_btn.text = "Cancelar"
                    save_btn.disabled = False
                    edit_btn.disabled = True
                    app.root.ids.nav_drawer.disabled = True
                    add_ingredient_1.disabled = False
                    add_ingredient_2.disabled = False
                    add_ingredient_3.disabled = False
                    add_ingredient_4.disabled = False
                    add_ingredient_5.disabled = False
                    add_ingredient_6.disabled = False
                    root.enable_diet_ingredient()
                
            
    
<UserScreen>    
    name: 'user_screen'
    on_pre_enter: self.charge_user_info()
    on_enter: app.root.ids.diet_screen.diet_option__clicked = 0
    MDBoxLayout:
        orientation: "vertical"
        pos_hint: {"top": 1}
        adaptive_height: True
        padding: (0, "80dp" , 0, 0)
        
        MDGridLayout:
            cols:3
            size_hint: (0.9,1)
            pos_hint: {"center_x":0.5, "center_y": 0.5}
            
            
            spacing: ("20dp",0)
            MDLabel:
                text: "Nombre"
                bold: True
                pos_hint: {"left": 1, "top": 0}
                size_hint: (None,1)
                
            MDLabel:
                text: "Peso"
                bold: True
                pos_hint: {"left": 1, "top": 0}
                size_hint: (None,1)
                width: "60dp"
            MDLabel:
                text: "Altura(cm)"
                bold: True
                pos_hint: {"left": 1, "top": 0}
                size_hint: (None,1)
                width: "80dp"
            
            MDTextField:
                id: name_tf_user
                text: ""
                readonly:True
                
            MDTextField:
                id: weight_tf_user 
                text: ""
                width: "20dp"
                readonly:True
                max_text_length: 6
                on_focus: self.required = True
                helper_text: "*"
                helper_text_mode: "on_error"
                on_text: root.error_message_letters(self.text, self)
                
                
            MDTextField:
                id: height_tf_user
                text: ""
                width: "20dp"
                readonly:True
                max_text_length: 5
                on_focus: self.required = True
                helper_text: "*"
                helper_text_mode: "on_error"
                on_text: root.error_message_letters(self.text, self)
                
        MDGridLayout:
            cols:2
            size_hint: (0.9,1)
            pos_hint: {"center_x":0.5, "center_y": 0.5}
            padding: (0,"80dp",0,0)
            spacing: ("20dp",0)
            
            MDLabel:
                text: "Edad"
                bold: True
                pos_hint: {"left": 1, "top": 0}
                size_hint: (None,1)
                width: "40dp"
                
            MDLabel:
                text: "Sexo"
                bold: True
                pos_hint: {"left": 1, "top": 0}
                size_hint: (None,1)
                width: "40dp"
                
            
            MDTextField:
                id: age_tf_user
                text: ""
                readonly:True
                width: "20dp"
                max_text_length: 3
                on_focus: self.required = True
                helper_text: "*"
                helper_text_mode: "on_error"
                on_text: root.error_message_letters(self.text, self)
                
                
            BoxLayout:
                orientation: "horizontal"
                spacing: "45dp"
                hola : male_cb_user
                BoxLayout:
                    orientation:"horizontal"                            
                    MDLabel:
                        text: "H"
                    MDCheckbox:
                        
                        group: "sex_cb"
                        id: male_cb_user
                        
                        disabled: True
                        
                BoxLayout:
                    orientation:"horizontal"
                    MDLabel:
                        text: "M"
                    MDCheckbox:
                        
                        group: "sex_cb"
                        id: female_cb_user
                        
                        disabled: True
        MDGridLayout:
            cols:2
            size_hint: (0.9,1)
            pos_hint: {"center_x":0.5, "center_y": 0.5}
            padding: (0,"320dp",0,0)
            spacing: ("-80dp","20dp")
            
            MDLabel:
                text: "Objetivo"
                bold: True
                font_size: "16.5dp"
                pos_hint: {"left": 1, "top": 1}
                size_hint: (None,None)
                width: "128dp"
                height: "20dp"
                
            Widget:
            
                                   
            BoxLayout:
                orientation:"horizontal"     
                spacing: "-90dp"          
                size_hint: (1, None)
                height: "20dp"     
                MDLabel:
                    text: "Perder Peso"
                    font_size: "15dp"
                    size_hint: (None,1)
                    width: "110dp"
                    
                MDCheckbox:
                    id: lose_cb_user
                    group: "objective_cb"
                    size: "48dp", "48dp"
                    disabled: True
                
                    
            BoxLayout:
                orientation:"horizontal" 
                size_hint: (1, None)
                height: "20dp"                              
                MDLabel:
                    text: "Mantener peso"
                    font_size: "15dp"
                    size_hint: (None,1)
                    width: "70dp"
                MDCheckbox:
                    id: maintain_cb_user
                    group: "objective_cb"
                    disabled: True
            
            BoxLayout:
                orientation:"horizontal"   
                spacing: "-90dp"             
                size_hint: (1, None)
                height: "20dp"                   
                MDLabel:
                    text: "Definición"
                    font_size: "15dp"
                    size_hint: (None,1)
                    width: "110dp"
                MDCheckbox:
                    id: define_cb_user
                    group: "objective_cb"
                    disabled: True
                    
                
            BoxLayout:
                orientation:"horizontal" 
                size_hint: (1, None)
                height: "20dp"                              
                MDLabel:
                
                    text: "Volumen limpio"
                    font_size: "15dp"
                    size_hint: (None,1)
                    width: "70dp"
                MDCheckbox:
                    id: clean_vol_cb_user
                    group: "objective_cb"
                    disabled: True
                    
                    
                    
                    
            BoxLayout:
                orientation:"horizontal"  
                size_hint: (1, None)
                height: "20dp"   
                spacing: "-90dp"                              
                MDLabel:
                    text: "Volumen"
                    font_size: "15dp"
                    size_hint: (None,1)
                    width: "110dp"
                MDCheckbox:
                    id: vol_cb_user
                    group: "objective_cb"
                    disabled: True
                   
                                 
        MDGridLayout:
            cols:2
            size_hint: (0.9,1)
            pos_hint: {"center_x":0.5, "center_y": 0.5}
            padding: (0,"150dp",0,0)
            spacing: ("-80dp","20dp")
            
            MDLabel:
                text: "Ejercicio semanal"
                bold: True
                font_size: "16.5dp"
                pos_hint: {"left": 1, "top": 1}
                size_hint: (None,None)
                width: "128dp"
                height: "20dp"
                
            Widget:
            
                                   
            BoxLayout:
                orientation:"horizontal"     
                spacing: "-90dp"          
                size_hint: (1, None)
                height: "20dp"     
                MDLabel:
                    text: "Sedentario"
                    font_size: "15dp"
                    size_hint: (None,1)
                    width: "110dp"
                    
                MDCheckbox:
                    id: sedentary_cb_user
                    group: "exercise_cb"
                    size: "48dp", "48dp"
                    disabled: True
                
                    
            BoxLayout:
                orientation:"horizontal" 
                size_hint: (1, None)
                height: "20dp"                              
                MDLabel:
                    text: "Bajo(1-3)"
                    font_size: "15dp"
                    size_hint: (None,1)
                    width: "70dp"
                MDCheckbox:
                    id: low_cb_user
                    group: "exercise_cb"
                    disabled: True
            
            BoxLayout:
                orientation:"horizontal"   
                spacing: "-90dp"             
                size_hint: (1, None)
                height: "20dp"                   
                MDLabel:
                    text: "Moderado (3-5)"
                    font_size: "15dp"
                    size_hint: (None,1)
                    width: "110dp"
                MDCheckbox:
                    id: moderated_cb_user
                    group: "exercise_cb"
                    disabled: True
                    
                
            BoxLayout:
                orientation:"horizontal" 
                size_hint: (1, None)
                height: "20dp"                              
                MDLabel:
                
                    text: "Alto (6-7)"
                    font_size: "15dp"
                    size_hint: (None,1)
                    width: "70dp"
                MDCheckbox:
                    id: high_cb_user
                    group: "exercise_cb"
                    disabled: True
                    
                    
                    
                    
            BoxLayout:
                orientation:"horizontal"  
                size_hint: (1, None)
                height: "20dp"   
                spacing: "-90dp"                              
                MDLabel:
                    text: "Pro (2 por día)"
                    font_size: "15dp"
                    size_hint: (None,1)
                    width: "110dp"
                MDCheckbox:
                    id: pro_cb_user
                    group: "exercise_cb"
                    disabled: True        
                
                    
        FloatLayout:
                    
            MDRaisedButton:
                id: save_btn_user
                text: "Guardar"
                md_bg_color: 0.08,0.07,0.45  
                text_color: "white"
                font_size: 16.2
                pos_hint: {"left":1, "bottom": 1}
                size_hint: (.33,.2)  
                disabled: True   
                on_release: root.save_btn_press()
                canvas.before:    
                    Color:
                        rgba: 0.08,0.07,0.45 ,1
                    Rectangle:
                        pos: self.pos
                        size: self.size
            
            MDRaisedButton:
                id: cancel_btn_user
                text: "Cancelar"
                md_bg_color: 0.08,0.07,0.45  
                text_color: "white"
                font_size: 16.2
                pos_hint: {"center_x":0.5, "bottom": 1}
                size_hint: (.34,.2)  
                disabled: True
                canvas.before:    
                    Color:
                        rgba: 0.08,0.07,0.45 ,1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                on_release:
                    save_btn_user.disabled = True
                    cancel_btn_user.disabled = True
                    edit_btn_user.disabled = False
                    name_tf_user.readonly = True
                    weight_tf_user.readonly = True
                    height_tf_user.readonly = True
                    age_tf_user.readonly = True
                    male_cb_user.disabled = True
                    female_cb_user.disabled = True
                    sedentary_cb_user.disabled = True
                    low_cb_user.disabled = True
                    moderated_cb_user.disabled = True
                    high_cb_user.disabled = True
                    pro_cb_user.disabled = True
                    lose_cb_user.disabled = True
                    maintain_cb_user.disabled = True
                    define_cb_user.disabled = True
                    clean_vol_cb_user.disabled = True
                    vol_cb_user.disabled = True
                    app.root.ids.nav_drawer.disabled = False
                    root.charge_user_info()    
                                        
                    
            MDRaisedButton:
                id: edit_btn_user
                text: "Editar"
                md_bg_color: 0.08,0.07,0.45  
                text_color: "white"
                font_size: 16.2
                pos_hint: {"right":1, "bottom": 1}
                size_hint: (.33,.2)  
                disabled: False
                canvas.before:    
                    Color:
                        rgba: 0.08,0.07,0.45 ,1
                    Rectangle:
                        pos: self.pos
                        size: self.size
                on_release: 
                
                    save_btn_user.disabled = False
                    cancel_btn_user.disabled = False
                    edit_btn_user.disabled = True
                    name_tf_user.readonly = False
                    weight_tf_user.readonly = False
                    height_tf_user.readonly = False
                    age_tf_user.readonly = False
                    male_cb_user.disabled = False
                    female_cb_user.disabled = False
                    sedentary_cb_user.disabled = False
                    low_cb_user.disabled = False
                    moderated_cb_user.disabled = False
                    high_cb_user.disabled = False
                    pro_cb_user.disabled = False  
                    lose_cb_user.disabled = False
                    maintain_cb_user.disabled = False
                    define_cb_user.disabled = False
                    clean_vol_cb_user.disabled = False
                    vol_cb_user.disabled = False  
                    app.root.ids.nav_drawer.disabled = True


<CalculatorScreen>
    name: 'calculator_screen'
    on_enter: app.root.ids.diet_screen.diet_option__clicked = 0
    MDBoxLayout:
        
        orientation: 'vertical'
        padding: (0, "70dp" , 0, 0)
        pos_hint: {"top": 1}
        spacing: "5dp"
        ScrollView:
            size_hint:(1,1)
            
    
            GridLayout:
                id: ingredients_box
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: "100dp"
                
            
                CalculatorFoodBlock:
                
        MDBoxLayout:    
            id: food_block
            padding : ("5dp",0,"5dp",0)
            size_hint: (1,None)
            height: "33dp"
            padding: ("2dp",0,"2dp","-20dp")
            
            
                
            MDTextField:
                id: kcal_result
                hint_text: "Kcal"
                size_hint: (0.14,None)
                height: "30dp"
                readonly: True
                text: "0"
                
            
            MDTextField:
                id: proteins_result
                hint_text: "Proteínas"
                size_hint: (0.185,None)
                height: "30dp"
                readonly: True
                text: "0"
                
            MDTextField:
                id: carbohydrates_result
                hint_text: "Glúcidos"
                size_hint: (0.175,None)
                height: "30dp"
                readonly: True
                text: "0"
            
            MDTextField:
                id: lipids_result
                hint_text: "Grasas"
                size_hint: (0.15,None)
                height: "30dp"
                readonly: True
                text: "0"
              
            MDTextField:
                id: sugar_result
                hint_text: "Azúcar"
                size_hint: (0.15,None)
                height: "30dp"
                readonly: True
                text: "0"
                
            MDTextField:
                id: salt_result
                hint_text : "Sal"
                size_hint: (0.10,None)
                height: "30dp"
                readonly: True
                text: "0"
                
                
        
        MDRaisedButton:
            text: "Nuevo Ingrediente"
            text_color: "white"
            md_bg_color: 0.08,0.07,0.45 
            font_size: 16.2
            size_hint_x: 1
            pos_hint: {"center_x": 0.5, "bottom": 1}
            on_press: root.buttonClicked()
            
<MainScreen>:
    name: "main_screen"
    
    BoxLayout:
        orientation: 'vertical'
        
        MDTopAppBar:
            id: title_bar
            title: 'Dietas'
            md_bg_color: 0.08,0.07,0.45                     
            specific_text_color: 1,1,1
            left_action_items: [["menu", lambda x: nav_drawer.set_state('toggle')]]
            
        Widget:


    MDNavigationLayout:

        ScreenManager:
            id: scr

            
            DietScreen:
                id: diet_screen
            UserScreen:
                id: user_screen
            CalculatorScreen:
            DietInsightScreen:
                id: diet_insight_screen
        
        MDNavigationDrawer:
            id: nav_drawer
        
            BoxLayout:
                orientation: 'vertical'
                spacing: '8dp'
               
                ScrollView:
                    MDList:

                        OneLineIconListItem:
                            text: 'Usuario'
                            on_press: 
                                scr.current= 'user_screen'
                                title_bar.title = "Usuario"
                                nav_drawer.set_state('close')
                            IconLeftWidgetWithoutTouch:
                                icon: 'account'
                                on_press: 
                                    scr.current= 'user_screen'
                                    title_bar.title = "Usuario"
                                    nav_drawer.set_state('close')
                                
                        OneLineListItem:
                            text: 'Dietas'
                            on_press: 
                                scr.current= 'diet_screen'
                                title_bar.title = "Dietas"
                                nav_drawer.set_state('close')
                                
                        OneLineListItem:
                            text: "Calcular comida"
                            on_press: 
                                scr.current= 'calculator_screen'
                                title_bar.title = "Calculadora Comida"
                                nav_drawer.set_state('close')
                                
                        
                                
                                
MainScreen:
            """)
    def on_start(self, **kwargs):
        self.root.ids.scr.children[0].display_diets()
        
        try: 
            a = DiskMaster
            b = a.recover_user("a")
            if b["weight"] == "" or b["height"] == "" or b["age"] == "" or b["sex"] == "" or b["exercise"] == "" or b["objective"] == "":
                self.root.ids.nav_drawer.disabled = True
                self.root.ids.scr.current = "user_screen"
        except:
            self.root.ids.nav_drawer.disabled = True
            self.root.ids.scr.current = "user_screen"
            self.root.ids.scr.children[0].ids.edit_btn_user.disabled = True
            self.root.ids.scr.children[0].ids.save_btn_user.disabled = False
            self.root.ids.scr.children[0].ids.cancel_btn_user.disabled = True           
            self.root.ids.scr.children[0].ids.name_tf_user.readonly = False
            self.root.ids.scr.children[0].ids.weight_tf_user.readonly = False
            self.root.ids.scr.children[0].ids.height_tf_user.readonly = False
            self.root.ids.scr.children[0].ids.age_tf_user.readonly = False
            self.root.ids.scr.children[0].ids.male_cb_user.disabled = False
            self.root.ids.scr.children[0].ids.female_cb_user.disabled = False
            self.root.ids.scr.children[0].ids.sedentary_cb_user.disabled = False
            self.root.ids.scr.children[0].ids.low_cb_user.disabled = False
            self.root.ids.scr.children[0].ids.moderated_cb_user.disabled = False
            self.root.ids.scr.children[0].ids.high_cb_user.disabled = False
            self.root.ids.scr.children[0].ids.pro_cb_user.disabled = False  
            self.root.ids.scr.children[0].ids.lose_cb_user.disabled = False
            self.root.ids.scr.children[0].ids.maintain_cb_user.disabled = False
            self.root.ids.scr.children[0].ids.define_cb_user.disabled = False
            self.root.ids.scr.children[0].ids.clean_vol_cb_user.disabled = False
            self.root.ids.scr.children[0].ids.vol_cb_user.disabled = False

        #StartupPopup().open()
        
DemoApp().run()

