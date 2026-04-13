import os
from core.gestor_datos import inicializar_sistema, guardar_analisis
from interfaz.entradas import capturar_portapapeles, seleccionar_archivo_local, pedir_metadatos

def mostrar_menu():
    print("\n" + "="*30)
    print("      LYRICSVIBE 🎵")
    print("="*30)
    print("1. 🎵 Analizar desde Portapapeles")
    print("2. 📁 Importar archivo .txt")
    print("3. 📚 Mi Biblioteca (Artistas)")
    print("4. 📈 Panel de Estadísticas")
    print("5. ❌ Salir")
    return input("\nElige una opción: ")

def main():
    # FASE 1: Arranque
    inicializar_sistema()
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            letra = capturar_portapapeles()
            if letra:
                artista, titulo = pedir_metadatos()
                if artista and titulo:
                    # Por ahora usamos un mood de 0.0 hasta que hagamos el analizador
                    guardar_analisis(artista, titulo, letra, 0.0)
                    print(f"\n[✓] '{titulo}' de {artista} guardado en la biblioteca.")

        elif opcion == "2":
            letra = seleccionar_archivo_local()
            if letra:
                artista, titulo = pedir_metadatos()
                if artista and titulo:
                    guardar_analisis(artista, titulo, letra, 0.0)
                    print(f"\n[✓] Archivo guardado correctamente.")

        elif opcion == "3":
            print("\n[Próximamente] Navegación por biblioteca...")

        elif opcion == "4":
            print("\n[Próximamente] Estadísticas temporales...")

        elif opcion == "5":
            print("\n¡Gracias por usar LyricsVibe! Hasta pronto.")
            break
        else:
            print("\n[!] Opción no válida.")

if __name__ == "__main__":
    main()