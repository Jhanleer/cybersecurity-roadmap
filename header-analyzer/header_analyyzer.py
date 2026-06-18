import requests
import argparse
def main():
    parser=argparse.ArgumentParser(description="Header analyzer")

    parser.add_argument("url", help="Colocar una URL")

    parser.add_argument("-t","--timeout", type=float, default=1.0, help="Timeout para la url en segundos")

    args=parser.parse_args()

    print(args.url)
    print(args.timeout)

    try:
        r= requests.get(args.url, timeout= args.timeout)
         
        print("Analizando: ",args.url)
     
        print("Estado: ",r.status_code)
        header_seguridad=["Strict-Transport-Security","Content-Security-Policy","X-Frame-Options", "X-Content-Type-Options", "Referrer-Policy", "Permissions-Policy"]
        f=0
        
        for u in header_seguridad:
            ur=r.headers.get(u)
            if ur is None:
                print("[-]",u,"Ausente")
            
            else:
                print("[+]",u, "Presente")
                f +=1
                
        print(f"Resultado: {f}/{len(header_seguridad)}")
    except requests.exceptions.ConnectionError:
        print("No se pudo conectar — el sitio no existe o está caído")
    except requests.exceptions.Timeout:
        print("El servidor tardó demasiado en responder")
    except requests.exceptions.InvalidURL:
        print("La URL no es válida")
    except requests.exceptions.RequestException as e:
        print(f"Error general: {e}")


if __name__ == "__main__":
    main()
