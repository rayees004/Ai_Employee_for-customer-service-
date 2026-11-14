from .gemini_client import Anthropic
from django.conf import settings

# initialize Gemini
client = Anthropic(api_key=settings.GEMINI_API_KEY)

anthropic_model = settings.GEMINI_MODEL



# SUPPORT SYSTEM PROMPT--> Maya's job description
SUPPORT_SYSTEM_PROMPT = """
You are Maya, a coustomer support agent at CoolBreeze AC.
You help coustormers with issues related to their AC orders.

Your responsibilities:
- Always use your tools to gather facts before responding
- Check order details when customer mentions their order
- Check refund history before making any refund decisions
- Be empatheti but honest

Your personality:
- friendly and professional
- Patient even when customer is angry 
- Clear and consise in your replies

Important rules:
- Always check order details first before responding 
- Never approve or deny a fefund yourself
- If refund decision is needed - tell customer you are checking with your team

"""
# SUPPOT TOOLS --> Tools Schemas, that ai will read

SUPPORT_TOOLS = [
    {"name":"get_order_details",
     "description":"Feth complete order details including status, carrier, tracking nmber and days since oreder was place. use this when customer mentions their order or complains about delivery.",
     "input_schema": {
         "type":"object",
         "properties":{
             "order_id":{
                 "type":"integer",
                 "description": "The order ID to look up"
             }
         },
         "required":["order_id"]
     }
     },
     {
         "name":"get_refund_history",
         "description":"Get complete refund history for a user. use this before making any refund related decisions.",
         "input_schema":{
             "type":"object",
             "properties":{
                 "user_id":{
                     "type":"integer",
                     "description":"The user ID to check refund history for"
                 }
             },
             "required":['user_id']

         }
     },
     {
        "name": "check_delivery_status",
        "description": "Check current delivery status using tracking number and carrier. Use this when customer complains about delayed or missing delivery.",
        "input_schema": {
            "type": "object",
            "properties": {
                "tracking_number": {
                    "type": "string",
                    "description": "The shipment tracking number"
                },
                "carrier": {
                    "type": "string",
                    "description": "The carrier name for example BlueDart or Delhivery"
                }
            },
            "required": ["tracking_number", "carrier"]
        }
    },
]

# Execute_tool() --> bridge between claude and pyhton functions(tools)

# Agent Loop --> while loop that loops until the task is done