from django.shortcuts import render, HttpResponse, redirect
from pyrebase import*
import firebase_admin
from firebase_admin import credentials, auth, storage, db

config = {
  "apiKey": "AIzaSyABZy-3mRT_t6IlqJU6b0bE6ui4A6Mee9E",
  "authDomain": "documents-b43fb.firebaseapp.com",
  "databaseURL": "https://documents-b43fb-default-rtdb.firebaseio.com",
  "projectId": "documents-b43fb",
  "storageBucket": "documents-b43fb.appspot.com",
  "messagingSenderId": "863812795401",
  "appId": "1:863812795401:web:2c8e58f2b1cc1c23ea8cd8",
  "serviceAccount":"ecodoc/key.json"
};

firebase = pyrebase.initialize_app(config)
service_account_key_path = "ecodoc/key.json"
cred = credentials.Certificate(service_account_key_path)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {'storageBucket': 'documents-b43fb.appspot.com'})
else:
    default_app = firebase_admin.get_app()

storage_client = storage.bucket(app=default_app)
db=firebase.database()
Auth = firebase.auth()

def register(request):
    email = ""
    password = ""
    alert_message = ""
    display_name=""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_properties = {
            "email": email,
            "password": password,
            "display_name": email
        }
        try:
            user = auth.create_user(**user_properties)
            alert_message="Registration successful"
        except Exception as e:
            alert_message = "Registration Unsuccessful: " + str(e)       
    return render(request, 'reg.html',{'alert_message':alert_message})

def login_view(request):
    email=""
    password=""
    user=""
    invalid=""
    global userid
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')
        userid = email
        try:
            user = Auth.sign_in_with_email_and_password(email, password)
            white_board_link1="https://miro.com/app/board/uXjVNlJwQD4=/"
            return render(request,'profile.html',{"white_board_link1":white_board_link1})     
        except Exception as e:
            invalid =e
    return render(request, 'login.html',{'alert_message':invalid})

def profile(request):
    return render(request,'profile.html')


def collab(request):
    white_board_link="https://app.mural.co/t/ecodoc9200/m/ecodoc9200/1709483836580/acc6b70858e95eb2c80756b7e369c91a32cf7934?sender=u50a55feed624d224102a3292"
    return render(request, 'collab.html',{"white_board_link":white_board_link})

def sch(request):
    return render(request, 'sch.html')

def home(request):
    return render(request, 'home.html')

def todo(request):
    return render(request, 'todo.html')

def kanban_board(request):
    return render(request, 'kanban.html')


def add_employee(request):
    selected_projects=[]
    if request.method == "POST":
        id=request.POST.get('ID')
        name=request.POST.get('name')
        email = request.POST.get('email')
        designation=request.POST.get('designation')
        selected_projects = request.POST.getlist('projects[]')
        selected_projects = [project for project in selected_projects if project]
        data=db.child("Employee").get()
        if (data.pyres is not None) and (str(id) in data.val()):
            return HttpResponse("ID already exists")
        else:
            info={"Id":id,"Name":name,'email': email, 'designation': designation, 'projects':selected_projects}
            db.child("Employee").child(id).set(info)
            return HttpResponse("ID added")
    else:
        return render(request,'addemp.html')
    
def view_employee(request):
    userid = "manshruti2589@gmail.com" 
    data = db.child("Employee").order_by_child("email").equal_to(userid).get()

    if data.pyres is not None and data.val():
        employee_data = list(data.val().values())[0]
        return render(request, 'user_profile.html', {'employee_data': employee_data})
    else:
        return HttpResponse("Employee not found")
    
def add_achievements(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        userid="manshruti2589@gmail.com"
        employee_data = db.child("Employee").order_by_child("email").equal_to(userid).get()
        
        if employee_data.each():
            employee_id = list(employee_data.val().keys())[0]
            existing_achievements = employee_data.val()[employee_id].get("achievements", {})
        else:
            return HttpResponse("Employee not found")
        
        existing_achievements[name] = {
            "name": name,
            "description": description
        }
 
        db.child("Employee").child(employee_id).child("achievements").update(existing_achievements)
        mes="Successfully added"
        return render(request, 'add_achievements.html',{'alert_message':mes})       
    else:
        return render(request, 'add_achievements.html')
    
def add_workhistory(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        userid="manshruti2589@gmail.com"
        employee_data = db.child("Employee").order_by_child("email").equal_to(userid).get()
        
        if employee_data.each():
            employee_id = list(employee_data.val().keys())[0]
            existing_history = employee_data.val()[employee_id].get("work_history", {})
        else:
            return HttpResponse("Employee not found")

        existing_history[name] = {
            "name": name,
            "description": description
        }
        
        db.child("Employee").child(employee_id).child("work_history").update(existing_history)
        mes="Successfully added"
        return render(request, 'add_workhistory.html',{'alert_message':mes})       
    else:
        return render(request, 'add_workhistory.html')
    
def add_skills(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        userid="manshruti2589@gmail.com"
        employee_data = db.child("Employee").order_by_child("email").equal_to(userid).get()
        
        if employee_data.each():
            employee_id = list(employee_data.val().keys())[0]
            existing_skills = employee_data.val()[employee_id].get("skills", {})
        else:
            return HttpResponse("Employee not found")
        
        existing_skills[name] = {
            "name": name,
            "description": description
        }
        
        db.child("Employee").child(employee_id).child("skills").update(existing_skills)
        mes="Successfully added"
        return render(request, 'add_skills.html',{'alert_message':mes})       
    else:
        return render(request, 'add_skills.html')
    
def project_login(request):
    invalid=""
    if request.method == 'POST':
        name = "ecodoc"
        password = request.POST.get('password')
        data = db.child("Projects").child(name).get()
            
        if data.each():
            project_data = data.each()[0].val()
            if data.val().get("password") == password:
                    google_drive_link=data.val().get("doclink")
                    whiteboard="https://app.mural.co/t/ecodoc9200/m/ecodoc9200/1709483836580/acc6b70858e95eb2c80756b7e369c91a32cf7934?sender=u50a55feed624d224102a3292"
                    return render(request, 'project.html',    {'google_drive_link': google_drive_link,
                                                               "whiteboard":whiteboard})
            else:
                invalid = "Invalid password"
        else:
            invalid = "Project not found"
    return render(request, 'pro_login.html',{'alert_message':invalid})

def employee_dir(request):
    project_name = "ecodoc"
    data = db.child("Employee").get()

    employees = []
    if data.each():
        for employee in data.each():
            employee_data = employee.val()
            projects = employee_data.get("projects", [])
            if project_name in projects:
                employees.append(employee_data)
        if employees:
            return render(request, 'empdir.html', {'employees': employees})
        else:
            return HttpResponse("No employees associated with project: {}".format(project_name))
    else:
        return HttpResponse("No employees found")

def note_list(request):
    notes = db.child("notes").get().val()
    unique_notes = {}
    for note_id, note in notes.items():
        if note['title'] not in unique_notes:
            unique_notes[note['title']] = note
    return render(request, 'note_list.html', {'notes': unique_notes})

def note_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        new_note = {'title': title, 'content': content}
        db.child("notes").child(title).set(new_note)
        return redirect('note_list')
    return render(request, 'note_list.html')

def note_delete(request,title):
    notes = db.child("notes").get().val()
    if title in notes.items():
        notes=db.child("notes").remove(title)
    return render(request, 'note_list.html', {'notes': notes})





















    


    




            
