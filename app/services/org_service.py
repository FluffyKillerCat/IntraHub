from sqlalchemy.orm import Session
from app.models.organizations import Organizations
from app.models.user import User
from app.models.admins import Admins
from app.models.user import User
def create_org(db: Session, admin, name):

    new_org = Organizations(

        created_id= admin.id,
        org_name= name.name
    )

    db.add(new_org)
    db.commit()
    db.refresh(new_org)

def add_user_to_org(db: Session, user_org_data, admin):

    is_org_admin = db.query(Admins).filter(Admins.org_id == user_org_data.org, Admins.user_id == admin).first()
    if is_org_admin:
        user  = user_org_data.user
        org = user_org_data.org

        user = db.query(User).filter(User.id == user).first()
        user.organization_id = org
        db.commit()
        db.refresh(user)
        return user

    else:
        return None
