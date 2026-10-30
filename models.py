from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    mobile_number: Mapped[str | None] = mapped_column(String(11), unique=True)
    role: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="resident",
        server_default="resident",
    )

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint(
            "mobile_number IS NULL OR mobile_number ~ '^09[0-9]{9}$'",
            name="ck_users_mobile_number",
        ),
        CheckConstraint(
            "role = 'staff' OR mobile_number IS NOT NULL",
            name="ck_users_resident_mobile_number",
        ),
        CheckConstraint(
            "role IN ('resident', 'staff')",
            name="ck_users_role",
        ),
    )


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey("services.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="waiting",
        server_default="waiting",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    called_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    served_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    no_show_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    left_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'left')",
            name="ck_tickets_status",
        ),
    )