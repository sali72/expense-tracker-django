from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from expenses.models import Expense
from users.models import UserProfile
from django.conf import settings

# Global motor client
motor_client = None


async def initialize_beanie():
    """Initialize the MongoDB connection with Beanie ODM"""
    global motor_client

    # Create Motor client
    connection_string = f"mongodb://{settings.DATABASES['default']['HOST']}:{settings.DATABASES['default']['PORT']}"
    motor_client = AsyncIOMotorClient(connection_string)

    # Initialize Beanie with the document models
    await init_beanie(
        database=motor_client[settings.DATABASES["default"]["NAME"]],
        document_models=[Expense, UserProfile],
    )

    return motor_client


def get_motor_client():
    """Get the global Motor client"""
    global motor_client
    if not motor_client:
        # If running in a sync context, create the client but don't initialize Beanie
        connection_string = f"mongodb://{settings.DATABASES['default']['HOST']}:{settings.DATABASES['default']['PORT']}"
        motor_client = AsyncIOMotorClient(connection_string)
    return motor_client


def close_motor_client():
    """Close the global Motor client"""
    global motor_client
    if motor_client:
        motor_client.close()
        motor_client = None
