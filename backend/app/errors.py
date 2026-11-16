"""Exceções de domínio e tratadores HTTP."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError


class DomainError(Exception):
    status_code = 400
    code = "DOMAIN_ERROR"

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class NotFoundError(DomainError):
    status_code = 404
    code = "NOT_FOUND"


class ConflictError(DomainError):
    status_code = 409
    code = "CONFLICT"


class ScheduleConflictError(ConflictError):
    code = "SCHEDULE_CONFLICT"


class BusinessRuleError(DomainError):
    status_code = 422
    code = "BUSINESS_RULE"


def _body(code: str, message: str, details=None):
    return {"code": code, "message": message, "details": details or {}}


def register_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_handler(_req: Request, exc: DomainError):
        return JSONResponse(status_code=exc.status_code, content=_body(exc.code, exc.message, exc.details))

    @app.exception_handler(RequestValidationError)
    async def validation_handler(_req: Request, exc: RequestValidationError):
        fields = {}
        for err in exc.errors():
            loc = ".".join(str(p) for p in err["loc"] if p != "body")
            msg = err["msg"].removeprefix("Value error, ")
            fields[loc or "body"] = msg
        return JSONResponse(
            status_code=422,
            content=_body("VALIDATION_ERROR", "Dados inválidos. Corrija os campos indicados.", {"fields": fields}),
        )

    @app.exception_handler(SQLAlchemyError)
    async def db_handler(_req: Request, _exc: SQLAlchemyError):
        return JSONResponse(status_code=500, content=_body("DATABASE_ERROR", "Erro ao acessar o banco de dados."))
