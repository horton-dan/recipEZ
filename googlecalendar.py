import os.path
from dotenv import load_dotenv
from sqlmodel import Session, create_engine, select
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dbcheck import checkMealTable
from tables import Meal

load_dotenv()



def selectMeal():

    engine = create_engine(os.getenv('postgres_url'), echo=False)
    with Session(engine) as session:
        statement = select(Meal)
        results = session.exec(statement)
        meals = results.all()
        print(meals)
    selection = input("Please select a meal:")
    if checkMealTable(selection):
        with Session(engine) as session:
            name_query = select(Meal.name).where(Meal.name == selection)
            ingredients_query = select(Meal.ingredients).where(Meal.name == selection)
            name = session.exec(name_query).first() 
            ingredients = session.exec(ingredients_query).first()
        return name, ingredients
    
    
       
       

def selectDate():
   print("Please insert dates in format: YYYY-MM-DD")
   day = input("What day do you want to have the Meal? ")
   return day



def authenticate():
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", os.getenv('SCOPES'))
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", os.getenv('SCOPES')
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_json())
  return creds


if __name__ == "__main__":
    authenticate()
    name, ingredients = selectMeal()
    if name:
        day = selectDate()
        creds = authenticate()
        event = {
            'summary': name,
            'description': str(ingredients),
            'start': {
                'date': day
            },
            'end': {
                'date': day
            },
            'reminders': {
                'useDefault': False
            }
        }
        try:
            service = build("calendar", "v3", credentials=creds)
            created_event = service.events().insert(calendarId=os.getenv('meal_calendar_id'), body=event).execute()
            print(f"Event created: {created_event.get('htmlLink')}")
        except HttpError as error:
            print(f"An error occurred: {error}")