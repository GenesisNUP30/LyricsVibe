import os
from core.gestor_datos import inicializar_sistema, guardar_analisis
from interfaz.entradas import capturar_portapapeles, seleccionar_archivo_local, pedir_metadatos
from core.analizador import limpiar_texto, obtener_sentimiento, generar_tags, obtener_top_palabras
from interfaz.visual import crear_nube_palabras, mostrar_dashboard
from core.estadisticas import obtener_resumen_temporal
from core.gestor_datos import listar_artistas

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
                    palabras_limpias = limpiar_texto(letra)
                    score = obtener_sentimiento(letra)
                    top_10 = obtener_top_palabras(palabras_limpias)
                    tags = generar_tags(score)
                    
                    # GUARDAR
                    guardar_analisis(artista, titulo, letra, score)
                    
                    # MOSTRAR RESULTADOS
                    print(f"\nANÁLISIS COMPLETADO: {tags}")
                    mostrar_dashboard(score, top_10)
                    crear_nube_palabras(top_10, artista)

        elif opcion == "2":
            letra = seleccionar_archivo_local()
            if letra:
                artista, titulo = pedir_metadatos()
                if artista and titulo:
                    guardar_analisis(artista, titulo, letra, 0.0)
                    print(f"\n[✓] Archivo guardado correctamente.")

        elif opcion == "3":
            artistas = listar_artistas()
            if not artistas:
                print("\n[!] Tu biblioteca está vacía.")
            else:
                print("\n--- Artistas en tu Biblioteca ---")
                for i, art in enumerate(artistas, 1):
                    print(f"{i}. {art}")
                    # Se podria añadir lógica para analizar la carpeta entera

        elif opcion == "4":
            print("\n¿Qué periodo quieres consultar?")
            print("1. Última semana (7 días)")
            print("2. Último mes (30 días)")
            sub_opcion = input("Elige: ")
            
            dias = 7 if sub_opcion == "1" else 30
            print(obtener_resumen_temporal(dias))

        elif opcion == "5":
            print("\n¡Gracias por usar LyricsVibe! Hasta pronto.")
            break
        else:
            print("\n[!] Opción no válida.")

if __name__ == "__main__":
    main()