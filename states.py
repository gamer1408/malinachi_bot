from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    waiting_name     = State()
    waiting_region   = State()
    waiting_quantity = State()
    waiting_phone    = State()
