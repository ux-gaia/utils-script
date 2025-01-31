import requests
import json

# URL de la API de Strapi
STRAPI_URL_LOCATIONS = 'https://mighty-frogs-714884b697.strapiapp.com/api/long-stays-locations'
STRAPI_URL_ZONES = 'https://mighty-frogs-714884b697.strapiapp.com/api/long-stays-zones'
TOKEN = '314a31883a08474cbccde0846259dab31631d80f49c7029d6aafb14470ef5bacb9924c0a82eb468cfd46c45b1b3b0eba796d860f54175c642c79cdae812d3d1a1d452d5bc2af7ce6b64123d414ca75dc4bd5fac2b7abf6c45097446918367f52f5012494fbdbb0ca19596d1b075234c0cd39f162452d69e1136a6b44886291b2'

# Cargar los datos de los archivos JSON
print('Cargando datos de edificios.json...')
with open('edificios.json') as f:
    edificios = json.load(f)

print('Cargando datos de gaiastays_apartamentos_columns_key_value.json...')
with open('gaiastays_apartamentos_columns_key_value.json') as f:
    apartamentos = json.load(f)

def send_post_request(url, data, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code != 200:
        print(f'Error en la solicitud: {response.status_code} - {response.text}')
        return None
    try:
        return response.json()
    except json.JSONDecodeError:
        print('Error al decodificar la respuesta JSON:')
        print(response.text)
        return None

# Función para subir un edificio a Strapi
def subir_edificio(edificio):
    print(f'Subiendo edificio: {edificio["nombre"]}')
    data = {
        'data': {
            'name': edificio['nombre'],
            'latitude': float(edificio['latitud'].replace(',', '.')),
            'longitude': float(edificio['longitud'].replace(',', '.')),
            'address': edificio['direccion'],
            'description': edificio['descripcion_edificio'],
            'transportInformation': edificio['transporte_publico_cercano'],
            'digitalConcierge': edificio['digital_concierge'],
            'smartLockers': edificio['loockers_inteligentes_para_paqueteria'],
            'communityTerrace': edificio['terraza_comunitaria'],
            'rooftop': edificio['rooftop'],
            'garden': edificio['jardin'],
            'multipurposeRoom': edificio['sala_multiusos'],
            'disabilityAdaptation': edificio['adaptado_para_personas_con_minusvalia'],
            'pool': edificio['piscina'],
            'communitySaloon': edificio['salon_comunitario'],
            'coWorking': edificio['co_working'],
            'gym': edificio['gimnasio']
        }
    }
    response = send_post_request(f'{STRAPI_URL_LOCATIONS}', data, TOKEN)
    if response and 'data' in response and 'id' in response['data']:
        print(f'Edificio subido con éxito: {edificio["nombre"]}, ID: {response["data"]["id"]}')
        return response['data']['id']
    else:
        print(f'Error al subir el edificio: {response}')
        return None

# Función para subir un apartamento a Strapi
def subir_apartamento(apartamento_key, apartamento, edificio_id):
    print(f'Subiendo apartamento: {apartamento_key} asociado al edificio ID: {edificio_id}')
    data = {
        'data': {
            'name': apartamento_key,
            'externalId': apartamento['identificador'],
            'description': apartamento['Descripción'],
            'long_stays_location': edificio_id,
            'euroPerMonth': float(apartamento['PRECIO/mes'].replace('.', '').replace(',', '.')),
            'flexibleCancellation': apartamento['Cancelación flexible'] == 'TRUE',
            'allIncluded': apartamento['Todo incluído'] == 'TRUE',
            'parking': apartamento['Cochera/Parking'] == 'TRUE',
            'storageRoom': apartamento['Alamcen/trastero'] == 'TRUE',
            'petFriendly': apartamento['Pet-friendly'] == 'TRUE',
            'exterior': apartamento['Exterior'] == 'TRUE',
            'tv': apartamento['TV'] == 'TRUE',
            'closetNumber': int(apartamento['nº armarios']) if apartamento['nº armarios'] else None,
            'tablesNumber': int(apartamento['nº mesillas']) if apartamento['nº mesillas'] else None,
            'windowsNumber': int(apartamento['nº ventanas']) if apartamento['nº ventanas'] else None,
            'bathroomsNumber': float(apartamento['nº cuartos de baño ']) if apartamento['nº cuartos de baño '] else None,
            'roomsNumber': int(apartamento['nº habitaciones']) if apartamento['nº habitaciones'] else None,
            'minimumMonthsNumber': int(apartamento['Estacia minima (meses)']) if apartamento['Estacia minima (meses)'] else None,
            'depositMonthsNumber': int(apartamento['Meses de fianza']) if apartamento['Meses de fianza'] else None,
            'area': float(apartamento['Metros cuadrados']) if apartamento['Metros cuadrados'] else None
        }
    }
    response = send_post_request(f'{STRAPI_URL_ZONES}', data, TOKEN)
    if response and 'data' in response and 'id' in response['data']:
        print(f'Apartamento subido con éxito: {apartamento_key}, ID: {response["data"]["id"]}')
        return response['data']['id']
    else:
        print(f'Error al subir el apartamento: {response}')
        return None

# Subir los edificios y obtener sus IDs
print('Subiendo edificios...')
edificio_ids = {}
for edificio in edificios:
    edificio_id = subir_edificio(edificio)
    if edificio_id:
        edificio_ids[edificio['nombre']] = edificio_id

# Subir los apartamentos y asociarlos con los edificios
print('Subiendo apartamentos...')
for apartamento_key, apartamento in apartamentos.items():
    edificio_nombre = apartamento.get('Edificio al que pertenece')
    if edificio_nombre in edificio_ids:
        subir_apartamento(apartamento_key, apartamento, edificio_ids[edificio_nombre])
    else:
        print(f'Edificio no encontrado para el apartamento: {apartamento_key}')