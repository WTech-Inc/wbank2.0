from main import app  
from extensions import db  
from sqlalchemy import text  
with app.app_context():  
    r=db.session.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'cashout'")).fetchall()  
    for c in r:  
        print(c[0]+': '+c[1])  
