from app.schemas.customer_schema import CustomerCreate, CustomerUpdate, CustomerResponse
from app.schemas.vehicle_schema import VehicleCreate, VehicleUpdate, VehicleResponse
from app.schemas.mechanic_schema import MechanicCreate, MechanicUpdate, MechanicResponse
from app.schemas.service_schema import ServiceCatalogCreate, ServiceCatalogUpdate, ServiceCatalogResponse
from app.schemas.service_booking_schema import ServiceBookingCreate, ServiceBookingCreateWithCustomer, ServiceBookingUpdate, ServiceBookingResponse
from app.schemas.conversation_schema import ConversationResponse
from app.schemas.message_schema import MessageResponse
from app.schemas.chatbot_schema import ChatRequest, ChatResponse, ConversationHistoryResponse

__all__ = [
    "CustomerCreate", "CustomerUpdate", "CustomerResponse",
    "VehicleCreate", "VehicleUpdate", "VehicleResponse",
    "MechanicCreate", "MechanicUpdate", "MechanicResponse",
    "ServiceCatalogCreate", "ServiceCatalogUpdate", "ServiceCatalogResponse",
    "ServiceBookingCreate", "ServiceBookingCreateWithCustomer", "ServiceBookingUpdate", "ServiceBookingResponse",
    "ConversationResponse", "MessageResponse",
    "ChatRequest", "ChatResponse", "ConversationHistoryResponse"
]
