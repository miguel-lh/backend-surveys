# encoding: utf-8


TYPE_3_SURVEYS = (
    ('DELIVERY_MAN', 'Repartidor'),
    ('CALL_CENTER', 'Call center'),
    ('BOTH', 'Ambos'),
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
    ('IN_PROGRESS', 'En proceso'),
    ('CANCELED', 'Cancelada'),
    ('FINISHED', 'Finalizada'),
)