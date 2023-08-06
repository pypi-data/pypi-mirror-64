from pydantic import BaseModel as BasicInput


class BasicFeedbackInput(BasicInput):
    """
    Basic input validator for feedbacks
    """

    request_id: str
    status: bool
    expected_result: str = None
