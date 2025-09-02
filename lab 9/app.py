from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Настройка базы данных (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель для заметок
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    important = db.Column(db.Boolean, default=False)

# Создание таблиц базы данных
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Получаем данные из формы
        note_text = request.form['note_text']
        is_important = 'note_important' in request.form
        
        # Создаем новую заметку
        new_note = Note(text=note_text, important=is_important)
        
        # Добавляем в базу данных
        db.session.add(new_note)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    # Получаем все заметки из базы
    notes = Note.query.all()
    return render_template('index.html', notes=notes)

@app.route('/delete/<int:id>')
def delete_note(id):
    # Находим заметку по ID и удаляем
    note_to_delete = Note.query.get_or_404(id)
    db.session.delete(note_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)