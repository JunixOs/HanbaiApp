class NotificacionService:
    def notificar_bajo_stock(self, producto_nombre, stock_actual):
        # Aquí podrías integrar un servicio de email real como SendGrid o SMTP
        mensaje = f"ALERTA: El producto {producto_nombre} tiene bajo stock ({stock_actual} unidades)."
        print(f"[EMAIL ENVIADO AL ADMIN] {mensaje}") # Simulación
        return True

    def notificar_compra_exitosa(self, email_cliente, id_venta):
        mensaje = f"Hola, tu compra #{id_venta} ha sido procesada exitosamente."
        print(f"[EMAIL ENVIADO A {email_cliente}] {mensaje}")
        return True