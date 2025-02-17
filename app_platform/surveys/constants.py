# encoding: utf-8


TYPE_3_SURVEYS = (
    ('DELIVERY_MAN', 'Repartidor'),
    ('CALL_CENTER', 'Call center'),
    ('BOTH', 'Ambos'),

    # Opciones para cuando el type es por PRODUCT_QUALITY    
    ('WHITE_CREAM', 'Nata Blanca'),
    ('BAD_TASTE', 'Mal Sabor'),
    ('BAD_SMELL', 'Mal Olor'),
    ('GREEN_WATER', 'Agua verde'),
    ('EXPIRED_EXPIRATION_DATE', 'Caducidad Vencida'),
    ('FOREIGN_BODY', 'Cuerpo extraño'),
    ('WARRANTY_SEAL', 'Sello de garantía'),
    ('BROKEN_CARAFE_WATER_LEAK', 'Garrafón roto / Fuga de agua'),
    ('BLUE_BLACK_PARTICLES', 'Partículas azules /negras'),
    ('OTHERS', 'Otros'),

)

TYPE_2_SURVEYS = (
    ('BAD_SERVICE', 'Mal servicio'),
    ('PRODUCT_QUALITY', 'Calidad en el producto'),
    ('OTHER_REASONS', 'Otras Razones'),
    ('GOOD_SERVICE', 'Buen servicio'),
)

TYPE_SURVEYS = (
    ('COMPLAINT', 'Queja'),
    ('SUGGESTION', 'Sugerencia'),
    ('CONGRATULATION', 'Felicitación'),
)

STATUS_SURVEYS = (
    ('PENDING', 'Pendiente'),
    ('IN_PROGRESS', 'En proceso'),
    ('CANCELED', 'Cancelada'),
    ('FINISHED', 'Finalizada'),
)