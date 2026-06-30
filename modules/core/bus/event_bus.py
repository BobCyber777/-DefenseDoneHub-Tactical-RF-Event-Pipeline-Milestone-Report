class EventBus:

    def __init__(self):
        self.events=[]


    def publish(self,event):

        self.events.append(event)

        print(
            f"[{event.severity}] {event.event_type}"
        )


    def get_events(self):

        return self.events
