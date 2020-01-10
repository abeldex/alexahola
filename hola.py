"""A custom skill needs to respond to events sent by the Alexa service. For instance, when you ask your Alexa device (e.g. Echo, Echo Dot, Echo Show, etc.) to "open hello world," your skill needs to respond to the LaunchRequest that is sent to your Hello World skill. With the ASK SDK for Python, you simply need to write a request handler, which is code to handle incoming requests and return a response. Your code is responsible for making sure that the right request handler is used to process incoming requests and for providing a response. The ASK SDK for Python provides two ways to create request handlers:

1.- Implement the AbstractRequestHandler class under ask_sdk_core.dispatch_components package. The class should contain implementations for can_handle and handle methods. This is described under Implementation using handler classes section.
2.- Use the request_handler decorator in instantiated skill builder object to tag functions that act as handlers for different incoming requests. This is described under Implementation using decorators section."""

"""To use handler classes, each request handler is written as a class that implements two methods of the AbstractRequestHandler class; can_handle and handle.

The can_handle method returns a Boolean value indicating if the request handler can create an appropriate response for the request. The can_handle method has access to the request type and additional attributes that the skill may have set in previous requests or even saved from a previous interaction. The Hello World skill only needs to reference the request information to decide if each handler can respond to an incoming request."""

"""Start by creating a skill builder object. The skill builder object helps in adding components responsible for handling input requests and generating custom responses for your skill.
----------------------------------------------------------"""
from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()

"""LaunchRequest handler
The following code example shows how to configure a handler to be invoked when the skill receives a LaunchRequest. The LaunchRequest event occurs when the skill is invoked without a specific intent.
----------------------------------------------------------"""

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hola, Bienvenido al Kit de Skills de la Alexa, ahora puedes decir Hola Mundo!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hola Mundo", speech_text)).set_should_end_session(
            False)
        return handler_input.response_builder.response
"""The can_handle function returns True if the incoming request is a LaunchRequest. The handle function generates and returns a basic greeting response.
----------------------------------------------------------"""
"""HelloWorldIntent handler
The following code example shows how to configure a handler to be invoked when the skill receives an intent request with the name HelloWorldIntent. Type or paste the following code into your hello_world.py file, after the previous handler.
----------------------------------------------------------"""
class HolaMundoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("HolaMundoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "El mundo es un lugar maravilloso, lástima que los humanos no lo cuidan como debería ser"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hola Mundo", speech_text)).set_should_end_session(
            True)
        return handler_input.response_builder.response
"""The can_handle function detects if the incoming request is an IntentRequest, and returns True if the intent name is HelloWorldIntent. The handle function generates and returns a basic "Hello World" response.
-----------------------------------------------------------"""

"""HelpIntent handler
The following code example shows how to configure a handler to be invoked when the skill receives the built-in intent AMAZON.HelpIntent. Type or paste the following code into your hello_world.py file, after the previous handler.
-----------------------------------------------------------"""
class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Puedes decirme Hola Mundo y te responderé que pienso!"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hola Mundo", speech_text))
        return handler_input.response_builder.response
"""Similar to the previous handler, this handler matches an IntentRequest with the expected intent name. Basic help instructions are returned, and .ask(speech_text) causes the user's microphone to open up for the user to respond.
----------------------------------------------------------"""

"""CancelAndStopIntent handler
The CancelAndStopIntentHandler is similar to the HelpIntent handler, as it is also triggered by the built-In AMAZON.CancelIntent or AMAZON.StopIntent Intents. The following example uses a single handler to respond to both intents. Type or paste the following code into your hello_world.py file, after the previous handler.
----------------------------------------------------------"""
class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Nos vemos luego, acuerdate de cuidar al mundo para que siga siendo un lugar maravilloso!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hola Mundo", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response
"""The response to both intents is the same, so having a single handler reduces repetitive code.
----------------------------------------------------------"""

"""Implementing exception handlers
The following sample adds a catch all exception handler to your skill, to ensure the skill returns a meaningful message for all exceptions.
----------------------------------------------------------"""
from ask_sdk_core.dispatch_components import AbstractExceptionHandler

class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Ah caray, no lo he entendido. Puedes repetirmelo una vez más!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HolaMundoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()