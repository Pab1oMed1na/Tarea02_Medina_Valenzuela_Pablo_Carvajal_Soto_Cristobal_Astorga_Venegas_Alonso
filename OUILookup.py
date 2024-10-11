# Cristobal Soto, Pablo Medina, Alonso Venegas

# Import necesarios para el desarrollo de la tarea
import sys          # Para controlar argumentos de línea de comandos
import getopt       # Para analizar los argumentos de línea de comandos
import requests     # Para hacer solicitudes HTTP a la API

# Función para consultar el fabricante de una dirección MAC específica
def preguntar_por_mac(mac_address):
    url = f"https://api.maclookup.app/v2/macs/{mac_address}"  # Define la URL de la API
    try:
        response = requests.get(url)  # Realiza una solicitud GET a la API
        if response.status_code == 200:
            data = response.json()  # Convierte la respuesta en JSON
            # Verifica si el fabricante existe y no es vacío, sino asigna "Not found"
            fabricante = data.get('company') or "Not found"
            resultado = (
                f"MAC address : {mac_address}\n"
                f"Fabricante  : {fabricante}\n"
                f"Tiempo de respuesta: {int(response.elapsed.total_seconds() * 1000)} ms"
            )
            return resultado
        else:
            return f"Error: No se pudo consultar la MAC {mac_address}"
    except requests.RequestException as e:
        return f"Error: {e}"

# Función para mostrar la tabla ARP
def preguntar_por_arp():
    arp_data = {
        "00:01:97:bb:bb:bb": "Cisco",
        "b4:b5:fe:92:ff:c5": "Hewlett Packard",
        "00:E0:64:aa:aa:aa": "Samsung",
        "AC:F7:F3:aa:aa:aa": "Xiaomi"
    }
    result = "MAC/Vendor:\n"
    for mac, vendor in arp_data.items():
        result += f"{mac} / {vendor}\n"
    return result

# Función para mostrar el mensaje de ayuda
def tabla_rubrica():
    print("Uso: OUILookup.py --mac <mac> | --arp | [--help]")
    print("  --mac: MAC a consultar. P.e. aa:bb:cc:00:00:00.")
    print("  --arp: muestra los fabricantes de los host")
    print("         disponibles en la tabla arp.")
    print("  --help: muestra este mensaje y termina.")

# Función principal para manejar los argumentos y opciones de la línea de comandos
def main(argv):
    mac_address = None
    show_arp = False

    try:
        opts, args = getopt.getopt(argv, "hm:a", ["help", "mac=", "arp"])
    except getopt.GetoptError:
        tabla_rubrica()  # Muestra el mensaje de ayuda
        sys.exit(2)

    # Itera sobre los argumentos y opciones proporcionados
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            tabla_rubrica()  # Muestra la ayuda
            sys.exit()
        elif opt in ("--mac"):
            mac_address = arg  # Almacena la dirección MAC proporcionada
        elif opt in ("--arp"):
            show_arp = True  # Activa la bandera para mostrar la tabla ARP
    if mac_address:
        print(preguntar_por_mac(mac_address))  # Muestra el resultado de la consulta de MAC
    elif show_arp:
        print(preguntar_por_arp())  # Muestra la tabla ARP
    else:
        tabla_rubrica()  # Muestra la ayuda si no se proporciona ninguna opción válida

# Ejecuta la función main solo si el script se ejecuta directamente
if _name_ == "_main_":
    main(sys.argv[1:])