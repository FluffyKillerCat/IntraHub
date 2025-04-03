from sqlalchemy.orm import Session
from app.models.organizations import Organizations
from app.models.user_orgs import UserOrgs
from app.models.admins import Admins

def create_org(db: Session, admin: int, name: str):

    new_org = Organizations(

        created_id= admin,
        org_name= name
    )

    db.add(new_org)
    db.commit()
    db.refresh(new_org)

def add_user_to_org(db: Session, user_id: int, org: int, curr_admin: int):

    is_org_admin = db.query(Admins).filter(Admins.org_id == org, Admins.user_id == curr_admin, Admins.status == 'accepted').first()
    if is_org_admin:

        new_user = UserOrgs(

        user_id= user_id,
        accepted_by= curr_admin,
        part_of = org
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    else:
        return None
