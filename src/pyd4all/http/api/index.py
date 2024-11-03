from datetime import date

from fastapi.responses import HTMLResponse
from fastui import FastUI, AnyComponent, prebuilt_html, components as c
from fastui.components.display import DisplayMode, DisplayLookup
from fastui.events import GoToEvent, BackEvent
from pydantic import BaseModel, Field

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Define the router for this endpoint
router = APIRouter()


# Define a Pydantic model for the user input
class UserCreateRequest(BaseModel):
    name: str
    email: str


# Example of in-memory storage for simplicity (use a database in real applications)
fake_user_db = []


class User(BaseModel):
    id: int
    name: str
    dob: date = Field(title='Date of Birth')


# define some users
users = [
    User(id=1, name='John', dob=date(1990, 1, 1)),
    User(id=2, name='Jack', dob=date(1991, 1, 1)),
    User(id=3, name='Jill', dob=date(1992, 1, 1)),
    User(id=4, name='Jane', dob=date(1993, 1, 1)),
]


@router.get("", response_model=FastUI, response_model_exclude_none=True)
def users_table() -> list[AnyComponent]:
    """
    Show a table of four users, `/api` is the endpoint the frontend will connect to
    when a user visits `/` to fetch components to render.
    """
    return [
        c.Page(  # Page provides a basic container for components
            components=[
                c.Heading(text='Users', level=2),  # renders `<h2>Users</h2>`
                c.Table(
                    data=users,
                    # define two columns for the table
                    columns=[
                        # the first is the users, name rendered as a link to their profile
                        DisplayLookup(field='name', on_click=GoToEvent(url='/user/{id}/')),
                        # the second is the date of birth, rendered as a date
                        DisplayLookup(field='dob', mode=DisplayMode.date),
                    ],
                ),
            ]
        ),
    ]