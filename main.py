import os
from core.gestor_datos import inicializar_sistema, guardar_analisis, listar_artistas, analizar_biblioteca_artista
from interfaz.entradas import capturar_portapapeles, seleccionar_archivo_local, pedir_metadatos
from core.analizador import limpiar_texto, obtener_sentimiento, generar_tags, obtener_top_palabras
from interfaz.visual import crear_nube_palabras, mostrar_dashboard
from core.estadisticas import obtener_resumen_temporal

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
                    palabras_limpias = limpiar_texto(letra)
                    score = obtener_sentimiento(letra)
                    top_10 = obtener_top_palabras(palabras_limpias)
                    tags = generar_tags(score)

                    guardar_analisis(artista, titulo, letra, score)

                    print(f"\nANÁLISIS COMPLETADO: {tags}")
                    mostrar_dashboard(score, top_10)
                    crear_nube_palabras(top_10, artista)

        elif opcion == "3":
            artistas = listar_artistas()
            if not artistas:
                print("\n[!] Tu biblioteca está vacía.")
            else:
                print("\n--- Artistas en tu Biblioteca ---")
                for i, art in enumerate(artistas, 1):
                    print(f"{i}. {art}")
                
                # El usuario elige un artista por número
                try:
                    eleccion = int(input("\nElige un artista (número): "))
                    if eleccion < 1 or eleccion > len(artistas):
                        print("[!] Número fuera de rango.")
                    else:
                        artista_elegido = artistas[eleccion - 1]
                        print(f"\n[⏳] Analizando biblioteca de {artista_elegido}...")

                        # Obtener datos de toda la biblioteca del artista
                        texto_combinado, num_canciones, mood_medio = analizar_biblioteca_artista(artista_elegido)

                        if not texto_combinado:
                            print("[!] No se encontraron canciones para este artista.")
                        else:
                            # Mostrar estadísticas agregadas
                            vibe = "Positiva" if mood_medio > 0.1 else "Melancólica" if mood_medio < -0.1 else "Neutral"
                            print(f"\n{'='*35}")
                            print(f"  📚 Biblioteca de {artista_elegido}")
                            print(f"{'='*35}")
                            print(f"  🎵 Canciones guardadas : {num_canciones}")
                            print(f"  🎭 Vibe media          : {vibe} ({mood_medio:.2f})")
                            print(f"{'='*35}")

                            # Generar nube de palabras maestra
                            palabras_maestras = limpiar_texto(texto_combinado)
                            top_maestro = obtener_top_palabras(palabras_maestras, top=50)

                            if top_maestro:
                                print("\n[🎨] Generando Nube Maestra de Palabras...")
                                crear_nube_palabras(top_maestro, f"{artista_elegido}_MAESTRO")
                            else:
                                print("[!] No hay suficiente texto para generar la nube.")

                except ValueError:
                    print("[!] Por favor, introduce un número válido.")

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