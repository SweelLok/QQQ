from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_all_pizzas():
    try:
        sqlite_connection = sqlite3.connect("sql_pizza.db")
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM db_pizza")
        pizzas = cursor.fetchall()
        return pizzas

    except sqlite3.Error as error:
        print("Помилка при отримані кода:", error)
        return []

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Піца отримана")

@app.get("/")
def login_page():
    return render_template("login.html")

@app.post("/login/")
def login():
    username = request.form.get("username")
    if username == "admin":
        return redirect(url_for("admin_page"))
    return redirect(url_for("home_page"))
    
@app.get("/admin")
def admin_page():
    pizzas = get_all_pizzas()
    context = {
        "back_button": "Повернутися на головну сторінку",
        "pizzas": pizzas
    }
    return render_template("admin.html", **context)

@app.get("/home")
def home_page():
    return render_template("index.html",
                            menu="Меню",
                            title="Oderman",
                            number="Номер телефону: +1 234 567 890")

@app.get("/menu/")
def menu_page():
    pizzas = get_all_pizzas()
    context = {
        "back_button": "Повернутися на головну сторінку",
        "pizzas": pizzas
    }
    return render_template("menu.html", **context)

@app.get("/add_pizza/")
def add_pizza():
    if request.method == "POST":
        name = request.form.get("name")
        ingrediens = request.form.get("ingrediens")
        price = request.form.get("price")

        try:
            sqlite_connection = sqlite3.connect("sql_pizza.db")
            cursor = sqlite_connection.cursor()
            insert_query = """INSERT INTO db_pizza 
            (name, ingrediens, price) 
            VALUES (?, ?, ?);"""
            cursor.execute(insert_query, (name, ingrediens, int(price)))
            sqlite_connection.commit()
            print("Нова піца успішно додана")

        except sqlite3.IntegrityError:
            print("Помилка: піца з такою назвою або інгредієнтами вже існує.")
        except sqlite3.Error as error:
            print("Помилка при роботі з SQLite:", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    return render_template("add_pizza.html")

@app.post("/add_pizza/")
def add_pizza():
    if request.method == "POST":
        name = request.form.get("name")
        ingrediens = request.form.get("ingrediens")
        price = request.form.get("price")

        try:
            sqlite_connection = sqlite3.connect("sql_pizza.db")
            cursor = sqlite_connection.cursor()
            insert_query = """INSERT INTO db_pizza 
            (name, ingrediens, price) 
            VALUES (?, ?, ?);"""
            cursor.execute(insert_query, (name, ingrediens, int(price)))
            sqlite_connection.commit()
            print("Нова піца успішно додана")

        except sqlite3.IntegrityError:
            print("Помилка: піца з такою назвою або інгредієнтами вже існує.")
        except sqlite3.Error as error:
            print("Помилка при роботі з SQLite:", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()

    return render_template("add_pizza.html")

if __name__ == "__main__":
    app.run(port=5050, debug=True)
