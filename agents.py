from inference.rules import evaluate_cart_rules


class MonitoringAgent:
    def analyze_input(self, carrito_id, producto_detectado, producto_registrado, pago_completado, zona, bateria):
        return {
            "carrito_id": carrito_id,
            "producto_detectado": producto_detectado,
            "producto_registrado": producto_registrado,
            "pago_completado": pago_completado,
            "zona": zona,
            "bateria": bateria
        }


class SecurityInferenceAgent:
    def evaluate_event(self, cart_data):
        return evaluate_cart_rules(
            producto_detectado=cart_data["producto_detectado"],
            producto_registrado=cart_data["producto_registrado"],
            pago_completado=cart_data["pago_completado"],
            zona=cart_data["zona"],
            bateria=cart_data["bateria"]
        )


class SupervisorAgent:
    def generate_report(self, cart_data, inference_result):
        reglas = inference_result["reglas_activadas"]
        decisiones = inference_result["decisiones"]
        explicaciones = inference_result["explicaciones"]

        report = f"""
Smart-Guard Expert analizó el evento del carrito {cart_data["carrito_id"]}.

Producto detectado:
{cart_data["producto_detectado"] if cart_data["producto_detectado"] else "Ninguno"}

Estado del producto:
{"Registrado en la compra" if cart_data["producto_registrado"] else "No registrado en la compra"}

Estado del pago:
{"Pago completado" if cart_data["pago_completado"] else "Pago pendiente"}

Zona actual:
{cart_data["zona"]}

Nivel de batería:
{cart_data["bateria"]}%

Reglas activadas:
{chr(10).join("- " + regla for regla in reglas)}

Decisiones tomadas:
{chr(10).join("- " + decision for decision in decisiones)}

Explicación del razonamiento:
{chr(10).join("- " + explicacion for explicacion in explicaciones)}
"""

        return report.strip()