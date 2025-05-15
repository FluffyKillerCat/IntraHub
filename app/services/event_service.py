from app.models.event import Event
from sqlalchemy.orm import Session
from app.models.organizations import Organizations
from app.models.event_attendee import EventAttendee
from app.services.token_service import get_current_token

from app.utilities.jwt import decode_access_token
def create_event(db: Session, creator_id, event_data, token):

    payload = decode_access_token(token)


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

            )



            db.add(new_event)
            db.commit()
            db.refresh(new_event)
            return new_event
        else:
            raise ValueError("Only Admins can make events")
    except Exception:
        raise ValueError("Only Admins can make events")





def get_all_events(db: Session, current_user, token):
    payload = decode_access_token(token)
    orgs = list(payload['orgs'].keys())

    # Query events associated with the organizations
    event_ids_subquery = db.query(Event.id).filter(Event.org_id.in_(orgs)).scalar_subquery()

    # Query users registered for those events
    registered_users = db.query(EventAttendee.user_id).filter(EventAttendee.event_id.in_(event_ids_subquery)).all()

    return registered_users


def get_event_by_id(db: Session, event_id: str, current_user, token):
    payload = decode_access_token(token)


    for org in payload['orgs']:
        event = db.query(Event).filter(Event.title == event_id, Event.org_id == org).first()
        if event:
            return event


def delete_event_title(db: Session, event_id: str, current_user, event, token):
    payload = decode_access_token(token)

    db.delete(event)
    db.commit()
    return event

