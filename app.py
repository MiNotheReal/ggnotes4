import re
from tkinter import W
from flask import Flask, redirect, render_template, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.widgets import TextArea
from wtforms.validators import InputRequired, Email, Length, Optional
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import os
from dotenv import load_dotenv
import requests
import Dictionary
import json


app = Flask(__name__)
app.config["SECRET_KEY"] = "Hello2"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://jyycpfgrvcjxfl:d3cd2c5f5f6602620363654e42e3277c52a5ea9d2350d128d4257fa2d67e5e9e@ec2-54-163-34-107.compute-1.amazonaws.com:5432/d9aoko2k9fsur5"
app.config['SQLALCHEMY_BINDS'] = {'champions' : 'postgres://yxwdfqtakwybbd:6ce576a71a5ebfe85c3e59caa50b25081cfe6a846f44774f8afe7aa9727b63ce@ec2-3-214-2-141.compute-1.amazonaws.com:5432/daj37adndjgcq5'}
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"




load_dotenv()
API_KEY = "RGAPI-8ba3d258-d8bf-43a5-8183-df6a8c4a32d6"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class Champions(db.Model):
    __bind_key__ = "champions"
    id = db.Column(db.Integer, primary_key=True)
    Userid = db.Column(db.String(7))
    championname = db.Column(db.String(20))
    notes = db.Column(db.String(1000))






@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField("password",validators=[InputRequired(),Length(min=8, max=80)])
    remember = BooleanField("remember me")

class RegisterForm(FlaskForm):
    email = StringField("email", validators=[InputRequired(), Email(message="Invalid email"), Length(max=50)])
    username = StringField("username", validators=[InputRequired(), Length(min=4, max=15)])
    champions = TextAreaField("champions", validators=[Optional(), Length(min=4, max=15)])
    password = PasswordField("password", validators=[InputRequired(), Length(min=8, max=80)])    

class NoteForm(FlaskForm):
    Aatrox=StringField("Aatrox",validators=[Optional(),Length(max=1000)])

class Championswitch(FlaskForm):
    Placeholder0=TextAreaField("",validators=[Optional(),Length(max=1000)])
    Placeholder1=TextAreaField("",validators=[Optional(),Length(max=1000)])
    Placeholder2=TextAreaField("",validators=[Optional(),Length(max=1000)])
    Placeholder3=TextAreaField("",validators=[Optional(),Length(max=1000)])
    Placeholder4=TextAreaField("",validators=[Optional(),Length(max=1000)])
    Placeholder5=TextAreaField("",validators=[Optional(),Length(max=1000)])
    Placeholder6=TextAreaField("",validators=[Optional(),Length(max=1000)])
    Placeholder7=TextAreaField("",validators=[Optional(),Length(max=1000)])
    Placeholder8=TextAreaField("",validators=[Optional(),Length(max=1000)])
    Placeholder9=TextAreaField("", validators=[Optional(),Length(max=1000)])
    Gameplan=TextAreaField("", validators=[Optional(),Length(max=3000)])


@app.route("/test")
def test():
    conn = sqlite3.connect("champions.db")
    cursor = conn.cursor()
    cursor.execute("select * from champions;")
    result = cursor.fetchall()
    length = len(result)
    list = []
    for Num in range(length):
        if result[Num][1] == str(current_user.id):
            list.append([result[Num]])
    return str(list)
            
@app.route("/championsearch", methods=["Get", "Post"])
def notes():
    if current_user.is_authenticated:
        LogedIn = "logout"
        Url_LogedIn = url_for('logout')
    else:
        LogedIn = "login"
        Url_LogedIn = url_for('login')

    return render_template('championsearch.html', LogedIn=LogedIn, Url_LogedIn=Url_LogedIn)


