from flask import Flask, render_template, request

app = Flask(__name__)

def get_all_contacts():
    contacts = []
    try:
        with open('contacts.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    if len(parts) == 2:
                        contacts.append({'name': parts[0], 'phone': parts[1]})
    except FileNotFoundError:
        pass
    return contacts

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form['name']
    phone = request.form['phone']
    
    with open('contacts.txt', 'a', encoding='utf-8') as f:
        f.write(f"{name},{phone}\n")
    
    return render_template('index.html', message="✅ ذخیره شد")

@app.route('/list')
def show_list():
    search_query = request.args.get('q', '')
    all_contacts = get_all_contacts()
    
    if search_query:
        filtered_contacts = []
        for c in all_contacts:
            if search_query in c['name'] or search_query in c['phone']:
                filtered_contacts.append(c)
        contacts = filtered_contacts
    else:
        contacts = all_contacts
    
    return render_template('list.html', contacts=contacts, query=search_query)

@app.route('/delete')
def delete_contact():
    phone = request.args.get('phone')
    if not phone:
        return "شماره تلفن ارسال نشده است", 400
    
    try:
        with open('contacts.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        return "هیچ مخاطبی وجود ندارد", 404
    
    with open('contacts.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            if phone not in line:
                f.write(line)
    
    contacts = get_all_contacts()
    return render_template('list.html', contacts=contacts, query='')

app.run(host='0.0.0.0', port=5000)
