# controllers/event_controller.py
from models.event import Event
from storage import events, users
create_messages = {
    "event_name": "Digite o nome do evento: ",
    "event_date": "Digite a data do evento (ex: 2025-02-01): ",
    "event_location": "Digite o local do evento: ",
    "event_description": "Digite a descrição do evento: "
}
def create_event(user):
    event_name = create_name()
    event_date = input("Digite a data do evento (ex: 2025-02-01): ")
    event_location = input("Digite o local do evento: ")
    event_description = input("Digite a descrição do evento: ")
    event = Event(event_name, event_date, event_location, event_description)
    events.append(event)
    event.addParticipant(user)  # Adiciona o criador como participante
    print("Evento criado com sucesso!")
    return event

def list_events():
    if not events:
        print("Nenhum evento disponível.")
        return
    for event in events:
        print(f"ID: {event.getId()} - {event.getEventName()} (Data: {event.getEventDate()})")

def invite_to_event(user):
    if not events:
        print("Nenhum evento disponível para convidar pessoas.")
        return
    list_events()
    try:
        event_id = int(input("Digite o ID do evento para convidar pessoas: "))
    except ValueError:
        print("ID inválido.")
        return
    event = next((e for e in events if e.getId() == event_id), None)
    if not event:
        print("Evento não encontrado.")
        return
    available_users = [u for u in users if u not in event.getParticipants()]
    if not available_users:
        print("Nenhum usuário disponível para convidar.")
        return
    for u in available_users:
        print(f"{u.getId()} - {u.getName()}")
    invite_ids = input("Digite os IDs dos usuários para convidar (separados por vírgula): ")
    invite_ids_list = invite_ids.split(',')
    for id_str in invite_ids_list:
        try:
            uid = int(id_str.strip())
        except ValueError:
            continue
        invited_user = next((u for u in available_users if u.getId() == uid), None)
        if invited_user:
            event.addParticipant(invited_user)
            invited_user.addNotification({
                "user": user,
                "message": f"{user.getName()} te convidou para o evento '{event.getEventName()}'.",
                "is_event_invite": True,
                "event_id": event.getId()
            })
            print(f"Usuário {invited_user.getName()} convidado para o evento.")
            
def show_event_details():
    if not events:
        print("Nenhum evento disponível.")
        return
    try:
        event_id = int(input("Digite o ID do evento para ver detalhes: "))
    except ValueError:
        print("ID inválido.")
        return
    event = next((e for e in events if e.getId() == event_id), None)
    if not event:
        print("Evento não encontrado.")
        return
    print(event)
    if event.getParticipants():
        print("Participantes:")
        for participant in event.getParticipants():
            print(f"- {participant.getName()}")
    else:
        print("Nenhum participante inscrito no evento.")