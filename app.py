from flask import Flask, render_template, request, redirect, url_for
import csv
from datetime import datetime

app = Flask(__name__)

@app.get("/")
def index():
    books = []
    with open('books.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            books.append(row)

    return render_template("index.html", books=books)

@app.get("/book/<int:book_id>")
def show_details(book_id):
    found_book = None

    with open('books.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for book in reader:
            if int(book['id']) == book_id:
                found_book = book
                break
        
    if found_book:
        return render_template("details.html", book=found_book)
    else:
        return "Book not found! / Livro não encontrado!", 404

@app.get("/add-book")
def show_add_form():
    return render_template("add-book.html")

@app.post("/add-book")
def add_book():
    
    # 1. Descobrir o próximo id
    with open('books.csv', mode='r', encoding='utf-8') as file:
        reader = list(csv.reader(file))
        last_id = 0

        if len(reader) > 1:
            last_row = reader[-1]
            if last_row:
                last_id = int(last_row[0])
        
        next_id = last_id + 1

    # 2. Converte a data para o formato desejado

    conclusion_date_raw = request.form.get("conclusion_date")
    date_object = datetime.strptime(conclusion_date_raw, "%Y-%m-%d")

    formatted_date = date_object.strftime("%m/%d/%Y")

    # 3. Coleta os dados
    new_book = [
        next_id,
        request.form.get("title"),
        request.form.get("author"),
        request.form.get("poster"),
        request.form.get("rating"),
        formatted_date,
        request.form.get("review")
    ]

    with open('books.csv', mode='a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(new_book)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)