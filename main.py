from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4, UUID

app = FastAPI()
db_notes = {}
class Notes(BaseModel):
    title : str
    description : str
    id: UUID | None = None

@app.get("/", summary="list of all notes", description="retuns all notes from database")
def notes():
    return list(db_notes.values())

@app.get("/notes/{note_id}", summary="get a single note", description="returns specific note from the database")
def get_notes(note_id : UUID):
    if note_id not in db_notes:
        raise HTTPException(status_code=404, detail="Notes Not Found")
    return db_notes[note_id]


@app.post("/notes/", summary="Add new note", description="create a new note with title and description")
def add_notes(note: Notes):
    if note.id in db_notes:
        raise HTTPException(status_code=400, detail="Note already exist")
    note_id = uuid4()
    note.id = note_id
    db_notes[note_id] = note
    return {"Message": "Note Added Successfully", "note_id": note_id}

@app.put("/notes/{note_id}", summary="Update the note", description="update the existing note")
def update_notes(note_id : UUID, note: Notes):
    if note_id not in db_notes:
        raise HTTPException(status_code=404, detail="Note Not Found.")
    note.id = note_id
    db_notes[note_id] = note
    return {"Message" : "Note Updated Successfully"}

@app.delete("/notes/{note_id}", summary="Delete the Note", description="Delete the specific note from the database")
def delete_notes(note_id: UUID):
    if note_id not in db_notes:
        raise HTTPException(status_code=404, detail="Notes not Found")
    del db_notes[note_id]
    return {"Message" : "Note Deleted Successfully."}
