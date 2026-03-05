# Import all the models, so that Base has them before being
# imported by Alembic or used by create_all
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.equipment import Equipo, Calibracion  # noqa
from app.models.quotation import Quotation, QuotationItem  # noqa
from app.models.service_order import ServiceOrder  # noqa
from app.models.customer_order import CustomerOrder, CustomerOrderItem  # noqa
