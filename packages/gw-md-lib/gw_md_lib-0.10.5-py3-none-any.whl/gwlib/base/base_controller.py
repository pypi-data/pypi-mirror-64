import sqlalchemy
from sqlalchemy.exc import IntegrityError

from gwlib.base.base_service import BaseService
from gwlib.base.errors import UserNotAllowed
from gwlib.http.responses import HTTP_BAD_REQUEST, HTTP_CONFLICT


class BaseController:

    def build_response(self, method=None, **kwargs):
        """
        Method to call a Service function and return a Http Response
        :type kwargs: dict
        :type method: function
        """
        try:
            response = method(**kwargs)
        # authentication section
        except UserNotAllowed as e:
            print("error", e)
        except KeyError as e:
            return HTTP_BAD_REQUEST(e)
        except IntegrityError as e:
            return HTTP_CONFLICT(e)
        except sqlalchemy.exc.InvalidRequestError as e:
            return HTTP_CONFLICT(e)
        return response

