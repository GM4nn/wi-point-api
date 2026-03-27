# strawberry
from strawberry.extensions import SchemaExtension

# db
from app.core.database import SessionLocal


class SQLAlchemySessionExtension(SchemaExtension):

    def on_operation(self):
        self.execution_context.context["db"] = SessionLocal()
        try:
            yield
        finally:
            self.execution_context.context["db"].close()
