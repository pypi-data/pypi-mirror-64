import sqlalchemy
from sqlalchemy.exc import IntegrityError

from gwlib.base.base_service import BaseService
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
        except KeyError as e:
            return HTTP_BAD_REQUEST(e)
        except IntegrityError as e:
            return HTTP_CONFLICT(e)
        except sqlalchemy.exc.InvalidRequestError as e:
            return HTTP_CONFLICT(e)
        return response




controller = BaseController()
user_service = BaseService()


# mi ruta
def save_user(**kwargs):
    return controller.build_response(method=user_service.save, **kwargs)