@app.route("/champion/<name>", methods=["Get", "Post"])
def champion(name):
    if current_user.is_authenticated:
        LogedIn = "logout"
        Url_LogedIn = url_for('logout')
    else:
        LogedIn = "login"
        Url_LogedIn = url_for('login')

    if name not in Dictionary.Champ_Logo_dict:
        return redirect(url_for("home"))
    replacer = name
    replacer = replacer.replace("&", "")
    replacer = replacer.replace(" ", "")
    replacer = replacer.replace("'", "")
    replacer = replacer.replace(",", "")
    champion = replacer
    form = Championswitch()
    conn = sqlite3.connect("champions.db")
    cursor = conn.cursor()
    if form.validate_on_submit():
        cursor.execute(f"select * from champions where Userid = {current_user.id} and championname =" + f"'{champion}';")
        result = cursor.fetchall()
        if bool(result) == True:
            Champions.query.filter_by(Userid=current_user.id, championname=champion).update({Champions.notes : form.Placeholder0 .data})
        else:
            new_note = Champions(Userid = current_user.id, championname = champion, notes = form.Placeholder0.data)     
            db.session.add(new_note)
        db.session.commit()
    cursor.execute(f"select * from champions where Userid = {current_user.id} and championname =" + f"'{champion}';")
    result = cursor.fetchall()
    if bool(result) == True:
        form.Placeholder0.data = result[0][3]
    


    return render_template('champion.html', LogedIn=LogedIn, Url_LogedIn=Url_LogedIn, champion=name, form=form)

@app.route("/add", methods=["Get", "Post"])
def add():
    form = NoteForm()
    



    if form.validate_on_submit():

        Champions.query.filter_by(Userid=current_user.id, championname="Aatrox").update({Champions.notes : form.Aatrox.data})
        db.session.commit()

    conn = sqlite3.connect("champions.db")
    cursor = conn.cursor()
    b = "sejuani"
    cursor.execute(f"select * from champions where Userid = {current_user.id} and championname =" + f"'{b}';")
    result = cursor.fetchall()
    if bool(result) == True:
        form.Aatrox.data = result[0][3]
    else:
        new_note = Champions(Userid = current_user.id, championname = "Aatrox", notes = "")       
        db.session.add(new_note)
        db.session.commit()

    return render_template("test.html", form=form)
    

@app.route('/<name>')
def index(name):
    return redirect(url_for("home"))



@app.route('/home')
def home():
    if current_user.is_authenticated:
        LogedIn = "logout"
        Url_LogedIn = url_for('logout')
    else:
        LogedIn = "login"
        Url_LogedIn = url_for('login')
    return render_template('index.html', LogedIn=LogedIn, Url_LogedIn=Url_LogedIn)

