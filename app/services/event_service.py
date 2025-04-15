from app.models.event import Event
from sqlalchemy.orm import Session
from app.models.organizations import Organizations

from app.services.token_service import get_current_token

from app.utilities.jwt import decode_access_token
def create_event(db: Session, creator_id, event_data, token):
    from datetime import datetime
    payload = decode_access_token(token)

    def calculate_status(event_date, end_time):
        now = datetime.utcnow()
        return (now.date() == event_date and now.time() <= end_time) or (now.date() < event_date)
    orgs = db.query(Organizations.org_name).all()

    if not any(org[0] == event_data.org_id for org in orgs):
        raise ValueError("Org not found")

    try:

        if event_data.org_id in payload['orgs'] and payload['orgs'][event_data.org_id] is True:
            new_event = Event(
                creator_id=creator_id.id,
                title=event_data.title,
                description=event_data.description,
                location=event_data.location,
                event_type=event_data.event_type,
                event_date=event_data.event_date,
                start_time=event_data.start_time,
                end_time=event_data.end_time,
                max_attendees=event_data.max_attendees,
                org_id = event_data.org_id,
                invitation_type=event_data.invitation_type,
                status = calculate_status(event_data.event_date, event_data.end_time)
            )



            db.add(new_event)
            db.commit()
            db.refresh(new_event)
            return new_event
        else:
            return None
    except Exception:
        return None





def get_all_events(db: Session, current_user, token):
    payload = decode_access_token(token)
    orgs  = list(payload['orgs'].keys())
    print(orgs)
    return db.query(Event).filter(Event.creator_id == current_user).all()


def get_event_by_id(db: Session, event_id: int, current_user):
    payload = get_current_token()
    if payload['org'] == current_user.organization_id and payload['sub'] == current_user.username:




        return db.query(Event).filter(Event.id == event_id, Event.creator_id == current_user).first()
