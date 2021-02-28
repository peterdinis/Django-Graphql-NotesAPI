import graphene
from graphene_django import DjangoObjectType
from .models import Note
from graphene import Argument

##  New Class


class NoteType(DjangoObjectType):
    class Meta:
        model = Note
        fields = ("name", "description", "completed")


class Query(graphene.ObjectType):
    all_notes = graphene.List(NoteType)
    note = graphene.Field(
        NoteType, id=graphene.ID()
    )  ###navrátenie jednej poznámky podľa id

    def resolve_all_notes(root, info):
        return Note.objects.all()  ## navrátime si všetky hodnoty z db

    def resolve_one_note(self, info, id):
        return Note.objects.get(pk=id)  ### tuto si dokážeme navrátiť jednej note


# create Note Field
class CreateNote(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()
        completed = graphene.Boolean()

    ## return type
    note = graphene.Field(NoteType)

    ## create mutation function
    def mutate(self, info, name, description, completed=False):
        note = Note.objects.create(name=name, description=description, completed=completed)
        note.save()
        return CreateNote(note=note)


### Update
class UpdateNote(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
        completed = graphene.Boolean()

    note = graphene.Field(NoteType)

    def mutate(self, info, id, name=None, description=None, completed=None):
        note = Note.objects.get(pk=id)
        note.name = name if name is not None else note.name
        note.description = description if description is not None else note.description
        completed = completed if completed is not None else note.completed

        note.save()
        return UpdateNote(note=note)


class DeleteNote(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    note = graphene.Field(NoteType)

    def mutate(self, info, id):
        note = Note.objects.get(pk=id)
        if note is not None:
            note.delete()

        return DeleteNote(note=note)


class Mutation(graphene.ObjectType):
    add_note = CreateNote.Field()
    delete_note = DeleteNote.Field()
    update_note = UpdateNote.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