@app.route('/login', methods=["Get", "Post"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for("home"))
        
        return "<h1> Invalid username or password </h1>"
    return render_template('login.html', form=form)

@app.route('/signup', methods=["Get", "Post"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method="sha256")
        new_user = User(username = form.username.data, email=form.email.data, password=hashed_password)       
        
        db.session.add(new_user)
        db.session.commit()
        
        

        return "<h1> New user has been created </h1>"

    return render_template('signup.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/Lobby", methods=["POST", "GET"])
def Lobby():
    if current_user.is_authenticated:
        LogedIn = "logout"
        Url_LogedIn = url_for('logout')
    else:
        LogedIn = "login"
        Url_LogedIn = url_for('login')

    
    Summoner_Names = str(request.form["name_input"])
    Summoner_Names = Summoner_Names.split(" joined the lobby ")
    Player_Num = len(Summoner_Names)
    replacer = str(Summoner_Names[Player_Num-1])
    replacer = replacer.replace(" joined the lobby", "")
    Summoner_Names.pop(Player_Num-1)
    Summoner_Names.append(replacer)
    
    #Ingame Check
    Ingame_Player = Summoner_Names[0]
    Ingame_Player_Acc_Info = requests.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{Ingame_Player}?api_key={API_KEY}")
    Ingame_Player_Sum_Id = str(Ingame_Player_Acc_Info.json()["id"])
    Ingame_Info = requests.get(f"https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{Ingame_Player_Sum_Id}?api_key={API_KEY}")
    Ingame_Inf = Ingame_Info.json()



    if (Ingame_Inf == {'status': {'message': 'Data not found', 'status_code': 404}}):

        tiers = []
        ranks = []
        winrates = []
        for x in range(Player_Num):
            Summoner_Name = Summoner_Names[x]
            Acc_Info = requests.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{Summoner_Name}?api_key={API_KEY}")
            Summoner_Id = str(Acc_Info.json()["id"])

            Sum_Info = requests.get(f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{Summoner_Id}?api_key={API_KEY}")
            if (str(Sum_Info.json()[0]["queueType"]) == "RANKED_SOLO_5x5"):
                Solo_Num = 0
            elif (str(Sum_Info.json()[1]["queueType"]) == "RANKED_SOLO_5x5"):
                Solo_Num = 1
            elif (str(Sum_Info.json()[2]["queueType"]) == "RANKED_SOLO_5x5"):
                Solo_Num = 2

            tiers.append(str(Sum_Info.json()[Solo_Num]["tier"]))
            ranks.append(str(Sum_Info.json()[Solo_Num]["rank"]))
            winrates.append(str(round((Sum_Info.json()[Solo_Num]["wins"] / (Sum_Info.json()[Solo_Num]["losses"] + Sum_Info.json()[Solo_Num]["wins"]))*100, 2)))

        return render_template(f"Lobby_Names{len(Summoner_Names)}.html", tiers=tiers , ranks=ranks , winrates=winrates, Summoner_Names=Summoner_Names, LogedIn=LogedIn, Url_LogedIn=Url_LogedIn)
    else:
        return redirect(url_for("ingame", Summoner_Names=Summoner_Names))


@app.route("/ingame", methods=["POST", "GET"])
def ingame():
    if current_user.is_authenticated:
        LogedIn = "logout"
        Url_LogedIn = url_for('logout')
    else:
        LogedIn = "login"
        Url_LogedIn = url_for('login')


    form = Championswitch()
    
    Summoner_Names = request.args["Summoner_Names"]
    Acc_Info = requests.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{Summoner_Names}?api_key={API_KEY}")
    Summoner_Id = str(Acc_Info.json()["id"])
    current_game = requests.get(f"https://euw1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{Summoner_Id}?api_key={API_KEY}")
    GameType = Dictionary.GameType_dict[str(current_game.json()["gameQueueConfigId"])]
    names = []
    champions = []
    champion_infos = []
    tiers = []
    ranks = []
    winrates = []
    Champ_Logos = []
    Games = []
    Wins = []
    MasteryLvl = []
    bans = []
    runes = []
    runeStyle = []
    runeNames = []
    for Num in range(10):
        #MasteryLvl.append((requests.get(f"https://euw1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{current_game.json()['participants'][Num]['summonerId']}/by-champion/{current_game.json()['participants'][Num]['championId']}?api_key={API_KEY}").json()["championLevel"]))
        champions.append(Dictionary.Champion_dict[current_game.json()["participants"][Num]["championId"]])
        names.append(current_game.json()["participants"][Num]["summonerName"])
        bans.append(Dictionary.Champ_Logo_dict[Dictionary.Champion_dict[current_game.json()["bannedChampions"][Num]["championId"]]])

    conn = sqlite3.connect("champions.db")
    cursor = conn.cursor()
    for Num in range(10):
        Champ_Logos.append(Dictionary.Champ_Logo_dict[champions[Num]])
        replacer = champions[Num]
        replacer = replacer.replace("&", "")
        replacer = replacer.replace(" ", "")
        replacer = replacer.replace("'", "")
        replacer = replacer.replace(",", "")
        replacer = replacer.replace(".", "")
        
        cursor.execute(f"select * from champions where Userid = {current_user.id} and championname =" + f"'{replacer}';")
        result = cursor.fetchall()
        if bool(result) == True:
            champion_infos.append(result[0][3])
        else:
            champion_infos.append("Note Space")

    #gettingRunes
    for Player_Num in range(10):
        runeStyle.append(current_game.json()["participants"][Player_Num]["perks"]["perkStyle"])
        runeStyle.append(current_game.json()["participants"][Player_Num]["perks"]["perkSubStyle"])
        for Perk_Num in range(9):
            runes.append(current_game.json()["participants"][Player_Num]["perks"]["perkIds"][Perk_Num])

    #getting Rune Names
    RuneInfos = requests.get(f"http://ddragon.leagueoflegends.com/cdn/10.16.1/data/en_US/runesReforged.json")
    RuneInfos = RuneInfos.json()
    for players in range(10):
        for mainRunes in range(4):
            for sub in RuneInfos:
                if sub["id"] == runeStyle[2*players]:
                    for sub2 in sub["slots"][mainRunes]["runes"]:
                        if int(sub2["id"]) == runes[(9*players) + mainRunes]:
                            runeNames.append(sub2["name"])  
        for secondaryRunes in range(2):
            for sub in RuneInfos:
                if sub["id"] == runeStyle[2*players+1]:
                    for triple in range(1,4):
                        for sub2 in sub["slots"][triple]["runes"]:
                            if int(sub2["id"]) == runes[(9*players) + 4 + secondaryRunes]:
                                runeNames.append(sub2["name"])
        for space in range(3):
            runeNames.append("None")

    for Num in range(10):
        Summoner_Name = names[Num]
        Acc_Info = requests.get(f"https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{Summoner_Name}?api_key={API_KEY}")
        Summoner_Id = str(Acc_Info.json()["id"])
        Sum_Info = requests.get(f"https://euw1.api.riotgames.com/lol/league/v4/entries/by-summoner/{Summoner_Id}?api_key={API_KEY}")
        if len(Sum_Info.json()) > 0:
            Queue_Num = len(Sum_Info.json())
            for Queue in range(Queue_Num):
                if (str(Sum_Info.json()[Queue]["queueType"]) == "RANKED_SOLO_5x5"):
                    Solo_Num = Queue
            tiers.append(str(Sum_Info.json()[Solo_Num]["tier"]))
            ranks.append(str(Sum_Info.json()[Solo_Num]["rank"]))
            Games.append(str((Sum_Info.json()[Solo_Num]["losses"] + Sum_Info.json()[Solo_Num]["wins"])))
            Wins.append(str(Sum_Info.json()[Solo_Num]["wins"]))
            winrates.append(str(round((Sum_Info.json()[Solo_Num]["wins"] / (Sum_Info.json()[Solo_Num]["losses"] + Sum_Info.json()[Solo_Num]["wins"]))*100, 2)))
        else:
            tiers.append("None")
            ranks.append("None")
            Games.append("None")
            Wins.append("None")
            winrates.append("None")

    
    return render_template("Ingame.html", champions=champions , names=names, champion_infos=champion_infos, winrates = winrates, LogedIn=LogedIn, Url_LogedIn=Url_LogedIn, form=form, Champ_Logos=Champ_Logos, Wins=Wins, Games=Games, MasteryLvl=MasteryLvl, bans=bans, GameType=GameType, runes=runes, runeNames=runeNames)

@app.route("/aftergame", methods=["POST", "GET"])
def aftergame():
    if current_user.is_authenticated:
        LogedIn = "logout"
        Url_LogedIn = url_for('logout')
    else:
        LogedIn = "login"
        Url_LogedIn = url_for('login')
        
    champions = request.args.getlist("champions")
    conn = sqlite3.connect("champions.db")
    cursor = conn.cursor()
    form = Championswitch()
    
    champion_data = []
    for Num in range(10):
        replacer = champions[Num]
        replacer = replacer.replace("&", "")
        replacer = replacer.replace(" ", "")
        replacer = replacer.replace("'", "")
        replacer = replacer.replace(",", "")
        champion_data.append(replacer)
    if form.validate_on_submit():
        for Num in range(10):
            cursor.execute(f"select * from champions where Userid = {current_user.id} and championname =" + f"'{champion_data[Num]}';")
            result = cursor.fetchall()
            if bool(result) == True:
                Safe = 'Champions.query.filter_by(Userid=current_user.id, championname="' + f'{champion_data[Num]}' + '").update({Champions.notes : form.' + f'Placeholder{Num}' + '.data})'
                eval(Safe)
            else:
                # new_note = Champions(Userid = current_user.id, championname = champion_data[Num], notes = "")
                exec('new_note = Champions(Userid = current_user.id, championname = champion_data[Num], notes = form.' + f'Placeholder{Num}'+ '.data)')       
                eval('db.session.add(new_note)')
            db.session.commit()


    for Num in range(10):
        cursor.execute(f"select * from champions where Userid = {current_user.id} and championname =" + f"'{champion_data[Num]}';")
        result = cursor.fetchall()
        if bool(result) == True:
            exec(f"form.Placeholder{Num}.data = result[0][3]")

    return render_template("aftergame.html", LogedIn=LogedIn, Url_LogedIn=Url_LogedIn, form=form, champions=champions)
    

if __name__ == '__main__':
    app.run(debug=True)
